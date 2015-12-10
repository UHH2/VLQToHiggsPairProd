#pragma once

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

class TpTpAnalysisModule: public AnalysisModule {
public:

    explicit TpTpAnalysisModule(Context & ctx);
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

    string version, type;
    // modules for setting up collections and cleaning
    vector<unique_ptr<AnalysisModule>> other_modules, common_modules;
    vector<unique_ptr<SelectionProducer>> sel_modules;
    vector<bool> sel_modules_passed;
    vector<unique_ptr<SelItemsHelper>> sel_helpers;
    // unique_ptr<AnalysisModule> writer_module; // for TMVA stuff

    // store the Hists collection
    unique_ptr<Hists> gen_hists;
    vector<unique_ptr<Hists>> v_hists_nosel;
    vector<vector<unique_ptr<Hists>>> v_hists;
    vector<vector<unique_ptr<Hists>>> v_hists_after_sel;

    vector<vector<shared_ptr<SelectionItem>>> SEL_ITEMS_FULL_SEL;

    // check category
    // unique_ptr<Selection> cat_check_module;

    // Event::Handle<int> h_ngenleps;
};