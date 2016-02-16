#!/usr/bin/env python

baseline_selection = [
    'gendecay_accept        == 1',
    # 'n_ak8_cleaned          >= 2'
]

sr2b_channel = baseline_selection + [
    'n_higgs_tags_2b_med    >= 1',
    # 'n_additional_btags_medium  >= 1',
]

sr1b_channel = baseline_selection + [
    'n_higgs_tags_2b_med    == 0',
    'n_higgs_tags_1b_med    >= 1',
    # 'n_additional_btags_medium  >= 1',
]

sb_channel = baseline_selection + [
    'n_higgs_tags_1b_med        == 0',
    # 'n_additional_btags_medium  >= 1',
]

sr2b_channel_clean = baseline_selection + [
    'n_ak8_cleaned          >= 2',
    'n_higgs_tags_2b_med_cleaned    >= 1',
    # 'n_additional_btags_medium  >= 1',
]

sr1b_channel_clean = baseline_selection + [
    'n_ak8_cleaned          >= 2',
    'n_higgs_tags_2b_med_cleaned    == 0',
    'n_higgs_tags_1b_med_cleaned    >= 1',
    # 'n_additional_btags_medium  >= 1',
]

sb_channel_clean = baseline_selection + [
    'n_ak8_cleaned          >= 2',
    'n_higgs_tags_1b_med_cleaned        == 0',
    # 'n_additional_btags_medium  >= 1',
]

sb_wjets_channel = baseline_selection + [
    'n_higgs_tags_1b_med        == 0',
    # 'n_additional_btags_medium  == 0',
]

el_channel = [
    'trigger_accept_el45   >= 1',
    'trigger_accept_mu45   == 0',
    'pt_ld_ak4_jet         > 250.',
    'pt_subld_ak4_jet      > 65.',
    'primary_lepton_pt     > 50.'
]

mu_channel = [
    'trigger_accept_mu45   >= 1',
    'primary_lepton_pt     > 47.'
]

eliso_channel = [
    'trigger_accept_isoEl27   >= 1'
]

muiso_channel = [
    'trigger_accept_isoMu20   >= 1'
]

dr_cut = [
    'first_ak8jet_dRak8    <= 2.8'
]
dr_cut_invert = [
    'first_ak8jet_dRak8    > 2.8'
]

# Electron channel

sr2b_el_channel = baseline_selection + [
    'is_muon                == 0',
    'n_higgs_tags_2b_med    >= 1',
    'n_additional_btags_medium  >= 1',
]
sr1b_el_channel = baseline_selection + [
    'is_muon                == 0',
    'n_higgs_tags_2b_med    == 0',
    'n_higgs_tags_1b_med    >= 1',
    'n_additional_btags_medium  >= 1',
]
sb_el_channel = baseline_selection + [
    'is_muon                == 0',
    'n_higgs_tags_1b_med        == 0',
    'n_additional_btags_medium  >= 1',
]

# Muon channel

sr2b_mu_channel = baseline_selection + [
    'is_muon                == 1',
    'n_higgs_tags_2b_med    >= 1',
    'n_additional_btags_medium  >= 1',
]
sr1b_mu_channel = baseline_selection + [
    'is_muon                == 1',
    'n_higgs_tags_2b_med    == 0',
    'n_higgs_tags_1b_med    >= 1',
    'n_additional_btags_medium  >= 1',
]
sb_mu_channel = baseline_selection + [
    'is_muon                == 1',
    'n_higgs_tags_1b_med        == 0',
    'n_additional_btags_medium  >= 1',
]


# No btag, 3 Ak8

sr2b_selection_0b_3ak8 = baseline_selection + [
    'n_higgs_tags_2b_med    >= 1',
    'n_ak8                  >= 3'
]
sr1b_selection_0b_3ak8 = baseline_selection + [
    'n_higgs_tags_2b_med    == 0',
    'n_higgs_tags_1b_med    >= 1',
    'n_ak8                  >= 3'
]
sb_selection_0b_3ak8 = baseline_selection + [
    'n_higgs_tags_1b_med        == 0',
    'n_additional_btags_medium  >= 1',
    'n_ak8                  >= 3'
]

# With btag, 3 Ak8

sr2b_selection_1b_3ak8 = baseline_selection + [
    'n_higgs_tags_2b_med    >= 1',
    'n_additional_btags_medium  >= 1',
    'n_ak8                  >= 3'
]
sr1b_selection_1b_3ak8 = baseline_selection + [
    'n_higgs_tags_2b_med    == 0',
    'n_higgs_tags_1b_med    >= 1',
    'n_additional_btags_medium  >= 1',
    'n_ak8                  >= 3'
]
sb_selection_1b_3ak8 = baseline_selection + [
    'n_higgs_tags_1b_med        == 0',
    'n_additional_btags_medium  >= 1',
    'n_ak8                  >= 3'
]

# No btag, 2 Ak8

sr2b_selection_0b_2ak8 = baseline_selection + [
    'n_higgs_tags_2b_med    >= 1',
    'n_ak8                  >= 2'
]
sr1b_selection_0b_2ak8 = baseline_selection + [
    'n_higgs_tags_2b_med    == 0',
    'n_higgs_tags_1b_med    >= 1',
    'n_ak8                  >= 2'
]
sb_selection_0b_2ak8 = baseline_selection + [
    'n_higgs_tags_1b_med        == 0',
    'n_additional_btags_medium  >= 1',
    'n_ak8                  >= 2'
]

# With btag, 2 Ak8

sr2b_selection_1b_2ak8 = baseline_selection + [
    'n_higgs_tags_2b_med    >= 1',
    'n_additional_btags_medium  >= 1',
    'n_ak8                  >= 2'
]
sr1b_selection_1b_2ak8 = baseline_selection + [
    'n_higgs_tags_2b_med    == 0',
    'n_higgs_tags_1b_med    >= 1',
    'n_additional_btags_medium  >= 1',
    'n_ak8                  >= 2'
]
sb_selection_1b_2ak8 = baseline_selection + [
    'n_higgs_tags_1b_med        == 0',
    'n_additional_btags_medium  >= 1',
    'n_ak8                  >= 2'
]