#!/usr/bin/env python

##################################### definition of UserConfig item changes ###


start_all_parallel = True


############################################################### script code ###
import varial
import sys
import os
import copy
import analysis

from varial.extensions import git
from ROOT import TLatex

from varial.extensions.sframe import SFrame
from varial import tools
if start_all_parallel:
    ToolChain = tools.ToolChainParallel
else:
    ToolChain = tools.ToolChain

import common_plot_new as common_plot
import plot_new as plot
from optparse import OptionParser
import tex_content_new as tex_content
from varial.extensions.hadd import Hadd
import varial.generators as gen
import varial.rendering as rnd
import UHH2.VLQSemiLepPreSel.cutflow_tables as cutflow_tables

varial.settings.max_num_processes = 12

basenames_pre = list('uhh2.AnalysisModuleRunner.'+f for f in [
    'DATA.SingleMuon_Run2015CD',
    'DATA.SingleEle_Run2015CD',
    'MC.QCD',
    'MC.WJets',
    'MC.DYJetsToLL',
    'MC.Diboson',
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

sig_scalefactors = {
    'TpTp_M-0700' : 100.,
    'TpTp_M-0800' : 100.,
    'TpTp_M-0900' : 100.,
    'TpTp_M-1000' : 100.,
    'TpTp_M-1100' : 1000.,
    'TpTp_M-1200' : 1000.,
    'TpTp_M-1300' : 1000.,
    'TpTp_M-1400' : 1000.,
    'TpTp_M-1500' : 10000.,
    'TpTp_M-1600' : 10000.,
    'TpTp_M-1700' : 10000.,
    'TpTp_M-1800' : 10000.,
}

sig_scalefactors_log = {
    'TpTp_M-0800' : 10.,
    'TpTp_M-1200' : 100.,
}

categories_pre = [ #"NoSelection",
        # 'IsoMuo20',
        # 'IsoEle27',
        'Mu45',
        'El45',
        # 'El105',
        # 'isoMuo20',
        # 'isoEle27',
        # 'mu45',
        # 'mu45cut55',
        # 'el105',
        # 'el45',
        # 'el45cut55',
        # 'isoEle27nonIsoMu',
        # 'isoMuo20cut25',
        # 'isoEle27cut30',
        # 'El45mva',
        ]


no_sys_uncerts = {
    'nominal'       : {'jecsmear_direction':'nominal'}
}

all_sys_uncerts = {
    # 'name' : {'item name': 'item value', ...},
    'jec_up'        : {'jecsmear_direction':'up'},
    'jec_down'      : {'jecsmear_direction':'down'},
    'jer_up'        : {'jersmear_direction':'up'},
    'jer_down'      : {'jersmear_direction':'down'},
    'nominal'       : {'jecsmear_direction':'nominal'}
    # 'jer_jec_up'    : {'jersmear_direction':'up','jecsmear_direction':'up'},
    # 'jer_jec_down'  : {'jersmear_direction':'down','jecsmear_direction':'down'},
}

def mod_2d_leg(entries):
    if len(entries) > 1:
        print 'WARNING More than one legend entry in 2D hist!'
    new_entry = (entries[0][0], entries[0][1], '')
    return [new_entry]

# twoD_cut_2d_dict = {
#     'title' : 'min(#Delta R(l,j))',
#     'y_title' : 'min(p_{T,rel}(l,j))',
#     '_set_leg_1_col_log' : {
#         'x_pos': 0.35,
#         'y_pos': 0.73,
#         'label_width': 0.30,
#         'label_height': 0.045,
#         'box_text_size' : 0.045,
#         'opt': '',
#         # 'opt_data': 'pl',
#         # 'reverse': True,
#         # 'sort_legend' : lambda w: 'TT ' in w[1],
#         # 'mod_legend' : mod_2d_leg
#     },
#     # 'text_box_log' : (0.6, 0.89, "#scale[0.45]{2.5 (e), 2.6 (#mu) fb^{-1} (13 TeV)}"),
# }

# twoD_cut_xy_dict = {
#     'y_max_log_fct' : 100000.,
#     '_set_leg_2_col_log' : {
#         'x_pos': 0.7,
#         'y_pos': 0.73,
#         'label_width': 0.30,
#         'label_height': 0.045,
#         'box_text_size' : 0.035,
#         'opt': 'f',
#         'opt_data': 'pl',
#         'reverse': True,
#         # 'sort_legend' : lambda w: 'TT ' in w[1],
#     },
# }

def set_x_ax_offset(wrp):
    wrp.second_pad.cd()

    wrp.bottom_hist.GetXaxis().SetTitleOffset(1.1)
    wrp.bottom_hist.Draw()
    wrp.main_pad.cd()

# text_box_lin_def = (0.54, 0.89, "#scale[0.45]{2.5 (e), 2.6 (#mu) fb^{-1} (13 TeV)}")


leg_2_col_def = {
    'x_pos': 0.68,
    'y_pos': 0.67,
    'label_width': 0.34,
    'label_height': 0.045,
    'box_text_size' : 0.035,
    'opt': 'f',
    'opt_data': 'pl',
    'reverse': True,
}

# '_set_leg_2_col_log' : {
#     'x_pos': 0.7,
#     'y_pos': 0.73,
#     'label_width': 0.30,
#     'label_height': 0.045,
#     'box_text_size' : 0.035,
#     'opt': 'f',
#     'opt_data': 'pl',
#     'reverse': True,
#     # 'sort_legend' : lambda w: 'TT ' in w[1],
# }

# '_set_leg_2_col_log' : {
#     'x_pos': 0.7,
#     'y_pos': 0.65,
#     'label_width': 0.30,
#     'label_height': 0.045,
#     'box_text_size' : 0.035,
#     'opt': 'f',
#     'opt_data': 'pl',
#     'reverse': True,
#     # 'sort_legend' : lambda w: 'TT ' in w[1],
# },
  
mod_dict = {
    'luminosity' : {
            'rebin' : 50,
            'title' : 'Luminosity bin',
            'y_max_fct' : 1.3,
            '_set_leg_1_col_lin' : {
                'x_pos': 0.75,
                'y_pos': 0.8,
                'label_width': 0.25,
                # 'mod_legend': lambda _: None
            },
            # 'y_max_log_fct' : 1000000.,

            # 'bot_plot_mod' : set_x_ax_offset
            # 'text_box_lin' : text_box_lin_def,
        },
    'N_PrimVertices' : {
            'rebin_list' : list(i - 0.5 for i in xrange(0, 31))
        },
    'N_PrimVertices_rebin_flex' : {
            'title' : 'N(Vertices)',
            'y_max_fct' : 1.2,
            # 'text_box_lin' : text_box_lin_def,
        },
    # 'twod_cut_hist_noIso' : {
    #         'title' : 'min(#Delta R(l,j))',
    #         'y_title' : 'min(p_{T,rel}(l,j))',
    #     },
    'twod_cut_hist_noIso_QCD' : {
            # 'y_max_log_fct' : 100000.,
            'y_min_gr_zero' : 1e-1,
            '_set_leg_2_col_log' : leg_2_col_def,
            'text_box_log' : [(0.19, 0.81, "#scale[0.5]{Multijet}")]
        },
    'twod_cut_hist_noIso_TpTp_M-0800' : {
            # 'y_max_log_fct' : 100000.,
            'y_min_gr_zero' : 1e-1,
            '_set_leg_2_col_log' : leg_2_col_def,
            'text_box_log' : [(0.19, 0.81, "#scale[0.5]{T#bar{T} (0.8 TeV) (#times 10)}")]
        },
    'twod_cut_hist_noIso_TpTp_M-1200' : {
            # 'y_max_log_fct' : 100000.,
            'y_min_gr_zero' : 1e-1,
            '_set_leg_2_col_log' : leg_2_col_def,
            'text_box_log' : [(0.19, 0.81, "#scale[0.5]{T#bar{T} (1.2 TeV) (#times 100)}")]
        },
    # 'twod_cut_hist_noIso_TpTp_M-1600' : dict(list(twoD_cut_2d_dict.items()) + [('text_box_log', [(0.6, 0.89, "#scale[0.45]{2.5 (e), 2.6 (#mu) fb^{-1} (13 TeV)}"), (0.19, 0.81, "#scale[0.5]{T#bar{T} (M_{T}=1.6 TeV)}")])]),
    # 'twod_cut_hist_noIso_QCD' : dict(list(twoD_cut_2d_dict.items()) + [('text_box_log', [(0.6, 0.89, "#scale[0.45]{2.5 (e), 2.6 (#mu) fb^{-1} (13 TeV)}"), (0.19, 0.81, "#scale[0.5]{Multijet}")])]),
    # 'twod_cut_hist_noIso_TpTp_M-0800' : dict(list(twoD_cut_2d_dict.items()) + [('text_box_log', [(0.6, 0.89, "#scale[0.45]{2.5 (e), 2.6 (#mu) fb^{-1} (13 TeV)}"), (0.19, 0.81, "#scale[0.5]{T#bar{T} (M_{T}=0.8 TeV)}")])]),
    # 'twod_cut_hist_noIso_TpTp_M-1200' : dict(list(twoD_cut_2d_dict.items()) + [('text_box_log', [(0.6, 0.89, "#scale[0.45]{2.5 (e), 2.6 (#mu) fb^{-1} (13 TeV)}"), (0.19, 0.81, "#scale[0.5]{T#bar{T} (M_{T}=1.2 TeV)}")])]),
    # 'twod_cut_hist_noIso_TpTp_M-1600' : dict(list(twoD_cut_2d_dict.items()) + [('text_box_log', [(0.6, 0.89, "#scale[0.45]{2.5 (e), 2.6 (#mu) fb^{-1} (13 TeV)}"), (0.19, 0.81, "#scale[0.5]{T#bar{T} (M_{T}=1.6 TeV)}")])]),
    'twod_cut_hist_noIso_px' : {
            # 'title' : 'min(#Delta R(l,j))',
            'y_max_log_fct' : 10000.,
            'y_min_gr_zero' : 100,
            '_set_leg_2_col_log' : leg_2_col_def,
            # 'text_box_log' : text_box_lin_def,
        },
    'twod_cut_hist_noIso_py' : {
            # 'title' : 'min(p_{T,rel}(l,j))',
            'y_max_log_fct' : 100000.,
            'y_min_gr_zero' : 1,
            '_set_leg_2_col_log' : leg_2_col_def,
            # 'text_box_log' : text_box_lin_def,
        },
    'cutflow' : {
            'y_max_log_fct' : 1000000.,
            '_set_leg_2_col_log' : {
                'x_pos': 0.73,
                'y_pos': 0.65,
                'label_width': 0.30,
                'label_height': 0.045,
                'box_text_size' : 0.035,
                'opt': 'f',
                'opt_data': 'pl',
                'reverse': True,
                # 'sort_legend' : lambda w: 'TT ' in w[1],
            },
            # 'bot_plot_mod' : set_x_ax_offset
        },
    'n_ak4' : {
            'y_max_fct' : 1.2,
            # 'text_box_lin' : text_box_lin_def,
            },
    'n_ak8' : {
            'y_max_fct' : 1.2,
            # 'text_box_lin' : text_box_lin_def,
            },
    'primary_muon_pt' : {
            'y_max_fct' : 1.2,
            'rebin' : 30,
            'bin_width' : 40,
            # 'rebin_list' : list(i for i in xrange(0, 624, 48)) + [1200],
            # 'title' : 'S_{T} [GeV]',
            # 'y_max_log_fct' : 10000.,
            # 'y_min_gr_zero' : 1e-3,
            # 'y_max_fct' : 1.2,
            # 'bin_width' : 100,
            # 'err_empty_bins' : True
            # 'text_box_lin' : text_box_lin_def,
            },
    'primary_electron_pt' : {
            'y_max_fct' : 1.2,
            'rebin' : 30,
            'bin_width' : 40,
            # 'rebin_list' : list(i for i in xrange(0, 624, 48)) + [1200],
            # 'title' : 'S_{T} [GeV]',
            # 'y_max_log_fct' : 10000.,
            # 'y_min_gr_zero' : 1e-3,
            # 'y_max_fct' : 1.2,
            # 'bin_width' : 100,
            # 'err_empty_bins' : True
            # 'text_box_lin' : text_box_lin_def,
            },
    ##### GENERAL VARIABLES ######
    'ST' : {
            'rebin' : 33,
            'rebin_list' : [0., 800., 900., 1000., 1200., 1500., 2000., 2500., 3000., 4500., 6500.],
            'title' : 'S_{T} [GeV]',
            'y_max_log_fct' : 10000.,
            'y_min_gr_zero' : 1e-3,
            'bin_width' : 200,
            'y_max_fct' : 1.2,
            # 'bin_width' : 100,
            'err_empty_bins' : True,
            # 'text_box_lin' : text_box_lin_def,
            },
    'ST_rebin_flex' : {
            'title' : 'S_{T} [GeV]',
            'y_max_log_fct' : 100000.,
            'y_min_gr_zero' : 2e-3,
            'bin_width' : 100,
            '_set_leg_2_col_log' : {
                    'x_pos': 0.7,
                    'y_pos': 0.65,
                    'label_width': 0.30,
                    'label_height': 0.045,
                    'box_text_size' : 0.035,
                    'opt': 'f',
                    'opt_data': 'pl',
                    'reverse': True,
                    # 'sort_legend' : lambda w: 'TT ' in w[1],
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
            'title' : 'S_{T} [GeV]',
            'y_max_log_fct' : 10000.,
            'y_min_gr_zero' : 1e-3,
            'y_max_fct' : 1.2,
            # 'bin_width' : 100,
            'err_empty_bins' : True,
            # 'text_box_lin' : text_box_lin_def,
            },
    'HT_rebin_flex' : {
            'title' : 'S_{T} [GeV]',
            'y_max_log_fct' : 100000.,
            'y_min_gr_zero' : 2e-3,
            'bin_width' : 100,
            '_set_leg_2_col_log' : {
                    'x_pos': 0.7,
                    'y_pos': 0.73,
                    'label_width': 0.30,
                    'label_height': 0.045,
                    'box_text_size' : 0.035,
                    'opt': 'f',
                    'opt_data': 'pl',
                    'reverse': True,
                    # 'sort_legend' : lambda w: 'TT ' in w[1],
                },
            'y_max_fct' : 1.2,
            # 'text_box_lin' : (0.19, 0.82, "#scale[0.8]{#bf{CMS}}"),
            # 'text_box_log' : (0.16, 0.91, "#scale[0.8]{#bf{CMS}}"),
            'err_empty_bins' : True,
            'draw_x_errs' : True,
            # 'draw_empty_bin_error' : True
            },
    'primary_lepton_pt' : {
            'y_max_fct' : 1.2,
            'rebin' : 25,
            # 'rebin_list' : list(i for i in xrange(0, 624, 48)) + [1200],
            # 'title' : 'S_{T} [GeV]',
            # 'y_max_log_fct' : 10000.,
            # 'y_min_gr_zero' : 1e-3,
            # 'y_max_fct' : 1.2,
            # 'bin_width' : 100,
            # 'err_empty_bins' : True
            # 'text_box_lin' : text_box_lin_def,
            },
    'primary_lepton_pt_rebin_flex' : {
            'y_max_fct' : 1.2,
            # 'rebin_list' : list(i for i in xrange(0, 624, 48)) + [1200],
            'bin_width' : 24,
            'draw_x_errs' : True,
            # 'title' : 'S_{T} [GeV]',
            # 'y_max_log_fct' : 10000.,
            # 'y_min_gr_zero' : 1e-3,
            # 'y_max_fct' : 1.2,
            # 'bin_width' : 100,
            # 'err_empty_bins' : True
            },
    'pt_ld_ak4_jet' : {
            'y_max_fct' : 1.2,
            'rebin' : 25,
            # 'rebin_list' : [0., 800., 900., 1000., 1200., 1500., 2000., 2500., 3000., 4500., 6500.],
            # 'title' : 'S_{T} [GeV]',
            # 'y_max_log_fct' : 10000.,
            # 'y_min_gr_zero' : 1e-3,
            # 'y_max_fct' : 1.2,
            # 'bin_width' : 100,
            # 'err_empty_bins' : True
            # 'text_box_lin' : text_box_lin_def,
            },
    'pt_subld_ak4_jet' : {
            'y_max_fct' : 1.2,
            'rebin' : 20,
            # 'rebin_list' : [0., 800., 900., 1000., 1200., 1500., 2000., 2500., 3000., 4500., 6500.],
            # 'title' : 'S_{T} [GeV]',
            # 'y_max_log_fct' : 10000.,
            # 'y_min_gr_zero' : 1e-3,
            # 'y_max_fct' : 1.2,
            # 'bin_width' : 100,
            # 'err_empty_bins' : True
            # 'text_box_lin' : text_box_lin_def,
            },
    'topjets[0].m_pt' : {
            'y_max_fct' : 1.2,
            'rebin' : 30,
            # 'rebin_list' : [0., 800., 900., 1000., 1200., 1500., 2000., 2500., 3000., 4500., 6500.],
            # 'title' : 'S_{T} [GeV]',
            # 'y_max_log_fct' : 10000.,
            # 'y_min_gr_zero' : 1e-3,
            # 'y_max_fct' : 1.2,
            # 'bin_width' : 100,
            # 'err_empty_bins' : True
            # 'text_box_lin' : text_box_lin_def,
            },
    'nomass_boost_2b_mass_softdrop' : {
            'rebin' : 30,
            'y_max_fct' : 1.6,
            'title' : 'M_{jet} [GeV]',
            # 'bin_width' : 5,
            'y_min_gr_zero' : 0.02,
            'y_max_log_fct' : 1000.,
            'scale' : 0.4,
            '_set_leg_1_col_lin' : {
                    'x_pos': 0.77,
                    'y_pos': 0.67,
                    'label_width': 0.20,
                    'label_height': 0.040,
                    'box_text_size' : 0.033,
                    'opt': 'f',
                    'opt_data': 'pl',
                    'reverse': True,
                    # 'sort_legend' : lambda w: 'TT ' in w[1],
                },
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
            'title' : 'M_{jet} [GeV]',
            'y_min_gr_zero' : 0.4,
            'y_max_log_fct' : 1000.,
            },
    'nobtag_boost_mass_nsjbtags' : {
            'title' : 'N(subjet b-tags)',
            'y_min_gr_zero' : 100,
            'y_max_log_fct' : 50.,
            '_set_leg_1_col_log' : {
                    'x_pos': 0.74,
                    'y_pos': 0.67,
                    'label_width': 0.30,
                    'label_height': 0.040,
                    'box_text_size' : 0.033,
                    'opt': 'f',
                    'opt_data': 'pl',
                    'reverse': True,
                    # 'sort_legend' : lambda w: 'TT ' in w[1],
                },
            # 'text_box_log' : (0.19, 0.82, "#scale[0.8]{#bf{CMS}}"),
            },
    'noboost_mass_1b[0].m_pt' : {
            'title' : 'p_{T} [GeV]',
            'rebin' : 50,
            # 'y_min_gr_zero' : 100,
            'y_max_log_fct' : 50.,
            },
    'noboost_mass_2b[0].m_pt' : {
            'title' : 'p_{T} [GeV]',
            'rebin' : 50,
            # 'y_min_gr_zero' : 100,
            'y_max_log_fct' : 50.,
            },
    }




# xml config editing functions

def do_set_cat(element_tree, catname):
    user_config = element_tree.getroot().find('Cycle').find('UserConfig')
    for item in user_config:
        if item.get('Name') == 'category':
            item.set('Value', catname)
            break

def make_higgs_split_item(element_tree, process='TpTp', final_states=None):
    tree_cycle = element_tree.getroot().find('Cycle')
    for ind, item in enumerate(tree_cycle.findall('InputData')):
        if process in item.get('Version'):
            for ver in final_states:
                split_smpl = copy.deepcopy(item)
                split_smpl.set('Version', split_smpl.get('Version')+'_'+ver)
                tree_cycle.insert(ind, split_smpl)
            tree_cycle.remove(item)

def do_set_eventnumber(element_tree, count=-1):
    input_data = element_tree.getroot().find('Cycle').findall('InputData')
    for attr in input_data:
        attr.set('NEventsMax', str(count))

def clean_input_data(element_tree, allowed_datasets):
    if allowed_datasets:
        tree_cycle = element_tree.getroot().find('Cycle')
        for item in tree_cycle.findall('InputData'):
            if all(f not in item.get('Version') for f in allowed_datasets):
                tree_cycle.remove(item)

def set_cacheable_false(element_tree, cacheable='False'):
    tree_cycle = element_tree.getroot().find('Cycle')
    for item in tree_cycle.findall('InputData'):
        item.set('Cacheable', cacheable)

def set_analysis_module(element_tree, analysis_module=''):
    if analysis_module:
        user_config = element_tree.getroot().find('Cycle').find('UserConfig')
        for item in user_config:
            if item.get('Name') == 'AnalysisModule':
                item.set('Value', analysis_module)
                break

def set_output_dir(element_tree, outputdir=''):
    if outputdir:
        sframe_cycle = element_tree.getroot().find('Cycle')
        sframe_cycle.set('OutputDirectory', outputdir)

def set_uncert(element_tree, uncert_name=''):
    if sys_uncerts:
        uncert = sys_uncerts[uncert_name]
        cycle = element_tree.getroot().find('Cycle')
        user_config = cycle.find('UserConfig')
        for name, value in uncert.iteritems():
            uc_item = list(i for i in user_config if i.get('Name') == name)
            assert uc_item, 'could not find item with name: %s' % name
            uc_item[0].set('Value', value)

# xml treecallback functions

# def set_uncert_func(uncert_name):
#     uncert = sys_uncerts[uncert_name]
#     def do_set_uncert(element_tree):
#         cycle = element_tree.getroot().find('Cycle')
#         user_config = cycle.find('UserConfig')
#         output_dir = cycle.get('OutputDirectory')
#         cycle.set('OutputDirectory', os.path.join(output_dir, uncert_name))

#         for name, value in uncert.iteritems():
#             uc_item = list(i for i in user_config if i.get('Name') == name)
#             assert uc_item, 'could not find item with name: %s' % name
#             uc_item[0].set('Value', value)

#     return do_set_uncert

def setup_for_finalsel(outputdir = '', allowed_datasets = None, count = '-1', analysis_module='', uncert_name='', categories=None):
    def tmp_func(element_tree):
        set_analysis_module(element_tree, analysis_module)
        set_output_dir(element_tree, outputdir)
        clean_input_data(element_tree, allowed_datasets)
        make_higgs_split_item(element_tree, 'TpTp', final_states_to_split_into_tp)
        make_higgs_split_item(element_tree, 'BpBp', final_states_to_split_into_bp)
        do_set_eventnumber(element_tree, count)
        set_uncert(element_tree, uncert_name)
        do_set_cat(element_tree, " ".join(categories))
    return tmp_func

def setup_for_presel(outputdir = '', allowed_datasets = None, count = '-1', analysis_module='', uncert_name='', categories=None):
    def tmp_func(element_tree):
        set_analysis_module(element_tree, analysis_module)
        set_output_dir(element_tree, outputdir)
        clean_input_data(element_tree, allowed_datasets)
        # make_higgs_split_item(element_tree, final_states_to_split_into)
        do_set_eventnumber(element_tree, count)
        # set_uncert(element_tree, uncert_name)
        do_set_cat(element_tree, " ".join(categories))
    return tmp_func


class MySFrameBatch(SFrame):

    def __init__(self, sel_type='', **kws):
        super(MySFrameBatch, self).__init__(**kws)
        # self.sel_type = sel_type

    def configure(self):
        self.xml_doctype = self.xml_doctype +"""
<!--
   <ConfigParse NEventsBreak="0" FileSplit="32" AutoResubmit="0" />
   <ConfigSGE RAM ="2" DISK ="2" Mail="dominik.nowatschin@cern.de" Notification="as" Workdir="workdir"/>
-->
"""


        if os.path.exists(self.cwd + 'workdir'):
            opt = ' -rl --exitOnQuestion'
        else:
            opt = ' -sl --exitOnQuestion'

        self.exe = 'sframe_batch.py' + opt



sframe_cfg_pre = '/afs/desy.de/user/n/nowatsd/xxl-af-cms/SFrameUHH2/CMSSW_7_6_3/src/UHH2/VLQToHiggsPairProd/config/TpTpPreselectionV2.xml'

def sel_data_hists(wrps):
    for w in wrps:
        if not (('SingleEle' in w.file_path and 'Mu45' in w.in_file_path) or ('SingleMuon' in w.file_path and 'El45' in w.in_file_path)):
            yield w

def set_leg_set(wrps):
    for w in wrps:
        if w.name == 'luminosity':
            w._legend_settings = {'mod_legend' : lambda _: None}
        yield w


def set_chan_text_box(wrps):
    for w in wrps:
        box_lin = []
        box_log = []
        if w.name in mod_dict:
            d = mod_dict[w.name]
            pars_lin = d.get('text_box_lin')
            if pars_lin:
                if not isinstance(pars_lin, list):
                    pars_lin = [pars_lin]
                box_lin += pars_lin
            pars_log = d.get('text_box_log')
            if pars_log:
                if not isinstance(pars_log, list):
                    pars_log = [pars_log]
                box_log += pars_log
        if 'Mu45' in w.in_file_path:
            box_lin += [(0.68, 0.89, "#scale[0.45]{2.6 fb^{-1} (13 TeV)}"), (0.19, 0.81, '#scale[0.5]{#mu channel}')]
            if 'TH2' in w.type:
                box_log += [(0.71, 0.89, "#scale[0.45]{2.6 fb^{-1} (13 TeV)}"), (0.16, 0.89, '#scale[0.5]{#mu channel}')]
            else:
                box_log += [(0.68, 0.89, "#scale[0.45]{2.6 fb^{-1} (13 TeV)}"), (0.16, 0.89, '#scale[0.5]{#mu channel}')]
        elif 'El45' in w.in_file_path:
            box_lin += [(0.68, 0.89, "#scale[0.45]{2.5 fb^{-1} (13 TeV)}"), (0.19, 0.81, '#scale[0.5]{e channel}')]
            if 'TH2' in w.type:
                box_log += [(0.71, 0.89, "#scale[0.45]{2.5 fb^{-1} (13 TeV)}"), (0.16, 0.89, '#scale[0.5]{e channel}')]
            else:
                box_log += [(0.68, 0.89, "#scale[0.45]{2.5 fb^{-1} (13 TeV)}"), (0.16, 0.89, '#scale[0.5]{e channel}')]
        w.text_box_log = box_log
        w.text_box_lin = box_lin
        yield w



def loader_hook_preselection(wrps):
    # wrps = varial.gen.gen_noex_rebin_nbins_max(wrps, nbins_max=60)
    wrps = common_plot.rebin_st_and_nak4(wrps, mod_dict)
    wrps = plot.common_loader_hook(wrps)
    wrps = sel_data_hists(wrps)
    wrps = common_plot.mod_title(wrps, mod_dict)
    # wrps = common_plot.norm_smpl(wrps, common_plot.pas_normfactors)
    # wrps = common_plot.norm_smpl(wrps, normfactors_ind_fs, calc_scl_fct=False)
    wrps = gen.gen_make_th2_projections(wrps)
    wrps = set_leg_set(wrps)
    # wrps = gen.sort(wrps, ['sys_info', 'in_file_path', 'sample'])
    # # if varial.settings.merge_decay_channels:
    # wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw'], print_warning=False)
        # wrps = vlq_common.merge_decay_channels(wrps, ['_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_other', print_warning=False)
    # wrps = itertools.ifilter(lambda w: not any(w.sample.endswith(g) for g in ['_other']), wrps)
    wrps = common_plot.mod_legend_no_thth(wrps)
    # if not varial.settings.flex_sig_norm:
    #     wrps = common_plot.norm_to_fix_xsec(wrps)
    wrps = sorted(wrps, key=lambda w: w.in_file_path)
    return wrps

def stack_setup_preselection(grps):
    grps = gen.mc_stack_n_data_sum(grps, None, True)
    grps = (set_chan_text_box(w) for w in grps)
    return grps

def get_style():
    # _style = style or varial.settings.style
    return [
        common_plot.mod_pre_bot_hist(mod_dict),
        common_plot.mk_split_err_ratio_plot_func_mod(poisson_errs=True),  # mk_pull_plot_func()
        # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
        rnd.mk_legend_func(),
        common_plot.mod_post_canv(mod_dict),
        # common_plot.mk_tobject_draw_func(TLatex(0.55, 0.89, "#scale[0.45]{2.5 (e), 2.6 (#mu) fb^{-1} (13 TeV)}"))
        # titlebox_func
    ]

def get_style_cf():
    # _style = style or varial.settings.style
    return [
        common_plot.mod_pre_bot_hist(),
        common_plot.mk_split_err_ratio_plot_func_mod(),  # mk_pull_plot_func()
        # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
        rnd.mk_legend_func(),
        common_plot.mod_post_canv(),
        common_plot.mk_tobject_draw_func(TLatex(0.55, 0.89, "#scale[0.45]{2.5 (e), 2.6 (#mu) fb^{-1} (13 TeV)}"))
        # titlebox_func
    ]

def mod_cf_labels(wrps):
    label_dict = {
        'trigger_accept_mu45' : 'Trigger',
        'trigger_accept_el45' : 'Trigger',
        '2D cut' : '2D iso.',
        'ST' : 'S_{T} > 600 GeV',
        'n_ak8' : 'N(AK8 jets) #geq 2',
        'n_ak4' : 'N(AK4 jets) #geq 3',
        'primary_electron_pt' : 'p_{T}(e) > 50 GeV',
        'pt_ld_ak4_jet' : 'p_{T}(1st AK4 jet) > 250 GeV',
        'pt_subld_ak4_jet' : 'p_{T}(2nd AK4 jet) > 75 GeV',
        'primary_muon_pt' : 'p_{T}(#mu) > 47 GeV',
    }

    for w in wrps:
        taxis = w.histo.GetXaxis()
        for i in xrange(w.histo.GetNbinsX() + 1):
            lab = label_dict.get(taxis.GetBinLabel(i), None)
            if lab:
                taxis.SetBinLabel(i, lab)
        taxis.SetTitleOffset(1.2)
        yield w

def cf_loader_hook(wrps):
    wrps = plot.common_loader_hook(wrps)
    wrps = sel_data_hists(wrps)
    wrps = cutflow_tables.rebin_cutflow(wrps)
    # wrps = mod_cf_labels(wrps)
    wrps = list(wrps)
    wrps = gen.sort(wrps, ['in_file_path', 'sample'])
    # wrps = list(wrps)
    # for w in wrps: print w.sample, w.in_file_path 
    #=== FIX MERGING WITH PREFIXES===
    # wrps = vlq_common.merge_decay_channels(wrps, postfixes=None, prefixes=['SingleMuon_', 'SingleEle_'], print_warning=False)
    # if varial.settings.merge_decay_channels:
    #     wrps = vlq_common.merge_decay_channels(wrps, postfixes=['_thth', '_thtz', '_thbw'], suffix='_thX', print_warning=True)
    #     wrps = vlq_common.merge_decay_channels(wrps, postfixes=['_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_other', print_warning=True)
    wrps = gen.sort(wrps, ['in_file_path'])
    return wrps

def mk_cutflow_chain_cat(category, pattern, datasets):
    cutflow_histos = varial.tools.HistoLoader(
        pattern=pattern,
        name='CutflowHistos',
        # pattern=common_plot.file_select(datasets_to_plot),
        # input_result_path='../../../../HistoLoader',
        filter_keyfunc=lambda w: 'cutflow' == w.in_file_path.split('/')[-1]\
                       and category == w.in_file_path.split('/')[0] \
                       and any(f in w.file_path for f in datasets),
                       # and (('SingleEle' not in w.file_path and 'Mu' in category) or\
                       # ('SingleMuon' not in w.file_path and 'El' in category)),
        # hook_loaded_histos=lambda w: cutflow_tables.rebin_cutflow(loader_hook(w))
        hook_loaded_histos=cf_loader_hook,
        # lookup_aliases=False
    )

    cutflow_stack_plots = varial.tools.Plotter(
        'CutflowStack',
        stack=True,
        input_result_path='../CutflowHistos',
        save_log_scale=True,
        hook_loaded_histos=lambda w: mod_cf_labels(w),
        canvas_post_build_funcs=get_style_cf(),
        mod_log=common_plot.mod_log_usr(mod_dict),
    )

    return varial.tools.ToolChain(category, [
        cutflow_histos,
        # cutflow_normed_plots,
        cutflow_tables.CutflowTableContent(eff_factor=1.),
        cutflow_tables.CutflowTableTxt(),
        cutflow_tables.CutflowTableTex(True, None),
        cutflow_stack_plots,
    ])

def mk_sframe_tools_and_plot(outputdir):
    # parser = OptionParser()

    # # parser.add_option('--output', type='string', action='store',
    # #                   dest='outputdir',
    # #                   help='Output directory')

    # # parser.add_option('--sel', type='string', action='store',
    # #                   dest='selection',
    # #                   help='Selection type (pre or final)')

    # (options, args) = parser.parse_args(argv)
    # argv = []

    count = '-1'

    global sys_uncerts
    allowed_datasets = []
    sframe_cfg = sframe_cfg_pre
    setup_for_ind_run = setup_for_presel
    # allowed_datasets=['TpTp']
    categories = categories_pre
    # analysis_module = 'TpTpTriggerStudy'
    analysis_module = 'TpTpPreselectionV2'
    sys_uncerts = all_sys_uncerts
    basenames = basenames_pre
    tex_base = '/Files_and_Plots*/Files_and_Plots_nominal/Plots/'
    # samples_to_plot = plot.almost_all_signals
    samples_to_plot = plot.less_samples_to_plot_pre
    varial.settings.fix_presel_sample = True
    filter_func = lambda w: any(f in w.in_file_path for f in ['Nm1Selection', 'PostSelection'])
    # varial.settings.merge_decay_channels = True

    def sf_batch_tc():
        plot_chain = []
        plot_chain += [Hadd(
            src_glob_path='../../SFrame/workdir*/uhh2.AnalysisModuleRunner.*.root',
            basenames=basenames,
            add_aliases_to_analysis=False,
            samplename_func=plot.get_samplename,
            # filter_keyfunc=lambda w: any(f in w for f in samples_to_plot)
            # overwrite=False
        )]
        plot_chain += [plot.mk_toolchain('Histograms', samples_to_plot,
            plotter_factory=plot.plotter_factory_stack( 
                hook_loaded_histos=loader_hook_preselection,
            #     mod_log=common_plot.mod_log_usr(mod_dict),
                # canvas_post_build_funcs=get_style()
                ),
            pattern='../Hadd/*.root',
            parallel=False,
            # input_result_path='../HistoLoader/HistoLoader*',
            # auto_legend=False,
            # name='HistogramsPostfit',
            # lookup_aliases=varial.settings.lookup_aliases
            )]
        # if options.selection == 'final':
            # plot_chain += [varial.tools.ToolChainParallel(
            #             'PlotsCompFinalStates',
            #             lazy_eval_tools_func=plot.mk_plots_and_cf(
            #                 datasets=plot.less_samples,
            #                 filter_keyfunc=lambda w: all(g not in w.file_path.split('/')[-1] for g in ['TpTp_M-0800', 'TpTp_M-1600'])\
            #                     and filter_func(w),
            #                 plotter_factory=plot.plotter_factory_stack(hook_loaded_histos=plot.loader_hook_compare_finalstates)
            #             )
            #         )]
        tc_list = []
        for uncert in sys_uncerts:
            sf_batch = MySFrameBatch(
                # sel_type=options.selection,
                cfg_filename=sframe_cfg,
                # xml_tree_callback=set_uncert_func(uncert),
                xml_tree_callback=setup_for_ind_run(outputdir='./', count='-1', analysis_module=analysis_module,
                    uncert_name=uncert, categories=categories, allowed_datasets=allowed_datasets),
                name='SFrame',
                add_aliases_to_analysis= False,
                # name='SFrame_' + uncert,
                halt_on_exception=False,
                )
            if uncert == 'nominal':
                tc_list.append(varial.tools.ToolChain('Files_and_Plots_'+uncert,[
                    sf_batch,
                    varial.tools.ToolChain(
                        'Plots',
                        plot_chain
                    )
                    ]))
            else:
                tc_list.append(varial.tools.ToolChain('Files_and_Plots_'+uncert,[
                    sf_batch
                    ]))

        return tc_list

    def tc_plot():
        base_dir = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/UHH2/VLQToHiggsPairProd/NewSamples-76X-v1/Preselection-v11'
        plot_path = 'Files_and_Plots/Files_and_Plots_nominal/Plots'
        hadd_pattern = varial.analysis.lookup_filename(os.path.join(base_dir, plot_path, 'Hadd/*.root'))
        # plot_chain = []
        # plot_chain += [Hadd(
        #     # src_glob_path='../../SFrame/workdir*/uhh2.AnalysisModuleRunner.*.root',
        #     src_glob_path=varial.analysis.lookup_filename(os.path.join(base_dir, 'Files_and_Plots/Files_and_Plots_nominal/SFrame/workdir/uhh2.AnalysisModuleRunner.MC.TpTp_*.root')),
        #     basenames=basenames,
        #     add_aliases_to_analysis=False,
        #     samplename_func=plot.get_samplename,
        #     name='HaddSignal'
        #     # filter_keyfunc=lambda w: any(f in w for f in samples_to_plot)
        #     # overwrite=False
        # )]

        plot_chain = plot.mk_toolchain('Histograms', samples_to_plot,
        # plot_chain += [plot.mk_toolchain('Histograms', samples_to_plot,
            plotter_factory=plot.plotter_factory_stack( 
                hook_loaded_histos=lambda w: common_plot.norm_smpl(loader_hook_preselection(w), sig_scalefactors, mk_legend=True),
                plot_setup=stack_setup_preselection,
                stack_setup=stack_setup_preselection,
            #     mod_log=common_plot.mod_log_usr(mod_dict),
                mod_log=common_plot.mod_log_usr(mod_dict),
                canvas_post_build_funcs=get_style()
                ),
            pattern=hadd_pattern,
            parallel=True,
            # input_result_path='../HistoLoader/HistoLoader*',
            # auto_legend=False,
            # name='HistogramsPostfit',
            # lookup_aliases=False
        )
        plot_chain_no_scale = plot.mk_toolchain('HistogramsNoScale', samples_to_plot,
        # plot_chain += [plot.mk_toolchain('Histograms', samples_to_plot,
            plotter_factory=plot.plotter_factory_stack( 
                hook_loaded_histos=lambda w: common_plot.norm_smpl(loader_hook_preselection(w), sig_scalefactors_log, mk_legend=True),
                plot_setup=stack_setup_preselection,
                stack_setup=stack_setup_preselection,
            #     mod_log=common_plot.mod_log_usr(mod_dict),
                mod_log=common_plot.mod_log_usr(mod_dict),
                canvas_post_build_funcs=get_style()
                ),
            pattern=hadd_pattern,
            parallel=True,
            # input_result_path='../HistoLoader/HistoLoader*',
            # auto_legend=False,
            # name='HistogramsPostfit',
            # lookup_aliases=False
        )
        # if options.selection == 'final':
            # plot_chain += [varial.tools.ToolChainParallel(
            #             'PlotsCompFinalStates',
            #             lazy_eval_tools_func=plot.mk_plots_and_cf(
            #                 datasets=plot.less_samples,
            #                 filter_keyfunc=lambda w: all(g not in w.file_path.split('/')[-1] for g in ['TpTp_M-0800', 'TpTp_M-1600'])\
            #                     and filter_func(w),
            #                 plotter_factory=plot.plotter_factory_stack(hook_loaded_histos=plot.loader_hook_compare_finalstates)
            #             )
            #         )]
        cf_chain = varial.tools.ToolChainParallel('CutflowPlots',
            list(mk_cutflow_chain_cat(cat, hadd_pattern, samples_to_plot) for cat in categories_pre),
            n_workers=1
            )

        return varial.tools.ToolChain('PlotsThesis', [
                plot_chain,
                plot_chain_no_scale,
                cf_chain
            ])

    def mk_tc_tex(source_dir):
        tc_tex = [
            tex_content.mk_plot_ind(
                (
                    ('ak4_sel_mu', os.path.join(source_dir, 'PlotsThesis/Histograms/StackedAll/Mu45/Nm1Selection/n_ak4_lin.pdf')),
                    ('ak4_sel_el', os.path.join(source_dir, 'PlotsThesis/Histograms/StackedAll/El45/Nm1Selection/n_ak4_lin.pdf')),
                    ('ak8_sel_mu', os.path.join(source_dir, 'PlotsThesis/Histograms/StackedAll/Mu45/Nm1Selection/n_ak8_lin.pdf')),
                    ('ak8_sel_el', os.path.join(source_dir, 'PlotsThesis/Histograms/StackedAll/El45/Nm1Selection/n_ak8_lin.pdf')),
                    ('st_sel_mu', os.path.join(source_dir, 'PlotsThesis/Histograms/StackedAll/Mu45/Nm1Selection/ST_lin.pdf')),
                    ('st_sel_el', os.path.join(source_dir, 'PlotsThesis/Histograms/StackedAll/El45/Nm1Selection/ST_lin.pdf')),
                    ('lep_sel_mu', os.path.join(source_dir, 'PlotsThesis/Histograms/StackedAll/Mu45/Nm1Selection/primary_muon_pt_lin.pdf')),
                    ('lep_sel_el', os.path.join(source_dir, 'PlotsThesis/Histograms/StackedAll/El45/Nm1Selection/primary_electron_pt_lin.pdf')),
                    ('twoD_qcd_sel_mu', os.path.join(source_dir, 'PlotsThesis/HistogramsNoScale/StackedAll/Mu45/Nm1Selection/twod_cut_hist_noIso_QCD_log.pdf')),
                    ('twoD_qcd_sel_el', os.path.join(source_dir, 'PlotsThesis/HistogramsNoScale/StackedAll/El45/Nm1Selection/twod_cut_hist_noIso_QCD_log.pdf')),
                    ('twoD_tt800_sel_mu', os.path.join(source_dir, 'PlotsThesis/HistogramsNoScale/StackedAll/Mu45/Nm1Selection/twod_cut_hist_noIso_TpTp_M-0800_log.pdf')),
                    ('twoD_tt800_sel_el', os.path.join(source_dir, 'PlotsThesis/HistogramsNoScale/StackedAll/El45/Nm1Selection/twod_cut_hist_noIso_TpTp_M-0800_log.pdf')),
                    ('twoD_tt1600_sel_mu', os.path.join(source_dir, 'PlotsThesis/HistogramsNoScale/StackedAll/Mu45/Nm1Selection/twod_cut_hist_noIso_TpTp_M-1600_log.pdf')),
                    ('twoD_tt1600_sel_el', os.path.join(source_dir, 'PlotsThesis/HistogramsNoScale/StackedAll/El45/Nm1Selection/twod_cut_hist_noIso_TpTp_M-1600_log.pdf')),
                    ('twoD_pTrel_mu', os.path.join(source_dir, 'PlotsThesis/HistogramsNoScale/StackedAll/Mu45/Nm1Selection/twod_cut_hist_noIso_py_log.pdf')),
                    ('twoD_pTrel_el', os.path.join(source_dir, 'PlotsThesis/HistogramsNoScale/StackedAll/El45/Nm1Selection/twod_cut_hist_noIso_py_log.pdf')),
                    ('twoD_dR_mu', os.path.join(source_dir, 'PlotsThesis/HistogramsNoScale/StackedAll/Mu45/Nm1Selection/twod_cut_hist_noIso_px_log.pdf')),
                    ('twoD_dR_el', os.path.join(source_dir, 'PlotsThesis/HistogramsNoScale/StackedAll/El45/Nm1Selection/twod_cut_hist_noIso_px_log.pdf')),
                    ('n_prim_vert_mu', os.path.join(source_dir, 'PlotsThesis/Histograms/StackedAll/Mu45/PostSelection/EventHists/N_PrimVertices_rebin_flex_lin.pdf')),
                    ('n_prim_vert_el', os.path.join(source_dir, 'PlotsThesis/Histograms/StackedAll/El45/PostSelection/EventHists/N_PrimVertices_rebin_flex_lin.pdf')),
                    ('lumi_mu', os.path.join(source_dir, 'PlotsThesis/Histograms/StackedAll/Mu45/PostSelection/LuminosityHists/luminosity_lin.pdf')),
                    ('lumi_el', os.path.join(source_dir, 'PlotsThesis/Histograms/StackedAll/El45/PostSelection/LuminosityHists/luminosity_lin.pdf')),
                    # ('ak8_sel_mu', os.path.join(source_dir, 'Preselection-v11/PlotsThesis/Histograms/StackedAll/Mu45/Nm1Selection/n_ak4_lin.pdf')),
                    # ('ak8_sel_el', os.path.join(source_dir, 'Preselection-v11/PlotsThesis/Histograms/StackedAll/El45/Nm1Selection/n_ak4_lin.pdf')),
                ),
                name='PreselectionPlots'),
            tex_content.mk_plot_ind(
                (
                    ('cutflow_mu', os.path.join(source_dir, 'PlotsThesis/CutflowPlots/Mu45/CutflowStack/cutflow_log.pdf'),),
                    ('cutflow_el', os.path.join(source_dir, 'PlotsThesis/CutflowPlots/El45/CutflowStack/cutflow_log.pdf'),),
                    # ('ak8_sel_mu', os.path.join(source_dir, 'Preselection-v11/PlotsThesis/Histograms/StackedAll/Mu45/Nm1Selection/n_ak4_lin.pdf')),
                    # ('ak8_sel_el', os.path.join(source_dir, 'Preselection-v11/PlotsThesis/Histograms/StackedAll/El45/Nm1Selection/n_ak4_lin.pdf')),
                ),
                (
                    ('cutflow_mu_table.tex', os.path.join(source_dir, 'PlotsThesis/CutflowPlots/Mu45/CutflowTableTex/cutflow_tabular.tex')),
                    ('cutflow_el_table.tex', os.path.join(source_dir, 'PlotsThesis/CutflowPlots/El45/CutflowTableTex/cutflow_tabular.tex')),
                ),
                name='CutflowPlots', size='0.7'),
            
        ] 
        tc_tex = varial.tools.ToolChain('CopyPlots', [
            varial.tools.ToolChain('TexThesis', tc_tex),
            varial.tools.CopyTool('/afs/desy.de/user/n/nowatsd/Documents/figures_thesis/', src='../TexThesis/*', ignore=('*.svn', '*.html', '*.log'), use_rsync=True, options='-qa --delete'),
            # varial.tools.CopyTool('/afs/desy.de/user/n/nowatsd/xxl-af-cms/PlotsToInspect', src='../../Plots_1/Histograms/StackedAll/Mu45/Nm1Selection', ignore=('*.svn', '*.log'), use_rsync=True, options='-qa --delete', name='CopyToolInspect'),
            # varial.tools.CopyTool('/afs/desy.de/user/n/nowatsd/xxl-af-cms/PlotsToInspect', src='../../Plots_1/CutflowPlots/Mu45/Cutflow*', ignore=('*.svn', '*.log'), use_rsync=True, options='-qa', name='CopyToolInspect2'),
            ])
        return tc_tex        


    return varial.tools.ToolChain(
        outputdir,
        [
            # git.GitAdder(),
            # ToolChain('Files_and_Plots',
            #     sf_batch_tc()
            # ),
            tc_plot(),
            varial.tools.WebCreator(no_tool_check=False),
            mk_tc_tex(outputdir),
            # mk_tex_tc_pre(options.outputdir+tex_base),
            # git.GitTagger(commit_prefix='In {0}'.format(options.outputdir)),
        ]
    )

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Provide output dir!'
        exit(-1)
    varial.tools.Runner(mk_sframe_tools_and_plot(sys.argv[1]), True)