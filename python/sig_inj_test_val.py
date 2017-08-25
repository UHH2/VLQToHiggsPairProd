#!/usr/bin/env python

import sys
import os
import time
import math
import glob
import pprint
import array

import varial.settings
import varial.rendering as rnd
import varial.generators as gen
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
import plot_noreweighting as pn
# import plot_thesis

from ROOT import TLatex, TH1, TH1F, TH2, TFile

import theta_auto

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
    'VLQToHiggsPairProd/NewSamples-76X-v1/FinalSelection-v26'
sub_path = 'Files_and_Plots2'

# common_plot.pas_normfactors = {}

# common_plot.norm_reg_dict = {}


uncerts = analysis.all_uncerts + ['sfel_trg', 'jsf'] # or get_sys_dir()


tp_histos = {
    'ST'                            : ('S_{T} [GeV]',                               65, 0, 6500),
    'n_ak4'                         : ('N(Ak4 Jets)',                      20, -.5, 19.5),
    'n_ak8'                         : ('N(Ak8 Jets)',                      11, -.5, 10.5),
    # 'pt_ld_ak4_jet'                 : ('p_{T} leading Ak4 Jet [GeV]',               100, 0., 2000.),
    # 'jets[].m_pt'              : ('p_{T} Jets [GeV]',             100, 0., 2000.),
    # 'jets[2].m_pt'              : ('p_{T} third Ak4 Jet [GeV]',             50, 0., 1000.),
    # 'jets[3].m_pt'              : ('p_{T} fourth Ak4 Jet [GeV]',             30, 0., 600.),
    # # 'pt_fourth_ak4_jet'              : ('p_{T} fourth Ak4 Jet',             30, 0., 600.),
    # 'pt_subld_ak4_jet'              : ('p_{T} subleading Ak4 Jet [GeV]',             80, 0., 1600.),
    # 'topjets[0].m_pt'                 : ('p_{T} leading Ak8 Jet [GeV]',               120, 0., 2400.),
    # 'topjets[1].m_pt'              : ('p_{T} subleading Ak8 Jet',             100, 0., 2000.),
    'HT'                            : ('H_{T} [GeV]',                               65, 0, 6500),
    'met'                           : ('missing E_{T} [GeV]',                              50, 0., 1000.),
    'primary_lepton_pt'             : ('Primary Lepton p_{T} [GeV]',               50, 0., 1200.),
    'n_additional_btags_medium'     : ('N(b-tags)',                             8, -.5, 7.5),
    # 'primary_muon_pt'               : ('Primary Muon p_{T} [GeV]',                 50, 0., 1200.),
    # 'primary_electron_pt'           : ('Primary Electron p_{T} [GeV]',             50, 0., 1200.),
    # 'PrimaryLepton.Particle.m_eta'                : ('#eta primary lepton',                  50, -3., 3.),
    'n_higgs_tags_1b_med'           : ('N(type-I Higgs-Tags)',           5, -.5, 4.5),
    'n_higgs_tags_2b_med'           : ('N(type-II Higgs-Tags)',          5, -.5, 4.5),
    'dR_jets_1_PrimaryLepton_cl'               : ('dR(ld. AK4 jet, primary lepton)',   50, 0., 5.),
    'dR_jets_2_PrimaryLepton_cl'           : ('dR(subld. AK4 jet, primary lepton))',   50, 0., 5.),
    'dR_higgs_tags_1b_med_1_PrimaryLepton_cl'                : ('dR(Higgs-Tag(1b), primary lepton)',   50, 0., 5.),
    'dR_higgs_tags_1b_med_1_jets_cl'               : ('dR(Higgs-Tag(1b), cl. AK4 jet)',   50, 0., 5.),
    'dR_higgs_tags_1b_med_1_topjets_cl'           : ('dR(Higgs-Tag(1b), cl. AK8 jet)',   50, 0., 5.),
    'dR_topjets_1_topjets_cl'                 : ('dR(ld. AK8 jet, cl. AK8 jet)',   50, 0., 5.),
    'noboost_mass_1b[0].m_pt'           : ('p_{T} type-I Higgs tag mass [GeV]',           100, 0., 2000.),
    'noboost_mass_2b[0].m_pt'           : ('p_{T} type-II Higgs tag mass [GeV]',           100, 0., 2000.),
    'nomass_boost_1b_mass_softdrop'           : ('groomed type-I Higgs tag mass [GeV]',           60, 0., 300.),
    'nomass_boost_2b_mass_softdrop'           : ('groomed type-II Higgs tag mass [GeV]',           60, 0., 300.),
    'nobtag_boost_mass_nsjbtags'           : ('N(subjet b-tags)',           6, -0.5, 5.5),
#     'n_higgs_tags_1b_med_sm_up'      : ('N(type-I Higgs-Tags)',           5, -.5, 4.5),
#     'n_higgs_tags_2b_med_sm_up'      : ('N(type-II Higgs-Tags)',           5, -.5, 4.5),
#     'n_higgs_tags_1b_med_sm_down'      : ('N(type-I Higgs-Tags)',           5, -.5, 4.5),
#     'n_higgs_tags_2b_med_sm_down'      : ('N(type-II Higgs-Tags)',           5, -.5, 4.5),
#     'n_higgs_tags_1b_med_sc_up'      : ('N(type-I Higgs-Tags)',           5, -.5, 4.5),
#     'n_higgs_tags_2b_med_sc_up'      : ('N(type-II Higgs-Tags)',           5, -.5, 4.5),
#     'n_higgs_tags_1b_med_sc_down'      : ('N(type-I Higgs-Tags)',           5, -.5, 4.5),
#     'n_higgs_tags_2b_med_sc_down'      : ('N(type-II Higgs-Tags)',           5, -.5, 4.5),
#     'noboost_mass_1b[0].m_pt'           : ('p_{T} type-I Higgs tag mass [GeV]',           100, 0., 2000.),
#     'noboost_mass_2b[0].m_pt'           : ('p_{T} type-II Higgs tag mass [GeV]',           100, 0., 2000.),
#     'nomass_boost_1b_mass_softdrop'           : ('groomed type-I Higgs tag mass [GeV]',           60, 0., 300.),
#     'nomass_boost_2b_mass_softdrop'           : ('groomed type-II Higgs tag mass [GeV]',           60, 0., 300.),
#     'nobtag_boost_mass_nsjbtags'           : ('N(subjet b-tags)',           6, -0.5, 5.5),
#     'n_prim_vertices'              : ("N(Primary Vertices)", 35, -.5, 34.5),
#     'n_ak8_higgs_cand'              : ('N(Higgs Candidates)',              8, -.5, 7.5),
}

tp_params = {
    'histos': tp_histos,
    'treename': 'AnalysisTree',
    'nm1' : False,
}

baseline_selection = [
    'gendecay_accept          == 1',
    'n_ak8                    >= 2',
    'n_ak4                    >= 3',
    'ST                       > 800',
]

baseline_selection_btag = baseline_selection + [
    'n_additional_btags_medium  >= 1',
]

comb_lep_chan = [
    'trigger_accept_el45 + trigger_accept_mu45          >= 1'
]

# final regions

sig_sel = [
    'dR_jets_2_PrimaryLepton_cl  > 1'
]

cr_sel = [
    'dR_jets_2_PrimaryLepton_cl  <= 1'
]

sr2b_channel = baseline_selection_btag + [
    'n_higgs_tags_2b_med    >= 1',
    # 'n_additional_btags_medium  >= 1',
]

sr1b_channel = baseline_selection_btag + [
    'n_higgs_tags_2b_med    == 0',
    'n_higgs_tags_1b_med    >= 1',
    # 'n_additional_btags_medium  >= 1',
]

sb_channel = baseline_selection_btag + [
    'n_higgs_tags_1b_med        == 0',
    'met                        >= 100',
    # 'n_additional_btags_medium  >= 1',
]

sb_ttbar_channel = baseline_selection + [
    'n_higgs_tags_1b_med        == 0',
    'n_additional_btags_medium  >= 2',
    'met                        >= 100',
]

sb_ttbar_channel_nomet = baseline_selection + [
    'n_higgs_tags_1b_med        == 0',
    'n_additional_btags_medium  >= 2',
    # 'met                        >= 100',
]

sb_wjets_channel = baseline_selection + [
    'n_higgs_tags_1b_med        == 0',
    'n_additional_btags_medium  == 0',
    'met                        >= 100',
]

# sb_ttbar_channel_w_htag = baseline_selection + [
#     # 'n_higgs_tags_1b_med        == 0',
#     'n_additional_btags_medium  >= 2',
#     # 'met                        >= 100',
# ]

# sb_wjets_channel_w_htag = baseline_selection + [
#     # 'n_higgs_tags_1b_med        == 0',
#     'n_additional_btags_medium  == 0',
#     'met                        >= 100',
# ]


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

# ht_reweight_ttbar_no_top_pt_reweight = 'weight_htrew_tt*0.914621131' # last factor to correct discrepancy due to data but that you had previously
ht_reweight_ttbar_no_top_pt_reweight = 'weight_htrew_tt' # last factor to correct discrepancy due to data but that you had previously
ht_reweight_wjets_no_top_pt_reweight = 'weight_htrew_wjets'
# ht_reweight_ttbar_w_top_pt_reweight = 'weight_htrew_tt_toppt'
# ht_reweight_wjets_w_top_pt_reweight = 'weight_htrew_wjets_toppt'
top_pt_reweight = '(weight_ttbar/0.9910819)'
top_pt_reweight_nomax = '(weight_ttbar_nomax/0.9910819)'
top_pt_reweight_new = '(weight_ttbar_new/1.)'
jetpt_reweight_ttbar_no_top_pt_reweight = 'weight_jetpt'
jetpt_reweight_wjets_no_top_pt_reweight = 'weight_jetpt'


final_regions_def = (
    ('BaseLineSelection_El45', baseline_selection+el_channel),
    ('BaseLineSelection_Mu45', baseline_selection+mu_channel),
    ('BaseLineSelectionBtag_El45', baseline_selection_btag+el_channel),
    ('BaseLineSelectionBtag_Mu45', baseline_selection_btag+mu_channel),
    # ('SidebandTTJetsRegion_Comb', comb_lep_chan     + sb_ttbar_channel),
    # ('SidebandWPlusJetsRegion_Comb', comb_lep_chan  + sb_wjets_channel),
    ('SignalRegion2b_El45', sr2b_channel + el_channel),
    ('SignalRegion1b_El45', sr1b_channel + el_channel),
    ('SidebandRegion_El45', sb_channel + el_channel),
    ('SignalRegion2b_Mu45', sr2b_channel + mu_channel),
    ('SignalRegion1b_Mu45', sr1b_channel + mu_channel),
    ('SidebandRegion_Mu45', sb_channel + mu_channel),
    ('SidebandTTJetsRegion_El45', sb_ttbar_channel + el_channel),
    ('SidebandTTJetsRegion_Mu45', sb_ttbar_channel + mu_channel),
    ('SidebandTTJetsNoMetRegion_El45', sb_ttbar_channel_nomet + el_channel),
    ('SidebandTTJetsNoMetRegion_Mu45', sb_ttbar_channel_nomet + mu_channel),
    ('SidebandWPlusJetsRegion_El45', sb_wjets_channel + el_channel),
    ('SidebandWPlusJetsRegion_Mu45', sb_wjets_channel + mu_channel),
)

final_regions_dr_sel = (
    ('BaseLineSelection_El45', baseline_selection+el_channel),
    ('BaseLineSelection_Mu45', baseline_selection+mu_channel),
    ('BaseLineSelectionBtag_El45', baseline_selection_btag+el_channel),
    ('BaseLineSelectionBtag_Mu45', baseline_selection_btag+mu_channel),
    # ('SidebandTTJetsRegion_Comb', comb_lep_chan     + sb_ttbar_channel),
    # ('SidebandWPlusJetsRegion_Comb', comb_lep_chan  + sb_wjets_channel),
    ('SignalRegion2b_El45', sr2b_channel + sig_sel + el_channel),
    ('SignalRegion1b_El45', sr1b_channel + sig_sel + el_channel),
    ('SidebandRegion_El45', sb_channel + sig_sel + el_channel),
    ('SignalRegion2b_Mu45', sr2b_channel + sig_sel + mu_channel),
    ('SignalRegion1b_Mu45', sr1b_channel + sig_sel + mu_channel),
    ('SidebandRegion_Mu45', sb_channel + sig_sel + mu_channel),
    ('SidebandTTJetsRegion_El45', sb_ttbar_channel + cr_sel + el_channel),
    ('SidebandTTJetsRegion_Mu45', sb_ttbar_channel + cr_sel + mu_channel),
    ('SidebandTTJetsNoMetRegion_El45', sb_ttbar_channel_nomet + cr_sel + el_channel),
    ('SidebandTTJetsNoMetRegion_Mu45', sb_ttbar_channel_nomet + cr_sel + mu_channel),
    ('SidebandWPlusJetsRegion_El45', sb_wjets_channel + cr_sel + el_channel),
    ('SidebandWPlusJetsRegion_Mu45', sb_wjets_channel + cr_sel + mu_channel),
    ('SidebandTTJetsDrInvRegion_El45', sb_ttbar_channel + sig_sel + el_channel),
    ('SidebandTTJetsDrInvRegion_Mu45', sb_ttbar_channel + sig_sel + mu_channel),
    ('SidebandTTJetsNoMetDrInvRegion_El45', sb_ttbar_channel_nomet + sig_sel + el_channel),
    ('SidebandTTJetsNoMetDrInvRegion_Mu45', sb_ttbar_channel_nomet + sig_sel + mu_channel),
    ('SidebandWPlusJetsDrInvRegion_El45', sb_wjets_channel + sig_sel + el_channel),
    ('SidebandWPlusJetsDrInvRegion_Mu45', sb_wjets_channel + sig_sel + mu_channel),
    # ('SidebandTTJetsWHtagRegion_El45', sb_ttbar_channel_w_htag + cr_sel + el_channel),
    # ('SidebandTTJetsWHtagRegion_Mu45', sb_ttbar_channel_w_htag + cr_sel + mu_channel),
    # ('SidebandWPlusJetsWHtagRegion_El45', sb_wjets_channel_w_htag + cr_sel + el_channel),
    # ('SidebandWPlusJetsWHtagRegion_Mu45', sb_wjets_channel_w_htag + cr_sel + mu_channel),
)

# def add_all_with_weight_uncertainties(dict_weight_uncerts):
#     def add_uncerts(base_path, regions, weights, samples, params):
#         pdf_params = params if params == treeproject_tptp.st_only_params else treeproject_tptp.st_plus_jets_params
#         def tmp():
#             sys_tps = []
#             sys_tps += treeproject_tptp.add_higgs_smear_uncerts(base_path, regions, weights, samples, params)
#             sys_tps += treeproject_tptp.add_generic_uncerts(base_path, regions, weights, samples, params)
#             sys_tps += treeproject_tptp.add_scale_var_uncerts(base_path, regions, weights, samples, params)
#             for weight_name, weight_dict in dict_weight_uncerts.iteritems():
#                 sys_tps += treeproject_tptp.add_weight_uncerts(base_path, regions, weights, weight_name, weight_dict, samples, params)
#             if treeproject_tptp.ttbar_smpl in samples:
#                 sys_tps += treeproject_tptp.add_ttbar_scale_uncerts(base_path, base_path, regions, weights, samples, params)
#             sys_tps += treeproject_tptp.add_jec_uncerts(base_path, regions, weights, samples, params)
#             sys_tps += treeproject_tptp.add_pdf_uncerts(base_path, regions, weights, samples, pdf_params)
#             return sys_tps
#         return tmp
#     return add_uncerts

# def add_only_weight_uncertainties(dict_weight_uncerts):
#     def add_uncerts(base_path, regions, weights, samples, params):
#         def tmp():
#             sys_tps = []
#             for weight_name, weight_dict in dict_weight_uncerts.iteritems():
#                 sys_tps += treeproject_tptp.add_weight_uncerts(base_path, regions, weights, weight_name, weight_dict, samples, params)
#             return sys_tps
#         return tmp
#     return add_uncerts

def_weights = dict(treeproject_tptp.sample_weights_def)

rebin_list = [0., 100., 200., 300., 400., 500., 600., 700., 800., 900., 1000., 1200., 1500., 2000., 2500., 3000., 4500., 6500.]

######################################################## limit calculation ###
class MakeSigInjRootFile(varial.tools.Tool):
    io = varial.pklio

    def __init__(
        self,
        input_path='../HistoLoader',
        filter_keyfunc=None,
        normfactors=None,
        toys_param='toys:1.0',
        dat_key = lambda w: w.is_data,
        sig_key = lambda w: w.is_signal,
        bkg_key = lambda w: w.is_background,
        cat_key=lambda w: w.category,  # lambda w: w.category,
        theta_root_file_name=None,
        do_merging=False,
        bootstrapped = True,
        name=None,
    ):
        super(MakeSigInjRootFile, self).__init__(name)
        self.input_path = input_path
        self.filter_keyfunc = filter_keyfunc
        self.normfactors = normfactors
        self.toys_param = toys_param
        self.dat_key = dat_key
        self.sig_key = sig_key
        self.bkg_key = bkg_key
        self.cat_key = cat_key
        self.theta_root_file_name = theta_root_file_name
        self.do_merging = do_merging
        self.bootstrapped = bootstrapped
        self.signals = []

    # def prepare_hist_sig_inj(self, wrps):

    #     def sort_signal_data(wrp):
    #         if wrp.is_data:
    #             return '0'
    #         elif wrp.is_signal:
    #             return '1'
    #         else:
    #             return '2'

    #     if self.filter_keyfunc:
    #         wrps = (w for w in wrps if self.filter_keyfunc(w))


    #     wrps = common_plot.norm_smpl(wrps, self.normfactors, calc_scl_fct=False, mark_scaled='br_scaled')
    #     wrps = gen.gen_rebin(wrps, rebin_list, True)
    #     # wrps = common_plot.rebin_st_and_nak4(wrps)
    #     wrps = varial.generators.gen_add_wrp_info(
    #         wrps, category=lambda w: w.in_file_path.split('/')[0])



    #     wrps = sorted(wrps, key=lambda w: w.in_file_path+'___'+w.name+'___'+sort_signal_data(w))
    #     wrps = merge_sig_data(wrps, False)
    #     return wrps


    # def make_histo_sig_inj(self, wrp):


    #     if isinstance(self.input_path, str):
    #         self.input_path = [self.input_path]
    #     wrpwrps = []
    #     for i in self.input_path:
    #         if i.startswith('..'):
    #             i = os.path.join(self.cwd, i)
    #         wrpwrps += list(self.lookup_result(p) for p in glob.glob(i))
    #     wrps = []
    #     for ws in wrpwrps:
    #         if ws:
    #             wrps += list(w for w in ws)
    #     assert wrps, 'no input for path: %s' % self.input_path
    #     wrps = self.prepare_hist_sig_inj(wrps)




    #     # if not sigs:
    #     #     self.message('WARNING No signal histograms, no limit setting possible.')
    #     #     # self.what = 'expected'
    #     #     self.with_signal = False
    #     # if not dats:
    #     #     self.message('WARNING No data histogram, only expected limits.')
    #     #     self.what = 'expected'
    #     #     self.with_data = False

    #     # res = varial.operations.merge(dats+sigs)
    #     # res.file_path = ''
    #     # # res.histo.Sumw2()
    #     # for i in xrange(1, res.histo.GetNbinsX() + 1):
    #     #     err = math.sqrt(res.histo.GetBinContent(i))
    #     #     res.histo.SetBinError(i, err)

    #     for w in wrps:
    #         setattr(wrp, self.cat_key(w) + '__bkg', w.histo)
    #     # for w in bkgs:
    #     #     setattr(wrp, self.cat_key(w) + '__' + w.sample, w.histo)
    #     # for w in sigs:
    #     #     setattr(wrp, self.cat_key(w) + '__' + w.sample, w.histo)
    #     return wrp


    def prepare_dat_sig_bkg(self, wrps):
        if self.filter_keyfunc:
            wrps = (w for w in wrps if self.filter_keyfunc(w))

        # if self.hook_loaded_histos:
        #     wrps = self.hook_loaded_histos(wrps)


        wrps = common_plot.norm_smpl(wrps, self.normfactors, calc_scl_fct=False, mark_scaled='br_scaled')
        wrps = gen.gen_rebin(wrps, rebin_list, True)
        # wrps = common_plot.rebin_st_and_nak4(wrps)
        wrps = varial.generators.gen_add_wrp_info(
            wrps, category=lambda w: w.in_file_path.split('/')[0])
        if self.do_merging:
            wrps = sorted(wrps, key=lambda w: '{0}___{1}___{2}'.format(w.sys_info, w.in_file_path, w.sample))
            wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw'], print_warning=False, yield_orig=False)

        wrps = list(wrps)
        dats = list(w for w in wrps if self.dat_key(w))
        sigs = list(w for w in wrps if self.sig_key(w))
        bkgs = list(w for w in wrps if self.bkg_key(w))
        for s in sigs:
            if s.sample not in self.signals:
                self.signals.append(s.sample)
        return dats, sigs, bkgs

    def add_nominal_hists(self, wrp):

        if isinstance(self.input_path, str):
            self.input_path = [self.input_path]
        wrpwrps = []
        for i in self.input_path:
            if i.startswith('..'):
                i = os.path.join(self.cwd, i)
            wrpwrps += list(self.lookup_result(p) for p in glob.glob(i))
        wrps = []
        for ws in wrpwrps:
            if ws:
                wrps += list(w for w in ws)
        assert wrps, 'no input for path: %s' % self.input_path
        dats, sigs, bkgs = self.prepare_dat_sig_bkg(wrps)

        assert bkgs, 'no background histograms present.'
        # assert sigs, 'no signal histograms present.'

        if not sigs:
            self.message('WARNING No signal histograms, no limit setting possible.')
            # self.what = 'expected'
            self.with_signal = False
        if not dats:
            self.message('WARNING No data histogram, only expected limits.')
            self.what = 'expected'
            self.with_data = False

        for w in dats:
            setattr(wrp, self.cat_key(w) + '__DATA', w.histo)
        for w in bkgs:
            setattr(wrp, self.cat_key(w) + '__' + w.sample, w.histo)
        for w in sigs:
            setattr(wrp, self.cat_key(w) + '__' + w.sample, w.histo)

    @staticmethod
    def store_histos_for_theta(wrp):
        # write manually
        f = TFile.Open(wrp.file_path, "RECREATE")
        f.cd()
        for key, value in wrp.__dict__.iteritems():
            if isinstance(value, TH1):
                value.SetName(key)
                value.Write()
        f.Close()
        return wrp

    def run(self):
        # clear workdir to make theta really run

        # use theta_auto.make_data and theta_auto.histogram_from_dbblob(blob_data, blob_uncertainties = None) functions to create theta histogram, then make rootfile from this histogram!



        if glob.glob(self.cwd+'*'):
            os.system('rm -rf %s*' % self.cwd)

        # create wrp
        hist_name = self.theta_root_file_name+'.root' if self.theta_root_file_name else 'ThetaHistos%s.root' % hex(hash(time.clock()))
        wrp = varial.wrappers.Wrapper(
            name='ThetaHistos',
            file_path=os.path.join(self.cwd, hist_name),
        )

        # add histograms and store for theta
        # wrp = self.make_histo_sig_inj(wrp)
        self.add_nominal_hists(wrp)
        self.store_histos_for_theta(wrp)

        base_dir = os.getcwd()
        os.chdir(self.cwd)

        # model_toys = test_model.simple_counting(s = 1.2, b = 10.0, n_obs = 7, b_uncertainty = 3.0)
        # model_toys = theta_auto.get_bootstrapped_model(model_toys)
        # N_toy = 1000
        # data = make_data(model_toys, 'toys:1.0', N_toy)

        # model.set_signal_process_groups({'':[]})


        theta_auto.config.workdir = '.'
        theta_auto.config.report = theta_auto.html_report('report.html')
        if not os.path.exists('plots'):
            os.mkdir('plots')

        options = theta_auto.Options()
        options.set('minimizer', 'strategy', 'robust')
        options.set('minimizer', 'minuit_tolerance_factor', '1000')
        
        try:
            model = theta_auto.build_model_from_rootfile(hist_name)
            print self.signals
            model.set_signal_processes(self.signals)
            model.fill_histogram_zerobins()
            if self.bootstrapped:
                new_model = theta_auto.get_bootstrapped_model(model, options=options, verbose=True)
            else:
                new_model = model
            toy_data = theta_auto.make_data(new_model, self.toys_param, 1, options=options, retval = 'data')
            # toy_histo = theta_auto.histogram_from_dbblob(toy_data.values()[0])
            # dict_histo = {'toy_histo' : toy_histo}
            for s in self.signals:
                theta_auto.write_histograms_to_rootfile(toy_data[s], 'ToyHisto__%s.root' % s)
            # print toy_data
        except:
            etype, evalue, etb = sys.exc_info()
            print etype, evalue, etb
            raise etype, evalue, etb
        finally:
            os.chdir(base_dir) 


        # except (AssertionError, IndexError, RuntimeError) as e:
            # self.message('WARNING Error occured during theta run: %s' % e)
        # finally:


        # if signal:
        #     model.set_signal_processes(signal)
        # else:
        # theta's config.workdir is broken for mle, where it writes temp data
        # into cwd. Therefore change into self.cwd.
        


# def mk_histoloader_merge(input_pattern, plot_hists=plot_hists, samples=samples_to_plot_thth):
#     return varial.tools.ToolChainParallel('HistoLoader',
#         list(varial.tools.HistoLoader(
#             pattern=map(lambda w: w.format('*'+g+'*'), input_pattern),
#             filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in samples) and\
#                 'Region_Comb' not in w.in_file_path and\
#                 any(w.in_file_path.endswith(f) for f in plot_hists),
#             hook_loaded_histos=plot.loader_hook_merge_regions,
#             name='HistoLoader_'+g,
#             lookup_aliases=False,
#             raise_on_empty_result=False,
#             quiet_mode=True
#             ) for g in samples))

# def mk_histograms_merge(uncerts=uncerts, name='Histograms', samples=samples_to_plot_thth):
#     return plot.mk_toolchain(name, samples,
#         plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=False, 
#             hook_loaded_histos=loader_hook_nominal_brs,
#             mod_log=common_plot.mod_log_usr(mod_dict),
#             canvas_post_build_funcs=get_style()),
#         pattern=None,
#         input_result_path='../HistoLoader/HistoLoader*',
#         # auto_legend=False,
#         # name='HistogramsPostfit',
#         # lookup_aliases=varial.settings.lookup_aliases
#         )

# def mk_histograms_merge_ratio_sb(uncerts=uncerts, name='HistogramsRatioSB'):
#     return plot.mk_toolchain(name, samples_to_plot_thth,
#         plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=False, 
#             hook_loaded_histos=plot.loader_hook_merge_lep_channels,
#             filter_keyfunc=lambda w: 'Run2015CD' not in w.file_path,
#             mod_log=common_plot.mod_log_usr(mod_dict),
#             canvas_post_build_funcs=[
#                 common_plot.mod_pre_bot_hist(),
#                 common_plot.mk_bottom_plot_sig_bkg_ratio(),  # mk_pull_plot_func()
#                 # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
#                 rnd.mk_legend_func(),
#                 common_plot.mod_post_canv(mod_dict),
#                 common_plot.mk_tobject_draw_func(TLatex(0.51, 0.91, "#scale[0.5]{2.6 (e), 2.7 (#mu) fb^{-1} (13 TeV)}"))
#             ]),
#         pattern=None,
#         input_result_path='../HistoLoader/HistoLoader*',
#         # auto_legend=False,
#         # name='HistogramsPostfit',
#         # lookup_aliases=varial.settings.lookup_aliases
#         )

# def mk_histograms_no_sig(uncerts=uncerts, name='HistogramsNoSig', samples=samples_to_plot_thth):
#     return plot.mk_toolchain(name, samples,
#         plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=False, 
#             filter_keyfunc=lambda w: all(g not in w.sample for g in ['TpTp_M-1200', 'TpTp_M-1600']) and w.sys_info == '',
#             hook_loaded_histos=plot.loader_hook_merge_lep_channels,
#             mod_log=common_plot.mod_log_usr(mod_dict),
#             canvas_post_build_funcs= [
#                 common_plot.mod_pre_bot_hist(),
#                 common_plot.mk_split_err_ratio_plot_func_mod(),  # mk_pull_plot_func()
#                 # rnd.mk_split_err_ratio_plot_func(),  # mk_pull_plot_func()
#                 rnd.mk_legend_func(),
#                 common_plot.mod_post_canv(mod_dict),
#                 common_plot.mk_tobject_draw_func(TLatex(0.51, 0.91, "#scale[0.5]{2.6 (e), 2.7 (#mu) fb^{-1} (13 TeV)}"))
#             ]),
#         pattern=None,
#         input_result_path='../HistoLoader/HistoLoader*',
#         # parallel=False
#         # auto_legend=False,
#         # name='HistogramsPostfit',
#         # lookup_aliases=varial.settings.lookup_aliases
#         )




normfactors_singlet = {
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

normfactors_th100 = {
    '_thth' : 1./0.111,
    '_tztz' : 0./0.111,
    '_bwbw' : 0./0.111,
    '_thtz' : 0./0.222,
    '_thbw' : 0./0.222,
    '_tzbw' : 0./0.222,
    '_bhbh' : 0./0.111,
    '_bzbz' : 0./0.111,
    '_twtw' : 0./0.111,
    '_bhbz' : 0./0.222,
    '_bhtw' : 0./0.222,
    '_bztw' : 0./0.222,
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

def merge_sig_data(wrps, print_warning=True):
    """histos must be sorted!!"""

    def do_merging(buf):
        if len(buf) > 2:
            raise RuntimeError('ERROR Need exactly two histograms (data+signal) to merge.')

        # buf = sorted(buf, key=lambda w: w.is_signal)
        res = varial.operations.merge(buf)
        res.file_path = ''
        # res.histo.Sumw2()
        for i in xrange(1, res.histo.GetNbinsX() + 1):
            err = math.sqrt(res.histo.GetBinContent(i))
            res.histo.SetBinError(i, err)
        del buf[:]
        return res

    buf = []
    for w in wrps:
        if w.is_data or w.is_signal:
            buf.append(w)
            if len(buf) == 2:
                yield do_merging(buf)
        else:
            if buf:
                if print_warning:
                    print 'WARNING In merge_sig_data: buffer not empty.\n' \
                          'Flushing remaining items:\n' + ' | '.join(
                        '%s, %s' % (w.sample, w.in_file_path) for w in buf
                    )
                yield do_merging(buf)
            yield w
    if buf:
        yield do_merging(buf)

def rm_ending(wrps):
    for w in wrps:
        for a in treeproject_tptp.tptp_final_states + treeproject_tptp.bpbp_final_states:
            if w.legend.endswith(a):
                w.legend = w.legend[:-len(a)]
        yield w


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

    wrps = plot.common_loader_hook(wrps)
    wrps = gen.gen_make_th2_projections(wrps)
    # wrps = gen.sort(wrps, ['sys_info', 'in_file_path', 'sample'])
    # wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_incl', print_warning=False, yield_orig=True)
    # wrps = list(wrps)
    # wrps = common_plot.norm_smpl(wrps, normfactors_ind_fs, calc_scl_fct=False, mark_scaled='br_scaled')
    # wrps = common_plot.mod_legend_eff_counts(wrps)
    wrps = sorted(wrps, key=key)
    wrps = varial.gen.group(wrps, key)
    wrps = varial.gen.gen_merge(wrps)
    wrps = varial.gen.gen_add_wrp_info(wrps, in_file_path=get_new_infile_path, region=get_base_selection, sys_info=get_sys_info)
    # wrps = list(wrps)
    # for w in wrps:
        # if w.sys_info.startswith('sfel') or w.sys_info.startswith('sfmu'):
            # print get_base_selection(w), w.sample, w.sys_info, w.variable
    return wrps

def loader_hook_toy_data(wrps):
                  
    def get_sample(wrp):
        name = os.path.basename(wrp.file_path)
        name = os.path.splitext(name)[0]
        name = name.split('__')[1]
        return name

    def get_in_file_path(wrp):
        path = os.path.basename(wrp.in_file_path)
        path = path.split('__')[0]+'/HT'
        return path

    def get_region(wrp):
        path = os.path.basename(wrp.in_file_path)
        path = path.split('__')[0]
        return path

    def mk_ht_rebin_hist(wrps):
        for w in wrps:
            r_list = array.array('d', rebin_list)
            ht = TH1F('HT_rebin_flex', 'HT_rebin_flex', 65, 0., 6500.)
            ht_rebin = ht.Rebin(
                len(r_list) - 1,
                'HT_rebin_flex',
                r_list
            )
            for i in xrange(w.histo.GetNbinsX()+2):
                if w.histo.GetBinContent(i):
                    print w.histo.GetBinContent(i)
                    ht_rebin.SetBinContent(i, w.histo.GetBinContent(i))
            w.histo = ht_rebin
            w.name = 'HT_rebin_flex'
            w.in_file_path += '_rebin_flex'
            yield w

    # wrps = common_plot.mod_legend(wrps)
    wrps = common_plot.add_wrp_info(wrps)
    wrps = (w for w in wrps if w.histo.Integral() > 1e-20)
    wrps = vlq_common.label_axes(wrps)
    wrps = common_plot.mod_title(wrps)
    # wrps = gen.sort(wrps, ['sys_info', 'in_file_path', 'sample'])
    # wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw'], suffix='_incl', print_warning=False, yield_orig=True)
    # wrps = list(wrps)
    # wrps = common_plot.norm_smpl(wrps, normfactors_ind_fs, calc_scl_fct=False, mark_scaled='br_scaled')
    # wrps = common_plot.mod_legend_eff_counts(wrps)
    wrps = varial.gen.gen_add_wrp_info(wrps,
        is_data=lambda _: True,
        sample=lambda _: 'Data',
        name=lambda _: 'HT',
        region=get_region,
        in_file_path=get_in_file_path)
    wrps = mk_ht_rebin_hist(wrps)
    # wrps = list(wrps)
    # for w in wrps:
        # if w.sys_info.startswith('sfel') or w.sys_info.startswith('sfmu'):
            # print get_base_selection(w), w.sample, w.sys_info, w.variable
    return wrps

def loader_hook_merge_sig_data(wrps, normfactors, do_merging=False):
    def sort_signal_data(wrp):
        if wrp.is_data:
            return '0'
        elif wrp.is_signal:
            return '1'
        else:
            return '2'

    wrps = common_plot.mod_title(wrps)
    # wrps = common_plot.mod_legend_no_thth(wrps)
    wrps = common_plot.norm_smpl(wrps, normfactors, calc_scl_fct=False, mark_scaled='br_scaled')
    if do_merging:
        wrps = sorted(wrps, key=lambda w: '{0}___{1}___{2}'.format(w.sys_info, w.in_file_path, w.sample))
        wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw'], print_warning=False, yield_orig=False)
        wrps = sorted(wrps, key=lambda w: '{0}___{1}___{2}'.format(w.sys_info, w.in_file_path, w.sample))
        wrps = vlq_common.merge_decay_channels(wrps, ['_bhbh', '_bhbz', '_bhtw', '_noH_bzbz', '_noH_bztw', '_noH_twtw'], print_warning=False, yield_orig=False)
    wrps = rm_ending(wrps)
    wrps = sorted(wrps, key=lambda w: w.in_file_path+'___'+w.name+'___'+sort_signal_data(w))
    wrps = merge_sig_data(wrps, False)
    wrps = common_plot.rebin_st_and_nak4(wrps)
    wrps = sorted(wrps, key=lambda w: w.region+'___'+w.name)
    return wrps

def loader_hook_nominal_brs(wrps, normfactors, do_merging=False):
    wrps = plot.common_loader_hook(wrps)
    wrps = common_plot.mod_title(wrps)
    wrps = common_plot.rebin_st_and_nak4(wrps)
    # wrps = common_plot.norm_smpl(wrps, normfactors_ind_fs, calc_scl_fct=False, mark_scaled='br_scaled')
    wrps = common_plot.norm_smpl(wrps, normfactors, calc_scl_fct=False, mark_scaled='br_scaled')
    if do_merging:
        wrps = sorted(wrps, key=lambda w: '{0}___{1}___{2}'.format(w.sys_info, w.in_file_path, w.sample))
        wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw'], print_warning=False, yield_orig=False)
        wrps = sorted(wrps, key=lambda w: '{0}___{1}___{2}'.format(w.sys_info, w.in_file_path, w.sample))
        wrps = vlq_common.merge_decay_channels(wrps, ['_bhbh', '_bhbz', '_bhtw', '_noH_bzbz', '_noH_bztw', '_noH_twtw'], print_warning=False, yield_orig=False)
    wrps = rm_ending(wrps)
    # wrps = set_line_style(wrps)
    # wrps = rename_samples(wrps)
    # wrps = sorted(wrps, key=lambda w: w.in_file_path+'___'+w.sys_info+'___'+w.sample)
    # wrps = vlq_common.merge_decay_channels(wrps, postfixes=['__TTbar', '__TTbar_split', '__SingleTop'], print_warning=False)
    # wrps = vlq_common.merge_decay_channels(wrps, postfixes=['__WJets', '__DYJets', '__Diboson'], print_warning=False)
    # wrps = remove_final_states(wrps)
    # wrps = common_plot.norm_smpl(wrps, {'_thth' : 1./0.0625}, calc_scl_fct=False, mark_scaled='br_scaled')
    # wrps = common_plot.mod_legend_no_thth(wrps)
    wrps = sorted(wrps, key=lambda w: w.region+'__'+w.name)
    return wrps


def loader_hook_nominal_brs_no_rebin(wrps, normfactors, do_merging=False):
    wrps = list(wrps)
    wrps = plot.common_loader_hook(wrps)
    wrps = common_plot.mod_title(wrps)
    # wrps = common_plot.rebin_st_and_nak4(wrps)
    # wrps = common_plot.norm_smpl(wrps, normfactors_ind_fs, calc_scl_fct=False, mark_scaled='br_scaled')
    wrps = common_plot.norm_smpl(wrps, normfactors, calc_scl_fct=False, mark_scaled='br_scaled')
    if do_merging:
        wrps = sorted(wrps, key=lambda w: '{0}___{1}___{2}'.format(w.sys_info, w.in_file_path, w.sample))
        wrps = vlq_common.merge_decay_channels(wrps, ['_thth', '_thtz', '_thbw', '_noH_tztz', '_noH_tzbw', '_noH_bwbw'], print_warning=False, yield_orig=False)
        wrps = sorted(wrps, key=lambda w: '{0}___{1}___{2}'.format(w.sys_info, w.in_file_path, w.sample))
        wrps = vlq_common.merge_decay_channels(wrps, ['_bhbh', '_bhbz', '_bhtw', '_noH_bzbz', '_noH_bztw', '_noH_twtw'], print_warning=False, yield_orig=False)
    wrps = rm_ending(wrps)
    # wrps = set_line_style(wrps)
    # wrps = rename_samples(wrps)
    # wrps = sorted(wrps, key=lambda w: w.in_file_path+'___'+w.sys_info+'___'+w.sample)
    # wrps = vlq_common.merge_decay_channels(wrps, postfixes=['__TTbar', '__TTbar_split', '__SingleTop'], print_warning=False)
    # wrps = vlq_common.merge_decay_channels(wrps, postfixes=['__WJets', '__DYJets', '__Diboson'], print_warning=False)
    # wrps = remove_final_states(wrps)
    # wrps = common_plot.norm_smpl(wrps, {'_thth' : 1./0.0625}, calc_scl_fct=False, mark_scaled='br_scaled')
    # wrps = common_plot.mod_legend_no_thth(wrps)
    wrps = sorted(wrps, key=lambda w: w.region+'__'+w.name)
    return wrps


def mk_histograms_sig_inj(name, excl_signal, samples, normfactors, do_merging):
    return varial.tools.ToolChain(name, [
        plot.mk_toolchain('HistogramNoFit', samples,
            plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, include_rate=False,
                # filter_keyfunc=lambda w: not w.sys_info and not w.is_data,
                # hook_loaded_histos=loader_hook_nominal_brs,
                hook_loaded_histos=lambda w: loader_hook_nominal_brs(w, normfactors, do_merging),
                stack_setup=lambda w: gen.mc_stack_n_data_sum(w, calc_sys_integral=True, add_sys_errs=True),
                plot_setup=lambda w: gen.mc_stack_n_data_sum(w, calc_sys_integral=True, add_sys_errs=True),
                # mod_log=common_plot.mod_log_usr(mod_dict),
                canvas_post_build_funcs=get_style()
                ),
            pattern=None,
            input_result_path='../../HistoLoader/HistoLoader*',
            # auto_legend=False,
            # name='HistogramsPostfit',
            # lookup_aliases=varial.settings.lookup_aliases
            ),
        plot.mk_toolchain('HistogramFit', samples,
            plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=False, 
                filter_keyfunc=lambda w: all(g not in w.sample for g in excl_signal) and w.sys_info == '',
                hook_loaded_histos=lambda w: loader_hook_merge_sig_data(w, normfactors, do_merging),
                mod_log=common_plot.mod_log_usr(mod_dict), # mod_dict
                canvas_post_build_funcs= get_style() + [common_plot.mk_fit_bottom_plot()]),
            pattern=None,
            input_result_path='../../HistoLoader/HistoLoader*',
            # parallel=False
            # auto_legend=False,
            # name='HistogramsPostfit',
            # lookup_aliases=varial.settings.lookup_aliases
            ),
        ]
    )

def plot_merged_channels_prefit_norew(final_dir, input_pat, samples, normfactors=normfactors_th100, do_merging=False):

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

    return varial.tools.ToolChain(final_dir, [
        varial.tools.ToolChainParallel('HistoLoader',
            list(varial.tools.HistoLoader(
                pattern=map(lambda w: w.format('*'+g+'*'), input_pat),
                # pattern=map(lambda w: w.format('*'+g+'*'), input_pat),
                filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in samples) and\
                    'Region_Comb' not in w.in_file_path and\
                    any(w.in_file_path.endswith(f) for f in plot_hists),
                hook_loaded_histos=loader_hook_merge_regions,
                name='HistoLoader_'+g,
                lookup_aliases=False,
                raise_on_empty_result=False,
                quiet_mode=True
                ) for g in samples)),
        plot.mk_toolchain('HistogramsPrefit', samples,
            plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, include_rate=False,
                # filter_keyfunc=lambda w: not w.sys_info and not w.is_data,
                # hook_loaded_histos=loader_hook_nominal_brs,
                hook_loaded_histos=lambda w: loader_hook_nominal_brs(w, normfactors, do_merging),
                stack_setup=lambda w: gen.mc_stack_n_data_sum(w, calc_sys_integral=True, add_sys_errs=True),
                plot_setup=lambda w: gen.mc_stack_n_data_sum(w, calc_sys_integral=True, add_sys_errs=True),
                # mod_log=common_plot.mod_log_usr(mod_dict),
                canvas_post_build_funcs=get_style()
                ),
            pattern=None,
            input_result_path='../HistoLoader/HistoLoader*',
            # auto_legend=False,
            # name='HistogramsPostfit',
            # lookup_aliases=varial.settings.lookup_aliases
            ),
        plot.mk_toolchain('HistogramsPrefitNoSysFit', samples,
            plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, include_rate=False,
                filter_keyfunc=lambda w: not w.is_signal and not w.sys_info and 'HT' in w.name,
                # hook_loaded_histos=loader_hook_nominal_brs,
                hook_loaded_histos=lambda w: loader_hook_nominal_brs(w, normfactors, do_merging),
                stack_setup=lambda w: gen.mc_stack_n_data_sum(w, calc_sys_integral=True, add_sys_errs=True),
                plot_setup=lambda w: gen.mc_stack_n_data_sum(w, calc_sys_integral=True, add_sys_errs=True),
                # stack_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, include_rate=False),
                # plot_setup=lambda w: stack_setup(w, analysis.rate_uncertainties, include_rate=False),
                # mod_log=common_plot.mod_log_usr(plot_thesis.mod_dict),
                canvas_post_build_funcs=get_style() + [common_plot.mk_fit_bottom_plot()]
                ),
            pattern=None,
            input_result_path='../HistoLoader/HistoLoader*',
            # parallel=False
            # auto_legend=False,
            # name='HistogramsPostfit',
            # lookup_aliases=varial.settings.lookup_aliases
            ),
        mk_histograms_sig_inj('HistogramsSigInj0800', ['BpBp_M-1200', 'BpBp_M-1600','TpTp_M-1200', 'TpTp_M-1600'], samples, normfactors, do_merging),
        mk_histograms_sig_inj('HistogramsSigInj1200', ['BpBp_M-0800', 'BpBp_M-1600','TpTp_M-0800', 'TpTp_M-1600'], samples, normfactors, do_merging),
        mk_histograms_sig_inj('HistogramsSigInj1600', ['BpBp_M-0800', 'BpBp_M-1200','TpTp_M-0800', 'TpTp_M-1200'], samples, normfactors, do_merging),

        # varial.tools.ToolChain('SigInjToyBootstrap', [
        #     MakeSigInjRootFile(
        #         input_path='../../HistoLoader/HistoLoader*',
        #         filter_keyfunc=lambda w: 'HT' in w.name, # and all(a not in w.sample for a in ['TpTp_M-1200', 'TpTp_M-1600']),
        #         normfactors=normfactors_th100,
        #         cat_key=lambda w: w.category,  # lambda w: w.category,
        #         theta_root_file_name=None,
        #         toys_param='toys-asimov:1.0',
        #         name='HistogramsSigInjToy'),
        #     varial.tools.ToolChainParallel('HistoLoader',
        #         list(varial.tools.HistoLoader(
        #             pattern=map(lambda w: '../' + w.format('*'+g+'*'), input_pat),
        #             # pattern=map(lambda w: w.format('*'+g+'*'), input_pat),
        #             filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in samples) and\
        #                 'Run2015' not in w.file_path and\
        #                 w.in_file_path.endswith('HT'),
        #             hook_loaded_histos=lambda w: common_plot.rebin_st_and_nak4(loader_hook_merge_regions(w)),
        #             name='HistoLoader_'+g,
        #             lookup_aliases=False,
        #             raise_on_empty_result=False,
        #             quiet_mode=True
        #             ) for g in samples) +\
        #         [
        #             varial.tools.HistoLoader(
        #                 pattern='../../HistogramsSigInjToy/ToyHisto*.root',
        #                 # pattern=map(lambda w: w.format('*'+g+'*'), input_pat),
        #                 # filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in samples) and\
        #                 #     'Run2015' not in w.file_path and\
        #                 #     w.in_file_path.endswith('HT'),
        #                 hook_loaded_histos=loader_hook_toy_data,
        #                 name='HistoLoader_ToyData',
        #                 lookup_aliases=False,
        #                 raise_on_empty_result=False,
        #                 quiet_mode=True
        #                 )
        #         ]
        #         ),
        #     plot.mk_toolchain('HistogramsTT800Inj', samples,
        #         plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, include_rate=False,
        #             filter_keyfunc=lambda w: all(a not in w.file_path for a in ['TpTp_M-1200', 'TpTp_M-1600']),
        #             # hook_loaded_histos=loader_hook_nominal_brs,
        #             hook_loaded_histos=lambda w: loader_hook_nominal_brs_no_rebin(w, normfactors, do_merging),
        #             stack_setup=lambda w: gen.mc_stack_n_data_sum(w, calc_sys_integral=True, add_sys_errs=True),
        #             plot_setup=lambda w: gen.mc_stack_n_data_sum(w, calc_sys_integral=True, add_sys_errs=True),
        #             # mod_log=common_plot.mod_log_usr(mod_dict),
        #             canvas_post_build_funcs=get_style()
        #             ),
        #         pattern=None,
        #         input_result_path='../HistoLoader/HistoLoader*',
        #         # auto_legend=False,
        #         # name='HistogramsPostfit',
        #         # lookup_aliases=varial.settings.lookup_aliases
        #         ),
        #     plot.mk_toolchain('HistogramsTT1600Inj', samples,
        #         plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, include_rate=False,
        #             filter_keyfunc=lambda w: all(a not in w.file_path for a in ['TpTp_M-0800', 'TpTp_M-1200']),
        #             # hook_loaded_histos=loader_hook_nominal_brs_no_rebin,
        #             hook_loaded_histos=lambda w: loader_hook_nominal_brs_no_rebin(w, normfactors, do_merging),
        #             stack_setup=lambda w: gen.mc_stack_n_data_sum(w, calc_sys_integral=True, add_sys_errs=True),
        #             plot_setup=lambda w: gen.mc_stack_n_data_sum(w, calc_sys_integral=True, add_sys_errs=True),
        #             # mod_log=common_plot.mod_log_usr(mod_dict),
        #             canvas_post_build_funcs=get_style()
        #             ),
        #         pattern=None,
        #         input_result_path='../HistoLoader/HistoLoader*',
        #         # auto_legend=False,
        #         # name='HistogramsPostfit',
        #         # lookup_aliases=varial.settings.lookup_aliases
        #         ),
        # ]),

        # varial.tools.ToolChain('SigInjToyDataDirect', [
        #     MakeSigInjRootFile(
        #         input_path='../../HistoLoader/HistoLoader*',
        #         filter_keyfunc=lambda w: not w.is_background and 'HT' in w.name, # and all(a not in w.sample for a in ['TpTp_M-1200', 'TpTp_M-1600']),
        #         normfactors=normfactors_th100,
        #         dat_key=lambda _: False,
        #         bkg_key=lambda w: w.is_data,
        #         cat_key=lambda w: w.category,  # lambda w: w.category,
        #         theta_root_file_name=None,
        #         toys_param='toys-asimov:1.0',
        #         bootstrapped=False,
        #         name='HistogramsSigInjToy'),
        #     varial.tools.ToolChainParallel('HistoLoader',
        #         list(varial.tools.HistoLoader(
        #             pattern=map(lambda w: '../' + w.format('*'+g+'*'), input_pat),
        #             # pattern=map(lambda w: w.format('*'+g+'*'), input_pat),
        #             filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in samples) and\
        #                 'Run2015' not in w.file_path and\
        #                 w.in_file_path.endswith('HT'),
        #             hook_loaded_histos=lambda w: common_plot.rebin_st_and_nak4(loader_hook_merge_regions(w)),
        #             name='HistoLoader_'+g,
        #             lookup_aliases=False,
        #             raise_on_empty_result=False,
        #             quiet_mode=True
        #             ) for g in samples) +\
        #         [
        #             varial.tools.HistoLoader(
        #                 pattern='../../HistogramsSigInjToy/ToyHisto*.root',
        #                 # pattern=map(lambda w: w.format('*'+g+'*'), input_pat),
        #                 # filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in samples) and\
        #                 #     'Run2015' not in w.file_path and\
        #                 #     w.in_file_path.endswith('HT'),
        #                 hook_loaded_histos=loader_hook_toy_data,
        #                 name='HistoLoader_ToyData',
        #                 lookup_aliases=False,
        #                 raise_on_empty_result=False,
        #                 quiet_mode=True
        #                 )
        #         ]
        #         ),
        #     plot.mk_toolchain('HistogramsTT800Inj', samples,
        #         plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, include_rate=False,
        #             filter_keyfunc=lambda w: all(a not in w.file_path for a in ['TpTp_M-1200', 'TpTp_M-1600']),
        #             # hook_loaded_histos=loader_hook_nominal_brs_no_rebin,
        #             hook_loaded_histos=lambda w: loader_hook_nominal_brs_no_rebin(w, normfactors, do_merging),
        #             stack_setup=lambda w: gen.mc_stack_n_data_sum(w, calc_sys_integral=True, add_sys_errs=True),
        #             plot_setup=lambda w: gen.mc_stack_n_data_sum(w, calc_sys_integral=True, add_sys_errs=True),
        #             # mod_log=common_plot.mod_log_usr(mod_dict),
        #             canvas_post_build_funcs=get_style()
        #             ),
        #         pattern=None,
        #         input_result_path='../HistoLoader/HistoLoader*',
        #         # auto_legend=False,
        #         # name='HistogramsPostfit',
        #         # lookup_aliases=varial.settings.lookup_aliases
        #         ),
        #     plot.mk_toolchain('HistogramsTT1600Inj', samples,
        #         plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, include_rate=False,
        #             filter_keyfunc=lambda w: all(a not in w.file_path for a in ['TpTp_M-0800', 'TpTp_M-1200']),
        #             # hook_loaded_histos=loader_hook_nominal_brs_no_rebin,
        #             hook_loaded_histos=lambda w: loader_hook_nominal_brs_no_rebin(w, normfactors, do_merging),
        #             stack_setup=lambda w: gen.mc_stack_n_data_sum(w, calc_sys_integral=True, add_sys_errs=True),
        #             plot_setup=lambda w: gen.mc_stack_n_data_sum(w, calc_sys_integral=True, add_sys_errs=True),
        #             # mod_log=common_plot.mod_log_usr(mod_dict),
        #             canvas_post_build_funcs=get_style()
        #             ),
        #         pattern=None,
        #         input_result_path='../HistoLoader/HistoLoader*',
        #         # auto_legend=False,
        #         # name='HistogramsPostfit',
        #         # lookup_aliases=varial.settings.lookup_aliases
        #         ),
        # ]),
        # varial.tools.ToolChain('SigInjToyBootstrapNoInj', [
        #     MakeSigInjRootFile(
        #         input_path='../../HistoLoader/HistoLoader*',
        #         filter_keyfunc=lambda w: 'HT' in w.name, # and all(a not in w.sample for a in ['TpTp_M-1200', 'TpTp_M-1600']),
        #         normfactors=normfactors_th100,
        #         toys_param='toys:0.0',
        #         cat_key=lambda w: w.category,  # lambda w: w.category,
        #         theta_root_file_name=None,
        #         name='HistogramsSigInjToy'),
        #     varial.tools.ToolChainParallel('HistoLoader',
        #         list(varial.tools.HistoLoader(
        #             pattern=map(lambda w: '../' + w.format('*'+g+'*'), input_pat),
        #             # pattern=map(lambda w: w.format('*'+g+'*'), input_pat),
        #             filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in samples) and\
        #                 'Run2015' not in w.file_path and\
        #                 w.in_file_path.endswith('HT'),
        #             hook_loaded_histos=lambda w: common_plot.rebin_st_and_nak4(loader_hook_merge_regions(w)),
        #             name='HistoLoader_'+g,
        #             lookup_aliases=False,
        #             raise_on_empty_result=False,
        #             quiet_mode=True
        #             ) for g in samples) +\
        #         [
        #             varial.tools.HistoLoader(
        #                 pattern='../../HistogramsSigInjToy/ToyHisto*.root',
        #                 # pattern=map(lambda w: w.format('*'+g+'*'), input_pat),
        #                 # filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in samples) and\
        #                 #     'Run2015' not in w.file_path and\
        #                 #     w.in_file_path.endswith('HT'),
        #                 hook_loaded_histos=loader_hook_toy_data,
        #                 name='HistoLoader_ToyData',
        #                 lookup_aliases=False,
        #                 raise_on_empty_result=False,
        #                 quiet_mode=True
        #                 )
        #         ]
        #         ),
        #     plot.mk_toolchain('HistogramsTT800Inj', samples,
        #         plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, include_rate=False,
        #             filter_keyfunc=lambda w: all(a not in w.file_path for a in ['TpTp_M-1200', 'TpTp_M-1600']),
        #             # hook_loaded_histos=loader_hook_nominal_brs_no_rebin,
        #             hook_loaded_histos=lambda w: loader_hook_nominal_brs_no_rebin(w, normfactors, do_merging),
        #             stack_setup=lambda w: gen.mc_stack_n_data_sum(w, calc_sys_integral=True, add_sys_errs=True),
        #             plot_setup=lambda w: gen.mc_stack_n_data_sum(w, calc_sys_integral=True, add_sys_errs=True),
        #             # mod_log=common_plot.mod_log_usr(mod_dict),
        #             canvas_post_build_funcs=get_style()
        #             ),
        #         pattern=None,
        #         input_result_path='../HistoLoader/HistoLoader*',
        #         # auto_legend=False,
        #         # name='HistogramsPostfit',
        #         # lookup_aliases=varial.settings.lookup_aliases
        #         ),
        #     plot.mk_toolchain('HistogramsTT1600Inj', samples,
        #         plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, include_rate=False,
        #             filter_keyfunc=lambda w: all(a not in w.file_path for a in ['TpTp_M-0800', 'TpTp_M-1200']),
        #             # hook_loaded_histos=loader_hook_nominal_brs_no_rebin,
        #             hook_loaded_histos=lambda w: loader_hook_nominal_brs_no_rebin(w, normfactors, do_merging),
        #             stack_setup=lambda w: gen.mc_stack_n_data_sum(w, calc_sys_integral=True, add_sys_errs=True),
        #             plot_setup=lambda w: gen.mc_stack_n_data_sum(w, calc_sys_integral=True, add_sys_errs=True),
        #             # mod_log=common_plot.mod_log_usr(mod_dict),
        #             canvas_post_build_funcs=get_style()
        #             ),
        #         pattern=None,
        #         input_result_path='../HistoLoader/HistoLoader*',
        #         # auto_legend=False,
        #         # name='HistogramsPostfit',
        #         # lookup_aliases=varial.settings.lookup_aliases
        #         ),
        # ]),

        # varial.tools.ToolChain('SigInjToyDataDirectNoInj', [
        #     MakeSigInjRootFile(
        #         input_path='../../HistoLoader/HistoLoader*',
        #         filter_keyfunc=lambda w: not w.is_background and 'HT' in w.name, # and all(a not in w.sample for a in ['TpTp_M-1200', 'TpTp_M-1600']),
        #         normfactors=normfactors_th100,
        #         toys_param='toys:0.0',
        #         dat_key=lambda _: False,
        #         bkg_key=lambda w: w.is_data,
        #         cat_key=lambda w: w.category,  # lambda w: w.category,
        #         theta_root_file_name=None,
        #         bootstrapped=False,
        #         name='HistogramsSigInjToy'),
        #     varial.tools.ToolChainParallel('HistoLoader',
        #         list(varial.tools.HistoLoader(
        #             pattern=map(lambda w: '../' + w.format('*'+g+'*'), input_pat),
        #             # pattern=map(lambda w: w.format('*'+g+'*'), input_pat),
        #             filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in samples) and\
        #                 'Run2015' not in w.file_path and\
        #                 w.in_file_path.endswith('HT'),
        #             hook_loaded_histos=lambda w: common_plot.rebin_st_and_nak4(loader_hook_merge_regions(w)),
        #             name='HistoLoader_'+g,
        #             lookup_aliases=False,
        #             raise_on_empty_result=False,
        #             quiet_mode=True
        #             ) for g in samples) +\
        #         [
        #             varial.tools.HistoLoader(
        #                 pattern='../../HistogramsSigInjToy/ToyHisto*.root',
        #                 # pattern=map(lambda w: w.format('*'+g+'*'), input_pat),
        #                 # filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in samples) and\
        #                 #     'Run2015' not in w.file_path and\
        #                 #     w.in_file_path.endswith('HT'),
        #                 hook_loaded_histos=loader_hook_toy_data,
        #                 name='HistoLoader_ToyData',
        #                 lookup_aliases=False,
        #                 raise_on_empty_result=False,
        #                 quiet_mode=True
        #                 )
        #         ]
        #         ),
        #     plot.mk_toolchain('HistogramsTT800Inj', samples,
        #         plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, include_rate=False,
        #             filter_keyfunc=lambda w: all(a not in w.file_path for a in ['TpTp_M-1200', 'TpTp_M-1600']),
        #             # hook_loaded_histos=loader_hook_nominal_brs_no_rebin,
        #             hook_loaded_histos=lambda w: loader_hook_nominal_brs_no_rebin(w, normfactors, do_merging),
        #             stack_setup=lambda w: gen.mc_stack_n_data_sum(w, calc_sys_integral=True, add_sys_errs=True),
        #             plot_setup=lambda w: gen.mc_stack_n_data_sum(w, calc_sys_integral=True, add_sys_errs=True),
        #             # mod_log=common_plot.mod_log_usr(mod_dict),
        #             canvas_post_build_funcs=get_style()
        #             ),
        #         pattern=None,
        #         input_result_path='../HistoLoader/HistoLoader*',
        #         # auto_legend=False,
        #         # name='HistogramsPostfit',
        #         # lookup_aliases=varial.settings.lookup_aliases
        #         ),
        #     plot.mk_toolchain('HistogramsTT1600Inj', samples,
        #         plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, include_rate=False,
        #             filter_keyfunc=lambda w: all(a not in w.file_path for a in ['TpTp_M-0800', 'TpTp_M-1200']),
        #             # hook_loaded_histos=loader_hook_nominal_brs_no_rebin,
        #             hook_loaded_histos=lambda w: loader_hook_nominal_brs_no_rebin(w, normfactors, do_merging),
        #             stack_setup=lambda w: gen.mc_stack_n_data_sum(w, calc_sys_integral=True, add_sys_errs=True),
        #             plot_setup=lambda w: gen.mc_stack_n_data_sum(w, calc_sys_integral=True, add_sys_errs=True),
        #             # mod_log=common_plot.mod_log_usr(mod_dict),
        #             canvas_post_build_funcs=get_style()
        #             ),
        #         pattern=None,
        #         input_result_path='../HistoLoader/HistoLoader*',
        #         # auto_legend=False,
        #         # name='HistogramsPostfit',
        #         # lookup_aliases=varial.settings.lookup_aliases
        #         ),
        # ]),
        varial.tools.WebCreator()
        ])


# samples_to_plot_tt = hists_to_plot + list(g + '_thth' for g in plot.less_signals) + list(g + '_noH_bwbw' for g in plot.less_signals)

def mk_tc_tex(base_dir):
    tc_tex = [
        tex_content.mk_plot_ind(
            (
                ('sig_inj_fit_tt_th_0800', '../../../HistogramsTTMergedOnlyTH/HistogramsSigInj0800/HistogramFit/StackedAll/SidebandTTJetsRegion/HT_rebin_flex_log.pdf'),
                ('sig_inj_fit_tt_th_1200', '../../../HistogramsTTMergedOnlyTH/HistogramsSigInj1200/HistogramFit/StackedAll/SidebandTTJetsRegion/HT_rebin_flex_log.pdf'),
                ('sig_inj_fit_tt_th_1600', '../../../HistogramsTTMergedOnlyTH/HistogramsSigInj1600/HistogramFit/StackedAll/SidebandTTJetsRegion/HT_rebin_flex_log.pdf'),
                ('sig_inj_fit_tt_bw_0800', '../../../HistogramsTTMergedOnlyBW/HistogramsSigInj0800/HistogramFit/StackedAll/SidebandTTJetsRegion/HT_rebin_flex_log.pdf'),
                ('sig_inj_fit_tt_bw_1200', '../../../HistogramsTTMergedOnlyBW/HistogramsSigInj1200/HistogramFit/StackedAll/SidebandTTJetsRegion/HT_rebin_flex_log.pdf'),
                ('sig_inj_fit_tt_bw_1600', '../../../HistogramsTTMergedOnlyBW/HistogramsSigInj1600/HistogramFit/StackedAll/SidebandTTJetsRegion/HT_rebin_flex_log.pdf'),
                ('sig_inj_fit_bb_tw_1200', '../../../HistogramsBBMergedOnlyTW/HistogramsSigInj1200/HistogramFit/StackedAll/SidebandTTJetsRegion/HT_rebin_flex_log.pdf'),
                ('sig_inj_fit_bb_tw_0800', '../../../HistogramsBBMergedOnlyTW/HistogramsSigInj0800/HistogramFit/StackedAll/SidebandTTJetsRegion/HT_rebin_flex_log.pdf'),
                ('sig_inj_fit_bb_tw_1600', '../../../HistogramsBBMergedOnlyTW/HistogramsSigInj1600/HistogramFit/StackedAll/SidebandTTJetsRegion/HT_rebin_flex_log.pdf'),
                ('sig_inj_fit_tt_singlet_0800', '../../../HistogramsTTMergedSinglet/HistogramsSigInj0800/HistogramFit/StackedAll/SidebandTTJetsRegion/HT_rebin_flex_log.pdf'),
                ('sig_inj_fit_tt_doublet_0800', '../../../HistogramsTTMergedDoublet/HistogramsSigInj0800/HistogramFit/StackedAll/SidebandTTJetsRegion/HT_rebin_flex_log.pdf'),
                ('sig_inj_fit_tt_singlet_1200', '../../../HistogramsTTMergedSinglet/HistogramsSigInj1200/HistogramFit/StackedAll/SidebandTTJetsRegion/HT_rebin_flex_log.pdf'),
                ('sig_inj_fit_tt_doublet_1200', '../../../HistogramsTTMergedDoublet/HistogramsSigInj1200/HistogramFit/StackedAll/SidebandTTJetsRegion/HT_rebin_flex_log.pdf'),
                ('sig_inj_fit_tt_singlet_1600', '../../../HistogramsTTMergedSinglet/HistogramsSigInj1600/HistogramFit/StackedAll/SidebandTTJetsRegion/HT_rebin_flex_log.pdf'),
                ('sig_inj_fit_tt_doublet_1600', '../../../HistogramsTTMergedDoublet/HistogramsSigInj1600/HistogramFit/StackedAll/SidebandTTJetsRegion/HT_rebin_flex_log.pdf'),
                ('st_sr_sig_inj_fit_tt_th_0800', '../../../HistogramsTTMergedOnlyTH/HistogramsSigInj0800/HistogramNoFit/StackedAll/SignalRegion2b/ST_rebin_flex_log.pdf'),
                ('st_sr_sig_inj_fit_tt_th_1200', '../../../HistogramsTTMergedOnlyTH/HistogramsSigInj1200/HistogramNoFit/StackedAll/SignalRegion2b/ST_rebin_flex_log.pdf'),
                ('st_sr_sig_inj_fit_tt_th_1600', '../../../HistogramsTTMergedOnlyTH/HistogramsSigInj1600/HistogramNoFit/StackedAll/SignalRegion2b/ST_rebin_flex_log.pdf'),
                ('st_sr_sig_inj_fit_tt_bw_0800', '../../../HistogramsTTMergedOnlyBW/HistogramsSigInj0800/HistogramNoFit/StackedAll/SignalRegion2b/ST_rebin_flex_log.pdf'),
                ('st_sr_sig_inj_fit_tt_bw_1200', '../../../HistogramsTTMergedOnlyBW/HistogramsSigInj1200/HistogramNoFit/StackedAll/SignalRegion2b/ST_rebin_flex_log.pdf'),
                ('st_sr_sig_inj_fit_tt_bw_1600', '../../../HistogramsTTMergedOnlyBW/HistogramsSigInj1600/HistogramNoFit/StackedAll/SignalRegion2b/ST_rebin_flex_log.pdf'),
                ('st_sr_sig_inj_fit_bb_tw_1200', '../../../HistogramsBBMergedOnlyTW/HistogramsSigInj1200/HistogramNoFit/StackedAll/SignalRegion2b/ST_rebin_flex_log.pdf'),
                ('st_sr_sig_inj_fit_bb_tw_0800', '../../../HistogramsBBMergedOnlyTW/HistogramsSigInj0800/HistogramNoFit/StackedAll/SignalRegion2b/ST_rebin_flex_log.pdf'),
                ('st_sr_sig_inj_fit_bb_tw_1600', '../../../HistogramsBBMergedOnlyTW/HistogramsSigInj1600/HistogramNoFit/StackedAll/SignalRegion2b/ST_rebin_flex_log.pdf'),
                ('st_sr_sig_inj_fit_tt_singlet_0800', '../../../HistogramsTTMergedSinglet/HistogramsSigInj0800/HistogramNoFit/StackedAll/SignalRegion2b/ST_rebin_flex_log.pdf'),
                ('st_sr_sig_inj_fit_tt_doublet_0800', '../../../HistogramsTTMergedDoublet/HistogramsSigInj0800/HistogramNoFit/StackedAll/SignalRegion2b/ST_rebin_flex_log.pdf'),
                ('st_sr_sig_inj_fit_tt_singlet_1200', '../../../HistogramsTTMergedSinglet/HistogramsSigInj1200/HistogramNoFit/StackedAll/SignalRegion2b/ST_rebin_flex_log.pdf'),
                ('st_sr_sig_inj_fit_tt_doublet_1200', '../../../HistogramsTTMergedDoublet/HistogramsSigInj1200/HistogramNoFit/StackedAll/SignalRegion2b/ST_rebin_flex_log.pdf'),
                ('st_sr_sig_inj_fit_tt_singlet_1600', '../../../HistogramsTTMergedSinglet/HistogramsSigInj1600/HistogramNoFit/StackedAll/SignalRegion2b/ST_rebin_flex_log.pdf'),
                ('st_sr_sig_inj_fit_tt_doublet_1600', '../../../HistogramsTTMergedDoublet/HistogramsSigInj1600/HistogramNoFit/StackedAll/SignalRegion2b/ST_rebin_flex_log.pdf'),
            ), name='SigInjPlotsNew'
        ),
    ]
    tc_tex = varial.tools.ToolChain('CopyPlots', [
        varial.tools.ToolChain('TexThesis', tc_tex),
        varial.tools.CopyTool('/afs/desy.de/user/n/nowatsd/Documents/figures_thesis/', src='../TexThesis/*', ignore=('*.svn', '*.log'), use_rsync=True, options='-qa --delete'),
        ])
    return tc_tex


def run_treeproject_with_reweighting(final_dir, treeprojector, weight_dict=None, params=None, final_states=None):
    weights = dict(def_weights)
    if weight_dict:
        weights.update(weight_dict)
    # source_dir = os.path.join(base_path, final_dir)
    # uncerts = analysis.all_uncerts + ['sfel_trg'] # or get_sys_dir()
    nom_pattern_def_tt = ['../../TreeProject/TreeProjectorDefTT/{0}.root', '../../TreeProject/TreeProjectorDefBkg/{0}.root']
    nom_pattern_def_bb = ['../../TreeProject/TreeProjectorDefBB/{0}.root', '../../TreeProject/TreeProjectorDefBkg/{0}.root']
    # sys_pattern_def_tt = list('../../TreeProject/SysTreeProjectorsDef*/%s*/{0}.root'% i for i in uncerts)
    # input_pattern_def_tt = nom_pattern_def_tt+sys_pattern_def_tt

    nom_pattern_dr_sel = ['../../TreeProject/TreeProjectorDrSel*/{0}.root']
    sys_pattern_dr_sel = list('../../TreeProject/SysTreeProjectorsDrSel*/%s*/{0}.root'% i for i in uncerts)
    input_pattern_dr_sel = nom_pattern_dr_sel+sys_pattern_dr_sel

    normfactors_singlet = {
        '_thth' : 0.0625/0.111,
        '_noH_tztz' : 0.0625/0.111,
        '_noH_bwbw' : 0.25/0.111,
        '_thtz' : 0.125/0.222,
        '_thbw' : 0.25/0.222,
        '_noH_tzbw' : 0.25/0.222,
    }

    normfactors_doublet = {
        '_thth' : 0.25/0.111,
        '_noH_tztz' : 0.25/0.111,
        '_noH_bwbw' : 0./0.111,
        '_thtz' : 0.5/0.222,
        '_thbw' : 0./0.222,
        '_noH_tzbw' : 0./0.222,
    }

    normfactors_th100 = {
        '_thth' : 1./0.111,
        '_noH_tztz' : 0./0.111,
        '_noH_bwbw' : 0./0.111,
        '_thtz' : 0./0.222,
        '_thbw' : 0./0.222,
        '_noH_tzbw' : 0./0.222,
    }

    normfactors_bw100 = {
        '_thth' : 0./0.111,
        '_noH_tztz' : 0./0.111,
        '_noH_bwbw' : 1./0.111,
        '_thtz' : 0./0.222,
        '_thbw' : 0./0.222,
        '_noH_tzbw' : 0./0.222,
    }

    normfactors_tw100 = {
        '_bhbh' : 0./0.111,
        '_noH_bzbz' : 0./0.111,
        '_noH_twtw' : 1./0.111,
        '_bhbz' : 0./0.222,
        '_bhtw' : 0./0.222,
        '_noH_bztw' : 0./0.222,
    }

    tptp_signals = [
        'TpTp_M-0800',
        'TpTp_M-1200',
        'TpTp_M-1600',
    ]
    bpbp_signals = [
        'BpBp_M-0800',
        'BpBp_M-1200',
        'BpBp_M-1600',
    ]

    tptp_final_states = [
        '_thth',
        '_thtz',
        '_thbw',
        '_noH_tztz',
        '_noH_tzbw',
        '_noH_bwbw',
    ]

    signals_tt = reduce(lambda x, y: x+y, (list(g + f for f in tptp_final_states) for g in tptp_signals)) # treeproject_tptp.tptp_signal_samples
    signals_tt_only_th = list(g + '_thth' for g in tptp_signals) # treeproject_tptp.tptp_signal_samples
    signals_tt_only_bw = list(g + '_noH_bwbw' for g in tptp_signals) # treeproject_tptp.tptp_signal_samples
    signals_bb_only_tw = list(g + '_noH_twtw' for g in bpbp_signals) # treeproject_tptp.tptp_signal_samples

    # signals_bb = treeproject_tptp.bpbp_signal_samples
    # final_states_tt = final_states or treeproject_tptp.tptp_final_states
    # final_states_bb = treeproject_tptp.bpbp_final_states

    # plot_hists = ['ST', 'HT', 'n_ak4', 'nomass_boost_1b_mass_softdrop', 'nomass_boost_2b_mass_softdrop', 'noboost_mass_1b[0].m_pt', 'noboost_mass_2b[0].m_pt',
    #     'nobtag_boost_mass_nsjbtags', 'jets[].m_pt', 'pt_ld_ak4_jet', 'pt_subld_ak4_jet', 'jets[2].m_pt','jets[3].m_pt',
    #     'met', 'primary_lepton_pt']


    tp_chain = [
        treeproject_tptp.mk_tp(base_path+'/'+sub_path, final_regions_def, weights, samples=treeproject_tptp.bkg_w_data, treeproject=treeprojector, 
            params=params or tp_params, name='TreeProjectorDefBkg'),
        # treeproject_tptp.mk_tp(base_path+'/'+sub_path, final_regions_dr_sel, weights, samples=treeproject_tptp.bkg_w_data, treeproject=treeprojector, 
        #     params=params or tp_params, name='TreeProjectorDrSelBkg'),
        treeproject_tptp.mk_tp(base_path+'/'+sub_path, final_regions_def, weights, samples=signals_tt, treeproject=treeprojector, 
            params=params or tp_params, name='TreeProjectorDefTT'),
        treeproject_tptp.mk_tp(base_path+'/'+sub_path, final_regions_def, weights, samples=signals_bb_only_tw, treeproject=treeprojector, 
            params=params or tp_params, name='TreeProjectorDefBB'),
        # treeproject_tptp.mk_tp(base_path+'/'+sub_path, final_regions_dr_sel, weights, samples=signals_tt, treeproject=treeprojector, 
        #     params=params or tp_params, name='TreeProjectorDrSelTT'),
    ]
    # if add_uncert_func:
    #     tp_chain += [treeproject_tptp.mk_sys_tps(add_uncert_func(base_path+'/'+sub_path, final_regions_all, weights,
    #         samples=treeproject_tptp.bkg_no_data, params=params or treeproject_tptp.sys_params),
    #         name='SysTreeProjectorsBkg', treeproject=treeprojector),
    #     ]
    #     tp_chain += list(treeproject_tptp.mk_sys_tps(add_uncert_func(base_path+'/'+sub_path, final_regions_all, weights,
    #         samples=list(s + g for s in treeproject_tptp.tptp_signals), params=params or treeproject_tptp.st_only_params),
    #         name='SysTreeProjectorsTT'+g, treeproject=treeprojector) for g in final_states_tt)

    return varial.tools.ToolChain(final_dir, [
        # varial.tools.ToolChain('TreeProject',[
        varial.tools.ToolChainParallel('TreeProject', tp_chain, n_workers=2),
        plot_merged_channels_prefit_norew('HistogramsTTMergedOnlyTH', list(os.path.join('..', a) for a in nom_pattern_def_tt), treeproject_tptp.bkg_w_data + signals_tt_only_th, normfactors=normfactors_th100, do_merging=False),
        plot_merged_channels_prefit_norew('HistogramsTTMergedSinglet', list(os.path.join('..', a) for a in nom_pattern_def_tt), treeproject_tptp.bkg_w_data + signals_tt, normfactors=normfactors_singlet, do_merging=True),
        plot_merged_channels_prefit_norew('HistogramsTTMergedDoublet', list(os.path.join('..', a) for a in nom_pattern_def_tt), treeproject_tptp.bkg_w_data + signals_tt, normfactors=normfactors_doublet, do_merging=True),
        plot_merged_channels_prefit_norew('HistogramsBBMergedOnlyTW', list(os.path.join('..', a) for a in nom_pattern_def_bb), treeproject_tptp.bkg_w_data + signals_bb_only_tw, normfactors=normfactors_tw100, do_merging=False),
        plot_merged_channels_prefit_norew('HistogramsTTMergedOnlyBW', list(os.path.join('..', a) for a in nom_pattern_def_tt), treeproject_tptp.bkg_w_data + signals_tt_only_bw, normfactors=normfactors_bw100, do_merging=False),
        varial.tools.WebCreator(),
        # mk_tc_tex(final_dir),
        varial.tools.CopyTool('/afs/desy.de/user/n/nowatsd/xxl-af-cms/PlotsToInspect', src='../*', ignore=('*.svn', '*.log'), use_rsync=True, options='-qa --delete', name='CopyToolInspect'),
        # pn.mk_histoloader_merge(list('../'+ i for i in input_pattern), plot_hists),
        # pn.mk_histograms_merge(uncerts, name='HistogramsMerged'),
        ])


# sframe_tools = mk_sframe_and_plot_tools()

from varial_ext.treeprojector import TreeProjector 
import multiprocessing as mp

if __name__ == '__main__':
    time.sleep(1)
    # src_dir = sys.argv[1]
    final_dir = sys.argv[1]
    treeproject = TreeProjector
    if len(sys.argv) > 2:
        use_batch = sys.argv[2]
        if use_batch == "True":
            from varial_ext.treeprojector_spark import SparkTreeProjector 
            treeproject = SparkTreeProjector
            # job_proc = mp.Process(target=treeproject_tptp._start_job_submitter)
            # job_proc.start()

    all_tools = varial.tools.ToolChainParallel(final_dir,
        [
            # run_treeproject_with_reweighting('HTReweighting', treeproject,
            #     add_uncert_func=add_all_with_weight_uncertainties({
            #             'jsf' : {
            #                 treeproject_tptp.ttbar_smpl : ht_reweight_ttbar_no_top_pt_reweight,
            #                 'WJets' : ht_reweight_wjets_no_top_pt_reweight
            #                 }
            #             }),
            #     weight_dict={
            #         treeproject_tptp.ttbar_smpl : treeproject_tptp.base_weight+'*'+ht_reweight_ttbar_no_top_pt_reweight,
            #         'WJets' : treeproject_tptp.base_weight+'*'+ht_reweight_wjets_no_top_pt_reweight,
            #     }),
            run_treeproject_with_reweighting('SigInjTests', treeproject, params=treeproject_tptp.st_plus_ht_params),
            varial.tools.WebCreator(no_tool_check=True)
            # combination_limits.mk_limit_list('Limits')
        ], n_workers=1)
    varial.tools.Runner(all_tools, default_reuse=True)
    # varial.tools.CopyTool('~/www/vlq_analysis/tight_selection2/',
    #     src=final_dir, use_rsync=True).run()