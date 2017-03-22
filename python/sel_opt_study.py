#!/usr/bin/env python

import sys
import os
import time
import math
import cPickle
import pprint

import varial.settings
import varial.analysis
import varial.rendering as rnd
import UHH2.VLQSemiLepPreSel.common as vlq_common

# import common_vlq
import tptp_settings
# import final_plotting
import common_plot_new as common_plot
import plot_new as plot
import tex_content_new as tex_content
# import tptp_sframe 
# import compare_crs
import analysis
import treeproject_tptp
import sensitivity
import common_sensitivity
import plot_noreweighting as pn
from varial.extensions.limits import ThetaLimits, LimitGraphsNew, add_th_curve

from ROOT import TLatex, TH2

varial.settings.max_num_processes = 23

# hists_to_plot = [
#     'SingleTop',
#     'QCD',
#     'DYJets',
#     'WJets',
#     'Run2015CD',
#     # 'Diboson'
#     'TTbar_split'
# ]

# samples_to_plot = hists_to_plot + list(g + '_thth' for g in plot.less_signals)

# base_path = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/UHH2/'\
#     'VLQToHiggsPairProd/NewSamples-76X-v1/FinalSelection-v25'
base_path = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/UHH2/'\
    'VLQToHiggsPairProd/NewSamples-76X-v1/FinalSelection-v27_with_loose_Htag'
sub_path = 'Files_and_Plots'

bkg_samples = [
    'TTbar',
    'WJets',
    'QCD',
    'DYJets',
    'SingleTop',
    'Diboson',
]

tptp_signals = [
    'TpTp_M-0700',
    'TpTp_M-0800',
    'TpTp_M-0900',
    'TpTp_M-1000',
    'TpTp_M-1100',
    'TpTp_M-1200',
    'TpTp_M-1300',
    'TpTp_M-1400',
    'TpTp_M-1500',
    'TpTp_M-1600',
    'TpTp_M-1700',
    'TpTp_M-1800',
]

# common_plot.pas_normfactors = {}

# common_plot.norm_reg_dict = {}


uncerts = analysis.all_uncerts + ['sfel_trg', 'jsf'] # or get_sys_dir()


# ht_reweight_ttbar_no_top_pt_reweight = 'weight_htrew_tt*0.914621131' # last factor to correct discrepancy due to data but that you had previously
# ht_reweight_ttbar_no_top_pt_reweight = 'weight_htrew_tt' # last factor to correct discrepancy due to data but that you had previously
# ht_reweight_wjets_no_top_pt_reweight = 'weight_htrew_wjets'
# ht_reweight_ttbar_w_top_pt_reweight = 'weight_htrew_tt_toppt'
# ht_reweight_wjets_w_top_pt_reweight = 'weight_htrew_wjets_toppt'
# top_pt_reweight = '(weight_ttbar/0.9910819)'
# jetpt_reweight_ttbar_no_top_pt_reweight = 'weight_jetpt'
# jetpt_reweight_wjets_no_top_pt_reweight = 'weight_jetpt'

# lepton selections

el_channel = [
    'trigger_accept_el45   >= 1',
    'trigger_accept_mu45   == 0',
    'pt_ld_ak4_jet         > 250.',
    'pt_subld_ak4_jet      > 70.',
    'primary_lepton_pt     > 50.'
]

mu_channel = [
    'trigger_accept_mu45   >= 1',
    'primary_lepton_pt     > 47.'
]

# comp med - loose

baseline_selection_comp_htag = [
    'gendecay_accept          == 1',
    # 'n_ak8                    >= 2',
    # 'n_ak4                    >= 3',
    'ST                       > 800',
    # 'n_additional_btags_medium  >= 1',
]

sr2b_med_channel = [
    'n_higgs_tags_2b_med    >= 1',
    # 'n_additional_btags_medium  >= 1',
]

sr1b_med_channel = [
    'n_higgs_tags_2b_med    == 0',
    'n_higgs_tags_1b_med    >= 1',
    # 'n_additional_btags_medium  >= 1',
]

sr1b_only_med_channel = [
    'n_higgs_tags_1b_med    >= 1',
    # 'n_additional_btags_medium  >= 1',
]

sb_med_channel = [
    'n_higgs_tags_1b_med        == 0',
    'met                        >= 100',
    # 'n_additional_btags_medium  >= 1',
]

sr2b_loose_channel = [
    'n_higgs_tags_2b_loose    >= 1',
    # 'n_additional_btags_medium  >= 1',
]

sr1b_loose_channel = [
    'n_higgs_tags_2b_loose    == 0',
    'n_higgs_tags_1b_loose    >= 1',
    # 'n_additional_btags_medium  >= 1',
]

sr1b_only_loose_channel = [
    'n_higgs_tags_1b_loose    >= 1',
    # 'n_additional_btags_medium  >= 1',
]

sb_loose_channel = [
    'n_higgs_tags_1b_loose        == 0',
    'met                        >= 100',
    # 'n_additional_btags_medium  >= 1',
]


legends_comp_htag = {
    'med_all' : 'med_all',
    'loose_all' : 'loose_all',
    'med_sig_both' : 'med_sig_both',
    'loose_sig_both' : 'loose_sig_both',
    'med_sig_only2' : 'med_sig_only2',
    'loose_sig_only2' : 'loose_sig_only2',
}

final_regions_comp_htag = {
    'med_2b1b0h' : (
        ('SignalRegion2b_El45', baseline_selection_comp_htag + sr2b_med_channel + el_channel),
        ('SignalRegion1b_El45', baseline_selection_comp_htag + sr1b_med_channel + el_channel),
        ('SidebandRegion_El45', baseline_selection_comp_htag + sb_med_channel + el_channel),
        ('SignalRegion2b_Mu45', baseline_selection_comp_htag + sr2b_med_channel + mu_channel),
        ('SignalRegion1b_Mu45', baseline_selection_comp_htag + sr1b_med_channel + mu_channel),
        ('SidebandRegion_Mu45', baseline_selection_comp_htag + sb_med_channel + mu_channel),
    ),
    'loose_2b1b0h' : (
        ('SignalRegion2b_El45', baseline_selection_comp_htag + sr2b_loose_channel + el_channel),
        ('SignalRegion1b_El45', baseline_selection_comp_htag + sr1b_loose_channel + el_channel),
        ('SidebandRegion_El45', baseline_selection_comp_htag + sb_loose_channel + el_channel),
        ('SignalRegion2b_Mu45', baseline_selection_comp_htag + sr2b_loose_channel + mu_channel),
        ('SignalRegion1b_Mu45', baseline_selection_comp_htag + sr1b_loose_channel + mu_channel),
        ('SidebandRegion_Mu45', baseline_selection_comp_htag + sb_loose_channel + mu_channel),
    ),
    'med_2b1b' : (
        ('SignalRegion2b_El45', baseline_selection_comp_htag + sr2b_med_channel + el_channel),
        ('SignalRegion1b_El45', baseline_selection_comp_htag + sr1b_med_channel + el_channel),
        ('SignalRegion2b_Mu45', baseline_selection_comp_htag + sr2b_med_channel + mu_channel),
        ('SignalRegion1b_Mu45', baseline_selection_comp_htag + sr1b_med_channel + mu_channel),
    ),
    'loose_2b1b' : (
        ('SignalRegion2b_El45', baseline_selection_comp_htag + sr2b_loose_channel + el_channel),
        ('SignalRegion1b_El45', baseline_selection_comp_htag + sr1b_loose_channel + el_channel),
        ('SignalRegion2b_Mu45', baseline_selection_comp_htag + sr2b_loose_channel + mu_channel),
        ('SignalRegion1b_Mu45', baseline_selection_comp_htag + sr1b_loose_channel + mu_channel),
    ),
    'med_1cat_2b' : (
        ('SignalRegion2b_El45', baseline_selection_comp_htag + sr2b_med_channel + el_channel),
        ('SignalRegion2b_Mu45', baseline_selection_comp_htag + sr2b_med_channel + mu_channel),
    ),
    'loose_1cat_2b' : (
        ('SignalRegion2b_El45', baseline_selection_comp_htag + sr2b_loose_channel + el_channel),
        ('SignalRegion2b_Mu45', baseline_selection_comp_htag + sr2b_loose_channel + mu_channel),
    ),
    'med_1cat_1b' : (
        ('SignalRegion1b_El45', baseline_selection_comp_htag + sr1b_only_med_channel + el_channel),
        ('SignalRegion1b_Mu45', baseline_selection_comp_htag + sr1b_only_med_channel + mu_channel),
    ),
    'loose_1cat_1b' : (
        ('SignalRegion1b_El45', baseline_selection_comp_htag + sr1b_only_loose_channel + el_channel),
        ('SignalRegion1b_Mu45', baseline_selection_comp_htag + sr1b_only_loose_channel + mu_channel),
    ),
}

# optimiziation studies for other cuts

baseline_selection_sel_opt = [
    'gendecay_accept          == 1',
    'ST                       > 800',
    # 'n_higgs_tags_2b_med    >= 1',
]

# comp kinematic variables

st_list = { 'st_800' : ['ST > 800'], 'st_900' : ['ST > 900']}
st_list_ext = { 'st_700' : ['ST > 700'], 'st_800' : ['ST > 800'], 'st_900' : ['ST > 900'], 'st_1000' : ['ST > 1000']}
n_ak4_list = { 'n_ak4-3' : ['n_ak4 >= 3'], 'n_ak4-4' : ['n_ak4 >= 4']}
n_ak4_list_ext = { 'n_ak4-3' : ['n_ak4 >= 3'], 'n_ak4-4' : ['n_ak4 >= 4'], 'n_ak4-5' : ['n_ak4 >= 5'], 'n_ak4-6' : ['n_ak4 >= 6'], 'n_ak4-7' : ['n_ak4 >= 7'], 'n_ak4-8' : ['n_ak4 >= 8']}
n_ak8_list = { 'n_ak8-2' : ['n_ak8 >= 2'], 'n_ak8-3' : ['n_ak8 >= 3']}
n_btag_list = { 'n_additional_btags_medium-0' : ['n_additional_btags_medium >= 0'], 'n_additional_btags_medium-1' : ['n_additional_btags_medium >= 1']}
n_btag_list_ext = { 'n_additional_btags_medium-0' : ['n_additional_btags_medium >= 0'], 'n_additional_btags_medium-1' : ['n_additional_btags_medium >= 1'], 'n_additional_btags_medium-2' : ['n_additional_btags_medium >= 2'], 'n_additional_btags_medium-3' : ['n_additional_btags_medium >= 3']}
lep_pt_list = { 'primary_lepton_pt-47' : ['primary_lepton_pt >= 47.'], 'primary_lepton_pt-60' : ['primary_lepton_pt >= 60.']}
met_list = { 'met-0' : ['met >= 0'], 'met-50' : ['met >= 50']}
ld_jet_pt_list = { 'ak4_pt_1-0' : ['pt_ld_ak4_jet >= 0'], 'ak4_pt_1-400' : ['pt_ld_ak4_jet >= 400']}
ld_jet_pt_list_ext = { 'ak4_pt_1-0' : ['pt_ld_ak4_jet >= 0'], 'ak4_pt_1-150' : ['pt_ld_ak4_jet >= 150'], 'ak4_pt_1-400' : ['pt_ld_ak4_jet >= 400']}
subld_jet_pt_list = { 'ak4_pt_2-0' : ['pt_subld_ak4_jet >= 0'], 'ak4_pt_2-75' : ['pt_subld_ak4_jet >= 75']}
subld_jet_pt_list_ext = { 'ak4_pt_2-0' : ['pt_subld_ak4_jet >= 0'], 'ak4_pt_2-75' : ['pt_subld_ak4_jet >= 75'], 'ak4_pt_2-150' : ['pt_subld_ak4_jet >= 150']}

final_regions_comp_kinvar = {}

for ak4_k, ak4_v in n_ak4_list.iteritems():
    for n_ak8_k, n_ak8_v in n_ak8_list.iteritems():
        for n_btag_k, n_btag_v in n_btag_list.iteritems():
            for lep_pt_k, lep_pt_v in lep_pt_list.iteritems():
                for met_k, met_v in met_list.iteritems():
                    final_regions_comp_kinvar['__'.join([ak4_k, n_ak8_k, n_btag_k, lep_pt_k, met_k])] =\
                        (
                            ('El_channel_2b', baseline_selection_sel_opt + sr2b_med_channel + el_channel + ak4_v + n_ak8_v + n_btag_v + lep_pt_v + met_v),
                            ('Mu_channel_2b', baseline_selection_sel_opt + sr2b_med_channel + mu_channel + ak4_v + n_ak8_v + n_btag_v + lep_pt_v + met_v),
                            ('El_channel_1b', baseline_selection_sel_opt + sr1b_med_channel + el_channel + ak4_v + n_ak8_v + n_btag_v + lep_pt_v + met_v),
                            ('Mu_channel_1b', baseline_selection_sel_opt + sr1b_med_channel + mu_channel + ak4_v + n_ak8_v + n_btag_v + lep_pt_v + met_v),
                        )

# for ak4_k, ak4_v in n_ak4_list.iteritems():
#     for n_ak8_k, n_ak8_v in n_ak8_list.iteritems():
#         for n_btag_k, n_btag_v in n_btag_list.iteritems():
#             # for lep_pt_k, lep_pt_v in lep_pt_list.iteritems():
#             #     for met_k, met_v in met_list.iteritems():
#             final_regions_comp_kinvar['__'.join([ak4_k, n_ak8_k, n_btag_k])] =\
#                 (
#                     ('El_channel', baseline_selection_sel_opt + el_channel + ak4_v + n_ak8_v + n_btag_v),
#                     ('Mu_channel', baseline_selection_sel_opt + mu_channel + ak4_v + n_ak8_v + n_btag_v)
#                 )

legends_comp_kinvar = dict((a, a.replace('__', ', ')) for a in final_regions_comp_kinvar)


# comp only n(AK4)

baseline_selection_only_nak4 = [
    'n_ak8                    >= 2',
    'n_additional_btags_medium      >= 1',
]

final_regions_comp_njets = {}

for ak4_k, ak4_v in n_ak4_list_ext.iteritems():
    final_regions_comp_njets[ak4_k] =\
        (
            ('El_channel_2b', baseline_selection_only_nak4 + baseline_selection_sel_opt + sr2b_med_channel + el_channel + ak4_v),
            ('Mu_channel_2b', baseline_selection_only_nak4 + baseline_selection_sel_opt + sr2b_med_channel + mu_channel + ak4_v),
            ('El_channel_1b', baseline_selection_only_nak4 + baseline_selection_sel_opt + sr1b_med_channel + el_channel + ak4_v),
            ('Mu_channel_1b', baseline_selection_only_nak4 + baseline_selection_sel_opt + sr1b_med_channel + mu_channel + ak4_v),
        )

# comp N(AK4 b-tags)

baseline_selection_with_nbtag = [
    'gendecay_accept          == 1',
    # 'n_additional_btags_medium      >= 1',
    'n_ak8                    >= 2',
    'n_ak4                    >= 3',
]

final_regions_comp_nbtag = {}

for n_btag_k, n_btag_v in n_btag_list_ext.iteritems():
    final_regions_comp_nbtag[n_btag_k] =\
        (
            ('El_channel_2b', baseline_selection_with_nbtag + sr2b_med_channel + el_channel + n_btag_v),
            ('Mu_channel_2b', baseline_selection_with_nbtag + sr2b_med_channel + mu_channel + n_btag_v),
            ('El_channel_1b', baseline_selection_with_nbtag + sr1b_med_channel + el_channel + n_btag_v),
            ('Mu_channel_1b', baseline_selection_with_nbtag + sr1b_med_channel + mu_channel + n_btag_v),
        )
# comp with ST

baseline_selection_with_st = [
    'gendecay_accept          == 1',
    'n_additional_btags_medium      >= 1',
    'n_ak8                    >= 2',
    'n_ak4                    >= 3',
]

final_regions_comp_st = {}

for st_k, st_v in st_list_ext.iteritems():
    final_regions_comp_st[st_k] =\
        (
            ('El_channel_2b', baseline_selection_with_st + sr2b_med_channel + el_channel + st_v),
            ('Mu_channel_2b', baseline_selection_with_st + sr2b_med_channel + mu_channel + st_v),
            ('El_channel_1b', baseline_selection_with_st + sr1b_med_channel + el_channel + st_v),
            ('Mu_channel_1b', baseline_selection_with_st + sr1b_med_channel + mu_channel + st_v),
        )

# comp more kin variables

baseline_selection_with_jetpt = [
    'gendecay_accept          == 1',
    'n_additional_btags_medium      >= 1',
    'n_ak8                    >= 2',
    'n_ak4                    >= 3',
    'ST                       > 800',
]

final_regions_comp_jetpt = {}

for ld_jet_pt_k, ld_jet_pt_v in ld_jet_pt_list.iteritems():
    for subld_jet_pt_k, subld_jet_pt_v in subld_jet_pt_list.iteritems():
        final_regions_comp_jetpt['__'.join([ld_jet_pt_k, subld_jet_pt_k])] =\
            (
                ('El_channel_2b', baseline_selection_with_jetpt + sr2b_med_channel + el_channel + ld_jet_pt_v + subld_jet_pt_v),
                ('Mu_channel_2b', baseline_selection_with_jetpt + sr2b_med_channel + mu_channel + ld_jet_pt_v + subld_jet_pt_v),
                ('El_channel_1b', baseline_selection_with_jetpt + sr1b_med_channel + el_channel + ld_jet_pt_v + subld_jet_pt_v),
                ('Mu_channel_1b', baseline_selection_with_jetpt + sr1b_med_channel + mu_channel + ld_jet_pt_v + subld_jet_pt_v),
            )


# comp more kin variables

baseline_selection_with_ptvar = [
    'gendecay_accept          == 1',
    'n_additional_btags_medium      >= 1',
    'n_ak8                    >= 2',
    'n_ak4                    >= 3',
    'ST                       > 800',
]

final_regions_comp_ptvar = {}

for st_k, st_v in st_list.iteritems():
    for ld_jet_pt_k, ld_jet_pt_v in ld_jet_pt_list.iteritems():
        for subld_jet_pt_k, subld_jet_pt_v in subld_jet_pt_list.iteritems():
            for lep_pt_k, lep_pt_v in lep_pt_list.iteritems():
                for met_k, met_v in met_list.iteritems():
                    final_regions_comp_ptvar['__'.join([st_k, ld_jet_pt_k, subld_jet_pt_k, lep_pt_k, met_k])] =\
                        (
                            ('El_channel_2b', baseline_selection_with_ptvar + sr2b_med_channel + el_channel + st_v + ld_jet_pt_v + subld_jet_pt_v + lep_pt_v + met_v),
                            ('Mu_channel_2b', baseline_selection_with_ptvar + sr2b_med_channel + mu_channel + st_v + ld_jet_pt_v + subld_jet_pt_v + lep_pt_v + met_v),
                            ('El_channel_1b', baseline_selection_with_ptvar + sr1b_med_channel + el_channel + st_v + ld_jet_pt_v + subld_jet_pt_v + lep_pt_v + met_v),
                            ('Mu_channel_1b', baseline_selection_with_ptvar + sr1b_med_channel + mu_channel + st_v + ld_jet_pt_v + subld_jet_pt_v + lep_pt_v + met_v),
                        )



def_weights = dict(treeproject_tptp.sample_weights_def)

dict_uncerts_default = {
    'TTbar' : 1.20,
    'WJets' : 1.20,
    'DYJets' : 1.20,
    'SingleTop' : 1.20,
    'Diboson' : 1.20,
    'QCD' : 2.0,
}

def get_model(dict_uncerts=None):
    def tmp(hist_dir):
        import theta_auto

        model = theta_auto.build_model_from_rootfile(
            hist_dir,
            include_mc_uncertainties = True)#mc uncertainties=true
        model.fill_histogram_zerobins()
        # if final_states:
        #     if isinstance(final_states, str):
        #         final_states = [final_states]
        #     model.set_signal_processes(final_states)
        # else:
        #     model.set_signal_process_groups({'':[]})
        model.set_signal_processes('TpTp_M-*')
        if dict_uncerts:
            for s, u in dict_uncerts.iteritems():
                model.add_lognormal_uncertainty(s+'_rate', math.log(u), s)
        # model.add_lognormal_uncertainty('ttbar_rate', math.log(dict_uncerts['TTbar']), 'TTbar')
        # model.add_lognormal_uncertainty('wjets_rate', math.log(dict_uncerts['WJets']), 'WJets')
        # model.add_lognormal_uncertainty('qcd_rate', math.log(dict_uncerts['QCD']), 'QCD')
        # model.add_lognormal_uncertainty('zjets_rate', math.log(dict_uncerts['DYJets']), 'DYJets')
        # model.add_lognormal_uncertainty('singlet_rate', math.log(dict_uncerts['SingleTop']), 'SingleTop')
        # for smpl in background_samples:
        #     model.add_lognormal_uncertainty('luminosity', math.log(1.027), smpl)
        return model
    return tmp

def lim_loader_hook(wrps, brs):
    wrps = sensitivity.loader_hook(brs, merge=False)(wrps)
    # wrps = sorted(wrps, key=lambda w: w.in_file_path)
    # wrps = gen.group(wrps, lambda w: w.in_file_path)
    # wrps = common_plot.make_uncertainty_histograms(wrps, None, uncerts, False, False)
    # wrps = list(w for ws in wrps for w in ws)
    # wrps = remove_nom_wrps(wrps)
    # wrps = rename_uncerts(wrps)
    # wrps = rename_samples(wrps)
    # wrps = sorted(wrps, key=lambda w: w.in_file_path+'___'+w.sys_info+'___'+w.sample)
    # wrps = vlq_common.merge_decay_channels(wrps, postfixes=['__TTbar', '__TTbar_split', '__SingleTop'], print_warning=False)
    # wrps = vlq_common.merge_decay_channels(wrps, postfixes=['__WJets', '__DYJets', '__Diboson'], print_warning=False)
    return wrps



# def get_lims_comp(wrp):
#     # wrp = grp[0]
#     theta_res_exp = cPickle.loads(wrp.res_exp)
#     # theta_res_obs = cPickle.loads(wrp.res_obs)
#     if not theta_res_exp:
#         self.message('ERROR Theta result empty.')
#         raise RuntimeError  
#     x_list = theta_res_exp.x
#     y_exp_list = theta_res_exp.y
#     # y_obs_list = theta_res_obs.y
#     # sigma1_band_low = theta_res_exp.bands[1][0]
#     # sigma2_band_low = theta_res_exp.bands[0][0]
#     # sigma1_band_high = theta_res_exp.bands[1][1]
#     # sigma2_band_high = theta_res_exp.bands[0][1]
#     return x_list, y_exp_list, None, None, None, None, None

def get_lims_comp_mass_split(grp):
    val_tup_list = []
    wrps = grp.wrps
    for wrp in wrps:
        theta_res_exp = cPickle.loads(wrp.res_exp)
        # theta_res_obs = cPickle.loads(wrp.res_obs)
        if not theta_res_exp:
            continue
        x = theta_res_exp.x
        y_exp = theta_res_exp.y
        # y_obs = theta_res_obs.y
        # sigma1_low = theta_res_exp.bands[1][0]
        # sigma2_low = theta_res_exp.bands[0][0]
        # sigma1_high = theta_res_exp.bands[1][1]
        # sigma2_high = theta_res_exp.bands[0][1]
        if not (len(x)==1):
            monitor.message('limits.get_lims_mass_split', 'WARNING Not exactly one mass point in limit wrapper! ' +\
                'Length of x/sigma1_low/sigma1_high/sigma2_low/sigma2_high: %s/%s/%s/%s/%s' % (str(len(x)), str(len(sigma1_low)), str(len(sigma1_high)), str(len(sigma2_low)), str(len(sigma2_high))))
        val_tup_list.append((x[0], y_exp[0]))
    val_tup_list = sorted(val_tup_list, key=lambda w: w[0])
    x_list = list(w[0] for w in val_tup_list)
    y_exp_list = list(w[1] for w in val_tup_list)
    # y_obs_list = list(w[2] for w in val_tup_list)
    # sigma1_band_low = list(w[3] for w in val_tup_list)
    # sigma2_band_low = list(w[4] for w in val_tup_list)
    # sigma1_band_high = list(w[5] for w in val_tup_list)
    # sigma2_band_high = list(w[6] for w in val_tup_list)
    return x_list, y_exp_list, None, None, None, None, None


def hook_lim_graph_comp(sel):
    def tmp(wrp):
        setattr(wrp, 'selection', sel)
    return tmp

def comp_get_leg(wrps):
    for w in wrps:
        # print w.legend
        # w.legend = leg_dict[w.legend]
        w.line_style = 2
        w.color = varial.analysis.get_color(w.selection)
        yield w

def loader_hook_lim_graphs_comp(wrps):
    wrps = comp_get_leg(wrps)
    wrps = sorted(wrps, key=lambda w: w.selection)
    return wrps

def select_single_sig(signal):
    def tmp(wrp):
        if (any(a in os.path.basename(wrp.file_path) for a in bkg_samples) or signal in wrp.file_path):
            return True
    return tmp

def run_tp_lim(final_dir, final_regions):
    weights = dict(def_weights)
    # source_dir = os.path.join(base_path, final_dir)
    # uncerts = analysis.all_uncerts + ['sfel_trg'] # or get_sys_dir()
    # nom_pattern = ['../TreeProject/TreeProjector*/{0}.root']
    # sys_pattern = list('../TreeProject/SysTreeProjectors*/%s*/{0}.root'% i for i in uncerts)
    # input_pattern = nom_pattern+sys_pattern

    signals_tt = treeproject_tptp.tptp_signal_samples_only_thth
    # signals_bb = treeproject_tptp.bpbp_signal_samples

    plot_hists = ['ST']



    return varial.tools.ToolChain('CompLimits_'+final_dir, [
        # varial.tools.ToolChain('TreeProject',[
        treeproject_tptp.mk_tp(base_path+'/'+sub_path, final_regions, weights,
            samples=treeproject_tptp.background_samples+signals_tt, treeproject=TreeProjector,
            params=treeproject_tptp.st_only_params, name='TreeProjector'),
        varial.tools.ToolChainParallel('Limits',
            list(varial.tools.ToolChain(sig,
                [
                    varial.tools.HistoLoader(
                        name='HistoLoader',
                        pattern='../../../TreeProjector/*.root',
                        filter_keyfunc=select_single_sig(sig),
                        hook_loaded_histos=lambda w: lim_loader_hook(w,  { 'w' : 0.0, 'z' : 0.0, 'h' : 1.0 })
                    ),
                    ThetaLimits(
                            name='ThetaLimit',
                            # input_path= '../HistoLoader',
                            cat_key=lambda w: w.category,
                            sys_key=lambda w: w.sys_info,
                            # hook_loaded_histos=loader_hook_rename_uncerts,
                            # name= 'ThetaLimitsSplit'+str(ind),
                            asymptotic=True,
                            # brs=brs,
                            # make_root_files_only=True,
                            # theta_root_file_name='HiggsTagTemplate_'+br_string+'_'+signal,
                            model_func=get_model(dict_uncerts_default),
                            hook_result_wrp=hook_lim_graph_comp(final_dir)
                            # do_postfit=False,
                        )
                ]
                ) for sig in tptp_signals
            )
        )
        # plot.mk_toolchain('Histograms', plot.less_samples_to_plot_only_th, 
        #     pattern=map(lambda w: w.format('*'), input_pattern),
        #     web_create=True,
        #     lookup_aliases=False
        #     # quiet_mode=True
        #     ),
        # pn.mk_histoloader_merge(list('../'+ i for i in input_pattern), plot_hists),
        # pn.mk_histograms_merge(uncerts, name='HistogramsMerged'),
        # varial.tools.WebCreator()
        ])

def setup_graphs(grps):
    for g in grps:
        # g.legend = ', '.join(g[0].legend.split(', ')[-2])
        # g.legend = g[0].selection.replace('n_additional_btags_medium', 'n_btags')
        g.selection = g[0].selection
        g.line_style = g[0].line_style
        g.color = varial.analysis.get_color(g.selection)
        yield g


# def group_graphs_plot_nak4(wrp):
#     save_string = '__'.join(w.selection.split('__')[3:])
#     save_string = save_string.replace('primary_lepton_pt', 'PLpt')
#     return save_string

# def mod_legend_n(grps):
#     for g in grps:
#         for w in g:
#             w.legend = ', '.join(w.legend.split(', ')[:])
#         yield g

def mod_legend_def(wrps):
    for w in wrps:
        # w.save_name = group_graphs_plot_n(w)
        w.legend = w.selection
        # print w.save_name
        yield w

def hook_graph_def(wrps):
    wrps = mod_legend_def(wrps)
    return wrps



def group_graphs_plot_n(wrp):
    save_string = '__'.join(wrp.selection.split('__')[3:])
    save_string = save_string.replace('primary_lepton_pt', 'PLpt')
    return save_string

def mod_legend_n(wrps):
    for w in wrps:
        w.save_name = group_graphs_plot_n(w)
        w.legend = ', '.join(w.selection.split('__')[:-2])
        w.legend = w.legend.replace('n_additional_btags_medium', 'n_btags')
        # print w.save_name
        yield w

def hook_graphs_n(wrps):
    wrps = mod_legend_n(wrps)
    wrps = sorted(wrps, key=lambda w: w.save_name)
    return wrps



def group_graphs_plot_pt(wrp):
    save_string = '__'.join(wrp.selection.split('__')[:-2])
    save_string = save_string.replace('n_additional_btags_medium', 'n_btag')
    return save_string
    
def mod_legend_pt(wrps):
    for w in wrps:
        w.save_name = group_graphs_plot_pt(w)
        # print w.legend
        w.legend = ', '.join(w.selection.split('__')[3:])
        w.legend = w.legend.replace('n_additional_btags_medium', 'n_btags')
        yield w

def hook_graphs_pt(wrps):
    wrps = mod_legend_pt(wrps)
    wrps = sorted(wrps, key=lambda w: w.save_name)
    return wrps



def group_graphs_plot_ptjet(wrp):
    save_string = '__'.join([wrp.selection.split('__')[0], wrp.selection.split('__')[3], wrp.selection.split('__')[4]])
    # save_string = save_string.replace('n_additional_btags_medium', 'n_btag')
    return save_string

def mod_legend_ptjet(wrps):
    for w in wrps:
        w.save_name = group_graphs_plot_ptjet(w)
        # print w.legend
        w.legend = ', '.join([w.selection.split('__')[1], w.selection.split('__')[2]])
        # w.legend = w.legend.replace('n_additional_btags_medium', 'n_btags')
        yield w

def hook_graphs_ptjet(wrps):
    wrps = mod_legend_ptjet(wrps)
    wrps = sorted(wrps, key=lambda w: w.save_name)
    return wrps



def group_graphs_plot_stmetleppt(wrp):
    save_string = '__'.join([wrp.selection.split('__')[1], wrp.selection.split('__')[2]])
    # save_string = save_string.replace('n_additional_btags_medium', 'n_btag')
    return save_string    

def mod_legend_stmetleppt(wrps):
    for w in wrps:
        w.save_name = group_graphs_plot_stmetleppt(w)
        # print w.legend
        w.legend = ', '.join([w.selection.split('__')[0], w.selection.split('__')[3], w.selection.split('__')[4]])
        # w.legend = w.legend.replace('n_additional_btags_medium', 'n_btags')
        yield w

def hook_graphs_stmetleppt(wrps):
    wrps = mod_legend_stmetleppt(wrps)
    wrps = sorted(wrps, key=lambda w: w.save_name)
    return wrps

def setup_graphs_plot(grps):
    grps = varial.plotter.default_plot_colorizer(grps)
    # grps = mod_legend_pt(grps)
    grps = sensitivity.add_th_curve(grps, common_sensitivity.theory_masses, common_sensitivity.theory_cs, min_thy=1e-2, legend='Theory T#bar{T} (NNLO)')
    # grps = sensitivity.plot_setup_graphs(grps,
    #             th_x=common_sensitivity.theory_masses,
    #             th_y=common_sensitivity.theory_cs)
    return grps

# sframe_tools = mk_sframe_and_plot_tools()



def mk_tc_tex(base_dir):
    tc_tex = [
        tex_content.mk_plot_ind(
            (
                ('htag_comp', os.path.join(base_path, base_dir)+'/HTagComp/LimitCurvesComparedCompHTag/lim_graph_log.pdf'),
                ('0h_comp', os.path.join(base_path, base_dir)+'/HTagComp/LimitCurvesComparedComp0H/lim_graph_log.pdf'),
                ('nvar_comp', os.path.join(base_path, base_dir)+'/KinVarComp/LimitCurvesComparedCompN/PLpt-47__met-0_log.pdf'),
                ('ptvar_comp', os.path.join(base_path, base_dir)+'/KinVarComp/LimitCurvesComparedCompPt/Nak4-3__Nak8-2__Nbtag-1_log.pdf'),
                ('nbtag_comp', os.path.join(base_path, base_dir)+'/NBtagComp/LimitCurvesCompared/lim_graph_log.pdf'),
                ('jetpt_comp', os.path.join(base_path, base_dir)+'/PtVarComp/LimitCurvesComparedCompPtJet/st_800__primary_lepton_pt-47__met-0_log.pdf'),
                ('stmetptlep_comp', os.path.join(base_path, base_dir)+'/PtVarComp/LimitCurvesComparedCompSTMETLepPt/ak4_pt_1-0__ak4_pt_2-0_log.pdf'),
            ), name='SelOptPlots'
        ),
    ]
    tc_tex = varial.tools.ToolChain('CopyPlots', [
        varial.tools.ToolChain('TexThesis', tc_tex),
        varial.tools.CopyTool('/afs/desy.de/user/n/nowatsd/Documents/figures_thesis/', src='../TexThesis/*', ignore=('*.svn', '*.html', '*.log'), use_rsync=True, options='-qa --delete'),
        ])
    return tc_tex





from varial_ext.treeprojector import TreeProjector 
import multiprocessing as mp

if __name__ == '__main__':
    time.sleep(1)
    # src_dir = sys.argv[1]
    final_dir = sys.argv[1]
    # treeproject = TreeProjector
    # if len(sys.argv) > 2:
    #     use_batch = sys.argv[2]
    #     if use_batch == "True":
    #         from varial_ext.treeprojector_spark import SparkTreeProjector 
    #         treeproject = SparkTreeProjector
            # job_proc = mp.Process(target=treeproject_tptp._start_job_submitter)
            # job_proc.start()



    htag_tools = varial.tools.ToolChain('HTagComp',
        [
            varial.tools.ToolChainParallel('CompLimits', list(run_tp_lim(a, b) for a, b in final_regions_comp_htag.iteritems()), n_workers=1),
            LimitGraphsNew(
                limit_path='../CompLimits/CompLimits_*/Limits/TpTp_M-*/ThetaLimit',
                plot_obs=False,
                split_mass=False,
                plot_1sigmabands=False,
                plot_2sigmabands=False,
                hook_loaded_graphs=loader_hook_lim_graphs_comp,
                group_graphs=lambda ws: varial.gen.group(
                        ws, key_func=lambda w: w.selection),
                setup_graphs=setup_graphs,
                get_lim_params=get_lims_comp_mass_split,
                ),
            varial.plotter.Plotter(
                name='LimitCurvesComparedCompHTag',
                input_result_path='../LimitGraphsNew',
                filter_keyfunc=lambda w: '2b1b0h' not in w.selection,
                # plot_setup=plot_setup,
                hook_loaded_histos=hook_graph_def,
                plot_grouper=lambda ws: varial.gen.group(
                        ws, key_func=lambda w: w.save_name),
                # save_name_func=varial.plotter.save_by_name_with_hash
                save_name_func=lambda w: w.save_name,
                plot_setup=setup_graphs_plot,
                # keep_content_as_result=True,
                # hook_canvas_post_build=lambda w: sensitivity.canvas_setup_post(w, max_y=100.),
                # canvas_post_build_funcs=[
                #     rnd.mk_legend_func(x_pos=.7, y_pos=0.7, label_width=0.25, label_height=0.06, text_size=0.036),
                #     # common_plot.mk_tobject_draw_func(TLatex(0.16, 0.89, "#scale[0.7]{#bf{CMS}}")),
                #     common_plot.mk_tobject_draw_func(TLatex(0.57, 0.89, "#scale[0.5]{2.3/2.6/2.7 fb^{-1} (13 TeV)}")),
                #     ],
                # save_lin_log_scale=True
                ),
            varial.plotter.Plotter(
                name='LimitCurvesComparedComp0H',
                input_result_path='../LimitGraphsNew',
                filter_keyfunc=lambda w: '1cat' not in w.selection and 'loose' not in w.selection,
                # plot_setup=plot_setup,
                hook_loaded_histos=hook_graph_def,
                plot_grouper=lambda ws: varial.gen.group(
                        ws, key_func=lambda w: w.save_name),
                # save_name_func=varial.plotter.save_by_name_with_hash
                save_name_func=lambda w: w.save_name,
                plot_setup=setup_graphs_plot,
                # keep_content_as_result=True,
                # hook_canvas_post_build=lambda w: sensitivity.canvas_setup_post(w, max_y=100.),
                # canvas_post_build_funcs=[
                #     rnd.mk_legend_func(x_pos=.7, y_pos=0.7, label_width=0.25, label_height=0.06, text_size=0.036),
                #     # common_plot.mk_tobject_draw_func(TLatex(0.16, 0.89, "#scale[0.7]{#bf{CMS}}")),
                #     common_plot.mk_tobject_draw_func(TLatex(0.57, 0.89, "#scale[0.5]{2.3/2.6/2.7 fb^{-1} (13 TeV)}")),
                #     ],
                # save_lin_log_scale=True
                )
        ]
        # + mk_graph_tc(legends_comp_htag)
        )
    kinvar_tools = varial.tools.ToolChain('KinVarComp',
        [
            varial.tools.ToolChainParallel('CompLimits', list(run_tp_lim(a, b) for a, b in final_regions_comp_kinvar.iteritems()), n_workers=1),
            LimitGraphsNew(
                limit_path='../CompLimits/CompLimits_*/Limits/TpTp_M-*/ThetaLimit',
                plot_obs=False,
                split_mass=False,
                plot_1sigmabands=False,
                plot_2sigmabands=False,
                hook_loaded_graphs=loader_hook_lim_graphs_comp,
                group_graphs=lambda ws: varial.gen.group(
                        ws, key_func=lambda w: w.selection),
                setup_graphs=setup_graphs,
                get_lim_params=get_lims_comp_mass_split,
                ),
            varial.plotter.Plotter(
                name='LimitCurvesComparedCompN',
                input_result_path='../LimitGraphsNew',
                filter_keyfunc=lambda w: 'n_ak4-5' not in w.selection,
                # plot_setup=plot_setup,
                hook_loaded_histos=hook_graphs_n,
                plot_grouper=lambda ws: varial.gen.group(
                        ws, key_func=lambda w: w.save_name),
                # save_name_func=varial.plotter.save_by_name_with_hash
                save_name_func=lambda w: w._renderers[0].save_name,
                plot_setup=setup_graphs_plot,
                # keep_content_as_result=True,
                # hook_canvas_post_build=lambda w: sensitivity.canvas_setup_post(w, max_y=100.),
                # canvas_post_build_funcs=[
                #     rnd.mk_legend_func(x_pos=.7, y_pos=0.7, label_width=0.25, label_height=0.06, text_size=0.036),
                #     # common_plot.mk_tobject_draw_func(TLatex(0.16, 0.89, "#scale[0.7]{#bf{CMS}}")),
                #     common_plot.mk_tobject_draw_func(TLatex(0.57, 0.89, "#scale[0.5]{2.3/2.6/2.7 fb^{-1} (13 TeV)}")),
                #     ],
                # save_lin_log_scale=True
                ),
            varial.plotter.Plotter(
                name='LimitCurvesComparedCompPt',
                input_result_path='../LimitGraphsNew',
                # filter_keyfunc=lambda w: 'Uncleaned' in w.legend,
                # plot_setup=plot_setup,
                hook_loaded_histos=hook_graphs_pt,
                plot_grouper=lambda ws: varial.gen.group(
                        ws, key_func=lambda w: w.save_name),
                # save_name_func=varial.plotter.save_by_name_with_hash
                save_name_func=lambda w: w._renderers[0].save_name,
                plot_setup=setup_graphs_plot,
                # keep_content_as_result=True,
                # hook_canvas_post_build=lambda w: sensitivity.canvas_setup_post(w, max_y=100.),
                # canvas_post_build_funcs=[
                #     rnd.mk_legend_func(x_pos=.7, y_pos=0.7, label_width=0.25, label_height=0.06, text_size=0.036),
                #     # common_plot.mk_tobject_draw_func(TLatex(0.16, 0.89, "#scale[0.7]{#bf{CMS}}")),
                #     common_plot.mk_tobject_draw_func(TLatex(0.57, 0.89, "#scale[0.5]{2.3/2.6/2.7 fb^{-1} (13 TeV)}")),
                #     ],
                # save_lin_log_scale=True
                )
        ]
        # + mk_graph_tc(legends_comp_kinvar)
        )
    njet_tools = varial.tools.ToolChain('NJetComp',
        [
            varial.tools.ToolChainParallel('CompLimits', list(run_tp_lim(a, b) for a, b in final_regions_comp_njets.iteritems()), n_workers=1),
            LimitGraphsNew(
                limit_path='../CompLimits/CompLimits_*/Limits/TpTp_M-*/ThetaLimit',
                plot_obs=False,
                split_mass=False,
                plot_1sigmabands=False,
                plot_2sigmabands=False,
                hook_loaded_graphs=loader_hook_lim_graphs_comp,
                group_graphs=lambda ws: varial.gen.group(
                        ws, key_func=lambda w: w.selection),
                setup_graphs=setup_graphs,
                get_lim_params=get_lims_comp_mass_split,
                ),
            varial.plotter.Plotter(
                name='LimitCurvesCompared',
                input_result_path='../LimitGraphsNew',
                # filter_keyfunc=lambda w: 'Uncleaned' in w.legend,
                # plot_setup=plot_setup,
                hook_loaded_histos=hook_graph_def,
                plot_grouper=lambda ws: varial.gen.group(
                        ws, key_func=lambda w: w.save_name),
                # save_name_func=varial.plotter.save_by_name_with_hash
                save_name_func=lambda w: w.save_name,
                plot_setup=setup_graphs_plot,
                # keep_content_as_result=True,
                # hook_canvas_post_build=lambda w: sensitivity.canvas_setup_post(w, max_y=100.),
                # canvas_post_build_funcs=[
                #     rnd.mk_legend_func(x_pos=.7, y_pos=0.7, label_width=0.25, label_height=0.06, text_size=0.036),
                #     # common_plot.mk_tobject_draw_func(TLatex(0.16, 0.89, "#scale[0.7]{#bf{CMS}}")),
                #     common_plot.mk_tobject_draw_func(TLatex(0.57, 0.89, "#scale[0.5]{2.3/2.6/2.7 fb^{-1} (13 TeV)}")),
                #     ],
                # save_lin_log_scale=True
                )
        ]
        # + mk_graph_tc(legends_comp_htag)
        )
    st_tools = varial.tools.ToolChain('STComp',
        [
            varial.tools.ToolChainParallel('CompLimits', list(run_tp_lim(a, b) for a, b in final_regions_comp_st.iteritems()), n_workers=1),
            LimitGraphsNew(
                limit_path='../CompLimits/CompLimits_*/Limits/TpTp_M-*/ThetaLimit',
                plot_obs=False,
                split_mass=False,
                plot_1sigmabands=False,
                plot_2sigmabands=False,
                hook_loaded_graphs=loader_hook_lim_graphs_comp,
                group_graphs=lambda ws: varial.gen.group(
                        ws, key_func=lambda w: w.selection),
                setup_graphs=setup_graphs,
                get_lim_params=get_lims_comp_mass_split,
                ),
            varial.plotter.Plotter(
                name='LimitCurvesCompared',
                input_result_path='../LimitGraphsNew',
                # filter_keyfunc=lambda w: all(g not in w.selection for g in ['n_ak4-5','n_ak4-4', 'n_ak8-3']),
                # plot_setup=plot_setup,
                hook_loaded_histos=hook_graph_def,
                plot_grouper=lambda ws: varial.gen.group(
                        ws, key_func=lambda w: w.save_name),
                # save_name_func=varial.plotter.save_by_name_with_hash
                save_name_func=lambda w: w.save_name,
                plot_setup=setup_graphs_plot,
                # keep_content_as_result=True,
                # hook_canvas_post_build=lambda w: sensitivity.canvas_setup_post(w, max_y=100.),
                # canvas_post_build_funcs=[
                #     rnd.mk_legend_func(x_pos=.7, y_pos=0.7, label_width=0.25, label_height=0.06, text_size=0.036),
                #     # common_plot.mk_tobject_draw_func(TLatex(0.16, 0.89, "#scale[0.7]{#bf{CMS}}")),
                #     common_plot.mk_tobject_draw_func(TLatex(0.57, 0.89, "#scale[0.5]{2.3/2.6/2.7 fb^{-1} (13 TeV)}")),
                #     ],
                # save_lin_log_scale=True
                )
        ]
        # + mk_graph_tc(legends_comp_htag)
        )
    jetpt_tools = varial.tools.ToolChain('JetPtComp',
        [
            varial.tools.ToolChainParallel('CompLimits', list(run_tp_lim(a, b) for a, b in final_regions_comp_jetpt.iteritems()), n_workers=1),
            LimitGraphsNew(
                limit_path='../CompLimits/CompLimits_*/Limits/TpTp_M-*/ThetaLimit',
                plot_obs=False,
                split_mass=False,
                plot_1sigmabands=False,
                plot_2sigmabands=False,
                hook_loaded_graphs=loader_hook_lim_graphs_comp,
                group_graphs=lambda ws: varial.gen.group(
                        ws, key_func=lambda w: w.selection),
                setup_graphs=setup_graphs,
                get_lim_params=get_lims_comp_mass_split,
                ),
            varial.plotter.Plotter(
                name='LimitCurvesCompared',
                input_result_path='../LimitGraphsNew',
                filter_keyfunc=lambda w: all(g not in w.selection for g in ['ak4_pt_1-400', 'ak4_pt_1-150']), 
                # plot_setup=plot_setup,
                hook_loaded_histos=hook_graph_def,
                plot_grouper=lambda ws: varial.gen.group(
                        ws, key_func=lambda w: w.save_name),
                # save_name_func=varial.plotter.save_by_name_with_hash
                save_name_func=lambda w: w.save_name,
                plot_setup=setup_graphs_plot,
                # keep_content_as_result=True,
                # hook_canvas_post_build=lambda w: sensitivity.canvas_setup_post(w, max_y=100.),
                # canvas_post_build_funcs=[
                #     rnd.mk_legend_func(x_pos=.7, y_pos=0.7, label_width=0.25, label_height=0.06, text_size=0.036),
                #     # common_plot.mk_tobject_draw_func(TLatex(0.16, 0.89, "#scale[0.7]{#bf{CMS}}")),
                #     common_plot.mk_tobject_draw_func(TLatex(0.57, 0.89, "#scale[0.5]{2.3/2.6/2.7 fb^{-1} (13 TeV)}")),
                #     ],
                # save_lin_log_scale=True
                )
        ]
        # + mk_graph_tc(legends_comp_htag)
        )
    nbtag_tools = varial.tools.ToolChain('NBtagComp',
        [
            varial.tools.ToolChainParallel('CompLimits', list(run_tp_lim(a, b) for a, b in final_regions_comp_nbtag.iteritems()), n_workers=1),
            LimitGraphsNew(
                limit_path='../CompLimits/CompLimits_*/Limits/TpTp_M-*/ThetaLimit',
                plot_obs=False,
                split_mass=False,
                plot_1sigmabands=False,
                plot_2sigmabands=False,
                hook_loaded_graphs=loader_hook_lim_graphs_comp,
                group_graphs=lambda ws: varial.gen.group(
                        ws, key_func=lambda w: w.selection),
                setup_graphs=setup_graphs,
                get_lim_params=get_lims_comp_mass_split,
                ),
            varial.plotter.Plotter(
                name='LimitCurvesCompared',
                input_result_path='../LimitGraphsNew',
                # filter_keyfunc=lambda w: 'Uncleaned' in w.legend,
                # plot_setup=plot_setup,
                hook_loaded_histos=hook_graph_def,
                plot_grouper=lambda ws: varial.gen.group(
                        ws, key_func=lambda w: w.save_name),
                # save_name_func=varial.plotter.save_by_name_with_hash
                save_name_func=lambda w: w.save_name,
                plot_setup=setup_graphs_plot,
                # keep_content_as_result=True,
                # hook_canvas_post_build=lambda w: sensitivity.canvas_setup_post(w, max_y=100.),
                # canvas_post_build_funcs=[
                #     rnd.mk_legend_func(x_pos=.7, y_pos=0.7, label_width=0.25, label_height=0.06, text_size=0.036),
                #     # common_plot.mk_tobject_draw_func(TLatex(0.16, 0.89, "#scale[0.7]{#bf{CMS}}")),
                #     common_plot.mk_tobject_draw_func(TLatex(0.57, 0.89, "#scale[0.5]{2.3/2.6/2.7 fb^{-1} (13 TeV)}")),
                #     ],
                # save_lin_log_scale=True
                )
        ]
        # + mk_graph_tc(legends_comp_htag)
        )
    ptvar_tools = varial.tools.ToolChain('PtVarComp',
        [
            varial.tools.ToolChainParallel('CompLimits', list(run_tp_lim(a, b) for a, b in final_regions_comp_ptvar.iteritems()), n_workers=1),
            LimitGraphsNew(
                limit_path='../CompLimits/CompLimits_*/Limits/TpTp_M-*/ThetaLimit',
                plot_obs=False,
                split_mass=False,
                plot_1sigmabands=False,
                plot_2sigmabands=False,
                hook_loaded_graphs=loader_hook_lim_graphs_comp,
                group_graphs=lambda ws: varial.gen.group(
                        ws, key_func=lambda w: w.selection),
                setup_graphs=setup_graphs,
                get_lim_params=get_lims_comp_mass_split,
                ),
            varial.plotter.Plotter(
                name='LimitCurvesComparedCompPtJet',
                input_result_path='../LimitGraphsNew',
                filter_keyfunc=lambda w: 'n_ak4-5' not in w.selection,
                # plot_setup=plot_setup,
                hook_loaded_histos=hook_graphs_ptjet,
                plot_grouper=lambda ws: varial.gen.group(
                        ws, key_func=lambda w: w.save_name),
                # save_name_func=varial.plotter.save_by_name_with_hash
                save_name_func=lambda w: w._renderers[0].save_name,
                plot_setup=setup_graphs_plot,
                # keep_content_as_result=True,
                # hook_canvas_post_build=lambda w: sensitivity.canvas_setup_post(w, max_y=100.),
                # canvas_post_build_funcs=[
                #     rnd.mk_legend_func(x_pos=.7, y_pos=0.7, label_width=0.25, label_height=0.06, text_size=0.036),
                #     # common_plot.mk_tobject_draw_func(TLatex(0.16, 0.89, "#scale[0.7]{#bf{CMS}}")),
                #     common_plot.mk_tobject_draw_func(TLatex(0.57, 0.89, "#scale[0.5]{2.3/2.6/2.7 fb^{-1} (13 TeV)}")),
                #     ],
                # save_lin_log_scale=True
                ),
            varial.plotter.Plotter(
                name='LimitCurvesComparedCompSTMETLepPt',
                input_result_path='../LimitGraphsNew',
                # filter_keyfunc=lambda w: 'Uncleaned' in w.legend,
                # plot_setup=plot_setup,
                hook_loaded_histos=hook_graphs_stmetleppt,
                plot_grouper=lambda ws: varial.gen.group(
                        ws, key_func=lambda w: w.save_name),
                # save_name_func=varial.plotter.save_by_name_with_hash
                save_name_func=lambda w: w._renderers[0].save_name,
                plot_setup=setup_graphs_plot,
                # keep_content_as_result=True,
                # hook_canvas_post_build=lambda w: sensitivity.canvas_setup_post(w, max_y=100.),
                # canvas_post_build_funcs=[
                #     rnd.mk_legend_func(x_pos=.7, y_pos=0.7, label_width=0.25, label_height=0.06, text_size=0.036),
                #     # common_plot.mk_tobject_draw_func(TLatex(0.16, 0.89, "#scale[0.7]{#bf{CMS}}")),
                #     common_plot.mk_tobject_draw_func(TLatex(0.57, 0.89, "#scale[0.5]{2.3/2.6/2.7 fb^{-1} (13 TeV)}")),
                #     ],
                # save_lin_log_scale=True
                )
        ]
        # + mk_graph_tc(legends_comp_kinvar)
        )
    all_tools = varial.tools.ToolChainParallel(final_dir,
        [htag_tools,
         njet_tools,
         kinvar_tools,
         st_tools,
         # jetpt_tools,
         nbtag_tools,
         ptvar_tools,
         mk_tc_tex(final_dir)
        ], n_workers=1
        )
    varial.tools.Runner(all_tools, default_reuse=True)
    # varial.tools.CopyTool('~/www/vlq_analysis/tight_selection2/',
    #     src=final_dir, use_rsync=True).run()