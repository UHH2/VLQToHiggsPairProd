#!/usr/bin/env python

from varial_ext.treeprojector import TreeProjector
import varial.monitor
try:
    from varial_ext.treeprojector_spark import SparkTreeProjector 
except ImportError:
    varial.monitor.message('treeproject_tptp', 'WARNING Run "use_spark" in order to use SparkTreeProjector')
    class SparkTreeProjector: pass
from os.path import join
import varial.settings
import varial.tools
import glob
import os
import ast
# import multiprocessing as mp
import itertools

# varial.settings.max_num_processes = 24

def _start_job_submitter():
    import socket
    hostname = socket.gethostname()
    spark_url = 'spark://%s:7077' % hostname
    from varial_ext.treeprojector_spark_sge import SGESubmitter
    # import varial_ext.treeprojector as tp
    SGESubmitter(40, spark_url).start()

# treeproject = TreeProjector

# if False:
#     treeproject = BatchTreeProjector
#     job_proc = mp.Process(target=_start_job_submitter)
#     job_proc.start()

iteration = [1]

st_only = {
    'ST'                            : ('S_{T} [GeV]',                               65, 0, 6500),
}

st_plus_jets = {
    'ST'                            : ('S_{T} [GeV]',                               65, 0, 6500),
    'n_ak4'                         : ('N(Ak4 Jets)',                      20, -.5, 19.5),
    'pt_ld_ak4_jet'                 : ('p_{T} leading Ak4 Jet [GeV]',               100, 0., 2000.),
    'pt_subld_ak4_jet'              : ('p_{T} subleading Ak4 Jet [GeV]',             80, 0., 1600.),
    'HT'                            : ('H_{T} [GeV]',                               65, 0, 6500),
    'jets[].m_pt'                   : ('p_{T} Jets [GeV]',             100, 0., 2000.),
}

core_histos = {
    'ST'                            : ('S_{T} [GeV]',                               65, 0, 6500),
    'n_ak4'                         : ('N(Ak4 Jets)',                      20, -.5, 19.5),
    'n_ak8'                         : ('N(Ak8 Jets)',                      11, -.5, 10.5),
    'pt_ld_ak4_jet'                 : ('p_{T} leading Ak4 Jet [GeV]',               100, 0., 2000.),
    'jets[].m_pt'              : ('p_{T} Jets [GeV]',             100, 0., 2000.),
    'jets[2].m_pt'              : ('p_{T} third Ak4 Jet [GeV]',             50, 0., 1000.),
    'jets[3].m_pt'              : ('p_{T} fourth Ak4 Jet [GeV]',             30, 0., 600.),
    # 'pt_fourth_ak4_jet'              : ('p_{T} fourth Ak4 Jet',             30, 0., 600.),
    'pt_subld_ak4_jet'              : ('p_{T} subleading Ak4 Jet [GeV]',             80, 0., 1600.),
    'topjets[0].m_pt'                 : ('p_{T} leading Ak8 Jet [GeV]',               120, 0., 2400.),
    'topjets[1].m_pt'              : ('p_{T} subleading Ak8 Jet',             100, 0., 2000.),
    'HT'                            : ('H_{T} [GeV]',                               65, 0, 6500),
    'met'                           : ('missing E_{T} [GeV]',                              50, 0., 1000.),
    'primary_lepton_pt'             : ('Primary Lepton p_{T} [GeV]',               50, 0., 1200.),
    'n_additional_btags_medium'     : ('N(b-tags)',                             8, -.5, 7.5),
    'primary_muon_pt'               : ('Primary Muon p_{T} [GeV]',                 50, 0., 1200.),
    'primary_electron_pt'           : ('Primary Electron p_{T} [GeV]',             50, 0., 1200.),
    'PrimaryLepton.Particle.m_eta'                : ('#eta primary lepton',                  50, -3., 3.),
    'n_higgs_tags_1b_med'           : ('N(type-I Higgs-Tags)',           5, -.5, 4.5),
    'n_higgs_tags_2b_med'           : ('N(type-II Higgs-Tags)',           5, -.5, 4.5),
    'n_higgs_tags_1b_med_sm10'      : ('N(type-I Higgs-Tags)',           5, -.5, 4.5),
    'n_higgs_tags_2b_med_sm10'      : ('N(type-II Higgs-Tags)',           5, -.5, 4.5),
    'n_higgs_tags_1b_med_sm20'      : ('N(type-I Higgs-Tags)',           5, -.5, 4.5),
    'n_higgs_tags_2b_med_sm20'      : ('N(type-II Higgs-Tags)',           5, -.5, 4.5),
    'noboost_mass_1b[0].m_pt'           : ('p_{T} type-I Higgs tag mass [GeV]',           100, 0., 2000.),
    'noboost_mass_2b[0].m_pt'           : ('p_{T} type-II Higgs tag mass [GeV]',           100, 0., 2000.),
    'nomass_boost_1b_mass_softdrop'           : ('groomed type-I Higgs tag mass [GeV]',           60, 0., 300.),
    'nomass_boost_2b_mass_softdrop'           : ('groomed type-II Higgs tag mass [GeV]',           60, 0., 300.),
    'nobtag_boost_mass_nsjbtags'           : ('N(subjet b-tags)',           6, -0.5, 5.5),
    'n_prim_vertices'              : ("N(Primary Vertices)", 35, -.5, 34.5),
    'n_ak8_higgs_cand'              : ('N(Higgs Candidates)',              8, -.5, 7.5),
}

more_histos = {
    # 'ak4_jets_btagged_dR_higgs_tags_1b_med'              : ('#Delta R(AK4 b-tag, Higgs tag)',             50, 0., 5.),
    # 'gen_ht'                            : ('Gen HT',                               65, 0, 6500),
    # 'parton_ht'                            : ('Parton HT',                               65, 0, 6500),
    # 'n_ak8_cleaned_dr'              : ('N(Ak8 Jets)',                      8, -.5, 7.5),
    'gendecay_accept'               : ('GenDecay Accept',                  2, -.5, 1.5),
    # 'n_higgs_tags_1b_med_cleaned_dr': ('N(Higgs-Tags, 1 med b)',           5, -.5, 4.5),
    # 'n_higgs_tags_2b_med_cleaned_dr': ('N(Higgs-Tags, 2 med b)',           5, -.5, 4.5),
    # 'n_jets_no_overlap'             : ('N(non-overlapping Ak4 jets)',      12, -.5, 11.5),
    'n_btags_medium'     : ('N(b-tags)',                             10, -.5, 9.5),
    'trigger_accept_mu45'           : ('Trigger Accepted Mu45',             2, -.5, 1.5),
    'trigger_accept_el45'           : ('Trigger Accepted El40',             2, -.5, 1.5),
    'trigger_accept_isoMu20'          : ('Trigger Accepted IsoMu',            2, -.5, 1.5),
    'trigger_accept_isoEl27'          : ('Trigger Accepted IsoMu',            2, -.5, 1.5),
    'is_muon'                       : ('Prim. Lep. is Muon',                2, -.5, 1.5),
    'dR_ak8_higgs_cand_1_ak4_jets_btagged_cl'                : ('dR(Higgs cand., cl. AK4 b-tag)',   50, 0., 5.),
    'dR_jets_1_PrimaryLepton_cl'               : ('dR(ld. AK4 jet, primary lepton)',   50, 0., 5.),
    'dR_jets_2_PrimaryLepton_cl'           : ('dR(subld. AK4 jet, primary lepton))',   50, 0., 5.),
    'dR_higgs_tags_1b_med_1_PrimaryLepton_cl'                : ('dR(Higgs-Tag(1b), primary lepton)',   50, 0., 5.),
    'dR_higgs_tags_1b_med_1_jets_cl'               : ('dR(Higgs-Tag(1b), cl. AK4 jet)',   50, 0., 5.),
    'dR_higgs_tags_1b_med_1_topjets_cl'           : ('dR(Higgs-Tag(1b), cl. AK8 jet)',   50, 0., 5.),
    'dR_topjets_1_topjets_cl'                 : ('dR(ld. AK8 jet, cl. AK8 jet)',   50, 0., 5.),
    'dR_wtags_loose_1_leptonic_w_cl'                 : ('dR(ld. AK8 jet, cl. AK8 jet)',   50, 0., 5.),
    'dR_wtags_tight_1_leptonic_w_cl'                 : ('dR(ld. AK8 jet, cl. AK8 jet)',   50, 0., 5.),
    'dR_wtags_loose_1_leptonic_w_iso_cl'                 : ('dR(ld. AK8 jet, cl. AK8 jet)',   50, 0., 5.),
    'dR_wtags_tight_1_leptonic_w_iso_cl'                 : ('dR(ld. AK8 jet, cl. AK8 jet)',   50, 0., 5.),
    # 'ak8_boost_gen_mass'           : ('Mass [GeV]',           100, 0., 2000.),
    # 'ak8_boost_diff_before'           : ('Mass [GeV]',           100, 0., 2000.),
    # 'ak8_boost_diff_10'           : ('Mass [GeV]',           100, 0., 2000.),
    # 'ak8_boost_diff_20'           : ('Mass [GeV]',           100, 0., 2000.),
    # 'ak8_boost_diff_before_sj'           : ('Mass [GeV]',           100, 0., 2000.),
    'nomass_boost_1b_gen_mass'           : ('Mass [GeV]',           60, 0., 300.),
    'nomass_boost_1b_diff_before'           : ('Mass [GeV]',           80, -1., 1.),
    'nomass_boost_1b_diff_10'           : ('Mass [GeV]',           80, -1., 1.),
    'nomass_boost_1b_diff_20'           : ('Mass [GeV]',           80, -1., 1.),
    'nomass_boost_1b_diff_before_sj'           : ('Mass [GeV]',           80, -1., 1.),
    'nomass_boost_2b_gen_mass'           : ('Mass [GeV]',           60, 0., 300.),
    'nomass_boost_2b_diff_before'           : ('Mass [GeV]',           80, -1., 1.),
    'nomass_boost_2b_diff_10'           : ('Mass [GeV]',           80, -1., 1.),
    'nomass_boost_2b_diff_20'           : ('Mass [GeV]',           80, -1., 1.),
    'nomass_boost_2b_diff_before_sj'           : ('Mass [GeV]',           80, -1., 1.),
    'wtags_tight_mass_softdrop'           : ('Mass [GeV]',           60, 0., 300.),
    'wtags_tight_mass_sj'           : ('Mass [GeV]',           60, 0., 300.),
    'wtags_tight_sm10_mass_softdrop'           : ('Mass [GeV]',           60, 0., 300.),
    'wtags_tight_sm20_mass_softdrop'           : ('Mass [GeV]',           60, 0., 300.),
    'wtags_loose_mass_softdrop'           : ('Mass [GeV]',           60, 0., 300.),
    'wtags_loose_mass_sj'           : ('Mass [GeV]',           60, 0., 300.),
    'wtags_loose_sm10_mass_softdrop'           : ('Mass [GeV]',           60, 0., 300.),
    'wtags_loose_sm20_mass_softdrop'           : ('Mass [GeV]',           60, 0., 300.),
    'n_toptags'              : ('N(Top tags)',              5, -.5, 4.5),
    # 'pt_fifth_ak4_jet'              : ('p_{T} fifth Ak4 Jet',             60, 0., 1500.),
    # 'pt_sixth_ak4_jet'              : ('p_{T} sixth Ak4 Jet',             60, 0., 1500.),
    # 'pt_third_ak8_jet'              : ('p_{T} third Ak8 Jet',             60, 0., 1500.),
    # 'first_ak8jet_eta'                : ('Eta 1st Ak8 Jet',                  50, -3., 3.),
    # 'first_ak8jet_mass'               : ('Mass 1st Ak8 Jet',                 60, 0., 300.),
    # 'first_ak8jet_nsjbtags'           : ('N(med sj b-tags) 1st Ak8 Jet',     4, -.5, 3.5),
    # 'first_ak8jet_pt'                 : ('p_{T} 1st Ak8 Jet',                   60, 0., 1500.),
    # 'first_ak8jet_dRlep'                : ('dR(1st TopJet, primary lepton)',   50, 0., 5.),
    # 'first_ak8jet_dRak4'               : ('dR(1st TopJet, nearest Ak4 Jet)',  50, 0., 5.),
    # 'first_ak8jet_dRak8'           : ('dR(1st TopJet, nearest Ak8 Jet)',  50, 0., 5.),
    # 'second_ak8jet_eta'                : ('Eta 2nd Ak8 Jet',                  50, -3., 3.),
    # 'second_ak8jet_mass'               : ('Mass 2nd Ak8 Jet',                 60, 0., 300.),
    # 'second_ak8jet_nsjbtags'           : ('N(med sj b-tags) 2nd Ak8 Jet',     4, -.5, 3.5),
    # 'second_ak8jet_pt'                 : ('p_{T} 2nd Ak8 Jet',                   60, 0., 1500.),
    # 'second_ak8jet_dRlep'                : ('dR(2nd TopJet, primary lepton)',   50, 0., 5.),
    # 'second_ak8jet_dRak4'               : ('dR(2nd TopJet, nearest Ak4 Jet)',  50, 0., 5.),
    # 'second_ak8jet_dRak8'           : ('dR(2nd TopJet, nearest Ak8 Jet)',  50, 0., 5.),
    # 'higgs_tag_1b_eta'                : ('Eta Higgs-Tag(1b)',                  50, -3., 3.),
    # 'higgs_tag_1b_mass'               : ('Mass Higgs-Tag(1b)',                 60, 0., 300.),
    # 'higgs_tag_1b_nsjbtags'           : ('N(med sj b-tags) Higgs-Tag(1b)',     4, -.5, 3.5),
    # 'higgs_tag_1b_pt'                 : ('p_{T} Higgs-Tag(1b)',                   60, 0., 1500.),
    # 'higgs_tag_2b_dRlep'                : ('dR(Higgs-Tag(2b), primary lepton)',   50, 0., 5.),
    # 'higgs_tag_2b_dRak4'               : ('dR(Higgs-Tag(2b), nearest Ak4 Jet)',  50, 0., 5.),
    # 'higgs_tag_2b_dRak8'           : ('dR(Higgs-Tag(2b), nearest Ak8 Jet)',  50, 0., 5.),
    # 'use_sr_sf'                     : ('Use SR SF',                         2, -.5, 1.5),

}
more_histos.update(core_histos)


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

bpbp_signals = [
    'BpBp_M-0700',
    'BpBp_M-0800',
    'BpBp_M-0900',
    'BpBp_M-1000',
    'BpBp_M-1100',
    'BpBp_M-1200',
    'BpBp_M-1300',
    'BpBp_M-1400',
    'BpBp_M-1500',
    'BpBp_M-1600',
    'BpBp_M-1700',
    'BpBp_M-1800',
]

tptp_signals_important = [
    'TpTp_M-0800',
    'TpTp_M-1000',
    'TpTp_M-1200',
    'TpTp_M-1600',
]

tptp_signals_rest = [
    'TpTp_M-0700',
    'TpTp_M-0900',
    # 'TpTp_M-1000',
    'TpTp_M-1100',
    # 'TpTp_M-1200',
    'TpTp_M-1300',
    'TpTp_M-1400',
    'TpTp_M-1500',
    'TpTp_M-1700',
    'TpTp_M-1800',
]

tptp_final_states = [
    '_thth',
    '_thtz',
    '_thbw',
    '_noH_tztz',
    '_noH_tzbw',
    '_noH_bwbw',
]

bpbp_final_states = [
    '_bhbh',
    '_bhbz',
    '_bhtw',
    '_noH_bzbz',
    '_noH_bztw',
    '_noH_twtw',
]

ttbar_smpl = 'TTbar_split'

background_samples = [
    ttbar_smpl,
    'SingleTop',
    'QCD',
    'DYJets',
    'WJets',
    'Diboson'
]

tptp_signal_samples = reduce(lambda x, y: x+y, (list(g + f for f in tptp_final_states) for g in tptp_signals))
tptp_signal_samples_important = reduce(lambda x, y: x+y, (list(g + f for f in tptp_final_states) for g in tptp_signals_important))
tptp_signal_samples_rest = reduce(lambda x, y: x+y, (list(g + f for f in tptp_final_states) for g in tptp_signals_rest))
tptp_signal_samples_reduced = reduce(lambda x, y: x+y, (list(g + f for f in tptp_final_states) for g in ['TpTp_M-0800', 'TpTp_M-1600']))
tptp_signal_samples_only_thth = list(g + '_thth' for g in tptp_signals)
bpbp_signal_samples = reduce(lambda x, y: x+y, (list(g + f for f in bpbp_final_states) for g in bpbp_signals))

bkg_w_data = background_samples + ['Run2015CD']
bkg_no_data = background_samples
samples_w_data = background_samples + tptp_signal_samples + ['Run2015CD']
samples_no_data = background_samples + tptp_signal_samples

base_weight = 'weight'

# # values below from FinalSelection-v14/RunWJetsSideband/fit_results_ht_sideband_w_toppt_reweight.txt
# # p0_from1000 = 1.252481
# # p1_from1000 = -0.000216602

# # p0_from0 = 1.353281
# # p1_from0 = -0.000251745

# # values below from FinalSelection-v14/RunWJetsSideband/fit_results_ht_sideband_w_toppt_reweight.txt

# p0_from0_no_top_pt_reweight = 1.165688
# p1_from0_no_top_pt_reweight = -0.000236061

# ht_reweight = '*({0}+{1}*HT)'.format(p0_from0_no_top_pt_reweight, p1_from0_no_top_pt_reweight)
# ttbar_reweight = '*(weight_ttbar/0.9910819)'

sample_weights_def = {
    ttbar_smpl : base_weight,
    'SingleTop' : base_weight,
    'QCD' : base_weight,
    'DYJets' : base_weight,
    'WJets' : base_weight,
    'Diboson' : base_weight,
    'Run2015CD' : '1',
}
sample_weights_def.update(dict((f, 'weight') for f in tptp_signal_samples))
sample_weights_def.update(dict((f, 'weight') for f in bpbp_signal_samples))


# import tptp_selections_treeproject as sel

all_params = {
    'histos': more_histos,
    'treename': 'AnalysisTree',
    'nm1' : False,
}

st_only_params = {
    'histos': st_only,
    'treename': 'AnalysisTree',
    'nm1' : False,
}

st_plus_jets_params = {
    'histos': st_plus_jets,
    'treename': 'AnalysisTree',
    'nm1' : False,
}

sys_params = {
    'histos': core_histos,
    'treename': 'AnalysisTree',
    'nm1' : False,
}


def mk_tp(input_pat, final_regions, weights=None, samples=samples_w_data, name='TreeProjector', treeproject=TreeProjector):
    sample_weights = weights or sample_weights_def
    sec_sel_weight = list((g, f, weights) for g, f in final_regions)
    all_files = glob.glob(join(input_pat, 'Files_and_Plots_nominal/SFrame/workdir/uhh2.AnalysisModuleRunner.*.root'))

    filenames = dict(
        (sample, list(f for f in all_files if sample in f))
        for sample in samples
    )
    kws = {}
    if treeproject == SparkTreeProjector:
        import socket
        hostname = socket.gethostname()
        kws['spark_url'] = 'spark://%s:7077' % hostname

    return treeproject(
        filenames, all_params, sec_sel_weight, 
        # suppress_job_submission=True, 
        name=name,
        **kws
    )

def add_jec_uncerts(base_path, final_regions, sample_weights, samples=samples_no_data, params=sys_params, treeproject=TreeProjector, **kws):
    # def tmp():
    jercs = list(
        (
            name.replace('_down', '__minus').replace('_up', '__plus'), 
            join(base_path, 'Files_and_Plots_' + name + '/SFrame/workdir/uhh2*.root')
        ) 
        for name in ('jec_down', 'jec_up', 'jer_down', 'jer_up')
    )
    
    nominal_sec_sel_weight = list((g, f, sample_weights) for g, f in final_regions)
    return list(
        treeproject(
            dict(
                (sample, list(f for f in glob.glob(pat) if (sample in f and 'Scale' not in f)))
                for sample in samples
            ), 
            params, 
            nominal_sec_sel_weight,
            add_aliases_to_analysis=False,
            name=name,
            **kws
        )
        for name, pat in jercs
    )
    # return tmp

def add_ttbar_scale_uncerts(path_ttbar_scale_files, base_path_nominal_files, final_regions, sample_weights, samples=samples_no_data, params=sys_params, treeproject=TreeProjector, **kws):
    # def tmp():
    files_ttbar_scale_up = join(path_ttbar_scale_files, 'Files_and_Plots_nominal/SFrame/workdir*/uhh2.AnalysisModuleRunner.MC.TTJets_ScaleUp_*.root')
    files_ttbar_scale_down = join(path_ttbar_scale_files, 'Files_and_Plots_nominal/SFrame/workdir*/uhh2.AnalysisModuleRunner.MC.TTJets_ScaleDown_*.root')
    files_nom_path = join(base_path_nominal_files, 'Files_and_Plots_nominal/SFrame/workdir/uhh2.AnalysisModuleRunner.*.root')
    dict_nom_files = dict(
        (sample, list(f for f in glob.glob(files_nom_path) if sample in f))
        for sample in samples
    )
    dict_up_files = dict(dict_nom_files)
    dict_up_files.update({ttbar_smpl : list(f for f in glob.glob(files_ttbar_scale_up))})
    dict_down_files = dict(dict_nom_files)
    dict_down_files.update({ttbar_smpl : list(f for f in glob.glob(files_ttbar_scale_down))})
    nominal_sec_sel_weight = list((g, f, sample_weights) for g, f in final_regions)
    return [
        treeproject(
            dict_up_files, 
            params, 
            nominal_sec_sel_weight,
            add_aliases_to_analysis=False,
            name='PSScale__plus',
            **kws
        ),
        treeproject(
            dict_down_files, 
            params, 
            nominal_sec_sel_weight,
            add_aliases_to_analysis=False,
            name='PSScale__minus',
            **kws
        )
    ]

def add_higgs_smear_uncerts(base_path, final_regions, sample_weights, samples=samples_no_data, params=sys_params, treeproject=TreeProjector, **kws):
    # def tmp():
    nominal_files = join(base_path, 'Files_and_Plots_nominal/SFrame/workdir/uhh2*.root') 
    filenames = dict(
        (sample, list(f for f in glob.glob(nominal_files) if sample in f))
        for sample in samples
    )
    final_regions_up = list((g, map(lambda w: w.replace('_sm10', ''), f)) for g, f in final_regions)
    final_regions_down = list((g, map(lambda w: w.replace('_sm10', '_sm20'), f)) for g, f in final_regions)

    sys_sec_sel_weight_reweight_weight = (
        ('higgs_smear__minus', list((g, f, sample_weights) for g, f in final_regions_down)),
        ('higgs_smear__plus', list((g, f, sample_weights) for g, f in final_regions_up))
    )
    return list(
        treeproject(
            filenames,
            params, 
            ssw,
            add_aliases_to_analysis=False,
            name=name,
            **kws
        )
        for name, ssw in sys_sec_sel_weight_reweight_weight
    )

def add_generic_uncerts(base_path, final_regions, sample_weights, samples=samples_no_data, params=sys_params, treeproject=TreeProjector, **kws):
    # def tmp():
    nominal_files = join(base_path, 'Files_and_Plots_nominal/SFrame/workdir/uhh2*.root') 
    filenames = dict(
        (sample, list(f for f in glob.glob(nominal_files) if sample in f))
        for sample in samples
    )
    sys_sec_sel_weight = list(
        (name, list((g, f, dict((a, c+w) for a, c in sample_weights.iteritems()))
            for g, f in final_regions) 
        )
        for name, w in (
            ('btag_bc__minus', '*weight_btag_bc_down*weight_btag_bc_down_sj/weight_btag'),
            ('btag_bc__plus', '*weight_btag_bc_up*weight_btag_bc_up_sj/weight_btag'),
            ('btag_udsg__minus', '*weight_btag_udsg_down*weight_btag_udsg_down_sj/weight_btag'),
            ('btag_udsg__plus', '*weight_btag_udsg_up*weight_btag_udsg_up_sj/weight_btag'),
            # ('sfmu_id__minus', '*weight_sfmu_id_down/weight_sfmu_id'),
            # ('sfmu_id__plus', '*weight_sfmu_id_up/weight_sfmu_id'),
            # ('sfmu_trg__minus', '*weight_sfmu_trg_down/weight_sfmu_trg'),
            # ('sfmu_trg__plus', '*weight_sfmu_trg_up/weight_sfmu_trg'),
            ('pu__minus', '*weight_pu_down/weight_pu'),
            ('pu__plus', '*weight_pu_up/weight_pu'),
            # ('twoD__minus', '*0.95'), # for 2D-cut
            # ('twoD__plus', '*1.05'), # for 2D-cut
            # ('ak4_jetpt__minus', '*weight_ak4_jetpt_down/weight_ak4_jetpt'),
            # ('ak4_jetpt__plus', '*weight_ak4_jetpt_up/weight_ak4_jetpt'),
        )
    )
    sys_sec_sel_weight += list(
        (name, list((g, f, dict((a, c+w) for a, c in sample_weights.iteritems()))
            for g, f in final_regions if 'Mu45' in g) 
        )
        for name, w in (
            ('sfmu_id__minus', '*weight_sfmu_id_down/weight_sfmu_id'),
            ('sfmu_id__plus', '*weight_sfmu_id_up/weight_sfmu_id'),
            ('sfmu_trg__minus', '*weight_sfmu_trg_down/weight_sfmu_trg'),
            ('sfmu_trg__plus', '*weight_sfmu_trg_up/weight_sfmu_trg'),
        )
    )
    sys_sec_sel_weight += list(
        (name, list((g, f, dict((a, c+w) for a, c in sample_weights.iteritems()))
            for g, f in final_regions if 'El45' in g) 
        )
        for name, w in (
            # ('sfel_id_trg__minus', '*0.95'),
            # ('sfel_id_trg__plus', '*1.05'),
            ('sfel_id__minus', '*weight_sfel_id_down/weight_sfel_id'),
            ('sfel_id__plus', '*weight_sfel_id_up/weight_sfel_id'),
            ('sfel_trg__minus', '*weight_sfel_trg_down/weight_sfel_trg'),
            ('sfel_trg__plus', '*weight_sfel_trg_up/weight_sfel_trg'),
        )
    )
    return list(
        treeproject(
            filenames,
            params, 
            ssw,
            add_aliases_to_analysis=False,
            name=name,
            **kws
        )
        for name, ssw in sys_sec_sel_weight
    )
    # return tmp


def add_pdf_uncerts(base_path, final_regions, sample_weights, samples=samples_no_data, params=st_only_params, treeproject=TreeProjector, **kws):
    # def tmp():
    nominal_files = join(base_path, 'Files_and_Plots_nominal/SFrame/workdir/uhh2*.root') 
    filenames = dict(
        (sample, list(f for f in glob.glob(nominal_files) if sample in f))
        for sample in samples
    )
    weight_dict_pdf = {}
    for d in glob.glob('weight_dict_pdf*'):
        with open(d) as f:
            weight_dict_pdf.update(ast.literal_eval(f.read()))
    weight_dict_pdf.update(dict((smpl, ['1']*100) for smpl in samples_no_data if smpl not in weight_dict_pdf))
    weight_dict_pdf.update(dict((smpl_fix, weight_dict_pdf[smpl]) for (smpl_fix, smpl) in itertools.izip(['BpBp_M-0700', 'BpBp_M-0800', 'BpBp_M-0900'], ['BpBp_M-700', 'BpBp_M-800', 'BpBp_M-900'])))
    for g in tptp_final_states:
        weight_dict_pdf.update(dict((s+g, weight_dict_pdf[s]) for s in tptp_signals))
    for g in bpbp_final_states:
        weight_dict_pdf.update(dict((s+g, weight_dict_pdf[s]) for s in bpbp_signals))
    # sys_params_pdf = {
    #     'histos': core_histos,
    #     'treename': 'AnalysisTree',
    # }
    sys_sec_sel_weight_pdf = list(
        ('pdf_weight_%i'%i, list((g, f,
            dict(
                    (smpl, sample_weights[smpl]+'*weight_pdf_%i/%s'%(i, weight_dict[i]))
                    for smpl, weight_dict in weight_dict_pdf.iteritems() if smpl in samples
                )
            ) for g, f in final_regions)
        )
        for i in xrange(100)
    )
    sys_tps_pdf = list(
        treeproject(
            filenames, 
            params, 
            ssw,
            add_aliases_to_analysis=False,
            name=name,
            **kws
        )
        for name, ssw in sys_sec_sel_weight_pdf
    )
    # sys_tps_pdf += [GenUncertHistoSquash(squash_func=varial.op.squash_sys_stddev)]
    sys_tps_pdf += [varial.tools.ToolChainParallel('GenUncertHistoSquash', list(GenUncertHistoSquash(squash_func=varial.op.squash_sys_stddev, sample='*'+s, load_aliases=False) for s in samples))]
    return [
        varial.tools.ToolChain('SysTreeProjectorsPDF', sys_tps_pdf),
        GenUncertUpDown(input_path='../SysTreeProjectorsPDF/GenUncertHistoSquash/GenUncertHistoSquash*', name='PDF__plus'),
        GenUncertUpDown(input_path='../SysTreeProjectorsPDF/GenUncertHistoSquash/GenUncertHistoSquash*', name='PDF__minus'),
        # GenUncertUpDown(input_path='../SysTreeProjectorsPDF/GenUncertHistoSquash*', norm=True, name='NormPDF__plus'),
        # GenUncertUpDown(input_path='../SysTreeProjectorsPDF/GenUncertHistoSquash*', norm=True, name='NormPDF__minus'),
    ]
    # return tmp


def add_scale_var_uncerts(base_path, final_regions, sample_weights, samples=samples_no_data, params=sys_params, treeproject=TreeProjector, **kws):
    # def tmp():
    nominal_files = join(base_path, 'Files_and_Plots_nominal/SFrame/workdir/uhh2*.root') 
    filenames = dict(
        (sample, list(f for f in glob.glob(nominal_files) if sample in f))
        for sample in samples
    )
    weight_dict_scale = {}
    for d in glob.glob('weight_dict_scale*'):
        with open(d) as f:
            weight_dict_scale.update(ast.literal_eval(f.read()))
    weight_dict_scale.update(dict((smpl, ['1']*9) for smpl in samples_no_data if smpl not in weight_dict_scale))
    weight_dict_scale.update(dict((smpl_fix, weight_dict_scale[smpl]) for (smpl_fix, smpl) in itertools.izip(['BpBp_M-0700', 'BpBp_M-0800', 'BpBp_M-0900'], ['BpBp_M-700', 'BpBp_M-800', 'BpBp_M-900'])))
    for g in tptp_final_states:
        weight_dict_scale.update(dict((s+g, weight_dict_scale[s]) for s in tptp_signals))
    for g in bpbp_final_states:
        weight_dict_scale.update(dict((s+g, weight_dict_scale[s]) for s in bpbp_signals))
    sys_sec_sel_weight_scalevar = list(
        ('scalevar_weight_%i'%i, list((g, f,
            dict(
                    (smpl, sample_weights[smpl]+'*weight_muRF_%i/%s'%(i, weight_dict[i]))
                    for smpl, weight_dict in weight_dict_scale.iteritems() if smpl in samples
                )
            ) for g, f in final_regions)
        )
        for i in [1, 2, 3, 4, 6, 8] # physical indices for scale variations without nominal value!
        # for i in [1, 2] # physical indices for scale variations without nominal value!
    )
    sys_tps_scalevar = list(
        treeproject(
            filenames, 
            params, 
            ssw,
            add_aliases_to_analysis=False,
            name=name,
            **kws
        )
        for name, ssw in sys_sec_sel_weight_scalevar
    )
    sys_tps_scalevar += [varial.tools.ToolChainParallel('GenUncertHistoSquash', list(GenUncertHistoSquash(squash_func=varial.op.squash_sys_env, sample='*'+s, load_aliases=False) for s in samples))]
    # sys_tps_scalevar += [GenUncertHistoSquash(squash_func=varial.op.squash_sys_env)]
    return [
        varial.tools.ToolChain('SysTreeProjectorsScaleVar', sys_tps_scalevar),
        GenUncertUpDown(input_path='../SysTreeProjectorsScaleVar/GenUncertHistoSquash/GenUncertHistoSquash*', name='ScaleVar__plus'),
        GenUncertUpDown(input_path='../SysTreeProjectorsScaleVar/GenUncertHistoSquash/GenUncertHistoSquash*', name='ScaleVar__minus'),
        # GenUncertUpDown(input_path='../SysTreeProjectorsScaleVar/GenUncertHistoSquash*', norm=True, name='NormScaleVar__plus'),
        # GenUncertUpDown(input_path='../SysTreeProjectorsScaleVar/GenUncertHistoSquash*', norm=True, name='NormScaleVar__minus'),
    ]
    # return tmp


def add_weight_uncerts(base_path, final_regions, sample_weights, weight_name, weight_dict, samples=samples_no_data, params=sys_params, treeproject=TreeProjector, **kws):
    # def tmp():
    nominal_files = join(base_path, 'Files_and_Plots_nominal/SFrame/workdir/uhh2*.root') 
    filenames = dict(
        (sample, list(f for f in glob.glob(nominal_files) if sample in f))
        for sample in samples
    )
    sample_weights_reweight_down = dict(sample_weights)
    sample_weights_reweight_up = dict(sample_weights)
    sample_weights_reweight_down.update(dict((proc, sample_weights[proc]+'*('+weight+')') for proc, weight in weight_dict.iteritems()))
    sample_weights_reweight_up.update(dict((proc, sample_weights[proc]+'/('+weight+')') for proc, weight in weight_dict.iteritems()))
    sys_sec_sel_weight_reweight_weight = (
        (weight_name+'__minus', list((g, f, sample_weights_reweight_down) for g, f in final_regions)),
        (weight_name+'__plus', list((g, f, sample_weights_reweight_up) for g, f in final_regions))
    )
    return list(
        treeproject(
            filenames,
            params, 
            ssw,
            add_aliases_to_analysis=False,
            name=name,
            **kws
        )
        for name, ssw in sys_sec_sel_weight_reweight_weight
    )

def add_one_sided_weight_uncerts(base_path, final_regions, sample_weights, weight_name, weight_dict, samples=samples_no_data, params=sys_params, treeproject=TreeProjector, **kws):
    # def tmp():
    nominal_files = join(base_path, 'Files_and_Plots_nominal/SFrame/workdir/uhh2*.root') 
    filenames = dict(
        (sample, list(f for f in glob.glob(nominal_files) if sample in f))
        for sample in samples
    )
    sample_weights_reweight_down = dict(sample_weights)
    sample_weights_reweight_up = dict(sample_weights)
    sample_weights_reweight_down.update(dict((proc, sample_weights[proc]+'*('+weight+')') for proc, weight in weight_dict.iteritems()))
    # sample_weights_reweight_up.update(dict((proc, sample_weights[proc]+'/('+weight+')') for proc, weight in weight_dict.iteritems()))
    sys_sec_sel_weight_reweight_weight = (
        (weight_name+'__minus', list((g, f, sample_weights_reweight_down) for g, f in final_regions)),
        (weight_name+'__plus', list((g, f, sample_weights_reweight_up) for g, f in final_regions))
    )
    return list(
        treeproject(
            filenames,
            params, 
            ssw,
            add_aliases_to_analysis=False,
            name=name,
            **kws
        )
        for name, ssw in sys_sec_sel_weight_reweight_weight
    )
    # return tmp

def mk_sys_tps(mk_sys_func, name='SysTreeProjectors', treeproject=TreeProjector):
    # sample_weights = weights or sample_weights_def
    # some defs
    # base_path = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII-25ns-v2/'\
    #     'CMSSW_7_4_15_patch1/src/UHH2/VLQToHiggsPairProd/Samples-25ns-v2/'\
    #     'TpTpFinalSelectionTreeOutput-v0wBTagSF/Files_and_Plots/'

    # first put together jerc uncert with nominal weights
    if mk_sys_func:
        if treeproject == SparkTreeProjector:
            import socket
            hostname = socket.gethostname()
            print hostname
            sys_tps = mk_sys_func(treeproject=SparkTreeProjector, spark_url='spark://%s:7077' % hostname)
        else:
            sys_tps = mk_sys_func(treeproject=TreeProjector)
    else:
        sys_tps = []
    

    for tp in sys_tps:
        iteration[0] += 1
        tp.iteration = 10 * iteration[0]  # batch tp's should not interfere

    return varial.tools.ToolChainParallel(
        name, sys_tps, n_workers=1
    )


class GenUncertHistoSquash(varial.tools.Tool):
    io = varial.pklio

    def __init__(self, squash_func=varial.op.squash_sys_stddev, sample='', load_aliases=True, **kws):
        super(GenUncertHistoSquash, self).__init__(**kws)
        self.squash_func = squash_func
        self.sample = sample
        self.rel_path = '*.root'
        self.load_aliases = load_aliases
        if self.sample:
            self.name = 'GenUncertHistoSquash_'+sample.replace('*', '')
            self.rel_path = self.sample+'.root'

    def run(self):
        sys_paths = glob.glob(self.cwd + '../../*_weight*')
        # sys_paths.remove(self.cwd + '../'+self.name)
        try:
            uncert_histos = (
                w
                for p in sys_paths
                for w in varial.diskio.bulk_load_histograms(
                            # varial.gen.dir_content(p+'/%s'%self.rel_path))
                            varial.gen.dir_content(p+'/%s'%self.rel_path, self.load_aliases))
                            # varial.gen.dir_content(p+'/%s.root'%self.sample))
            )
        except RuntimeError as e:
            self.message(e)
            return
        uncert_histos = varial.gen.gen_add_wrp_info(uncert_histos, 
            category=lambda w: w.in_file_path.split('/')[0],
            # variable=lambda w: w.in_file_path.split('/')[1])
            variable=lambda w: w.in_file_path.split('/')[1],
            sample=lambda w: w.file_path.split('/')[-1].split('.')[0])
        uncert_histos = sorted(uncert_histos, key=lambda w: w.sample+'___'+w.category+'___'+w.variable)
        # uncert_histos = list(uncert_histos)
        # for w in uncert_histos: print w.sample, w.file_path, w.in_file_path
        uncert_histos = varial.gen.group(uncert_histos, lambda w: w.sample+'___'+w.category+'___'+w.variable)
        # uncert_histos = list(uncert_histos)
        # print len(uncert_histos)
        # uncert_histos = list(uncert_histos)
        # for p in uncert_histos: print list((g.file_path, g.in_file_path) for g in p)
        uncert_histos = (self.squash_func(h) for h in uncert_histos)
        self.result = list(uncert_histos)
        varial.diskio.close_open_root_files()
        os.system('touch %s/webcreate_denial' % self.cwd)


class GenUncertUpDown(varial.tools.Tool):
    io = varial.pklio

    def __init__(self, input_path, norm=False, **kws):
        super(GenUncertUpDown, self).__init__(**kws)
        self.input_path = input_path
        self.norm = norm

    def run(self):
        assert '__plus' in self.name or '__minus' in self.name
        factor = 1. if '__plus' in self.name else -1.
        self.message('INFO adding error with factor: %i' % factor)

        def set_values(w):
            h = w.histo
            if w.histo_sys_err:
                h_sys = w.histo_sys_err
            else:
                h_sys = w.histo
            for i in xrange(h_sys.GetNbinsX()+2):
                h.SetBinContent(i, h_sys.GetBinContent(i) 
                                   + factor*h_sys.GetBinError(i))
            w.histo_sys_err = None
            return w

        def norm_thing(wrps):
            sigs = varial.gen.dir_content('../../TreeProjector/*.root')
            # sigs = (s for s in sigs if '/TpTp_' in s.file_path)
            sigs = (s for s in sigs if s.name in core_histos.keys())
            # sigs = (s for s in sigs if 'SignalRegion' in s.in_file_path)
            sigs = varial.gen.load(sigs)
            sigs = varial.gen.gen_add_wrp_info(sigs, 
                category=lambda w: w.in_file_path.split('/')[0])
            sigs = dict((s.sample+'_'+s.name+'_'+s.category, s.histo) for s in sigs)
            for w in wrps:
                if w.histo.Integral() and w.sample+'_'+w.name+'_'+w.category in sigs.keys():
                    w.histo.Scale(sigs[w.sample+'_'+w.name+'_'+w.category].Integral() / w.histo.Integral())
                    yield w

        from itertools import groupby

        def store(grps):
            for g in grps:
                sample = g.wrps[0].sample
                wrps = sorted(g.wrps, key=lambda a: a.category)
                wrps = dict((k, list(w)) for k, w in groupby(wrps, key=lambda a: a.category))
                for k, ws in wrps.iteritems():
                    fsw = varial.analysis.fileservice(k)
                    for w in ws: fsw.append(w.histo)
                varial.diskio.write_fileservice(sample)
                yield g


        input_list = glob.glob(os.path.join(self.cwd, self.input_path)) # '../SysTreeProjectorsPDF/GenUncertHistoSquash*'
        histos = list(self.lookup_result(k) for k in input_list)
        histos = list(h for g in histos for h in g)
        assert histos


        histos = (varial.op.copy(w) for w in histos)
        histos = varial.gen.gen_add_wrp_info(histos, 
            category=lambda w: w.in_file_path.split('/')[0],
            variable=lambda w: w.in_file_path.split('/')[1],
            sample=lambda w: w.file_path.split('/')[-1].split('.')[0])
        histos = (set_values(w) for w in histos)
        if self.norm:
            histos = norm_thing(histos)
        histos = sorted(histos, key=lambda w: w.sample)
        histos = varial.gen.group(histos, lambda w: w.sample)
        histos = store(histos)
        histos = list(histos)

        alia = varial.diskio.generate_aliases(self.cwd + '*.root')
        alia = varial.gen.gen_add_wrp_info(alia, 
            sample=lambda a: os.path.basename(os.path.splitext(a.file_path)[0]))
        self.result = list(alia)
        varial.diskio.close_open_root_files()
        os.system('touch %s/aliases.in.result' % self.cwd)
        os.system('touch %s/webcreate_denial' % self.cwd)

import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Input file pattern needed!'
        exit(-1)
    input_pat = sys.argv[1]
    varial.tools.Runner(mk_tp(input_pat))

