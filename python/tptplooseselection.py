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
import common_sframe 

#====PLOTTING====

def mk_tools():

    return [
        varial.tools.mk_rootfile_plotter(
            pattern=common_plot.file_stack_less_signal_split(),
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
        cutflow_tables.mk_cutflow_chain(common_plot.file_stack_all_split(), common_plot.loader_hook)
        ]


#====SFRAME====

sframe_cfg = '/nfs/dust/cms/user/nowatsd/sFrameNew/CMSSW_7_4_7/src/UHH2/VLQToHiggsPairProd/config/TpTpLooseSelection.xml'

tptp_loose_datasets = [
    'Run2015B_Ele',
    'Run2015B_Mu',
    'Run2015B_Had',
    # 'TpTp_M-700',
    'TpTp_M-800',
    # 'TpTp_M-900',
    # 'TpTp_M-1000',
    # 'TpTp_M-1100',
    # 'TpTp_M-1200',
    # 'TpTp_M-1300',
    # 'TpTp_M-1400',
    # 'TpTp_M-1500',
    'TpTp_M-1600',
    # 'TpTp_M-1700',
    # 'TpTp_M-1800',
    # 'QCD_Pt15to30',
    # 'QCD_Pt30to50',
    # 'QCD_Pt50to80',
    'QCD_Pt80to120',
    'QCD_Pt120to170',
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

def mk_sframe_and_plot_tools(version='TestLoose', count=-1):
    """Makes a toolchain for one category with sframe and plots."""
    sframe = SFrame(
        cfg_filename=sframe_cfg,
        xml_tree_callback=common_sframe.set_eventnumber_datasets_and_split(count=count, allowed_datasets=tptp_loose_datasets), # 
    )
    plots = varial.tools.ToolChainParallel(
        'Plots_more_signals',
        lazy_eval_tools_func=mk_tools
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