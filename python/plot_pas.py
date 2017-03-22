#!/usr/bin/env python

import sys
import os
import time
import itertools
import copy

import varial.settings as settings
import varial.rendering as rnd
import varial.generators as gen
import varial.wrappers as wrappers
import varial.tools
import UHH2.VLQSemiLepPreSel.common as vlq_common


# import common_vlq
import tptp_settings
# import final_plotting
import common_plot_new as common_plot
import plot_new as plot
# import tptp_sframe 
# import compare_crs
import analysis
import sensitivity
import combination_limits
import tex_content_new as tex_content
from get_eff_count import CountTable, EffTable # EffNumTable, 

from ROOT import TLatex, TH2
import ROOT

settings.canvas_size_x = 600
settings.canvas_size_y = 500

settings.tot_error_color = ROOT.kBlack
settings.tot_error_fill = 3004

settings.defaults_BottomPlot['y_min'] = -1.99
settings.defaults_BottomPlot['y_max'] = 1.99

settings.defaults_Legend.update({
    'y_pos': 0.76,
    })

settings.colors.update({
    # 'Background' : 920,
    # 'nominal' : 1,
    # 'plus' : 2,
    # 'minus' : 3,
    # 'TTbar': 632 - 7,
    # 'WJets': 400-9,
    # 'ZJets': 432-9,
    # 'DYJets': 432-9,
    # 'DYJetsToLL': 432-9,
    # 'SingleT': 416-9,
    # 'SingleTop': 416-9,
    # 'Diboson' :616-9,
    'TOP' : ROOT.kAzure + 8,
    'EWK' : ROOT.kMagenta - 2,
    'QCD': ROOT.kOrange + 5,
    'TpTp_M-0800' : ROOT.kBlack,
    'TpTp_M-1200' : ROOT.kBlack,
    'TpTp_M-1200_thX' : ROOT.kBlack,
    'TpTp_M-1200_other' : ROOT.kBlack,
})

settings.stacking_order = [
    'QCD',
    'EWK',
    'TOP',
]


settings.stack_line_color = None
settings.signal_linewidth = 3

settings.bottom_pad_height = 0.25

# def apply_split_pad_styles(cnv_wrp):
#     main, scnd = cnv_wrp.main_pad, cnv_wrp.second_pad

#     main.SetTopMargin(0.1)
#     main.SetBottomMargin(0.35)
#     #main.SetRightMargin(0.04)
#     #main.SetLeftMargin(0.16)

#     scnd.SetTopMargin(0.)
#     scnd.SetBottomMargin(0.375)
#     #scnd.SetRightMargin(0.04)
#     #scnd.SetLeftMargin(0.16)
#     scnd.SetRightMargin(main.GetRightMargin())
#     scnd.SetLeftMargin(main.GetLeftMargin())
#     scnd.SetGridy()

#     first_obj = cnv_wrp.first_obj
#     first_obj.GetYaxis().CenterTitle(1)
#     first_obj.GetYaxis().SetTitleSize(0.045)
#     first_obj.GetYaxis().SetTitleOffset(1.3)
#     first_obj.GetYaxis().SetLabelSize(0.055)
#     first_obj.GetXaxis().SetNdivisions(505)

# settings.apply_split_pad_styles = apply_split_pad_styles


line_styles = {
    'TpTp_M-0800' : 1,
    'TpTp_M-1200' : 2,
    'TpTp_M-1200_thX' : 1,
    'TpTp_M-1200_other' : 2,
}

# signals = {'TpTp_M-0800' : ROOT.kViolet,
#     'TpTp_M-1200' : ROOT.kBlue,
#     'TpTp_M-1600' : ROOT.kRed
#     }
# final_states = final_states = ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw', '_incl']

# for s, c in signals.iteritems():
#     settings.colors.update(dict((s + f, c) for f in final_states))
#     settings.colors.update({s+'_thX' : ROOT.kAzure, s+'_other' : ROOT.kMagenta})

bkgs_to_plot = [
    'SingleTop',
    'QCD',
    'DYJets',
    'WJets',
    'Run2015CD',
    'Diboson',
    'TTbar_split'
]

bpbp_samples = ['BpBp_M-0800', 'BpBp_M-1200']

bpbp_finalstates = [
    '_bhbh',
    '_bhbz',
    '_bhtw',
    '_noH_bzbz',
    '_noH_bztw',
    '_noH_twtw',
    ]

less_signals = ['TpTp_M-0800', 'TpTp_M-1200']

samples_to_plot = bkgs_to_plot + list(g + '_thth' for g in less_signals)

samples_to_plot_all = bkgs_to_plot + reduce(lambda x, y: x+y, (list(g + f for f in plot.final_states_to_plot) for g in less_signals))

samples_for_tables = bkgs_to_plot + reduce(lambda x, y: x+y, (list(g + f for f in plot.final_states_to_plot) for g in plot.almost_all_signals))

samples_for_tables += reduce(lambda x, y: x+y, (list(g + f for f in bpbp_finalstates) for g in bpbp_samples))

# base_path = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/UHH2/'\
#     'VLQToHiggsPairProd/NewSamples-76X-v1/FinalSelection-v25'
base_path = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/UHH2/'\
    'VLQToHiggsPairProd/NewSamples-76X-v1/FinalSelection-v26'

mod_dict = {

    ##### GENERAL VARIABLES ######
    'ST' : {
            'rebin_list' : [0., 800., 900., 1000., 1200., 1500., 2000., 2500., 3000., 4500., 6500.],
            'title' : 'S_{T} [GeV]',
            'y_max_log_fct' : 10000.,
            'y_min_gr_zero' : 1e-3,
            'y_max_fct' : 1.2,
            'bin_width' : 100,
            'err_empty_bins' : True
            },
    'ST_rebin_flex' : {
            'title' : 'S_{T} [GeV]',
            'y_max_log_fct' : 100000.,
            'y_min_gr_zero' : 2e-3,
            'bin_width' : 100,
            'set_leg_2_col_log' : {
                    'x_pos': 0.7,
                    'y_pos': 0.7,
                    'label_width': 0.30,
                    'label_height': 0.045,
                    'box_text_size' : 0.035,
                    'opt': 'f',
                    'opt_data': 'pl',
                    'reverse': True,
                    'sort_legend' : lambda w: 'TT ' in w[1],
                },
            'y_max_fct' : 1.2,
            'text_box_lin' : [(0.19, 0.8, "#scale[0.7]{#bf{CMS}}"), (0.19, 0.745, "#scale[0.6]{#it{Preliminary}}")],
            'text_box_log' : (0.16, 0.89, "#scale[0.7]{#bf{CMS}} #scale[0.6]{#it{Preliminary}}"),
            'err_empty_bins' : True,
            'draw_x_errs' : True,
            # 'draw_empty_bin_error' : True
            },

    'nomass_boost_2b_mass_softdrop' : {
            # 'rebin_list' : list(x for x in xrange(0, 80, 20)) + list(x for x in xrange(80, 310, 10)), # [0., 800., 900., 1000., 1200., 1500., 2000., 2500., 3000., 4500., 6500.],
            'rebin' : 15,
            'y_max_fct' : 1.6,
            'title' : 'M_{jet} [GeV]',
            'bin_width' : 20,
            'y_min_gr_zero' : 0.02,
            'y_max_log_fct' : 1000.,
            'scale' : 0.4,
            'set_leg_1_col_lin' : {
                    'x_pos': 0.75,
                    'y_pos': 0.67,
                    'label_width': 0.20,
                    'label_height': 0.040,
                    'box_text_size' : 0.033,
                    'opt': 'f',
                    'opt_data': 'pl',
                    'reverse': True,
                    'sort_legend' : lambda w: 'TT ' in w[1],
                },
            'text_box_lin' : [(0.19, 0.8, "#scale[0.7]{#bf{CMS}}"), (0.19, 0.745, "#scale[0.6]{#it{Preliminary}}")],
            },
    'nomass_boost_2b_mass_softdrop_rebin_flex' : {
            # 'rebin_list' : list(x for x in xrange(0, 310, 10)) # [0., 800., 900., 1000., 1200., 1500., 2000., 2500., 3000., 4500., 6500.],
            # 'rebin' : 30,
            'y_max_fct' : 1.3,
            'title' : 'M_{jet} [GeV]',
            'bin_width' : 5,
            'y_min_gr_zero' : 0.02,
            'y_max_log_fct' : 1000.,
            'scale' : 0.4,
            'set_leg_1_col_lin' : {
                    'x_pos': 0.75,
                    'y_pos': 0.67,
                    'label_width': 0.20,
                    'label_height': 0.040,
                    'box_text_size' : 0.033,
                    'opt': 'f',
                    'opt_data': 'pl',
                    'reverse': True,
                    'sort_legend' : lambda w: 'TT ' in w[1],
                },
            'text_box_lin' : (0.19, 0.79, "#scale[0.7]{#bf{CMS}}"),
            },
    'nobtag_boost_mass_nsjbtags' : {
            'title' : 'N(subjet b-tags)',
            'y_min_gr_zero' : 100,
            'y_max_log_fct' : 50.,
            'set_leg_1_col_log' : {
                    'x_pos': 0.74,
                    'y_pos': 0.67,
                    'label_width': 0.30,
                    'label_height': 0.040,
                    'box_text_size' : 0.033,
                    'opt': 'f',
                    'opt_data': 'pl',
                    'reverse': True,
                    'sort_legend' : lambda w: 'TT ' in w[1],
                },
            'text_box_log' : [(0.19, 0.8, "#scale[0.7]{#bf{CMS}}"), (0.19, 0.745, "#scale[0.6]{#it{Preliminary}}")],
            },
    }

def get_style():
    # _style = style or varial.settings.style
    return [
        common_plot.mod_pre_bot_hist(),
        # common_plot.mk_split_err_ratio_plot_func_mod(poisson_errs=True),  # mk_pull_plot_func()
        # common_plot.mk_pull_plot_func(),  # mk_pull_plot_func()
        common_plot.mk_pull_plot_func_poisson(),  # mk_pull_plot_func()
        # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
        rnd.mk_legend_func(),
        common_plot.mod_post_canv(mod_dict),
        common_plot.mk_tobject_draw_func(TLatex(0.53, 0.89, "#scale[0.45]{2.5 (e), 2.6 (#mu) fb^{-1} (13 TeV)}"))
    ]

# def get_style_poisson():
#     # _style = style or varial.settings.style
#     return [
#         common_plot.mod_pre_bot_hist(),
#         # common_plot.mk_split_err_ratio_plot_func_mod(poisson_errs=True),  # mk_pull_plot_func()
#         common_plot.mk_pull_plot_func_poisson(),  # mk_pull_plot_func()
#         # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
#         rnd.mk_legend_func(),
#         common_plot.mod_post_canv(mod_dict),
#         common_plot.mk_tobject_draw_func(TLatex(0.51, 0.91, "#scale[0.5]{2.6 (e), 2.7 (#mu) fb^{-1} (13 TeV)}"))
#     ]



#           final state BRs:
#           nominal:            sample:
# bwbw:     0.25                0.111
# tZbw:     0.25                0.222
# tZtZ:     0.0625              0.111
# tHbW:     0.25                0.222
# tHtZ:     0.125               0.222
# tHtH:     0.0625              0.111

plot.normfactors_ind_fs = {
    '_thth' : 0.0625/0.111,
    '_tztz' : 0.0625/0.111,
    '_bwbw' : 0.25/0.111,
    '_thtz' : 0.125/0.222,
    '_thbw' : 0.25/0.222,
    '_tzbw' : 0.25/0.222,
    '_bhbh' : 0.0625/0.111,
    '_bzbz' : 0.0625/0.111,
    '_twtw' : 0.25/0.111,
    '_bhbz' : 0.125/0.222,
    '_bhtw' : 0.25/0.222,
    '_bztw' : 0.25/0.222,
}

normfactors_ind_fs_rev = {
    '_thth' : 1./0.0625,
    '_tztz' : 1./0.0625,
    '_bwbw' : 1./0.25,
    '_thtz' : 1./0.125,
    '_thbw' : 1./0.25,
    '_tzbw' : 1./0.25,
    '_bhbh' : 1./0.0625,
    '_bzbz' : 1./0.0625,
    '_twtw' : 1./0.25,
    '_bhbz' : 1./0.125,
    '_bhtw' : 1./0.25,
    '_bztw' : 1./0.25,
}

# plot.normfactors_ind_fs = None

plot.normfactors_ind_fs_rev = None

# source_dir = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/'\
#     'UHH2/VLQToHiggsPairProd/NewSamples-76X-v1/FinalSelection-v24/'\
#     'Run8_withHighMassTTbarSample/RunAnalysis/HTReweighting/TreeProject'
source_dir = base_path+'/FullTreeProject/HTReweighting/TreeProject/'

uncerts = list(analysis.all_uncerts)# or get_sys_dir()
uncerts.remove('sfmu_trg')
uncerts.remove('sflep_trg')
# nom_pattern = [source_dir+'/TreeProjector/{0}.root',
#                source_dir+'/TreeProjectorDiboson/{0}.root']
nom_pattern = [source_dir+'/TreeProjectorBkg/{0}.root',
               source_dir+'/TreeProjectorTT/{0}.root']
# sys_pattern = list(source_dir+'/SysTreeProjectors/%s*/{0}.root'% i for i in uncerts) +\
#               list(source_dir+'/SysTreeProjectorsDiboson/%s*/{0}.root'% i for i in uncerts)
sys_pattern = list(source_dir+'/SysTreeProjectorsBkg/%s*/{0}.root'% i for i in uncerts) +\
              list(source_dir+'/SysTreeProjectorsTT*/%s*/{0}.root'% i for i in uncerts)

bpbp_pattern = [source_dir+'/TreeProjectorBB/{0}.root'] + list(source_dir+'/SysTreeProjectorsBB*/%s*/{0}.root'% i for i in uncerts)

input_pattern = nom_pattern+sys_pattern

theta_lim_path = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/'\
    'UHH2/VLQToHiggsPairProd/NewSamples-76X-v1/FinalSelection-v24/'\
    'Run8_withHighMassTTbarSample/RunAnalysis/HTReweighting/Limit/'\
    'BackgroundOnlyFitNoTheory/CR/ThetaLimit/'


def rename_samples(wrps):
    for w in wrps:
        if w.sample in ['TTbar', 'TTbar_split', 'SingleTop']:
            w.sample = 'TOP__'+w.sample
            w.legend = 'TOP'
        if w.sample in ['WJets', 'DYJets', 'Diboson']:
            w.sample = 'EWK__'+w.sample
            w.legend = 'EWK'
        # if w.sample == 'QCD':
        #     w.sample = 'qcd'
        yield w

def set_line_style(wrps):
    for w in wrps:
        if w.sample in line_styles.keys():
            w.histo.SetLineStyle(line_styles[w.sample])
        yield w

def set_line_width(wrps):
    for w in wrps:
        if w.is_signal:
            w.histo.SetLineWidth(3)
        yield w

def scale_new_lumi(wrps):
    for w in wrps:
        if not w.is_data:
            w.histo.Scale(0.973)
        yield w

# def stack_setup(grps, rate_uncertainties=analysis.rate_uncertainties, shape_uncertainties=analysis.shape_uncertainties, include_rate=False):
#     grps = common_plot.make_uncertainty_histograms(grps, rate_uncertainties, shape_uncertainties, include_rate)
#     grps = gen.mc_stack_n_data_sum(grps, calc_sys_integral=True)
#     # if varial.settings.flex_sig_norm:
#     #     grps = common_plot.norm_to_bkg(grps)
#     # grps = common_plot.make_empty_bin_error(grps)
#     return grps


    # kws['plot_grouper'] = lambda g: group_by_uncerts(g, lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))

def group_by_uncerts_comp_ht_scalevar(wrps, first_sort_func):
    def sort_key_func(wrp):
        if wrp.sys_info.startswith('ScaleVar') or wrp.sys_info.startswith('jsf') or wrp.sys_info.startswith('rate'):
            return 'comp_th'
        elif wrp.sys_info:
            return wrp.sys_info.split('__')[0]
        else:
            return ''

    wrps = itertools.groupby(wrps, first_sort_func)
    for k1, g in wrps:
        g = sorted(g, key=sort_key_func)
        # g = list(g)
        nominal = g[0]
        sys_uncerts = itertools.groupby(g[1:], sort_key_func)
        for k2, sys in sys_uncerts:
            # print nominal.in_file_path, nominal.sample, nominal.sys_info, list((s.in_file_path, s.sample, s.sys_info) for s in sys)
            nom_copy = copy.copy(nominal)
            nom_copy.name = nom_copy.name+'__'+nom_copy.sample+'__'+k2
            yield wrappers.WrapperWrapper([nom_copy]+list(sys), name=k1+'__'+k2)


# def loader_hook_merge_regions(wrps):
#     def get_base_selection(wrp):
#         res = wrp.in_file_path.split('/')[0]
#         if len(res.split('_')) > 1:
#             res = res.split('_')[0]
#         return res 

#     def get_sys_info(wrp):
#         if '_id__' in wrp.sys_info or '_trg__' in wrp.sys_info:
#             return 'sflep'+wrp.sys_info[4:]
#         else:
#             return wrp.sys_info

#     def get_new_infile_path(wrp):
#         comps = wrp.in_file_path.split('/')
#         return get_base_selection(wrp)+'/'+'/'.join(comps[1:])
                  
#     key = lambda w: '{0}___{1}___{2}___{3}'.format(get_base_selection(w), w.sample, get_sys_info(w), w.variable)

#     wrps = plot.common_loader_hook(wrps)
#     wrps = gen.gen_make_th2_projections(wrps)
#     # wrps = gen.sort(wrps, ['sys_info', 'in_file_path', 'sample'])
#     # wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_incl', print_warning=False, yield_orig=True)
#     wrps = list(wrps)
#     # wrps = common_plot.norm_smpl(wrps, normfactors_ind_fs, calc_scl_fct=False)
#     # wrps = common_plot.mod_legend_eff_counts(wrps)
#     wrps = sorted(wrps, key=key)
#     wrps = varial.gen.group(wrps, key)
#     wrps = varial.gen.gen_merge(wrps)
#     wrps = varial.gen.gen_add_wrp_info(wrps, in_file_path=get_new_infile_path, region=get_base_selection, sys_info=get_sys_info)
#     wrps = list(wrps)
#     for w in wrps:
#         if w.sys_info.startswith('sfel') or w.sys_info.startswith('sfmu'):
#             print get_base_selection(w), w.sample, w.sys_info, w.variable
#     return wrps

def loader_hook_compare_finalstates(wrps):
    wrps = common_plot.rebin_st_and_nak4(wrps, mod_dict)
    wrps = plot.common_loader_hook(wrps)
    # wrps = common_plot.norm_smpl(wrps, normfactors_ind_fs_rev, calc_scl_fct=False)
    wrps = sorted(wrps, key=lambda w: '{0}___{1}___{2}'.format(w.sys_info, w.in_file_path, w.sample))
    wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw'], suffix='_thX', print_warning=False)
    wrps = sorted(wrps, key=lambda w: '{0}___{1}___{2}'.format(w.sys_info, w.in_file_path, w.sample))
    wrps = vlq_common.merge_decay_channels(wrps, ['_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_other', print_warning=False)
    wrps = set_line_style(wrps)
    # wrps = set_line_width(wrps)
    # wrps = gen.apply_linecolor(wrps)
    wrps = common_plot.mod_legend_eff_counts(wrps)
    wrps = scale_new_lumi(wrps)
    wrps = common_plot.norm_smpl(wrps, common_plot.pas_normfactors, mk_legend=False)
    # wrps = rename_samples(wrps)
    # wrps = sorted(wrps, key=lambda w: w.in_file_path+'___'+w.sys_info+'___'+w.sample)
    # wrps = vlq_common.merge_decay_channels(wrps, postfixes=['__TTbar', '__TTbar_split', '__SingleTop'], print_warning=False)
    # wrps = vlq_common.merge_decay_channels(wrps, postfixes=['__WJets', '__DYJets', '__Diboson'], print_warning=False)
    wrps = gen.sort(wrps, ['in_file_path'])
    # wrps = list(wrps)
    # for w in wrps: print w.in_file_path, w.sample, w.legend, w.sys_info
    return wrps

def merge_bkgs(grps):
    for wrps in grps:
        name = wrps.name
        wrps = rename_samples(wrps)
        wrps = sorted(wrps, key=lambda w: w.in_file_path+'___'+w.sys_info+'___'+w.sample)
        wrps = vlq_common.merge_decay_channels(wrps, postfixes=['__TTbar', '__TTbar_split', '__SingleTop'], print_warning=False)
        wrps = vlq_common.merge_decay_channels(wrps, postfixes=['__WJets', '__DYJets', '__Diboson'], print_warning=False)
        yield varial.wrappers.WrapperWrapper(list(wrps), name=name)

def stack_setup(grps, rate_uncertainties=analysis.rate_uncertainties, shape_uncertainties=analysis.shape_uncertainties, include_rate=False, stack_order=settings.stacking_order):
    grps = common_plot.make_uncertainty_histograms(grps, rate_uncertainties, shape_uncertainties, include_rate)
    grps = merge_bkgs(grps)
    grps = gen.mc_stack_n_data_sum(grps, merge_mc_key_func=lambda w: varial.analysis.get_stack_position(w, stack_order), calc_sys_integral=True, add_sys_errs=True)
    # grps = common_plot.make_empty_bin_error(grps)
    return grps

def plot_merged_channels_higgs(final_dir):
    # plot_hists = ['ST', 'HT', 'n_ak4', 'topjets[0].m_pt', 'topjets[1].m_pt',
    #                 'n_ak8', 'met', 'pt_ld_ak4_jet', 'pt_subld_ak4_jet', 'jets[2].m_pt','jets[3].m_pt', 'jets[].m_pt', 'n_additional_btags_medium', 'n_prim_vertices',
    #                 'n_higgs_tags_1b_med_sm10', 'n_higgs_tags_2b_med_sm10', 'primary_electron_pt', 'primary_muon_pt', 'PrimaryLepton.Particle.m_eta', 'wtags_mass_softdrop',
    #                 'nobtag_boost_mass_nsjbtags', 'nomass_boost_1b_mass_softdrop', 'nomass_boost_2b_mass_softdrop', 'noboost_mass_1b[0].m_pt', 'noboost_mass_2b[0].m_pt']
    plot_hists = ['ST', 'HT', 'n_ak4', 'nomass_boost_1b_mass_softdrop', 'nomass_boost_2b_mass_softdrop', 'noboost_mass_1b[0].m_pt', 'noboost_mass_2b[0].m_pt', 'nobtag_boost_mass_nsjbtags']

    stacking_order = [
        'TOP',
        'EWK',
        'QCD',
    ]

    return varial.tools.ToolChain(final_dir, [
        varial.tools.ToolChainParallel('HistoLoader',
        list(varial.tools.HistoLoader(
            pattern=map(lambda w: w.format('*'+g+'*'), input_pattern),
            filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in samples_to_plot_all) and\
                'Region_Comb' not in w.in_file_path and\
                any(w.in_file_path.endswith(f) for f in plot_hists), # and\
                # common_plot.unselect_theory_uncert(w),
            hook_loaded_histos=plot.loader_hook_merge_regions,
            name='HistoLoader_'+g,
            lookup_aliases=False,
            raise_on_empty_result=False,
            quiet_mode=True
            ) for g in samples_to_plot_all)),
        # mk_toolchain('HistogramsNormToInt',
        #     filter_keyfunc=lambda w: 'TpTp' not in w.file_path,
        #     pattern=None, input_result_path='../HistoLoader/HistoLoader*',
        #     plotter_factory=plotter_factory_stack(analysis.rate_uncertainties, def_uncerts, hook_loaded_histos=loader_hook_norm_to_int,
        #         plot_setup=stack_setup_norm_all_to_intgr)),
        plot.mk_toolchain('HistogramsHiggsComp', pattern=None, input_result_path='../HistoLoader/HistoLoader*',
            filter_keyfunc=lambda w: all(g not in w.sample for g in ['TpTp_M-0800', 'TpTp_M-1600']) and common_plot.unselect_theory_uncert(w),
            plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=True, 
                hook_loaded_histos=loader_hook_compare_finalstates,
                stack_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=True, stack_order=stacking_order),
                plot_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=True, stack_order=stacking_order),
                mod_log=common_plot.mod_log_usr(mod_dict),
                canvas_post_build_funcs=get_style()
                ),
            parallel=True
            # pattern=None, input_result_path='../HistoLoader/HistoLoader*'
            ),
        # plot.mk_toolchain('HistogramsCompUncerts', samples_to_plot_all,
        #     filter_keyfunc=lambda w: any(f in w.file_path for f in [analysis.ttbar_smpl, 'QCD', 'WJets', 'TpTp_M-0800', 'TpTp_M-1600']) and any(w.in_file_path.endswith(g) for g in ['ST']),   
        #     plotter_factory=plot.plotter_factory_uncerts(
        #         hook_loaded_histos=lambda w: plot.loader_hook_uncerts(loader_hook_compare_finalstates(w), 
        #             analysis.rate_uncertainties, uncerts, include_rate=False)),
        #     pattern=None, input_result_path='../HistoLoader/HistoLoader*'),
        # plot.mk_toolchain('HistogramsCompScaleVarHTRew', samples_to_plot_all,
        #     filter_keyfunc=lambda w: any(f in w.file_path for f in [analysis.ttbar_smpl, 'QCD', 'WJets', 'TpTp_M-0800', 'TpTp_M-1600']) and any(w.in_file_path.endswith(g) for g in ['ST']),   
        #     plotter_factory=plot.plotter_factory_uncerts(
        #         hook_loaded_histos=lambda w: plot.loader_hook_uncerts(loader_hook_compare_finalstates(w), 
        #             analysis.rate_uncertainties, uncerts, include_rate=False),
        #         plot_grouper=lambda g: group_by_uncerts_comp_ht_scalevar(g, lambda w: '{0}___{1}'.format(w.in_file_path, w.sample)),
        #         ),
        #     pattern=None, input_result_path='../HistoLoader/HistoLoader*'),
        # mk_toolchain('HistogramsNoDataHiggsComp', pattern=None, input_result_path='../HistoLoader/HistoLoader*',
        #     filter_keyfunc=lambda w: 'Run2015CD' not in w.file_path.split('/')[-1] and all(g not in w.sample for g in ['TpTp_M-0800', 'TpTp_M-1600']),
        #     plotter_factory=plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=True, 
        #         hook_loaded_histos=loader_hook_compare_finalstates,
        #         )
        #     ),
        varial.tools.WebCreator()
        ])

def remove_final_states(wrps):
    for w in wrps:
        if not any(w.sample.endswith(a) for a in ['_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw']):
            # print w.sample
            yield w



def loader_hook_nominal_brs(wrps):
    wrps = plot.common_loader_hook(wrps)
    wrps = common_plot.mod_title(wrps)
    wrps = common_plot.rebin_st_and_nak4(wrps, mod_dict)
    wrps = sorted(wrps, key=lambda w: '{0}___{1}___{2}'.format(w.sys_info, w.in_file_path, w.sample))
    wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw'], print_warning=True, yield_orig=False)
    wrps = sorted(wrps, key=lambda w: '{0}___{1}___{2}'.format(w.sys_info, w.in_file_path, w.sample))
    wrps = vlq_common.merge_decay_channels(wrps, ['_bhbh', '_bhbz', '_bhtw', '_noH_bzbz', '_noH_bztw', '_noH_twtw'], print_warning=True, yield_orig=False)
    wrps = set_line_style(wrps)
    wrps = scale_new_lumi(wrps)
    # wrps = rename_samples(wrps)
    # wrps = sorted(wrps, key=lambda w: w.in_file_path+'___'+w.sys_info+'___'+w.sample)
    # wrps = vlq_common.merge_decay_channels(wrps, postfixes=['__TTbar', '__TTbar_split', '__SingleTop'], print_warning=False)
    # wrps = vlq_common.merge_decay_channels(wrps, postfixes=['__WJets', '__DYJets', '__Diboson'], print_warning=False)
    # wrps = remove_final_states(wrps)
    # wrps = common_plot.norm_smpl(wrps, {'_thth' : 1./0.0625}, calc_scl_fct=False)
    # wrps = common_plot.mod_legend_no_thth(wrps)
    wrps = sorted(wrps, key=lambda w: w.region+'__'+w.name)
    return wrps

def loader_hook_postfit_nominal_brs(wrps, theta_res_path, signal, rate_uncertainties):
    wrps = loader_hook_nominal_brs(wrps)
    wrps = sensitivity.scale_bkg_postfit(wrps, theta_res_path, signal, rate_uncertainties)
    return wrps


def stack_setup_postfit(grps, theta_res_path, signal, rate_uncertainties, shape_uncertainties, include_rate):
    grps = sensitivity.plot_setup_postfit(grps, theta_res_path, signal, rate_uncertainties, shape_uncertainties, include_rate)
    grps = merge_bkgs(grps)
    grps = gen.mc_stack_n_data_sum(grps, calc_sys_integral=True, add_sys_errs=True)
    # grps = common_plot.make_empty_bin_error(grps)
    return grps

def plot_merged_channels_postfit(final_dir):

    # settings.stacking_order = [
    #     'QCD',
    #     'EWK',
    #     'TOP',
    # ]

    return varial.tools.ToolChain(final_dir, [
        varial.tools.ToolChainParallel('HistoLoaderPost',
            list(varial.tools.HistoLoader(
                pattern=map(lambda w: w.format('*'+g+'*'), input_pattern),
                filter_keyfunc=lambda w: common_plot.unselect_theory_uncert(w) and\
                    any(f in w.file_path.split('/')[-1] for f in samples_to_plot_all) and\
                    'Region_Comb' not in w.in_file_path and\
                    any(w.in_file_path.endswith(f) for f in ['ST']),
                hook_loaded_histos=plot.loader_hook_merge_regions,
                name='HistoLoader_'+g,
                lookup_aliases=False,
                raise_on_empty_result=False,
                quiet_mode=True
                ) for g in samples_to_plot_all)),
        plot.mk_toolchain('HistogramsPostfit',
            plotter_factory=sensitivity.plotter_factory_postfit(theta_lim_path, '', analysis.rate_uncertainties, uncerts, True,
                hook_loaded_histos=lambda w: loader_hook_postfit_nominal_brs(w, theta_lim_path, '', analysis.rate_uncertainties),
                stack_setup=lambda w: stack_setup_postfit(w, theta_lim_path, '', analysis.rate_uncertainties, uncerts, True),
                plot_setup=lambda w: stack_setup_postfit(w, theta_lim_path, '', analysis.rate_uncertainties, uncerts, True),
                mod_log=common_plot.mod_log_usr(mod_dict),
                canvas_post_build_funcs=get_style()),
            pattern=None,
            input_result_path='../HistoLoaderPost/HistoLoader*',
            # auto_legend=False,
            # name='HistogramsPostfit',
            # lookup_aliases=varial.settings.lookup_aliases
            ),
        varial.tools.WebCreator()
        ])

def plot_merged_channels_prefit(final_dir):

    # settings.stacking_order = [
    #     'QCD',
    #     'EWK',
    #     'TOP',
    # ]

    return varial.tools.ToolChain(final_dir, [
        varial.tools.ToolChainParallel('HistoLoaderPre',
            list(varial.tools.HistoLoader(
                pattern=map(lambda w: w.format('*'+g+'*'), input_pattern),
                filter_keyfunc=lambda w: common_plot.unselect_theory_uncert(w) and\
                    any(f in w.file_path.split('/')[-1] for f in samples_to_plot_all) and\
                    'Region_Comb' not in w.in_file_path and\
                    any(w.in_file_path.endswith(f) for f in ['ST']),
                hook_loaded_histos=plot.loader_hook_merge_regions,
                name='HistoLoader_'+g,
                lookup_aliases=False,
                raise_on_empty_result=False,
                quiet_mode=True
                ) for g in samples_to_plot_all)),
        plot.mk_toolchain('HistogramsPrefit', samples_to_plot_all,
            plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=False, 
                hook_loaded_histos=loader_hook_nominal_brs,
                stack_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=False),
                plot_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=False),
                mod_log=common_plot.mod_log_usr(mod_dict),
                canvas_post_build_funcs=get_style()
                ),
            pattern=None,
            input_result_path='../HistoLoaderPre/HistoLoader*',
            # auto_legend=False,
            # name='HistogramsPostfit',
            # lookup_aliases=varial.settings.lookup_aliases
            ),
        varial.tools.WebCreator()
        ])

table_block_signal_small = [
    (r'$\mathrm{T\bar{T}}$ (0.8 TeV)', lambda w: 'Integral___TpTp_M-0800' in w, True),
    (r'$\mathrm{T\bar{T}}$ (1.2 TeV)', lambda w: 'Integral___TpTp_M-1200' in w, True),
    # (r'$\mathrm{T\bar{T}}$ (1.6 TeV)', lambda w: 'Integral___TpTp_M-1600' in w, True),
]

table_block_signal_small_bb = [
    (r'$\mathrm{B\bar{B}}$ (0.8 TeV)', lambda w: 'Integral___BpBp_M-0800' in w, True),
    (r'$\mathrm{B\bar{B}}$ (1.2 TeV)', lambda w: 'Integral___BpBp_M-1200' in w, True),
    # (r'$\mathrm{T\bar{T}}$ (1.6 TeV)', lambda w: 'Integral___TpTp_M-1600' in w, True),
]

table_block_background = [
    ('TOP', lambda w: 'Integral___TOP' in w, False, True),
    ('EWK', lambda w: 'Integral___EWK' in w, False, True),
    ('QCD', lambda w: 'Integral___QCD' in w, False, True),
]

def plot_merged_channels_tables(final_dir):
    return varial.tools.ToolChain(final_dir, [
        varial.tools.ToolChainParallel('HistoLoaderPost',
            list(varial.tools.HistoLoader(
                pattern=map(lambda w: w.format('*'+g+'*'), input_pattern + bpbp_pattern),
                filter_keyfunc=lambda w: common_plot.unselect_theory_uncert(w) and\
                    any(f in w.file_path.split('/')[-1] for f in samples_for_tables) and\
                    'Region_Comb' not in w.in_file_path and\
                    any(w.in_file_path.endswith(f) for f in ['ST']),
                hook_loaded_histos=plot.loader_hook_merge_regions,
                name='HistoLoader_'+g,
                lookup_aliases=False,
                raise_on_empty_result=False,
                quiet_mode=True
                ) for g in samples_for_tables)),
        plot.mk_toolchain('HistogramsTablesPostfit', samples_for_tables,
            plotter_factory=sensitivity.plotter_factory_postfit(theta_lim_path, '', analysis.rate_uncertainties, uncerts, True,
                hook_loaded_histos=lambda w: loader_hook_postfit_nominal_brs(w, theta_lim_path, '', analysis.rate_uncertainties),
                stack_setup=lambda w: stack_setup_postfit(w, theta_lim_path, '', analysis.rate_uncertainties, uncerts, True),
                plot_setup=lambda w: stack_setup_postfit(w, theta_lim_path, '', analysis.rate_uncertainties, uncerts, True),
                mod_log=common_plot.mod_log_usr(mod_dict),
                canvas_post_build_funcs=get_style()),
            pattern=None,
            input_result_path='../HistoLoaderPost/HistoLoader*',
            # auto_legend=False,
            # name='HistogramsPostfit',
            # lookup_aliases=varial.settings.lookup_aliases
            ),
        plot.mk_toolchain('HistogramsTablesPrefit', samples_for_tables,
            plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=False, 
                hook_loaded_histos=loader_hook_nominal_brs,
                stack_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=False),
                plot_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=False),
                mod_log=common_plot.mod_log_usr(mod_dict),
                canvas_post_build_funcs=get_style()
                ),
            pattern=None,
            input_result_path='../HistoLoaderPost/HistoLoader*',
            # auto_legend=False,
            # name='HistogramsPostfit',
            # lookup_aliases=varial.settings.lookup_aliases
            ),
        plot.mk_toolchain('HistogramsTablesEffs', samples_for_tables,
            plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=False,
                hook_loaded_histos=lambda w: common_plot.norm_smpl(w, normfactors_ind_fs_rev, calc_scl_fct=False)),
            pattern=None,
            input_result_path='../HistoLoaderPost/HistoLoader*',
            # auto_legend=False,
            # name='HistogramsPostfit',
            # lookup_aliases=varial.settings.lookup_aliases
            ),
        CountTable([
                table_block_signal_small,
                table_block_background,
                [(r'\textbf{Total Background}', lambda w: 'Integral___bkg_sum' in w)],
                [(r'\textbf{Data}', lambda w: 'Integral___Run2015CD' in w)],
            ],
            common_plot.get_table_category_block('HistogramsTablesPostfit', style='paper'),
            squash_errs=True,
            name='CountTablePostFit'
            ),
        CountTable([
                table_block_signal_small,
                table_block_background,
                table_block_signal_small_bb,
                [(r'\textbf{Total Background}', lambda w: 'Integral___bkg_sum' in w)],
                [(r'\textbf{Data}', lambda w: 'Integral___Run2015CD' in w)],
            ],
            common_plot.get_table_category_block('HistogramsTablesPrefit', style='paper'),
            squash_errs=True,
            name='CountTablePreFit'
            ),
        EffTable([
                common_plot.table_block_signal_fs_800,
                common_plot.table_block_signal_fs_1200,
                common_plot.table_block_signal_bb_fs_800,
                common_plot.table_block_signal_bb_fs_1200,
            ],
            common_plot.get_table_category_block('HistogramsTablesEffs', style='paper'),
            common_plot.norm_factors,
            squash_errs=True,
            name='EffTableCompFS'
            ),
        varial.tools.WebCreator()
        ])

def mk_tc_tex(source_dir):
    tc_tex_an = [
        tex_content.mk_plot_ind(
            (
                ('st_sideband_ttbar', os.path.join(base_path, source_dir)+'/PostFitPlots/HistogramsPostfit/StackedAll/SidebandTTJetsRegion/ST_rebin_flex_log.pdf'),
                ('st_sideband_wjets', os.path.join(base_path, source_dir)+'/PostFitPlots/HistogramsPostfit/StackedAll/SidebandWPlusJetsRegion/ST_rebin_flex_log.pdf'),
                ('st_h1b', os.path.join(base_path, source_dir)+'/PostFitPlots/HistogramsPostfit/StackedAll/SignalRegion1b/ST_rebin_flex_log.pdf'),
                ('st_h2b', os.path.join(base_path, source_dir)+'/PostFitPlots/HistogramsPostfit/StackedAll/SignalRegion2b/ST_rebin_flex_log.pdf'),
                ('st_h2b_lin', os.path.join(base_path, source_dir)+'/PostFitPlots/HistogramsPostfit/StackedAll/SignalRegion2b/ST_rebin_flex_lin.pdf'),
            ), name='PaperPlotsPostfit'),
        tex_content.mk_plot_ind(
            (
                ('higgs_tag_mass', os.path.join(base_path, source_dir)+'/HiggsPlots/HistogramsHiggsComp/StackedAll/BaseLineSelection/nomass_boost_2b_mass_softdrop_lin.pdf'),
                ('higgs_tag_sjbtags', os.path.join(base_path, source_dir)+'/HiggsPlots/HistogramsHiggsComp/StackedAll/BaseLineSelection/nobtag_boost_mass_nsjbtags_log.pdf'),
                ('st_sideband_ttbar', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/ST_rebin_flex_log.pdf'),
                ('st_sideband_wjets', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/ST_rebin_flex_log.pdf'),
                ('st_h1b', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SignalRegion1b/ST_rebin_flex_log.pdf'),
                ('st_h2b', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SignalRegion2b/ST_rebin_flex_log.pdf'),
                ('st_h2b_lin', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SignalRegion2b/ST_rebin_flex_lin.pdf'),
            ), name='PaperPlotsPrefit'),
        tex_content.mk_plot_ind(
            (
                ('st_sideband_ttbar', os.path.join(base_path, source_dir)+'/PostFitPlots/HistogramsPostfit/StackedAll/SidebandTTJetsRegion/ST_rebin_flex_log.png'),
                ('st_sideband_wjets', os.path.join(base_path, source_dir)+'/PostFitPlots/HistogramsPostfit/StackedAll/SidebandWPlusJetsRegion/ST_rebin_flex_log.png'),
                ('st_h1b', os.path.join(base_path, source_dir)+'/PostFitPlots/HistogramsPostfit/StackedAll/SignalRegion1b/ST_rebin_flex_log.png'),
                ('st_h2b', os.path.join(base_path, source_dir)+'/PostFitPlots/HistogramsPostfit/StackedAll/SignalRegion2b/ST_rebin_flex_log.png'),
                ('st_h2b_lin', os.path.join(base_path, source_dir)+'/PostFitPlots/HistogramsPostfit/StackedAll/SignalRegion2b/ST_rebin_flex_lin.png'),
            ), name='PaperPlotsPostfitPNG'),
        tex_content.mk_plot_ind(
            (
                ('higgs_tag_mass', os.path.join(base_path, source_dir)+'/HiggsPlots/HistogramsHiggsComp/StackedAll/BaseLineSelection/nomass_boost_2b_mass_softdrop_lin.png'),
                ('higgs_tag_sjbtags', os.path.join(base_path, source_dir)+'/HiggsPlots/HistogramsHiggsComp/StackedAll/BaseLineSelection/nobtag_boost_mass_nsjbtags_log.png'),
                ('st_sideband_ttbar', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/ST_rebin_flex_log.png'),
                ('st_sideband_wjets', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/ST_rebin_flex_log.png'),
                ('st_h1b', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SignalRegion1b/ST_rebin_flex_log.png'),
                ('st_h2b', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SignalRegion2b/ST_rebin_flex_log.png'),
                ('st_h2b_lin', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SignalRegion2b/ST_rebin_flex_lin.png'),
            ), name='PaperPlotsPrefitPNG'),
        tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/Tables/EffTableCompFS/count_table_content.tex', name='EffTableCompFS'),
        # tex_content.mk_autoTable(path_an+'/MergeChannelsTablesNoTheory/CountTablePAS/count_table_content.tex', name='CountTable'),
        tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/Tables/CountTablePostFit/count_table_content.tex', name='CountTablePostFit'),
        tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/Tables/CountTablePreFit/count_table_content.tex', name='CountTablePreFit'),
        # tex_content.mk_autoContentSysTabs(os.path.join(base_path, source_dir)+'/Ind_Limits/Limit_bW0p5_tZ0p25_tH0p25/ThetaLimits', 'SysTabs', mass_points=['TTM0700', 'TTM1200', 'TTM1700'], regions=regions),
        # tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/MergeChannelsTablesNoTheory/EffTableCompFSPAS/count_table_content.tex', name='EffTableCompFS_'+name),
        # tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/MergeChannelsTablesNoTheory/CountTablePAS/count_table_content.tex', name='CountTable_'+name),
        # tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/BackgroundOnlyFitNoTheory/CR/PostFitPlots/CountTablePostFitPAS/count_table_content.tex', name='CountTablePostFit_'+name),
        
    ]
    tc_tex_an = varial.tools.ToolChain('CopyPlots', [
        varial.tools.ToolChain('TexPaper', tc_tex_an),
        varial.tools.CopyTool('dnowatsc@lxplus.cern.ch:Paper-Dir/notes/B2G-16-024/trunk/', src='../TexPaper/*', ignore=('*.svn', '*.html', '*.log'), use_rsync=True),
        ])
    return tc_tex_an

# sframe_tools = mk_sframe_and_plot_tools()

import sys

if __name__ == '__main__':
    time.sleep(1)
    # src_dir = sys.argv[1]
    final_dir = sys.argv[1]
    all_tools = varial.tools.ToolChainParallel(final_dir,
        [
            plot_merged_channels_higgs('HiggsPlots'),
            plot_merged_channels_postfit('PostFitPlots'),
            plot_merged_channels_prefit('PreFitPlots'),
            plot_merged_channels_tables('Tables'),
            mk_tc_tex(final_dir),
            varial.tools.WebCreator()
            # combination_limits.mk_limit_list('Limits')
        ], n_workers=1)
    varial.tools.Runner(all_tools, default_reuse=True)
    # varial.tools.CopyTool('~/www/vlq_analysis/tight_selection2/',
    #     src=final_dir, use_rsync=True).run()