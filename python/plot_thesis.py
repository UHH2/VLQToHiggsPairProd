#!/usr/bin/env python

import sys
import os
import time
import itertools
import copy
import pprint
import cPickle

import varial.settings as settings
import varial.rendering as rnd
import varial.generators as gen
import varial.wrappers as wrappers
import varial.tools as tools
import varial.extensions.limits as limits
import varial.analysis
import UHH2.VLQSemiLepPreSel.common as vlq_common
from varial.plotter import Plotter

# import common_vlq
import tptp_settings
# import final_plotting
import common_plot_new as common_plot
import plot_new as plot
# import tptp_sframe 
# import compare_crs
import analysis
import sensitivity
import common_sensitivity
import combination_limits
import model_vlqpair
import bkg_only_fit
import treeproject_tptp
import tex_content_new as tex_content
import sel_opt_study
from get_eff_count import CountTable, EffTable # EffNumTable, 

from ROOT import TLatex, TH2
import ROOT

# PUT THE SETTINGS BELOW INTO ONE GENERAL "THESIS-SETTINGS" FILE?

settings.canvas_size_x = 600
settings.canvas_size_y = 500


# settings.stat_error_color = 923
# settings.stat_error_fill = 3002
settings.tot_error_color = (1, 0.4)
settings.tot_error_fill = 3844


# settings.defaults_BottomPlot['y_min'] = -2.9
# settings.defaults_BottomPlot['y_max'] = 2.9

settings.defaults_Legend.update({
    'y_pos': 0.71,
    'x_pos': 0.66,
    })



# settings.colors.update({
#     # 'Background' : 920,
#     # 'nominal' : 1,
#     # 'plus' : 2,
#     # 'minus' : 3,
#     # 'TTbar': 632 - 7,
#     # 'WJets': 400-9,
#     # 'ZJets': 432-9,
#     # 'DYJets': 432-9,
#     # 'DYJetsToLL': 432-9,
#     # 'SingleT': 416-9,
#     # 'SingleTop': 416-9,
#     # 'Diboson' :616-9,
#     'TOP' : ROOT.kAzure + 8,
#     'EWK' : ROOT.kMagenta - 2,
#     'QCD': ROOT.kOrange + 5,
#     'TpTp_M-0800' : ROOT.kBlack,
#     'TpTp_M-1200' : ROOT.kBlack,
#     'TpTp_M-1200_thX' : ROOT.kBlack,
#     'TpTp_M-1200_other' : ROOT.kBlack,
# })

# settings.stacking_order = [
#     'QCD',
#     'EWK',
#     'TOP',
# ]


# settings.stack_line_color = None
# settings.signal_linewidth = 3

# settings.bottom_pad_height = 0.35

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

sig_scalefactors = {
    'TpTp_M-0700' : 10.,
    'TpTp_M-0800' : 10.,
    'TpTp_M-0900' : 10.,
    'TpTp_M-1000' : 10.,
    'TpTp_M-1100' : 100.,
    'TpTp_M-1200' : 100.,
    'TpTp_M-1300' : 100.,
    'TpTp_M-1400' : 100.,
    'TpTp_M-1500' : 1000.,
    'TpTp_M-1600' : 1000.,
    'TpTp_M-1700' : 1000.,
    'TpTp_M-1800' : 1000.,
}

# line_styles = {
#     'TpTp_M-0800' : 1,
#     'TpTp_M-1200' : 2,
#     'TpTp_M-0800_thX' : 1,
#     'TpTp_M-0800_other' : 2,
#     'TpTp_M-1200_thX' : 1,
#     'TpTp_M-1200_other' : 2,
# }

# signals = {'TpTp_M-0800' : ROOT.kViolet,
#     'TpTp_M-1200' : ROOT.kBlue,
#     'TpTp_M-1600' : ROOT.kRed
#     }
# final_states = final_states = ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw', '_incl']

# for s, c in signals.iteritems():
#     settings.colors.update(dict((s + f, c) for f in final_states))
#     settings.colors.update({s+'_thX' : ROOT.kAzure, s+'_other' : ROOT.kMagenta})

bkg_samples = [
    'SingleTop',
    'QCD',
    'DYJets',
    'WJets',
    'Diboson',
    'TTbar'
]


non_sig_samples = bkg_samples + ['Run2015CD']

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

final_states_all = [
    '_thth',
    '_thtz',
    '_thbw',
    '_noH_tztz',
    '_noH_tzbw',
    '_noH_bwbw',
]

final_states_to_plot = [
    '_thth',
    # '_thtz',
    # '_thbw',
    # '_noH_tztz',
    # '_noH_tzbw',
    # '_noH_bwbw',
]

samples_to_plot = non_sig_samples + list(g + '_thth' for g in less_signals)

samples_all = non_sig_samples + reduce(lambda x, y: x+y, (list(g + f for f in final_states_all) for g in less_signals))

samples_to_plot_all = non_sig_samples + reduce(lambda x, y: x+y, (list(g + f for f in final_states_to_plot) for g in less_signals))

samples_for_tables = non_sig_samples + reduce(lambda x, y: x+y, (list(g + f for f in final_states_to_plot) for g in plot.almost_all_signals))

samples_for_tables += reduce(lambda x, y: x+y, (list(g + f for f in bpbp_finalstates) for g in bpbp_samples))

# base_path = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/UHH2/'\
#     'VLQToHiggsPairProd/NewSamples-76X-v1/FinalSelection-v25'
base_path = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/UHH2/'\
    'VLQToHiggsPairProd/NewSamples-76X-v1/FinalSelection-v26'

def_leg_dict_1col_lin = {
    'x_pos': 0.72,
    'y_pos': 0.65,
    'label_width': 0.20,
    'label_height': 0.040,
    'box_text_size' : 0.033,
    'opt': 'f',
    'opt_data': 'pl',
    'reverse': True,
    'sort_legend' : lambda w: 'TT ' in w[1],
}

mod_dict = {

    ##### GENERAL VARIABLES ######
    'ST' : {
            'rebin_list' : [0., 800., 900., 1000., 1200., 1500., 2000., 2500., 3000., 4500., 6500.],
            'title' : 'S_{T} [GeV]',
            'y_max_log_fct' : 10000.,
            'y_min_gr_zero' : 1e-3,
            'y_max_fct' : 1.2,
            # 'bin_width' : 100,
            'err_empty_bins' : True
            },
    'ST_rebin_flex' : {
            'title' : 'S_{T} [GeV]',
            'y_max_log_fct' : 1000000.,
            'y_min_gr_zero' : 2e-5,
            'bin_width' : 100,
            '_set_leg_2_col_log' : {
                    'x_pos': 0.68,
                    'y_pos': 0.66,
                    'label_width': 0.32,
                    'label_height': 0.045,
                    'box_text_size' : 0.035,
                    'opt': 'f',
                    'opt_data': 'pl',
                    'reverse': True,
                    'sort_legend' : lambda w: 'TT ' in w[1],
                },
            'y_max_fct' : 1.2,
            # 'text_box_lin' : (0.19, 0.82, "#scale[0.8]{#bf{CMS}}"),
            # 'text_box_log' : (0.16, 0.91, "#scale[0.8]{#bf{CMS}}"),
            'err_empty_bins' : True,
            'draw_x_errs' : True,
            # 'draw_empty_bin_error' : True
            },
    'HT' : {
            'rebin_list' : [0., 100., 200., 300., 400., 500., 600., 700., 800., 900., 1000., 1200., 1500., 2000., 2500., 3000., 4500., 6500.],
            # 'rebin_list' : [0., 800., 900., 1000., 1200., 1500., 2000., 2500., 3000., 4500., 6500.],
            'title' : 'H_{T} [GeV]',
            'y_max_log_fct' : 10000.,
            'y_min_gr_zero' : 1e-3,
            'y_max_fct' : 1.2,
            # 'bin_width' : 100,
            'err_empty_bins' : True
            },
    'HT_rebin_flex' : {
            'title' : 'H_{T} [GeV]',
            'y_max_log_fct' : 100000.,
            'y_min_gr_zero' : 2e-3,
            'bin_width' : 100,
            '_set_leg_2_col_log' : {
                    'x_pos': 0.7,
                    'y_pos': 0.66,
                    'label_width': 0.30,
                    'label_height': 0.045,
                    'box_text_size' : 0.035,
                    'opt': 'f',
                    'opt_data': 'pl',
                    'reverse': True,
                    'sort_legend' : lambda w: 'TT ' in w[1],
                },
            'y_max_fct' : 1.2,
            # 'text_box_lin' : (0.19, 0.82, "#scale[0.8]{#bf{CMS}}"),
            # 'text_box_log' : (0.16, 0.91, "#scale[0.8]{#bf{CMS}}"),
            'err_empty_bins' : True,
            'draw_x_errs' : True,
            # 'draw_empty_bin_error' : True
            },
    'primary_lepton_pt' : {
            'rebin' : 25,
            '_set_leg_1_col_lin' : def_leg_dict_1col_lin,
            },
    'primary_lepton_pt_rebin_flex' : {
            # 'rebin_list' : list(i for i in xrange(0, 624, 48)) + [1200],
            'bin_width' : 24,
            'draw_x_errs' : True,
            },
    'pt_ld_ak4_jet' : {
            'rebin' : 25,
            '_set_leg_1_col_lin' : def_leg_dict_1col_lin,
            },
    'pt_subld_ak4_jet' : {
            'rebin' : 20,
            '_set_leg_1_col_lin' : def_leg_dict_1col_lin,
            },
    'jets[2].m_pt' : {
            'rebin' : 25,
            '_set_leg_1_col_lin' : def_leg_dict_1col_lin,
            },
    'jets[3].m_pt' : {
            'rebin' : 25,
            '_set_leg_1_col_lin' : def_leg_dict_1col_lin,
            },
    'topjets[0].m_pt' : {
            'rebin' : 30,
            },
    'met' : {
            'rebin' : 25,
            'title' : '#slash{E}_{T}',
            '_set_leg_1_col_lin' : def_leg_dict_1col_lin,
            },
    'n_ak4' : {
            '_set_leg_1_col_lin' : def_leg_dict_1col_lin,
            },
    'nomass_boost_2b_mass_softdrop' : {
            'rebin' : 30,
            'y_max_fct' : 2.,
            'title' : 'M_{jet}(H-tag, 2 b-tagged subjets) [GeV]',
            # 'bin_width' : 5,
            'y_min_gr_zero' : 0.02,
            'y_max_log_fct' : 1000.,
            'scale' : 0.4,
            # '_set_leg_1_col_lin' : def_leg_dict_1col_lin,
            # 'text_box_lin' : (0.19, 0.82, "#scale[0.8]{#bf{CMS}}"),
            },
    # 'nomass_boost_2b_mass_softdrop_rebin_flex' : {
    #         'y_max_fct' : 1.3,
    #         'title' : 'M_{jet} [GeV]',
    #         'bin_width' : 5,
    #         'y_min_gr_zero' : 0.02,
    #         'y_max_log_fct' : 1000.,
    #         'scale' : 0.4,
    #         '_set_leg_1_col_lin' : {
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
    #         # 'text_box_lin' : (0.19, 0.82, "#scale[0.8]{#bf{CMS}}"),
    #         },
    'nomass_boost_1b_mass_softdrop' : {
            'rebin' : 30,
            # 'title' : 'M_{jet}(p_{T}-leading Higgs cand., 1 subjet b-tag) [GeV]',
            'title' : 'M_{jet}(H-tag, 1 b-tagged subjet) [GeV]',
            'y_min_gr_zero' : 0.4,
            'y_max_log_fct' : 1000.,
            'y_max_fct' : 1.8,
            'scl_fct' : 3,
            # '_set_leg_1_col_lin' : def_leg_dict_1col_lin,
            },
    'nobtag_boost_mass_nsjbtags' : {
            'rebin_list' : [-0.5, 0.5, 1.5, 2.5],
            'title' : 'N(b-tagged subjets)',
            'y_min_gr_zero' : 100,
            'y_max_log_fct' : 50.,
            # '_set_leg_1_col_log' : {
            #         'x_pos': 0.71,
            #         'y_pos': 0.67,
            #         'label_width': 0.30,
            #         'label_height': 0.040,
            #         'box_text_size' : 0.033,
            #         'opt': 'f',
            #         'opt_data': 'pl',
            #         'reverse': True,
            #         'sort_legend' : lambda w: 'TT ' in w[1],
            #     },
            # 'text_box_log' : (0.19, 0.82, "#scale[0.8]{#bf{CMS}}"),
            },
    'nobtag_boost_mass_nsjbtags_rebin_flex' : {
            'title' : 'N(b-tagged subjets)',
            'y_min_gr_zero' : 10,
            'y_max_log_fct' : 1000.,
            # '_set_leg_1_col_log' : {
            #         'x_pos': 0.75,
            #         'y_pos': 0.67,
            #         'label_width': 0.25,
            #         'label_height': 0.040,
            #         'box_text_size' : 0.033,
            #         'opt': 'f',
            #         'opt_data': 'pl',
            #         'reverse': True,
            #         'sort_legend' : lambda w: 'TT ' in w[1],
            #     },
            # 'draw_empty_bin_error' : True,
            },
    'noboost_mass_1b[0].m_pt' : {
            'title' : 'p_{T}(H-tag, 1 b-tagged subjet) [GeV]',
            'rebin' : 50,
            'scl_fct' : 3,
            # 'y_min_gr_zero' : 100,
            'y_max_log_fct' : 50.,
            },
    'noboost_mass_2b[0].m_pt' : {
            'title' : 'p_{T}(H-tag, 2 b-tagged subjets) [GeV]',
            'rebin' : 50,
            # 'y_min_gr_zero' : 100,
            'y_max_log_fct' : 50.,
            },
    'n_additional_btags_medium' : {
            'title' : 'N(b-tagged AK4 jets)',
            'y_min_gr_zero' : 0.001,
            'y_max_log_fct' : 100000.,
            '_set_leg_1_col_log' : {
                    'x_pos': 0.71,
                    'y_pos': 0.67,
                    'label_width': 0.25,
                    'label_height': 0.040,
                    'box_text_size' : 0.033,
                    'opt': 'f',
                    'opt_data': 'pl',
                    'reverse': True,
                    'sort_legend' : lambda w: 'TT ' in w[1],
                },
            # 'draw_empty_bin_error' : True,
            },
    'n_higgs_tags_1b_med' : {
            'title' : 'N(H-tagged AK8 jets, 1 b-tagged subjet)',
            'y_min_gr_zero' : 0.001,
            'y_max_log_fct' : 100000.,
            '_set_leg_1_col_log' : {
                    'x_pos': 0.71,
                    'y_pos': 0.67,
                    'label_width': 0.25,
                    'label_height': 0.040,
                    'box_text_size' : 0.033,
                    'opt': 'f',
                    'opt_data': 'pl',
                    'reverse': True,
                    'sort_legend' : lambda w: 'TT ' in w[1],
                },
            # 'draw_empty_bin_error' : True,
            },
    'n_higgs_tags_2b_med' : {
            'title' : 'N(H-tagged AK8 jets, 2 b-tagged subjets)',
            'y_min_gr_zero' : 0.0001,
            'y_max_log_fct' : 1000.,
            '_set_leg_1_col_log' : {
                    'x_pos': 0.71,
                    'y_pos': 0.67,
                    'label_width': 0.25,
                    'label_height': 0.040,
                    'box_text_size' : 0.033,
                    'opt': 'f',
                    'opt_data': 'pl',
                    'reverse': True,
                    'sort_legend' : lambda w: 'TT ' in w[1],
                },
            # 'draw_empty_bin_error' : True,
            },
    }

def get_style():
    # _style = style or varial.settings.style
    return [
        common_plot.mod_pre_bot_hist(mod_dict),
        common_plot.mk_split_err_ratio_plot_func_mod(poisson_errs=True),  # mk_pull_plot_func()
        # common_plot.mk_pull_plot_func(),  # mk_pull_plot_func()
        # common_plot.mk_pull_plot_func_poisson(),  # mk_pull_plot_func()
        # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
        rnd.mk_legend_func(),
        common_plot.mod_post_canv(mod_dict),
        common_plot.mk_tobject_draw_func(TLatex(0.52, 0.89, "#scale[0.45]{2.5 (e), 2.6 (#mu) fb^{-1} (13 TeV)}"))
    ]

# def get_style_poisson():
#     # _style = style or varial.settings.style
#     return [
#         common_plot.mod_pre_bot_hist(mod_dict),
#         # common_plot.mk_split_err_ratio_plot_func_mod(poisson_errs=True),  # mk_pull_plot_func()
#         common_plot.mk_pull_plot_func_poisson(),  # mk_pull_plot_func()
#         # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
#         rnd.mk_legend_func(),
#         common_plot.mod_post_canv(mod_dict),
#         common_plot.mk_tobject_draw_func(TLatex(0.51, 0.91, "#scale[0.5]{2.5 (e), 2.6 (#mu) fb^{-1} (13 TeV)}"))
#     ]



#           final state BRs:
#           nominal:            sample:
# bwbw:     0.25                0.111
# tZbw:     0.25                0.222
# tZtZ:     0.0625              0.111
# tHbW:     0.25                0.222
# tHtZ:     0.125               0.222
# tHtH:     0.0625              0.111

# plot.normfactors_ind_fs = {
#     '_thth' : 0.0625/0.111,
#     '_tztz' : 0.0625/0.111,
#     '_bwbw' : 0.25/0.111,
#     '_thtz' : 0.125/0.222,
#     '_thbw' : 0.25/0.222,
#     '_tzbw' : 0.25/0.222,
#     '_bhbh' : 0.0625/0.111,
#     '_bzbz' : 0.0625/0.111,
#     '_twtw' : 0.25/0.111,
#     '_bhbz' : 0.125/0.222,
#     '_bhtw' : 0.25/0.222,
#     '_bztw' : 0.25/0.222,
# }

# normfactors_ind_fs_rev = {
#     '_thth' : 1./0.0625,
#     '_tztz' : 1./0.0625,
#     '_bwbw' : 1./0.25,
#     '_thtz' : 1./0.125,
#     '_thbw' : 1./0.25,
#     '_tzbw' : 1./0.25,
#     '_bhbh' : 1./0.0625,
#     '_bzbz' : 1./0.0625,
#     '_twtw' : 1./0.25,
#     '_bhbz' : 1./0.125,
#     '_bhtw' : 1./0.25,
#     '_bztw' : 1./0.25,
# }

# QUESTION: which benchmark to use?? 100% tH or singlet/doublet??
# normfactors_ind_fs = {
#     '_thth' : 1./0.111,
#     '_tztz' : 0./0.111,
#     '_bwbw' : 0./0.111,
#     '_thtz' : 0./0.222,
#     '_thbw' : 0./0.222,
#     '_tzbw' : 0./0.222,
#     '_bhbh' : 0.0625/0.111,
#     '_bzbz' : 0.0625/0.111,
#     '_twtw' : 0.25/0.111,
#     '_bhbz' : 0.125/0.222,
#     '_bhtw' : 0.25/0.222,
#     '_bztw' : 0.25/0.222,
# }

# normfactors = {
#     '_thth' : 0.0625,
#     '_tztz' : 0.0625,
#     '_bwbw' : 0.25,
#     '_thtz' : 0.125,
#     '_thbw' : 0.25,
#     '_tzbw' : 0.25,
#     '_bhbh' : 0.0625,
#     '_bzbz' : 0.0625,
#     '_twtw' : 0.25,
#     '_bhbz' : 0.125,
#     '_bhtw' : 0.25,
#     '_bztw' : 0.25,
# }

glob_do_merging = False

normfactors_ind_fs = {
    '_thth' : 1./0.111,
    '_tztz' : 0./0.111,
    '_bwbw' : 0./0.111,
    '_thtz' : 0./0.222,
    '_thbw' : 0./0.222,
    '_tzbw' : 0./0.222,
    # '_bhbh' : 0.0625/0.111,
    # '_bzbz' : 0.0625/0.111,
    # '_twtw' : 0.25/0.111,
    # '_bhbz' : 0.125/0.222,
    # '_bhtw' : 0.25/0.222,
    # '_bztw' : 0.25/0.222,
}

normfactors_ind_fs_rev = {
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

# plot.normfactors_ind_fs = None

plot.normfactors_ind_fs_rev = None

# source_dir_htrew = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/'\
#     'UHH2/VLQToHiggsPairProd/NewSamples-76X-v1/FinalSelection-v24/'\
#     'Run8_withHighMassTTbarSample/RunAnalysis/HTReweighting/TreeProject'
source_dir_htrew = base_path+'/FullTreeProject/HTReweighting/TreeProject/'
source_dir_norew = base_path+'/FullTreeProject/NoReweighting/TreeProject/'
source_dir_top_pt_old = base_path+'/FullTreeProject/TopPtReweighting/TreeProject/'
source_dir_top_pt_old_nomax = base_path+'/FullTreeProject/TopPtNoMaxReweighting/TreeProject/'
source_dir_top_pt_new = base_path+'/FullTreeProject/TopPtNewReweighting/TreeProject/'

uncerts = list(analysis.all_uncerts)# or get_sys_dir()
uncerts.remove('sfmu_trg')
uncerts.remove('sflep_trg')
# nom_pattern_htrew = [source_dir_htrew+'/TreeProjector/{0}.root',
#                source_dir_htrew+'/TreeProjectorDiboson/{0}.root']
nom_pattern_htrew = [source_dir_htrew+'/TreeProjectorBkg/{0}.root',
               source_dir_htrew+'/TreeProjectorTT/{0}.root']
nom_pattern_htrew_bb = [source_dir_htrew+'/TreeProjectorBkg/{0}.root',
               source_dir_htrew+'/TreeProjectorBB/{0}.root']
nom_pattern_norew = [source_dir_norew+'/TreeProjectorBkg/{0}.root',
               source_dir_norew+'/TreeProjectorTT/{0}.root']
nom_pattern_top_pt_old = [source_dir_top_pt_old+'/TreeProjectorBkg/{0}.root',
               source_dir_top_pt_old+'/TreeProjectorTT/{0}.root']
nom_pattern_top_pt_old_nomax = [source_dir_top_pt_old_nomax+'/TreeProjectorBkg/{0}.root',
               source_dir_top_pt_old_nomax+'/TreeProjectorTT/{0}.root']
nom_pattern_top_pt_new = [source_dir_top_pt_new+'/TreeProjectorBkg/{0}.root',
               source_dir_top_pt_new+'/TreeProjectorTT/{0}.root']
# sys_pattern_htrew = list(source_dir_htrew+'/SysTreeProjectors/%s*/{0}.root'% i for i in uncerts) +\
#               list(source_dir_htrew+'/SysTreeProjectorsDiboson/%s*/{0}.root'% i for i in uncerts)
sys_pattern_htrew = list(source_dir_htrew+'/SysTreeProjectorsBkg/%s*/{0}.root'% i for i in uncerts + ['sfmu_trg']) +\
              list(source_dir_htrew+'/SysTreeProjectorsTT*/%s*/{0}.root'% i for i in uncerts + ['sfmu_trg'])
sys_pattern_htrew_bb = list(source_dir_htrew+'/SysTreeProjectorsBkg/%s*/{0}.root'% i for i in uncerts + ['sfmu_trg']) +\
              list(source_dir_htrew+'/SysTreeProjectorsBB*/%s*/{0}.root'% i for i in uncerts + ['sfmu_trg'])
sys_pattern_norew = list(source_dir_norew+'/SysTreeProjectorsBkg/%s*/{0}.root'% i for i in uncerts + ['sfmu_trg']) +\
              list(source_dir_norew+'/SysTreeProjectorsTT*/%s*/{0}.root'% i for i in uncerts + ['sfmu_trg'])
sys_pattern_top_pt_old = list(source_dir_top_pt_old+'/SysTreeProjectorsBkg/%s*/{0}.root'% i for i in ['top_pt_reweight', 'ScaleVar']) +\
              list(source_dir_top_pt_old+'/SysTreeProjectorsTT*/%s*/{0}.root'% i for i in ['top_pt_reweight', 'ScaleVar'])
sys_pattern_top_pt_old_nomax = list(source_dir_top_pt_old_nomax+'/SysTreeProjectorsBkg/%s*/{0}.root'% i for i in ['top_pt_reweight', 'ScaleVar']) +\
              list(source_dir_top_pt_old_nomax+'/SysTreeProjectorsTT*/%s*/{0}.root'% i for i in ['top_pt_reweight', 'ScaleVar'])
sys_pattern_top_pt_new = list(source_dir_top_pt_new+'/SysTreeProjectorsBkg/%s*/{0}.root'% i for i in ['top_pt_reweight', 'ScaleVar']) +\
              list(source_dir_top_pt_new+'/SysTreeProjectorsTT*/%s*/{0}.root'% i for i in ['top_pt_reweight', 'ScaleVar'])

bpbp_pattern = [source_dir_htrew+'/TreeProjectorBB/{0}.root'] + list(source_dir_htrew+'/SysTreeProjectorsBB*/%s*/{0}.root'% i for i in uncerts)

input_pattern_htrew = nom_pattern_htrew+sys_pattern_htrew
input_pattern_norew = nom_pattern_norew+sys_pattern_norew
input_pattern_top_pt_old = nom_pattern_top_pt_old+sys_pattern_top_pt_old
input_pattern_top_pt_old_nomax = nom_pattern_top_pt_old_nomax+sys_pattern_top_pt_old_nomax
input_pattern_top_pt_new = nom_pattern_top_pt_new+sys_pattern_top_pt_new

# theta_lim_path = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/'\
#     'UHH2/VLQToHiggsPairProd/NewSamples-76X-v1/FinalSelection-v24/'\
#     'Run8_withHighMassTTbarSample/RunAnalysis/HTReweighting/Limit/'\
#     'BackgroundOnlyFitNoTheory/CR/ThetaLimit/'
theta_lim_path = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/'\
    'UHH2/VLQToHiggsPairProd/NewSamples-76X-v1/FinalSelection-v26/ThesisPlots_1/BkgStudies/'\
    'NormEvalHTReweighting/ThetaLimit/'

dum_rate_uncerts = {
    'TTbar' : 1.20,
    'WJets' : 1.20,
    # 'DYJets' : 1.20,
    'SingleTop' : 1.16,
    'Diboson' : 1.15,
    'QCD' : 2.0,
}


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

# def set_line_style(wrps):
#     for w in wrps:
#         if w.sample in line_styles.keys():
#             w.histo.SetLineStyle(line_styles[w.sample])
#         yield w

def set_line_width(wrps):
    for w in wrps:
        if w.is_signal:
            w.histo.SetLineWidth(3)
        yield w

# def stack_setup(grps, rate_uncertainties=analysis.rate_uncertainties, shape_uncertainties=analysis.shape_uncertainties, include_rate=False):
#     grps = common_plot.make_uncertainty_histograms(grps, rate_uncertainties, shape_uncertainties, include_rate)
#     grps = gen.mc_stack_n_data_sum(grps, calc_sys_integral=True)
#     # if varial.settings.flex_sig_norm:
#     #     grps = common_plot.norm_to_bkg(grps)
#     # grps = common_plot.make_empty_bin_error(grps)
#     return grps


    kws['plot_grouper'] = lambda g: group_by_uncerts(g, lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))

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


def loader_hook_merge_regions(wrps, do_merging=True):
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

    wrps = plot.common_loader_hook(wrps)
    wrps = gen.gen_make_th2_projections(wrps)
    # wrps = gen.sort(wrps, ['sys_info', 'in_file_path', 'sample'])
    # wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_incl', print_warning=False, yield_orig=True)
    # wrps = list(wrps)
    # wrps = common_plot.norm_smpl(wrps, normfactors_ind_fs, calc_scl_fct=False)
    # wrps = common_plot.mod_legend_eff_counts(wrps)
    if do_merging:
        wrps = sorted(wrps, key=key)
        wrps = varial.gen.group(wrps, key)
        wrps = varial.gen.gen_merge(wrps)
        wrps = varial.gen.gen_add_wrp_info(wrps, in_file_path=get_new_infile_path, region=get_base_selection, sys_info=get_sys_info)
    else:
        wrps = varial.gen.gen_add_wrp_info(wrps, region=lambda w: w.in_file_path.split('/')[0])
    # wrps = list(wrps)
    # for w in wrps:
        # if w.sys_info.startswith('sfel') or w.sys_info.startswith('sfmu'):
            # print get_base_selection(w), w.sample, w.sys_info, w.variable
    wrps = sorted(wrps, key=lambda w: w.in_file_path)
    return wrps


def loader_hook_compare_finalstates(wrps):
    wrps = common_plot.rebin_st_and_nak4(wrps, mod_dict)
    wrps = plot.common_loader_hook(wrps)
    wrps = common_plot.mod_title(wrps, mod_dict)
    # wrps = common_plot.norm_smpl(wrps, normfactors_ind_fs_rev, calc_scl_fct=False)
    # wrps = common_plot.norm_smpl(wrps, normfactors_ind_fs, calc_scl_fct=False)
    wrps = sorted(wrps, key=lambda w: '{0}___{1}___{2}'.format(w.sys_info, w.in_file_path, w.sample))
    wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw'], suffix='_thX', print_warning=False)
    wrps = sorted(wrps, key=lambda w: '{0}___{1}___{2}'.format(w.sys_info, w.in_file_path, w.sample))
    wrps = vlq_common.merge_decay_channels(wrps, ['_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_other', print_warning=False)
    wrps = common_plot.set_line_style(wrps)
    # wrps = set_line_width(wrps)
    # wrps = gen.apply_linecolor(wrps)
    wrps = common_plot.norm_smpl_var(wrps, mod_dict)
    wrps = common_plot.mod_legend_eff_counts(wrps)
    # wrps = common_plot.norm_smpl(wrps, common_plot.pas_normfactors, mk_legend=False)
    # wrps = rename_samples(wrps)
    # wrps = sorted(wrps, key=lambda w: w.in_file_path+'___'+w.sys_info+'___'+w.sample)
    # wrps = vlq_common.merge_decay_channels(wrps, postfixes=['__TTbar', '__TTbar_split', '__SingleTop'], print_warning=False)
    # wrps = vlq_common.merge_decay_channels(wrps, postfixes=['__WJets', '__DYJets', '__Diboson'], print_warning=False)
    wrps = sorted(wrps, key=lambda w: w.in_file_path)
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
    # grps = merge_bkgs(grps)
    grps = gen.mc_stack_n_data_sum(grps, merge_mc_key_func=lambda w: varial.analysis.get_stack_position(w, stack_order), calc_sys_integral=True, add_sys_errs=True)
    # grps = common_plot.make_empty_bin_error(grps)
    return grps

def plot_merged_channels_higgs(final_dir):
    # plot_hists = ['ST', 'HT', 'n_ak4', 'topjets[0].m_pt', 'topjets[1].m_pt',
    #                 'n_ak8', 'met', 'pt_ld_ak4_jet', 'pt_subld_ak4_jet', 'jets[2].m_pt','jets[3].m_pt', 'jets[].m_pt', 'n_additional_btags_medium', 'n_prim_vertices',
    #                 'n_higgs_tags_1b_med_sm10', 'n_higgs_tags_2b_med_sm10', 'primary_electron_pt', 'primary_muon_pt', 'PrimaryLepton.Particle.m_eta', 'wtags_mass_softdrop',
    #                 'nobtag_boost_mass_nsjbtags', 'nomass_boost_1b_mass_softdrop', 'nomass_boost_2b_mass_softdrop', 'noboost_mass_1b[0].m_pt', 'noboost_mass_2b[0].m_pt']
    plot_hists = ['ST', 'HT', 'n_ak4', 'nomass_boost_1b_mass_softdrop', 'nomass_boost_2b_mass_softdrop', 'noboost_mass_1b[0].m_pt', 'noboost_mass_2b[0].m_pt', 'nobtag_boost_mass_nsjbtags']

    # stacking_order = [
    #     'TOP',
    #     'EWK',
    #     'QCD',
    # ]

    return tools.ToolChain(final_dir, [
        tools.ToolChainParallel('HistoLoader',
        list(tools.HistoLoader(
            pattern=map(lambda w: w.format('*'+g+'*'), input_pattern_htrew),
            filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in samples_all) and\
                'Region_Comb' not in w.in_file_path and\
                any(w.in_file_path.endswith(f) for f in plot_hists), # and\
                # common_plot.unselect_theory_uncert(w),
            hook_loaded_histos=loader_hook_merge_regions,
            name='HistoLoader_'+g,
            lookup_aliases=False,
            raise_on_empty_result=False,
            quiet_mode=True
            ) for g in samples_all)),
        # mk_toolchain('HistogramsNormToInt',
        #     filter_keyfunc=lambda w: 'TpTp' not in w.file_path,
        #     pattern=None, input_result_path='../HistoLoader/HistoLoader*',
        #     plotter_factory=plotter_factory_stack(analysis.rate_uncertainties, def_uncerts, hook_loaded_histos=loader_hook_norm_to_int,
        #         plot_setup=stack_setup_norm_all_to_intgr)),
        plot.mk_toolchain('HistogramsHiggsComp', pattern=None, input_result_path='../HistoLoader/HistoLoader*',
            filter_keyfunc=lambda w: all(g not in w.sample for g in ['TpTp_M-0800', 'TpTp_M-1600']) and common_plot.unselect_theory_uncert(w),
            plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=False, 
                hook_loaded_histos=loader_hook_compare_finalstates,
                stack_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=False, stack_order=settings.stacking_order),
                plot_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=False, stack_order=settings.stacking_order),
                mod_log=common_plot.mod_log_usr(mod_dict),
                canvas_post_build_funcs=get_style()
                ),
            parallel=True
            # pattern=None, input_result_path='../HistoLoader/HistoLoader*'
            ),
        # plot.mk_toolchain('HistogramsCompUncerts', samples_to_plot_all,
        #     filter_keyfunc=lambda w: any(f in w.file_path for f in [analysis.ttbar_smpl, 'QCD', 'WJets', 'TpTp_M-0800', 'TpTp_M-1600']) and any(w.in_file_path.endswith(g) for g in ['ST']),   
        #     plotter_factory=plot.plotter_factory_uncerts(
        #         hook_loaded_histos=lambda w: loader_hook_uncerts(loader_hook_compare_finalstates(w), 
        #             analysis.rate_uncertainties, uncerts, include_rate=False)),
        #     pattern=None, input_result_path='../HistoLoader/HistoLoader*'),
        # plot.mk_toolchain('HistogramsCompScaleVarHTRew', samples_to_plot_all,
        #     filter_keyfunc=lambda w: any(f in w.file_path for f in [analysis.ttbar_smpl, 'QCD', 'WJets', 'TpTp_M-0800', 'TpTp_M-1600']) and any(w.in_file_path.endswith(g) for g in ['ST']),   
        #     plotter_factory=plot.plotter_factory_uncerts(
        #         hook_loaded_histos=lambda w: loader_hook_uncerts(loader_hook_compare_finalstates(w), 
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
        tools.WebCreator()
        ])





def remove_final_states(wrps):
    for w in wrps:
        if not any(w.sample.endswith(a) for a in ['_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw']):
            # print w.sample
            yield w

def mod_wrp_norm(wrps):
    for w in wrps:
        w.y_max_log_fct = 1000.
        if not w.is_data and not w.is_signal:
            w.tot_fill_color = (2, 0.6)
            w.tot_fill_style = 3744
            # w.draw_option_legend = 'ple'
            # w.draw_x_errs = True
            w.tot_err_legend = 'Tot. bkg. uncert. (shape)'
            # w.draw_option_sum = 'sameE3'
            # print w.sample
            w._set_leg_2_col_log = None
            w._set_leg_1_col_log = {
                    'x_pos': 0.57,
                    'y_pos': 0.77,
                    'label_width': 0.25,
                    'label_height': 0.050,
                    'box_text_size' : 0.036,
                    'opt': 'f',
                    'opt_data': 'pl',
                    'reverse': True,
                    'sort_legend' : lambda w: 'TT ' in w[1],
                }
            w.histo.GetYaxis().SetTitle('A.U.')
        if w.is_data:
            w.draw_option = 'E0'
            w.draw_option_legend = 'ple'
        yield w

def mod_wrp_comp_uncert(wrps):
    for w in wrps:
        if 'ST_rebin_flex' in w.name:
            w.y_max_log_fct = 1000.
            w.y_min_gr_zero_ind = 2e-3
        yield w


def mod_wrp_comp_uncert_htrew_theo(wrps):
    for w in wrps:
        w.y_max_log_fct = 100000.
        # w._set_leg_2_col_log = {
        #         'x_pos': 0.68,
        #         'y_pos': 0.66,
        #         'label_width': 0.32,
        #         'label_height': 0.045,
        #         'box_text_size' : 0.035,
        #         'opt': 'f',
        #         'opt_data': 'pl',
        #         'reverse': True,
        #         # 'sort_legend' : lambda w: 'TT ' in w[1],
        #     }
        yield w


def filter_out_exp_unc(w):
    if w.sys_info:
        if any(g in w.sys_info for g in ['PDF', 'ScaleVar', 'PSScale']):
            return False
    return True



def filter_out_theo_unc(w):
    if w.sys_info:
        if any(g in w.sys_info for g in ['PDF', 'ScaleVar', 'PSScale']):
            return True
        else:
            return False
    return True


def loader_hook_nominal_brs(wrps, do_merging=glob_do_merging):
    wrps = plot.common_loader_hook(wrps)
    wrps = common_plot.mod_title(wrps, mod_dict)
    wrps = common_plot.rebin_st_and_nak4(wrps, mod_dict)
    wrps = common_plot.norm_smpl(wrps, normfactors_ind_fs, calc_scl_fct=False)
    if do_merging:
        wrps = sorted(wrps, key=lambda w: '{0}___{1}___{2}'.format(w.sys_info, w.in_file_path, w.sample))
        wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw'], print_warning=False, yield_orig=False)
        wrps = sorted(wrps, key=lambda w: '{0}___{1}___{2}'.format(w.sys_info, w.in_file_path, w.sample))
        wrps = vlq_common.merge_decay_channels(wrps, ['_bhbh', '_bhbz', '_bhtw', '_noH_bzbz', '_noH_bztw', '_noH_twtw'], print_warning=False, yield_orig=False)
    else:
        wrps = common_plot.mod_legend_no_thth(wrps)
    wrps = common_plot.set_line_style(wrps)
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

def loader_hook_norm_to_int_no_rebin(wrps):
    key = lambda w: '{0}___{1}___{2}___{3}'.format(w.in_file_path, w.is_data, w.is_signal if not w.is_signal else w.sample, w.sys_info)

    wrps = sorted(wrps, key=key)
    wrps = varial.gen.group(wrps, key)
    wrps = varial.gen.gen_merge(wrps)
    wrps = mod_wrp_norm(wrps)
    wrps = common_plot.norm_to_int(wrps)
    return wrps

def loader_hook_norm_to_int(wrps):
    wrps = common_plot.rebin_st_and_nak4(wrps, mod_dict)
    wrps = loader_hook_norm_to_int_no_rebin(wrps)
    return wrps

def loader_hook_uncerts(wrps, rate_uncertainties=analysis.rate_uncertainties, shape_uncertainties=analysis.shape_uncertainties, include_rate=False):
    wrps = sorted(wrps, key=lambda w: w.in_file_path)
    wrps = gen.group(wrps, lambda w: w.in_file_path)
    wrps = common_plot.make_uncertainty_histograms(wrps, rate_uncertainties, shape_uncertainties, include_rate)
    wrps = list(w for ws in wrps for w in ws)
    wrps = common_plot.set_line_width(wrps)
    wrps = mod_wrp_comp_uncert(wrps)
    wrps = sorted(wrps, key=lambda w: '{0}___{1}'.format(w.in_file_path, w.sample))
    return wrps


y_range_dict = {
    'TTbar_jec' : 0.5,
    'WJets_jec' : 0.3,
    'TTbar_jer' : 0.5,
    'WJets_jer' : 0.3,
}

def mk_style_uncert_plots(wrps):
    n = 0
    col_dict = {}
    for wrp in wrps:
        d = 1 if 'up' in wrp.legend else (-1 if 'down' in wrp.legend else 0)
        if d == 1:
            wrp.obj.SetLineColor(898)
            # wrp.obj.SetLineStyle(2)
        elif d == -1:
            wrp.obj.SetLineColor(434)
            # wrp.obj.SetLineStyle(2)
        wrp.obj.SetLineStyle(1)
        yield wrp

def mk_style_uncert_plots_ht_scalevar(wrps, colors):
    n = 0
    col_dict = {}
    for wrp in wrps:
        u = wrp.sys_info.split('__')[0]
        if u in col_dict:
            color = col_dict[u]
        else:
            color = colors[n % len(colors)]
            col_dict[u] = color
            n += 1
        wrp.obj.SetLineColor(color)
        wrp.color = color
        wrp.obj.SetLineWidth(2)
        # if d == 'up':
        # elif d == 'down':
            # wrp.obj.SetLineStyle(3)
        yield wrp

def set_yrange(grps):
    for g in grps:
        g = list(g)
        u, _ = g[1].legend.split(' ') if len(g[1].legend.split(' ')) == 2 else ('nominal', '')
        g[0].y_range = y_range_dict.get(g[0].sample+'_'+u, None)
        yield g        


sys_leg_dict = {
    'jec' : 'JES',
    'jer' : 'JER',
    'btag_bc' : 'b-tag heavy fl.',
    'btag_udsg' : 'b-tag light fl.',
    'ScaleVar' : '#mu_{RF} scales',
    'top_pt_reweight' : 'top-p_{T} rew.',
    'jsf' : 'H_{T} rew.',
    'ht_reweight' : 'H_{T} rew.',
    'pu' : 'pileup rew.',
    'higgs_scale' : 'AK8 jet m. sc.',
    'higgs_smear' : 'AK8 jet m. res.',
    'sfmu_trg' : '#mu trigger eff.',
    'sfmu_id' : '#mu id. eff.',
    'sfel_id' : 'e id. eff.',
}

def set_legend(wrps):
    for w in wrps:
        if not w.sys_info:
            w.legend = w.legend + ' nominal'
        else:
            smpl = w.legend
            tmp = w.sys_info.split('__')[0]
            tmp = sys_leg_dict.get(tmp, tmp)
            sys_dir = w.sys_info.split('__')[1]
            sys_dir = sys_dir.replace('plus', 'up').replace('minus', 'down')
            w.legend = ' '.join([smpl, tmp, sys_dir])
            w.histo.SetTitle(' '.join([smpl, tmp, sys_dir]))
        yield w

def plot_setup_uncerts_def(grps):
    grps = (set_legend(ws) for ws in grps)
    grps = (mk_style_uncert_plots(ws) for ws in grps)
    grps = list(grps)
    grps = set_yrange(grps)
    # grps = varial.plotter.default_plot_colorizer(grps)
    return grps

def plot_setup_uncerts_ht_scalevar(grps):

    grps = (set_legend(ws) for ws in grps)
    grps = (mk_style_uncert_plots_ht_scalevar(ws, [1, 898, 434, 801, 417]) for ws in grps)
    grps = list(grps)
    grps = set_yrange(grps)
    # grps = varial.plotter.default_plot_colorizer(grps)
    return grps


def stack_setup_postfit(grps, theta_res_path, signal, rate_uncertainties, shape_uncertainties, include_rate, veto_squash=()):
    grps = sensitivity.plot_setup_postfit(grps, theta_res_path, signal, rate_uncertainties, shape_uncertainties, include_rate, veto_squash)
    # grps = merge_bkgs(grps)
    grps = gen.mc_stack_n_data_sum(grps, calc_sys_integral=True, add_sys_errs=True)
    # grps = common_plot.make_empty_bin_error(grps)
    return grps

def stack_setup_norm_all_to_intgr(grps, rate_uncertainties=analysis.rate_uncertainties, shape_uncertainties=analysis.shape_uncertainties, include_rate=False):
    grps = common_plot.make_uncertainty_histograms(grps, rate_uncertainties, shape_uncertainties, include_rate)
    grps = gen.mc_stack_n_data_sum(grps, calc_sys_integral=False, add_sys_errs=True)
    # grps = common_plot.norm_stack_to_integral(grps)
    return grps



##### TODO: revisit squashing of uncertainties and assigning rate uncertainties!!!

def plot_merged_channels_postfit(final_dir):

    # settings.stacking_order = [
    #     'QCD',
    #     'EWK',
    #     'TOP',
    # ]

    return tools.ToolChain(final_dir, [
        tools.ToolChainParallel('HistoLoader',
            list(tools.HistoLoader(
                pattern=map(lambda w: w.format('*'+g+'*'), input_pattern_htrew),
                filter_keyfunc=lambda w: common_plot.unselect_theory_uncert(w) and\
                    any(f in w.file_path.split('/')[-1] for f in samples_to_plot_all) and\
                    'Region_Comb' not in w.in_file_path and\
                    any(w.in_file_path.endswith(f) for f in ['ST']),
                hook_loaded_histos=loader_hook_merge_regions,
                name='HistoLoader_'+g,
                lookup_aliases=False,
                raise_on_empty_result=False,
                quiet_mode=True
                ) for g in samples_to_plot_all)),
        plot.mk_toolchain('Histograms',
            plotter_factory=sensitivity.plotter_factory_postfit(theta_lim_path, '', dum_rate_uncerts, uncerts, True,
                hook_loaded_histos=lambda w: loader_hook_postfit_nominal_brs(w, theta_lim_path, '', dum_rate_uncerts),
                stack_setup=lambda w: stack_setup_postfit(w, theta_lim_path, '', dum_rate_uncerts, uncerts, True, ['QCD_rate', 'Diboson_rate', 'DYJets_rate', 'SingleTop_rate']),
                plot_setup=lambda w: stack_setup_postfit(w, theta_lim_path, '', dum_rate_uncerts, uncerts, True, ['QCD_rate', 'Diboson_rate', 'DYJets_rate', 'SingleTop_rate']),
                mod_log=common_plot.mod_log_usr(mod_dict),
                canvas_post_build_funcs=get_style()),
            pattern=None,
            input_result_path='../HistoLoader/HistoLoader*',
            parallel=False,
            # auto_legend=False,
            # name='HistogramsPostfit',
            # lookup_aliases=varial.settings.lookup_aliases
            ),
        plot.mk_toolchain('HistogramsPulls', samples_to_plot_all,
            plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=False,
                # filter_keyfunc=lambda w: not w.sys_info and not w.is_data,
                # hook_loaded_histos=loader_hook_nominal_brs,
                hook_loaded_histos=loader_hook_nominal_brs,
                stack_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=False),
                plot_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=False),
                mod_log=common_plot.mod_log_usr(mod_dict),
                canvas_post_build_funcs=[
                        common_plot.mod_pre_bot_hist(mod_dict),
                        # common_plot.mk_split_err_ratio_plot_func_mod(poisson_errs=True),  # mk_pull_plot_func()
                        # common_plot.mk_pull_plot_func(),  # mk_pull_plot_func()
                        common_plot.mk_pull_plot_func_poisson(y_min=-1.99, y_max=1.99),  # mk_pull_plot_func()
                        # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
                        rnd.mk_legend_func(),
                        common_plot.mod_post_canv(mod_dict),
                        common_plot.mk_tobject_draw_func(TLatex(0.53, 0.89, "#scale[0.45]{2.5 (e), 2.6 (#mu) fb^{-1} (13 TeV)}"))
                    ]
                ),
            pattern=None,
            input_result_path='../HistoLoader/HistoLoader*',
            # auto_legend=False,
            # name='HistogramsPostfit',
            # lookup_aliases=varial.settings.lookup_aliases
            ),
        tools.WebCreator()
        ])










def plot_merged_channels_prefit_norew(final_dir):

    plot_hists = [
        'ST',
        'HT',
        'n_ak4',
        'n_ak8',
        'nomass_boost_1b_mass_softdrop',
        'nomass_boost_2b_mass_softdrop',
        'noboost_mass_1b[0].m_pt',
        'noboost_mass_2b[0].m_pt',
        'nobtag_boost_mass_nsjbtags',
        'primary_lepton_pt',
        'pt_ld_ak4_jet',
        'pt_subld_ak4_jet',
        'topjets[0].m_pt',
        'topjets[1].m_pt',
        'met',
        'n_additional_btags_medium',
        'jets[].m_pt',
        'jets[2].m_pt',
        'jets[3].m_pt',
        'n_higgs_tags_1b_med',
        'n_higgs_tags_2b_med',
        'n_prim_vertices',
        ]

    # mod_dict_uncert = {

    #     'ST_rebin_flex' : {
    #             'title' : 'S_{T} [GeV]',
    #             'y_max_log_fct' : 100000.,
    #             'y_min_gr_zero' : 2e-3,
    #             'bin_width' : 100,
    #             '_set_leg_2_col_log' : {
    #                     'x_pos': 0.68,
    #                     'y_pos': 0.66,
    #                     'label_width': 0.32,
    #                     'label_height': 0.045,
    #                     'box_text_size' : 0.035,
    #                     'opt': 'f',
    #                     'opt_data': 'pl',
    #                     'reverse': True,
    #                     'sort_legend' : lambda w: 'TT ' in w[1],
    #                 },
    #             'y_max_fct' : 1.2,
    #             # 'text_box_lin' : (0.19, 0.82, "#scale[0.8]{#bf{CMS}}"),
    #             # 'text_box_log' : (0.16, 0.91, "#scale[0.8]{#bf{CMS}}"),
    #             'err_empty_bins' : True,
    #             'draw_x_errs' : True,
    #             # 'draw_empty_bin_error' : True
    #             },
    # }

    return tools.ToolChain(final_dir, [
        tools.ToolChainParallel('HistoLoader',
            list(tools.HistoLoader(
                pattern=map(lambda w: w.format('*'+g+'*'), input_pattern_norew),
                filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in samples_all) and\
                    'Region_Comb' not in w.in_file_path and\
                    any(w.in_file_path.endswith(f) for f in plot_hists),
                hook_loaded_histos=loader_hook_merge_regions,
                name='HistoLoader_'+g,
                lookup_aliases=False,
                raise_on_empty_result=False,
                quiet_mode=True
                ) for g in samples_all)),
        # plot.mk_toolchain('HistogramsHiggsCompNoSysNoDatNorm', samples_to_plot_all, 
        #     filter_keyfunc=lambda w: all(g not in w.sample for g in ['TpTp_M-1200', 'TpTp_M-1600']) and not w.sys_info and not w.is_data,
        #     plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=False, 
        #         hook_loaded_histos=lambda w: loader_hook_norm_to_int_no_rebin(loader_hook_compare_finalstates(w)),
        #         # stack_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=False),
        #         plot_setup=stack_setup_norm_all_to_intgr,
        #         mod_log=common_plot.mod_log_usr(mod_dict),
        #         canvas_post_build_funcs=[
        #                 common_plot.mod_pre_bot_hist(mod_dict),
        #                 common_plot.mk_split_err_ratio_plot_func_mod(poisson_errs=True),  # mk_pull_plot_func()
        #                 # common_plot.mk_pull_plot_func(),  # mk_pull_plot_func()
        #                 # common_plot.mk_pull_plot_func_poisson(),  # mk_pull_plot_func()
        #                 # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
        #                 rnd.mk_legend_func(x_pos=.55, y_pos=0.67, label_width=0.25, label_height=0.05, text_size=0.036),
        #                 common_plot.mod_post_canv(mod_dict),
        #                 common_plot.mk_tobject_draw_func(TLatex(0.16, 0.89, "#scale[0.6]{Simulation}")),
        #                 common_plot.mk_tobject_draw_func(TLatex(0.78, 0.89, "#scale[0.5]{(13 TeV)}"))
        #             ]
        #         ),
        #     pattern=None,
        #     input_result_path='../HistoLoader/HistoLoader*',
        #     quiet_mode=False
        #     # parallel=True
        #     # pattern=None, input_result_path='../HistoLoader/HistoLoader*'
        #     ),
        plot.mk_toolchain('HistogramsHiggsCompNoSysNoDat', samples_all, 
            filter_keyfunc=lambda w: all(g not in w.sample for g in ['TpTp_M-1200', 'TpTp_M-1600']) and not w.sys_info and not w.is_data,
            plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=False, 
                hook_loaded_histos=lambda w: common_plot.norm_smpl(loader_hook_compare_finalstates(w), sig_scalefactors, mk_legend=True),
                stack_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=False),
                plot_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=False),
                mod_log=common_plot.mod_log_usr(mod_dict),
                canvas_post_build_funcs=[
                        common_plot.mod_pre_bot_hist(mod_dict),
                        common_plot.mk_split_err_ratio_plot_func_mod(poisson_errs=True),  # mk_pull_plot_func()
                        # common_plot.mk_pull_plot_func(),  # mk_pull_plot_func()
                        # common_plot.mk_pull_plot_func_poisson(),  # mk_pull_plot_func()
                        # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
                        rnd.mk_legend_func(x_pos=0.65, y_pos=0.67, label_width=0.25, label_height=0.04, text_size=0.036),
                        common_plot.mod_post_canv(mod_dict),
                        common_plot.mk_tobject_draw_func(TLatex(0.16, 0.89, "#scale[0.6]{Simulation}")),
                        common_plot.mk_tobject_draw_func(TLatex(0.56, 0.89, "#scale[0.45]{2.5 (e), 2.6 (#mu) fb^{-1} (13 TeV)}"))
                    ]
                ),
            pattern=None,
            input_result_path='../HistoLoader/HistoLoader*',
            quiet_mode=False
            # parallel=True
            # pattern=None, input_result_path='../HistoLoader/HistoLoader*'
            ),
        plot.mk_toolchain('HistogramsPrefitNoSysNoDat', samples_to_plot_all,
            plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=False,
                filter_keyfunc=lambda w: not w.sys_info and not w.is_data,
                # hook_loaded_histos=loader_hook_nominal_brs,
                hook_loaded_histos=lambda w: common_plot.norm_smpl(loader_hook_nominal_brs(w), sig_scalefactors, mk_legend=True),
                stack_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=False),
                plot_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=False),
                mod_log=common_plot.mod_log_usr(mod_dict),
                canvas_post_build_funcs=[
                        common_plot.mod_pre_bot_hist(mod_dict),
                        # common_plot.mk_split_err_ratio_plot_func_mod(poisson_errs=True),  # mk_pull_plot_func()
                        # common_plot.mk_pull_plot_func(),  # mk_pull_plot_func()
                        # common_plot.mk_pull_plot_func_poisson(),  # mk_pull_plot_func()
                        # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
                        rnd.mk_legend_func(x_pos=.53, y_pos=0.67, label_width=0.25, label_height=0.05, text_size=0.036),
                        common_plot.mod_post_canv(mod_dict),
                        common_plot.mk_tobject_draw_func(TLatex(0.16, 0.89, "#scale[0.6]{Simulation}")),
                        common_plot.mk_tobject_draw_func(TLatex(0.56, 0.89, "#scale[0.45]{2.5 (e), 2.6 (#mu) fb^{-1} (13 TeV)}"))
                    ]
                ),
            pattern=None,
            input_result_path='../HistoLoader/HistoLoader*',
            # auto_legend=False,
            # name='HistogramsPostfit',
            # lookup_aliases=varial.settings.lookup_aliases
            ),
        plot.mk_toolchain('HistogramsPrefit', samples_to_plot_all,
            plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=False,
                # filter_keyfunc=lambda w: not w.sys_info and not w.is_data,
                # hook_loaded_histos=loader_hook_nominal_brs,
                hook_loaded_histos=loader_hook_nominal_brs,
                stack_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=False),
                plot_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=False),
                mod_log=common_plot.mod_log_usr(mod_dict),
                canvas_post_build_funcs=get_style()
                ),
            pattern=None,
            input_result_path='../HistoLoader/HistoLoader*',
            # auto_legend=False,
            # name='HistogramsPostfit',
            # lookup_aliases=varial.settings.lookup_aliases
            ),
        plot.mk_toolchain('HistogramsNormToIntAll',
            filter_keyfunc=lambda w: 'TpTp' not in w.file_path,
            pattern=None, input_result_path='../HistoLoader/HistoLoader*',
            plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, hook_loaded_histos=loader_hook_norm_to_int,
                plot_setup=stack_setup_norm_all_to_intgr,
                canvas_post_build_funcs=[
                    common_plot.mod_pre_bot_hist(mod_dict),
                    common_plot.mk_split_err_ratio_plot_func_mod(poisson_errs=True, tot_fill_color=(2, 0.6), tot_fill_style=3744, draw_stat_err=False),  # mk_pull_plot_func()
                    # common_plot.mk_pull_plot_func(),  # mk_pull_plot_func()
                    # common_plot.mk_pull_plot_func_poisson(),  # mk_pull_plot_func()
                    # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
                    rnd.mk_legend_func(),
                    common_plot.mod_post_canv(mod_dict),
                    common_plot.mk_tobject_draw_func(TLatex(0.52, 0.89, "#scale[0.45]{2.5 (e), 2.6 (#mu) fb^{-1} (13 TeV)}"))
                ]
            )),
        plot.mk_toolchain('HistogramsNormToIntExpSyst',
            filter_keyfunc=lambda w: 'TpTp' not in w.file_path and filter_out_exp_unc(w),
            pattern=None, input_result_path='../HistoLoader/HistoLoader*',
            plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, hook_loaded_histos=loader_hook_norm_to_int,
                plot_setup=stack_setup_norm_all_to_intgr,
                canvas_post_build_funcs=[
                    common_plot.mod_pre_bot_hist(mod_dict),
                    common_plot.mk_split_err_ratio_plot_func_mod(poisson_errs=True, tot_fill_color=(2, 0.6), tot_fill_style=3744, draw_stat_err=False),  # mk_pull_plot_func()
                    # common_plot.mk_pull_plot_func(),  # mk_pull_plot_func()
                    # common_plot.mk_pull_plot_func_poisson(),  # mk_pull_plot_func()
                    # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
                    rnd.mk_legend_func(),
                    common_plot.mod_post_canv(mod_dict),
                    common_plot.mk_tobject_draw_func(TLatex(0.52, 0.89, "#scale[0.45]{2.5 (e), 2.6 (#mu) fb^{-1} (13 TeV)}"))
                ]
            )),
        plot.mk_toolchain('HistogramsNormToIntThSyst',
            filter_keyfunc=lambda w: 'TpTp' not in w.file_path and filter_out_theo_unc(w),
            pattern=None, input_result_path='../HistoLoader/HistoLoader*',
            plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, hook_loaded_histos=loader_hook_norm_to_int,
                plot_setup=stack_setup_norm_all_to_intgr,
                canvas_post_build_funcs=[
                    common_plot.mod_pre_bot_hist(mod_dict),
                    common_plot.mk_split_err_ratio_plot_func_mod(poisson_errs=True, tot_fill_color=(2, 0.6), tot_fill_style=3744, draw_stat_err=False),  # mk_pull_plot_func()
                    # common_plot.mk_pull_plot_func(),  # mk_pull_plot_func()
                    # common_plot.mk_pull_plot_func_poisson(),  # mk_pull_plot_func()
                    # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
                    rnd.mk_legend_func(),
                    common_plot.mod_post_canv(mod_dict),
                    common_plot.mk_tobject_draw_func(TLatex(0.52, 0.89, "#scale[0.45]{2.5 (e), 2.6 (#mu) fb^{-1} (13 TeV)}"))
                ]
            )),
        plot.mk_toolchain('HistogramsPrefitNoSysFit', samples_to_plot_all,
            plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=False,
                filter_keyfunc=lambda w: not w.is_signal and not w.sys_info and 'HT' in w.name,
                # hook_loaded_histos=loader_hook_nominal_brs,
                hook_loaded_histos=lambda w: common_plot.norm_smpl(loader_hook_nominal_brs(w), sig_scalefactors, mk_legend=True),
                stack_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=False),
                plot_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=False),
                mod_log=common_plot.mod_log_usr(mod_dict),
                canvas_post_build_funcs=get_style() + [common_plot.mk_fit_bottom_plot()]
                ),
            pattern=None,
            input_result_path='../HistoLoader/HistoLoader*',
            # auto_legend=False,
            # name='HistogramsPostfit',
            # lookup_aliases=varial.settings.lookup_aliases
            ),
        plot.mk_toolchain('HistogramsCompUncerts', samples_to_plot_all,
            filter_keyfunc=lambda w: any(f in w.file_path for f in [analysis.ttbar_smpl, 'QCD', 'WJets', 'TpTp_M-0800', 'TpTp_M-1200']) and any(w.in_file_path.endswith(g) for g in ['ST']),   
            plotter_factory=plot.plotter_factory_uncerts(
                hook_loaded_histos=lambda w: loader_hook_uncerts(loader_hook_nominal_brs(w), 
                    analysis.rate_uncertainties, uncerts, include_rate=False),
                plot_setup=plot_setup_uncerts_def,
                mod_log=common_plot.mod_log_usr(mod_dict),
                canvas_post_build_funcs= [
                    # common_plot.mod_pre_bot_hist(mod_dict),
                    rnd.mk_legend_func(x_pos=0.32, y_pos=0.76, label_width=0.25, label_height=0.05, text_size=0.036),
                    common_plot.mk_bottom_plot_ratio_uncerts(),
                    common_plot.mk_tobject_draw_func(TLatex(0.16, 0.89, "#scale[0.6]{Simulation}")),
                    common_plot.mk_tobject_draw_func(TLatex(0.52, 0.89, "#scale[0.45]{2.5 (e), 2.6 (#mu) fb^{-1} (13 TeV)}")),
                    # common_plot.mod_post_canv(mod_dict_uncert),
                    ]),
            pattern=None, input_result_path='../HistoLoader/HistoLoader*'),
        plot.mk_toolchain('HistogramsPrefitNoSysNoDatNoScale', samples_to_plot_all,
            plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=False,
                filter_keyfunc=lambda w: not w.sys_info and not w.is_data,
                # hook_loaded_histos=loader_hook_nominal_brs,
                hook_loaded_histos=lambda w: loader_hook_nominal_brs(w),
                stack_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=False),
                plot_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=False),
                mod_log=common_plot.mod_log_usr(mod_dict),
                canvas_post_build_funcs=[
                        common_plot.mod_pre_bot_hist(mod_dict),
                        # common_plot.mk_split_err_ratio_plot_func_mod(poisson_errs=True),  # mk_pull_plot_func()
                        # common_plot.mk_pull_plot_func(),  # mk_pull_plot_func()
                        # common_plot.mk_pull_plot_func_poisson(),  # mk_pull_plot_func()
                        # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
                        rnd.mk_legend_func(x_pos=.53, y_pos=0.67, label_width=0.25, label_height=0.05, text_size=0.036),
                        common_plot.mod_post_canv(mod_dict),
                        common_plot.mk_tobject_draw_func(TLatex(0.16, 0.89, "#scale[0.6]{Simulation}")),
                        common_plot.mk_tobject_draw_func(TLatex(0.56, 0.89, "#scale[0.45]{2.5 (e), 2.6 (#mu) fb^{-1} (13 TeV)}"))
                    ]
                ),
            pattern=None,
            input_result_path='../HistoLoader/HistoLoader*',
            # auto_legend=False,
            # name='HistogramsPostfit',
            # lookup_aliases=varial.settings.lookup_aliases
            ),
        tools.WebCreator()
        ])












def plot_merged_channels_prefit_top_pt(final_dir):

    # settings.stacking_order = [
    #     'QCD',
    #     'EWK',
    #     'TOP',
    # ]


    return tools.ToolChain(final_dir, list(
        tools.ToolChain(name, [
            tools.ToolChainParallel('HistoLoader',
                list(tools.HistoLoader(
                    pattern=map(lambda w: w.format('*'+g+'*'), pat),
                    filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in samples_to_plot_all) and\
                        'Region_Comb' not in w.in_file_path and\
                        any(w.in_file_path.endswith(f) for f in ['ST'])\
                        and 'TpTp' not in w.file_path,
                    hook_loaded_histos=loader_hook_merge_regions,
                    name='HistoLoader_'+g,
                    lookup_aliases=False,
                    raise_on_empty_result=False,
                    quiet_mode=True
                    ) for g in samples_to_plot_all)),
                plot.mk_toolchain('Histograms', samples_to_plot_all,
                    plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, ['top_pt_reweight', 'ScaleVar'], include_rate=False, 
                        hook_loaded_histos=lambda w: loader_hook_nominal_brs(w, False),
                        stack_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, ['top_pt_reweight', 'ScaleVar'], include_rate=False),
                        plot_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, ['top_pt_reweight', 'ScaleVar'], include_rate=False),
                        mod_log=common_plot.mod_log_usr(mod_dict),
                        canvas_post_build_funcs=get_style()
                        ),
                    pattern=None,
                    input_result_path='../HistoLoader/HistoLoader*',
                    # auto_legend=False,
                    # name='HistogramsPostfit',
                    # lookup_aliases=varial.settings.lookup_aliases
                    ),
                plot.mk_toolchain('HistogramsNormToIntAll', samples_to_plot_all,
                    filter_keyfunc=lambda w: 'TpTp' not in w.file_path, 
                    pattern=None, input_result_path='../HistoLoader/HistoLoader*',
                    plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, ['top_pt_reweight', 'ScaleVar'], hook_loaded_histos=loader_hook_norm_to_int,
                        plot_setup=stack_setup_norm_all_to_intgr,
                        canvas_post_build_funcs=[
                            common_plot.mod_pre_bot_hist(mod_dict),
                            common_plot.mk_split_err_ratio_plot_func_mod(poisson_errs=True, tot_fill_color=(2, 0.6), tot_fill_style=3744, draw_stat_err=False),  # mk_pull_plot_func()
                            # common_plot.mk_pull_plot_func(),  # mk_pull_plot_func()
                            # common_plot.mk_pull_plot_func_poisson(),  # mk_pull_plot_func()
                            # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
                            rnd.mk_legend_func(),
                            common_plot.mod_post_canv(mod_dict),
                            common_plot.mk_tobject_draw_func(TLatex(0.52, 0.89, "#scale[0.45]{2.5 (e), 2.6 (#mu) fb^{-1} (13 TeV)}"))
                        ]
                    )),
                plot.mk_toolchain('HistogramsCompUncerts', samples_to_plot_all,
                    filter_keyfunc=lambda w: any(f in w.file_path for f in [analysis.ttbar_smpl]) and any(w.in_file_path.endswith(g) for g in ['ST']),   
                    plotter_factory=plot.plotter_factory_uncerts(
                        hook_loaded_histos=lambda w: loader_hook_uncerts(loader_hook_compare_finalstates(w), 
                            analysis.rate_uncertainties, ['top_pt_reweight'], include_rate=False),
                        plot_setup=plot_setup_uncerts_def,
                        mod_log=common_plot.mod_log_usr(),
                        canvas_post_build_funcs= [
                            # common_plot.mod_pre_bot_hist(mod_dict),
                            rnd.mk_legend_func(x_pos=0.32, y_pos=0.76, label_width=0.25, label_height=0.05, text_size=0.036),
                            common_plot.mk_bottom_plot_ratio_uncerts(),
                            common_plot.mk_tobject_draw_func(TLatex(0.16, 0.89, "#scale[0.6]{Simulation}")),
                            common_plot.mk_tobject_draw_func(TLatex(0.52, 0.89, "#scale[0.45]{2.5 (e), 2.6 (#mu) fb^{-1} (13 TeV)}"))
                            ]),
                    pattern=None, input_result_path='../HistoLoader/HistoLoader*'),
                tools.WebCreator()
                ]
            ) for name, pat in [('TopPtOld', input_pattern_top_pt_old), ('TopPtOldNoMax', input_pattern_top_pt_old_nomax), ('TopPtNew', input_pattern_top_pt_new)]
        )
    )

def group_by_uncerts_comp_ht_scalevar(wrps, first_sort_func):
    def sort_key_func(wrp):
        if wrp.sys_info.startswith('ScaleVar') or wrp.sys_info.startswith('jsf') or wrp.sys_info.startswith('rate') or wrp.sys_info.startswith('PDF'):
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















def plot_merged_channels_prefit(final_dir):

    # settings.stacking_order = [
    #     'QCD',
    #     'EWK',
    #     'TOP',
    # ]

    plot_hists = [
        'ST',
        'HT',
        'n_ak4',
        'n_ak8',
        'nomass_boost_1b_mass_softdrop',
        'nomass_boost_2b_mass_softdrop',
        'noboost_mass_1b[0].m_pt',
        'noboost_mass_2b[0].m_pt',
        'nobtag_boost_mass_nsjbtags',
        'primary_lepton_pt',
        'pt_ld_ak4_jet',
        'pt_subld_ak4_jet',
        'topjets[0].m_pt',
        'topjets[1].m_pt',
        'met',
        'n_additional_btags_medium',
        'jets[].m_pt',
        'jets[2].m_pt',
        'jets[3].m_pt',
        'n_higgs_tags_1b_med',
        'n_higgs_tags_2b_med',
        'n_prim_vertices',
        ]

    def sort_leg_comp_uncert(l):
        comps = l.split(' ')
        if comps[-1] == 'nominal':
            return 'zzz'
        elif comps[-1] == 'MC':
            return 'aaa'
        else:
            return comps[-2]


    return tools.ToolChain(final_dir, [
        tools.ToolChainParallel('HistoLoader',
            list(tools.HistoLoader(
                pattern=map(lambda w: w.format('*'+g+'*'), input_pattern_htrew),
                filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in samples_to_plot_all) and\
                    'Region_Comb' not in w.in_file_path and\
                    any(w.in_file_path.endswith(f) for f in plot_hists),
                hook_loaded_histos=loader_hook_merge_regions,
                name='HistoLoader_'+g,
                lookup_aliases=False,
                raise_on_empty_result=False,
                quiet_mode=True
                ) for g in samples_to_plot_all)),
        plot.mk_toolchain('HistogramsPrefitNoSys', samples_to_plot_all,
            plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=False, 
                filter_keyfunc=lambda w: not w.is_signal and not w.sys_info and common_plot.unselect_theory_uncert(w),
                hook_loaded_histos=loader_hook_nominal_brs,
                stack_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=False),
                plot_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=False),
                mod_log=common_plot.mod_log_usr(mod_dict),
                canvas_post_build_funcs=get_style()
                ),
            pattern=None,
            input_result_path='../HistoLoader/HistoLoader*',
            # auto_legend=False,
            # name='HistogramsPostfit',
            # lookup_aliases=varial.settings.lookup_aliases
            ),
        plot.mk_toolchain('HistogramsPrefit', samples_to_plot_all,
            plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=False,
                filter_keyfunc=common_plot.unselect_theory_uncert,
                hook_loaded_histos=loader_hook_nominal_brs,
                stack_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=False),
                plot_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=False),
                mod_log=common_plot.mod_log_usr(mod_dict),
                canvas_post_build_funcs=get_style()
                ),
            pattern=None,
            input_result_path='../HistoLoader/HistoLoader*',
            # auto_legend=False,
            # name='HistogramsPostfit',
            # lookup_aliases=varial.settings.lookup_aliases
            ),
        plot.mk_toolchain('HistogramsCompScaleVarHTRew', samples_to_plot_all,
            filter_keyfunc=lambda w: any(f in w.file_path for f in [analysis.ttbar_smpl, 'WJets', 'TpTp_M-0800', 'TpTp_M-1600']) and any(w.in_file_path.endswith(g) for g in ['ST']),   
            plotter_factory=plot.plotter_factory_uncerts(
                hook_loaded_histos=lambda w: mod_wrp_comp_uncert_htrew_theo(loader_hook_uncerts(loader_hook_compare_finalstates(w), 
                    analysis.rate_uncertainties, uncerts, include_rate=False)),
                plot_grouper=lambda g: group_by_uncerts_comp_ht_scalevar(g, lambda w: '{0}___{1}'.format(w.in_file_path, w.sample)),
                mod_log=common_plot.mod_log_usr(mod_dict),
                plot_setup=plot_setup_uncerts_ht_scalevar,
                canvas_post_build_funcs= [
                    # common_plot.mod_pre_bot_hist(mod_dict),
                    rnd.mk_legend_func(x_pos=0.63, y_pos=0.67, label_width=0.25, label_height=0.05, text_size=0.036, sort_legend=sort_leg_comp_uncert),
                    common_plot.mk_bottom_plot_ratio_uncerts(),
                    common_plot.mk_tobject_draw_func(TLatex(0.16, 0.89, "#scale[0.6]{Simulation}")),
                    common_plot.mk_tobject_draw_func(TLatex(0.52, 0.89, "#scale[0.45]{2.5 (e), 2.6 (#mu) fb^{-1} (13 TeV)}"))
                    ]
                ),
            pattern=None, input_result_path='../HistoLoader/HistoLoader*'),
        plot.mk_toolchain('HistogramsCompUncerts', samples_to_plot_all,
            filter_keyfunc=lambda w: any(f in w.file_path for f in [analysis.ttbar_smpl, 'QCD', 'WJets', 'TpTp_M-0800', 'TpTp_M-1200']) and any(w.in_file_path.endswith(g) for g in ['ST']),   
            plotter_factory=plot.plotter_factory_uncerts(
                hook_loaded_histos=lambda w: loader_hook_uncerts(loader_hook_nominal_brs(w), 
                    analysis.rate_uncertainties, uncerts, include_rate=False),
                plot_setup=plot_setup_uncerts_def,
                mod_log=common_plot.mod_log_usr(mod_dict),
                canvas_post_build_funcs= [
                    # common_plot.mod_pre_bot_hist(mod_dict),
                    rnd.mk_legend_func(x_pos=0.32, y_pos=0.76, label_width=0.25, label_height=0.05, text_size=0.036),
                    common_plot.mk_bottom_plot_ratio_uncerts(),
                    common_plot.mk_tobject_draw_func(TLatex(0.16, 0.89, "#scale[0.6]{Simulation}")),
                    common_plot.mk_tobject_draw_func(TLatex(0.52, 0.89, "#scale[0.45]{2.5 (e), 2.6 (#mu) fb^{-1} (13 TeV)}")),
                    # common_plot.mod_post_canv(mod_dict_uncert),
                    ]),
            pattern=None, input_result_path='../HistoLoader/HistoLoader*'),
        # plot.mk_toolchain('HistogramsHiggsCompNoSysNoDat', samples_all, 
        #     filter_keyfunc=lambda w: all(g not in w.sample for g in ['TpTp_M-1200', 'TpTp_M-1600']),
        #     plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=False, 
        #         hook_loaded_histos=lambda w: common_plot.norm_smpl(loader_hook_compare_finalstates(w), sig_scalefactors, mk_legend=True),
        #         stack_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=False),
        #         plot_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=False),
        #         mod_log=common_plot.mod_log_usr(mod_dict),
        #         canvas_post_build_funcs=[
        #                 common_plot.mod_pre_bot_hist(mod_dict),
        #                 common_plot.mk_split_err_ratio_plot_func_mod(poisson_errs=True),  # mk_pull_plot_func()
        #                 # common_plot.mk_pull_plot_func(),  # mk_pull_plot_func()
        #                 # common_plot.mk_pull_plot_func_poisson(),  # mk_pull_plot_func()
        #                 # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
        #                 rnd.mk_legend_func(x_pos=0.65, y_pos=0.67, label_width=0.25, label_height=0.04, text_size=0.036),
        #                 common_plot.mod_post_canv(mod_dict),
        #                 common_plot.mk_tobject_draw_func(TLatex(0.16, 0.89, "#scale[0.6]{Simulation}")),
        #                 common_plot.mk_tobject_draw_func(TLatex(0.56, 0.89, "#scale[0.45]{2.5 (e), 2.6 (#mu) fb^{-1} (13 TeV)}"))
        #             ]
        #         ),
        #     pattern=None,
        #     input_result_path='../HistoLoader/HistoLoader*',
        #     quiet_mode=False
        #     # parallel=True
        #     # pattern=None, input_result_path='../HistoLoader/HistoLoader*'
        #     ),
        plot.mk_toolchain('HistogramsPrefitPulls', samples_to_plot_all,
            plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=False,
                # filter_keyfunc=lambda w: not w.sys_info and not w.is_data,
                # hook_loaded_histos=loader_hook_nominal_brs,
                hook_loaded_histos=loader_hook_nominal_brs,
                stack_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=False),
                plot_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, uncerts, include_rate=False),
                mod_log=common_plot.mod_log_usr(mod_dict),
                canvas_post_build_funcs=[
                        common_plot.mod_pre_bot_hist(mod_dict),
                        # common_plot.mk_split_err_ratio_plot_func_mod(poisson_errs=True),  # mk_pull_plot_func()
                        # common_plot.mk_pull_plot_func(),  # mk_pull_plot_func()
                        common_plot.mk_pull_plot_func_poisson(),  # mk_pull_plot_func()
                        # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
                        rnd.mk_legend_func(),
                        common_plot.mod_post_canv(mod_dict),
                        common_plot.mk_tobject_draw_func(TLatex(0.53, 0.89, "#scale[0.45]{2.5 (e), 2.6 (#mu) fb^{-1} (13 TeV)}"))
                    ]
                ),
            pattern=None,
            input_result_path='../HistoLoader/HistoLoader*',
            # auto_legend=False,
            # name='HistogramsPostfit',
            # lookup_aliases=varial.settings.lookup_aliases
            ),
        tools.WebCreator()
        ])



def plot_comp_hists_split_channel(final_dir):

    # settings.stacking_order = [
    #     'QCD',
    #     'EWK',
    #     'TOP',
    # ]

    plot_hists = [
        'ST',
        'HT',
        # 'n_ak4',
        # 'n_ak8',
        # 'nomass_boost_1b_mass_softdrop',
        # 'nomass_boost_2b_mass_softdrop',
        # 'noboost_mass_1b[0].m_pt',
        # 'noboost_mass_2b[0].m_pt',
        # 'nobtag_boost_mass_nsjbtags',
        # 'primary_lepton_pt',
        # 'pt_ld_ak4_jet',
        # 'pt_subld_ak4_jet',
        # 'topjets[0].m_pt',
        # 'topjets[1].m_pt',
        # 'met',
        # 'n_additional_btags_medium',
        # 'jets[].m_pt',
        # 'jets[2].m_pt',
        # 'jets[3].m_pt',
        # 'n_higgs_tags_1b_med',
        # 'n_higgs_tags_2b_med',
        # 'n_prim_vertices',
        ]



    return tools.ToolChain(final_dir, [
        tools.ToolChainParallel('HistoLoader',
            list(tools.HistoLoader(
                pattern=map(lambda w: w.format('*'+g+'*'), input_pattern_htrew),
                filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in samples_to_plot_all) and\
                    'Region_Comb' not in w.in_file_path and\
                    any(w.in_file_path.endswith(f) for f in plot_hists),
                hook_loaded_histos=lambda w: loader_hook_merge_regions(w, False),
                name='HistoLoader_'+g,
                lookup_aliases=False,
                raise_on_empty_result=False,
                quiet_mode=True
                ) for g in samples_to_plot_all)),
        plot.mk_toolchain('HistogramsCompUncerts', samples_to_plot_all,
            filter_keyfunc=lambda w: any(f in w.file_path for f in [analysis.ttbar_smpl, 'QCD', 'WJets', 'TpTp_M-0800', 'TpTp_M-1200']) and any(w.in_file_path.endswith(g) for g in ['ST']),   
            plotter_factory=plot.plotter_factory_uncerts(
                hook_loaded_histos=lambda w: loader_hook_uncerts(loader_hook_nominal_brs(w), 
                    analysis.rate_uncertainties, uncerts+['sfmu_trg'], include_rate=False),
                plot_setup=plot_setup_uncerts_def,
                mod_log=common_plot.mod_log_usr(mod_dict),
                canvas_post_build_funcs= [
                    # common_plot.mod_pre_bot_hist(mod_dict),
                    rnd.mk_legend_func(x_pos=0.32, y_pos=0.76, label_width=0.25, label_height=0.05, text_size=0.036),
                    common_plot.mk_bottom_plot_ratio_uncerts(),
                    common_plot.mk_tobject_draw_func(TLatex(0.16, 0.89, "#scale[0.6]{Simulation}")),
                    common_plot.mk_tobject_draw_func(TLatex(0.52, 0.89, "#scale[0.45]{2.5 (e), 2.6 (#mu) fb^{-1} (13 TeV)}")),
                    # common_plot.mod_post_canv(mod_dict_uncert),
                    ]),
            pattern=None, input_result_path='../HistoLoader/HistoLoader*'),
        tools.WebCreator()
        ])




                                                                                                              
#                                          bbbbbbbb                                                         
# TTTTTTTTTTTTTTTTTTTTTTT                  b::::::b            lllllll                                      
# T:::::::::::::::::::::T                  b::::::b            l:::::l                                      
# T:::::::::::::::::::::T                  b::::::b            l:::::l                                      
# T:::::TT:::::::TT:::::T                   b:::::b            l:::::l                                      
# TTTTTT  T:::::T  TTTTTT  aaaaaaaaaaaaa    b:::::bbbbbbbbb     l::::l     eeeeeeeeeeee        ssssssssss   
#         T:::::T          a::::::::::::a   b::::::::::::::bb   l::::l   ee::::::::::::ee    ss::::::::::s  
#         T:::::T          aaaaaaaaa:::::a  b::::::::::::::::b  l::::l  e::::::eeeee:::::eess:::::::::::::s 
#         T:::::T                   a::::a  b:::::bbbbb:::::::b l::::l e::::::e     e:::::es::::::ssss:::::s
#         T:::::T            aaaaaaa:::::a  b:::::b    b::::::b l::::l e:::::::eeeee::::::e s:::::s  ssssss 
#         T:::::T          aa::::::::::::a  b:::::b     b:::::b l::::l e:::::::::::::::::e    s::::::s      
#         T:::::T         a::::aaaa::::::a  b:::::b     b:::::b l::::l e::::::eeeeeeeeeee        s::::::s   
#         T:::::T        a::::a    a:::::a  b:::::b     b:::::b l::::l e:::::::e           ssssss   s:::::s 
#       TT:::::::TT      a::::a    a:::::a  b:::::bbbbbb::::::bl::::::le::::::::e          s:::::ssss::::::s
#       T:::::::::T      a:::::aaaa::::::a  b::::::::::::::::b l::::::l e::::::::eeeeeeee  s::::::::::::::s 
#       T:::::::::T       a::::::::::aa:::a b:::::::::::::::b  l::::::l  ee:::::::::::::e   s:::::::::::ss  
#       TTTTTTTTTTT        aaaaaaaaaa  aaaa bbbbbbbbbbbbbbbb   llllllll    eeeeeeeeeeeeee    sssssssssss    
                                                                                                              
                                                                                                              
                                                                                                              
                                                                                                              
                                                                                                              
                                                                                                              
                                                                                                              




def loader_hook_tables_eff(wrps):
    wrps = plot.common_loader_hook(wrps)
    wrps = common_plot.mod_title(wrps, mod_dict)
    # wrps = common_plot.rebin_st_and_nak4(wrps, mod_dict)
    wrps = common_plot.norm_smpl(wrps, normfactors_ind_fs_rev, calc_scl_fct=False)
    # if do_merging:
        # wrps = sorted(wrps, key=lambda w: '{0}___{1}___{2}'.format(w.sys_info, w.in_file_path, w.sample))
        # wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw'], print_warning=False, yield_orig=False)
        # wrps = sorted(wrps, key=lambda w: '{0}___{1}___{2}'.format(w.sys_info, w.in_file_path, w.sample))
        # wrps = vlq_common.merge_decay_channels(wrps, ['_bhbh', '_bhbz', '_bhtw', '_noH_bzbz', '_noH_bztw', '_noH_twtw'], print_warning=False, yield_orig=False)
    # wrps = set_line_style(wrps)
    # wrps = rename_samples(wrps)
    # wrps = sorted(wrps, key=lambda w: w.in_file_path+'___'+w.sys_info+'___'+w.sample)
    # wrps = vlq_common.merge_decay_channels(wrps, postfixes=['__TTbar', '__TTbar_split', '__SingleTop'], print_warning=False)
    # wrps = vlq_common.merge_decay_channels(wrps, postfixes=['__WJets', '__DYJets', '__Diboson'], print_warning=False)
    # wrps = remove_final_states(wrps)
    # wrps = common_plot.norm_smpl(wrps, {'_thth' : 1./0.0625}, calc_scl_fct=False)
    # wrps = common_plot.mod_legend_no_thth(wrps)
    wrps = sorted(wrps, key=lambda w: w.region+'__'+w.name)
    return wrps

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


table_block_background = common_plot.table_block_background

def get_table_category_block_all(hist_path='Histograms'):
    return [
        ('Preselection', common_plot.get_dict('../%s/StackedAll/BaseLineSelection' % hist_path, 'ST')),
        ('0H category', common_plot.get_dict('../%s/StackedAll/SidebandRegion' % hist_path, 'ST')),
        ('H1b category', common_plot.get_dict('../%s/StackedAll/SignalRegion1b' % hist_path , 'ST')),
        ('H2b category', common_plot.get_dict('../%s/StackedAll/SignalRegion2b' % hist_path, 'ST')),
        ('boosted Higgs comb.', common_plot.get_dict_comb('../%s/StackedAll/SignalRegion*' % hist_path, 'ST')),
    ]

def get_table_category_block_final_cats(hist_path='Histograms'):
    return [
        ('0H category', common_plot.get_dict('../%s/StackedAll/SidebandRegion' % hist_path, 'ST')),
        ('H1b category', common_plot.get_dict('../%s/StackedAll/SignalRegion1b' % hist_path , 'ST')),
        ('H2b category', common_plot.get_dict('../%s/StackedAll/SignalRegion2b' % hist_path, 'ST')),
    ]

def get_table_category_block_final_cats_comb(hist_path='Histograms'):
    return [
        ('0H category', common_plot.get_dict('../%s/StackedAll/SidebandRegion' % hist_path, 'ST')),
        ('H1b category', common_plot.get_dict('../%s/StackedAll/SignalRegion1b' % hist_path , 'ST')),
        ('H2b category', common_plot.get_dict('../%s/StackedAll/SignalRegion2b' % hist_path, 'ST')),
        # ('boosted Higgs comb.', common_plot.get_dict_comb('../%s/StackedAll/SignalRegion*' % hist_path, 'ST')),
    ]

def plot_merged_channels_tables(final_dir):
    return tools.ToolChain(final_dir, [
        tools.ToolChainParallel('HistoLoaderPost',
            list(tools.HistoLoader(
                pattern=map(lambda w: w.format('*'+g+'*'), input_pattern_htrew + bpbp_pattern),
                filter_keyfunc=lambda w: common_plot.unselect_theory_uncert(w) and\
                    any(f in w.file_path.split('/')[-1] for f in samples_for_tables) and\
                    'Region_Comb' not in w.in_file_path and\
                    any(w.in_file_path.endswith(f) for f in ['ST']),
                hook_loaded_histos=loader_hook_merge_regions,
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
                hook_loaded_histos=loader_hook_tables_eff
                ),
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
            get_table_category_block_final_cats('HistogramsTablesPostfit'),
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
            get_table_category_block_final_cats('HistogramsTablesPrefit'),
            squash_errs=True,
            name='CountTablePreFit'
            ),
        EffTable([
                common_plot.table_block_signal_fs_800,
                common_plot.table_block_signal_fs_1200,
                # common_plot.table_block_signal_bb_fs_800,
                # common_plot.table_block_signal_bb_fs_1200,
            ],
            get_table_category_block_all('HistogramsTablesEffs'),
            common_plot.norm_factors,
            squash_errs=True,
            name='EffTableCompFSAll'
            ),
        EffTable([
                common_plot.table_block_signal_fs_800,
                common_plot.table_block_signal_fs_1200,
                # common_plot.table_block_signal_bb_fs_800,
                # common_plot.table_block_signal_bb_fs_1200,
            ],
            get_table_category_block_final_cats('HistogramsTablesEffs'),
            common_plot.norm_factors,
            squash_errs=True,
            name='EffTableCompFSFinalCuts'
            ),
        EffTable([
                common_plot.table_block_signal_fs_800,
                common_plot.table_block_signal_fs_1200,
                # common_plot.table_block_signal_bb_fs_800,
                # common_plot.table_block_signal_bb_fs_1200,
            ],
            get_table_category_block_final_cats_comb('HistogramsTablesEffs'),
            common_plot.norm_factors,
            squash_errs=True,
            name='EffTableCompFSFinalCutsComb'
            ),
        tools.WebCreator()
        ])


                                                                                                            
                                                                                                            
# LLLLLLLLLLL               iiii                            iiii           tttt                           
# L:::::::::L              i::::i                          i::::i       ttt:::t                           
# L:::::::::L               iiii                            iiii        t:::::t                           
# LL:::::::LL                                                           t:::::t                           
#   L:::::L               iiiiiii    mmmmmmm    mmmmmmm   iiiiiii ttttttt:::::ttttttt        ssssssssss   
#   L:::::L               i:::::i  mm:::::::m  m:::::::mm i:::::i t:::::::::::::::::t      ss::::::::::s  
#   L:::::L                i::::i m::::::::::mm::::::::::m i::::i t:::::::::::::::::t    ss:::::::::::::s 
#   L:::::L                i::::i m::::::::::::::::::::::m i::::i tttttt:::::::tttttt    s::::::ssss:::::s
#   L:::::L                i::::i m:::::mmm::::::mmm:::::m i::::i       t:::::t           s:::::s  ssssss 
#   L:::::L                i::::i m::::m   m::::m   m::::m i::::i       t:::::t             s::::::s      
#   L:::::L                i::::i m::::m   m::::m   m::::m i::::i       t:::::t                s::::::s   
#   L:::::L         LLLLLL i::::i m::::m   m::::m   m::::m i::::i       t:::::t    ttttttssssss   s:::::s 
# LL:::::::LLLLLLLLL:::::Li::::::im::::m   m::::m   m::::mi::::::i      t::::::tttt:::::ts:::::ssss::::::s
# L::::::::::::::::::::::Li::::::im::::m   m::::m   m::::mi::::::i      tt::::::::::::::ts::::::::::::::s 
# L::::::::::::::::::::::Li::::::im::::m   m::::m   m::::mi::::::i        tt:::::::::::tt s:::::::::::ss  
# LLLLLLLLLLLLLLLLLLLLLLLLiiiiiiiimmmmmm   mmmmmm   mmmmmmiiiiiiii          ttttttttttt    sssssssssss    


from limit_thesis import *                                                                                                          
                                                                                                            




                                                                   
                                                                   
# TTTTTTTTTTTTTTTTTTTTTTT                                        
# T:::::::::::::::::::::T                                        
# T:::::::::::::::::::::T                                        
# T:::::TT:::::::TT:::::T                                        
# TTTTTT  T:::::T  TTTTTT    eeeeeeeeeeee    xxxxxxx      xxxxxxx
#         T:::::T          ee::::::::::::ee   x:::::x    x:::::x 
#         T:::::T         e::::::eeeee:::::ee  x:::::x  x:::::x  
#         T:::::T        e::::::e     e:::::e   x:::::xx:::::x   
#         T:::::T        e:::::::eeeee::::::e    x::::::::::x    
#         T:::::T        e:::::::::::::::::e      x::::::::x     
#         T:::::T        e::::::eeeeeeeeeee       x::::::::x     
#         T:::::T        e:::::::e               x::::::::::x    
#       TT:::::::TT      e::::::::e             x:::::xx:::::x   
#       T:::::::::T       e::::::::eeeeeeee    x:::::x  x:::::x  
#       T:::::::::T        ee:::::::::::::e   x:::::x    x:::::x 
#       TTTTTTTTTTT          eeeeeeeeeeeeee  xxxxxxx      xxxxxxx
                                                                   
                                                                   
                                                                   
                                                                   
                                                                   
                                                                   
                                                                   


def mk_tc_tex(source_dir):
    tc_tex = [
        tex_content.mk_plot_ind(
            (
                ('pt_1b', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/noboost_mass_1b[0].m_pt_lin.pdf'),
                ('pt_2b', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/noboost_mass_2b[0].m_pt_lin.pdf'),
                ('mass_2b', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/nomass_boost_2b_mass_softdrop_lin.pdf'),
                ('mass_1b', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/nomass_boost_1b_mass_softdrop_lin.pdf'),
                ('nsjbtags', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDat/StackedAll/BaseLineSelection/nobtag_boost_mass_nsjbtags_rebin_flex_log.pdf'),
            ), name='HiggsPlotsNoDat'
        ),
        tex_content.mk_plot_ind(
            (
                ('pt_1b', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDatNorm/StackedAll/BaseLineSelection/noboost_mass_1b[0].m_pt_lin.pdf'),
                ('pt_2b', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDatNorm/StackedAll/BaseLineSelection/noboost_mass_2b[0].m_pt_lin.pdf'),
                ('mass_2b', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDatNorm/StackedAll/BaseLineSelection/nomass_boost_2b_mass_softdrop_lin.pdf'),
                ('mass_1b', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDatNorm/StackedAll/BaseLineSelection/nomass_boost_1b_mass_softdrop_lin.pdf'),
                ('nsjbtags', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsHiggsCompNoSysNoDatNorm/StackedAll/BaseLineSelection/nobtag_boost_mass_nsjbtags_lin.pdf'),
            ), name='HiggsPlotsNoDatNorm'
        ),
        tex_content.mk_plot_ind(
            (
                ('ST', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefitNoSysNoDat/StackedAll/BaseLineSelection/ST_lin.pdf'),
                ('ST_0h', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefitNoSysNoDatNoScale/StackedAll/SidebandRegion/ST_rebin_flex_log.pdf'),
                ('ST_h1b', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefitNoSysNoDatNoScale/StackedAll/SignalRegion1b/ST_rebin_flex_log.pdf'),
                ('ST_h2b', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefitNoSysNoDatNoScale/StackedAll/SignalRegion2b/ST_rebin_flex_log.pdf'),
                # ('HT', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefitNoSysNoDat/StackedAll/BaseLineSelection/HT_lin.pdf'),
                ('n_ak4', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefitNoSysNoDat/StackedAll/BaseLineSelection/n_ak4_lin.pdf'),
                ('n_ak8', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefitNoSysNoDat/StackedAll/BaseLineSelection/n_ak8_lin.pdf'),
                # ('nomass_boost_1b_mass_softdrop', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefitNoSysNoDat/StackedAll/BaseLineSelection/nomass_boost_1b_mass_softdrop_lin.pdf'),
                # ('nomass_boost_2b_mass_softdrop', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefitNoSysNoDat/StackedAll/BaseLineSelection/nomass_boost_2b_mass_softdrop_lin.pdf'),
                # ('noboost_mass_1b_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefitNoSysNoDat/StackedAll/BaseLineSelection/noboost_mass_1b[0].m_pt_lin.pdf'),
                # ('noboost_mass_2b_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefitNoSysNoDat/StackedAll/BaseLineSelection/noboost_mass_2b[0].m_pt_lin.pdf'),
                # ('nobtag_boost_mass_nsjbtags', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefitNoSysNoDat/StackedAll/BaseLineSelection/nobtag_boost_mass_nsjbtags_lin.pdf'),
                ('primary_lepton_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefitNoSysNoDat/StackedAll/BaseLineSelection/primary_lepton_pt_lin.pdf'),
                ('pt_ld_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefitNoSysNoDat/StackedAll/BaseLineSelection/pt_ld_ak4_jet_lin.pdf'),
                ('pt_subld_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefitNoSysNoDat/StackedAll/BaseLineSelection/pt_subld_ak4_jet_lin.pdf'),
                ('topjets_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefitNoSysNoDat/StackedAll/BaseLineSelection/topjets[0].m_pt_lin.pdf'),
                ('topjets_1_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefitNoSysNoDat/StackedAll/BaseLineSelection/topjets[1].m_pt_lin.pdf'),
                ('met', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefitNoSysNoDat/StackedAll/BaseLineSelection/met_lin.pdf'),
                # ('jets_incl_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefitNoSysNoDat/StackedAll/BaseLineSelection/jets[].m_pt_lin.pdf'),
                ('n_additional_btags_medium', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefitNoSysNoDat/StackedAll/BaseLineSelection/n_additional_btags_medium_log.pdf'),
                ('n_higgs_tags_1b_med', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefitNoSysNoDat/StackedAll/BaseLineSelection/n_higgs_tags_1b_med_log.pdf'),
                ('n_higgs_tags_2b_med', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefitNoSysNoDat/StackedAll/BaseLineSelection/n_higgs_tags_2b_med_log.pdf'),
                # ('n_prim_vertices', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefitNoSysNoDat/StackedAll/BaseLineSelection/n_prim_vertices_lin.pdf'),
            ), name='PreselectionPlotsNoDat'
        ),
        tex_content.mk_plot_ind(
            (
                ('sb_tt_ST', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/ST_rebin_flex_log.pdf'),
                ('sb_tt_HT', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/HT_rebin_flex_log.pdf'),
                ('sb_tt_n_ak4', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/n_ak4_lin.pdf'),
                ('sb_tt_n_ak8', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/n_ak8_lin.pdf'),
                ('sb_tt_nomass_boost_1b_mass_softdrop', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/nomass_boost_1b_mass_softdrop_lin.pdf'),
                ('sb_tt_nomass_boost_2b_mass_softdrop', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/nomass_boost_2b_mass_softdrop_lin.pdf'),
                ('sb_tt_noboost_mass_1b_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/noboost_mass_1b[0].m_pt_lin.pdf'),
                ('sb_tt_noboost_mass_2b_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/noboost_mass_2b[0].m_pt_lin.pdf'),
                ('sb_tt_nobtag_boost_mass_nsjbtags', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/nobtag_boost_mass_nsjbtags_lin.pdf'),
                ('sb_tt_primary_lepton_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/primary_lepton_pt_lin.pdf'),
                ('sb_tt_pt_ld_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/pt_ld_ak4_jet_lin.pdf'),
                ('sb_tt_pt_subld_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/pt_subld_ak4_jet_lin.pdf'),
                ('sb_tt_pt_third_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/jets[2].m_pt_lin.pdf'),
                ('sb_tt_pt_fourth_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/jets[3].m_pt_lin.pdf'),
                ('sb_tt_topjets_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/topjets[0].m_pt_lin.pdf'),
                ('sb_tt_topjets_1_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/topjets[1].m_pt_lin.pdf'),
                ('sb_tt_met', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/met_lin.pdf'),
                ('sb_tt_jets_incl_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/jets[].m_pt_lin.pdf'),
                ('sb_tt_n_additional_btags_medium', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/n_additional_btags_medium_log.pdf'),
                ('sb_tt_n_higgs_tags_1b_med', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/n_higgs_tags_1b_med_log.pdf'),
                ('sb_tt_n_higgs_tags_2b_med', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/n_higgs_tags_2b_med_log.pdf'),
                ('sb_tt_n_prim_vertices', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/n_prim_vertices_lin.pdf'),
                ('sb_wjets_ST', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/ST_rebin_flex_log.pdf'),
                ('sb_wjets_HT', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/HT_rebin_flex_log.pdf'),
                ('sb_wjets_n_ak4', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/n_ak4_lin.pdf'),
                ('sb_wjets_n_ak8', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/n_ak8_lin.pdf'),
                ('sb_wjets_nomass_boost_1b_mass_softdrop', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/nomass_boost_1b_mass_softdrop_lin.pdf'),
                ('sb_wjets_nomass_boost_2b_mass_softdrop', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/nomass_boost_2b_mass_softdrop_lin.pdf'),
                ('sb_wjets_noboost_mass_1b_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/noboost_mass_1b[0].m_pt_lin.pdf'),
                ('sb_wjets_noboost_mass_2b_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/noboost_mass_2b[0].m_pt_lin.pdf'),
                ('sb_wjets_nobtag_boost_mass_nsjbtags', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/nobtag_boost_mass_nsjbtags_lin.pdf'),
                ('sb_wjets_primary_lepton_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/primary_lepton_pt_lin.pdf'),
                ('sb_wjets_pt_ld_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/pt_ld_ak4_jet_lin.pdf'),
                ('sb_wjets_pt_subld_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/pt_subld_ak4_jet_lin.pdf'),
                ('sb_wjets_pt_third_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/jets[2].m_pt_lin.pdf'),
                ('sb_wjets_pt_fourth_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/jets[3].m_pt_lin.pdf'),
                ('sb_wjets_topjets_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/topjets[0].m_pt_lin.pdf'),
                ('sb_wjets_topjets_1_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/topjets[1].m_pt_lin.pdf'),
                ('sb_wjets_met', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/met_lin.pdf'),
                ('sb_wjets_jets_incl_pt', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/jets[].m_pt_lin.pdf'),
                ('sb_wjets_n_additional_btags_medium', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/n_additional_btags_medium_log.pdf'),
                ('sb_wjets_n_higgs_tags_1b_med', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/n_higgs_tags_1b_med_log.pdf'),
                ('sb_wjets_n_higgs_tags_2b_med', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/n_higgs_tags_2b_med_log.pdf'),
                ('sb_wjets_n_prim_vertices', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/n_prim_vertices_lin.pdf'),
            ), name='SidebandPlotsSyst'
        ),
        tex_content.mk_plot_ind(
            (
                ('sb_ttbar_all', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsNormToIntAll/StackedAll/SidebandTTJetsRegion/ST_rebin_flex_log.pdf'),
                ('sb_ttbar_exp', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsNormToIntExpSyst/StackedAll/SidebandTTJetsRegion/ST_rebin_flex_log.pdf'),
                ('sb_ttbar_theo', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsNormToIntThSyst/StackedAll/SidebandTTJetsRegion/ST_rebin_flex_log.pdf'),
                ('sb_wjets_all', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsNormToIntAll/StackedAll/SidebandWPlusJetsRegion/ST_rebin_flex_log.pdf'),
                ('sb_wjets_exp', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsNormToIntExpSyst/StackedAll/SidebandWPlusJetsRegion/ST_rebin_flex_log.pdf'),
                ('sb_wjets_theo', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsNormToIntThSyst/StackedAll/SidebandWPlusJetsRegion/ST_rebin_flex_log.pdf'),
            ), name='NormPlotsSideband'
        ),
        tex_content.mk_plot_ind(
            (
                ('top_pt_reweight_sb', os.path.join(base_path, source_dir)+'/TopPtCompPlots/TopPtNew/Histograms/StackedAll/SidebandTTJetsRegion/ST_rebin_flex_log.pdf'),
                ('top_pt_reweight_norm', os.path.join(base_path, source_dir)+'/TopPtCompPlots/TopPtNew/HistogramsNormToIntAll/StackedAll/SidebandTTJetsRegion/ST_rebin_flex_log.pdf'),
                ('top_pt_reweight_comp_unc', os.path.join(base_path, source_dir)+'/TopPtCompPlots/TopPtNew/HistogramsCompUncerts/StackedAll/SidebandTTJetsRegion/ST_rebin_flex__TTbar__top_pt_reweight_log.pdf'),
            ), name='TopPtPlots'
        ),
        tex_content.mk_plot_ind(
            (
                ('lin_func_ttbar', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefitNoSysFit/StackedAll/SidebandTTJetsRegion/HT_rebin_flex_log.pdf'),
                ('lin_func_wjets', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsPrefitNoSysFit/StackedAll/SidebandWPlusJetsRegion/HT_rebin_flex_log.pdf'),
            ), name='FitPlots'
        ),
        tex_content.mk_plot_ind(
            (
                ('sb_tt_ST', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/ST_rebin_flex_log.pdf'),
                ('sb_tt_HT', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/HT_rebin_flex_log.pdf'),
                ('sb_tt_n_ak4', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/n_ak4_lin.pdf'),
                ('sb_tt_n_ak8', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/n_ak8_lin.pdf'),
                ('sb_tt_nomass_boost_1b_mass_softdrop', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/nomass_boost_1b_mass_softdrop_lin.pdf'),
                ('sb_tt_nomass_boost_2b_mass_softdrop', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/nomass_boost_2b_mass_softdrop_lin.pdf'),
                ('sb_tt_noboost_mass_1b_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/noboost_mass_1b[0].m_pt_lin.pdf'),
                ('sb_tt_noboost_mass_2b_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/noboost_mass_2b[0].m_pt_lin.pdf'),
                ('sb_tt_nobtag_boost_mass_nsjbtags', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/nobtag_boost_mass_nsjbtags_lin.pdf'),
                ('sb_tt_primary_lepton_pt', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/primary_lepton_pt_lin.pdf'),
                ('sb_tt_pt_ld_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/pt_ld_ak4_jet_lin.pdf'),
                ('sb_tt_pt_subld_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/pt_subld_ak4_jet_lin.pdf'),
                ('sb_tt_pt_third_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/jets[2].m_pt_lin.pdf'),
                ('sb_tt_pt_fourth_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/jets[3].m_pt_lin.pdf'),
                ('sb_tt_topjets_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/topjets[0].m_pt_lin.pdf'),
                ('sb_tt_topjets_1_pt', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/topjets[1].m_pt_lin.pdf'),
                ('sb_tt_met', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/met_lin.pdf'),
                ('sb_tt_jets_incl_pt', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/jets[].m_pt_lin.pdf'),
                ('sb_tt_n_additional_btags_medium', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/n_additional_btags_medium_log.pdf'),
                ('sb_tt_n_higgs_tags_1b_med', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/n_higgs_tags_1b_med_log.pdf'),
                ('sb_tt_n_higgs_tags_2b_med', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/n_higgs_tags_2b_med_log.pdf'),
                ('sb_tt_n_prim_vertices', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandTTJetsRegion/n_prim_vertices_lin.pdf'),
                ('sb_wjets_ST', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/ST_rebin_flex_log.pdf'),
                ('sb_wjets_HT', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/HT_rebin_flex_log.pdf'),
                ('sb_wjets_n_ak4', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/n_ak4_lin.pdf'),
                ('sb_wjets_n_ak8', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/n_ak8_lin.pdf'),
                ('sb_wjets_nomass_boost_1b_mass_softdrop', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/nomass_boost_1b_mass_softdrop_lin.pdf'),
                ('sb_wjets_nomass_boost_2b_mass_softdrop', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/nomass_boost_2b_mass_softdrop_lin.pdf'),
                ('sb_wjets_noboost_mass_1b_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/noboost_mass_1b[0].m_pt_lin.pdf'),
                ('sb_wjets_noboost_mass_2b_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/noboost_mass_2b[0].m_pt_lin.pdf'),
                ('sb_wjets_nobtag_boost_mass_nsjbtags', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/nobtag_boost_mass_nsjbtags_lin.pdf'),
                ('sb_wjets_primary_lepton_pt', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/primary_lepton_pt_lin.pdf'),
                ('sb_wjets_pt_ld_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/pt_ld_ak4_jet_lin.pdf'),
                ('sb_wjets_pt_subld_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/pt_subld_ak4_jet_lin.pdf'),
                ('sb_wjets_pt_third_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/jets[2].m_pt_lin.pdf'),
                ('sb_wjets_pt_fourth_ak4_jet', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/jets[3].m_pt_lin.pdf'),
                ('sb_wjets_topjets_0_pt', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/topjets[0].m_pt_lin.pdf'),
                ('sb_wjets_topjets_1_pt', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/topjets[1].m_pt_lin.pdf'),
                ('sb_wjets_met', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/met_lin.pdf'),
                ('sb_wjets_jets_incl_pt', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/jets[].m_pt_lin.pdf'),
                ('sb_wjets_n_additional_btags_medium', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/n_additional_btags_medium_log.pdf'),
                ('sb_wjets_n_higgs_tags_1b_med', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/n_higgs_tags_1b_med_log.pdf'),
                ('sb_wjets_n_higgs_tags_2b_med', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/n_higgs_tags_2b_med_log.pdf'),
                ('sb_wjets_n_prim_vertices', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandWPlusJetsRegion/n_prim_vertices_lin.pdf'),
            ), name='SidebandPlotsSystWithRew'
        ),
        tex_content.mk_plot_ind(
            (
                ('comp_htrew_theo_uncerts_ttbar', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsCompScaleVarHTRew/StackedAll/BaseLineSelection/ST_rebin_flex__TTbar__comp_th_log.pdf'),
                ('comp_htrew_theo_uncerts_wjets', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsCompScaleVarHTRew/StackedAll/BaseLineSelection/ST_rebin_flex__WJets__comp_th_log.pdf'),
                ('comp_norew_jec_ttbar', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TTbar__jec_log.pdf'),
                ('comp_norew_jec_wjets', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__WJets__jec_log.pdf'),
                ('comp_norew_jec_tptp1200', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TpTp_M-1200_thth__jec_log.pdf'),
                ('comp_norew_jer_ttbar', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TTbar__jer_log.pdf'),
                ('comp_norew_jer_wjets', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__WJets__jer_log.pdf'),
                ('comp_norew_jer_tptp1200', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TpTp_M-1200_thth__jer_log.pdf'),
                ('comp_norew_btag_bc_ttbar', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TTbar__btag_bc_log.pdf'),
                ('comp_norew_btag_bc_wjets', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__WJets__btag_bc_log.pdf'),
                ('comp_norew_btag_bc_tptp1200', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TpTp_M-1200_thth__btag_bc_log.pdf'),
                ('comp_norew_btag_udsg_ttbar', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TTbar__btag_udsg_log.pdf'),
                ('comp_norew_btag_udsg_wjets', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__WJets__btag_udsg_log.pdf'),
                ('comp_norew_btag_udsg_tptp1200', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TpTp_M-1200_thth__btag_udsg_log.pdf'),
                ('comp_norew_scalevar_ttbar', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TTbar__ScaleVar_log.pdf'),
                ('comp_norew_scalevar_wjets', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__WJets__ScaleVar_log.pdf'),
                ('comp_norew_scalevar_tptp1200', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TpTp_M-1200_thth__ScaleVar_log.pdf'),
                ('comp_norew_pdf_ttbar', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TTbar__PDF_log.pdf'),
                ('comp_norew_pdf_wjets', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__WJets__PDF_log.pdf'),
                ('comp_norew_pdf_tptp1200', os.path.join(base_path, source_dir)+'/PreFitPlotsNoRew/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TpTp_M-1200_thth__PDF_log.pdf'),
                ('comp_htrew_htrew_ttbar', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TTbar__jsf_log.pdf'),
                ('comp_htrew_htrew_wjets', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__WJets__jsf_log.pdf'),
                # ('comp_norew_htrew_tptp1200', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TpTp_M-1200_thth__jsf_log.pdf'),
                ('comp_htrew_pu_ttbar', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TTbar__pu_log.pdf'),
                ('comp_htrew_pu_wjets', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__WJets__pu_log.pdf'),
                ('comp_htrew_pu_tptp1200', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TpTp_M-1200_thth__pu_log.pdf'),
                ('comp_htrew_jms_ttbar', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TTbar__higgs_scale_log.pdf'),
                ('comp_htrew_jms_wjets', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__WJets__higgs_scale_log.pdf'),
                ('comp_htrew_jms_tptp1200', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TpTp_M-1200_thth__higgs_scale_log.pdf'),
                ('comp_htrew_jmr_ttbar', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TTbar__higgs_smear_log.pdf'),
                ('comp_htrew_jmr_wjets', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__WJets__higgs_smear_log.pdf'),
                ('comp_htrew_jmr_tptp1200', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsCompUncerts/StackedAll/SignalRegion2b/ST_rebin_flex__TpTp_M-1200_thth__higgs_smear_log.pdf'),
                ('comp_htrew_mutrg_ttbar', os.path.join(base_path, source_dir)+'/SplitLepCompSyst/HistogramsCompUncerts/StackedAll/SignalRegion2b_Mu45/ST_rebin_flex__TTbar__sfmu_trg_log.pdf'),
                ('comp_htrew_mutrg_wjets', os.path.join(base_path, source_dir)+'/SplitLepCompSyst/HistogramsCompUncerts/StackedAll/SignalRegion2b_Mu45/ST_rebin_flex__WJets__sfmu_trg_log.pdf'),
                ('comp_htrew_mutrg_tptp1200', os.path.join(base_path, source_dir)+'/SplitLepCompSyst/HistogramsCompUncerts/StackedAll/SignalRegion2b_Mu45/ST_rebin_flex__TpTp_M-1200_thth__sfmu_trg_log.pdf'),
                ('comp_htrew_muid_ttbar', os.path.join(base_path, source_dir)+'/SplitLepCompSyst/HistogramsCompUncerts/StackedAll/SignalRegion2b_Mu45/ST_rebin_flex__TTbar__sfmu_id_log.pdf'),
                ('comp_htrew_muid_wjets', os.path.join(base_path, source_dir)+'/SplitLepCompSyst/HistogramsCompUncerts/StackedAll/SignalRegion2b_Mu45/ST_rebin_flex__WJets__sfmu_id_log.pdf'),
                ('comp_htrew_muid_tptp1200', os.path.join(base_path, source_dir)+'/SplitLepCompSyst/HistogramsCompUncerts/StackedAll/SignalRegion2b_Mu45/ST_rebin_flex__TpTp_M-1200_thth__sfmu_id_log.pdf'),
                ('comp_htrew_elid_ttbar', os.path.join(base_path, source_dir)+'/SplitLepCompSyst/HistogramsCompUncerts/StackedAll/SignalRegion2b_El45/ST_rebin_flex__TTbar__sfel_id_log.pdf'),
                ('comp_htrew_elid_wjets', os.path.join(base_path, source_dir)+'/SplitLepCompSyst/HistogramsCompUncerts/StackedAll/SignalRegion2b_El45/ST_rebin_flex__WJets__sfel_id_log.pdf'),
                ('comp_htrew_elid_tptp1200', os.path.join(base_path, source_dir)+'/SplitLepCompSyst/HistogramsCompUncerts/StackedAll/SignalRegion2b_El45/ST_rebin_flex__TpTp_M-1200_thth__sfel_id_log.pdf'),
            ), name='CompSystUncerts'
        ),


        tex_content.mk_plot_ind(
            (
                ('bkg_only_check_norew_postfit', os.path.join(base_path, source_dir)+'/BkgStudies/BkgOnlyNoReweighting/PostFit/cnv_post_fit_.pdf'),
                ('bkg_only_check_htrew_postfit', os.path.join(base_path, source_dir)+'/BkgStudies/BkgOnlyHTReweighting/PostFit/cnv_post_fit_.pdf'),
                ('bkg_only_check_norew_corr_mat', os.path.join(base_path, source_dir)+'/BkgStudies/BkgOnlyNoReweighting/CorrelationPlot/correlation_matrix_d42c0f_lin.pdf'),
                ('bkg_only_check_htrew_corr_mat', os.path.join(base_path, source_dir)+'/BkgStudies/BkgOnlyHTReweighting/CorrelationPlot/correlation_matrix_d42c0f_lin.pdf'),
            ), name='CompBkgModels'
        ),
        tex_content.mk_plot_ind(
            (
                ('norm_eval_postfit', os.path.join(base_path, source_dir)+'/BkgStudies/NormEvalHTReweighting/PostFit/cnv_post_fit_.pdf'),
                ('sb_tt_ST', os.path.join(base_path, source_dir)+'/PostFitPlots/Histograms/StackedAll/SidebandTTJetsRegion/ST_rebin_flex_log.pdf'),
                ('sb_wjets_ST', os.path.join(base_path, source_dir)+'/PostFitPlots/Histograms/StackedAll/SidebandWPlusJetsRegion/ST_rebin_flex_log.pdf'),
                ('0h_ST', os.path.join(base_path, source_dir)+'/PostFitPlots/Histograms/StackedAll/SidebandRegion/ST_rebin_flex_log.pdf'),
                ('h1b_ST', os.path.join(base_path, source_dir)+'/PostFitPlots/Histograms/StackedAll/SignalRegion1b/ST_rebin_flex_log.pdf'),
                ('h2b_ST', os.path.join(base_path, source_dir)+'/PostFitPlots/Histograms/StackedAll/SignalRegion2b/ST_rebin_flex_log.pdf'),
                ('0h_ST_pull', os.path.join(base_path, source_dir)+'/PostFitPlots/HistogramsPulls/StackedAll/SidebandRegion/ST_rebin_flex_log.pdf'),
                ('h1b_ST_pull', os.path.join(base_path, source_dir)+'/PostFitPlots/HistogramsPulls/StackedAll/SignalRegion1b/ST_rebin_flex_log.pdf'),
                ('h2b_ST_pull', os.path.join(base_path, source_dir)+'/PostFitPlots/HistogramsPulls/StackedAll/SignalRegion2b/ST_rebin_flex_log.pdf'),
            ), name='PostFitPlots'
        ),
        tex_content.mk_plot_ind(
            (
                # ('sb_tt_ST', os.path.join(base_path, source_dir)+'/PostFitPlots/Histograms/StackedAll/SidebandTTJetsRegion/ST_rebin_flex_log.pdf'),
                # ('sb_wjets_ST', os.path.join(base_path, source_dir)+'/PostFitPlots/Histograms/StackedAll/SidebandWPlusJetsRegion/ST_rebin_flex_log.pdf'),
                ('pt_1b', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/BaseLineSelection/noboost_mass_1b[0].m_pt_lin.pdf'),
                ('pt_2b', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/BaseLineSelection/noboost_mass_2b[0].m_pt_lin.pdf'),
                ('mass_2b', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/BaseLineSelection/nomass_boost_2b_mass_softdrop_lin.pdf'),
                ('mass_1b', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/BaseLineSelection/nomass_boost_1b_mass_softdrop_lin.pdf'),
                ('nsjbtags', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/BaseLineSelection/nobtag_boost_mass_nsjbtags_lin.pdf'),
                ('0h_ST', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SidebandRegion/ST_rebin_flex_log.pdf'),
                ('h1b_ST', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SignalRegion1b/ST_rebin_flex_log.pdf'),
                ('h2b_ST', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefit/StackedAll/SignalRegion2b/ST_rebin_flex_log.pdf'),
                ('sb_tt_ST_pull', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefitPulls/StackedAll/SidebandTTJetsRegion/ST_rebin_flex_log.pdf'),
                ('sb_wjets_ST_pull', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefitPulls/StackedAll/SidebandWPlusJetsRegion/ST_rebin_flex_log.pdf'),
                ('0h_ST_pull', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefitPulls/StackedAll/SidebandRegion/ST_rebin_flex_log.pdf'),
                ('h1b_ST_pull', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefitPulls/StackedAll/SignalRegion1b/ST_rebin_flex_log.pdf'),
                ('h2b_ST_pull', os.path.join(base_path, source_dir)+'/PreFitPlots/HistogramsPrefitPulls/StackedAll/SignalRegion2b/ST_rebin_flex_log.pdf'),
            ), name='PreFitPlots'
        ),
        tex_content.mk_plot_ind(
            (
                ('lim_tt_tH100', os.path.join(base_path, source_dir)+'/FinalLimitsTT_2/IndLimits/Limit_bW0p0_tZ0p0_tH1p0/LimitCurvesCompared/lim_graph_log.pdf'),
                ('lim_tt_singlet', os.path.join(base_path, source_dir)+'/FinalLimitsTT_2/IndLimits/Limit_bW0p5_tZ0p25_tH0p25/LimitCurvesCompared/lim_graph_log.pdf'),
                ('lim_tt_doublet', os.path.join(base_path, source_dir)+'/FinalLimitsTT_2/IndLimits/Limit_bW0p0_tZ0p5_tH0p5/LimitCurvesCompared/lim_graph_log.pdf'),
                # ('lim_bb_tH100', os.path.join(base_path, source_dir)+'/FinalLimitsTT_2/IndLimits/Limit_tW0p0_bZ0p0_bH1p0/LimitCurvesCompared/lim_graph_log.pdf'),
                ('lim_bb_singlet', os.path.join(base_path, source_dir)+'/FinalLimitsBB/IndLimits/Limit_tW0p5_bZ0p25_bH0p25/LimitCurvesCompared/lim_graph_log.pdf'),
                ('lim_bb_doublet', os.path.join(base_path, source_dir)+'/FinalLimitsBB/IndLimits/Limit_tW0p0_bZ0p5_bH0p5/LimitCurvesCompared/lim_graph_log.pdf'),
                ('lim_tt_triangle_exp', os.path.join(base_path, source_dir)+'/FinalLimitsTT_2/LimitTriangle/PlotterBoxExp/lim_exp_lin.pdf'),
                ('lim_tt_triangle_obs', os.path.join(base_path, source_dir)+'/FinalLimitsTT_2/LimitTriangle/PlotterBoxObs/lim_obs_lin.pdf'),
                ('lim_bb_triangle_exp', os.path.join(base_path, source_dir)+'/FinalLimitsBB/LimitTriangle/PlotterBoxExp/lim_exp_lin.pdf'),
                ('lim_bb_triangle_obs', os.path.join(base_path, source_dir)+'/FinalLimitsBB/LimitTriangle/PlotterBoxObs/lim_obs_lin.pdf'),
            ), name='FinalLimits'
        ),
        tex_content.mk_autoContentSysTabs(os.path.join(base_path, source_dir, 'FinalLimitsTT_2/IndLimits/Limit_bW0p0_tZ0p0_tH1p0/ThetaLimits/{0}'), 'SysTabs', mass_points=['TpTp_M-0800', 'TpTp_M-1200', 'TpTp_M-1600'], regions=final_regions),
        tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/Tables/EffTableCompFSAll/count_table_content.tex', name='EffTableCompFSAll'),
        tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/Tables/EffTableCompFSFinalCuts/count_table_content.tex', name='EffTableCompFSFinalCuts'),
        tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/Tables/EffTableCompFSFinalCutsComb/count_table_content.tex', name='EffTableCompFSFinalCutsComb'),
        # tex_content.mk_autoTable(path_an+'/MergeChannelsTablesNoTheory/CountTablePAS/count_table_content.tex', name='CountTable'),
        tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/Tables/CountTablePostFit/count_table_content.tex', name='CountTablePostFit'),
        tex_content.mk_autoTable(os.path.join(base_path, source_dir)+'/Tables/CountTablePreFit/count_table_content.tex', name='CountTablePreFit'),
    ]
    tc_tex = tools.ToolChain('CopyPlots', [
        tools.ToolChain('TexThesis', tc_tex),
        tools.CopyTool('/afs/desy.de/user/n/nowatsd/Documents/figures_thesis/', src='../TexThesis/*', ignore=('*.svn', '*.html', '*.log'), use_rsync=True, options='-qa --delete'),
        ])
    return tc_tex

# sframe_tools = mk_sframe_and_plot_tools()

import sys

if __name__ == '__main__':
    time.sleep(1)
    # src_dir = sys.argv[1]
    final_dir = sys.argv[1]
    all_tools = tools.ToolChainParallel(final_dir,
        [
            # plot_merged_channels_prefit_norew('PreFitPlotsNoRew'),
            # plot_merged_channels_prefit_top_pt('TopPtCompPlots'),
            # # plot_merged_channels_higgs('HiggsPlots'),
            # plot_merged_channels_postfit('PostFitPlots'),
            # plot_merged_channels_prefit('PreFitPlots'),
            # plot_comp_hists_split_channel('SplitLepCompSyst'),
            # plot_merged_channels_tables('Tables'),
            # mk_tc_comp_bkg_mdl('BkgStudies'),
            mk_tc_all_limits('FinalLimitsTT_2'),
            # mk_tc_all_limits_bb('FinalLimitsBB'),
            mk_tc_tex(final_dir),
            tools.WebCreator()
            # combination_limits.mk_limit_list('Limits')
        ], n_workers=1)
    tools.Runner(all_tools, default_reuse=True)
    # tools.CopyTool('~/www/vlq_analysis/tight_selection2/',
    #     src=final_dir, use_rsync=True).run()