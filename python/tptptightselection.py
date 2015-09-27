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

sframe_cfg = '/nfs/dust/cms/user/nowatsd/sFrameNew/CMSSW_7_4_7/src/UHH2/VLQToHiggsPairProd/config/TpTpTightSelectionRunII.xml'

def mk_sframe_and_plot_tools(version='TestFinal', count=-1,
                allowed_datasets = []):
    """Makes a toolchain for one category with sframe and plots."""
    sframe = SFrame(
        cfg_filename=sframe_cfg,
        xml_tree_callback=common_sframe.set_eventnumber_datasets_and_split(
            count=count, allowed_datasets=allowed_datasets,
        ), # 
    )
    plots = varial.tools.ToolChainParallel(
        'Plots_more_signals',
        # lazy_eval_tools_func=mk_tools_cats(signal_regions+control_regions)
        lazy_eval_tools_func=mk_tools
    )
    tc_list = [
        sframe,
        plots,
        varial.tools.WebCreator(no_tool_check=True)
    ]

    tc = varial.tools.ToolChain(version, tc_list)
    return tc



