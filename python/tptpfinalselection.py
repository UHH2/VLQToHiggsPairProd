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
                pattern=common_plot.file_selected_split(),
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

# def mk_tools():

#     return [
#         varial.tools.mk_rootfile_plotter(
#             pattern=common_plot.file_stack_all_unsplit(),
#             name='StackedAll',
#             plotter_factory=lambda **w: final_plotting.plotter_factory_stack(common_plot.normfactors, **w),
#             combine_files=True,
#             # filter_keyfunc=lambda w: 'Cutflow' not in w.in_file_path
#             ),
#         varial.tools.mk_rootfile_plotter(
#             pattern=common_plot.file_no_signals(),
#             name='NormedNoSignals',
#             plotter_factory=lambda **w: final_plotting.plotter_factory_norm(**w),
#             combine_files=True,
#             # filter_keyfunc=lambda w: 'Cutflow' not in w.in_file_path
#             ),
#         varial.tools.mk_rootfile_plotter(
#             pattern=common_plot.file_split_signals(),
#             name='NormedSignals',
#             plotter_factory=lambda **w: final_plotting.plotter_factory_norm(**w),
#             combine_files=True,
#             # filter_keyfunc=lambda w: 'Cutflow' not in w.in_file_path
#             ),
#         cutflow_tables.mk_cutflow_chain(common_plot.file_stack_all_unsplit(), common_plot.loader_hook)
#         ]


#====SFRAME====

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
        'Plots',
        lazy_eval_tools_func=mk_tools_cats(signal_regions+control_regions)
        # lazy_eval_tools_func=mk_tools
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
