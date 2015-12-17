#!/usr/bin/env python

import sys
import os
import time

import varial.tools
import varial.generators as gen
import varial.analysis as analysis
from varial.sample import Sample
from varial.extensions.sframe import SFrame

import UHH2.VLQSemiLepPreSel.cutflow_tables as cutflow_tables

# import common_vlq
import tptp_settings
import final_plotting
import common_plot
import tptp_sframe
# import analysis

#====PLOTTING====

file_path = '/nfs/dust/cms/user/tholenhe/VLQSemiLepPreSel/Run2-ntuple/'

datasets_to_plot = [
    'Run2015D',
    'TpTp_M-800',
    'TpTp_M-1600',
    'QCD',
    'TTbar',
    'WJets',
    'ZJets',
    'SingleT',
]

# def file_pattern(allowed_datasets=None):
#     file_list = list(file_path+'uhh2.AnalysisModuleRunner.'+g+'.root' for g in allowed_datasets)
#     print file_list
#     return file_list

def mk_tools(datasets_to_plot=None):
    def create():

        return [
            varial.tools.mk_rootfile_plotter(
                pattern=common_plot.file_selected_unsplit(datasets_to_plot, file_path),
                name='StackedAll',
                plotter_factory=lambda **w: final_plotting.plotter_factory_stack({'TpTp' : 10.}, **w),
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
            cutflow_tables.mk_cutflow_chain(common_plot.file_selected_unsplit(datasets_to_plot, file_path), common_plot.loader_hook)
            ]
    return create

#====SFRAME====

# sframe_cfg = '/nfs/dust/cms/user/nowatsd/sFrameNew/CMSSW_7_4_7/src/UHH2/VLQToHiggsPairProd/config/TpTpLooseSelection.xml'

def mk_sframe_and_plot_tools(version='TestPre', allowed_datasets=None):
    """Makes a toolchain for one category with sframe and plots."""
    # sframe = SFrame(
    #     cfg_filename=sframe_cfg,
    #     xml_tree_callback=tptp_sframe.set_eventnumber_datasets_and_split(count=count, allowed_datasets=allowed_datasets), # 
    # )
    plots = varial.tools.ToolChainParallel(
        'Plots',
        lazy_eval_tools_func=mk_tools(allowed_datasets)
    )
    tc = varial.tools.ToolChain(
        version,
        [
            # sframe,
            plots,
            varial.tools.WebCreator(no_tool_check=True)
        ]
    )
    return tc

# sframe_tools = mk_sframe_and_plot_tools()


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