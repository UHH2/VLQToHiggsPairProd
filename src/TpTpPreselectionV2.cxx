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
#include "UHH2/VLQToHiggsPairProd/include/TpTpAnalysisModule.h"

using namespace std;
using namespace uhh2;

// using namespace vlqToHiggsPair;

// typedef VectorAndSelection MyAndSelection;

class TpTpPreselectionV2: public TpTpAnalysisModule {
public:

    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_BASELINE_SEL {
        shared_ptr<SelectionItem>(new SelDatD("ST", "ST", 45, 0, 4500, 700)),
        shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 8, -.5, 7.5, 2)),
        shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak8_jet", "Pt leading Ak8 Jet", 60, 0., 1500., 300.)),
        // shared_ptr<SelectionItem>(new SelDatD("HT", "HT", 25, 0, 4500)),
        // shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 8, -.5, 7.5, 3)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak8_jet", "Pt leading Ak8 Jet", 60, 0., 1500., 300.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak8_jet_cleaned", "Pt leading Ak8 Jet", 60, 0., 1500.)),
        // shared_ptr<SelectionItem>(new SelDatF("primary_muon_pt_dRak8", "Primary Muon (dRak8) p_T", 90, 0., 900.))
    };

    const vector<shared_ptr<SelectionItem>> ADDITIONAL_SEL_ITEMS {
        shared_ptr<SelectionItem>(new SelDatI("n_ak4", "N(Ak4 Jets)", 15, -.5, 14.5)),
        shared_ptr<SelectionItem>(new SelDatI("n_leptons", "N(Leptons)", 6, -.5, 5.5)),
        shared_ptr<SelectionItem>(new SelDatI("is_muon", "PrimLep is muon", 2, -.5, 1.5)),
        shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 5, -.5, 4.5)),
        shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 5, -.5, 4.5)),
        shared_ptr<SelectionItem>(new SelDatI("n_topjets_uncleaned", "N(Ak8 jets, uncleaned)", 7, -.5, 6.5)),
        shared_ptr<SelectionItem>(new SelDatI("n_topjets_cleaned", "N(Ak8 jets, dR-cleaned)", 7, -.5, 6.5)),
        shared_ptr<SelectionItem>(new SelDatF("leading_mu_pt", "Leading Muon p_T", 90, 0., 900., 40.)),
        shared_ptr<SelectionItem>(new SelDatF("leading_ele_pt", "Leading Electron p_T", 90, 0., 900., 40.)),
        shared_ptr<SelectionItem>(new SelDatF("primary_lepton_eta", "Primary Lepton eta", 60, -3., 3.)),
        // shared_ptr<SelectionItem>(new SelDatI("primary_lepton_charge", "N(Ak8 jets, dR-cleaned)", 7, -.5, 6.5)),


        // shared_ptr<SelectionItem>(new SelDatD("HT", "HT", 25, 0, 4500)),
        // shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 8, -.5, 7.5, 3)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak8_jet", "Pt leading Ak8 Jet", 60, 0., 1500., 300.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak8_jet_cleaned", "Pt leading Ak8 Jet", 60, 0., 1500.)),
        // shared_ptr<SelectionItem>(new SelDatF("primary_muon_pt_dRak8", "Primary Muon (dRak8) p_T", 90, 0., 900.))
    };

    const float DR_2D_CUT_PRESEL = 0.4;
    const float DPT_2D_CUT_PRESEL = 40.0;

    explicit TpTpPreselectionV2(Context & ctx);
    virtual bool process(Event & event) override;

private:
    unique_ptr<AnalysisModule> common_module;
    vector<unique_ptr<AnalysisModule>> pre_modules;
    vector<unique_ptr<Hists>> v_hists_nosel;

};




TpTpPreselectionV2::TpTpPreselectionV2(Context & ctx) : TpTpAnalysisModule(ctx) {

    other_modules.emplace_back(new CollectionProducer<Electron>(ctx,
                "electrons",
                "electrons_iso"
                ));
    pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "topjets",
                "topjets_uncleaned"
                ));
    pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "topjets",
                "topjets_cleaned"
                ));
    
    CommonModules* commonObjectCleaning = new CommonModules();
    commonObjectCleaning->set_jet_id(AndId<Jet>(JetPFID(JetPFID::WP_LOOSE), PtEtaCut(30.0,2.4)));
    commonObjectCleaning->disable_jersmear();
        // commonObjectCleaning->disable_mcpileupreweight();
    commonObjectCleaning->set_electron_id(AndId<Electron>(ElectronID_Spring15_25ns_medium_noIso,PtEtaCut(20.0, 2.4)));
    commonObjectCleaning->set_muon_id(AndId<Muon>(MuonIDMedium(),PtEtaCut(20.0, 2.1)));
    commonObjectCleaning->switch_jetlepcleaner(true);
    commonObjectCleaning->switch_jetPtSorter(true);
        // commonObjectCleaning->disable_lumisel();
    commonObjectCleaning->init(ctx);
    common_module.reset(commonObjectCleaning);

        // modules.emplace_back(new CollectionProducer<TopJet>(ctx,
        //     "topjets",
        //     "ak8jets_uncleaned"
        //     ));
    if (ctx.get("dataset_type", "") == "MC") {
        pre_modules.emplace_back(new GenericTopJetCorrector(ctx, JERFiles::Summer15_25ns_L23_AK8PFchs_MC, "topjets"));
        pre_modules.emplace_back(new GenericTopJetCorrector(ctx, JERFiles::Summer15_25ns_L123_AK8PFchs_MC, "patJetsAk8CHSJetsSoftDropPacked_daughters"));
        pre_modules.emplace_back(new GenericTopJetCorrector(ctx, JERFiles::Summer15_25ns_L123_AK8PFchs_MC, "patJetsHepTopTagCHSPacked_daughters"));
        pre_modules.emplace_back(new GenericSubJetCorrector(ctx, JERFiles::Summer15_25ns_L123_AK4PFchs_MC, "topjets"));
        pre_modules.emplace_back(new GenericSubJetCorrector(ctx, JERFiles::Summer15_25ns_L123_AK4PFchs_MC, "patJetsAk8CHSJetsSoftDropPacked_daughters"));
        pre_modules.emplace_back(new GenericSubJetCorrector(ctx, JERFiles::Summer15_25ns_L123_AK4PFchs_MC, "patJetsHepTopTagCHSPacked_daughters"));
        // ====== IMPLEMENT TOPJETLEPTONCLEANER BY KEYMATCHING!========
        pre_modules.emplace_back(new TopJetLeptonCleaner(ctx, JERFiles::Summer15_25ns_L23_AK8PFchs_MC));
        // pre_modules.emplace_back(new GenericTopJetCleaner(ctx, PtEtaCut(150., 2.4), "topjets"));
            // pre_modules.emplace_back(new TopJetLeptonCleaner(ctx, JERFiles::Summer15_25ns_L123_AK8PFchs_MC, "ak8jets_cleaned"));
            // pre_modules.emplace_back(new TopJetLeptonCleaner(ctx, JERFiles::Summer15_25ns_L123_AK8PFchs_MC, "patJetsHepTopTagCHSPacked_daughters"));
            // pre_modules.emplace_back(new GenericTopJetCleaner(ctx, PtEtaCut(150., 2.4), "ak8jets_cleaned"));
            // pre_modules.emplace_back(new GenericTopJetCleaner(ctx, PtEtaCut(150., 2.4), "patJetsHepTopTagCHSPacked_daughters"));
    }
    else {
        pre_modules.emplace_back(new GenericTopJetCorrector(ctx, JERFiles::Summer15_25ns_L23_AK8PFchs_DATA, "topjets"));
        pre_modules.emplace_back(new GenericTopJetCorrector(ctx, JERFiles::Summer15_25ns_L123_AK8PFchs_DATA, "patJetsAk8CHSJetsSoftDropPacked_daughters"));
        pre_modules.emplace_back(new GenericTopJetCorrector(ctx, JERFiles::Summer15_25ns_L123_AK8PFchs_DATA, "patJetsHepTopTagCHSPacked_daughters"));
        pre_modules.emplace_back(new GenericSubJetCorrector(ctx, JERFiles::Summer15_25ns_L123_AK4PFchs_DATA, "topjets"));
        pre_modules.emplace_back(new GenericSubJetCorrector(ctx, JERFiles::Summer15_25ns_L123_AK4PFchs_DATA, "patJetsAk8CHSJetsSoftDropPacked_daughters"));
        pre_modules.emplace_back(new GenericSubJetCorrector(ctx, JERFiles::Summer15_25ns_L123_AK4PFchs_DATA, "patJetsHepTopTagCHSPacked_daughters"));
        // ====== IMPLEMENT TOPJETLEPTONCLEANER BY KEYMATCHING!========
        pre_modules.emplace_back(new TopJetLeptonCleaner(ctx, JERFiles::Summer15_25ns_L23_AK8PFchs_DATA));
        // pre_modules.emplace_back(new GenericTopJetCleaner(ctx, PtEtaCut(125., 2.4), "topjets"));
            // pre_modules.emplace_back(new TopJetLeptonCleaner(ctx, JERFiles::Summer15_25ns_L123_AK8PFchs_MC, "ak8jets_cleaned"));
            // pre_modules.emplace_back(new TopJetLeptonCleaner(ctx, JERFiles::Summer15_25ns_L123_AK8PFchs_MC, "patJetsHepTopTagCHSPacked_daughters"));
            // pre_modules.emplace_back(new GenericTopJetCleaner(ctx, PtEtaCut(150., 2.4), "ak8jets_cleaned"));
            // pre_modules.emplace_back(new GenericTopJetCleaner(ctx, PtEtaCut(150., 2.4), "patJetsHepTopTagCHSPacked_daughters"));
    }
    pre_modules.emplace_back(new TopJetCleaner(ctx, MinMaxDeltaRId<Electron>(ctx, "electrons", 0.2), "topjets_cleaned"));
    pre_modules.emplace_back(new TopJetCleaner(ctx, MinMaxDeltaRId<Muon>(ctx, "muons", 0.2), "topjets_cleaned"));
    pre_modules.emplace_back(new TopJetCleaner(ctx, PtEtaCut(200., 2.4), "topjets"));
    
    // check if there is exactly 1 Top Tag; if yes, make sure that all higgs tags are
    // well separated from it by making a dR requirement of 1.5
    other_modules.emplace_back(new PrimaryLeptonOwn<Muon>(ctx, "muons", "PrimaryMuon_iso", MuonId(MuonIso())));
    other_modules.emplace_back(new PrimaryLeptonInfoProducer(ctx, "PrimaryMuon_iso", "primary_muon_pt_iso", "primary_muon_eta_iso", "primary_muon_charge_iso"));
    other_modules.emplace_back(new PrimaryLeptonOwn<Electron>(ctx, "electrons_iso", "PrimaryElectron_iso", ElectronId(AndId<Electron>(PtEtaCut(20., 2.4), ElectronID_Spring15_25ns_medium))));
    other_modules.emplace_back(new PrimaryLeptonInfoProducer(ctx, "PrimaryElectron_iso", "primary_electron_pt_iso", "primary_electron_eta_iso", "primary_electron_charge_iso"));

    other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx, "topjets_uncleaned", "n_topjets_uncleaned"));
    other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx, "topjets_cleaned", "n_topjets_cleaned"));

          
    

    
    vector<string> categories = split(ctx.get("category", ""));
    // std::vector<string> categories = {"Mu45", "IsoMuo24", "Mu15_PFHT600", "PFHT800"}; // "NoSelection","IsoMuo24-clean", "Mu15_PFHT600-clean", "PFHT800-clean", "PFHT800-uncleaned"

    for (auto const & cat : categories) {

        string triggername = "trigger_accept_"+cat;
        SEL_ITEMS_FULL_SEL.push_back(SEL_ITEMS_BASELINE_SEL);

        // if (split(cat, "-").size() > 1 && split(cat, "-")[1] == "uncleaned") {
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_ak8_uncleaned", "N(Ak8 Jets)", 8, -.5, 7.5, 3));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_ld_ak8_jet_uncleaned", "Pt leading Ak8 Jet", 60, 0., 1500., 300.));            
        // }
        // else {
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_ak8", "N(Ak8 Jets)", 8, -.5, 7.5, 3));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_ld_ak8_jet", "Pt leading Ak8 Jet", 60, 0., 1500., 300.));            
        // }

        if (cat == "NoSelection") {
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_isoMu20", "Trigger Accept", 2, -.5, 1.5, 2)); // make sure that NoSelection doesn't write out anything
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_isoEl27", "Trigger Accept", 2, -.5, 1.5));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_mu45", "Trigger Accept", 2, -.5, 1.5));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_el45", "Trigger Accept", 2, -.5, 1.5));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_muon_pt_iso", "Primary Muon p_T", 90, 0., 900.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_electron_pt_iso", "Primary Electron p_T", 90, 0., 900.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_lepton_pt", "Primary Lepton p_T", 90, 0., 900.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_subld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500.));
        }
        else if (cat == "IsoMuo20") {
            SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin(), new SelDatI("trigger_accept_isoMu20", "Trigger Accept", 2, -.5, 1.5, 1));
            SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+1, new SelDatF("primary_muon_pt_iso", "Primary Muon p_T", 90, 0., 900., 40.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_subld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500.));
        }
        else if (cat == "IsoEle27") {
            SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin(), new SelDatI("trigger_accept_isoEl27", "Trigger Accept", 2, -.5, 1.5, 1));
            SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+1, new SelDatF("primary_electron_pt_iso", "Primary Electron p_T", 90, 0., 900., 40.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_subld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500.));
        }
        else if (cat == "Mu45") {
            
            SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin(), new SelDatI("trigger_accept_mu45", "Trigger Accept", 2, -.5, 1.5, 1));
            SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+1, new SelDatF("primary_lepton_pt", "Primary Lepton p_T", 90, 0., 900., 47.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_subld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500.));
        }
        else if (cat == "El45") {
            
            SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin(), new SelDatI("trigger_accept_el45", "Trigger Accept", 2, -.5, 1.5, 1));
            SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+1, new SelDatF("primary_lepton_pt", "Primary Lepton p_T", 90, 0., 900., 50.));
            SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+2, new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500., 250.));
            SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+3, new SelDatF("pt_subld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500., 65.));
        }

        for (auto const & sel_item : ADDITIONAL_SEL_ITEMS)
            SEL_ITEMS_FULL_SEL.back().push_back(sel_item);

        // else if (cat == "Mu15_PFHT600") {
        //     other_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_Mu15_IsoVVVL_PFHT600_v*"}, triggername));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI(triggername, "Trigger Accept", 2, -.5, 1.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_muon_pt_noIso", "Primary Muon p_T", 90, 0., 900., 40.));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatD("HT", "HT", 25, 0, 4500, 650));
        // }
        // else if (cat == "PFHT800") {
        //     if (type == "MC")
        //         other_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_PFHT800Emu_v*"}, triggername));
        //     else
        //         other_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_PFHT800_v*"}, triggername));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI(triggername, "Trigger Accept", 2, -.5, 1.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_muon_pt_noIso", "Primary Muon p_T", 90, 0., 900., 40.));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatD("HT", "HT", 25, 0, 4500, 850));
        // }

        unsigned pos_2d_cut = (cat == "El45") ? 4 : 2;

        other_modules.emplace_back(new TwoDCutProducer(ctx, "PrimaryLepton", "TwoDcut_Dr_noIso", "TwoDcut_Dpt_noIso"));
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
            // for (auto const & hist_helper : fatjet_hists)
            //     v_hists_nosel.emplace_back(hist_helper.book_histograms(ctx, "NoSelection"));
            v_hists_nosel.emplace_back(new OwnHistCollector(ctx, cat, type == "MC", CSVBTag(CSVBTag::WP_MEDIUM), {"ev", "mu", "el", "jet", "lumi", "cmstopjet", "ak8softdroptopjet", "cmstopjet_uncleaned"}));
            continue;
        }

        auto nm1_hists = new Nm1SelHists(ctx, cat+"/Nm1Selection", *sel_helpers.back());
        auto cf_hists = new VLQ2HTCutflow(ctx, cat+"/Cutflow", *sel_helpers.back());

        string lep_pt = (cat == "IsoMuo20" || cat == "IsoEle27") ? "primary_muon_pt_iso" : "primary_lepton_pt";
        // string = (split(cat, "-").size() > 1 && split(cat, "-")[1] == "uncleaned") ? "_uncleaned" : "";
        map<string, SelectedSelHists*> selected_sel_hists;
        // selected_sel_hists["NoSTCut"] = new SelectedSelHists(ctx, cat+"/NoSTCut", *sel_helpers.back(), {}, {"ST"});
        // selected_sel_hists["NoNAk8JetsCut"] = new SelectedSelHists(ctx, cat+"/NoNAk8JetsCut", *sel_helpers.back(), {}, {"n_ak8"});
        selected_sel_hists["NoAk8PtCut"] = new SelectedSelHists(ctx, cat+"/NoAk8PtCut", *sel_helpers.back(), {}, {"pt_ld_ak8_jet"});
        selected_sel_hists["NoNAk8Cut"] = new SelectedSelHists(ctx, cat+"/NoNAk8Cut", *sel_helpers.back(), {}, {"n_ak8"});
        // selected_sel_hists["OnlyTriggerAndLeptonCut"] = new SelectedSelHists(ctx, cat+"/OnlyTriggerAndLeptonCut", *sel_helpers.back(), {triggername, "primary_muon_pt_"+iso_suffix});
        // selected_sel_hists["OnlyTriggerLeptonAnd2DCut"] = new SelectedSelHists(ctx, cat+"/OnlyTriggerLeptonAnd2DCut", *sel_helpers.back(), {triggername, "primary_muon_pt_"+iso_suffix, "twoD_cut"});
        // selected_sel_hists["OnlySTCut"] = new SelectedSelHists(ctx, cat+"/OnlySTCut", *sel_helpers.back(), {triggername, "primary_muon_pt_"+iso_suffix, "twoD_cut", "ST", "HT"});
        // selected_sel_hists["OnlyAk8PtCut"] = new SelectedSelHists(ctx, cat+"/OnlyAk8PtCut", *sel_helpers.back(), {triggername, "primary_muon_pt_"+iso_suffix, "twoD_cut", "pt_ld_ak8_jet"});
        // selected_sel_hists["OnlyNAk8Cut"] = new SelectedSelHists(ctx, cat+"/OnlyNAk8Cut", *sel_helpers.back(), {triggername, "primary_muon_pt_"+iso_suffix, "twoD_cut", "n_ak8"});



        // append 2D cut
        float dr_2d, dpt_2d;
        if (cat == "IsoMuo20" || cat == "IsoEle27") {
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
            hist.second->insert_additional_hist(ak8jet_hists->book_histograms(ctx, cat+"/"+hist.first));
            hist.second->insert_additional_hist(new JetCleaningControlPlots(ctx, cat+"/"+hist.first+"/JetCleaningControlPlots", "weight_ak4_jetpt"));
            // for (auto const & hist_helper : fatjet_hists) {
            //     hist.second->insert_additional_hist(hist_helper.book_histograms(ctx, cat+"/"+hist.first));
            // }
            // hist.second->insert_additional_hist(new OwnHistCollector(ctx, cat+"/"+hist.first, type == "MC"));
            v_hists.back().emplace_back(hist.second);
        }

        v_hists.back().emplace_back(nm1_hists);
        v_hists.back().emplace_back(cf_hists);
        sel_helpers.back()->fill_hists_vector(v_hists_after_sel.back(), cat+"/PostSelection");
        v_hists_after_sel.back().emplace_back(new TwoDCutHist(ctx, cat+"/PostSelection", "TwoDcut_Dr_iso", "TwoDcut_Dpt_iso", "twod_cut_hist_iso"));
        v_hists_after_sel.back().emplace_back(new TwoDCutHist(ctx, cat+"/PostSelection", "TwoDcut_Dr_noIso", "TwoDcut_Dpt_noIso", "twod_cut_hist_noIso"));
        v_hists_after_sel.back().emplace_back(ak8jet_hists->book_histograms(ctx, cat+"/PostSelection"));
        // for (auto const & hist_helper : fatjet_hists) {
        //     v_hists_after_sel.back().emplace_back(hist_helper.book_histograms(ctx, cat+"/PostSelection"));
        //     selected_sel_hists["NoHiggsTagCut"]->insert_additional_hist(hist_helper.book_histograms(ctx, cat+"/NoHiggsTagCut"));
        // }
        v_hists_after_sel.back().emplace_back(new OwnHistCollector(ctx, cat+"/PostSelection", type == "MC", CSVBTag(CSVBTag::WP_MEDIUM), {"ev", "mu", "el", "jet", "lumi", "cmstopjet", "ak8softdroptopjet", "cmstopjet_cleaned"}));
        v_hists_after_sel.back().emplace_back(new JetCleaningControlPlots(ctx, cat+"/PostSelection/JetCleaningControlPlots", "weight_ak4_jetpt"));
        v_hists_after_sel.back().emplace_back(new JetCleaningControlPlots(ctx, cat+"/PostSelection/JetCleaningControlPlotsUp", "weight_ak4_jetpt_up"));
        v_hists_after_sel.back().emplace_back(new JetCleaningControlPlots(ctx, cat+"/PostSelection/JetCleaningControlPlotsDown", "weight_ak4_jetpt_down"));
        // v_hists_after_sel.emplace_back(new HistCollector(ctx, "EventHistsPost"));
        v_hists_after_sel.back().emplace_back(new BTagMCEfficiencyHists(ctx, cat+"/BTagMCEfficiencyHists", CSVBTag::WP_MEDIUM, "tj_btag_sf_coll"));

    }


}


bool TpTpPreselectionV2::process(Event & event) {

    if (!common_module->process(event))
        return false;

    for (auto const & mod : pre_modules)
        mod->process(event);

    assert(event.topjets);
    sort_by_pt(*event.topjets);

    TpTpAnalysisModule::process(event);

    // fill histograms without selection
    for (auto & hist : v_hists_nosel) {
        hist->fill(event);
    }
    
    // run all modules

    for (bool pass_sel : sel_modules_passed) {
        if (pass_sel) return true;
    }


    return false;
}

UHH2_REGISTER_ANALYSIS_MODULE(TpTpPreselectionV2)
