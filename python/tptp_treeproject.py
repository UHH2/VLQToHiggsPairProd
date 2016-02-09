#!/usr/bin/env python

from varial_ext.treeprojector import TreeProjector #, SGETreeProjector
from os.path import join
import varial.tools
import glob

# varial.settings.max_num_processes = 24

core_histos = {
    'ST'                            : ('ST',                               45, 0, 4500),
    'n_ak4'                         : ('N(Ak4 Jets)',                      14, -.5, 13.5),
    'n_ak8'                         : ('N(Ak8 Jets)',                      8, -.5, 7.5),
    'pt_ld_ak4_jet'                 : ('Pt leading Ak4 Jet',               60, 0., 1500.),
    'pt_ld_ak8_jet'                 : ('Pt leading Ak8 Jet',               60, 0., 1500.),
    'primary_lepton_pt'             : ('Primary Lepton p_T',               90, 0., 900.),
}

more_histos = {
    'gendecay_accept'               : ('GenDecay Accept',                  2, -.5, 1.5),
    # 'ST_cleaned'                    : ('ST cleaned',                       45, 0, 4500),
    'n_additional_btags_medium'     : ('N(non-overlapping medium b-tags)', 8, -.5, 7.5),
    # 'n_ak4_pt_cleaned'              : ('N(Ak4 Jets, cleaned)',             14, -.5, 13.5),
    # 'n_ak8_pt_cleaned'              : ('N(Ak8 Jets, cleaned)',             8, -.5, 7.5),
    'n_ak8_higgs_cand'              : ('N(Higgs Candidates)',              8, -.5, 7.5),
    'n_higgs_tags_1b_med'           : ('N(Higgs-Tags, 1 med b)',           5, -.5, 4.5),
    'n_higgs_tags_2b_med'           : ('N(Higgs-Tags, 2 med b)',           5, -.5, 4.5),
    'n_jets_no_overlap'             : ('N(non-overlapping Ak4 jets)',      12, -.5, 11.5),
    # 'pt_ld_ak4_jet_cleaned'         : ('Pt leading Ak4 Jet, cleaned',      60, 0., 1500.),
    # 'pt_ld_ak8_jet_cleaned'         : ('Pt leading Ak8 Jet, cleaned',      60, 0., 1500.),
    'trigger_accept_mu45'           : ('Trigger Accepted Mu45',             2, -.5, 1.5),
    'trigger_accept_el45'           : ('Trigger Accepted El40',             2, -.5, 1.5),
    'trigger_accept_isoMu20'          : ('Trigger Accepted IsoMu',            2, -.5, 1.5),
    'trigger_accept_isoEl27'          : ('Trigger Accepted IsoMu',            2, -.5, 1.5),
    'is_muon'                       : ('Prim. Lep. is Muon',                2, -.5, 1.5),
    'first_ak8jet_eta'                : ('Eta 1st Ak8 Jet',                  50, -3., 3.),
    'first_ak8jet_mass'               : ('Mass 1st Ak8 Jet',                 60, 0., 300.),
    'first_ak8jet_nsjbtags'           : ('N(med sj b-tags) 1st Ak8 Jet',     4, -.5, 3.5),
    'first_ak8jet_pt'                 : ('Pt 1st Ak8 Jet',                   60, 0., 1500.),
    'first_ak8jet_dRlep'                : ('dR(1st TopJet, primary lepton)',   50, 0., 5.),
    'first_ak8jet_dRak4'               : ('dR(1st TopJet, nearest Ak4 Jet)',  50, 0., 5.),
    'first_ak8jet_dRak8'           : ('dR(1st TopJet, nearest Ak8 Jet)',  50, 0., 5.),
    'second_ak8jet_eta'                : ('Eta 2nd Ak8 Jet',                  50, -3., 3.),
    'second_ak8jet_mass'               : ('Mass 2nd Ak8 Jet',                 60, 0., 300.),
    'second_ak8jet_nsjbtags'           : ('N(med sj b-tags) 2nd Ak8 Jet',     4, -.5, 3.5),
    'second_ak8jet_pt'                 : ('Pt 2nd Ak8 Jet',                   60, 0., 1500.),
    'second_ak8jet_dRlep'                : ('dR(2nd TopJet, primary lepton)',   50, 0., 5.),
    'second_ak8jet_dRak4'               : ('dR(2nd TopJet, nearest Ak4 Jet)',  50, 0., 5.),
    'second_ak8jet_dRak8'           : ('dR(2nd TopJet, nearest Ak8 Jet)',  50, 0., 5.),
    'higgs_tag_1b_eta'                : ('Eta Higgs-Tag(1b)',                  50, -3., 3.),
    'higgs_tag_1b_mass'               : ('Mass Higgs-Tag(1b)',                 60, 0., 300.),
    'higgs_tag_1b_nsjbtags'           : ('N(med sj b-tags) Higgs-Tag(1b)',     4, -.5, 3.5),
    'higgs_tag_1b_pt'                 : ('Pt Higgs-Tag(1b)',                   60, 0., 1500.),
    'higgs_tag_1b_dRlep'                : ('dR(Higgs-Tag(1b), primary lepton)',   50, 0., 5.),
    'higgs_tag_1b_dRak4'               : ('dR(Higgs-Tag(1b), nearest Ak4 Jet)',  50, 0., 5.),
    'higgs_tag_1b_dRak8'           : ('dR(Higgs-Tag(1b), nearest Ak8 Jet)',  50, 0., 5.),
    'higgs_tag_2b_eta'                : ('Eta Higgs-Tag(2b)',                  50, -3., 3.),
    'higgs_tag_2b_mass'               : ('Mass Higgs-Tag(2b)',                 60, 0., 300.),
    'higgs_tag_2b_nsjbtags'           : ('N(med sj b-tags) Higgs-Tag(2b)',     4, -.5, 3.5),
    'higgs_tag_2b_pt'                 : ('Pt Higgs-Tag(2b)',                   60, 0., 1500.),
    'higgs_tag_2b_dRlep'                : ('dR(Higgs-Tag(2b), primary lepton)',   50, 0., 5.),
    'higgs_tag_2b_dRak4'               : ('dR(Higgs-Tag(2b), nearest Ak4 Jet)',  50, 0., 5.),
    'higgs_tag_2b_dRak8'           : ('dR(Higgs-Tag(2b), nearest Ak8 Jet)',  50, 0., 5.),
    # 'use_sr_sf'                     : ('Use SR SF',                         2, -.5, 1.5),
}
more_histos.update(core_histos)

params = {
    'histos': more_histos,
    'treename': 'AnalysisTree',
}

signals = [
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

final_states = [
    '_thth',
    # '_thtz',
    # '_thbw',
    # '_noH_tztz',
    # '_noH_tzbw',
    # '_noH_bwbw',
]

background_samples = [
    'TTbar',
    'SingleTop',
    'QCD',
    'DYJets',
    'WJets',
]

signal_samples = reduce(lambda x, y: x+y, (list(g + f for f in final_states) for g in signals))

samples = background_samples + signal_samples + ['Run2015D']
samples_no_data = background_samples + signal_samples

sample_weights = {
    'TTbar' : 'weight*weight_ak4_jetpt',
    'SingleTop' : 'weight*weight_ak4_jetpt',
    'QCD' : 'weight*weight_ak4_jetpt',
    'DYJets' : 'weight*weight_ak4_jetpt',
    'WJets' : 'weight*weight_ak4_jetpt',
    'Run2015D' : 'weight*weight_ak4_jetpt',
}
sample_weights.update(dict((f, 'weight') for f in signal_samples))


import tptp_selections_treeproject as sel

sec_sel_weight = [
    ('BaseLineSelectionEl45', sel.el_channel, sample_weights), # *weight_ak4_jetpt
    ('BaseLineSelectionMu45', sel.mu_channel, sample_weights), # *weight_ak4_jetpt
    # ('BaseLineSelection', sel.baseline_selection, 'weight*weight_ak4_jetpt'), # *weight_ak4_jetpt
    ('SignalRegion2b_El45', sel.sr2b_channel + sel.el_channel, sample_weights), # *weight_ak4_jetpt
    ('SignalRegion1b_El45', sel.sr1b_channel + sel.el_channel, sample_weights), # *weight_ak4_jetpt
    ('SidebandRegion_El45', sel.sb_channel + sel.el_channel, sample_weights), # *weight_ak4_jetpt
    ('SignalRegion2b_Mu45', sel.sr2b_channel + sel.mu_channel, sample_weights), # *weight_ak4_jetpt
    ('SignalRegion1b_Mu45', sel.sr1b_channel + sel.mu_channel, sample_weights), # *weight_ak4_jetpt
    ('SidebandRegion_Mu45', sel.sb_channel + sel.mu_channel, sample_weights), # *weight_ak4_jetpt
    # # ('SidebandRegion_El45DRCut', sel.sb_channel + sel.el_channel + sel.dr_cut_invert, 'weight*weight_ak4_jetpt'), # *weight_ak4_jetpt
    # # ('SidebandRegion_Mu45DRCut', sel.sb_channel + sel.mu_channel + sel.dr_cut_invert, 'weight*weight_ak4_jetpt'), # *weight_ak4_jetpt
    # ('SidebandWJetsRegion_El45', sel.sb_wjets_channel + sel.el_channel, 'weight*weight_ak4_jetpt'), # *weight_ak4_jetpt
    # ('SidebandWJetsRegion_Mu45', sel.sb_wjets_channel + sel.mu_channel, 'weight*weight_ak4_jetpt'), # *weight_ak4_jetpt
    # ('SignalRegion2b_El45iso', sel.sr2b_channel + sel.eliso_channel, 'weight*weight_ak4_jetpt'), # *weight_ak4_jetpt
    # ('SignalRegion1b_El45iso', sel.sr1b_channel + sel.eliso_channel, 'weight*weight_ak4_jetpt'), # *weight_ak4_jetpt
    # ('SidebandRegion_El45iso', sel.sb_channel + sel.eliso_channel, 'weight*weight_ak4_jetpt'), # *weight_ak4_jetpt
    # ('SignalRegion2b_Mu45iso', sel.sr2b_channel + sel.muiso_channel, 'weight*weight_ak4_jetpt'), # *weight_ak4_jetpt
    # ('SignalRegion1b_Mu45iso', sel.sr1b_channel + sel.muiso_channel, 'weight*weight_ak4_jetpt'), # *weight_ak4_jetpt
    # ('SidebandRegion_Mu45iso', sel.sb_channel + sel.muiso_channel, 'weight*weight_ak4_jetpt'), # *weight_ak4_jetpt
    # ('SignalRegion2b_El45DRCut', sel.sr2b_channel + sel.el_channel + sel.dr_cut, 'weight*weight_ak4_jetpt'), # *weight_ak4_jetpt
    # ('SignalRegion1b_El45DRCut', sel.sr1b_channel + sel.el_channel + sel.dr_cut, 'weight*weight_ak4_jetpt'), # *weight_ak4_jetpt
    # ('SidebandRegion_El45DRCut', sel.sb_channel + sel.el_channel + sel.dr_cut, 'weight*weight_ak4_jetpt'), # *weight_ak4_jetpt
    # ('SignalRegion2b_Mu45DRCut', sel.sr2b_channel + sel.mu_channel + sel.dr_cut, 'weight*weight_ak4_jetpt'), # *weight_ak4_jetpt
    # ('SignalRegion1b_Mu45DRCut', sel.sr1b_channel + sel.mu_channel + sel.dr_cut, 'weight*weight_ak4_jetpt'), # *weight_ak4_jetpt
    # ('SidebandRegion_Mu45DRCut', sel.sb_channel + sel.mu_channel + sel.dr_cut_invert, 'weight*weight_ak4_jetpt'), # *weight_ak4_jetpt
    # ('SignalRegion2b_1addB_3ak8', sel.sr2b_selection_1b_3ak8, 'weight'),
    # ('SignalRegion1b_1addB_3ak8', sel.sr1b_selection_1b_3ak8, 'weight'),
    # ('SidebandRegion_1addB_3ak8', sel.sb_selection_1b_3ak8, 'weight'),
    # ('SignalRegion2b_1addB_2ak8', sel.sr2b_selection_1b_2ak8, sample_weights),
    # ('SignalRegion1b_1addB_2ak8', sel.sr1b_selection_1b_2ak8, sample_weights),
    # ('SidebandRegion_1addB_2ak8', sel.sb_selection_1b_2ak8, sample_weights),
]


def mk_tp(input_pat):
    all_files = glob.glob(join(input_pat, 'Files_and_Plots_nominal/SFrame/workdir/uhh2.AnalysisModuleRunner.*.root'))
    filenames = dict(
        (sample, list(f for f in all_files if sample in f))
        for sample in samples
    )

    return TreeProjector(
        filenames, params, sec_sel_weight, 
        # suppress_job_submission=True, 
        name='TreeProjector',
    )


def mk_sys_tps(base_path):
    # some defs
    # base_path = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII-25ns-v2/'\
    #     'CMSSW_7_4_15_patch1/src/UHH2/VLQToHiggsPairProd/Samples-25ns-v2/'\
    #     'TpTpFinalSelectionTreeOutput-v0wBTagSF/Files_and_Plots/'
    sys_params = {
        'histos': core_histos,
        'treename': 'AnalysisTree',
    }

    # first put together jerc uncert with nominal weights
    jercs = list(
        (
            name.replace('_down', '__minus').replace('_up', '__plus'), 
            join(base_path, 'Files_and_Plots_' + name + '/SFrame/workdir/uhh2*.root')
        ) 
        for name in ('jec_down', 'jec_up', 'jer_down', 'jer_up')
    )
    nominal_sec_sel_weight = [
        ('BaseLineSelectionEl45', sel.el_channel, sample_weights), # *weight_ak4_jetpt
        ('BaseLineSelectionMu45', sel.mu_channel, sample_weights), # *weight_ak4_jetpt
        ('SignalRegion2b_El45', sel.sr2b_channel + sel.el_channel, sample_weights),
        ('SignalRegion1b_El45', sel.sr1b_channel + sel.el_channel, sample_weights),
        ('SidebandRegion_El45', sel.sb_channel + sel.el_channel, sample_weights),
        ('SignalRegion2b_Mu45', sel.sr2b_channel + sel.mu_channel, sample_weights),
        ('SignalRegion1b_Mu45', sel.sr1b_channel + sel.mu_channel, sample_weights),
        ('SidebandRegion_Mu45', sel.sb_channel + sel.mu_channel, sample_weights),
    ]
    sys_tps = list(
        TreeProjector(
            dict(
                (sample, list(f for f in glob.glob(pat) if sample in f))
                for sample in samples_no_data
            ), 
            sys_params, 
            nominal_sec_sel_weight,
            add_aliases_to_analysis=False,
            name=name,
        )
        for name, pat in jercs
    )

    # next put together nominal samples with with weight uncerts.
    nominal_files = join(base_path, 'Files_and_Plots_nominal/SFrame/workdir/uhh2*.root') 
    filenames = dict(
        (sample, list(f for f in glob.glob(nominal_files) if sample in f))
        for sample in samples_no_data
    )
    sys_sec_sel_weight = list(
        (name, [
            ('BaseLineSelectionEl45', sel.el_channel, dict((a, f+w) for a, f in sample_weights.iteritems())), # *weight_ak4_jetpt
            ('BaseLineSelectionMu45', sel.mu_channel, dict((a, f+w) for a, f in sample_weights.iteritems())), # *weight_ak4_jetpt
            # ('BaseLineSelection', sel.baseline_selection, dict((a, f+w) for a, f in sample_weights.iteritems())),
            ('SignalRegion2b_El45', sel.sr2b_channel + sel.el_channel, dict((a, f+w) for a, f in sample_weights.iteritems())),
            ('SignalRegion1b_El45', sel.sr1b_channel + sel.el_channel, dict((a, f+w) for a, f in sample_weights.iteritems())),
            ('SidebandRegion_El45', sel.sb_channel + sel.el_channel, dict((a, f+w) for a, f in sample_weights.iteritems())),
            ('SignalRegion2b_Mu45', sel.sr2b_channel + sel.mu_channel, dict((a, f+w) for a, f in sample_weights.iteritems())),
            ('SignalRegion1b_Mu45', sel.sr1b_channel + sel.mu_channel, dict((a, f+w) for a, f in sample_weights.iteritems())),
            ('SidebandRegion_Mu45', sel.sb_channel + sel.mu_channel, dict((a, f+w) for a, f in sample_weights.iteritems())),
        ])
        # (name, [
        #     ('BaseLineSelectionEl45', sel.el_channel, sample_weights), # *weight_ak4_jetpt
        #     ('BaseLineSelectionMu45', sel.mu_channel, sample_weights), # *weight_ak4_jetpt
        #     ('SignalRegion2b_El45', sel.sr2b_channel + sel.el_channel, sample_weights),
        #     ('SignalRegion1b_El45', sel.sr1b_channel + sel.el_channel, sample_weights),
        #     ('SidebandRegion_El45', sel.sb_channel + sel.el_channel, sample_weights),
        #     ('SignalRegion2b_Mu45', sel.sr2b_channel + sel.mu_channel, sample_weights),
        #     ('SignalRegion1b_Mu45', sel.sr1b_channel + sel.mu_channel, sample_weights),
        #     ('SidebandRegion_Mu45', sel.sb_channel + sel.mu_channel, sample_weights),
        # ])
        for name, w in (
            ('btag_bc__minus', '*weight_btag_bc_down/weight_btag'),
            ('btag_bc__plus', '*weight_btag_bc_up/weight_btag'),
            ('btag_udsg__minus', '*weight_btag_udsg_down/weight_btag'),
            ('btag_udsg__plus', '*weight_btag_udsg_up/weight_btag'),
            ('sfmu_id__minus', '*weight_sfmu_id_down/weight_sfmu_id'),
            ('sfmu_id__plus', '*weight_sfmu_id_up/weight_sfmu_id'),
            ('sfmu_trg__minus', '*weight_sfmu_trg_down/weight_sfmu_trg'),
            ('sfmu_trg__plus', '*weight_sfmu_trg_up/weight_sfmu_trg'),
            ('pu__minus', '*weight_pu_down/weight_pu'),
            ('pu__plus', '*weight_pu_up/weight_pu'),
            ('ak4_jetpt__minus', '*weight_ak4_jetpt_down/weight_ak4_jetpt'),
            ('ak4_jetpt__plus', '*weight_ak4_jetpt_up/weight_ak4_jetpt'),
        )
    )
    sys_tps += list(
        TreeProjector(
            filenames,
            sys_params, 
            ssw,
            add_aliases_to_analysis=False,
            name=name,
        )
        for name, ssw in sys_sec_sel_weight
    )

    # make it complete with a tooloolchain!
    return varial.tools.ToolChain(
        'SysTreeProjectors', sys_tps
    )

import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Input file pattern needed!'
        exit(-1)
    input_pat = sys.argv[1]
    varial.tools.Runner(mk_tp(input_pat))

