#include <iostream>
#include <memory>

#include "UHH2/VLQToHiggsPairProd/include/TpTpAnalysisModule.h"

#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Event.h"
#include "UHH2/core/include/Utils.h"
#include "UHH2/common/include/CleaningModules.h"
#include "UHH2/common/include/ElectronIds.h"
#include "UHH2/common/include/MuonIds.h"
#include "UHH2/common/include/EventVariables.h"
#include "UHH2/common/include/JetIds.h"
#include "UHH2/common/include/TopJetIds.h"
#include "UHH2/common/include/NSelections.h"
#include "UHH2/common/include/GenTools.h"
#include "UHH2/common/include/PartonHT.h"
#include "UHH2/common/include/JetCorrections.h"
#include "UHH2/common/include/MCWeight.h"
#include "UHH2/common/include/TTbarReconstruction.h"
#include "UHH2/common/include/ObjectIdUtils.h"
#include "UHH2/common/include/AdditionalSelections.h"
#include "UHH2/common/include/CollectionProducer.h"
#include "UHH2/common/include/PrintingModules.h"


#include "UHH2/VLQSemiLepPreSel/include/EventHists.h"
#include "UHH2/VLQSemiLepPreSel/include/CustomizableGenHists.h"
#include "UHH2/VLQSemiLepPreSel/include/VLQCommonModules.h"
#include "UHH2/VLQSemiLepPreSel/include/SelectionHists.h"
#include "UHH2/VLQSemiLepPreSel/include/SelectionItem.h"
// #include "UHH2/VLQToHiggsPairProd/include/VLQPair_selectionItems.h"
#include "UHH2/VLQToHiggsPairProd/include/VLQPair_additionalModules.h"
#include "UHH2/VLQToHiggsPairProd/include/VLQPair_additionalHists.h"
// #include "UHH2/VLQToHiggsPairProd/include/VLQPair_triggerPaths.h"
// #include "UHH2/VLQToHiggsPairProd/include/TpTpCommonModules.h"

using namespace std;
using namespace uhh2;

TpTpAnalysisModule::TpTpAnalysisModule(Context & ctx) {
    // If needed, access the configuration of the module here, e.g.:
    // string testvalue = ctx.get("TestKey", "<not set>");
    // cout << "TestKey in the configuration was: " << testvalue << endl;
    version = ctx.get("dataset_version", "");
    type = ctx.get("dataset_type", "");
    // type = ctx.get("cycle_type", "PreSelection");
    
    // If running in SFrame, the keys "dataset_version", "dataset_type" and "dataset_lumi"
    // are set to the according values in the xml file. For CMSSW, these are
    // not set automatically, but can be set in the python config file.
    for(auto & kv : ctx.get_all()){
        cout << " " << kv.first << " = " << kv.second << endl;
    }

    common_modules.emplace_back(new PrimaryLepton(ctx, "PrimaryLepton", 9999.f, 10.f)); 
    common_modules.emplace_back(new PrimaryLeptonOwn<Muon>(ctx, "muons", "PrimaryMuon_noIso"));
    // common_modules.emplace_back(new PrimaryLeptonOwn<Muon>(ctx, "muons", "PrimaryMuon_dRak8", MuonId(MinMaxDeltaRId<TopJet>(ctx, "topjets", 0.1))));
    common_modules.emplace_back(new HTCalculator(ctx, boost::none, "HT"));
    common_modules.emplace_back(new STCalculator(ctx, "ST"));
    common_modules.emplace_back(new CollectionProducer<Jet>(ctx,
        "jets",
        "b_jets_loose",
        JetId(CSVBTag(CSVBTag::WP_LOOSE))
        ));
    common_modules.emplace_back(new CollectionProducer<Jet>(ctx,
        "jets",
        "b_jets_medium",
        JetId(CSVBTag(CSVBTag::WP_MEDIUM))
        ));
    common_modules.emplace_back(new CollectionProducer<Jet>(ctx,
        "jets",
        "b_jets_tight",
        JetId(CSVBTag(CSVBTag::WP_TIGHT))
        ));
    common_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
        "b_jets_loose",
        "n_btags_loose"
        // JetId(CSVBTag(CSVBTag::WP_LOOSE))
        ));
    common_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
        "b_jets_medium",
        "n_btags_medium"
        // JetId(CSVBTag(CSVBTag::WP_MEDIUM))
        ));
    common_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
        "b_jets_tight",
        "n_btags_tight"
        // JetId(CSVBTag(CSVBTag::WP_TIGHT))
        ));


    // Other CutProducers
    common_modules.emplace_back(new NLeptonsProducer(ctx, "n_leptons"));
    common_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx, "jets", "n_jets"));
    common_modules.emplace_back(new METProducer(ctx, "met"));
    common_modules.emplace_back(new PartPtProducer<Jet>(ctx, "jets", "leading_jet_pt", 1));
    common_modules.emplace_back(new PartPtProducer<Jet>(ctx, "jets", "subleading_jet_pt", 2));
    common_modules.emplace_back(new PartPtProducer<Muon>(ctx, "muons", "leading_mu_pt", 1));
    common_modules.emplace_back(new PartPtProducer<Electron>(ctx, "electrons", "leading_ele_pt", 1));

    // get pt of the top tagged jet with smallest pt, just to see if PtEtaCut Id is working
    // common_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "toptags", "smallest_pt_toptags", -1));

    common_modules.emplace_back(new PrimaryLeptonInfoProducer(ctx, "PrimaryLepton", "primary_lepton_pt"));
    common_modules.emplace_back(new PrimaryLeptonInfoProducer(ctx, "PrimaryMuon_noIso", "primary_muon_pt_noIso", "primary_muon_eta_noIso", "primary_muon_charge_noIso"));

    // class that takes care of applying CommonModules (with JEC, jet-lepton-cleaning, MCWeight etc.),
    // produces all handles for generic quantities like n_jets, met, etc.
    // tptp_commonModules.reset(new TpTpCommonModules(ctx));

    // EventWeightOutputHandle only needed for TMVA studies
    // other_common_modules.emplace_back(new EventWeightOutputHandle(ctx));

}


bool TpTpAnalysisModule::process(Event & event) {

    // run all modules

    for (auto & mod : pre_modules) {
        mod->process(event);
    }

    for (auto & mod : common_modules) {
        mod->process(event);
    }

    for (auto & mod : other_modules) {
        mod->process(event);
    }

    sel_modules_passed.clear();

    for (unsigned i = 0; i < sel_modules.size(); ++i) {
    
        bool all_accepted = sel_modules[i]->process(event);
        sel_modules_passed.push_back(all_accepted);

        // fill histograms
        if (all_accepted) {
            for (auto & hist : v_hists_after_sel[i]) {
                hist->fill(event);
            }
        }
    }

    // all hists
    for (auto & hist_vec : v_hists) {
        for (auto & hist : hist_vec) {
            hist->fill(event);
        }
    }

    // fill histograms without selection
    for (auto & hist : v_hists_nosel) {
        hist->fill(event);
    }

    // decide whether or not to keep the current event in the output:
    return true;
}
