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
#include "UHH2/VLQToHiggsPairProd/include/VLQPair_selectionItems.h"
#include "UHH2/VLQToHiggsPairProd/include/VLQPair_additionalModules.h"
#include "UHH2/VLQToHiggsPairProd/include/VLQPair_additionalHists.h"
#include "UHH2/VLQToHiggsPairProd/include/VLQPair_triggerPaths.h"
#include "UHH2/VLQToHiggsPairProd/include/TpTpCommonModules.h"

using namespace std;
using namespace uhh2;

// using namespace vlqToHiggsPair;

// typedef VectorAndSelection MyAndSelection;

static const vector<shared_ptr<SelectionItem>> SEL_ITEMS_BASELINE_SEL {
    // shared_ptr<SelectionItem>(new SelDatI("trigger_accept", "trigger accept", 2, -.5, 1.5, 1)),
    // shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt", "primary lepton p_{T}",90, 0, 900 ,25.)),
    shared_ptr<SelectionItem>(new SelDatD("ST", "ST", 25, 0, 4500, 700)),
    shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_noT", "N(Higgs-Tags)", 5, -.5, 4.5, 1)),
    // shared_ptr<SelectionItem>(new SelDatI("n_btags",                "N_{b-tag}",                              11, -.5, 10.5         ,1      )),
    // shared_ptr<SelectionItem>(new SelDatF("leading_jet_pt",         "leading jet p_{T}",                      50,   0, 1500                 )),
};

static const float DR_2D_CUT_PRESEL = 0.4;
static const float DPT_2D_CUT_PRESEL = 40.0;

class TpTpAnalysisModule: public AnalysisModule {
public:

    explicit TpTpAnalysisModule(Context & ctx);
    virtual bool process(Event & event);

private:

    void swap_selitems(vector<shared_ptr<SelectionItem>> & sel_items,
                       SelectionItem * new_item, int new_pos = -1) {
        unsigned insert_pos = new_pos >= 0 ? new_pos : 0;
        for (unsigned i = 0; i < sel_items.size(); ++i) {
            if (sel_items[i]->name() == new_item->name()) {
                sel_items.erase(sel_items.begin()+i);
                insert_pos = new_pos >= 0 ? new_pos : i;
            }
        }
        sel_items.insert(sel_items.begin()+insert_pos, shared_ptr<SelectionItem>(move(new_item)));
    }

    string version, type;
    // modules for setting up collections and cleaning
    unique_ptr<AnalysisModule> tptp_commonModules;
    vector<unique_ptr<AnalysisModule>> other_modules;
    vector<unique_ptr<SelectionProducer>> sel_modules;
    vector<unique_ptr<SelItemsHelper>> sel_helpers;
    vector<NParticleMultiHistProducerHelper<TopJet>> fatjet_hists;
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




TpTpAnalysisModule::TpTpAnalysisModule(Context & ctx) {

    // const float MIN_HIGGS_MASS = 60.f;
    // const float MAX_HIGGS_MASS = 150.f;


    // If needed, access the configuration of the module here, e.g.:
    // string testvalue = ctx.get("TestKey", "<not set>");
    // cout << "TestKey in the configuration was: " << testvalue << endl;
    version = ctx.get("dataset_version", "");
    type = ctx.get("dataset_type", "");
    type = ctx.get("cycle_type", "PreSelection");
    
    // If running in SFrame, the keys "dataset_version", "dataset_type" and "dataset_lumi"
    // are set to the according values in the xml file. For CMSSW, these are
    // not set automatically, but can be set in the python config file.
    for(auto & kv : ctx.get_all()){
        cout << " " << kv.first << " = " << kv.second << endl;
    }

    // class that takes care of applying CommonModules (with JEC, jet-lepton-cleaning, MCWeight etc.),
    // produces all handles for generic quantities like n_jets, met, etc.
    tptp_commonModules.reset(new TpTpCommonModules(ctx));

    // EventWeightOutputHandle only needed for TMVA studies
    // other_modules.emplace_back(new EventWeightOutputHandle(ctx));

    
    // if (version == "Run2015D_Mu") {
    //     other_modules.emplace_back(new TriggerAcceptProducer(ctx, QCDTEST_MUON_TRIGGER_PATHS_DATA, "trigger_accept"));
    // } else if (version == "Run2015D_Ele") {
    //     other_modules.emplace_back(new TriggerAcceptProducer(ctx, {}, "trigger_accept"));
    // } else if (version == "Run2015D_Had") {
    //     other_modules.emplace_back(new TriggerAcceptProducer(ctx, {}, "trigger_accept"));
    // } else {
    //     other_modules.emplace_back(new TriggerAcceptProducer(ctx, QCDTEST_MUON_TRIGGER_PATHS, "trigger_accept"));
    // }


    // cms top tags

    
    
    // check if there is exactly 1 Top Tag; if yes, make sure that all higgs tags are
    // well separated from it by making a dR requirement of 1.5
    

    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "patJetsAk8CHSJetsSoftDropPacked_daughters",
                "higgs_tags",
                TopJetId(AndId<TopJet>(PtEtaCut(300., 2.4), HiggsFlexBTag(60., 150., CSVBTag(CSVBTag::WP_LOOSE), CSVBTag(CSVBTag::WP_LOOSE))))
                ));
    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "higgs_tags",
                "higgs_tags_noT",
                TopJetId(MinMaxDeltaRId<TopJet>(ctx, "cmsToptags", "min_dr_higgs"))
                ));

    
    other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "higgs_tags_noT",
                "n_higgs_tags_noT"
                ));
    other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "higgs_tags",
                "n_higgs_tags"
                ));

    fatjet_hists.emplace_back("Ak8SoftDrop_all", "patJetsAk8CHSJetsSoftDropPacked_daughters", vector<string>{"pt", "eta", "phi", "mass_sj"});
    
    fatjet_hists.emplace_back("higgs_tags", "higgs_tags", vector<string>{"pt", "eta", "phi", "mass_sj", "tau21", "n_sjbtags-loose", "n_sjbtags-medium"});
    fatjet_hists.back().add_level("dRtop_cleaned", "higgs_tags_noT", vector<string>{"pt", "eta", "phi", "mass_sj", "tau21", "n_sjbtags-loose", "n_sjbtags-medium"});

    
    // vector<string> categories = split(ctx.get("category", ""));
    std::vector<string> categories = {"NoT-IsoMuo24", "NoT-Mu45", "NoT-Mu15_PFHT600", "NoT-PFHT800"};

    for (auto const & cat : categories) {

        SEL_ITEMS_FULL_SEL.push_back(SEL_ITEMS_BASELINE_SEL);
        if (split(cat, "-")[1] == "IsoMuo24") {
            other_modules.emplace_back(new PrimaryLeptonOwn<Muon>(ctx, "muons", "PrimaryMuon_"+cat, MuonId(MuonIso())));
            other_modules.emplace_back(new LeptonPtProducer(ctx, "PrimaryMuon_"+cat, "primary_muon_pt_"+cat));
            other_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_IsoMu24_eta2p1_v*"}, "trigger_accept_"+cat));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_"+cat, "Trigger Accept", 2, -.5, 1.5, 1));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_muon_pt_"+cat, "Primary Muon p_T", 90, 0., 900., 30.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatD("HT", "HT", 25, 0, 4500));
        }
        else if (split(cat, "-")[1] == "Mu45") {
            other_modules.emplace_back(new PrimaryLeptonOwn<Muon>(ctx, "muons", "PrimaryMuon_"+cat)); 
            other_modules.emplace_back(new LeptonPtProducer(ctx, "PrimaryMuon_"+cat, "primary_muon_pt_"+cat));
            other_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_Mu45_eta2p1_v*"}, "trigger_accept_"+cat));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_"+cat, "Trigger Accept", 2, -.5, 1.5, 1));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_muon_pt_"+cat, "Primary Muon p_T", 90, 0., 900., 50.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatD("HT", "HT", 25, 0, 4500));
        }
        else if (split(cat, "-")[1] == "Mu15_PFHT600") {
            other_modules.emplace_back(new PrimaryLeptonOwn<Muon>(ctx, "muons", "PrimaryMuon_"+cat));
            other_modules.emplace_back(new LeptonPtProducer(ctx, "PrimaryMuon_"+cat, "primary_muon_pt_"+cat));
            other_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_Mu15_IsoVVVL_PFHT600_v*"}, "trigger_accept_"+cat));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_"+cat, "Trigger Accept", 2, -.5, 1.5, 1));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_muon_pt_"+cat, "Primary Muon p_T", 90, 0., 900., 20.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatD("HT", "HT", 25, 0, 4500, 650));
        }
        else if (split(cat, "-")[1] == "PFHT800") {
            other_modules.emplace_back(new PrimaryLeptonOwn<Muon>(ctx, "muons", "PrimaryMuon_"+cat));
            other_modules.emplace_back(new LeptonPtProducer(ctx, "PrimaryMuon_"+cat, "primary_muon_pt_"+cat));
            other_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_PFHT800Emu_v*"}, "trigger_accept_"+cat));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_"+cat, "Trigger Accept", 2, -.5, 1.5, 1));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_muon_pt_"+cat, "Primary Muon p_T", 90, 0., 900., 20.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatD("HT", "HT", 25, 0, 4500, 850));
        }
        other_modules.emplace_back(new TwoDCutProducer(ctx, "PrimaryMuon_"+cat, "TwoDcut_Dr_"+cat, "TwoDcut_Dpt_"+cat));


        vector<string> item_names;
        for (auto const & seli : SEL_ITEMS_FULL_SEL.back()) 
            item_names.push_back(seli->name());

        sel_helpers.emplace_back(new SelItemsHelper(SEL_ITEMS_FULL_SEL.back(), ctx, item_names, cat+"_sel_accept", cat+"_sel_all_accepted"));
        // sel_helper.declare_items_for_output();
        sel_modules.emplace_back(new SelectionProducer(ctx, *sel_helpers.back()));

        // 3. Set up Hists classes:

        // TODO: set up and fill other histogram classes, e.g. your own HistCollector stuff

        v_hists.emplace_back(vector<unique_ptr<Hists>>());
        v_hists_after_sel.emplace_back(vector<unique_ptr<Hists>>());

        if (!v_hists_nosel.size()) {
            sel_helpers.back()->fill_hists_vector(v_hists_nosel, "NoSelection");
            for (auto const & hist_helper : fatjet_hists)
                v_hists_nosel.emplace_back(hist_helper.book_histograms(ctx, "NoSelection"));
                v_hists_nosel.emplace_back(new OwnHistCollector(ctx, "NoSelection"));
        }

        auto nm1_hists = new Nm1SelHists(ctx, cat+"/Nm1Selection", *sel_helpers.back());
        auto cf_hists = new VLQ2HTCutflow(ctx, cat+"/Cutflow", *sel_helpers.back());

        map<string, SelectedSelHists*> selected_sel_hists;
        selected_sel_hists["NoSTCut"] = new SelectedSelHists(ctx, cat+"/NoSTCut", *sel_helpers.back(), {}, {"ST"});
        selected_sel_hists["NoTriggerCut"] = new SelectedSelHists(ctx, cat+"/NoTriggerCut", *sel_helpers.back(), {}, {"trigger_accept"+cat});
        selected_sel_hists["NoLeptonCut"] = new SelectedSelHists(ctx, cat+"/NoLeptonCut", *sel_helpers.back(), {}, {"primary_muon_pt"+cat});
        selected_sel_hists["No2DCut"] = new SelectedSelHists(ctx, cat+"/No2DCut", *sel_helpers.back(), {}, {"twoD_cut"});
        selected_sel_hists["NoTopTagCut"] = new SelectedSelHists(ctx, cat+"/NoTopTagCut", *sel_helpers.back(), {}, {"n_cmsToptags"});
        selected_sel_hists["NoHiggsTagCut"] = new SelectedSelHists(ctx, cat+"/NoHiggsTagCut", *sel_helpers.back(), {}, {"n_higgs_tags_noT"});
        selected_sel_hists["OnlySTCut"] = new SelectedSelHists(ctx, cat+"/OnlySTCut", *sel_helpers.back(), {"ST"});
        selected_sel_hists["OnlyTriggerCut"] = new SelectedSelHists(ctx, cat+"/OnlyTriggerCut", *sel_helpers.back(), {"trigger_accept"+cat});
        selected_sel_hists["OnlyLeptonCut"] = new SelectedSelHists(ctx, cat+"/OnlyLeptonCut", *sel_helpers.back(), {"primary_muon_pt"+cat});
        selected_sel_hists["Only2DCut"] = new SelectedSelHists(ctx, cat+"/Only2DCut", *sel_helpers.back(), {"twoD_cut"});
        selected_sel_hists["OnlyTopTagCut"] = new SelectedSelHists(ctx, cat+"/OnlyTopTagCut", *sel_helpers.back(), {"n_cmsToptags"});
        selected_sel_hists["OnlyHiggsTagCut"] = new SelectedSelHists(ctx, cat+"/OnlyHiggsTagCut", *sel_helpers.back(), {"n_higgs_tags_noT"});



        // append 2D cut
        unsigned pos_2d_cut = 4;
        float dr_2d, dpt_2d;
        if (split(cat, "-")[1] == "IsoMuo24") {
            dr_2d = 0.;
            dpt_2d = 0.;
        }
        else {
            dr_2d = DR_2D_CUT_PRESEL;
            dpt_2d = DPT_2D_CUT_PRESEL;
        }
        sel_modules.back()->insert_selection(pos_2d_cut, new TwoDCutSel(ctx, dr_2d, dpt_2d, "TwoDcut_Dr_"+cat, "TwoDcut_Dpt_"+cat));
        nm1_hists->insert_hists(pos_2d_cut, new TwoDCutHist(ctx, cat+"/Nm1Selection", "TwoDcut_Dr_"+cat, "TwoDcut_Dpt_"+cat));
        cf_hists->insert_step(pos_2d_cut, "2D cut");
        for (auto hist : selected_sel_hists) {
            hist.second->insert_hist_and_sel(pos_2d_cut, new TwoDCutHist(ctx, cat+"/"+hist.first, "TwoDcut_Dr_"+cat, "TwoDcut_Dpt_"+cat), "twoD_cut");
            // for (auto const & hist_helper : fatjet_hists) {
            //     hist.second->insert_additional_hist(hist_helper.book_histograms(ctx, cat+"/"+hist.first));
            // }
            // v_hists.back().emplace_back(new OwnHistCollector(ctx, cat+"/"+hist.first));
            v_hists.back().emplace_back(hist.second);
        }

        v_hists.back().emplace_back(nm1_hists);
        v_hists.back().emplace_back(cf_hists);
        sel_helpers.back()->fill_hists_vector(v_hists_after_sel.back(), cat+"/PostSelection");
        for (auto const & hist_helper : fatjet_hists)
            v_hists_after_sel.back().emplace_back(hist_helper.book_histograms(ctx, cat+"/PostSelection"));
        v_hists_after_sel.back().emplace_back(new OwnHistCollector(ctx, cat+"/PostSelection"));

        // v_hists_after_sel.emplace_back(new HistCollector(ctx, "EventHistsPost"));

    }


}


bool TpTpAnalysisModule::process(Event & event) {

    // cout << "TpTpAnalysisModule: Starting to process event (runid, eventid) = (" << event.run << ", " << event.event << ")" << endl;

    // TEST STUFF HERE



    // run all modules

    tptp_commonModules->process(event);

    for (auto & mod : other_modules) {
        mod->process(event);
    }

    // run selection

    // if (!cat_check_module->passes(event)) {
    //     return false;
    // }

    bool any_trigger = false;

    for (unsigned i = 0; i < sel_modules.size(); ++i) {
    
        bool all_accepted = sel_modules[i]->process(event);

        // fill histograms
        if (all_accepted) {
            any_trigger = true;
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

    for (auto & hist : v_hists_nosel) {
        hist->fill(event);
    }

    // decide whether or not to keep the current event in the output:
    return any_trigger;
}

UHH2_REGISTER_ANALYSIS_MODULE(TpTpAnalysisModule)
