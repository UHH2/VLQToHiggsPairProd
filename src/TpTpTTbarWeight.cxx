#include <iostream>
#include <memory>

#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Event.h"
#include "UHH2/core/include/Utils.h"
#include "UHH2/common/include/CleaningModules.h"
#include "UHH2/common/include/CommonModules.h"
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
#include "UHH2/common/include/TTbarGen.h"


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

class TpTpTTbarWeight: public AnalysisModule {
public:

    explicit TpTpTTbarWeight(Context & ctx);
    virtual bool process(Event & event);

protected:
    

    // void swap_selitems(vector<shared_ptr<SelectionItem>> & sel_items,
    //                    SelectionItem * new_item, int new_pos = -1) {
    //     unsigned insert_pos = new_pos >= 0 ? new_pos : 0;
    //     for (unsigned i = 0; i < sel_items.size(); ++i) {
    //         if (sel_items[i]->name() == new_item->name()) {
    //             sel_items.erase(sel_items.begin()+i);
    //             insert_pos = new_pos >= 0 ? new_pos : i;
    //         }
    //     }
    //     sel_items.insert(sel_items.begin()+insert_pos, shared_ptr<SelectionItem>(move(new_item)));
    // }

    // modules for setting up collections and cleaning
    vector<unique_ptr<AnalysisModule>> other_modules;
    vector<vector<unique_ptr<Hists>>> v_hists;


    // check category
    // unique_ptr<Selection> cat_check_module;

    // Event::Handle<int> h_ngenleps;
};

TpTpTTbarWeight::TpTpTTbarWeight(Context & ctx) {
    // If needed, access the configuration of the module here, e.g.:
    // string testvalue = ctx.get("TestKey", "<not set>");
    // cout << "TestKey in the configuration was: " << testvalue << endl;

    other_modules.emplace_back(new TTbarGenProducer(ctx, "ttbargen"));
    other_modules.emplace_back(new TopPtWeight(ctx, "ttbargen", 0.159, -0.00141));

    v_hists.emplace_back(vector<unique_ptr<Hists>>());
    v_hists.back().emplace_back(new TopPtWeightHist(ctx, "TTbarWeight", "weight_ttbar"));
}


bool TpTpTTbarWeight::process(Event & event) {

    // run all modules

    // sort_by_pt(*event.jets);
    // sort_by_pt(*event.topjets);
    // sort_by_pt(event.get(patjets_));

    // std::cout << "AFTER lepton cleaning:\n";
    // std::cout << "  Ak4 jets:";
    // for (auto const & jet : *event.jets) {std::cout << " " << jet.pt();}
    // std::cout << std::endl;
    // std::cout << "  Slimmed Ak8 jets:";
    // for (auto const & jet : *event.topjets) {std::cout << " " << jet.pt();}
    // std::cout << std::endl;
    // std::cout << "  Packed Ak8 jets:";
    // for (auto const & jet : event.get(patjets_)) {std::cout << " " << jet.pt();}
    // std::cout << std::endl;

    for (auto & mod : other_modules) {
        mod->process(event);
    }

    // all hists
    for (auto & hist_vec : v_hists) {
        for (auto & hist : hist_vec) {
            hist->fill(event);
        }
    }

    // fill histograms without selection
    // for (auto & hist : v_hists_nosel) {
    //     hist->fill(event);
    // }

    // decide whether or not to keep the current event in the output:
    return false;
}

UHH2_REGISTER_ANALYSIS_MODULE(TpTpTTbarWeight)
