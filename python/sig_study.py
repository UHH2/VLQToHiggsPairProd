#!/usr/bin/env python

import sys
import os
import time
import itertools
import copy
import ctypes
import pprint

import varial.settings
import varial.tools
import varial.generators as gen
import varial.rendering as rnd
# import varial.analysis as analysis
# from varial.sample import Sample
# from varial.extensions.sframe import SFrame
from varial.extensions.hadd import Hadd
from varial.extensions.sframe import SFrame
import varial.wrappers as wrappers
import varial.operations as op

import UHH2.VLQSemiLepPreSel.cutflow_tables as cutflow_tables
import UHH2.VLQSemiLepPreSel.common as vlq_common

import varial.settings
# import common_vlq
import tptp_settings
import tptpsframe_runner
# import final_plotting
import plot_new as plot
import common_plot_new as common_plot
# import tptp_sframe 
# import compare_crs
import analysis
import tex_content_new as tex_content

from ROOT import TLatex, TH2, kGreen, kOrange

varial.settings.max_num_processes = 24

sframe_cfg = '/afs/desy.de/user/n/nowatsd/xxl-af-cms/SFrameUHH2/CMSSW_7_6_3/src/UHH2/VLQToHiggsPairProd/config/TpTpSignalStudies.xml'

basenames_signals = list('uhh2.AnalysisModuleRunner.'+f for f in [
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
    ])

final_states = tptpsframe_runner.final_states_to_split_into_tp + ['lep_T', 'lep_top', 'lep_other']

basenames_signals_split = reduce(lambda x, y: x+ y, (list(g + '_' + f for f in final_states) for g in basenames_signals))

basenames_backgrounds = list('uhh2.AnalysisModuleRunner.'+f for f in [
    'MC.TTbar',
    'MC.WJets',
    'MC.QCD'
    ])

basenames = basenames_signals_split + basenames_backgrounds

varial.settings.colors.update({
    'TpTp_M-0800' : kGreen+1,
    'TpTp_M-1200' : kOrange+7, # 417
    'TpTp_M-1600' : 596,
    'TTbar': 632,
    'WJets': 860,
    'El45_pt200_pt50' : 2,
    'El105' : 3,
    'El27_iso' : 4,
    'Mu45' : 2,
    'Mu20_iso' : 3,
})

def sort_legend_signal(w):
    if 'TeV' in w:
        mass = w[-8:-5]
        return -float(mass)
    else:
        return -100

varial.settings.defaults_Legend.update({
    'y_pos': 0.86,
    'x_pos': 0.6,
    'label_width': 0.3,
    'label_height': 0.06,
    'box_text_size' : 0.05,
    'sort_legend' : sort_legend_signal,
    })

# varial.settings.canvas_size_x = 550
# varial.settings.canvas_size_y = 500


def apply_axis_style(obj, y_bounds):
    _, y_max = y_bounds
    obj.GetXaxis().SetNoExponent()
    obj.GetXaxis().SetLabelSize(0.052)
    obj.GetXaxis().SetTitleSize(0.055)
    obj.GetYaxis().SetTitleSize(0.055)
    obj.GetXaxis().SetTitleOffset(1.)
    obj.GetYaxis().SetTitleOffset(0.9)
    obj.SetMinimum(y_max / 10000.)
    obj.SetMaximum(y_max * 1.1)

varial.settings.apply_axis_style = apply_axis_style


default_canv_attr = dict(common_plot.default_canv_attr)

default_canv_attr.update({
    # 'y_min_gr_zero' : 1e-9,
    'y_max_fct' : 1.4,
    # 'y_max_log_fct' : 1.,
    # '_set_leg_2_col_lin' : False,
    # '_set_leg_2_col_log' : False,
    # '_set_leg_1_col_lin' : False,
    # '_set_leg_1_col_log' : False,
    # 'move_exp' : False,
    # 'no_exp' : False,
})

mod_dict = {
    'higgs_dRDecay_all' : {
            # 'y_max_fct' : 1.3,
            'title' : '#DeltaR(H decay products)',
            # 'bin_width' : 5,
            # 'y_min_gr_zero' : 0.02,
            # 'y_max_log_fct' : 1000.,
            # 'scale' : 0.4,
            '_set_leg_1_col_lin' : {
                    'x_pos': 0.7,
                    'y_pos': 0.7,
                    # 'label_width': 0.30,
                    # 'label_height': 0.040,
                    # 'box_text_size' : 0.033,
                    # 'opt': 'f',
                    # 'opt_data': 'pl',
                    # 'reverse': True,
                    # 'sort_legend' : lambda w: 'TT ' in w[1],
                },
            # 'text_box_lin' : (0.19, 0.82, "#scale[0.8]{#bf{CMS}}"),
            },
    'higgs_to_bb_dRDecay_all' : {
            'rebin_list' : list(float(i)/10 for i in xrange(0, 41)),
            'title' : '#DeltaR_{H #rightarrow b#bar{b}}(b,#bar{b})',
            'y_pad_margin' : 0.16,
            '_set_leg_1_col_lin' : {
                    'x_pos': 0.7,
                    'y_pos': 0.7,
                },
            },
    'higgs_to_bb_dRDecay_all_rebin_flex' : {
            'title' : '#DeltaR_{H #rightarrow b#bar{b}}(b,#bar{b})',
            'y_pad_margin' : 0.16,
            '_set_leg_1_col_lin' : {
                    'x_pos': 0.7,
                    'y_pos': 0.7,
                },
            },
    'higgs_pt_all' : {
            'rebin' : 50,
            # 'y_max_fct' : 1.3,
            'title' : 'p_{T}(H)',
            '_set_leg_1_col_lin' : {
                    'x_pos': 0.7,
                    'y_pos': 0.7,
                },
            },
    'W_from_T_dRDecay_all' : {
            # 'y_max_fct' : 1.3,
            'title' : '#DeltaR(W decay products)',
            '_set_leg_1_col_lin' : {
                    'x_pos': 0.7,
                    'y_pos': 0.7,
                },
            },
    'W_from_T_pt_all' : {
            'rebin' : 50,
            # 'y_max_fct' : 1.3,
            'title' : 'p_{T}(W)',
            '_set_leg_1_col_lin' : {
                    'x_pos': 0.7,
                    'y_pos': 0.7,
                },
            },
    'W_dRDecay_all' : {
            # 'y_max_fct' : 1.3,
            'rebin_list' : list(float(i)/10 for i in xrange(0, 41)),
            'title' : "#DeltaR_{W #rightarrow q#bar{q}'}(q,#bar{q}')",
            'y_pad_margin' : 0.16,
            # 'title' : '#DeltaR(W decay products)',
            '_set_leg_1_col_lin' : {
                    'x_pos': 0.7,
                    'y_pos': 0.7,
                },
            },
    'W_dRDecay_all_rebin_flex' : {
            # 'y_max_fct' : 1.3,
            'title' : "#DeltaR_{W #rightarrow q#bar{q}'}(q,#bar{q}')",
            'y_pad_margin' : 0.16,
            # 'title' : '#DeltaR(W decay products)',
            '_set_leg_1_col_lin' : {
                    'x_pos': 0.7,
                    'y_pos': 0.7,
                },
            },
    'W_pt_all' : {
            'rebin' : 50,
            # 'y_max_fct' : 1.3,
            'title' : 'p_{T}(W)',
            '_set_leg_1_col_lin' : {
                    'x_pos': 0.7,
                    'y_pos': 0.7,
                },
            },
    'spec_max_deltaR_topprod' : {
            # 'y_max_fct' : 1.3,
            'title' : 'max(#DeltaR_{t #rightarrow bl#nu}(b,l,#nu))',
            'y_pad_margin' : 0.16,
            '_set_leg_1_col_lin' : {
                    'x_pos': 0.7,
                    'y_pos': 0.7,
                },
            },
    }

colors_mu = [797, 434, 409]
colors_el = [625, 596, 617]
all_colors = colors_el+colors_mu
markers = [(21, 1), (22, 1.2), (23, 1.2), (20, 1), (24, 1), (25, 1), (26, 1)]

def get_style():
    # _style = style or varial.settings.style
    return [
        common_plot.mod_pre_bot_hist(mod_dict),
        common_plot.mk_split_err_ratio_plot_func_mod(poisson_errs=True),  # mk_pull_plot_func()
        # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
        rnd.mk_legend_func(),
        common_plot.mod_post_canv(dict_cnv_attr=mod_dict, default_attr=default_canv_attr),
        # titlebox_func
    ]



def add_eff_to_wrp(wrps):
    for w in wrps:
        if w.name.endswith('_incl_eff'):
            eff_x, eff_y = ctypes.c_double(), ctypes.c_double()
            w.graph.GetPoint(0, eff_x, eff_y)
            y_plus = w.graph.GetErrorYhigh(0)
            y_minus = w.graph.GetErrorYlow(0)
            setattr(w, w.sample+'_efficiency', (eff_y.value, y_plus, -y_minus))
        yield w

def mod_title(wrps):
    for w in wrps:
        if 'electron' in w.name:
            x_ax_post = '(e) [GeV]'
        elif 'muon' in w.name:
            x_ax_post = '(#mu) [GeV]'
        if 'FullSelectionST' in w.in_file_path:
            x_ax_pre = 'S_{T}'
        else:
            x_ax_pre = 'p_{T}'
        # if isinstance(w, varial.wrappers.HistoWrapper):
        #     w.histo.GetXaxis().SetTitle(x_ax_pre+x_ax_post)
        # elif isinstance(w, varial.wrappers.GraphWrapper):
        #     w.graph.GetXaxis().SetTitle(x_ax_pre+x_ax_post)
        w.obj.GetXaxis().SetTitle(x_ax_pre+x_ax_post)

        # if isinstance(w, varial.wrappers.HistoWrapper):
        #     w.histo.GetYaxis().SetTitle('Efficiency')
        # elif isinstance(w, varial.wrappers.GraphWrapper):
        #     w.graph.GetYaxis().SetTitle('Efficiency')
        w.obj.GetYaxis().SetTitle('Efficiency')

        yield w

def mod_title_norm(wrps):
    for w in wrps:
        w.histo.GetYaxis().SetTitle('Arbitrary units')
        # w.histo.GetXaxis().SetTitle('test')
        yield w

rebin_list_pt = list(i for i in xrange(0, 1000, 80))
rebin_list_pt += list(i for i in xrange(1000, 1600, 240))
rebin_list_pt += list(i for i in xrange(1600, 2400, 480))

# print rebin_list_pt

def rebin(wrps):
    for w in wrps:
        if '_pt_' in w.name and not isinstance(w.histo, TH2) and not 'incl' in w.name:
            new_w_flex = op.rebin(w, rebin_list_pt, True)
            suffix = w.name[-4:]
            new_w_flex.name = w.name[:-4]+'_rebin_flex'+suffix
            new_w_flex.in_file_path = w.in_file_path[:-4]+'_rebin_flex'+suffix
            yield new_w_flex
        yield w

def rebin_fix(wrps):
    for w in wrps:
        if '_pt_' in w.name:
            new_w_flex = op.rebin_nbins_max(w, 30)
            yield new_w_flex
        yield w

def mk_marker(wrps):
    for w in wrps:
        if isinstance(w, wrappers.GraphWrapper):
            w.graph.SetMarkerStyle(1)
        yield w

def marker_style(wrps, markers=markers):
    n = 0
    for wrp in wrps:
        mrk = markers[n % len(markers)]
        n += 1
        if isinstance(wrp, wrappers.GraphWrapper):
            wrp.graph.SetMarkerStyle(mrk[0])
            wrp.graph.SetMarkerSize(mrk[1])
        yield wrp

def marker_col(wrps):
    n = 0
    for wrp in wrps:
        if 'electron' in wrp.name:
            col = colors_el[n % len(colors_el)]
        elif 'muon' in wrp.name:
            col = colors_mu[n % len(colors_mu)]
        else:
            col = all_colors[n % len(all_colors)]
        n += 1
        wrp.obj.SetLineColor(col)
        wrp.obj.SetMarkerColor(col)
        yield wrp



def set_line_style(wrps):
    line_style = {
        'TpTp_M-0800' : 7,
        'TpTp_M-1200' : 1,
        'TpTp_M-1600' : 2,
    }
    for wrp in wrps:
        if line_style.get(wrp.sample, None):
            wrp.obj.SetLineStyle(line_style[wrp.sample])
        yield wrp

def colorize_gen_hists(wrps):
    col_dict = {
        'TpTp_M-0800' : 628,
        'TpTp_M-1200' : 412,
        'TpTp_M-1600' : 596,
    }
    for wrp in wrps:
        if col_dict.get(wrp.sample, None):
            wrp.obj.SetLineColor(col_dict[wrp.sample])
        yield wrp


def add_eff_to_info(canvas_builders):

    for cnv in canvas_builders:
        # TODO when rendering goes generator
        # for r in cnv._renderers:
        #     for sample, eff in r.__dict__.iteritems():
        #         if sample.endswith('_efficiency'):
        #             print sample, eff
        cnv.__dict__.update(dict(
            (sample, eff)
            for r in cnv._renderers
            if isinstance(r, rnd.GraphRenderer)  # applies also to StackRnd.
            for sample, eff in r.__dict__.iteritems()
            if sample.endswith('_efficiency')
        ))
        # pprint.pprint(cnv.__dict__.keys(
        # for r in cnv._renderers:
        #     for sample, eff in r.__dict__.iteritems():
        #         if sample.endswith('_efficiency'):
        #             print sample, eff))
        yield cnv


def mk_name(wrp):
    if wrp.is_signal:
        return 'sig_'
    else:
        return 'bkg_'

def plot_grouper_sep_sig_bkg(wrps):
    # if separate_th2:
    #     wrps = rename_th2(wrps)
    return gen.group(wrps, key_func=lambda w: mk_name(w)+'___'+w.in_file_path)

def comp_trg_group(wrp):
    split_name = wrp.name.split('_')
    full_ind = split_name.index('full') if 'full' in wrp.name else split_name.index('base')
    lep = wrp.name.split('_')[0]
    plot = '_'.join(split_name[full_ind:])
    return lep + '__' + plot + '__' + wrp.sample

def plot_grouper_comp_trg(wrps):

    wrps = sorted(wrps, key=comp_trg_group)
    # if separate_th2:
    #     wrps = rename_th2(wrps)
    return gen.group(wrps, key_func=comp_trg_group)

def mod_legend_comp_trg(wrps):
    dict_leg = {
        'muon_pt_iso_full' : 'Iso. #mu sel.',
        'muon_pt_full' : 'Non-iso. #mu sel.',
        'electron_pt_iso_full' : 'Iso. e sel.',
        'electron_pt_full' : 'Non-iso. e sel.',
        'electron_pt_105_full' : 'Non-iso., high-p_{T} e sel.',
    }

    for w in wrps:

        # if w.name.startswith('electron'):
        #     chan = 'El'
        #     suf = '45_pt200_pt50'
        #     if '105' in w.name:
        #         suf = '105'
        #     elif 'iso' in w.name:
        #         suf = '27_iso'
        # elif w.name.startswith('muon'):
        #     chan = 'Mu'
        #     suf = '45'
        #     if 'iso' in w.name:
        #         suf = '20_iso'
        # w.legend = chan + suf
        for k, v in dict_leg.iteritems():
            if w.name.startswith(k):
                w.legend = v
                w.draw_option_legend = 'ple'
        yield w

# def plot_grouper_sep_sig_bkg(wrps):
#     # if separate_th2:
#     #     wrps = rename_th2(wrps)
#     return gen.group(wrps, key_func=lambda w: mk_name(w)+'___'+w.in_file_path)

def mod_cnv_postbuild(cnvs):
    cnvs = common_plot.add_sample_integrals(cnvs)
    cnvs = add_eff_to_info(cnvs)
    return cnvs

def filter_bkg_base(wrps):
    for w in wrps:
        if not (not w.is_signal and 'base' in w.in_file_path):
            yield w

def filter_signal(wrps):
    for w in wrps:
        if w.is_signal:
            yield w


def loader_hook_eff(wrps):
    # wrps = common_plot.rebin_st_and_nak4(wrps)
    # wrps = plot.common_loader_hook(wrps)
    wrps = rebin(wrps)
    # wrps = rebin_fix(wrps)
    wrps = common_plot.add_wrp_info(wrps, sig_ind=common_plot.signal_indicators) # , use_hadd_sample=False
    wrps = filter_bkg_base(wrps)
    wrps = common_plot.mod_legend(wrps)
    wrps = vlq_common.label_axes(wrps)
    # wrps = common_plot.mod_title(wrps)
    # wrps = common_plot.norm_smpl(wrps, common_plot.pas_normfactors)
    # wrps = common_plot.norm_smpl(wrps, normfactors_ind_fs, calc_scl_fct=False)
    # wrps = gen.gen_make_th2_projections(wrps)

    wrps = sorted(wrps, key=lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))
    wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_all', print_warning=False, yield_orig=True)
    wrps = sorted(wrps, key=lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))
    wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw'], suffix='_thX', print_warning=False, yield_orig=True)
    wrps = sorted(wrps, key=lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))
    wrps = vlq_common.merge_decay_channels(wrps, ['_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_other', print_warning=False, yield_orig=True)
    wrps = gen.gen_make_eff_graphs(wrps, yield_everything=True, pair_func=lambda w, l: w.sample+'_'+w.in_file_path[:-l])
    wrps = mk_marker(wrps)
    wrps = add_eff_to_wrp(wrps)
    wrps = common_plot.mod_legend_no_thth(wrps)
    wrps = sorted(wrps, key=lambda w: w.in_file_path)
    return wrps

def loader_hook_gen_hists(wrps):
    wrps = common_plot.rebin_st_and_nak4(wrps, mod_dict)
    # wrps = plot.common_loader_hook(wrps)
    # wrps = rebin(wrps)
    # wrps = rebin_fix(wrps)
    wrps = common_plot.add_wrp_info(wrps, sig_ind=common_plot.signal_indicators) # , use_hadd_sample=False
    wrps = filter_signal(wrps)
    wrps = common_plot.mod_legend(wrps)
    wrps = vlq_common.label_axes(wrps)
    wrps = common_plot.mod_title(wrps, mod_dict)

    wrps = sorted(wrps, key=lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))
    wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw'], print_warning=False, yield_orig=False)
    wrps = gen.gen_norm_to_integral(wrps)
    wrps = mod_title_norm(wrps)
    # wrps = sorted(wrps, key=lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))
    # wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw'], suffix='_thX', print_warning=False, yield_orig=True)
    # wrps = sorted(wrps, key=lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))
    # wrps = vlq_common.merge_decay_channels(wrps, ['_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_other', print_warning=False, yield_orig=False)
    wrps = gen.gen_make_eff_graphs(wrps, yield_everything=True, pair_func=lambda w, l: w.sample+'_'+w.in_file_path[:-l])
    wrps = gen.apply_linewidth(wrps, 3)
    wrps = set_line_style(wrps)
    # wrps = colorize_gen_hists(wrps)
    # wrps = mk_marker(wrps)
    wrps = add_eff_to_wrp(wrps)
    wrps = sorted(wrps, key=lambda w: w.in_file_path)
    return wrps

def loader_hook_split_leps(wrps):
    # wrps = common_plot.rebin_st_and_nak4(wrps)
    # wrps = plot.common_loader_hook(wrps)
    wrps = rebin(wrps)
    # wrps = rebin_fix(wrps)
    wrps = common_plot.add_wrp_info(wrps, sig_ind=common_plot.signal_indicators) # , use_hadd_sample=False
    # wrps = filter_signal(wrps)
    wrps = common_plot.mod_legend(wrps)
    wrps = vlq_common.label_axes(wrps)

    # wrps = sorted(wrps, key=lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))
    # wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_all', print_warning=False, yield_orig=False)
    # wrps = sorted(wrps, key=lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))
    # wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw'], suffix='_thX', print_warning=False, yield_orig=True)
    # wrps = sorted(wrps, key=lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))
    # wrps = vlq_common.merge_decay_channels(wrps, ['_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_other', print_warning=False, yield_orig=False)
    wrps = gen.gen_make_eff_graphs(wrps, yield_everything=True, pair_func=lambda w, l: w.sample+'_'+w.in_file_path[:-l])
    wrps = mk_marker(wrps)
    wrps = add_eff_to_wrp(wrps)
    wrps = sorted(wrps, key=lambda w: w.in_file_path)
    return wrps

def loader_hook_comp_trg(wrps):
    # wrps = common_plot.rebin_st_and_nak4(wrps)
    # wrps = plot.common_loader_hook(wrps)
    wrps = common_plot.add_wrp_info(wrps, sig_ind=common_plot.signal_indicators) # , use_hadd_sample=False
    wrps = rebin(wrps)
    # wrps = rebin_fix(wrps)
    # wrps = common_plot.mod_legend(wrps)
    wrps = vlq_common.label_axes(wrps)
    wrps = mod_legend_comp_trg(wrps)

    wrps = sorted(wrps, key=lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))
    wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_all', print_warning=False, yield_orig=True)
    wrps = sorted(wrps, key=lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))
    wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw'], suffix='_thX', print_warning=False, yield_orig=True)
    wrps = sorted(wrps, key=lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))
    wrps = vlq_common.merge_decay_channels(wrps, ['_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_other', print_warning=False, yield_orig=False)
    wrps = gen.gen_make_eff_graphs(wrps, yield_everything=True, pair_func=lambda w, l: w.sample+'_'+w.in_file_path[:-l])
    wrps = mod_title(wrps)
    # wrps = mk_marker(wrps)
    wrps = add_eff_to_wrp(wrps)
    wrps = sorted(wrps, key=lambda w: w.in_file_path)
    return wrps

def loader_hook_split_leps_comp_trg(wrps):
    # wrps = common_plot.rebin_st_and_nak4(wrps)
    # wrps = plot.common_loader_hook(wrps)
    wrps = rebin(wrps)
    # wrps = rebin_fix(wrps)
    wrps = common_plot.add_wrp_info(wrps, sig_ind=common_plot.signal_indicators) # , use_hadd_sample=False
    # wrps = filter_signal(wrps)
    wrps = common_plot.mod_legend(wrps)
    wrps = mod_legend_comp_trg(wrps)
    wrps = vlq_common.label_axes(wrps)

    # wrps = sorted(wrps, key=lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))
    # wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_all', print_warning=False, yield_orig=False)
    # wrps = sorted(wrps, key=lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))
    # wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw'], suffix='_thX', print_warning=False, yield_orig=True)
    # wrps = sorted(wrps, key=lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))
    # wrps = vlq_common.merge_decay_channels(wrps, ['_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_other', print_warning=False, yield_orig=False)
    wrps = gen.gen_make_eff_graphs(wrps, yield_everything=True, pair_func=lambda w, l: w.sample+'_'+w.in_file_path[:-l])
    wrps = mk_marker(wrps)
    wrps = add_eff_to_wrp(wrps)
    wrps = sorted(wrps, key=lambda w: w.in_file_path)
    return wrps


def plot_setup_comp_trg(grps):
    grps = (marker_col(ws) for ws in grps)
    grps = (marker_col(ws) for ws in grps)
    grps = (marker_style(ws, markers) for ws in grps)
    grps = list(grps)
    return grps



def plotter_factory_eff():

    def tmp(**kws):
        # common_plot.plotter_factory_eff(common_plot.normfactors, **kws)
        kws['filter_keyfunc'] = lambda w: 'GenHists' not in w.in_file_path
        kws['hook_loaded_histos'] = loader_hook_eff
        # kws['plot_grouper'] = plot_grouper_sep_sig_bkg
        # kws['plot_setup'] = lambda w: stack_setup_norm_sig(w, rate_uncertainties, shape_uncertainties, include_rate)
        # kws['stack_setup'] = lambda w: stack_setup_norm_sig(w, rate_uncertainties, shape_uncertainties, include_rate)
        # kws['canvas_post_build_funcs'] += [rnd.TitleBox(text='CMS Simulation 20fb^{-1} @ 13TeV')]
        # kws['y_axis_scale'] = 'lin'
        kws['hook_canvas_post_build'] = mod_cnv_postbuild
        # kws['hook_canvas_post_build'] = canvas_setup_post
        # kws['hook_canvas_pre_build'] = common_plot.mod_pre_canv
        # kws['save_name_func'] = lambda w: mk_name(w._renderers[0])+w.name
        kws['canvas_post_build_funcs'] = get_style()
        kws['mod_log'] = common_plot.mod_log_usr()
        return varial.tools.Plotter(stack=False, **kws)
    return tmp

def plotter_factory_comp_trg(**args):

    def tmp(**kws):
        # common_plot.plotter_factory_eff(common_plot.normfactors, **kws)
        kws['filter_keyfunc'] = lambda w: 'base' not in w.in_file_path and (w.in_file_path.endswith('_sub') or w.in_file_path.endswith('_tot'))
        kws['hook_loaded_histos'] = loader_hook_comp_trg
        kws['plot_grouper'] = plot_grouper_comp_trg
        kws['plot_setup'] = plot_setup_comp_trg
        kws['stack_setup'] = plot_setup_comp_trg
        # kws['plot_setup'] = lambda w: stack_setup_norm_sig(w, rate_uncertainties, shape_uncertainties, include_rate)
        # kws['stack_setup'] = lambda w: stack_setup_norm_sig(w, rate_uncertainties, shape_uncertainties, include_rate)
        # kws['canvas_post_build_funcs'] += [rnd.TitleBox(text='CMS Simulation 20fb^{-1} @ 13TeV')]
        # kws['y_axis_scale'] = 'lin'
        kws['hook_canvas_post_build'] = mod_cnv_postbuild
        # kws['hook_canvas_post_build'] = canvas_setup_post
        # kws['hook_canvas_pre_build'] = common_plot.mod_pre_canv
        kws['save_name_func'] = lambda w: comp_trg_group(w._renderers[0])
        kws['canvas_post_build_funcs'] = get_style()
        kws['mod_log'] = common_plot.mod_log_usr()
        kws.update(args)
        return varial.tools.Plotter(stack=False, **kws)
    return tmp

def plotter_factory_gen_plots(**args):

    def tmp(**kws):
        # common_plot.plotter_factory_eff(common_plot.normfactors, **kws)
        kws['filter_keyfunc'] = lambda w: 'GenHists' in w.in_file_path and '_lep_' not in w.file_path
        kws['hook_loaded_histos'] = loader_hook_gen_hists
        # kws['plot_grouper'] = plot_grouper_comp_trg
        # kws['plot_setup'] = lambda w: stack_setup_norm_sig(w, rate_uncertainties, shape_uncertainties, include_rate)
        # kws['stack_setup'] = lambda w: stack_setup_norm_sig(w, rate_uncertainties, shape_uncertainties, include_rate)
        # kws['canvas_post_build_funcs'] += [rnd.TitleBox(text='CMS Simulation 20fb^{-1} @ 13TeV')]
        # kws['y_axis_scale'] = 'lin'
        kws['hook_canvas_post_build'] = mod_cnv_postbuild
        # kws['hook_canvas_post_build'] = canvas_setup_post
        # kws['hook_canvas_pre_build'] = common_plot.mod_pre_canv
        # kws['save_name_func'] = lambda w: comp_trg_group(w._renderers[0])
        kws['canvas_post_build_funcs'] = get_style()
        kws['mod_log'] = common_plot.mod_log_usr()
        kws.update(args)
        return varial.tools.Plotter(stack=False, **kws)
    return tmp

def plotter_factory_split_leps():

    def tmp(**kws):
        # common_plot.plotter_factory_eff(common_plot.normfactors, **kws)
        kws['filter_keyfunc'] = lambda w: '_lep_' in w.file_path
        kws['hook_loaded_histos'] = loader_hook_split_leps
        # kws['plot_grouper'] = plot_grouper_comp_trg
        # kws['plot_setup'] = lambda w: stack_setup_norm_sig(w, rate_uncertainties, shape_uncertainties, include_rate)
        # kws['stack_setup'] = lambda w: stack_setup_norm_sig(w, rate_uncertainties, shape_uncertainties, include_rate)
        # kws['canvas_post_build_funcs'] += [rnd.TitleBox(text='CMS Simulation 20fb^{-1} @ 13TeV')]
        # kws['y_axis_scale'] = 'lin'
        kws['hook_canvas_post_build'] = mod_cnv_postbuild
        # kws['hook_canvas_post_build'] = canvas_setup_post
        # kws['hook_canvas_pre_build'] = common_plot.mod_pre_canv
        # kws['save_name_func'] = lambda w: comp_trg_group(w._renderers[0])
        kws['canvas_post_build_funcs'] = get_style()
        kws['mod_log'] = common_plot.mod_log_usr()
        return varial.tools.Plotter(stack=False, **kws)
    return tmp

def plotter_factory_split_leps_comp_trg():

    def tmp(**kws):
        # common_plot.plotter_factory_eff(common_plot.normfactors, **kws)
        kws['filter_keyfunc'] = lambda w: 'base' not in w.in_file_path and (w.in_file_path.endswith('_sub') or w.in_file_path.endswith('_tot')) and '_lep_' in w.file_path
        kws['hook_loaded_histos'] = loader_hook_split_leps_comp_trg
        kws['plot_grouper'] = plot_grouper_comp_trg
        # kws['canvas_post_build_funcs'] += [rnd.TitleBox(text='CMS Simulation 20fb^{-1} @ 13TeV')]
        # kws['y_axis_scale'] = 'lin'
        kws['hook_canvas_post_build'] = mod_cnv_postbuild
        # kws['hook_canvas_post_build'] = canvas_setup_post
        # kws['hook_canvas_pre_build'] = common_plot.mod_pre_canv
        kws['save_name_func'] = lambda w: comp_trg_group(w._renderers[0])
        kws['canvas_post_build_funcs'] = get_style()
        kws['mod_log'] = common_plot.mod_log_usr()
        return varial.tools.Plotter(stack=False, **kws)
    return tmp

def sframe_setup(outputdir = '', allowed_datasets=None, count = '10000', categories=None, cacheable='False', fs=final_states):
    def tmp_func(element_tree):
        # set_analysis_module(element_tree, analysis_module)
        tptpsframe_runner.set_cacheable_false(element_tree, cacheable)
        tptpsframe_runner.set_output_dir(element_tree, outputdir)
        tptpsframe_runner.clean_input_data(element_tree, allowed_datasets)
        tptpsframe_runner.make_higgs_split_item(element_tree, 'TpTp', fs)
        # make_higgs_split_item(element_tree, 'BpBp', final_states_to_split_into_bp)
        tptpsframe_runner.do_set_eventnumber(element_tree, count)
        # set_uncert(element_tree, uncert_name)
        if categories:
            tptpsframe_runner.do_set_cat(element_tree, " ".join(categories))
    return tmp_func

class MySFrameBatch(SFrame):

    def __init__(self, sel_type='', **kws):
        super(MySFrameBatch, self).__init__(**kws)
        self.sel_type = sel_type

    def configure(self):
        self.xml_doctype = self.xml_doctype +"""
<!--
   <ConfigParse NEventsBreak="50000" FileSplit="0" AutoResubmit="0" />
   <ConfigSGE RAM ="2" DISK ="2" Mail="dominik.nowatschin@cern.de" Notification="as" Workdir="workdir"/>
-->
"""

        if os.path.exists(self.cwd + 'workdir'):
            opt = ' -rl --exitOnQuestion'
        else:
            opt = ' -sl --exitOnQuestion'

        self.exe = 'sframe_batch.py' + opt

def mk_tc_tex(source_dir):
    tc_tex = [
        tex_content.mk_plot_ind(
            (
                ('dr_top_prod', os.path.join(source_dir, 'Plots/PlotsGen/StackedAll/NoSelection/GenHists/spec_max_deltaR_topprod_lin.pdf')),
                ('dr_higg_prod', os.path.join(source_dir, 'Plots/PlotsGen/StackedAll/NoSelection/GenHists/higgs_dRDecay_all_lin.pdf')),
                ('dr_higg_to_bb_prod', os.path.join(source_dir, 'Plots/PlotsGen/StackedAll/NoSelection/GenHists/higgs_to_bb_dRDecay_all_lin.pdf')),
                ('T_pt', os.path.join(source_dir, 'Plots/PlotsGen/StackedAll/NoSelection/GenHists/tprime_pt_all_lin.pdf')),
                ('T_eta', os.path.join(source_dir, 'Plots/PlotsGen/StackedAll/NoSelection/GenHists/tprime_eta_all_lin.pdf')),
                ('T_phi', os.path.join(source_dir, 'Plots/PlotsGen/StackedAll/NoSelection/GenHists/tprime_phi_all_lin.pdf')),
                ('t_pt', os.path.join(source_dir, 'Plots/PlotsGen/StackedAll/NoSelection/GenHists/t_pt_all_lin.pdf')),
                ('t_eta', os.path.join(source_dir, 'Plots/PlotsGen/StackedAll/NoSelection/GenHists/t_eta_all_lin.pdf')),
                ('t_phi', os.path.join(source_dir, 'Plots/PlotsGen/StackedAll/NoSelection/GenHists/t_phi_all_lin.pdf')),
                ('higgs_pt', os.path.join(source_dir, 'Plots/PlotsGen/StackedAll/NoSelection/GenHists/higgs_pt_all_lin.pdf')),
                ('higgs_eta', os.path.join(source_dir, 'Plots/PlotsGen/StackedAll/NoSelection/GenHists/higgs_eta_all_lin.pdf')),
                ('higgs_phi', os.path.join(source_dir, 'Plots/PlotsGen/StackedAll/NoSelection/GenHists/higgs_phi_all_lin.pdf')),
                ('el_pt', os.path.join(source_dir, 'Plots/PlotsGen/StackedAll/NoSelection/GenHists/el_pt_all_lin.pdf')),
                ('mu_pt', os.path.join(source_dir, 'Plots/PlotsGen/StackedAll/NoSelection/GenHists/mu_pt_all_lin.pdf')),
                ('top_pt_vs_max_dR_TpTp_M-1600', os.path.join(source_dir, 'Plots/PlotsGen/StackedAll/NoSelection/GenHists/spec_top_pt_vs_max_dR_TpTp_M-1600_lin.pdf')),
            ), name='GenPlots'),
        tex_content.mk_plot_ind(
            (
                ('el_incl_qcd_eff_pt', os.path.join(source_dir, 'Plots/PlotsCompTrg/StackedAll/NoSelection/FullSelection/electron__full_rebin_flex_eff__QCD_lin.pdf')),
                ('el_incl_T0800_eff_pt', os.path.join(source_dir, 'Plots/PlotsCompTrg/StackedAll/NoSelection/FullSelection/electron__full_rebin_flex_eff__TpTp_M-0800_all_lin.pdf')),
                ('el_incl_T1600_eff_pt', os.path.join(source_dir, 'Plots/PlotsCompTrg/StackedAll/NoSelection/FullSelection/electron__full_rebin_flex_eff__TpTp_M-1600_all_lin.pdf')),
                ('mu_incl_qcd_eff_pt', os.path.join(source_dir, 'Plots/PlotsCompTrg/StackedAll/NoSelection/FullSelection/muon__full_rebin_flex_eff__QCD_lin.pdf')),
                ('mu_incl_T0800_eff_pt', os.path.join(source_dir, 'Plots/PlotsCompTrg/StackedAll/NoSelection/FullSelection/muon__full_rebin_flex_eff__TpTp_M-0800_all_lin.pdf')),
                ('mu_incl_T1600_eff_pt', os.path.join(source_dir, 'Plots/PlotsCompTrg/StackedAll/NoSelection/FullSelection/muon__full_rebin_flex_eff__TpTp_M-1600_all_lin.pdf')),
                ('el_T_T0800_eff_pt', os.path.join(source_dir, 'Plots/PlotsCompTrg/StackedAll/NoSelection/FullSelection/electron__full_rebin_flex_eff__TpTp_M-0800_lep_T_lin.pdf')),
                ('el_T_T1600_eff_pt', os.path.join(source_dir, 'Plots/PlotsCompTrg/StackedAll/NoSelection/FullSelection/electron__full_rebin_flex_eff__TpTp_M-1600_lep_T_lin.pdf')),
                ('mu_T_T0800_eff_pt', os.path.join(source_dir, 'Plots/PlotsCompTrg/StackedAll/NoSelection/FullSelection/muon__full_rebin_flex_eff__TpTp_M-0800_lep_T_lin.pdf')),
                ('mu_T_T1600_eff_pt', os.path.join(source_dir, 'Plots/PlotsCompTrg/StackedAll/NoSelection/FullSelection/muon__full_rebin_flex_eff__TpTp_M-1600_lep_T_lin.pdf')),
                ('el_top_T0800_eff_pt', os.path.join(source_dir, 'Plots/PlotsCompTrg/StackedAll/NoSelection/FullSelection/electron__full_rebin_flex_eff__TpTp_M-0800_lep_top_lin.pdf')),
                ('el_top_T1600_eff_pt', os.path.join(source_dir, 'Plots/PlotsCompTrg/StackedAll/NoSelection/FullSelection/electron__full_rebin_flex_eff__TpTp_M-1600_lep_top_lin.pdf')),
                ('mu_top_T0800_eff_pt', os.path.join(source_dir, 'Plots/PlotsCompTrg/StackedAll/NoSelection/FullSelection/muon__full_rebin_flex_eff__TpTp_M-0800_lep_top_lin.pdf')),
                ('mu_top_T1600_eff_pt', os.path.join(source_dir, 'Plots/PlotsCompTrg/StackedAll/NoSelection/FullSelection/muon__full_rebin_flex_eff__TpTp_M-1600_lep_top_lin.pdf')),
            ), name='TriggerStudies'),        
    ]
    tc_tex_paper = [
        tex_content.mk_plot_ind(
            (
                ('dr_top_prod', os.path.join(source_dir, 'Plots/PlotsGenPaper/StackedAll/NoSelection/GenHists/spec_max_deltaR_topprod_lin.pdf')),
                ('dr_w_all_prod', os.path.join(source_dir, 'Plots/PlotsGenPaper/StackedAll/NoSelection/GenHists/W_dRDecay_all_lin.pdf')),
                ('dr_w_all_prod_rebin', os.path.join(source_dir, 'Plots/PlotsGenPaper/StackedAll/NoSelection/GenHists/W_dRDecay_all_rebin_flex_lin.pdf')),
                ('dr_w_fromT_prod', os.path.join(source_dir, 'Plots/PlotsGenPaper/StackedAll/NoSelection/GenHists/W_from_T_dRDecay_all_lin.pdf')),
                ('w_all_pt', os.path.join(source_dir, 'Plots/PlotsGenPaper/StackedAll/NoSelection/GenHists/W_pt_all_lin.pdf')),
                ('w_fromT_pt', os.path.join(source_dir, 'Plots/PlotsGenPaper/StackedAll/NoSelection/GenHists/W_from_T_pt_all_lin.pdf')),
                ('dr_higg_prod', os.path.join(source_dir, 'Plots/PlotsGenPaper/StackedAll/NoSelection/GenHists/higgs_dRDecay_all_lin.pdf')),
                ('dr_higg_to_bb_prod', os.path.join(source_dir, 'Plots/PlotsGenPaper/StackedAll/NoSelection/GenHists/higgs_to_bb_dRDecay_all_lin.pdf')),
                ('dr_higg_to_bb_prod_rebin', os.path.join(source_dir, 'Plots/PlotsGenPaper/StackedAll/NoSelection/GenHists/higgs_to_bb_dRDecay_all_rebin_flex_lin.pdf')),
                ('higgs_pt', os.path.join(source_dir, 'Plots/PlotsGenPaper/StackedAll/NoSelection/GenHists/higgs_pt_all_lin.pdf')),
            ), name='GenPlots'),
        tex_content.mk_plot_ind(
            (
                ('dr_top_prod', os.path.join(source_dir, 'Plots/PlotsGenPaper/StackedAll/NoSelection/GenHists/spec_max_deltaR_topprod_lin.png')),
                ('dr_w_all_prod', os.path.join(source_dir, 'Plots/PlotsGenPaper/StackedAll/NoSelection/GenHists/W_dRDecay_all_lin.png')),
                ('dr_w_all_prod_rebin', os.path.join(source_dir, 'Plots/PlotsGenPaper/StackedAll/NoSelection/GenHists/W_dRDecay_all_rebin_flex_lin.png')),
                ('dr_w_fromT_prod', os.path.join(source_dir, 'Plots/PlotsGenPaper/StackedAll/NoSelection/GenHists/W_from_T_dRDecay_all_lin.png')),
                ('w_all_pt', os.path.join(source_dir, 'Plots/PlotsGenPaper/StackedAll/NoSelection/GenHists/W_pt_all_lin.png')),
                ('w_fromT_pt', os.path.join(source_dir, 'Plots/PlotsGenPaper/StackedAll/NoSelection/GenHists/W_from_T_pt_all_lin.png')),
                ('dr_higg_prod', os.path.join(source_dir, 'Plots/PlotsGenPaper/StackedAll/NoSelection/GenHists/higgs_dRDecay_all_lin.png')),
                ('dr_higg_to_bb_prod', os.path.join(source_dir, 'Plots/PlotsGenPaper/StackedAll/NoSelection/GenHists/higgs_to_bb_dRDecay_all_lin.png')),
                ('dr_higg_to_bb_prod_rebin', os.path.join(source_dir, 'Plots/PlotsGenPaper/StackedAll/NoSelection/GenHists/higgs_to_bb_dRDecay_all_rebin_flex_lin.png')),
                ('higgs_pt', os.path.join(source_dir, 'Plots/PlotsGenPaper/StackedAll/NoSelection/GenHists/higgs_pt_all_lin.png')),
            ), name='GenPlotsPNG'),
    ]
    tc_tex = varial.tools.ToolChain('CopyPlots', [
        varial.tools.ToolChain('TexThesis', tc_tex),
        varial.tools.ToolChain('TexPaper', tc_tex_paper),
        varial.tools.CopyTool('/afs/desy.de/user/n/nowatsd/Documents/figures_thesis/', src='../TexThesis/*', ignore=('*.svn', '*.html', '*.log'), use_rsync=True, options='-qa --delete', name='CopyToolThesis'),
        # varial.tools.CopyTool('/afs/desy.de/user/n/nowatsd/xxl-af-cms/PlotsToInspect', src='../../*', ignore=('*.svn', '*.log'), use_rsync=True, options='-qa --delete', name='CopyToolInspect'),
        varial.tools.CopyTool('dnowatsc@lxplus.cern.ch:Paper-Dir/papers/B2G-16-024/trunk/', src='../TexPaper/*', ignore=('*.svn', '*.html', '*.log'), options='-qa --delete', use_rsync=True, name='CopyToolPaper'),
        ])
    return tc_tex

def run_sframe(name='Test'):
    sig_samples = [
        # 'TpTp_M-0700',
        'TpTp_M-0800',
        # 'TpTp_M-0900',
        # 'TpTp_M-1000',
        # 'TpTp_M-1100',
        'TpTp_M-1200',
        # 'TpTp_M-1300',
        # 'TpTp_M-1400',
        # 'TpTp_M-1500',
        'TpTp_M-1600',
        # 'TpTp_M-1700',
        # 'TpTp_M-1800',
    ]
    bkg_samples = [
        # 'TTbar',
        # 'WJets_LNu_HT2500ToInf'
        # 'WJets'
        # 'QCD',
        # 'QCD_Pt600to800_MuEnrichedPt5',
        # 'QCD_Pt800to1000_MuEnrichedPt5',
        # 'QCD_Pt1000toInf_MuEnrichedPt5',
        # 'QCD_Pt-300toInf_EMEnriched',
        # 'QCD_Pt_170to250_bcToE',
        # 'QCD_Pt_250toInf_bcToE',
    ]

    # sframe = MySFrameBatch(
    #     cfg_filename=sframe_cfg,
    #     # xml_tree_callback=set_uncert_func(uncert),
    #     xml_tree_callback=sframe_setup(outputdir='./', allowed_datasets=samples, count='-1', cacheable='False'),
    #     name='SFrame',
    #     add_aliases_to_analysis= False,
    #     # name='SFrame_' + uncert,
    #     halt_on_exception=False,
    #     )
    sframe = varial.tools.ToolChainParallel('SFrame', 
        list(SFrame(
                cfg_filename=sframe_cfg,
                # xml_tree_callback=set_uncert_func(uncert),
                xml_tree_callback=sframe_setup(outputdir='./', count='100000', allowed_datasets=[a], cacheable='True', fs=[b]),
                name='workdir_'+a+'_'+b,
                add_aliases_to_analysis=False,
                # name='SFrame_' + uncert,
                halt_on_exception=False)
            for a in sig_samples for b in final_states)
         + list(SFrame(
                cfg_filename=sframe_cfg,
                # xml_tree_callback=set_uncert_func(uncert),
                xml_tree_callback=sframe_setup(outputdir='./', count='500000', allowed_datasets=[a], cacheable='True'),
                name='workdir_'+a,
                add_aliases_to_analysis=False,
                # name='SFrame_' + uncert,
                halt_on_exception=False)
            for a in bkg_samples),
        n_workers=23
        )

    return varial.tools.ToolChain(name, [
        sframe,
        Hadd(
                src_glob_path='../SFrame/workdir*/uhh2.AnalysisModuleRunner.*.root',
                basenames=basenames,
                add_aliases_to_analysis=False,
                samplename_func=plot.get_samplename,
                # filter_keyfunc=lambda w: any(f in w for f in samples_to_plot)
                # overwrite=False
            ),
        varial.tools.ToolChainParallel('Plots', [
            # varial.tools.ToolChain(
            #     'Plots',
            #     lazy_eval_tools_func=plot.mk_plots(pattern='../../Hadd/*.root', web_create=True, plotter_factory=plotter_factory_eff())
            # ),
            # varial.tools.ToolChain(
            #     'PlotsCompTrg',
            #     lazy_eval_tools_func=plot.mk_plots(pattern='../../Hadd/*.root', web_create=True,
            #         plotter_factory=plotter_factory_comp_trg(
            #             canvas_post_build_funcs=get_style() + [
            #                 common_plot.mk_tobject_draw_func(TLatex(0.77, 0.89, "#scale[0.6]{(13 TeV)}")),
            #                 # common_plot.mk_tobject_draw_func(TLatex(0.19, 0.79, "#scale[0.8]{#bf{CMS}}")),
            #                 common_plot.mk_tobject_draw_func(TLatex(0.16, 0.89, "#scale[0.6]{Simulation}")),
            #                 ]
            #             )
            #         )
            # ),
            varial.tools.ToolChain(
                'PlotsGen',
                lazy_eval_tools_func=plot.mk_plots(pattern='../../Hadd/*.root', web_create=True,
                    plotter_factory=plotter_factory_gen_plots(
                        canvas_post_build_funcs=[
                            common_plot.mod_pre_bot_hist(mod_dict),
                            # common_plot.mk_split_err_ratio_plot_func_mod(poisson_errs=True),  # mk_pull_plot_func()
                            # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
                            rnd.mk_legend_func(),
                            common_plot.mod_post_canv(dict_cnv_attr=mod_dict, default_attr=default_canv_attr),
                            # titlebox_func
                            common_plot.mk_tobject_draw_func(TLatex(0.76, 0.89, "#scale[0.6]{(13 TeV)}")),
                            # common_plot.mk_tobject_draw_func(TLatex(0.19, 0.79, "#scale[0.8]{#bf{CMS}}")),
                            common_plot.mk_tobject_draw_func(TLatex(0.16, 0.89, "#scale[0.6]{Simulation}")),
                            ]
                        )
                    )
            ),
            # varial.tools.ToolChain(
            #     'PlotsGenPaper',
            #     lazy_eval_tools_func=plot.mk_plots(pattern='../../Hadd/*.root', web_create=True,
            #         plotter_factory=plotter_factory_gen_plots(
            #             canvas_post_build_funcs=[
            #                 common_plot.mod_pre_bot_hist(mod_dict),
            #                 # common_plot.mk_split_err_ratio_plot_func_mod(poisson_errs=True),  # mk_pull_plot_func()
            #                 # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
            #                 rnd.mk_legend_func(),
            #                 common_plot.mod_post_canv(dict_cnv_attr=mod_dict, default_attr=default_canv_attr),
            #                 # titlebox_func
            #                 common_plot.mk_tobject_draw_func(TLatex(0.76, 0.89, "#scale[0.6]{(13 TeV)}")),
            #                 common_plot.mk_tobject_draw_func(TLatex(0.19, 0.79, "#scale[0.8]{#bf{CMS}}")),
            #                 common_plot.mk_tobject_draw_func(TLatex(0.19, 0.73, "#scale[0.6]{#it{Simulation}}")),
            #                 ])
            #         )
            # ),
            # varial.tools.ToolChain(
            #     'PlotsSplitLeps',
            #     lazy_eval_tools_func=plot.mk_plots(pattern='../../Hadd/*.root', web_create=True, plotter_factory=plotter_factory_split_leps())
            # ),
            # varial.tools.ToolChain(
            #     'PlotsSplitLepsCompTrg',
            #     lazy_eval_tools_func=plot.mk_plots(pattern='../Hadd/*.root', web_create=True, plotter_factory=plotter_factory_split_leps_comp_trg())
            # ),
            ],
        n_workers=1),
        mk_tc_tex(name),
        varial.tools.WebCreator()
    ])



def plot_only(version='Test', pattern=''):
    plots = varial.tools.ToolChain(
        'Plots',
        lazy_eval_tools_func=plot.mk_plots(pattern=pattern, web_create=True, plotter_factory=plotter_factory_eff())
    )
    tc = varial.tools.ToolChain(
        version,
        [
            plots
        ]
    )
    return tc

if __name__ == '__main__':
    time.sleep(1)
    # src_dir = sys.argv[1]
    src_dir = sys.argv[1]
    reuse = True
    if len(sys.argv) > 2:
        reuse = sys.argv[2] == 'True'
    # all_tools = plot_only(version=final_dir, pattern=src_dir)
    all_tools = run_sframe(src_dir)
    varial.tools.Runner(all_tools, default_reuse=reuse)
    # varial.tools.CopyTool('~/www/vlq_analysis/tight_selection2/',
    #     src=final_dir, use_rsync=True).run()