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

# normfactors = common_plot.normfactors
# normfactors.update({'TpTp' : 1.})

datasets_to_plot = common_datasets_to_plot = [
    # 'Run2015B',
    'TpTp_M-800_thth',
    'TpTp_M-800_thtz',
    'TpTp_M-800_thbw',
    'TpTp_M-1600_thth',
    'TpTp_M-1600_thtz',
    'TpTp_M-1600_thbw',
    'QCD',
    'TTbar',
    'WJets',
    'ZJets',
    'SingleT',
]



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

def rebin_st_hists(wrps):
    for w in wrps:
        if w.variable == 'ST':
            w.histo.Rebin(2)
        yield w


def mod_legend(wrps):
    for w in wrps:
        for m in ['800', '1600']:
            if m in w.legend:
                w.legend = "T'T' M"+m
        yield w


def loader_hook_final(wrps, smpl_fct=None):
    wrps = final_plotting.loader_hook_norm_smpl(wrps, smpl_fct)
    wrps = rebin_st_hists(wrps)
    wrps = mod_legend(wrps)
    return wrps

def plotter_factory_final(smpl_fct=None, **kws):
    # kws['filter_keyfunc'] = lambda w: 'TH' in w.type
    kws['hook_loaded_histos'] = lambda w: loader_hook_final(w, smpl_fct)
    kws['plot_setup'] = final_plotting.stack_setup_norm_sig
    kws['stack_setup'] = final_plotting.stack_setup_norm_sig
    # kws['canvas_decorators'] += [rnd.TitleBox(text='CMS Simulation 20fb^{-1} @ 13TeV')]
    kws['save_lin_log_scale'] = True
    # kws['canvas_decorators'] = [varial.rendering.Legend]
    return varial.tools.Plotter(**kws)

def filter_for_fsp(w):
    if (('DATA' not in w.file_path and w.in_file_path.endswith('ST'))
        )\
        and ('PostSelection' in w.in_file_path):
        return True
    else:
        return False

def mk_tools_cats(categories=None):
    def create():
        plot_chain = [
            
            varial.tools.mk_rootfile_plotter(
                pattern=common_plot.file_selected_split(datasets_to_plot),
                name='StackedAll',
                filter_keyfunc=filter_for_fsp,
                plotter_factory=lambda **w: plotter_factory_final(common_plot.normfactors, **w),
                combine_files=True,
                # filter_keyfunc=lambda w: 'Cutflow' not in w.in_file_path
                ),
            # varial.tools.mk_rootfile_plotter(
            #     pattern=common_plot.file_no_signals(),
            #     name='NormedNoSignals',
            #     plotter_factory=lambda **w: final_plotting.plotter_factory_norm(**w),
            #     combine_files=True,
            #     # filter_keyfunc=lambda w: 'Cutflow' not in w.in_file_path
            #     ),
            # varial.tools.mk_rootfile_plotter(
            #     pattern=common_plot.file_split_signals(),
            #     name='NormedSignals',
            #     plotter_factory=lambda **w: final_plotting.plotter_factory_norm(**w),
            #     combine_files=True,
            #     # filter_keyfunc=lambda w: 'Cutflow' not in w.in_file_path
            #     ),
            
            ]
        cutflow_cat = []
        for cat in categories:
            cutflow_cat.append(mk_cutflow_chain_cr(
                cat,
                common_plot.loader_hook))
        plot_chain.append(varial.tools.ToolChain('CutflowTools', cutflow_cat))

        return plot_chain
    return create


#====SFRAME====

dir_limit = 'Limits3fb_2'

sframe_cfg = '/nfs/dust/cms/user/nowatsd/sFrameNew/CMSSW_7_4_7/src/UHH2/VLQToHiggsPairProd/config/TpTpFinalSelection.xml'

def mk_sframe_and_plot_tools(analysis_module='', version='TestFinal', count=-1,
                allowed_datasets = [], signal_regions=[], control_regions=[]):
    """Makes a toolchain for one category with sframe and plots."""
    sframe = SFrame(
        cfg_filename=sframe_cfg,
        xml_tree_callback=common_sframe.set_category_datasets_eventnumber_and_split(
            catname=' '.join(signal_regions+control_regions),
            count=count, allowed_datasets=allowed_datasets,
            analysis_module=analysis_module
        ), # 
    )
    plots = varial.tools.ToolChainParallel(
        'Plots_for_fsp2',
        lazy_eval_tools_func=mk_tools_cats(signal_regions+control_regions)
    )
    tc_list = [
        sframe,
        plots
    ]
    if analysis_module == 'TpTpControlRegion':
        tc_list.append(varial.tools.ToolChain(
                'CompareControlRegion2',
                lazy_eval_tools_func=compare_crs.mk_tc(
                    srs=signal_regions, crs=control_regions)
                ))
    elif analysis_module == 'TpTpFinalSelectionRunII':
        tc_list.append(sensitivity.mk_tc(dir_limit))

    tc_list.append(varial.tools.WebCreator(no_tool_check=True))

    tc = varial.tools.ToolChain(version, tc_list)
    return tc