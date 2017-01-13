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
# import varial.analysis as analysis
# from varial.sample import Sample
# from varial.extensions.sframe import SFrame
from varial.extensions.hadd import Hadd
import varial.wrappers as wrappers
import varial.operations as op

import UHH2.VLQSemiLepPreSel.cutflow_tables as cutflow_tables
import UHH2.VLQSemiLepPreSel.common as vlq_common

# import common_vlq
import tptp_settings
# import final_plotting
import common_plot_new as common_plot
# import tptp_sframe 
# import compare_crs
import analysis

from ROOT import TLatex, TH2

# varial.settings.max_num_processes = 1

#====PLOTTING====

#====DEFINITIONS====

src_dir_rel = '../Hadd'

normsignal = 20.

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
    '_bhbh' : 1./0.111,
    '_bzbz' : 1./0.111,
    '_twtw' : 1./0.111,
    '_bhbz' : 1./0.222,
    '_bhtw' : 1./0.222,
    '_bztw' : 1./0.222,
}

normfactors_ind_fs_rev = {
    '_thth' : 0.111,
    '_tztz' : 0.111,
    '_bwbw' : 0.111,
    '_thtz' : 0.222,
    '_thbw' : 0.222,
    '_tzbw' : 0.222,
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
    'TpTp_M-0800',
    'TpTp_M-0900',
    'TpTp_M-1000',
    'TpTp_M-1100',
    'TpTp_M-1200',
    'TpTp_M-1300',
    # 'TpTp_M-1400',
    'TpTp_M-1500',
    'TpTp_M-1600',
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

almost_all_signals = [
    'TpTp_M-0700',
    'TpTp_M-0800',
    'TpTp_M-0900',
    'TpTp_M-1000',
    'TpTp_M-1100',
    'TpTp_M-1200',
    'TpTp_M-1300',
    # 'TpTp_M-1400',
    'TpTp_M-1500',
    'TpTp_M-1600',
    'TpTp_M-1700',
    # 'TpTp_M-1800',
]

backgrounds_wo_ttbar = [
    'SingleTop',
    'QCD',
    'DYJets',
    'WJets',
    'Run2015CD',
    'Diboson'
]

other_samples_to_plot = backgrounds_wo_ttbar + ['TTbar_split']
other_samples_to_plot_pre = backgrounds_wo_ttbar + ['TTbar']

samples_to_plot_final = other_samples_to_plot + reduce(lambda x, y: x+y, (list(g + f for f in final_states_to_plot) for g in signals_to_plot))
more_samples = other_samples_to_plot + reduce(lambda x, y: x+y, (list(g + f for f in final_states_to_plot) for g in more_signals))
less_samples = other_samples_to_plot + reduce(lambda x, y: x+y, (list(g + f for f in final_states_to_plot) for g in less_signals))
almost_all_samples = other_samples_to_plot + reduce(lambda x, y: x+y, (list(g + f for f in final_states_to_plot) for g in almost_all_signals))

samples_to_plot_only_th = other_samples_to_plot + list(g + '_thth' for g in signals_to_plot)
more_samples_to_plot_only_th = other_samples_to_plot + list(g + '_thth' for g in more_signals)
less_samples_to_plot_only_th = other_samples_to_plot + list(g + '_thth' for g in less_signals)

samples_to_plot_pre = other_samples_to_plot_pre + signals_to_plot
less_samples_to_plot_pre = other_samples_to_plot_pre + less_signals

get_samplename = vlq_common.get_samplename


def common_loader_hook(wrps):
    wrps = common_plot.add_wrp_info(wrps, sig_ind=common_plot.signal_indicators) # , use_hadd_sample=False
    wrps = common_plot.mod_legend(wrps)
    wrps = (w for w in wrps if w.histo.Integral() > 1e-20)
    wrps = vlq_common.label_axes(wrps)
    wrps = common_plot.mod_title(wrps)
    return wrps


#=======FOR ALL PLOTS=======



def loader_hook_finalstates_excl(wrps):
    # wrps = varial.gen.gen_noex_rebin_nbins_max(wrps, nbins_max=60)
    wrps = common_plot.rebin_st_and_nak4(wrps)
    wrps = common_loader_hook(wrps)
    wrps = common_plot.norm_smpl(wrps, common_plot.pas_normfactors)
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
    wrps = sorted(wrps, key=lambda w: w.in_file_path)
    return wrps



def loader_hook_norm_to_int(wrps):
    key = lambda w: '{0}___{1}___{2}___{3}'.format(w.in_file_path, w.is_data, w.is_signal if not w.is_signal else w.sample, w.sys_info)

    # wrps = loader_hook_finalstates_excl(wrps)
    wrps = sorted(wrps, key=key)
    wrps = varial.gen.group(wrps, key)
    wrps = varial.gen.gen_merge(wrps)
    wrps = common_plot.norm_to_int(wrps)
    return wrps

# def add_sfel_trg_uncert():


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
    wrps = list(wrps)
    for w in wrps:
        if w.sys_info.startswith('sfel') or w.sys_info.startswith('sfmu'):
            print get_base_selection(w), w.sample, w.sys_info, w.variable
    return wrps

def loader_hook_merge_lep_channels(wrps):
    # wrps = merge_regions(wrps)
    # wrps = itertools.ifilter(lambda w: all(f not in w.sample for f in ['_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw', '_incl']), wrps)
    wrps = common_loader_hook(wrps)
    wrps = common_plot.norm_smpl(wrps, common_plot.pas_normfactors)
    wrps = common_plot.mod_title(wrps)
    wrps = common_plot.mod_legend_no_thth(wrps)
    if not varial.settings.flex_sig_norm:
        wrps = common_plot.norm_to_fix_xsec(wrps, True)
    wrps = common_plot.rebin_st_and_nak4(wrps)
    wrps = sorted(wrps, key=lambda w: w.region+'__'+w.name)
    return wrps


def loader_hook_compare_finalstates(wrps):
    wrps = common_plot.rebin_st_and_nak4(wrps)
    wrps = common_loader_hook(wrps)
    wrps = common_plot.norm_smpl(wrps, common_plot.pas_normfactors)
    wrps = common_plot.norm_smpl(wrps, normfactors_ind_fs_rev, calc_scl_fct=False)
    wrps = sorted(wrps, key=lambda w: '{0}___{1}___{2}'.format(w.sys_info, w.in_file_path, w.sample))
    wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw'], suffix='_thX', print_warning=False)
    wrps = sorted(wrps, key=lambda w: '{0}___{1}___{2}'.format(w.sys_info, w.in_file_path, w.sample))
    wrps = vlq_common.merge_decay_channels(wrps, ['_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_other', print_warning=False)
    wrps = common_plot.mod_legend_eff_counts(wrps)
    if not varial.settings.flex_sig_norm:
        wrps = common_plot.norm_to_fix_xsec(wrps, True)
    wrps = gen.sort(wrps, ['in_file_path'])
    return wrps

def loader_hook_uncerts(wrps, rate_uncertainties=analysis.rate_uncertainties, shape_uncertainties=analysis.shape_uncertainties, include_rate=False):
    wrps = sorted(wrps, key=lambda w: w.in_file_path)
    wrps = gen.group(wrps, lambda w: w.in_file_path)
    wrps = common_plot.make_uncertainty_histograms(wrps, rate_uncertainties, shape_uncertainties, include_rate)
    wrps = list(w for ws in wrps for w in ws)
    wrps = common_plot.set_line_width(wrps)
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

# def canvas_setup_post(grps):
#     grps = common_plot.add_sample_integrals(grps)
#     grps = common_plot.mod_post_canv(grps)
#     return grps


def stack_setup_norm_sig(grps, rate_uncertainties=analysis.rate_uncertainties, shape_uncertainties=analysis.shape_uncertainties, include_rate=False):
    grps = common_plot.make_uncertainty_histograms(grps, rate_uncertainties, shape_uncertainties, include_rate)
    grps = gen.mc_stack_n_data_sum(grps, calc_sys_integral=True, add_sys_errs=True)
    if varial.settings.flex_sig_norm:
        grps = common_plot.norm_to_bkg(grps)
    # grps = common_plot.make_empty_bin_error(grps)
    return grps

def stack_setup_norm_all_to_intgr(grps, rate_uncertainties=analysis.rate_uncertainties, shape_uncertainties=analysis.shape_uncertainties, include_rate=False):
    grps = common_plot.make_uncertainty_histograms(grps, rate_uncertainties, shape_uncertainties, include_rate)
    grps = gen.mc_stack_n_data_sum(grps, calc_sys_integral=False, add_sys_errs=True)
    # grps = common_plot.norm_stack_to_integral(grps)
    return grps

# def plot_grouper_by_in_file_path_mod(wrps, separate_th2=True):
#     if separate_th2:
#         wrps = varial.plotter.rename_th2(wrps)
#     wrps = common_plot.copy_wrp_for_log(wrps)
#     wrps = sorted(wrps, key=lambda w: w.scale+'___'+w.in_file_path)
#     return gen.group(wrps, key_func=lambda w: w.scale+'___'+w.in_file_path)

def plot_grouper_by_uncerts(wrps, separate_th2=True):
    if separate_th2:
        wrps = varial.plotter.rename_th2(wrps)
    wrps = common_plot.copy_wrp_for_log(wrps)
    wrps = sorted(wrps, key=lambda w: '{0}___{1}___{2}'.format(w.scale, w.in_file_path, w.sample))
    wrps = group_by_uncerts(wrps, lambda w: '{0}___{1}___{2}'.format(w.scale, w.in_file_path, w.sample))
    # wrps = sorted(wrps, key=lambda w: w.scale+'___'+w.in_file_path)
    return wrps

def plotter_factory_stack(rate_uncertainties=analysis.rate_uncertainties, shape_uncertainties=analysis.shape_uncertainties, include_rate=False, **args):
    def tmp(**kws):
        # common_plot.plotter_factory_stack(common_plot.normfactors, **kws)
        # kws['filter_keyfunc'] = lambda w: (f in w.sample for f in datasets_to_plot)
        kws['hook_loaded_histos'] = loader_hook_finalstates_excl
        # kws['plot_grouper'] = plot_grouper_by_in_file_path_mod
        kws['plot_setup'] = lambda w: stack_setup_norm_sig(w, rate_uncertainties, shape_uncertainties, include_rate)
        kws['stack_setup'] = lambda w: stack_setup_norm_sig(w, rate_uncertainties, shape_uncertainties, include_rate)
        # kws['canvas_post_build_funcs'] += [rnd.TitleBox(text='CMS Simulation 20fb^{-1} @ 13TeV')]
        # kws['y_axis_scale'] = 'lin'
        kws['hook_canvas_post_build'] = common_plot.add_sample_integrals
        # kws['hook_canvas_post_build'] = canvas_setup_post
        # kws['hook_canvas_pre_build'] = common_plot.mod_pre_canv
        kws['canvas_post_build_funcs'] = common_plot.get_style()
        kws['mod_log'] = common_plot.mod_log_usr()
        kws.update(**args)
        return varial.tools.Plotter(**kws)
    return tmp


def plotter_factory_uncerts(rate_uncertainties=analysis.rate_uncertainties, shape_uncertainties=analysis.shape_uncertainties, include_rate=False, **args):
    def tmp(**kws):
        # common_plot.plotter_factory_stack(common_plot.normfactors, **kws)
        # kws['filter_keyfunc'] = lambda w: (f in w.sample for f in datasets_to_plot)
        kws['hook_loaded_histos'] = lambda w: loader_hook_uncerts(loader_hook_finalstates_excl(w), rate_uncertainties, shape_uncertainties, include_rate)
        kws['plot_grouper'] = lambda g: group_by_uncerts(g, lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))
        kws['plot_setup'] = plot_setup_uncerts
        kws['hook_canvas_post_build'] = common_plot.add_sample_integrals
        kws['canvas_post_build_funcs'] = [
            # common_plot.mod_pre_bot_hist(),
            common_plot.mk_bottom_plot_ratio_uncerts(),  # mk_pull_plot_func()
            # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
            rnd.mk_legend_func(),
            # common_plot.mod_post_canv(mod_dict),
            ]
        kws.update(**args)
        return varial.tools.Plotter(**kws)
    return tmp

def mk_plots(datasets=None, parallel=True, web_create=False, **kws):
    if datasets:
        dataset_filter = lambda w: any(f in os.path.basename(w.file_path) for f in datasets)
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
        n_workers = None if parallel else 1
        plot_chain = [varial.plotter.RootFilePlotter(n_workers=n_workers, **args)]
        if web_create:
            plot_chain += [varial.tools.WebCreator()]
        return plot_chain
    return create

def mk_toolchain(name, datasets=None, parallel=True, web_create=False, **kws):
    return varial.tools.ToolChain(
        name,
        lazy_eval_tools_func=mk_plots(datasets, parallel, web_create, **kws)
        )


def plot_only(version='Test', pattern=''):
    plots = varial.tools.ToolChain(
        'Plots',
        lazy_eval_tools_func=mk_plots(pattern=pattern, web_create=True)
    )
    tc = varial.tools.ToolChain(
        version,
        [
            plots
        ]
    )
    return tc
        
# def plot_merged_channels(final_dir):
#     source_dir = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/'\
#         'UHH2/VLQToHiggsPairProd/NewSamples-76X-v1/FinalSelection-v24/'\
#         'Run8_withHighMassTTbarSample/RunAnalysis/HTReweighting/TreeProject'
#     uncerts = analysis.all_uncerts # or get_sys_dir()
#     nom_pattern = [source_dir+'/TreeProjector/{0}.root',
#                    source_dir+'/TreeProjectorDiboson/{0}.root']
#     sys_pattern = list(source_dir+'/SysTreeProjectors/%s*/{0}.root'% i for i in uncerts) +\
#                   list(source_dir+'/SysTreeProjectorsDiboson/%s*/{0}.root'% i for i in uncerts)
#     input_pattern = nom_pattern+sys_pattern
#     # plot_hists = ['ST', 'HT', 'n_ak4', 'topjets[0].m_pt', 'topjets[1].m_pt',
#     #                 'n_ak8', 'met', 'pt_ld_ak4_jet', 'pt_subld_ak4_jet', 'jets[2].m_pt','jets[3].m_pt', 'jets[].m_pt', 'n_additional_btags_medium', 'n_prim_vertices',
#     #                 'n_higgs_tags_1b_med_sm10', 'n_higgs_tags_2b_med_sm10', 'primary_electron_pt', 'primary_muon_pt', 'PrimaryLepton.Particle.m_eta', 'wtags_mass_softdrop',
#     #                 'nobtag_boost_mass_nsjbtags', 'nomass_boost_1b_mass_softdrop', 'nomass_boost_2b_mass_softdrop', 'noboost_mass_1b[0].m_pt', 'noboost_mass_2b[0].m_pt']
#     plot_hists = ['ST', 'HT', 'n_ak4', 'nomass_boost_1b_mass_softdrop', 'nomass_boost_2b_mass_softdrop', 'noboost_mass_1b[0].m_pt', 'noboost_mass_2b[0].m_pt', 'nobtag_boost_mass_nsjbtags']

#     return varial.tools.ToolChain(final_dir, [
#         varial.tools.ToolChainParallel('HistoLoader',
#         list(varial.tools.HistoLoader(
#             pattern=map(lambda w: w.format('*'+g+'*'), input_pattern),
#             filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in less_samples) and\
#                 'Region_Comb' not in w.in_file_path and\
#                 any(w.in_file_path.endswith(f) for f in plot_hists) and\
#                 common_plot.unselect_theory_uncert(w),
#             hook_loaded_histos=loader_hook_merge_regions,
#             name='HistoLoader_'+g,
#             lookup_aliases=False,
#             raise_on_empty_result=False,
#             quiet_mode=True
#             ) for g in less_samples)),
#         # mk_toolchain('Histograms', less_samples_to_plot_only_th,
#         #     plotter_factory=plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=True, hook_loaded_histos=loader_hook_merge_lep_channels),
#         #     pattern=None, input_result_path='../HistoLoader/HistoLoader*'),
#         # mk_toolchain('HistogramsCompUncerts', less_samples_to_plot_only_th,
#         #     filter_keyfunc=lambda w: any(f in w.file_path for f in [treeproject_tptp.ttbar_smpl, 'QCD', 'WJets', 'TpTp_M-0800', 'TpTp_M-1600']) and any(w.in_file_path.endswith(g) for g in ['ST', 'HT']),   
#         #     plotter_factory=plotter_factory_uncerts(
#         #         hook_loaded_histos=lambda w: loader_hook_uncerts(loader_hook_merge_lep_channels(w), 
#         #             analysis.rate_uncertainties, uncerts, include_rate=True)),
#         #     pattern=None, input_result_path='../HistoLoader/HistoLoader*'),
#         # mk_toolchain('HistogramsNormToInt',
#         #     filter_keyfunc=lambda w: 'TpTp' not in w.file_path,
#         #     pattern=None, input_result_path='../HistoLoader/HistoLoader*',
#         #     plotter_factory=plotter_factory_stack(analysis.rate_uncertainties, def_uncerts, hook_loaded_histos=loader_hook_norm_to_int,
#         #         plot_setup=stack_setup_norm_all_to_intgr)),
#         mk_toolchain('HistogramsHiggsComp', pattern=None, input_result_path='../HistoLoader/HistoLoader*',
#             filter_keyfunc=lambda w: all(g not in w.sample for g in ['TpTp_M-0800', 'TpTp_M-1600']),
#             plotter_factory=plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=True, 
#                 hook_loaded_histos=loader_hook_compare_finalstates,
#                 ),
#             parallel=True
#             # pattern=None, input_result_path='../HistoLoader/HistoLoader*'
#             ),
#         # mk_toolchain('HistogramsNoDataHiggsComp', pattern=None, input_result_path='../HistoLoader/HistoLoader*',
#         #     filter_keyfunc=lambda w: 'Run2015CD' not in w.file_path.split('/')[-1] and all(g not in w.sample for g in ['TpTp_M-0800', 'TpTp_M-1600']),
#         #     plotter_factory=plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=True, 
#         #         hook_loaded_histos=loader_hook_compare_finalstates,
#         #         )
#         #     ),
#         varial.tools.WebCreator()
#         ])

# sframe_tools = mk_sframe_and_plot_tools()

import sys

if __name__ == '__main__':
    time.sleep(1)
    # src_dir = sys.argv[1]
    src_dir = sys.argv[1]
    final_dir = sys.argv[2]
    all_tools = plot_only(version=final_dir, pattern=src_dir)
    varial.tools.Runner(all_tools, default_reuse=True)
    # varial.tools.CopyTool('~/www/vlq_analysis/tight_selection2/',
    #     src=final_dir, use_rsync=True).run()