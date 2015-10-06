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

datasets_to_plot = common_datasets_to_plot = [
    'Run2015B',
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


def resize_n_hists(wrps):
    for w in wrps:
        if w.variable.startswith('n_toptags'):
            w.histo.GetXaxis().SetRange(0, 5)
        yield w


def mod_legend(wrps):
    for w in wrps:
        for m in ['800', '1600']:
            if m in w.legend:
                w.legend = "T'T' M"+m
        yield w


def loader_hook_tight(wrps, smpl_fct=None):
    wrps = final_plotting.loader_hook_norm_smpl(wrps, smpl_fct)
    wrps = resize_n_hists(wrps)
    wrps = mod_legend(wrps)
    return wrps

def plotter_factory_tight(smpl_fct=None, **kws):
    # kws['filter_keyfunc'] = lambda w: 'TH' in w.type
    kws['hook_loaded_histos'] = lambda w: loader_hook_tight(w, smpl_fct)
    kws['plot_setup'] = final_plotting.stack_setup_norm_sig
    kws['stack_setup'] = final_plotting.stack_setup_norm_sig
    # kws['canvas_decorators'] += [rnd.TitleBox(text='CMS Simulation 20fb^{-1} @ 13TeV')]
    kws['save_lin_log_scale'] = True
    # kws['canvas_decorators'] = [varial.rendering.Legend]
    return varial.tools.Plotter(**kws)


def filter_h_mass_plot(w):
    if (('DATA' not in w.file_path and w.in_file_path.endswith('mass_sj_ld_ak8_boost_loose_2b'))
        or (w.in_file_path.endswith('ST'))
        or ('n_toptags_boost' in w.in_file_path)
        or ('n_ak8_all' in w.in_file_path)
        )\
        and ('OnlySTCut' in w.in_file_path):
        return True
    else:
        return False


def mk_tools():

    return [
        varial.tools.mk_rootfile_plotter(
            pattern=common_plot.file_selected_split(datasets_to_plot),
            name='StackedAll',
            filter_keyfunc=filter_h_mass_plot,
            plotter_factory=lambda **w: plotter_factory_tight(common_plot.normfactors, **w),
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
        cutflow_tables.mk_cutflow_chain(common_plot.file_stack_all_split(), common_plot.loader_hook)
        ]


#====SFRAME====

sframe_cfg = '/nfs/dust/cms/user/nowatsd/sFrameNew/CMSSW_7_4_7/src/UHH2/VLQToHiggsPairProd/config/TpTpTightSelectionRunII.xml'

def mk_sframe_and_plot_tools(version='TestFinal', count=-1,
                allowed_datasets = []):
    """Makes a toolchain for one category with sframe and plots."""
    sframe = SFrame(
        cfg_filename=sframe_cfg,
        xml_tree_callback=common_sframe.set_datasets_eventnumber_and_split(
            count=count, allowed_datasets=allowed_datasets,
        ), # 
    )
    plots = varial.tools.ToolChainParallel(
        'Plots_for_fsp3',
        lazy_eval_tools_func=mk_tools
    )
    tc_list = [
        sframe,
        plots,
        varial.tools.WebCreator(no_tool_check=True)
    ]

    tc = varial.tools.ToolChain(version, tc_list)
    return tc



