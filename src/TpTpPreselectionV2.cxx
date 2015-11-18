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
#include "UHH2/VLQToHiggsPairProd/include/TpTpAnalysisModule.h"

using namespace std;
using namespace uhh2;

// using namespace vlqToHiggsPair;

// typedef VectorAndSelection MyAndSelection;

class TpTpPreselectionV2: public TpTpAnalysisModule {
public:

    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_BASELINE_SEL {
        shared_ptr<SelectionItem>(new SelDatD("ST", "ST", 45, 0, 4500, 700)),
        shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 5, -.5, 4.5, 3)),
        shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak8_jet", "Pt leading Ak8 Jet", 60, 0., 1500., 300.))
    };

    const float DR_2D_CUT_PRESEL = 0.4;
    const float DPT_2D_CUT_PRESEL = 40.0;

    explicit TpTpPreselectionV2(Context & ctx);
    virtual bool process(Event & event) override;

private:
    vector<NParticleMultiHistProducerHelper<TopJet>> fatjet_hists;

};




TpTpPreselectionV2::TpTpPreselectionV2(Context & ctx) : TpTpAnalysisModule(ctx) {
    
    
    // check if there is exactly 1 Top Tag; if yes, make sure that all higgs tags are
    // well separated from it by making a dR requirement of 1.5
    

    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "patJetsAk8CHSJetsSoftDropPacked_daughters",
                "ak8_boost",
                TopJetId(PtEtaCut(300., 2.4))
                ));

    other_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "patJetsAk8CHSJetsSoftDropPacked_daughters", "pt_ld_ak8_jet", 1));
    // other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
    //             "ak8_boost",
    //             "ak8_boost_2b",
    //             TopJetId(HiggsFlexBTag(0., 99999., CSVBTag(CSVBTag::WP_LOOSE), CSVBTag(CSVBTag::WP_LOOSE)))
    //             ));
    // other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
    //             "ak8_boost_2b",
    //             "higgs_tags",
    //             TopJetId(HiggsFlexBTag(60., 150.))
    //             ));
    // other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
    //             "higgs_tags",
    //             "higgs_tags_noT",
    //             TopJetId(MinMaxDeltaRId<TopJet>(ctx, "cmsToptags", "min_dr_higgs"))
    //             ));
    other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "patJetsAk8CHSJetsSoftDropPacked_daughters",
                "n_ak8"
                ));
    
    // other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
    //             "higgs_tags_noT",
    //             "n_higgs_tags"
    //             ));
    // other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
    //             "higgs_tags",
    //             "n_higgs_tags"
    //             ));

    // fatjet_hists.emplace_back("Ak8SoftDrop_all", "patJetsAk8CHSJetsSoftDropPacked_daughters", vector<string>{"pt", "eta", "phi", "mass_sj", "n_subjets"});
    // fatjet_hists.back().add_level("Ak8SoftDrop_boost", "ak8_boost", vector<string>{"pt", "eta", "mass_sj", "tau21", "n_sjbtags-loose", "n_sjbtags-medium"});
    // fatjet_hists.back().back().add_level("two_subjet_btags", "ak8_boost_2b", vector<string>{"pt", "eta", "mass_sj", "tau21", "n_sjbtags-loose"});
    // fatjet_hists.back().back().back().add_level("Higgs-Tags", "higgs_tags", vector<string>{"pt", "eta", "mass_sj", "tau21", "n_sjbtags-loose"});
    
    // fatjet_hists.emplace_back("higgs_tags", "higgs_tags", vector<string>{"pt", "eta", "phi", "mass_sj", "tau21", "n_sjbtags-loose", "n_sjbtags-medium"});
    // fatjet_hists.back().add_level("dRtop_cleaned", "higgs_tags_noT", vector<string>{"pt", "eta", "phi", "mass_sj", "tau21", "n_sjbtags-loose", "n_sjbtags-medium"});

    
    // vector<string> categories = split(ctx.get("category", ""));
    std::vector<string> categories = {"IsoMuo24", "Mu45", "Mu15_PFHT600", "PFHT800"}; // "NoSelection"

    for (auto const & cat : categories) {

        string triggername = "trigger_accept_"+cat;

        SEL_ITEMS_FULL_SEL.push_back(SEL_ITEMS_BASELINE_SEL);
        if (cat == "NoSelection") {
            if (type == "MC")
                other_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_IsoMu24_eta2p1_v*", "HLT_Mu45_eta2p1_v*", "HLT_Mu15_IsoVVVL_PFHT600_v*", "HLT_PFHT800Emu_v*"}, "trigger_accept_all"));
            else
                other_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_IsoMu27_v*", "HLT_Mu45_eta2p1_v*", "HLT_Mu15_IsoVVVL_PFHT600_v*", "HLT_PFHT800Emu_v*"}, "trigger_accept_all"));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_all", "Trigger Accept", 2, -.5, 1.5));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_muon_pt_iso", "Primary Muon p_T", 90, 0., 900.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_muon_pt_noIso", "Primary Muon p_T", 90, 0., 900.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatD("HT", "HT", 25, 0, 4500));
        }
        else if (cat == "IsoMuo24") {
            if (type == "MC")
                other_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_IsoMu24_eta2p1_v*"}, triggername));
            else
                other_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_IsoMu27_v*"}, triggername));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI(triggername, "Trigger Accept", 2, -.5, 1.5, 1));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_muon_pt_iso", "Primary Muon p_T", 90, 0., 900., 32.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatD("HT", "HT", 25, 0, 4500));
        }
        else if (cat == "Mu45") {
            other_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_Mu45_eta2p1_v*"}, triggername));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI(triggername, "Trigger Accept", 2, -.5, 1.5, 1));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_muon_pt_noIso", "Primary Muon p_T", 90, 0., 900., 50.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatD("HT", "HT", 25, 0, 4500));
        }
        else if (cat == "Mu15_PFHT600") {
            other_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_Mu15_IsoVVVL_PFHT600_v*"}, triggername));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI(triggername, "Trigger Accept", 2, -.5, 1.5, 1));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_muon_pt_noIso", "Primary Muon p_T", 90, 0., 900., 20.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatD("HT", "HT", 25, 0, 4500, 650));
        }
        else if (cat == "PFHT800") {
            other_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_PFHT800Emu_v*"}, triggername));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI(triggername, "Trigger Accept", 2, -.5, 1.5, 1));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_muon_pt_noIso", "Primary Muon p_T", 90, 0., 900., 20.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatD("HT", "HT", 25, 0, 4500, 850));
        }

        unsigned pos_2d_cut = 4;

        other_modules.emplace_back(new TwoDCutProducer(ctx, "PrimaryMuon_noIso", "TwoDcut_Dr_noIso", "TwoDcut_Dpt_noIso"));
        other_modules.emplace_back(new TwoDCutProducer(ctx, "PrimaryMuon_iso", "TwoDcut_Dr_iso", "TwoDcut_Dpt_iso"));

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

        if (cat == "NoSelection") {
            sel_helpers.back()->fill_hists_vector(v_hists_nosel, "NoSelection");
            v_hists_nosel.emplace_back(new TwoDCutHist(ctx, "NoSelection", "TwoDcut_Dr_iso", "TwoDcut_Dpt_iso", "twod_cut_hist_iso"));
            v_hists_nosel.emplace_back(new TwoDCutHist(ctx, "NoSelection", "TwoDcut_Dr_noIso", "TwoDcut_Dpt_noIso", "twod_cut_hist_noIso"));
            for (auto const & hist_helper : fatjet_hists)
                v_hists_nosel.emplace_back(hist_helper.book_histograms(ctx, "NoSelection"));
            v_hists_nosel.emplace_back(new OwnHistCollector(ctx, "NoSelection", type == "MC"));
            continue;
        }

        auto nm1_hists = new Nm1SelHists(ctx, cat+"/Nm1Selection", *sel_helpers.back());
        auto cf_hists = new VLQ2HTCutflow(ctx, cat+"/Cutflow", *sel_helpers.back());

        string suffix = (cat == "IsoMuo24") ? "iso" : "noIso";
        map<string, SelectedSelHists*> selected_sel_hists;
        selected_sel_hists["NoSTCut"] = new SelectedSelHists(ctx, cat+"/NoSTCut", *sel_helpers.back(), {}, {"ST"});
        selected_sel_hists["NoNAk8JetsCut"] = new SelectedSelHists(ctx, cat+"/NoNAk8JetsCut", *sel_helpers.back(), {}, {"n_ak8"});
        selected_sel_hists["NoAk8PtCut"] = new SelectedSelHists(ctx, cat+"/NoAk8PtCut", *sel_helpers.back(), {}, {"pt_ld_ak8_jet"});
        selected_sel_hists["OnlyTriggerAndLeptonCut"] = new SelectedSelHists(ctx, cat+"/OnlyTriggerAndLeptonCut", *sel_helpers.back(), {triggername, "primary_muon_pt_"+suffix});
        selected_sel_hists["OnlyTriggerLeptonAnd2DCut"] = new SelectedSelHists(ctx, cat+"/OnlyTriggerLeptonAnd2DCut", *sel_helpers.back(), {triggername, "primary_muon_pt_"+suffix, "twoD_cut"});
        selected_sel_hists["OnlySTCut"] = new SelectedSelHists(ctx, cat+"/OnlySTCut", *sel_helpers.back(), {triggername, "primary_muon_pt_"+suffix, "twoD_cut", "ST"});
        selected_sel_hists["OnlyAk8PtCut"] = new SelectedSelHists(ctx, cat+"/OnlyAk8PtCut", *sel_helpers.back(), {triggername, "primary_muon_pt_"+suffix, "twoD_cut", "pt_ld_ak8_jet"});
        selected_sel_hists["OnlyNAk8Cut"] = new SelectedSelHists(ctx, cat+"/OnlyNAk8Cut", *sel_helpers.back(), {triggername, "primary_muon_pt_"+suffix, "twoD_cut", "n_ak8"});



        // append 2D cut
        float dr_2d, dpt_2d;
        if (cat == "IsoMuo24") {
            dr_2d = 0.;
            dpt_2d = 0.;
        }
        else {
            dr_2d = DR_2D_CUT_PRESEL;
            dpt_2d = DPT_2D_CUT_PRESEL;
        }
        
        sel_modules.back()->insert_selection(pos_2d_cut, new TwoDCutSel(ctx, dr_2d, dpt_2d, "TwoDcut_Dr_noIso", "TwoDcut_Dpt_noIso"));
        nm1_hists->insert_hists(pos_2d_cut, new TwoDCutHist(ctx, cat+"/Nm1Selection", "TwoDcut_Dr_noIso", "TwoDcut_Dpt_noIso", "twod_cut_hist_noIso"));
        cf_hists->insert_step(pos_2d_cut, "2D cut");
        for (auto hist : selected_sel_hists) {
            hist.second->insert_hist_and_sel(pos_2d_cut, new TwoDCutHist(ctx, cat+"/"+hist.first, "TwoDcut_Dr_noIso", "TwoDcut_Dpt_noIso", "twod_cut_hist_noIso"), "twoD_cut");
            // for (auto const & hist_helper : fatjet_hists) {
            //     hist.second->insert_additional_hist(hist_helper.book_histograms(ctx, cat+"/"+hist.first));
            // }
            hist.second->insert_additional_hist(new OwnHistCollector(ctx, cat+"/"+hist.first, type == "MC"));
            v_hists.back().emplace_back(hist.second);
        }

        v_hists.back().emplace_back(nm1_hists);
        v_hists.back().emplace_back(cf_hists);
        sel_helpers.back()->fill_hists_vector(v_hists_after_sel.back(), cat+"/PostSelection");
        v_hists_after_sel.back().emplace_back(new TwoDCutHist(ctx, cat+"/PostSelection", "TwoDcut_Dr_iso", "TwoDcut_Dpt_iso", "twod_cut_hist_iso"));
        v_hists_after_sel.back().emplace_back(new TwoDCutHist(ctx, cat+"/PostSelection", "TwoDcut_Dr_noIso", "TwoDcut_Dpt_noIso", "twod_cut_hist_noIso"));
        // for (auto const & hist_helper : fatjet_hists) {
        //     v_hists_after_sel.back().emplace_back(hist_helper.book_histograms(ctx, cat+"/PostSelection"));
        //     selected_sel_hists["NoHiggsTagCut"]->insert_additional_hist(hist_helper.book_histograms(ctx, cat+"/NoHiggsTagCut"));
        // }
        v_hists_after_sel.back().emplace_back(new OwnHistCollector(ctx, cat+"/PostSelection", type == "MC"));

        // v_hists_after_sel.emplace_back(new HistCollector(ctx, "EventHistsPost"));

    }


}


bool TpTpPreselectionV2::process(Event & event) {

    if(!TpTpAnalysisModule::process(event))
        return false;

    // run all modules

    for (bool pass_sel : sel_modules_passed) {
        if (pass_sel) return true;
    }

    return false;
}

UHH2_REGISTER_ANALYSIS_MODULE(TpTpPreselectionV2)
