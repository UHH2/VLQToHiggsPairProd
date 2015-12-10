#pragma once

#include <vector>
#include "TH2F.h"

#include "UHH2/common/include/Utils.h"
#include "UHH2/VLQSemiLepPreSel/include/SelectionItem.h"


static const vector<std::string> QCDTEST_MUON_TRIGGER_PATHS {
    // "HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v*",
    // "HLT_Ele105_CaloIdVT_GsfTrkIdT_v*",
    // "HLT_Ele32_eta2p1_WP75_Gsf_v*",

    // "HLT_Mu40_eta2p1_PFJet200_PFJet50_v*",
    "HLT_Mu45_eta2p1_v*",
    // "HLT_Mu50_v*",
    // "HLT_IsoMu24_eta2p1_v*",
    // "HLT_IsoMu27_v*",

    // "HLT_PFHT800Emu_v*",
};

static const vector<std::string> QCDTEST_MUON_TRIGGER_PATHS_DATA {
    // "HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v*",
    // "HLT_Ele105_CaloIdVT_GsfTrkIdT_v*",
    // "HLT_Ele32_eta2p1_WPLoose_Gsf_v*",

    // "HLT_Mu40_eta2p1_PFJet200_PFJet50_v*",
    "HLT_Mu45_eta2p1_v*",
    // "HLT_Mu50_v*",
    // "HLT_IsoMu24_eta2p1_v*",
    // "HLT_IsoMu27_v*",

    // "HLT_PFHT800_v*",
};

static const vector<std::string> QCDTEST_MUON_TRIGGER_PATHS_DATA_ELE_VETO {
    // "HLT_Mu40_eta2p1_PFJet200_PFJet50_v*",
    "HLT_Mu45_eta2p1_v*",
    "HLT_Mu50_v*",
    "HLT_IsoMu24_eta2p1_v*",
    "HLT_IsoMu27_v*",
};

static const vector<std::string> QCDTEST_MUON_TRIGGER_PATHS_DATA_HAD_VETO {
    // "HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v*",
    "HLT_Ele105_CaloIdVT_GsfTrkIdT_v*",
    "HLT_Ele32_eta2p1_WPLoose_Gsf_v*",

    // "HLT_Mu40_eta2p1_PFJet200_PFJet50_v*",
    "HLT_Mu45_eta2p1_v*",
    "HLT_Mu50_v*",
    "HLT_IsoMu24_eta2p1_v*",
    "HLT_IsoMu27_v*",
};