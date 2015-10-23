#!/usr/bin/env python

import os
import sys
import time

from ROOT import TH1F

import varial.tools
import varial.generators as gen
import varial.analysis as analysis
from varial.sample import Sample
from varial.extensions.sframe import SFrame
import varial.rendering as rnd

import UHH2.VLQSemiLepPreSel.cutflow_tables as cutflow_tables

# import common_vlq
import common_plot
import compare_crs
import tptp_settings
import final_plotting
import sensitivity
import common_sframe


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

def rebin_hists(wrps, hist_name='', factor=2):
    for w in wrps:
        if w.variable == hist_name:
            w.histo.Rebin(factor)
        yield w


def resize_n_hists(wrps):
    for w in wrps:
        if 'n_toptags' in w.in_file_path:
            # w.histo.SetAxisRange(-0.5, 4.5, "X")
            histo = TH1F(w.histo.GetName(), w.histo.GetTitle(), 5, -.5, 4.5)
            for i in range(0, 5):
                histo.SetBinContent(i, w.histo.GetBinContent(i))
            w.histo = histo
        yield w

def nice_axis_labels(wrps):
    for w in wrps:
        if 'n_toptags' in w.in_file_path:
            # w.histo.SetAxisRange(-0.5, 4.5, "X")
            w.histo.GetXaxis().SetTitle('N(top-tags)')
        elif 'n_ak8_boost_loose_2b_m60-150_noT' in w.in_file_path:
            # w.histo.SetAxisRange(-0.5, 4.5, "X")
            w.histo.GetXaxis().SetTitle('N(higgs-tags)')
        elif 'pt_ld_ak8_all_loose_2b_m60-150_noT' in w.in_file_path:
            # w.histo.SetAxisRange(-0.5, 4.5, "X")
            w.histo.GetXaxis().SetTitle('p_{T}(Higgs candidate)')
        elif 'n_ak8_all' in w.in_file_path:
            # w.histo.SetAxisRange(-0.5, 4.5, "X")
            w.histo.GetXaxis().SetTitle('N(Ak8 jets)')
        elif 'mass_sj_ld_ak8_boost_loose_2b' in w.in_file_path:
            # w.histo.SetAxisRange(-0.5, 4.5, "X")
            w.histo.GetXaxis().SetTitle('M(Higgs candidate)')
        yield w


def mod_legend(wrps):
    for w in wrps:
        for m in ['800', '1600']:
            if m in w.legend:
                w.legend = "T'T' M"+m
        yield w


def loader_hook_tight(wrps, smpl_fct=None):
    wrps = resize_n_hists(wrps)
    wrps = final_plotting.loader_hook_norm_smpl(wrps, smpl_fct)
    # wrps = rebin_hists(wrps, 'primary_lepton_pt', 2)
    wrps = nice_axis_labels(wrps)
    wrps = mod_legend(wrps)
    return wrps

def plotter_factory_tight(smpl_fct=None, **kws):
    # kws['filter_keyfunc'] = lambda w: 'TH' in w.type
    kws['hook_loaded_histos'] = lambda w: loader_hook_tight(w, smpl_fct)
    kws['plot_setup'] = final_plotting.stack_setup_norm_sig
    kws['stack_setup'] = final_plotting.stack_setup_norm_sig
    kws['canvas_decorators'] += [rnd.TitleBox(text='552.67 fb^{-1} @ 13TeV')]
    kws['save_lin_log_scale'] = True
    # kws['canvas_decorators'] = [varial.rendering.Legend]
    return varial.tools.Plotter(**kws)


def filter_for_fsp(w):
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
            pattern=common_plot.file_selected_unsplit(datasets_to_plot),
            name='StackedAll',
            # filter_keyfunc=filter_for_fsp,
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
        cutflow_tables.mk_cutflow_chain(common_plot.file_selected_unsplit(datasets_to_plot), common_plot.loader_hook)
        ]


#====SFRAME====

sframe_cfg = '/nfs/dust/cms/user/nowatsd/sFrameNew/CMSSW_7_4_9/src/UHH2/VLQToHiggsPairProd/config/TpTpTightSelectionRunII.xml'

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
        'Plots',
        lazy_eval_tools_func=mk_tools
    )
    tc_list = [
        # sframe,
        plots,
        varial.tools.WebCreator(no_tool_check=True)
    ]

    tc = varial.tools.ToolChain(version, tc_list)
    return tc



