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

    // NEW VALUES FOR CUTS BELOW, OLD ONES COMMENTED OUT! USE THE NEW ONES WHEN RERUNNING PRESELECTION (and make sure you implement tighter cuts in TpTpFinalSelectionTreeOutput.cxx)

    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_NO_SEL {};

    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_BASELINE_SEL {
        // shared_ptr<SelectionItem>(new SelDatD("ST", "ST", 65, 0, 6500, 700)),
        // shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 8, -.5, 7.5, 2)),
        // shared_ptr<SelectionItem>(new SelDatI("n_ak4", "N(Ak4 Jets)", 20, -.5, 19.5, 3)),
        shared_ptr<SelectionItem>(new SelDatD("ST", "ST", 65, 0, 6500, 500)),
        shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 8, -.5, 7.5, 1)),
        shared_ptr<SelectionItem>(new SelDatI("n_ak4", "N(Ak4 Jets)", 20, -.5, 19.5, 3)),
        // shared_ptr<SelectionItem>(new SelDatD("HT", "HT", 25, 0, 4500)),
        // shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 8, -.5, 7.5, 3)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak8_jet", "Pt leading Ak8 Jet", 60, 0., 1500., 300.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak8_jet_cleaned", "Pt leading Ak8 Jet", 60, 0., 1500.)),
        // shared_ptr<SelectionItem>(new SelDatF("primary_muon_pt_dRak8", "Primary Muon (dRak8) p_{T}", 60, 0., 1200.))
    };

    const vector<shared_ptr<SelectionItem>> ADDITIONAL_SEL_ITEMS {
        // shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak8_jet", "Pt leading Ak8 Jet", 60, 0., 1500.)),
        // shared_ptr<SelectionItem>(new SelDatI("n_leptons", "N(Leptons)", 6, -.5, 5.5)),
        // shared_ptr<SelectionItem>(new SelDatI("is_muon", "PrimLep is muon", 2, -.5, 1.5)),
        // shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 5, -.5, 4.5)),
        // shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 5, -.5, 4.5)),
        // shared_ptr<SelectionItem>(new SelDatI("n_topjets_uncleaned", "N(Ak8 jets, uncleaned)", 7, -.5, 6.5)),
        // shared_ptr<SelectionItem>(new SelDatI("n_topjets_cleaned", "N(Ak8 jets, dR-cleaned)", 7, -.5, 6.5)),
        // shared_ptr<SelectionItem>(new SelDatF("leading_mu_pt", "Leading Muon p_{T}", 60, 0., 1200.)),
        // shared_ptr<SelectionItem>(new SelDatF("leading_ele_pt", "Leading Electron p_{T}", 60, 0., 1200.)),
        // shared_ptr<SelectionItem>(new SelDatF("primary_lepton_eta", "Primary Lepton eta", 60, -3., 3.)),
        // shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt", "Primary Lepton p_{T}", 60, 0., 1200.)),
        // shared_ptr<SelectionItem>(new SelDatI("primary_lepton_charge", "N(Ak8 jets, dR-cleaned)", 7, -.5, 6.5)),

        // shared_ptr<SelectionItem>(new SelDatD("HT", "HT", 25, 0, 4500)),
        // shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 8, -.5, 7.5, 3)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak8_jet", "Pt leading Ak8 Jet", 60, 0., 1500., 300.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak8_jet_cleaned", "Pt leading Ak8 Jet", 60, 0., 1500.)),
        // shared_ptr<SelectionItem>(new SelDatF("primary_muon_pt_dRak8", "Primary Muon (dRak8) p_{T}", 60, 0., 1200.))
    };

    const float DR_2D_CUT_PRESEL = 0.4;
    const float DPT_2D_CUT_PRESEL = 40.0;

    unsigned pos_2d_cut = 0;

    explicit TpTpPreselectionV2(Context & ctx);
    virtual bool process(Event & event) override;

private:
    unique_ptr<AnalysisModule> common_module;
    vector<unique_ptr<AnalysisModule>> pre_modules;
    vector<shared_ptr<Hists>> v_hists_nosel;

};




TpTpPreselectionV2::TpTpPreselectionV2(Context & ctx) : TpTpAnalysisModule(ctx) {

    // pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
    //             "topjets",
    //             "topjets_uncleaned"
    //             ));
    // pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
    //             "topjets",
    //             "topjets_cleaned"
    //             ));
    
    CommonModules* commonObjectCleaning = new CommonModules();
    commonObjectCleaning->set_jet_id(AndId<Jet>(JetPFID(JetPFID::WP_LOOSE), PtEtaCut(10.0,2.4)));
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
        pre_modules.emplace_back(new GenericTopJetCorrector(ctx, JERFiles::Fall15_25ns_L23_AK8PFchs_MC, "topjets"));
        pre_modules.emplace_back(new GenericTopJetCorrector(ctx, JERFiles::Fall15_25ns_L123_AK8PFchs_MC, "patJetsAk8CHSJetsSoftDropPacked_daughters"));
        // pre_modules.emplace_back(new GenericTopJetCorrector(ctx, JERFiles::Fall15_25ns_L123_AK8PFchs_MC, "patJetsHepTopTagCHSPacked_daughters"));
        pre_modules.emplace_back(new GenericSubJetCorrector(ctx, JERFiles::Fall15_25ns_L123_AK4PFchs_MC, "topjets"));
        pre_modules.emplace_back(new GenericSubJetCorrector(ctx, JERFiles::Fall15_25ns_L123_AK4PFchs_MC, "patJetsAk8CHSJetsSoftDropPacked_daughters"));
        // pre_modules.emplace_back(new GenericSubJetCorrector(ctx, JERFiles::Fall15_25ns_L123_AK4PFchs_MC, "patJetsHepTopTagCHSPacked_daughters"));
        // ====== IMPLEMENT TOPJETLEPTONCLEANER BY KEYMATCHING!========
        // pre_modules.emplace_back(new TopJetLeptonCleaner(ctx, JERFiles::Fall15_25ns_L23_AK8PFchs_MC));
        // pre_modules.emplace_back(new GenericTopJetCleaner(ctx, PtEtaCut(150., 2.4), "topjets"));
            // pre_modules.emplace_back(new TopJetLeptonCleaner(ctx, JERFiles::Fall15_25ns_L123_AK8PFchs_MC, "ak8jets_cleaned"));
            // pre_modules.emplace_back(new TopJetLeptonCleaner(ctx, JERFiles::Fall15_25ns_L123_AK8PFchs_MC, "patJetsHepTopTagCHSPacked_daughters"));
            // pre_modules.emplace_back(new GenericTopJetCleaner(ctx, PtEtaCut(150., 2.4), "ak8jets_cleaned"));
            // pre_modules.emplace_back(new GenericTopJetCleaner(ctx, PtEtaCut(150., 2.4), "patJetsHepTopTagCHSPacked_daughters"));
    }
    else {
        pre_modules.emplace_back(new GenericTopJetCorrector(ctx, JERFiles::Fall15_25ns_L23_AK8PFchs_DATA, "topjets"));
        pre_modules.emplace_back(new GenericTopJetCorrector(ctx, JERFiles::Fall15_25ns_L123_AK8PFchs_DATA, "patJetsAk8CHSJetsSoftDropPacked_daughters"));
        // pre_modules.emplace_back(new GenericTopJetCorrector(ctx, JERFiles::Fall15_25ns_L123_AK8PFchs_DATA, "patJetsHepTopTagCHSPacked_daughters"));
        pre_modules.emplace_back(new GenericSubJetCorrector(ctx, JERFiles::Fall15_25ns_L123_AK4PFchs_DATA, "topjets"));
        pre_modules.emplace_back(new GenericSubJetCorrector(ctx, JERFiles::Fall15_25ns_L123_AK4PFchs_DATA, "patJetsAk8CHSJetsSoftDropPacked_daughters"));
        // pre_modules.emplace_back(new GenericSubJetCorrector(ctx, JERFiles::Fall15_25ns_L123_AK4PFchs_DATA, "patJetsHepTopTagCHSPacked_daughters"));
        // ====== IMPLEMENT TOPJETLEPTONCLEANER BY KEYMATCHING!========
        // pre_modules.emplace_back(new TopJetLeptonCleaner(ctx, JERFiles::Fall15_25ns_L23_AK8PFchs_DATA));
        // pre_modules.emplace_back(new GenericTopJetCleaner(ctx, PtEtaCut(125., 2.4), "topjets"));
            // pre_modules.emplace_back(new TopJetLeptonCleaner(ctx, JERFiles::Fall15_25ns_L123_AK8PFchs_MC, "ak8jets_cleaned"));
            // pre_modules.emplace_back(new TopJetLeptonCleaner(ctx, JERFiles::Fall15_25ns_L123_AK8PFchs_MC, "patJetsHepTopTagCHSPacked_daughters"));
            // pre_modules.emplace_back(new GenericTopJetCleaner(ctx, PtEtaCut(150., 2.4), "ak8jets_cleaned"));
            // pre_modules.emplace_back(new GenericTopJetCleaner(ctx, PtEtaCut(150., 2.4), "patJetsHepTopTagCHSPacked_daughters"));
    }
    // pre_modules.emplace_back(new TopJetCleaner(ctx, MinMaxDeltaRId<Electron>(ctx, "electrons", 0.2), "topjets_cleaned"));
    // pre_modules.emplace_back(new TopJetCleaner(ctx, MinMaxDeltaRId<Muon>(ctx, "muons", 0.2), "topjets_cleaned"));

    // pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
    //             "topjets",
    //             "topjets_uncleaned"
    //             ));
    // pre_modules.emplace_back(new TopJetCleaner(ctx, MinMaxDeltaRId<Electron>(ctx, "electrons", 0.2), "topjets"));
    // pre_modules.emplace_back(new TopJetCleaner(ctx, MinMaxDeltaRId<Muon>(ctx, "muons", 0.2), "topjets"));
    pre_modules.emplace_back(new TopJetCleaner(ctx, PtEtaCut(0., 2.4), "topjets"));
    // pre_modules.emplace_back(new TopJetCleaner(ctx, PtEtaCut(200., 2.4), "topjets_uncleaned"));

    // other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx, "topjets_uncleaned", "n_topjets_uncleaned"));
    // other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx, "topjets_cleaned", "n_topjets_cleaned"));

          
    

    
    vector<string> categories = split(ctx.get("category", ""));
    // std::vector<string> categories = {"Mu45", "IsoMuo24", "Mu15_PFHT600", "PFHT800"}; // "NoSelection","IsoMuo24-clean", "Mu15_PFHT600-clean", "PFHT800-clean", "PFHT800-uncleaned"

    for (auto const & cat : categories) {

        string triggername = "trigger_accept_"+cat;
        SEL_ITEMS_FULL_SEL.push_back(SEL_ITEMS_NO_SEL);

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
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_muon_pt_iso", "Primary Muon p_{T}", 60, 0., 1200.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_electron_pt_iso", "Primary Electron p_{T}", 60, 0., 1200.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_muon_pt", "Primary Muon p_{T}", 60, 0., 1200.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_electron_pt", "Primary Electron p_{T}", 60, 0., 1200.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_lepton_pt_mva_loose", "Primary Lepton p_{T}", 60, 0., 1200.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_lepton_pt_iso", "Primary Lepton p_{T}", 60, 0., 1200.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_electron_pt_mva_loose", "Primary Lepton p_{T}", 60, 0., 1200.));
            // SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_lepton_pt", "Primary Lepton p_{T}", 60, 0., 1200.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_subld_ak4_jet", "Pt subleading Ak4 Jet", 60, 0., 1500.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_lepton_pt", "Primary Lepton p_{T}", 60, 0., 1200.));
        }
        else if (cat == "IsoMuo20") {
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_muon_pt_iso", "Primary Muon p_{T}", 60, 0., 1200., 40.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_isoMu20", "Trigger Accept", 2, -.5, 1.5, 1));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_subld_ak4_jet", "Pt subleading Ak4 Jet", 60, 0., 1500.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_lepton_pt", "Primary Lepton p_{T}", 60, 0., 1200.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_lepton_pt_iso", "Primary Lepton p_{T}", 60, 0., 1200.));
        }
        else if (cat == "IsoEle27") {
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_electron_pt_iso", "Primary Electron p_{T}", 60, 0., 1200., 40.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_isoEl27", "Trigger Accept", 2, -.5, 1.5, 1));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_isoMu20", "Trigger Accept", 2, -.5, 1.5, 0, 0));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_subld_ak4_jet", "Pt subleading Ak4 Jet", 60, 0., 1500.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_lepton_pt", "Primary Lepton p_{T}", 60, 0., 1200.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_lepton_pt_iso", "Primary Lepton p_{T}", 60, 0., 1200.));
        }
        else if (cat == "Mu45") {
            
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_mu45", "Trigger Accept", 2, -.5, 1.5, 1));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_muon_pt", "Primary Muon p_{T}", 60, 0., 1200., 47.));
            for (auto sel : SEL_ITEMS_BASELINE_SEL) {
                SEL_ITEMS_FULL_SEL.back().emplace_back(sel);
            }
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_subld_ak4_jet", "Pt subleading Ak4 Jet", 60, 0., 1500.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_el45", "Trigger Accept", 2, -.5, 1.5));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_lep_comb", "Trigger Accept", 2, -.5, 1.5));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_lepton_pt", "Primary Lepton p_{T}", 60, 0., 1200.));
            pos_2d_cut = 2;
        }
        else if (cat == "El45") {
            
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_el45", "Trigger Accept", 2, -.5, 1.5, 1));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_electron_pt", "Primary Electron p_{T}", 60, 0., 1200., 50.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500., 150.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_subld_ak4_jet", "Pt subleading Ak4 Jet", 60, 0., 1500., 35.));
            for (auto sel : SEL_ITEMS_BASELINE_SEL) {
                SEL_ITEMS_FULL_SEL.back().emplace_back(sel);
            }
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_mu45", "Trigger Accept", 2, -.5, 1.5, 0, 0));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_lep_comb", "Trigger Accept", 2, -.5, 1.5));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_lepton_pt", "Primary Lepton p_{T}", 60, 0., 1200.));
            pos_2d_cut = 4;
        }
        else if (cat == "El105") {
            
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_electron_pt", "Primary Electron p_{T}", 60, 0., 1200., 115.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_subld_ak4_jet", "Pt subleading Ak4 Jet", 60, 0., 1500.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_el105", "Trigger Accept", 2, -.5, 1.5, 1));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_mu45", "Trigger Accept", 2, -.5, 1.5, 0, 0));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_lep_comb", "Trigger Accept", 2, -.5, 1.5));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_lepton_pt_el105", "Primary Lepton p_{T}", 60, 0., 1200.));
        }
        else if (cat == "El45mva") {
            
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_electron_pt_mva_loose", "Primary Electron p_{T}", 60, 0., 1200., 50.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500., 150.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_subld_ak4_jet", "Pt subleading Ak4 Jet", 60, 0., 1500., 35.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_el45", "Trigger Accept", 2, -.5, 1.5, 1));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_mu45", "Trigger Accept", 2, -.5, 1.5, 0, 0));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_lep_comb", "Trigger Accept", 2, -.5, 1.5));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_lepton_pt", "Primary Lepton p_{T}", 60, 0., 1200.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_lepton_pt_mva_loose", "Primary Lepton p_{T}", 60, 0., 1200.));
        }
        // else if (cat == "MuElComb") {
            
        //     SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin(), new SelDatI("trigger_accept_lep_comb", "Trigger Accept", 2, -.5, 1.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin(), new SelDatF("primary_lepton_pt", "Primary Lepton p_{T}", 60, 0., 1200., 47.));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_mu45", "Trigger Accept", 2, -.5, 1.5));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_el45", "Trigger Accept", 2, -.5, 1.5));
        //     // SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+2, new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500.));
        //     // SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+3, new SelDatF("pt_subld_ak4_jet", "Pt subleading Ak4 Jet", 60, 0., 1500.));
        // }

        for (auto const & sel_item : ADDITIONAL_SEL_ITEMS)
            SEL_ITEMS_FULL_SEL.back().push_back(sel_item);

        // else if (cat == "Mu15_PFHT600") {
        //     other_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_Mu15_IsoVVVL_PFHT600_v*"}, triggername));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI(triggername, "Trigger Accept", 2, -.5, 1.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_muon_pt_noIso", "Primary Muon p_{T}", 60, 0., 1200., 40.));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatD("HT", "HT", 25, 0, 4500, 650));
        // }
        // else if (cat == "PFHT800") {
        //     if (type == "MC")
        //         other_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_PFHT800Emu_v*"}, triggername));
        //     else
        //         other_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_PFHT800_v*"}, triggername));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI(triggername, "Trigger Accept", 2, -.5, 1.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_muon_pt_noIso", "Primary Muon p_{T}", 60, 0., 1200., 40.));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatD("HT", "HT", 25, 0, 4500, 850));
        // }

        // unsigned pos_2d_cut = 4;

        other_modules.emplace_back(new TwoDCutProducer(ctx, "PrimaryMuon_iso", "TwoDcut_Dr_iso", "TwoDcut_Dpt_iso"));

        vector<string> item_names;
        for (auto const & seli : SEL_ITEMS_FULL_SEL.back()) 
            item_names.push_back(seli->name());

        sel_helpers.emplace_back(new SelItemsHelper(SEL_ITEMS_FULL_SEL.back(), ctx, item_names, cat+"_sel_accept", cat+"_sel_all_accepted"));
        // sel_helper.declare_items_for_output();
        sel_modules.emplace_back(new SelectionProducer(ctx, *sel_helpers.back()));

        // 3. Set up Hists classes:

        // TODO: set up and fill other histogram classes, e.g. your own HistCollector stuff

        v_hists.emplace_back(vector<shared_ptr<Hists>>());
        v_hists_after_sel.emplace_back(vector<shared_ptr<Hists>>());

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

        // string lep_pt = (cat == "IsoMuo20" || cat == "IsoEle27") ? "primary_muon_pt_iso" : "primary_lepton_pt";
        // string = (split(cat, "-").size() > 1 && split(cat, "-")[1] == "uncleaned") ? "_uncleaned" : "";
        map<string, SelectedSelHists*> selected_sel_hists;
        // selected_sel_hists["NoSTCut"] = new SelectedSelHists(ctx, cat+"/NoSTCut", *sel_helpers.back(), {}, {"ST"});
        // selected_sel_hists["NoNAk8JetsCut"] = new SelectedSelHists(ctx, cat+"/NoNAk8JetsCut", *sel_helpers.back(), {}, {"n_ak8"});
        // selected_sel_hists["NoNAk4Cut"] = new SelectedSelHists(ctx, cat+"/NoNAk4Cut", *sel_helpers.back(), {}, {"n_ak4"});
        // selected_sel_hists["NoNAk8Cut"] = new SelectedSelHists(ctx, cat+"/NoNAk8Cut", *sel_helpers.back(), {}, {"n_ak8"});
        // selected_sel_hists["NoNAk8NAk4Cut"] = new SelectedSelHists(ctx, cat+"/NoNAk8NAk4Cut", *sel_helpers.back(), {}, {"n_ak8", "n_ak4"});
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

        if (cat == "El105") {
            sel_modules.back()->insert_selection(pos_2d_cut, new TwoDCutSel(ctx, dr_2d, dpt_2d, "TwoDcut_Dr_noIso_el105", "TwoDcut_Dpt_noIso_el105"));
            nm1_hists->insert_hists(pos_2d_cut, new TwoDCutHist(ctx, cat+"/Nm1Selection", "TwoDcut_Dr_noIso_el105", "TwoDcut_Dpt_noIso_el105", "twod_cut_hist_noIso"));
        }
        else if (cat == "El45mva") {
            sel_modules.back()->insert_selection(pos_2d_cut, new TwoDCutSel(ctx, dr_2d, dpt_2d, "TwoDcut_Dr_noIso_mvaID", "TwoDcut_Dpt_noIso_mvaID"));
            nm1_hists->insert_hists(pos_2d_cut, new TwoDCutHist(ctx, cat+"/Nm1Selection", "TwoDcut_Dr_noIso_mvaID", "TwoDcut_Dpt_noIso_mvaID", "twod_cut_hist_mvaIDloose"));
        }
        else {
            sel_modules.back()->insert_selection(pos_2d_cut, new TwoDCutSel(ctx, dr_2d, dpt_2d, "TwoDcut_Dr_noIso", "TwoDcut_Dpt_noIso"));
            nm1_hists->insert_hists(pos_2d_cut, new TwoDCutHist(ctx, cat+"/Nm1Selection", "TwoDcut_Dr_noIso", "TwoDcut_Dpt_noIso", "twod_cut_hist_noIso"));
        }
        cf_hists->insert_step(pos_2d_cut, "2D cut");
        // if (cat == "MuElComb") {
        //     sel_modules.back()->insert_selection(pos_2d_cut-1, new TriggerAwareHandleSelection<float>(ctx, "pt_subld_ak4_jet", "trigger_accept_el45", 70., 0.));
        //     sel_modules.back()->insert_selection(pos_2d_cut-1, new TriggerAwareHandleSelection<float>(ctx, "pt_ld_ak4_jet", "trigger_accept_el45", 250., 0.));
        //     nm1_hists->insert_hists(pos_2d_cut-1, new HandleHist<float>(ctx, cat+"/Nm1Selection", "pt_subld_ak4_jet", "Pt subleading Ak4 Jet", 60, 0., 1500.));
        //     nm1_hists->insert_hists(pos_2d_cut-1, new HandleHist<float>(ctx, cat+"/Nm1Selection", "pt_ld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500.));
        //     cf_hists->insert_step(pos_2d_cut-1, "pt_subld_ak4_jet");
        //     cf_hists->insert_step(pos_2d_cut-1, "pt_ld_ak4_jet");
        //     v_hists_after_sel.back().emplace_back(new HandleHist<float>(ctx, cat+"/PostSelection", "pt_subld_ak4_jet", "Pt subleading Ak4 Jet", 60, 0., 1500.));
        //     v_hists_after_sel.back().emplace_back(new HandleHist<float>(ctx, cat+"/PostSelection", "pt_ld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500.));
        // }
        for (auto hist : selected_sel_hists) {
            hist.second->insert_hist_and_sel(pos_2d_cut, new TwoDCutHist(ctx, cat+"/"+hist.first, "TwoDcut_Dr_noIso", "TwoDcut_Dpt_noIso", "twod_cut_hist_noIso"), "twoD_cut");
            // if (cat == "MuElComb") {
            //     hist.second->insert_hist_and_sel(pos_2d_cut-1, new HandleHist<float>(ctx, cat+"/"+hist.first, "pt_ld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500.), "pt_ld_ak4_jet");
            //     hist.second->insert_hist_and_sel(pos_2d_cut-1, new HandleHist<float>(ctx, cat+"/"+hist.first, "pt_subld_ak4_jet", "Pt subleading Ak4 Jet", 60, 0., 1500.), "pt_subld_ak4_jet");
            // }
            hist.second->insert_additional_hist(ak8jet_hists->book_histograms(ctx, cat+"/"+hist.first));
            // hist.second->insert_additional_hist(new JetCleaningControlPlots(ctx, cat+"/"+hist.first+"/JetCleaningControlPlots", "weight_ak4_jetpt"));
            // for (auto const & hist_helper : fatjet_hists) {
            //     hist.second->insert_additional_hist(hist_helper.book_histograms(ctx, cat+"/"+hist.first));
            // }
            hist.second->insert_additional_hist(new OwnHistCollector(ctx, cat+"/"+hist.first, type == "MC", CSVBTag(CSVBTag::WP_MEDIUM), {"mu", "el", "cmstopjet", "ak8softdroptopjet"}));
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
        v_hists_after_sel.back().emplace_back(new OwnHistCollector(ctx, cat+"/PostSelection", type == "MC", CSVBTag(CSVBTag::WP_MEDIUM), {"ev", "mu", "el", "jet", "lumi", "cmstopjet", "ak8softdroptopjet"}));
        // v_hists_after_sel.back().emplace_back(new ExtendedTopJetHists(ctx, cat+"/PostSelection/Ak8JetsUnCleaned", CSVBTag(CSVBTag::WP_MEDIUM), 2, "topjets_uncleaned"));
        if (version.find("TpTp") != string::npos) {
            CustomizableGenHists * gen_hists = new CustomizableGenHists(ctx, cat+"/NoSelection/GenHists");
            gen_hists->add_genhistcoll(8000001, 0, {"mass", "decay", "dRDecay", "dPhiDecay", "dEtaDecay"});
            gen_hists->add_genhistcoll(8000001, 0, {"mass", "decay", "dRDecay", "dPhiDecay", "dEtaDecay"}, GenParticleId(GenParticleDaughterId(8000001, 6, 25)), "_to_tH");
            gen_hists->add_genhistcoll(6, 0, {"decay", "dRDecay", "dPhiDecay", "dEtaDecay"});
            gen_hists->add_genhistcoll(25, 0, {"decay", "dRDecay", "dPhiDecay", "dEtaDecay"});
            gen_hists->add_genhistcoll(25, 0, {"decay", "dRDecay", "dPhiDecay", "dEtaDecay"}, GenParticleId(GenParticleDaughterId(25, 5, 5)), "_to_bb");
            v_hists.back().push_back(shared_ptr<CustomizableGenHists>(gen_hists));
        }
        // v_hists_after_sel.back().emplace_back(new JetCleaningControlPlots(ctx, cat+"/PostSelection/JetCleaningControlPlots", "weight_ak4_jetpt"));
        // v_hists_after_sel.back().emplace_back(new JetCleaningControlPlots(ctx, cat+"/PostSelection/JetCleaningControlPlotsUp", "weight_ak4_jetpt_up"));
        // v_hists_after_sel.back().emplace_back(new JetCleaningControlPlots(ctx, cat+"/PostSelection/JetCleaningControlPlotsDown", "weight_ak4_jetpt_down"));
        // v_hists_after_sel.emplace_back(new HistCollector(ctx, "EventHistsPost"));
        if ((cat == "El45" || cat == "Mu45") && ctx.get("dataset_type", "") == "MC")
            v_hists_after_sel.back().emplace_back(new BTagMCEfficiencyHists(ctx, cat+"/BTagMCEfficiencyHists", CSVBTag::WP_MEDIUM, "tj_btag_sf_coll"));

    }


}


bool TpTpPreselectionV2::process(Event & event) {

    if (!common_module->process(event)) {
        return false;
    }

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
        if (pass_sel) {
            return true;
        }
    }


    return false;
}

UHH2_REGISTER_ANALYSIS_MODULE(TpTpPreselectionV2)
