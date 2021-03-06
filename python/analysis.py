#!/usr/bin/env python


# import UHH2.VLQSemiLepPreSel.vlq_settings as vlq_settings
# import UHH2.VLQSemiLepPreSel.common as common
# import tptpfinalselection
# import tptplooseselection
# import tptptightselection
# import tptppreselection
# import sensitivity
# import tex_content

# import varial.tools
# import varial.extensions.git as git
# import varial.extensions.make as make
# import os
# import sys

# import tptp_settings


ttbar_smpl = 'TTbar_split'


rate_uncertainties = {
    'TTbar' : 1.087,
    'WJets' : 1.06,
    'QCD' : 2.0,
    # 'DYJets' : 1.20,
    'SingleTop' : 1.16,
    'Diboson' : 1.15
}

def_uncerts = [
    'jec',
    'jer',
    'btag_bc',
    'btag_udsg',
    'sfmu_id',
    'sfmu_trg',
    'sfel_id',
    # 'sfel_trg',
    'sflep_id',
    'sflep_trg',
    'pu',
    'PDF',
    'ScaleVar',
    'rate',
    'PSScale',
    'higgs_smear',
    'higgs_scale',
    # 'top_pt_weight',
    # 'sflep_id',
    # 'sflep_trg'
]

all_uncerts = def_uncerts + ['ht_reweight', 'jsf']
shape_uncertainties = all_uncerts

more_uncerts = def_uncerts + ['ht_reweight_one_side', 'top_pt_reweight_one_side']

