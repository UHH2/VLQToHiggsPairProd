#!/usr/bin/env python

import sys
import os
import time
import itertools
import copy

import varial.settings
import varial.tools
import varial.generators as gen
import varial.rendering as rnd
import varial.analysis as analysis
from varial.sample import Sample
# from varial.extensions.sframe import SFrame
from varial.extensions.hadd import Hadd
import varial.wrappers as wrappers
import varial.operations as op

import UHH2.VLQSemiLepPreSel.cutflow_tables as cutflow_tables
import UHH2.VLQSemiLepPreSel.common as vlq_common

# import common_vlq
import tptp_settings
# import final_plotting
import common_plot
# import tptp_sframe 
import sensitivity
import compare_crs

from ROOT import TLatex, TH2

# varial.settings.max_num_processes = 1

#====PLOTTING====

#====DEFINITIONS====

src_dir_rel = '../Hadd'

normsignal = 20.

basenames_final = list('uhh2.AnalysisModuleRunner.'+f for f in [
    'DATA.SingleMuon_Run2015CD',
    'DATA.SingleEle_Run2015CD',
    'MC.QCD',
    'MC.WJets',
    'MC.DYJetsToLL',
    'MC.SingleTop',
    'MC.TTbar',
    'MC.TTJets_ScaleUp',
    'MC.TTJets_ScaleDown',
    'MC.TpTp_M-0700_thth', 'MC.TpTp_M-0700_thtz', 'MC.TpTp_M-0700_thbw', 'MC.TpTp_M-0700_noH_tztz', 'MC.TpTp_M-0700_noH_tzbw', 'MC.TpTp_M-0700_noH_bwbw',
    'MC.TpTp_M-0800_thth', 'MC.TpTp_M-0800_thtz', 'MC.TpTp_M-0800_thbw', 'MC.TpTp_M-0800_noH_tztz', 'MC.TpTp_M-0800_noH_tzbw', 'MC.TpTp_M-0800_noH_bwbw',
    'MC.TpTp_M-0900_thth', 'MC.TpTp_M-0900_thtz', 'MC.TpTp_M-0900_thbw', 'MC.TpTp_M-0900_noH_tztz', 'MC.TpTp_M-0900_noH_tzbw', 'MC.TpTp_M-0900_noH_bwbw',
    'MC.TpTp_M-1000_thth', 'MC.TpTp_M-1000_thtz', 'MC.TpTp_M-1000_thbw', 'MC.TpTp_M-1000_noH_tztz', 'MC.TpTp_M-1000_noH_tzbw', 'MC.TpTp_M-1000_noH_bwbw',
    'MC.TpTp_M-1100_thth', 'MC.TpTp_M-1100_thtz', 'MC.TpTp_M-1100_thbw', 'MC.TpTp_M-1100_noH_tztz', 'MC.TpTp_M-1100_noH_tzbw', 'MC.TpTp_M-1100_noH_bwbw',
    'MC.TpTp_M-1200_thth', 'MC.TpTp_M-1200_thtz', 'MC.TpTp_M-1200_thbw', 'MC.TpTp_M-1200_noH_tztz', 'MC.TpTp_M-1200_noH_tzbw', 'MC.TpTp_M-1200_noH_bwbw',
    'MC.TpTp_M-1300_thth', 'MC.TpTp_M-1300_thtz', 'MC.TpTp_M-1300_thbw', 'MC.TpTp_M-1300_noH_tztz', 'MC.TpTp_M-1300_noH_tzbw', 'MC.TpTp_M-1300_noH_bwbw',
    'MC.TpTp_M-1400_thth', 'MC.TpTp_M-1400_thtz', 'MC.TpTp_M-1400_thbw', 'MC.TpTp_M-1400_noH_tztz', 'MC.TpTp_M-1400_noH_tzbw', 'MC.TpTp_M-1400_noH_bwbw',
    'MC.TpTp_M-1500_thth', 'MC.TpTp_M-1500_thtz', 'MC.TpTp_M-1500_thbw', 'MC.TpTp_M-1500_noH_tztz', 'MC.TpTp_M-1500_noH_tzbw', 'MC.TpTp_M-1500_noH_bwbw',
    'MC.TpTp_M-1600_thth', 'MC.TpTp_M-1600_thtz', 'MC.TpTp_M-1600_thbw', 'MC.TpTp_M-1600_noH_tztz', 'MC.TpTp_M-1600_noH_tzbw', 'MC.TpTp_M-1600_noH_bwbw',
    'MC.TpTp_M-1700_thth', 'MC.TpTp_M-1700_thtz', 'MC.TpTp_M-1700_thbw', 'MC.TpTp_M-1700_noH_tztz', 'MC.TpTp_M-1700_noH_tzbw', 'MC.TpTp_M-1700_noH_bwbw',
    'MC.TpTp_M-1800_thth', 'MC.TpTp_M-1800_thtz', 'MC.TpTp_M-1800_thbw', 'MC.TpTp_M-1800_noH_tztz', 'MC.TpTp_M-1800_noH_tzbw', 'MC.TpTp_M-1800_noH_bwbw',
    'MC.BpBp_M-0700_bhbh', 'MC.BpBp_M-0700_bhbz', 'MC.BpBp_M-0700_bhtw', 'MC.BpBp_M-0700_noH_bzbz', 'MC.BpBp_M-0700_noH_bztw', 'MC.BpBp_M-0700_noH_twtw',
    'MC.BpBp_M-0800_bhbh', 'MC.BpBp_M-0800_bhbz', 'MC.BpBp_M-0800_bhtw', 'MC.BpBp_M-0800_noH_bzbz', 'MC.BpBp_M-0800_noH_bztw', 'MC.BpBp_M-0800_noH_twtw',
    'MC.BpBp_M-0900_bhbh', 'MC.BpBp_M-0900_bhbz', 'MC.BpBp_M-0900_bhtw', 'MC.BpBp_M-0900_noH_bzbz', 'MC.BpBp_M-0900_noH_bztw', 'MC.BpBp_M-0900_noH_twtw',
    'MC.BpBp_M-1000_bhbh', 'MC.BpBp_M-1000_bhbz', 'MC.BpBp_M-1000_bhtw', 'MC.BpBp_M-1000_noH_bzbz', 'MC.BpBp_M-1000_noH_bztw', 'MC.BpBp_M-1000_noH_twtw',
    'MC.BpBp_M-1100_bhbh', 'MC.BpBp_M-1100_bhbz', 'MC.BpBp_M-1100_bhtw', 'MC.BpBp_M-1100_noH_bzbz', 'MC.BpBp_M-1100_noH_bztw', 'MC.BpBp_M-1100_noH_twtw',
    'MC.BpBp_M-1200_bhbh', 'MC.BpBp_M-1200_bhbz', 'MC.BpBp_M-1200_bhtw', 'MC.BpBp_M-1200_noH_bzbz', 'MC.BpBp_M-1200_noH_bztw', 'MC.BpBp_M-1200_noH_twtw',
    'MC.BpBp_M-1300_bhbh', 'MC.BpBp_M-1300_bhbz', 'MC.BpBp_M-1300_bhtw', 'MC.BpBp_M-1300_noH_bzbz', 'MC.BpBp_M-1300_noH_bztw', 'MC.BpBp_M-1300_noH_twtw',
    'MC.BpBp_M-1400_bhbh', 'MC.BpBp_M-1400_bhbz', 'MC.BpBp_M-1400_bhtw', 'MC.BpBp_M-1400_noH_bzbz', 'MC.BpBp_M-1400_noH_bztw', 'MC.BpBp_M-1400_noH_twtw',
    'MC.BpBp_M-1500_bhbh', 'MC.BpBp_M-1500_bhbz', 'MC.BpBp_M-1500_bhtw', 'MC.BpBp_M-1500_noH_bzbz', 'MC.BpBp_M-1500_noH_bztw', 'MC.BpBp_M-1500_noH_twtw',
    'MC.BpBp_M-1600_bhbh', 'MC.BpBp_M-1600_bhbz', 'MC.BpBp_M-1600_bhtw', 'MC.BpBp_M-1600_noH_bzbz', 'MC.BpBp_M-1600_noH_bztw', 'MC.BpBp_M-1600_noH_twtw',
    'MC.BpBp_M-1700_bhbh', 'MC.BpBp_M-1700_bhbz', 'MC.BpBp_M-1700_bhtw', 'MC.BpBp_M-1700_noH_bzbz', 'MC.BpBp_M-1700_noH_bztw', 'MC.BpBp_M-1700_noH_twtw',
    'MC.BpBp_M-1800_bhbh', 'MC.BpBp_M-1800_bhbz', 'MC.BpBp_M-1800_bhtw', 'MC.BpBp_M-1800_noH_bzbz', 'MC.BpBp_M-1800_noH_bztw', 'MC.BpBp_M-1800_noH_twtw',
    ])

basenames_pre = list('uhh2.AnalysisModuleRunner.'+f for f in [
    'DATA.SingleMuon_Run2015CD',
    'DATA.SingleEle_Run2015CD',
    'MC.QCD',
    'MC.WJets',
    'MC.DYJetsToLL',
    'MC.SingleTop',
    'MC.TTbar',
    'MC.TTJets_ScaleUp',
    'MC.TTJets_ScaleDown',
    'MC.TpTp_M-0700',
    'MC.TpTp_M-0800',
    'MC.TpTp_M-0900',
    'MC.TpTp_M-1000',
    'MC.TpTp_M-1100',
    'MC.TpTp_M-1200',
    'MC.TpTp_M-1300',
    'MC.TpTp_M-1400',
    'MC.TpTp_M-1500',
    'MC.TpTp_M-1600',
    'MC.TpTp_M-1700',
    'MC.TpTp_M-1800',
    'MC.BpBp_M-0700',
    'MC.BpBp_M-0800',
    'MC.BpBp_M-0900',
    'MC.BpBp_M-1000',
    'MC.BpBp_M-1100',
    'MC.BpBp_M-1200',
    'MC.BpBp_M-1300',
    'MC.BpBp_M-1400',
    'MC.BpBp_M-1500',
    'MC.BpBp_M-1600',
    'MC.BpBp_M-1700',
    'MC.BpBp_M-1800',
    ])

normfactors_comp = {
    '_thX' : 1./0.56,
    '_other' : 1./0.44,
    # '_thth' : 1./0.11,
}

normfactors_ind_fs = {
    '_thth' : 1./0.111,
    '_tztz' : 1./0.111,
    '_bwbw' : 1./0.111,
    '_thtz' : 1./0.222,
    '_thbw' : 1./0.222,
    '_tzbw' : 1./0.222,
}


signals_to_plot = [
    'TpTp_M-0700',
    # 'TpTp_M-0800',
    # 'TpTp_M-0900',
    'TpTp_M-1000',
    # 'TpTp_M-1100',
    # 'TpTp_M-1200',
    'TpTp_M-1300',
    # 'TpTp_M-1400',
    # 'TpTp_M-1500',
    # 'TpTp_M-1600',
    'TpTp_M-1700',
    # 'TpTp_M-1800',
]

more_signals = [
    'TpTp_M-0700',
    # 'TpTp_M-0800',
    'TpTp_M-0900',
    'TpTp_M-1000',
    'TpTp_M-1100',
    # 'TpTp_M-1200',
    'TpTp_M-1300',
    # 'TpTp_M-1400',
    'TpTp_M-1500',
    # 'TpTp_M-1600',
    'TpTp_M-1700',
    # 'TpTp_M-1800',
]

less_signals = [
    # 'TpTp_M-0700',
    'TpTp_M-0800',
    # 'TpTp_M-0900',
    # 'TpTp_M-1000',
    # 'TpTp_M-1100',
    'TpTp_M-1200',
    # 'TpTp_M-1300',
    # # 'TpTp_M-1400',
    # 'TpTp_M-1500',
    'TpTp_M-1600',
    # 'TpTp_M-1700',
    # 'TpTp_M-1800',
]

final_states_to_plot = [
    '_thth',
    '_thtz',
    '_thbw',
    '_noH_tztz',
    '_noH_tzbw',
    '_noH_bwbw',
]

other_samples_to_plot = [
    'TTbar',
    'SingleTop',
    'QCD',
    'DYJets',
    'WJets',
    'Run2015CD',
]

samples_to_plot_final = other_samples_to_plot + reduce(lambda x, y: x+y, (list(g + f for f in final_states_to_plot) for g in signals_to_plot))
more_samples = other_samples_to_plot + reduce(lambda x, y: x+y, (list(g + f for f in final_states_to_plot) for g in more_signals))
less_samples = other_samples_to_plot + reduce(lambda x, y: x+y, (list(g + f for f in final_states_to_plot) for g in less_signals))

samples_to_plot_only_th = other_samples_to_plot + list(g + '_thth' for g in signals_to_plot)
more_samples_to_plot_only_th = other_samples_to_plot + list(g + '_thth' for g in more_signals)
less_samples_to_plot_only_th = other_samples_to_plot + list(g + '_thth' for g in less_signals)

samples_to_plot_pre = other_samples_to_plot + signals_to_plot
less_samples_to_plot_pre = other_samples_to_plot + less_signals

get_samplename = vlq_common.get_samplename

# varial.settings.pretty_names.update({
#     'no sel._tex' : 'no sel.',
#     'trigger_accept_el45_tex' : 'trigger',
#     'trigger_accept_mu45_tex' : 'trigger',
#     'primary_lepton_pt_tex' : 'p_T(Lepton)',
#     'primary_electron_pt_tex' : 'p_T(Electron)',
#     'primary_muon_pt_tex' : 'p_T(Muon)',
#     'pt_ld_ak4_jet_tex' : 'p_T(1st AK4 jet)',
#     'pt_subld_ak4_jet_tex' : 'p_T(2nd AK4 jet)',
#     '2D cut_tex' : '2D cut',
#     'ST_tex' : 'ST',
#     'n_ak4_tex' : 'N(AK4 jets)',
#     'n_ak8_tex' : 'N(AK8 jets)',
#     'pt_ld_ak8_jet_tex' : 'p_T(1st AK8 jet)',
#     'output/input_tex' : 'output/input',
#     'TpTp_M-0700' : 'TT M0700',
#     'TpTp_M-1000' : 'TT M1000',
#     'TpTp_M-1300' : 'TT M1300',
#     'TpTp_M-1700' : 'TT M1700',
#     'DYJetsToLL' : 'DY + jets',
#     'SingleTop' : 'Single T',
#     'WJets' : 'W + jets'
# } )


def common_loader_hook(wrps):
    wrps = common_plot.add_wrp_info(wrps, sig_ind=common_plot.signal_indicators) # , use_hadd_sample=False
    wrps = common_plot.mod_legend(wrps)
    wrps = (w for w in wrps if w.histo.Integral() > 1e-20)
    wrps = vlq_common.label_axes(wrps)
    wrps = common_plot.mod_title(wrps)
    return wrps

#=======FOR CUTFLOWS=======

def cf_loader_hook(wrps):
    wrps = common_loader_hook(wrps)
    wrps = cutflow_tables.rebin_cutflow(wrps)
    wrps = gen.sort(wrps, ['in_file_path', 'sample'])
    # wrps = list(wrps)
    # for w in wrps: print w.sample, w.in_file_path 
    #=== FIX MERGING WITH PREFIXES===
    # wrps = vlq_common.merge_decay_channels(wrps, postfixes=None, prefixes=['SingleMuon_', 'SingleEle_'], print_warning=False)
    if varial.settings.merge_decay_channels:
        wrps = vlq_common.merge_decay_channels(wrps, postfixes=['_thth', '_thtz', '_thbw'], suffix='_thX', print_warning=True)
        wrps = vlq_common.merge_decay_channels(wrps, postfixes=['_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_other', print_warning=True)
    wrps = gen.sort(wrps, ['in_file_path'])
    return wrps

def mk_cutflow_chain_cat(category, loader_hook, datasets):
    cutflow_histos = varial.tools.HistoLoader(
        pattern='../../../../Hadd/*.root',
        name='CutflowHistos',
        # pattern=common_plot.file_select(datasets_to_plot),
        # input_result_path='../../../../HistoLoader',
        filter_keyfunc=lambda w: 'cutflow' == w.in_file_path.split('/')[-1]\
                       and category == w.in_file_path.split('/')[0] \
                       and any(f in w.file_path for f in datasets),
                       # and (('SingleEle' not in w.file_path and 'Mu' in category) or\
                       # ('SingleMuon' not in w.file_path and 'El' in category)),
        # hook_loaded_histos=lambda w: cutflow_tables.rebin_cutflow(loader_hook(w))
        hook_loaded_histos=cf_loader_hook
    )

    cutflow_stack_plots = varial.tools.Plotter(
        'CutflowStack',
        stack=True,
        input_result_path='../CutflowHistos',
        save_log_scale=True,
        canvas_decorators=common_plot.get_style()
    )

    # cutflow_normed_plots = varial.tools.Plotter(
    #     'CutflowNormed',
    #     # stack=False,
    #     plot_grouper=varial.plotter.plot_grouper_by_in_file_path,
    #     hook_loaded_histos=gen.gen_norm_to_max_val,
    #     input_result_path='../CutflowHistos',
    #     # plot_setup=varial.plotter.default_plot_colorizer,
    #     save_lin_log_scale=True,
    #     canvas_decorators=[varial.rendering.Legend]
    # )

    return varial.tools.ToolChain(category, [
        cutflow_histos,
        # cutflow_normed_plots,
        cutflow_stack_plots,
        cutflow_tables.CutflowTableContent(eff_factor=1.),
        cutflow_tables.CutflowTableTxt(),
        cutflow_tables.CutflowTableTex(True, None),
    ])


#=======FOR ALL PLOTS=======



def loader_hook_finalstates_excl(wrps):
    # wrps = varial.gen.gen_noex_rebin_nbins_max(wrps, nbins_max=60)
    wrps = common_plot.rebin_st_and_nak4(wrps)
    wrps = common_loader_hook(wrps)
    wrps = common_plot.norm_smpl(wrps, common_plot.normfactors)
    wrps = common_plot.norm_smpl(wrps, normfactors_ind_fs, calc_scl_fct=False)
    wrps = gen.gen_make_th2_projections(wrps)
    # wrps = gen.sort(wrps, ['sys_info', 'in_file_path', 'sample'])
    # # if varial.settings.merge_decay_channels:
    # wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw'], print_warning=False)
        # wrps = vlq_common.merge_decay_channels(wrps, ['_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_other', print_warning=False)
    # wrps = itertools.ifilter(lambda w: not any(w.sample.endswith(g) for g in ['_other']), wrps)
    wrps = common_plot.mod_legend_no_thth(wrps)
    if not varial.settings.flex_sig_norm:
        wrps = common_plot.norm_to_fix_xsec(wrps)
    return wrps



def loader_hook_norm_to_int(wrps):
    key = lambda w: '{0}___{1}___{2}___{3}'.format(w.in_file_path, w.is_data, w.is_signal if not w.is_signal else w.sample, w.sys_info)

    wrps = loader_hook_finalstates_excl(wrps)
    wrps = sorted(wrps, key=key)
    wrps = varial.gen.group(wrps, key)
    wrps = varial.gen.gen_merge(wrps)
    wrps = common_plot.norm_to_int(wrps)
    return wrps


# def merge_final_states(wrps):
#     wrps = common_loader_hook(wrps)
#     wrps = common_plot.norm_smpl(wrps, common_plot.normfactors)
#     wrps = gen.gen_make_th2_projections(wrps)
#     # # wrps = gen.sort(wrps, ['sys_info', 'in_file_path', 'sample'])
#     # # wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_incl', print_warning=False, yield_orig=True)
#     # wrps = list(wrps)
#     wrps = common_plot.norm_smpl(wrps, normfactors_ind_fs, calc_scl_fct=False)
#     # wrps = common_plot.mod_legend_eff_counts(wrps)
#     return wrps


# def loader_hook_compare_finalstates_split_lepton_channels(wrps):
#     wrps = common_loader_hook(wrps)
#     wrps = common_plot.norm_smpl(wrps, common_plot.normfactors)
#     wrps = gen.gen_make_th2_projections(wrps)
#     wrps = common_plot.norm_smpl(wrps, normfactors_ind_fs, calc_scl_fct=False)
#     wrps = common_plot.mod_legend_eff_counts(wrps)
#     wrps = common_plot.rebin_st_and_nak4(wrps)
#     return wrps


def loader_hook_merge_regions(wrps):
    def get_base_selection(wrp):
        res = wrp.in_file_path.split('/')[0]
        if len(res.split('_')) > 1:
            res = res.split('_')[0]
        return res 

    def get_sys_info(wrp):
        if '_id__' in wrp.sys_info or '_trg__' in wrp.sys_info:
            return 'sflep'+wrp.sys_info[4:]
        else:
            return wrp.sys_info

    def get_new_infile_path(wrp):
        comps = wrp.in_file_path.split('/')
        return get_base_selection(wrp)+'/'+'/'.join(comps[1:])
                  
    key = lambda w: '{0}___{1}___{2}___{3}'.format(get_base_selection(w), w.sample, get_sys_info(w), w.variable)

    wrps = common_loader_hook(wrps)
    wrps = gen.gen_make_th2_projections(wrps)
    # wrps = gen.sort(wrps, ['sys_info', 'in_file_path', 'sample'])
    # wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_incl', print_warning=False, yield_orig=True)
    wrps = list(wrps)
    wrps = common_plot.norm_smpl(wrps, normfactors_ind_fs, calc_scl_fct=False)
    # wrps = common_plot.mod_legend_eff_counts(wrps)
    wrps = sorted(wrps, key=key)
    wrps = varial.gen.group(wrps, key)
    wrps = varial.gen.gen_merge(wrps)
    wrps = varial.gen.gen_add_wrp_info(wrps, in_file_path=get_new_infile_path, region=get_base_selection, sys_info=get_sys_info)
    return wrps

def loader_hook_merge_lep_channels(wrps):
    # wrps = merge_regions(wrps)
    # wrps = itertools.ifilter(lambda w: all(f not in w.sample for f in ['_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw', '_incl']), wrps)
    wrps = common_plot.norm_smpl(wrps, common_plot.normfactors)
    wrps = common_plot.mod_title(wrps)
    wrps = common_plot.mod_legend_no_thth(wrps)
    if not varial.settings.flex_sig_norm:
        wrps = common_plot.norm_to_fix_xsec(wrps)
    wrps = common_plot.rebin_st_and_nak4(wrps)
    wrps = sorted(wrps, key=lambda w: w.region+'__'+w.name)
    return wrps

# def loader_hook_split_lep_channels(wrps):
#     # wrps = merge_regions(wrps)
#     wrps = common_plot.mod_legend_eff_counts(wrps)
#     wrps = sorted(wrps, key=lambda w: w.region+'__'+w.name+'__'+w.sample)
#     return wrps

def loader_hook_compare_finalstates(wrps):
    wrps = common_plot.rebin_st_and_nak4(wrps)
    wrps = common_loader_hook(wrps)
    wrps = common_plot.norm_smpl(wrps, common_plot.normfactors)
    # wrps = common_plot.norm_smpl(wrps, common_plot.normfactors)
    # wrps = gen.gen_make_th2_projections(wrps)
    wrps = sorted(wrps, key=lambda w: '{0}___{1}___{2}'.format(w.sys_info, w.in_file_path, w.sample))
    # wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_incl', print_warning=False, yield_orig=True)
    # wrps = gen.sort(wrps, ['sys_info', 'in_file_path', 'sample'])
    wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw'], suffix='_thX', print_warning=False)
    wrps = sorted(wrps, key=lambda w: '{0}___{1}___{2}'.format(w.sys_info, w.in_file_path, w.sample))
    wrps = vlq_common.merge_decay_channels(wrps, ['_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_other', print_warning=False)
    # wrps = itertools.ifilter(lambda w: not any(w.sample.endswith(g) for g in ['_thth','_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw']), wrps)
    # wrps = common_plot.norm_smpl(wrps, normfactors_ind_fs, calc_scl_fct=False)
    wrps = common_plot.norm_smpl(wrps, normfactors_comp)
    wrps = common_plot.mod_legend_eff_counts(wrps)
    if not varial.settings.flex_sig_norm:
        wrps = common_plot.norm_to_fix_xsec(wrps)
    wrps = gen.sort(wrps, ['in_file_path'])
    return wrps


def loader_hook_uncerts(wrps):
    def set_line_width(wrps):
        for w in wrps:
            if isinstance(w, wrappers.HistoWrapper):
                w.histo.SetLineWidth(2)
            yield w

    wrps = loader_hook_finalstates_excl(wrps)
    wrps = set_line_width(wrps)
    wrps = sorted(wrps, key=lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))
    return wrps


def group_by_uncerts(wrps, first_sort_func):
    def sort_key_func(wrp):
        if wrp.sys_info:
            return wrp.sys_info.split('__')[0]
        else:
            return ''

    wrps = itertools.groupby(wrps, first_sort_func)
    for k1, g in wrps:
        g = sorted(g, key=sort_key_func)
        g = list(g)
        nominal = g[0]
        sys_uncerts = itertools.groupby(g[1:], sort_key_func)
        for k2, sys in sys_uncerts:
            # print nominal.in_file_path, nominal.sample, nominal.sys_info, list((s.in_file_path, s.sample, s.sys_info) for s in sys)
            nom_copy = copy.copy(nominal)
            nom_copy.name = nom_copy.name+'__'+nom_copy.sample+'__'+k2
            yield wrappers.WrapperWrapper([nom_copy]+list(sys), name=k1+'__'+k2)

# def group_gen_reco_ht(wrps):

#     wrps = itertools.groupby(wrps, first_sort_func)
#     for k1, g in wrps:
#         g = sorted(g, key=lambda w: '{0}'.format())
#         g = list(g)
#         nominal = g[0]
#         sys_uncerts = itertools.groupby(g[1:], sort_key_func)
#         for k2, sys in sys_uncerts:
#             # print nominal.in_file_path, nominal.sample, nominal.sys_info, list((s.in_file_path, s.sample, s.sys_info) for s in sys)
#             nom_copy = copy.copy(nominal)
#             nom_copy.name = nom_copy.name+'__'+nom_copy.sample+'__'+k2
#             yield wrappers.WrapperWrapper([nom_copy]+list(sys), name=k1+'__'+k2)

def plot_setup_uncerts(grps):
    def set_legend(wrps):
        for w in wrps:
            if not w.sys_info:
                w.legend = 'nominal'
            else:
                w.legend = w.sys_info.split('__')[1]
            yield w

    grps = (set_legend(ws) for ws in grps)
    grps = varial.plotter.default_plot_colorizer(grps)
    return grps

# def canvas_setup_pre(grps):
#     grps = common_plot.mod_pre_canv(grps)
#     return grps

def canvas_setup_post(grps):
    grps = common_plot.add_sample_integrals(grps)
    grps = common_plot.mod_post_canv(grps)
    return grps


def stack_setup_norm_sig(grps):
    grps = gen.mc_stack_n_data_sum(grps, calc_sys_integral=True)
    if varial.settings.flex_sig_norm:
        grps = common_plot.norm_to_bkg(grps)
    return grps

def stack_setup_norm_all_to_intgr(grps):
    grps = gen.mc_stack_n_data_sum(grps, calc_sys_integral=False)
    # grps = common_plot.norm_stack_to_integral(grps)
    return grps

def plot_grouper_by_in_file_path_mod(wrps, separate_th2=True):
    if separate_th2:
        wrps = varial.plotter.rename_th2(wrps)
    wrps = common_plot.copy_wrp_for_log(wrps)
    wrps = sorted(wrps, key=lambda w: w.scale+'___'+w.in_file_path)
    return gen.group(wrps, key_func=lambda w: w.scale+'___'+w.in_file_path)

def plotter_factory_stack(**args):
    def tmp(**kws):
        # common_plot.plotter_factory_stack(common_plot.normfactors, **kws)
        # kws['filter_keyfunc'] = lambda w: (f in w.sample for f in datasets_to_plot)
        kws['hook_loaded_histos'] = loader_hook_finalstates_excl
        kws['plot_grouper'] = plot_grouper_by_in_file_path_mod
        kws['plot_setup'] = stack_setup_norm_sig
        kws['stack_setup'] = stack_setup_norm_sig
        # kws['canvas_decorators'] += [rnd.TitleBox(text='CMS Simulation 20fb^{-1} @ 13TeV')]
        # kws['y_axis_scale'] = 'lin'
        kws['hook_canvas_post_build'] = canvas_setup_post
        # kws['hook_canvas_pre_build'] = common_plot.mod_pre_canv
        kws['canvas_decorators'] = common_plot.get_style()
        kws.update(**args)
        return varial.tools.Plotter(**kws)
    return tmp


def plotter_factory_uncerts(**args):
    def tmp(**kws):
        # common_plot.plotter_factory_stack(common_plot.normfactors, **kws)
        # kws['filter_keyfunc'] = lambda w: (f in w.sample for f in datasets_to_plot)
        kws['hook_loaded_histos'] = loader_hook_uncerts
        kws['plot_grouper'] = lambda w: group_by_uncerts(w, 
            lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))
        kws['plot_setup'] = plot_setup_uncerts
        # kws['stack_setup'] = stack_setup_norm_sig
        # kws['canvas_decorators'] += [rnd.TitleBox(text='CMS Simulation 20fb^{-1} @ 13TeV')]
        # kws['y_axis_scale'] = 'lin'
        # kws['save_name_func'] = lambda w: w.save_name
        # kws['hook_canvas_post_build'] = common_plot.add_sample_integrals
        kws['canvas_decorators'] = [
            common_plot.BottomPlotUncertRatio,
            varial.rendering.Legend,
            # varial.rendering.TitleBox(text='#scale[1.2]{#bf{#it{Work in Progress}}}')
            ]
        kws.update(**args)
        return varial.tools.Plotter(**kws)
    return tmp

def mk_plots_and_cf(categories=None, datasets=None, **kws):
    if datasets:
        dataset_filter = lambda w: any(f in w.file_path.split('/')[-1] for f in datasets)
    else:
        dataset_filter = lambda w: w
    args = {
        'pattern' : '../Hadd/*.root',
        # 'filter_keyfunc' : filter_func,
        'plotter_factory' : plotter_factory_stack(),
        'auto_legend' : False,
        'name' : 'StackedAll',
        'lookup_aliases' : varial.settings.lookup_aliases
    }
    args.update(**kws)
    if 'filter_keyfunc' in args.keys():
        filter_func = args['filter_keyfunc']
        args['filter_keyfunc'] = lambda w: filter_func(w) and dataset_filter(w)
    else:
        args['filter_keyfunc'] = dataset_filter
    def create():
        plot_chain = [varial.plotter.RootFilePlotter(**args)]
        if categories:
            cutflow_cat = []
            for cat in categories:
                if cat is not 'NoSelection' and cat is not 'CombinedElMu':
                    cutflow_cat.append(mk_cutflow_chain_cat(
                        cat,
                        common_loader_hook,
                        datasets))
            plot_chain.append(varial.tools.ToolChain('CutflowTools', cutflow_cat))

        return plot_chain
    return create

def mk_toolchain(name, datasets=None, categories=None, **kws):
    return varial.tools.ToolChainParallel(
        name,
        lazy_eval_tools_func=mk_plots_and_cf(categories=categories, datasets=datasets, **kws)
        )

import tex_content

def plot_only(version='Test', pattern='', categories=None):
    plots = varial.tools.ToolChainParallel(
        'Plots',
        lazy_eval_tools_func=mk_plots_and_cf(pattern=pattern, categories=categories)
    )
    tc = varial.tools.ToolChain(
        version,
        [
            plots,
            varial.tools.WebCreator(no_tool_check=True)
        ]
    )
    return tc

# sframe_tools = mk_sframe_and_plot_tools()

import sys
import tptpsframe_runner as sframe

if __name__ == '__main__':
    time.sleep(1)
    src_dir = sys.argv[1]
    final_dir = sys.argv[2]
    if len(sys.argv) >= 3:
        cats = sys.argv[3:]
    else:
        cats = None
    all_tools = plot_only(version=final_dir, pattern=src_dir, categories=cats)
    varial.tools.Runner(all_tools, default_reuse=False)
    # varial.tools.CopyTool('~/www/vlq_analysis/tight_selection2/',
    #     src=final_dir, use_rsync=True).run()