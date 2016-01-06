#!/usr/bin/env python

from varial_ext.treeprojector import TreeProjector, SGETreeProjector
from os.path import join
import varial.tools
import glob


histo_names_args = {
    'gendecay_accept' :            ('GenDecay Accept',                  2, -.5, 1.5),
    'n_ak8' :                      ('N(Ak8 Jets)',                      8, -.5, 7.5),
    'ST' :                         ('ST',                               45, 0, 4500),
    'pt_ld_ak8_jet' :              ('Pt leading Ak8 Jet',               60, 0., 1500.),
    'primary_muon_pt_noIso' :      ('Primary Muon p_T',                 90, 0., 900.),
    'n_higgs_tags_1b_med' :        ('N(Higgs Tags, 1 b)',               8, -.5, 7.5),
    'n_higgs_tags_2b_med' :        ('N(Higgs Tags, 2 b)',               8, -.5, 7.5),
    'n_ak8_higgs_cand' :           ('N(Higgs Candidates)',              8, -.5, 7.5),
    'n_jets_no_overlap' :          ('N(non-overlapping Ak4 jets)',      12, -.5, 11.5),
    'max_n_subjet_btags' :         ('max N(medium sj b-tags)',          4, -.5, 3.5),
    'mass_higgs_cands_max_btag' :  ('Mass(Higgs cand max btag)',        30, 0., 300.),
    'n_higgs_tags_1b_med'  :       ('N(Higgs-Tags, 1 med b)',           5, -.5, 4.5),
    'n_higgs_tags_2b_med'  :       ('N(Higgs-Tags, 2 med b)',           5, -.5, 4.5),
    'n_additional_btags_medium'  : ('N(non-overlapping medium b-tags)', 8, -.5, 7.5),
    'use_sr_sf' :                  ('Use SR SF',                        2, -.5, 1.5),
}
params = {
    'histos': histo_names_args,
    'treename': 'AnalysisTree',
}

signals = [
    # 'TpTp_M-700',
    'TpTp_M-800',
    # 'TpTp_M-900',
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
    'ST',
    'QCD',
    'DYJets',
    'WJets',
    'Run2015D',
] +  reduce(lambda x, y: x+y, (list(g + f for f in final_states) for g in signals))

baseline_selection = [
    'gendecay_accept        == 1',
    'n_ak8                  > 2'
]

sr2b_selection = baseline_selection + [
    'n_higgs_tags_2b_med    >= 1',
]
sr1b_selection = baseline_selection + [
    'n_higgs_tags_2b_med    == 0',
    'n_higgs_tags_1b_med    >= 1',
]

sb_selection = baseline_selection + [
    'n_higgs_tags_1b_med        == 0',
    'n_additional_btags_medium  >= 1',
]


sec_sel_weight = [
    ('BaseLineSelection', baseline_selection, 'weight'),
    ('SignalRegion2b', sr2b_selection, 'weight'),
    ('SignalRegion1b', sr1b_selection, 'weight'),
    ('SidebandRegion', sb_selection, 'weight'),
]


def mk_tp(input_pat):
    all_files = glob.glob(input_pat)
    filenames = dict(
        (sample, list(f for f in all_files if sample in f))
        for sample in samples
    )

    return TreeProjector(
        samples, filenames, params, sec_sel_weight, 
        # suppress_job_submission=True, 
        name='TreeProjector',
    )


def mk_sys_tps():
    # some defs
    base_path = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII-25ns-v2/'\
        'CMSSW_7_4_15_patch1/src/UHH2/VLQToHiggsPairProd/Samples-25ns-v2/'\
        'TpTpFinalSelectionTreeOutput-v0wBTagSF/Files_and_Plots/'
    sys_params = {
        'histos': {'ST': histo_names_args['ST']},
        'treename': 'AnalysisTree',
    }

    # first put together jerc uncert with nominal weights
    jercs = list(
        (
            name.replace('_down', '__minus').replace('_up', '__plus'), 
            base_path + 'Files_and_Plots_' + name + '/SFrame/' + name + '/workdir/uhh2*.root'
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
    nominal_files = base_path + 'Files_and_Plots_nominal/SFrame/nominal/workdir/uhh2*.root' 
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
            samples, 
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

