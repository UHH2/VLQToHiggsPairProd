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

from ROOT import TLatex, TH2

varial.settings.max_num_processes = 24

sframe_cfg = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/UHH2/VLQToHiggsPairProd/config/TpTpSignalStudies.xml'

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
    'TTbar': 632,
    'WJets': 860,
    'El45_pt200_pt50' : 2,
    'El105' : 3,
    'El27_iso' : 4,
    'Mu45' : 2,
    'Mu20_iso' : 3,
})

varial.settings.defaults_Legend.update({
    'y_pos': 0.76,
    })

default_canv_attr = dict(common_plot.default_canv_attr)

default_canv_attr.update({
    # 'y_min_gr_zero' : 1e-9,
    'y_max_fct' : 1.3,
    # 'y_max_log_fct' : 1.,
    # 'set_leg_2_col_lin' : False,
    # 'set_leg_2_col_log' : False,
    # 'set_leg_1_col_lin' : False,
    # 'set_leg_1_col_log' : False,
    # 'move_exp' : False,
    # 'no_exp' : False,
})

mod_dict = {
    # 'nomass_boost_2b_mass_softdrop_rebin_flex' : {
    #         'y_max_fct' : 1.3,
    #         'title' : 'M_{jet} [GeV]',
    #         'bin_width' : 5,
    #         'y_min_gr_zero' : 0.02,
    #         'y_max_log_fct' : 1000.,
    #         'scale' : 0.4,
    #         'set_leg_1_col_lin' : {
    #                 'x_pos': 0.74,
    #                 'y_pos': 0.67,
    #                 'label_width': 0.30,
    #                 'label_height': 0.040,
    #                 'box_text_size' : 0.033,
    #                 'opt': 'f',
    #                 'opt_data': 'pl',
    #                 'reverse': True,
    #                 'sort_legend' : lambda w: 'TT ' in w[1],
    #             },
    #         'text_box_lin' : (0.19, 0.82, "#scale[0.8]{#bf{CMS}}"),
    #         },
    }

def get_style():
    # _style = style or varial.settings.style
    return [
        common_plot.mod_pre_bot_hist(),
        common_plot.mk_split_err_ratio_plot_func_mod(poisson_errs=True),  # mk_pull_plot_func()
        # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
        rnd.mk_legend_func(),
        common_plot.mod_post_canv(default_attr=default_canv_attr),
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
            x_ax_pre = 'Electron'
        elif 'muon' in w.name:
            x_ax_pre = 'Muon'
        else:
            x_ax_pre = 'AK8 Jet'
        if 'pt' in w.name:
            x_ax_post = ' p_{T} [GeV]'
        elif 'eta' in w.name:
            x_ax_post = ' #eta'
        elif 'mass' in w.name:
            x_ax_post = ' Mass [GeV]'
        elif 'nsjbtags' in w.name:
            x_ax_post = ' N(sj b-tags)'
        else:
            x_ax_post = ''
        if isinstance(w, varial.wrappers.HistoWrapper):
            w.histo.GetXaxis().SetTitle(x_ax_pre+x_ax_post)
        elif isinstance(w, varial.wrappers.GraphWrapper):
            w.graph.GetXaxis().SetTitle(x_ax_pre+x_ax_post)

        if '1b' in w.name:
            y_ax_post = ' (H-tag, #geq 1 sj b-tag)'
        elif '2b' in w.name:
            y_ax_post = ' (H-tag, 2 sj b-tags)'
        else:
            y_ax_post = ''
        if 'eff' in w.name:
            if isinstance(w, varial.wrappers.HistoWrapper):
                w.histo.GetYaxis().SetTitle('Efficiency'+y_ax_post)
            elif isinstance(w, varial.wrappers.GraphWrapper):
                w.graph.GetYaxis().SetTitle('Efficiency'+y_ax_post)

        yield w

def mod_title_norm(wrps):
    for w in wrps:
        w.histo.GetYaxis().SetTitle('A. U.')
        yield w

rebin_list_pt = list(i for i in xrange(0, 1000, 40))
rebin_list_pt += list(i for i in xrange(1000, 1600, 120))
rebin_list_pt += list(i for i in xrange(1600, 2400, 240))

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
    for w in wrps:
        if w.name.startswith('electron'):
            chan = 'El'
            suf = '45_pt200_pt50'
            if '105' in w.name:
                suf = '105'
            elif 'iso' in w.name:
                suf = '27_iso'
        elif w.name.startswith('muon'):
            chan = 'Mu'
            suf = '45'
            if 'iso' in w.name:
                suf = '20_iso'
        w.legend = chan + suf
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
    # wrps = common_plot.rebin_st_and_nak4(wrps)
    # wrps = plot.common_loader_hook(wrps)
    wrps = rebin(wrps)
    # wrps = rebin_fix(wrps)
    wrps = common_plot.add_wrp_info(wrps, sig_ind=common_plot.signal_indicators) # , use_hadd_sample=False
    wrps = filter_signal(wrps)
    wrps = common_plot.mod_legend(wrps)
    wrps = vlq_common.label_axes(wrps)

    wrps = sorted(wrps, key=lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))
    wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw'], print_warning=False, yield_orig=False)
    wrps = gen.gen_norm_to_integral(wrps)
    wrps = mod_title_norm(wrps)
    # wrps = sorted(wrps, key=lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))
    # wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw'], suffix='_thX', print_warning=False, yield_orig=True)
    # wrps = sorted(wrps, key=lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))
    # wrps = vlq_common.merge_decay_channels(wrps, ['_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_other', print_warning=False, yield_orig=False)
    wrps = gen.gen_make_eff_graphs(wrps, yield_everything=True, pair_func=lambda w, l: w.sample+'_'+w.in_file_path[:-l])
    wrps = mk_marker(wrps)
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
    wrps = rebin(wrps)
    # wrps = rebin_fix(wrps)
    wrps = common_plot.add_wrp_info(wrps, sig_ind=common_plot.signal_indicators) # , use_hadd_sample=False
    wrps = common_plot.mod_legend(wrps)
    wrps = mod_legend_comp_trg(wrps)
    wrps = vlq_common.label_axes(wrps)

    wrps = sorted(wrps, key=lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))
    wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_all', print_warning=False, yield_orig=True)
    wrps = sorted(wrps, key=lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))
    wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw'], suffix='_thX', print_warning=False, yield_orig=True)
    wrps = sorted(wrps, key=lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))
    wrps = vlq_common.merge_decay_channels(wrps, ['_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_other', print_warning=False, yield_orig=False)
    wrps = gen.gen_make_eff_graphs(wrps, yield_everything=True, pair_func=lambda w, l: w.sample+'_'+w.in_file_path[:-l])
    wrps = mk_marker(wrps)
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

def plotter_factory_comp_trg():

    def tmp(**kws):
        # common_plot.plotter_factory_eff(common_plot.normfactors, **kws)
        kws['filter_keyfunc'] = lambda w: 'base' not in w.in_file_path and (w.in_file_path.endswith('_sub') or w.in_file_path.endswith('_tot'))
        kws['hook_loaded_histos'] = loader_hook_comp_trg
        kws['plot_grouper'] = plot_grouper_comp_trg
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
        return varial.tools.Plotter(stack=False, **kws)
    return tmp

def plotter_factory_gen_plots():

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
                ('dr_top_prod', os.path.join(source_dir, 'PlotsGen/StackedAll/NoSelection/GenHists/spec_max_deltaR_topprod_lin.pdf')),
                ('dr_higg_prod', os.path.join(source_dir, 'PlotsGen/StackedAll/NoSelection/GenHists/higgs_dRDecay_all_lin.pdf')),
                ('T_pt', os.path.join(source_dir, 'PlotsGen/StackedAll/NoSelection/GenHists/tprime_pt_all_lin.pdf')),
                ('T_eta', os.path.join(source_dir, 'PlotsGen/StackedAll/NoSelection/GenHists/tprime_eta_all_lin.pdf')),
                ('T_phi', os.path.join(source_dir, 'PlotsGen/StackedAll/NoSelection/GenHists/tprime_phi_all_lin.pdf')),
                ('t_pt', os.path.join(source_dir, 'PlotsGen/StackedAll/NoSelection/GenHists/t_pt_all_lin.pdf')),
                ('t_eta', os.path.join(source_dir, 'PlotsGen/StackedAll/NoSelection/GenHists/t_eta_all_lin.pdf')),
                ('t_phi', os.path.join(source_dir, 'PlotsGen/StackedAll/NoSelection/GenHists/t_phi_all_lin.pdf')),
                ('higgs_pt', os.path.join(source_dir, 'PlotsGen/StackedAll/NoSelection/GenHists/higgs_pt_all_lin.pdf')),
                ('higgs_eta', os.path.join(source_dir, 'PlotsGen/StackedAll/NoSelection/GenHists/higgs_eta_all_lin.pdf')),
                ('higgs_phi', os.path.join(source_dir, 'PlotsGen/StackedAll/NoSelection/GenHists/higgs_phi_all_lin.pdf')),
                ('el_pt', os.path.join(source_dir, 'PlotsGen/StackedAll/NoSelection/GenHists/el_pt_all_lin.pdf')),
                ('mu_pt', os.path.join(source_dir, 'PlotsGen/StackedAll/NoSelection/GenHists/mu_pt_all_lin.pdf')),
                ('top_pt_vs_max_dR_TpTp_M-1600', os.path.join(source_dir, 'PlotsGen/StackedAll/NoSelection/GenHists/spec_top_pt_vs_max_dR_TpTp_M-1600_lin.pdf')),
            ), name='GenPlots'),
        tex_content.mk_plot_ind(
            (
                ('el_incl_qcd_eff_pt', os.path.join(source_dir, 'PlotsCompTrg/StackedAll/NoSelection/FullSelection/electron__full_rebin_flex_eff__QCD_lin.pdf')),
                ('el_incl_T0800_eff_pt', os.path.join(source_dir, 'PlotsCompTrg/StackedAll/NoSelection/FullSelection/electron__full_rebin_flex_eff__TpTp_M-0800_all_lin.pdf')),
                ('el_incl_T1600_eff_pt', os.path.join(source_dir, 'PlotsCompTrg/StackedAll/NoSelection/FullSelection/electron__full_rebin_flex_eff__TpTp_M-1600_all_lin.pdf')),
                ('mu_incl_qcd_eff_pt', os.path.join(source_dir, 'PlotsCompTrg/StackedAll/NoSelection/FullSelection/muon__full_rebin_flex_eff__QCD_lin.pdf')),
                ('mu_incl_T0800_eff_pt', os.path.join(source_dir, 'PlotsCompTrg/StackedAll/NoSelection/FullSelection/muon__full_rebin_flex_eff__TpTp_M-0800_all_lin.pdf')),
                ('mu_incl_T1600_eff_pt', os.path.join(source_dir, 'PlotsCompTrg/StackedAll/NoSelection/FullSelection/muon__full_rebin_flex_eff__TpTp_M-1600_all_lin.pdf')),
                ('el_T_T0800_eff_pt', os.path.join(source_dir, 'PlotsCompTrg/StackedAll/NoSelection/FullSelection/electron__full_rebin_flex_eff__TpTp_M-0800_lep_T_lin.pdf')),
                ('el_T_T1600_eff_pt', os.path.join(source_dir, 'PlotsCompTrg/StackedAll/NoSelection/FullSelection/electron__full_rebin_flex_eff__TpTp_M-1600_lep_T_lin.pdf')),
                ('mu_T_T0800_eff_pt', os.path.join(source_dir, 'PlotsCompTrg/StackedAll/NoSelection/FullSelection/muon__full_rebin_flex_eff__TpTp_M-0800_lep_T_lin.pdf')),
                ('mu_T_T1600_eff_pt', os.path.join(source_dir, 'PlotsCompTrg/StackedAll/NoSelection/FullSelection/muon__full_rebin_flex_eff__TpTp_M-1600_lep_T_lin.pdf')),
                ('el_top_T0800_eff_pt', os.path.join(source_dir, 'PlotsCompTrg/StackedAll/NoSelection/FullSelection/electron__full_rebin_flex_eff__TpTp_M-0800_lep_top_lin.pdf')),
                ('el_top_T1600_eff_pt', os.path.join(source_dir, 'PlotsCompTrg/StackedAll/NoSelection/FullSelection/electron__full_rebin_flex_eff__TpTp_M-1600_lep_top_lin.pdf')),
                ('mu_top_T0800_eff_pt', os.path.join(source_dir, 'PlotsCompTrg/StackedAll/NoSelection/FullSelection/muon__full_rebin_flex_eff__TpTp_M-0800_lep_top_lin.pdf')),
                ('mu_top_T1600_eff_pt', os.path.join(source_dir, 'PlotsCompTrg/StackedAll/NoSelection/FullSelection/muon__full_rebin_flex_eff__TpTp_M-1600_lep_top_lin.pdf')),
            ), name='TriggerStudies'),
        # tex_content.mk_plot_ind(
        #     (
        #         ('higgs_tag_mass', os.path.join(base_path, source_dir)+'/HiggsPlots/HistogramsHiggsComp/StackedAll/BaseLineSelection/nomass_boost_2b_mass_softdrop_lin.pdf'),
        #         ('higgs_tag_sjbtags', os.path.join(base_path, source_dir)+'/HiggsPlots/HistogramsHiggsComp/StackedAll/BaseLineSelection/nobtag_boost_mass_nsjbtags_log.pdf'),
        #         ('st_sideband_ttbar', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/ST_rebin_flex_log.pdf'),
        #         ('st_sideband_wjets', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/ST_rebin_flex_log.pdf'),
        #         ('st_h1b', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SignalRegion1b/ST_rebin_flex_log.pdf'),
        #         ('st_h2b', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SignalRegion2b/ST_rebin_flex_log.pdf'),
        #         ('st_h2b_lin', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SignalRegion2b/ST_rebin_flex_lin.pdf'),
        #     ), name='PaperPlotsPrefit'),
        # tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/Tables/EffTableCompFS/count_table_content.tex', name='EffTableCompFS'),
        # # tex_content.mk_autoTable(path_an+'/MergeChannelsTablesNoTheory/CountTablePAS/count_table_content.tex', name='CountTable'),
        # tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/Tables/CountTablePostFit/count_table_content.tex', name='CountTablePostFit'),
        # tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/Tables/CountTablePreFit/count_table_content.tex', name='CountTablePreFit'),
        # tex_content.mk_autoContentSysTabs(os.path.join(base_path, source_dir)+'/Ind_Limits/Limit_bW0p5_tZ0p25_tH0p25/ThetaLimits', 'SysTabs', mass_points=['TTM0700', 'TTM1200', 'TTM1700'], regions=regions),
        # tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/MergeChannelsTablesNoTheory/EffTableCompFSPAS/count_table_content.tex', name='EffTableCompFS_'+name),
        # tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/MergeChannelsTablesNoTheory/CountTablePAS/count_table_content.tex', name='CountTable_'+name),
        # tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/BackgroundOnlyFitNoTheory/CR/PostFitPlots/CountTablePostFitPAS/count_table_content.tex', name='CountTablePostFit_'+name),
        
    ]
    tc_tex = varial.tools.ToolChain('CopyPlots', [
        varial.tools.ToolChain('TexThesis', tc_tex),
        varial.tools.CopyTool('/afs/desy.de/user/n/nowatsd/Documents/figures_thesis/', src='../TexThesis/*', ignore=('*.svn', '*.html', '*.log'), use_rsync=True, options='-qa --delete'),
        ])
    return tc_tex

def run_sframe(name='Test'):
    sig_samples = [
        # 'TpTp_M-0700',
        'TpTp_M-0800',
        # 'TpTp_M-0900',
        # 'TpTp_M-1000',
        # 'TpTp_M-1100',
        # 'TpTp_M-1200',
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
        'QCD_Pt600to800_MuEnrichedPt5',
        'QCD_Pt800to1000_MuEnrichedPt5',
        'QCD_Pt1000toInf_MuEnrichedPt5',
        'QCD_Pt-300toInf_EMEnriched',
        'QCD_Pt_170to250_bcToE',
        'QCD_Pt_250toInf_bcToE',
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
        varial.tools.ToolChain(
            'Plots',
            lazy_eval_tools_func=plot.mk_plots(pattern='../Hadd/*.root', web_create=True, plotter_factory=plotter_factory_eff())
        ),
        varial.tools.ToolChain(
            'PlotsCompTrg',
            lazy_eval_tools_func=plot.mk_plots(pattern='../Hadd/*.root', web_create=True, plotter_factory=plotter_factory_comp_trg())
        ),
        varial.tools.ToolChain(
            'PlotsGen',
            lazy_eval_tools_func=plot.mk_plots(pattern='../Hadd/*.root', web_create=True, plotter_factory=plotter_factory_gen_plots())
        ),
        varial.tools.ToolChain(
            'PlotsSplitLeps',
            lazy_eval_tools_func=plot.mk_plots(pattern='../Hadd/*.root', web_create=True, plotter_factory=plotter_factory_split_leps())
        ),
        # varial.tools.ToolChain(
        #     'PlotsSplitLepsCompTrg',
        #     lazy_eval_tools_func=plot.mk_plots(pattern='../Hadd/*.root', web_create=True, plotter_factory=plotter_factory_split_leps_comp_trg())
        # ),
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