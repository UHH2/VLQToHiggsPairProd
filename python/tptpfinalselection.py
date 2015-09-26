#!/usr/bin/env python

import os
import sys
import time

import varial.tools
import varial.generators as gen
import varial.analysis as analysis
from varial.sample import Sample
from varial.extensions.sframe import SFrame

import UHH2.VLQSemiLepPreSel.cutflow_tables as cutflow_tables

# import common_vlq
import common_plot
import compare_crs
import tptp_settings
import final_plotting
import sensitivity
import common_sframe

#====PLOTTING====

def mk_cutflow_chain_cr(category, loader_hook):
    cutflow_histos = varial.tools.HistoLoader(
        name='CutflowHistos',
        # pattern=input_pat,
        filter_keyfunc=lambda w: 'cutflow' == w.in_file_path.split('/')[-1] and\
                       category == w.in_file_path.split('/')[0],
        hook_loaded_histos=lambda w: cutflow_tables.gen_rebin_cutflow(loader_hook(w))
    )

    cutflow_stack_plots = varial.tools.Plotter(
        'CutflowStack',
        stack=True,
        input_result_path='../CutflowHistos',
        save_log_scale=True,
        canvas_decorators=[varial.rendering.Legend]
    )

    # cutflow_normed_plots = varial.tools.Plotter(
    #     'CutflowNormed',
    #     stack=False,
    #     plot_grouper=varial.plotter.plot_grouper_by_in_file_path,
    #     hook_loaded_histos=gen.gen_norm_to_max_val,
    #     input_result_path='../CutflowHistos',
    #     save_log_scale=True,
    #     canvas_decorators=[varial.rendering.Legend]
    # )

    return varial.tools.ToolChain(category, [
        cutflow_histos,
        cutflow_stack_plots,
        # cutflow_normed_plots,
        cutflow_tables.CutflowTableContent(),
        cutflow_tables.CutflowTableTxt(),
        cutflow_tables.CutflowTableTex(None, True),
    ])

def mk_tools_cats(categories=None):
    def create():
        plot_chain = [
            
            varial.tools.mk_rootfile_plotter(
                pattern=common_plot.file_stack_all_unsplit(),
                name='StackedAll',
                plotter_factory=lambda **w: final_plotting.plotter_factory_stack(common_plot.normfactors, **w),
                combine_files=True,
                # filter_keyfunc=lambda w: 'Cutflow' not in w.in_file_path
                ),
            varial.tools.mk_rootfile_plotter(
                pattern=common_plot.file_no_signals(),
                name='NormedNoSignals',
                plotter_factory=lambda **w: final_plotting.plotter_factory_norm(**w),
                combine_files=True,
                # filter_keyfunc=lambda w: 'Cutflow' not in w.in_file_path
                ),
            varial.tools.mk_rootfile_plotter(
                pattern=common_plot.file_split_signals(),
                name='NormedSignals',
                plotter_factory=lambda **w: final_plotting.plotter_factory_norm(**w),
                combine_files=True,
                # filter_keyfunc=lambda w: 'Cutflow' not in w.in_file_path
                ),
            
            ]
        cutflow_cat = []
        for cat in categories:
            cutflow_cat.append(mk_cutflow_chain_cr(
                cat,
                common_plot.loader_hook))
        plot_chain.append(varial.tools.ToolChain('CutflowTools', cutflow_cat))

        return plot_chain
    return create

def mk_tools():

    return [
        varial.tools.mk_rootfile_plotter(
            pattern=common_plot.file_stack_all_unsplit(),
            name='StackedAll',
            plotter_factory=lambda **w: final_plotting.plotter_factory_stack(common_plot.normfactors, **w),
            combine_files=True,
            # filter_keyfunc=lambda w: 'Cutflow' not in w.in_file_path
            ),
        varial.tools.mk_rootfile_plotter(
            pattern=common_plot.file_no_signals(),
            name='NormedNoSignals',
            plotter_factory=lambda **w: final_plotting.plotter_factory_norm(**w),
            combine_files=True,
            # filter_keyfunc=lambda w: 'Cutflow' not in w.in_file_path
            ),
        varial.tools.mk_rootfile_plotter(
            pattern=common_plot.file_split_signals(),
            name='NormedSignals',
            plotter_factory=lambda **w: final_plotting.plotter_factory_norm(**w),
            combine_files=True,
            # filter_keyfunc=lambda w: 'Cutflow' not in w.in_file_path
            ),
        cutflow_tables.mk_cutflow_chain(common_plot.file_stack_all_unsplit(), common_plot.loader_hook)
        ]


#====SFRAME====

tptp_tight_datasets = [
    'Run2015B_Ele',
    'Run2015B_Mu',
    'Run2015B_Had',
    # 'TpTp_M-700',
    'TpTp_M-800',
    'TpTp_M-900',
    'TpTp_M-1000',
    'TpTp_M-1100',
    # 'TpTp_M-1200',
    'TpTp_M-1300',
    # 'TpTp_M-1400',
    # 'TpTp_M-1500',
    'TpTp_M-1600',
    # 'TpTp_M-1700',
    # 'TpTp_M-1800',
    # 'QCD_Pt15to30',
    # 'QCD_Pt30to50',
    # 'QCD_Pt50to80',
    # 'QCD_Pt80to120',
    # 'QCD_Pt120to170',
    'QCD_Pt170to300',
    'QCD_Pt300to470',
    'QCD_Pt470to600',
    'QCD_Pt600to800',
    'QCD_Pt800to1000',
    'QCD_Pt1000to1400',
    'QCD_Pt1400to1800',
    'QCD_Pt1800to2400',
    'QCD_Pt2400to3200',
    'QCD_Pt3200toInf',
    # 'TTbar',
    'TTbar_Mtt0to700',
    'TTbar_Mtt700to1000',
    'TTbar_Mtt1000toInf',
    'WJets',
    'ZJetsM10to50',
    'ZJetsM50toInf',
    'SingleT_tChannel',
    'SingleT_WAntitop',
    'SingleT_WTop',
]

sframe_cfg = '/nfs/dust/cms/user/nowatsd/sFrameNew/CMSSW_7_4_7/src/UHH2/VLQToHiggsPairProd/config/TpTpFinalSelection.xml'

def mk_sframe_and_plot_tools(analysis_module='', version='TestFinal', count=-1,
                signal_regions=[], control_regions=[]):
    """Makes a toolchain for one category with sframe and plots."""
    sframe = SFrame(
        cfg_filename=sframe_cfg,
        xml_tree_callback=common_sframe.set_category_datasets_eventnumber_and_split(
            catname=' '.join(signal_regions+control_regions),
            count=count, allowed_datasets=tptp_tight_datasets,
            analysis_module=analysis_module
        ), # 
    )
    plots = varial.tools.ToolChainParallel(
        'Plots_more_signals',
        # lazy_eval_tools_func=mk_tools_cats(signal_regions+control_regions)
        lazy_eval_tools_func=mk_tools
    )
    tc_list = [
        sframe,
        plots
    ]
    if analysis_module == 'TpTpControlRegion':
        tc_list.append(varial.tools.ToolChain(
                'CompareControlRegion',
                lazy_eval_tools_func=compare_crs.mk_tc(
                    srs=signal_regions, crs=control_regions)
                ))
    elif analysis_module == 'TpTpFinalSelectionRunII':
        tc_list.append(sensitivity.mk_tc())

    tc_list.append(varial.tools.WebCreator(no_tool_check=True))

    tc = varial.tools.ToolChain(version, tc_list)
    return tc

# sframe_tools_final = mk_sframe_and_plot_tools_final_new()

if __name__ == '__main__':
    time.sleep(1)
    all_tools = mk_tools()
    tc = varial.tools.ToolChain(
        final_dir, all_tools)
    varial.tools.Runner(tc)
    # varial.tools.WebCreator(no_tool_check=True).run()   
    for itool in all_tools:
        dir_name = os.path.join('./'+final_dir, itool.name)
        print dir_name
        varial.tools.WebCreator(working_dir=dir_name).run()
    # varial.tools.CopyTool('~/www/vlq_analysis/tight_selection2/',
    #     src=final_dir, use_rsync=True).run()


# for control regions:

# sframe_cfg_control_region = '/nfs/dust/cms/user/nowatsd/sFrameNew/CMSSW_7_4_7/src/UHH2/VLQToHiggsPairProd/config/TpTpControlRegion.xml'


# def mk_sframe_and_plot_tools_control_region_new():
#     """Makes a toolchain for one category with sframe and plots."""
#     sframe = SFrame(
#         cfg_filename=sframe_cfg,
#         xml_tree_callback=set_category_datasets_eventnumber_and_split(
#             catname=' '.join(signal_regions+control_regions),
#             count="-1", allowed_datasets=tptp_tight_datasets
#         ), # 
#     )
#     plots = varial.tools.ToolChainParallel(
#         'Plots',
#         lazy_eval_tools_func=tight_plot.mk_tools_cats(signal_regions+control_regions)
#     )
#     tc = varial.tools.ToolChain(
#         'FilesAndPlots_v14_moreCrs',
#         [
#             sframe,
#             plots,
#             varial.tools.ToolChain(
#                 'CompareControlRegion',
#                 lazy_eval_tools_func=compare_crs.mk_tc(srs=signal_regions, crs=control_regions)
#                 ),
#             varial.tools.WebCreator(no_tool_check=True)
#         ]
#     )
#     return tc

# sframe_tools_control_region = mk_sframe_and_plot_tools_control_region_new()