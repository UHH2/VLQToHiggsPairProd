#!/usr/bin/env python

import sys
import os
import time

import varial.settings
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
import common_sframe 

varial.settings.use_parallel_chains = False


#====PLOTTING====

datasets_to_plot = [
    'Run2015D',
    'TpTp_M-800_thth',
    'TpTp_M-800_thtz',
    'TpTp_M-800_thbw',
    'TpTp_M-1600_thth',
    'TpTp_M-1600_thtz',
    'TpTp_M-1600_thbw',
    'QCD',
    'TTbar',
    'WJets',
    'DYJets',
    'SingleT',
]

test_list = [
            'uhh2.AnalysisModuleRunner.MC.QCD_Pt1000toInf_MuEnr.root',
            'uhh2.AnalysisModuleRunner.MC.TpTp_M-1600.root',
            'uhh2.AnalysisModuleRunner.MC.TpTp_M-1000.root',
            'uhh2.AnalysisModuleRunner.MC.TpTp_M-800.root'
            ]

def mk_tools():

    return [
        varial.tools.mk_rootfile_plotter(
            # pattern=common_plot.file_selected_split(datasets_to_plot),
            pattern=test_list,
            name='StackedAll',
            plotter_factory=lambda **w: final_plotting.plotter_factory_stack(common_plot.normfactors, **w),
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
        cutflow_tables.mk_cutflow_chain(test_list, common_plot.loader_hook)
        ]


#====SFRAME====

sframe_cfg = '/nfs/dust/cms/user/nowatsd/sFrameNew/CMSSW_7_4_9/src/UHH2/VLQToHiggsPairProd/config/TpTpLooseSelection.xml'

def mk_sframe_and_plot_tools(version='TestLoose', count=-1, allowed_datasets=None):
    """Makes a toolchain for one category with sframe and plots."""
    sframe = SFrame(
        cfg_filename=sframe_cfg,
        xml_tree_callback=common_sframe.set_datasets_eventnumber_and_split_loose(count=count, allowed_datasets=allowed_datasets), # 
    )
    plots = varial.tools.ToolChainParallel(
        'Plots',
        lazy_eval_tools_func=mk_tools
    )
    tc = varial.tools.ToolChain(
        version,
        [
            sframe,
            plots,
            varial.tools.WebCreator(no_tool_check=True)
        ]
    )
    return tc

# sframe_tools = mk_sframe_and_plot_tools()

import sys

if __name__ == '__main__':
    time.sleep(1)
    final_dir = sys.argv[1]
    all_tools = mk_tools()
    # tc = varial.tools.ToolChainParallel(
    tc = varial.tools.ToolChain(
        final_dir, all_tools)
    varial.tools.Runner(tc)
    varial.tools.WebCreator(no_tool_check=True).run()   
    # for itool in all_tools:
    #     dir_name = os.path.join('./'+final_dir, itool.name)
    #     print dir_name
    #     varial.tools.WebCreator(working_dir=dir_name).run()
    # varial.tools.CopyTool('~/www/vlq_analysis/tight_selection2/',
    #     src=final_dir, use_rsync=True).run()