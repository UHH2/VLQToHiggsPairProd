#!/usr/bin/env python

from varial_ext.treeprojector import TreeProjector #, SGETreeProjector
from os.path import join
import varial.tools
import glob


histo_names_args = {
    'gendecay_accept'               : ('GenDecay Accept',                  2, -.5, 1.5),
    'ST'                            : ('ST',                               45, 0, 4500),
    # 'ST_cleaned'                    : ('ST cleaned',                       45, 0, 4500),
    'n_additional_btags_medium'     : ('N(non-overlapping medium b-tags)', 8, -.5, 7.5),
    'n_ak4'                         : ('N(Ak4 Jets)',                      14, -.5, 13.5),
    # 'n_ak4_pt_cleaned'              : ('N(Ak4 Jets, cleaned)',             14, -.5, 13.5),
    'n_ak8'                         : ('N(Ak8 Jets)',                      8, -.5, 7.5),
    # 'n_ak8_pt_cleaned'              : ('N(Ak8 Jets, cleaned)',             8, -.5, 7.5),
    'n_ak8_higgs_cand'              : ('N(Higgs Candidates)',              8, -.5, 7.5),
    'n_higgs_tags_1b_med'           : ('N(Higgs-Tags, 1 med b)',           5, -.5, 4.5),
    'n_higgs_tags_2b_med'           : ('N(Higgs-Tags, 2 med b)',           5, -.5, 4.5),
    'n_jets_no_overlap'             : ('N(non-overlapping Ak4 jets)',      12, -.5, 11.5),
    'primary_lepton_pt'             : ('Primary Lepton p_T',               90, 0., 900.),
    'pt_ld_ak4_jet'                 : ('Pt leading Ak4 Jet',               60, 0., 1500.),
    # 'pt_ld_ak4_jet_cleaned'         : ('Pt leading Ak4 Jet, cleaned',      60, 0., 1500.),
    'pt_ld_ak8_jet'                 : ('Pt leading Ak8 Jet',               60, 0., 1500.),
    # 'pt_ld_ak8_jet_cleaned'         : ('Pt leading Ak8 Jet, cleaned',      60, 0., 1500.),
    'deltaRlep_topjets_1'           : ('dR(1st TopJet, primary lepton)',   50, 0., 5.),
    'deltaRak4_topjets_1'           : ('dR(1st TopJet, nearest Ak4 Jet)',  50, 0., 5.),
    'deltaRak8_topjets_1'           : ('dR(1st TopJet, nearest Ak8 Jet)',  50, 0., 5.),
    'deltaRlep_topjets_2'           : ('dR(2nd TopJet, primary lepton)',   50, 0., 5.),
    'deltaRak4_topjets_2'           : ('dR(2nd TopJet, nearest Ak4 Jet)',  50, 0., 5.),
    'deltaRak8_topjets_2'           : ('dR(2nd TopJet, nearest Ak8 Jet)',  50, 0., 5.),
    'deltaRlep_higgs_tags_1b_med_1' : ('dR(H-Tag(1b), primary lepton)',    50, 0., 5.),
    'deltaRak4_higgs_tags_1b_med_1' : ('dR(H-Tag(1b), nearest Ak4 Jet)',   50, 0., 5.),
    'deltaRak8_higgs_tags_1b_med_1' : ('dR(H-Tag(1b), nearest Ak8 Jet)',   50, 0., 5.),
    'deltaRlep_higgs_tags_2b_med_1' : ('dR(H-Tag(2b), primary lepton)',    50, 0., 5.),
    'deltaRak4_higgs_tags_2b_med_1' : ('dR(H-Tag(2b), nearest Ak4 Jet)',   50, 0., 5.),
    'deltaRak8_higgs_tags_2b_med_1' : ('dR(H-Tag(2b), nearest Ak8 Jet)',   50, 0., 5.),
    # 'topjeteta_1'                : ('Eta 1st Ak8 Jet',                  50, -3., 3.),
    # 'topjeteta_2'                : ('Eta 2nd Ak8 Jet',                  50, -3., 3.),
    # 'topjetmass_1'               : ('Mass 1st Ak8 Jet',                 60, 0., 300.),
    # 'topjetmass_2'               : ('Mass 2nd Ak8 Jet',                 60, 0., 300.),
    # 'topjetnsjbtags_1'           : ('N(med sj b-tags) 1st Ak8 Jet',     4, -.5, 3.5),
    # 'topjetnsjbtags_2'           : ('N(med sj b-tags) 2nd Ak8 Jet',     4, -.5, 3.5),
    # 'topjetpt_1'                 : ('Pt 1st Ak8 Jet',                   60, 0., 1500.),
    # 'topjetpt_2'                 : ('Pt 2nd Ak8 Jet',                   60, 0., 1500.),
    'trigger_accept_mu45'           : ('Trigger Accepted Mu45',             2, -.5, 1.5),
    'trigger_accept_el40'           : ('Trigger Accepted El40',             2, -.5, 1.5),
    'trigger_accept_isoMu'          : ('Trigger Accepted IsoMu',            2, -.5, 1.5),
    'is_muon'                       : ('Prim. Lep. is Muon',                2, -.5, 1.5),
    'use_sr_sf'                     : ('Use SR SF',                         2, -.5, 1.5),
}
params = {
    'histos': histo_names_args,
    'treename': 'AnalysisTree',
}

signals = [
    'TpTp_M-700',
    'TpTp_M-800',
    'TpTp_M-900',
    'TpTp_M-1000',
    # 'TpTp_M-1100',
    'TpTp_M-1200',
    # 'TpTp_M-1300',
    'TpTp_M-1400',
    # 'TpTp_M-1500',
    'TpTp_M-1600',
    # 'TpTp_M-1700',
    # 'TpTp_M-1800',
]

final_states = [
    '_thth',
    '_thtz',
    '_thbw',
    '_noH_tztz',
    '_noH_tzbw',
    '_noH_bwbw',
]

samples = [
    'TTbar',
    'SingleTop',
    'QCD',
    'DYJets',
    'WJets',
    'Run2015D',
] +  reduce(lambda x, y: x+y, (list(g + f for f in final_states) for g in signals))


import tptp_selections_treeproject as sel






sec_sel_weight = [
    ('BaseLineSelection', sel.baseline_selection, 'weight'), # *ak4_jetpt_weight
    ('SignalRegion2b_Electron', sel.sr2b_el_channel, 'weight'), # *ak4_jetpt_weight
    ('SignalRegion1b_Electron', sel.sr1b_el_channel, 'weight'), # *ak4_jetpt_weight
    ('SidebandRegion_Electron', sel.sb_el_channel, 'weight'), # *ak4_jetpt_weight
    ('SignalRegion2b_Muon', sel.sr2b_mu_channel, 'weight'), # *ak4_jetpt_weight
    ('SignalRegion1b_Muon', sel.sr1b_mu_channel, 'weight'), # *ak4_jetpt_weight
    ('SidebandRegion_Muon', sel.sb_mu_channel, 'weight'), # *ak4_jetpt_weight
    # ('SignalRegion2b_1addB_3ak8', sel.sr2b_selection_1b_3ak8, 'weight'),
    # ('SignalRegion1b_1addB_3ak8', sel.sr1b_selection_1b_3ak8, 'weight'),
    # ('SidebandRegion_1addB_3ak8', sel.sb_selection_1b_3ak8, 'weight'),
    # ('SignalRegion2b_1addB_2ak8', sel.sr2b_selection_1b_2ak8, 'weight'),
    # ('SignalRegion1b_1addB_2ak8', sel.sr1b_selection_1b_2ak8, 'weight'),
    # ('SidebandRegion_1addB_2ak8', sel.sb_selection_1b_2ak8, 'weight'),
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
        'histos': {'ST': histo_names_args['ST']},
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
        ('SignalRegion2b', sr2b_selection, 'weight'),
        ('SignalRegion1b', sr1b_selection, 'weight'),
        ('SidebandRegion', sb_selection, 'weight'),
    ]
    sys_tps = list(
        TreeProjector(
            samples, 
            dict(
                (sample, list(f for f in glob.glob(pat) if sample in f))
                for sample in samples
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
        for sample in samples
    )
    sys_sec_sel_weight = list(
        (name, [
            ('SignalRegion2b', sr2b_selection, 'weight*' + w),
            ('SignalRegion1b', sr1b_selection, 'weight*' + w),            
            ('SidebandRegion', sb_selection, 'weight*' + w),
        ])
        for name, w in (
            ('btag_bc__minus', 'weight_btag_bc_down/weight_btag'),
            ('btag_bc__plus', 'weight_btag_bc_up/weight_btag'),
            ('btag_udsg__minus', 'weight_btag_udsg_down/weight_btag'),
            ('btag_udsg__plus', 'weight_btag_udsg_up/weight_btag'),
            ('sfmu_id__minus', 'weight_sfmu_id_down/weight_sfmu_id'),
            ('sfmu_id__plus', 'weight_sfmu_id_up/weight_sfmu_id'),
            ('sfmu_trg__minus', 'weight_sfmu_trg_down/weight_sfmu_trg'),
            ('sfmu_trg__plus', 'weight_sfmu_trg_up/weight_sfmu_trg'),
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

