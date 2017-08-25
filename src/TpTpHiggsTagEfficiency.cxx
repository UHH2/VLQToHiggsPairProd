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
#include "UHH2/common/include/JetCorrections.h"
#include "UHH2/common/include/MCWeight.h"
#include "UHH2/common/include/ObjectIdUtils.h"
#include "UHH2/common/include/CollectionProducer.h"
#include "UHH2/common/include/JetHists.h"
#include "UHH2/common/include/TTbarGen.h"
#include "UHH2/common/include/TTbarGenHists.h"


#include "UHH2/VLQSemiLepPreSel/include/EventHists.h"
#include "UHH2/VLQSemiLepPreSel/include/CustomizableGenHists.h"
#include "UHH2/VLQSemiLepPreSel/include/VLQCommonModules.h"
#include "UHH2/VLQSemiLepPreSel/include/SelectionHists.h"
#include "UHH2/VLQSemiLepPreSel/include/SelectionItem.h"
// #include "UHH2/VLQToHiggsPairProd/include/VLQPair_selectionItems.h"
#include "UHH2/VLQToHiggsPairProd/include/VLQPair_additionalModules.h"
#include "UHH2/VLQToHiggsPairProd/include/VLQPair_additionalHists.h"
#include "UHH2/VLQToHiggsPairProd/include/VLQPair_massReco.h"
// #include "UHH2/VLQToHiggsPairProd/include/VLQPair_triggerPaths.h"
// #include "UHH2/VLQToHiggsPairProd/include/TpTpCommonModules.h"
#include "UHH2/VLQToHiggsPairProd/include/TpTpAnalysisModule.h"

using namespace std;
using namespace uhh2;

// using namespace vlqToHiggsPair;

// typedef VectorAndSelection MyAndSelection;

class TpTpHiggsTagEfficiency: public TpTpAnalysisModule {
public:

    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_BASELINE_SEL {
        shared_ptr<SelectionItem>(new SelDatI("gendecay_accept", "GenDecay Accept", 2, -.5, 1.5, 1)),
        // shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 10, -.5, 9.5, 2)),
        };

    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_EL45_SEL {
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_el45", "Trigger Accept", 2, -.5, 1.5, 1)),
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_mu45", "Trigger Accept Mu45", 2, -.5, 1.5, 0, 0)),
        shared_ptr<SelectionItem>(new SelDatF("primary_electron_pt", "Primary Lepton p_T", 100, 0., 1200., 50.)),
        shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 100, 0., 2000., 250.)),
        shared_ptr<SelectionItem>(new SelDatF("pt_subld_ak4_jet", "Pt subleading Ak4 Jet", 40, 0., 1600., 70.)),
        shared_ptr<SelectionItem>(new SelDatF("primary_muon_pt", "Primary Lepton p_T", 100, 0., 1200.)),
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_lep_comb", "Trigger Accept", 2, -.5, 1.5)),
        shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt", "Primary Lepton p_T", 100, 0., 1200.)),
        // shared_ptr<SelectionItem>(new SelDatF("primary_electron_pt_tight", "Primary Lepton p_T", 100, 0., 1200.)),
        // shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 10, -.5, 9.5, 2)),
        };

    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_Mu45_SEL {
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_mu45", "Trigger Accept", 2, -.5, 1.5, 1)),
        shared_ptr<SelectionItem>(new SelDatF("primary_muon_pt", "Primary Lepton p_T", 100, 0., 1200., 47.)),
        shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 100, 0., 2000.)),
        shared_ptr<SelectionItem>(new SelDatF("pt_subld_ak4_jet", "Pt subleading Ak4 Jet", 40, 0., 1600.)),
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_el45", "Trigger Accept El45", 2, -.5, 1.5)),
        shared_ptr<SelectionItem>(new SelDatF("primary_electron_pt", "Primary Lepton p_T", 100, 0., 1200.)),
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_lep_comb", "Trigger Accept", 2, -.5, 1.5)),
        shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt", "Primary Lepton p_T", 100, 0., 1200.)),
        // shared_ptr<SelectionItem>(new SelDatF("primary_electron_pt_tight", "Primary Lepton p_T", 100, 0., 1200.)),
        // shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 10, -.5, 9.5, 2)),
        };

    explicit TpTpHiggsTagEfficiency(Context & ctx);
    virtual bool process(Event & event) override;

private:
    unique_ptr<AnalysisModule> common_module;
    // unique_ptr<NParticleMultiHistProducerHelper<TopJet>> ak8jet_hists/*, ca15jet_hists*/;
    unique_ptr<AnalysisModule> btag_sf_sr, btag_sf_cr, ele_trg_sf, ele_trg_nosf;
    Event::Handle<double> weight_hndl;
    Event::Handle<float> weight_ele_hndl;
    // Event::Handle<float> jetpt_weight_hndl;
    // Event::Handle<int> use_sr_sf_hndl;
    // vector<vector<unique_ptr<Hists>>> v_reweighted_hists_after_sel;
    vector<shared_ptr<Hists>> v_lep_combined_hists;
    vector<string> categories;

};



TpTpHiggsTagEfficiency::TpTpHiggsTagEfficiency(Context & ctx) : TpTpAnalysisModule(ctx) {

    auto data_dir_path = ctx.get("data_dir_path");
    CommonModules* commonObjectCleaning = new CommonModules();
    // commonObjectCleaning->set_jet_id(AndId<Jet>(JetPFID(JetPFID::WP_LOOSE), PtEtaCut(30.0,2.4)));
    commonObjectCleaning->disable_jersmear();
    commonObjectCleaning->disable_jec();
    commonObjectCleaning->disable_mcpileupreweight();
    // commonObjectCleaning->set_electron_id(AndId<Electron>(ElectronID_Spring15_25ns_medium_noIso,PtEtaCut(20.0, 2.4)));
    // commonObjectCleaning->set_muon_id(AndId<Muon>(MuonIDTight(),PtEtaCut(20.0, 2.1)));
    // commonObjectCleaning->switch_jetlepcleaner(true);
    // commonObjectCleaning->switch_jetPtSorter(true);
    // commonObjectCleaning->disable_lumisel();
    commonObjectCleaning->init(ctx);
    common_module.reset(commonObjectCleaning);

    // other_modules.emplace_back(new MCPileupReweight(ctx));
    
    weight_hndl = ctx.declare_event_output<double>("weight");


    // auto ak8_corr_bef = (type == "MC") ? JERFiles::Fall15_25ns_L23_AK8PFchs_MC 
    // : JERFiles::Fall15_25ns_L23_AK8PFchs_DATA;
    // auto ak8_corr_aft = (type == "MC") ? JERFiles::Fall15_25ns_L123_AK8PFchs_MC 
    // : JERFiles::Fall15_25ns_L123_AK8PFchs_DATA;
    // auto ak4_corr = (type == "MC") ? JERFiles::Fall15_25ns_L123_AK4PFchs_MC 
    // : JERFiles::Fall15_25ns_L123_AK4PFchs_DATA;
    // // if (ctx.get("jecsmear_direction", "nominal") != "nominal") {
    // pre_modules.emplace_back(new GenericTopJetCorrector(ctx,
    //     ak8_corr_bef, "topjets"));
    // pre_modules.emplace_back(new GenericSubJetCorrector(ctx,
    //     ak4_corr, "topjets"));
    // pre_modules.emplace_back(new AK8SoftDropCorr(ctx, "topjets"));
    // pre_modules.emplace_back(new GenericTopJetCorrector(ctx,
    //     ak8_corr_aft, "topjets"));
    // pre_modules.emplace_back(new JetCorrector(ctx, ak4_corr));
    // // }


    // if (type == "MC") {
    //     pre_modules.emplace_back(new JetResolutionSmearer(ctx));
    // }

    // pre_modules.emplace_back(new JetCleaner(ctx, AndId<Jet>(JetPFID(JetPFID::WP_LOOSE), PtEtaCut(30.0,2.4))));
    // other_modules.emplace_back(new MCMuonScaleFactor(ctx, 
    //     data_dir_path + "MuonID_Z_RunCD_Reco76X_Feb15.root", 
    //     "MC_NUM_MediumID_DEN_genTracks_PAR_pt_spliteta_bin1", 1., "id", "nominal", "prim_mu_coll"));
    // other_modules.emplace_back(new MCMuonScaleFactor(ctx, 
    //     data_dir_path + "SingleMuonTrigger_Z_RunCD_Reco76X_Feb15.root", 
    //     "runD_Mu45_eta2p1_PtEtaBins", 0.5, "trg", "nominal", "prim_mu_coll"));
    // // other_modules.emplace_back(new MCElectronScaleFactor(ctx, 
    // //     ctx.get("ele_sf_trg_file"), 
    // //     "CutBasedMedium", 0., "id", "nominal", "prim_ele_coll"));
    // other_modules.emplace_back(new MCElectronScaleFactor(ctx, 
    //     ctx.get("ele_sf_trg_file"), 
    //     "EGamma_SF2D", 0., "id", "nominal", "prim_ele_coll", true));
    // ele_trg_sf.reset(new MCConstantScalefactor(ctx, 
    //             0.99, 0.02, "sfel_trg", true));
    // ele_trg_nosf.reset(new MCConstantScalefactor(ctx, 
    //             1., 0., "sfel_trg", true));
   

    // weight_ele_hndl = ctx.get_handle<float>("weight_el_trg");

    // =====PRODUCERS========

    // other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
    //             "topjets",
    //             "ak8_nonoverlap",
    //             TopJetId(MinMaxDeltaRId<TopJet>(ctx, "higgs_tags_1b_med", 1.))
    //             ));

    other_modules.emplace_back(new CollectionProducer<Jet>(ctx,
                "jets",
                "ak4_jets_btagged",
                JetId(CSVBTag(CSVBTag::WP_MEDIUM))
                ));

    // btag_sf_sr.reset(new MCBTagScaleFactor(ctx, CSVBTag::WP_MEDIUM, "ak8_higgs_cand"));

    // DISABLE WHEN CALCULATING PRODUCING THE BTAG EFFICIENCY HISTS!
    // bool create_btag_eff = string2bool(ctx.get("create_btag_eff", "false"));
    // if (!create_btag_eff) {
    //     // other_modules.emplace_back(new MCBTagScaleFactor(ctx, CSVBTag::WP_MEDIUM, "tj_btag_sf_coll"));
    //     other_modules.emplace_back(new MCBTagScaleFactor(ctx, CSVBTag::WP_MEDIUM, "jets_no_overlap"));
    //     other_modules.emplace_back(new MCBTagScaleFactor(ctx, CSVBTag::WP_MEDIUM, "ak8_higgs_cand",
    //                                                         "central",
    //                                                         "lt",
    //                                                         "incl",
    //                                                         "MCBtagEfficiencies",
    //                                                         "_sj",
    //                                                         "BTagCalibrationSubjet"));

    // }
        // btag_sf_cr.reset(new MCBTagScaleFactor(ctx, CSVBTag::WP_MEDIUM, "tj_btag_sf_coll"));

    // other_modules.emplace_back(new HiggsMassSmear(ctx,
    //             "topjets",
    //             false, false
    //             ));
    // other_modules.emplace_back(new HiggsMassSmear(ctx,
    //             "ak8_boost",
    //             false, false
    //             ));
    // other_modules.emplace_back(new HiggsMassSmear(ctx,
    //             "nomass_boost_1b",
    //             false, false
    //             ));
    // other_modules.emplace_back(new HiggsMassSmear(ctx,
    //             "nomass_boost_2b",
    //             false, false
    //             ));


    
    common_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "topjets",
                "higgs_tags_1b_med_nopt",
                TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)))
                ));
    common_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "topjets",
                "higgs_tags_2b_med_nopt",
                TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)))
                ));




    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost",
                "higgs_tags_1b_med",
                TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)))
                // true
                ));
    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost",
                "higgs_tags_2b_med",
                TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)))
                // true
                ));
    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost",
                "higgs_tags_1b_med",
                TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)))
                ));
    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost",
                "higgs_tags_2b_med",
                TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)))
                ));


    if (version.find("thth") != string::npos) {
        other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
            GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::TopID, ParticleID::HiggsID)),
            GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::TopID, ParticleID::HiggsID))
            ));
    }
    else if (version.find("thtz") != string::npos) {
        other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
            GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::TopID, ParticleID::HiggsID)),
            GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::TopID, ParticleID::ZID))
            ));
    }
    else if (version.find("thbw") != string::npos) {
        other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
            GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::TopID, ParticleID::HiggsID)),
            GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::BottomID, ParticleID::WID))
            ));
    }
    else if (version.find("noH_tztz") != string::npos) {
        other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
            GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::TopID, ParticleID::ZID)),
            GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::TopID, ParticleID::ZID))
            ));
    }
    else if (version.find("noH_tzbw") != string::npos) {
        other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
            GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::TopID, ParticleID::ZID)),
            GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::BottomID, ParticleID::WID))
            ));
    }
    else if (version.find("noH_bwbw") != string::npos) {
        other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
            GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::BottomID, ParticleID::WID)),
            GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::BottomID, ParticleID::WID))
            ));
    }
    else if (version.find("bhbh") != string::npos) {
        other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
            GenParticleId(GenParticleDaughterId(ParticleID::BprimeID, ParticleID::BottomID, ParticleID::HiggsID)),
            GenParticleId(GenParticleDaughterId(ParticleID::BprimeID, ParticleID::BottomID, ParticleID::HiggsID))
            ));
    }
    else if (version.find("bhbz") != string::npos) {
        other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
            GenParticleId(GenParticleDaughterId(ParticleID::BprimeID, ParticleID::BottomID, ParticleID::HiggsID)),
            GenParticleId(GenParticleDaughterId(ParticleID::BprimeID, ParticleID::BottomID, ParticleID::ZID))
            ));
    }
    else if (version.find("bhtw") != string::npos) {
        other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
            GenParticleId(GenParticleDaughterId(ParticleID::BprimeID, ParticleID::BottomID, ParticleID::HiggsID)),
            GenParticleId(GenParticleDaughterId(ParticleID::BprimeID, ParticleID::TopID, ParticleID::WID))
            ));
    }
    else if (version.find("noH_bzbz") != string::npos) {
        other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
            GenParticleId(GenParticleDaughterId(ParticleID::BprimeID, ParticleID::BottomID, ParticleID::ZID)),
            GenParticleId(GenParticleDaughterId(ParticleID::BprimeID, ParticleID::BottomID, ParticleID::ZID))
            ));
    }
    else if (version.find("noH_bztw") != string::npos) {
        other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
            GenParticleId(GenParticleDaughterId(ParticleID::BprimeID, ParticleID::BottomID, ParticleID::ZID)),
            GenParticleId(GenParticleDaughterId(ParticleID::BprimeID, ParticleID::TopID, ParticleID::WID))
            ));
    }
    else if (version.find("noH_twtw") != string::npos) {
        other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
            GenParticleId(GenParticleDaughterId(ParticleID::BprimeID, ParticleID::TopID, ParticleID::WID)),
            GenParticleId(GenParticleDaughterId(ParticleID::BprimeID, ParticleID::TopID, ParticleID::WID))
            ));
    }

    else {
        other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
            GenParticleId(TrueId<GenParticle>::is_true), GenParticleId(TrueId<GenParticle>::is_true)));
    }

    other_modules.emplace_back(new TrueFalseProducer(ctx, "chan_accept", false));

    categories = split(ctx.get("category", ""));

    // for (auto const & fs : final_states) {
    for (auto const & cat : categories) {


        SEL_ITEMS_FULL_SEL.push_back(SEL_ITEMS_BASELINE_SEL);


        if (split(cat, "_")[0] == "Mu45") {
            for (auto const & sel_item : SEL_ITEMS_Mu45_SEL)
                SEL_ITEMS_FULL_SEL.back().push_back(sel_item);
        }
        else if (split(cat, "_")[0] == "El45") {
            for (auto const & sel_item : SEL_ITEMS_EL45_SEL)
                SEL_ITEMS_FULL_SEL.back().push_back(sel_item);
        }
        
        // if (version.find("SingleEle") != string::npos && split(cat, "_")[0] == "Mu45") {
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("chan_accept", "GenDecay Accept", 2, -.5, 1.5, 1));
        // }
        // else if (version.find("SingleMuon") != string::npos && split(cat, "_")[0] == "El45") {
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("chan_accept", "GenDecay Accept", 2, -.5, 1.5, 1));
        // }
        
        // else if (split(cat, "_")[0] == "El45MVALoose") {
        //     for (auto const & sel_item : SEL_ITEMS_EL45MVALOOSE_SEL)
        //         SEL_ITEMS_FULL_SEL.back().push_back(sel_item);
        // }
        // else if (split(cat, "_")[0] == "El45MVATight") {
        //     for (auto const & sel_item : SEL_ITEMS_EL45MVATIGHT_SEL)
        //         SEL_ITEMS_FULL_SEL.back().push_back(sel_item);
        // }



        // for (auto const & sel_item : ADDITIONAL_SEL_ITEMS)
        //     SEL_ITEMS_FULL_SEL.back().push_back(sel_item);

        // if (type == "MC") {
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatD("parton_ht", "Parton HT", 45, 0, 4500));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_ld_ak4_genjet", "Pt first Ak4 GenJet", 100, 0., 2000.));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_subld_ak4_genjet", "Pt second Ak4 GenJet", 40, 0., 1600.));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_third_ak4_genjet", "Pt third Ak4 GenJet", 50, 0., 1000.));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_fourth_ak4_genjet", "Pt fourth Ak4 GenJet", 30, 0., 600.));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_fifth_ak4_genjet", "Pt fifth Ak4 GenJet", 25, 0., 500.));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_sixth_ak4_genjet", "Pt sixth Ak4 GenJet", 20, 0., 400.));
        // }


        vector<string> item_names;
        for (auto const & seli : SEL_ITEMS_FULL_SEL.back()) 
            item_names.push_back(seli->name());

        sel_helpers.emplace_back(new SelItemsHelper(SEL_ITEMS_FULL_SEL.back(), ctx, item_names, "sel_accept_"+cat, "sel_all_accepted_"+cat));
        // sel_helper.declare_items_for_output();
        sel_modules.emplace_back(new SelectionProducer(ctx, *sel_helpers.back()));

        // if (split(cat, "-")[0] == "HiggsTag0Med") {
        sel_helpers.back()->declare_items_for_output();
        // }
        // 3. Set up Hists classes:

        // TODO: set up and fill other histogram classes, e.g. your own HistCollector stuff

        v_hists.emplace_back(vector<shared_ptr<Hists>>());
        v_hists_after_sel.emplace_back(vector<shared_ptr<Hists>>());
        // v_reweighted_hists_after_sel.emplace_back(vector<shared_ptr<Hists>>());
        // v_genhist_2h_after_sel.emplace_back(vector<shared_ptr<Hists>>());
        // v_genhist_1h_after_sel.emplace_back(vector<shared_ptr<Hists>>());


        // auto nm1_hists = new Nm1SelHists(ctx, cat+"/Nm1Selection", *sel_helpers.back());
        // auto cf_hists = new VLQ2HTCutflow(ctx, cat+"/Cutflow", *sel_helpers.back());

        

        // v_hists.back().emplace_back(nm1_hists);
        // v_hists.back().emplace_back(cf_hists);
        sel_helpers.back()->fill_hists_vector(v_hists.back(), cat+"/NoSelection");
        sel_helpers.back()->fill_hists_vector(v_hists_after_sel.back(), cat+"/PostSelection");

        
        if (version.find("TpTp") != string::npos || version.find("BpBp") != string::npos) {

            ///////// HIGGS TAG EFFICIENCIES FOR MULTIPLE GEN REQUIREMENTS AS FUNCTION OF RECO VARIABLES
            // v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/HiggsTagEfficiencyPreNoPt", "ak8_1b", "topjets",
            //     TopJetId(JetClosestGenPartId(25, 5, 0.8)), TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)))));
            // v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/HiggsTagEfficiencyPreNoPt", "ak8_2b", "topjets",
            //     TopJetId(JetClosestGenPartId(25, 5, 0.8)), TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)))));

            // v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/HiggsTagEfficiencyPre", "ak8_1b", "topjets",
            //     TopJetId(JetClosestGenPartId(25, 5, 0.8)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
            // v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/HiggsTagEfficiencyPre", "ak8_2b", "topjets",
            //     TopJetId(JetClosestGenPartId(25, 5, 0.8)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));

            // v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/HiggsTagEfficiencyPreHiggsPt300", "ak8_1b", "topjets",
            //     TopJetId(JetClosestGenPartId(25, 5, 0.8, 300.)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
            // v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/HiggsTagEfficiencyPreHiggsPt300", "ak8_2b", "topjets",
            //     TopJetId(JetClosestGenPartId(25, 5, 0.8, 300.)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));

            // v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/HiggsTagEfficiencyPreHiggsBsInJet", "ak8_1b", "topjets",
            //     TopJetId(JetClosestGenPartId(25, 5, 0.8, 0., true)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
            // v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/HiggsTagEfficiencyPreHiggsBsInJet", "ak8_2b", "topjets",
            //     TopJetId(JetClosestGenPartId(25, 5, 0.8, 0., true)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));

            // v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/HiggsTagEfficiencyPreHiggsPt300BsInJet", "ak8_1b", "topjets",
            //     TopJetId(JetClosestGenPartId(25, 5, 0.8, 300., true)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
            // v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/HiggsTagEfficiencyPreHiggsPt300BsInJet", "ak8_2b", "topjets",
            //     TopJetId(JetClosestGenPartId(25, 5, 0.8, 300., true)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
            // v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/HiggsTagEfficiencyPreHiggsPt300BsInJet", "ak8_ex_1b", "topjets",
            //     TopJetId(JetClosestGenPartId(25, 5, 0.8, 300., true)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), VetoId<Jet>(CSVBTag(CSVBTag::WP_MEDIUM))), PtEtaCut(300., 3.)))));

            ///////// HIGGS TAG EFFICIENCIES FOR MULTIPLE GEN REQUIREMENTS AS FUNCTION OF GEN VARIABLES
            v_hists.back().emplace_back(new TagEffHists<GenParticle>(ctx, cat+"/HiggsTagEfficiencyPreGenPart", "ak8_1b", "genparticles",
                GenParticleId(GenPartClosestJetID<TopJet>(ctx, "topjets", 25, 5, 0.8)), GenParticleId(GenPartClosestJetID<TopJet>(ctx, "higgs_tags_1b_med", 25, 5, 0.8))));
            v_hists.back().emplace_back(new TagEffHists<GenParticle>(ctx, cat+"/HiggsTagEfficiencyPreGenPart", "ak8_2b", "genparticles",
                GenParticleId(GenPartClosestJetID<TopJet>(ctx, "topjets", 25, 5, 0.8)), GenParticleId(GenPartClosestJetID<TopJet>(ctx, "higgs_tags_2b_med", 25, 5, 0.8))));

            v_hists.back().emplace_back(new TagEffHists<GenParticle>(ctx, cat+"/HiggsTagEfficiencyPreGenPartHiggsPt300", "ak8_1b", "genparticles",
                GenParticleId(GenPartClosestJetID<TopJet>(ctx, "topjets", 25, 5, 0.8, 300.)), GenParticleId(GenPartClosestJetID<TopJet>(ctx, "higgs_tags_1b_med", 25, 5, 0.8, 300.))));
            v_hists.back().emplace_back(new TagEffHists<GenParticle>(ctx, cat+"/HiggsTagEfficiencyPreGenPartHiggsPt300", "ak8_2b", "genparticles",
                GenParticleId(GenPartClosestJetID<TopJet>(ctx, "topjets", 25, 5, 0.8, 300.)), GenParticleId(GenPartClosestJetID<TopJet>(ctx, "higgs_tags_2b_med", 25, 5, 0.8, 300.))));

            v_hists.back().emplace_back(new TagEffHists<GenParticle>(ctx, cat+"/HiggsTagEfficiencyPreGenPartHiggsBsInJet", "ak8_1b", "genparticles",
                GenParticleId(GenPartClosestJetID<TopJet>(ctx, "topjets", 25, 5, 0.8, 0., true)), GenParticleId(GenPartClosestJetID<TopJet>(ctx, "higgs_tags_1b_med", 25, 5, 0.8, 300., true))));
            v_hists.back().emplace_back(new TagEffHists<GenParticle>(ctx, cat+"/HiggsTagEfficiencyPreGenPartHiggsBsInJet", "ak8_2b", "genparticles",
                GenParticleId(GenPartClosestJetID<TopJet>(ctx, "topjets", 25, 5, 0.8, 0., true)), GenParticleId(GenPartClosestJetID<TopJet>(ctx, "higgs_tags_2b_med", 25, 5, 0.8, 300., true))));

            v_hists.back().emplace_back(new TagEffHists<GenParticle>(ctx, cat+"/HiggsTagEfficiencyPreGenPartHiggsPt300BsInJet", "ak8_1b", "genparticles",
                GenParticleId(GenPartClosestJetID<TopJet>(ctx, "topjets", 25, 5, 0.8, 300., true)), GenParticleId(GenPartClosestJetID<TopJet>(ctx, "higgs_tags_1b_med", 25, 5, 0.8, 300., true))));
            v_hists.back().emplace_back(new TagEffHists<GenParticle>(ctx, cat+"/HiggsTagEfficiencyPreGenPartHiggsPt300BsInJet", "ak8_2b", "genparticles",
                GenParticleId(GenPartClosestJetID<TopJet>(ctx, "topjets", 25, 5, 0.8, 300., true)), GenParticleId(GenPartClosestJetID<TopJet>(ctx, "higgs_tags_2b_med", 25, 5, 0.8, 300., true))));

            ///////// EFFICIENCIES OF HIGGS TAGGING CUTS
            v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/PtCutEfficiencyPre", "ak8_1b", "topjets",
                TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), JetClosestGenPartId(25, 5, 0.8))), TopJetId(PtEtaCut(300., 3.))));
            v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/PtCutEfficiencyPre", "ak8_2b", "topjets",
                TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), JetClosestGenPartId(25, 5, 0.8))), TopJetId(PtEtaCut(300., 3.))));

            v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MassCutEfficiencyPre", "ak8_1b", "topjets",
                TopJetId(AndId<TopJet>(HiggsFlexBTag(0., 999999., CSVBTag(CSVBTag::WP_MEDIUM)), JetClosestGenPartId(25, 5, 0.8, 0., true), PtEtaCut(300., 3.))), TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)))));
            v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MassCutEfficiencyPre", "ak8_2b", "topjets",
                TopJetId(AndId<TopJet>(HiggsFlexBTag(0., 999999., CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), JetClosestGenPartId(25, 5, 0.8, 0., true), PtEtaCut(300., 3.))), TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)))));

            v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/SubjetBtagCutEfficiencyPre", "ak8_1b", "topjets",
                TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS), JetClosestGenPartId(25, 5, 0.8, 0., true), PtEtaCut(300., 3.))), TopJetId(HiggsFlexBTag(0., 999999., CSVBTag(CSVBTag::WP_MEDIUM)))));
            v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/SubjetBtagCutEfficiencyPre", "ak8_2b", "topjets",
                TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS), JetClosestGenPartId(25, 5, 0.8, 0., true), PtEtaCut(300., 3.))), TopJetId(HiggsFlexBTag(0., 999999., CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)))));
            
            CustomizableGenHists * gen_hists = new CustomizableGenHists(ctx, cat+"/NoSelection/GenHists");
            gen_hists->add_genhistcoll(8000001, 0, {"mass", "decay", "dRDecay", "dPhiDecay", "dEtaDecay"});
            gen_hists->add_genhistcoll(8000001, 0, {"mass", "decay", "dRDecay", "dPhiDecay", "dEtaDecay"}, GenParticleId(GenParticleDaughterId(8000001, 6, 25)), "_to_tH");
            gen_hists->add_genhistcoll(6, 0, {"decay", "dRDecay", "dPhiDecay", "dEtaDecay"});
            gen_hists->add_genhistcoll(11, 0, {"charge", "mother", "number"});
            gen_hists->add_genhistcoll(13, 0, {"charge", "mother", "number"});
            gen_hists->add_genhistcoll(11, 0, {"charge", "mother", "number"}, GenParticleId(GenParticleMotherId(0, 6)), "_from_T");
            gen_hists->add_genhistcoll(13, 0, {"charge", "mother", "number"}, GenParticleId(GenParticleMotherId(0, 6)), "_from_T");
            gen_hists->add_genhistcoll(11, 0, {"charge", "mother", "number"}, GenParticleId(GenParticleMotherId(6)), "_from_top");
            gen_hists->add_genhistcoll(13, 0, {"charge", "mother", "number"}, GenParticleId(GenParticleMotherId(6)), "_from_top");
            gen_hists->add_genhistcoll(25, 0, {"decay", "dRDecay", "dPhiDecay", "dEtaDecay"});
            gen_hists->add_genhistcoll(25, 0, {"decay", "dRDecay", "dPhiDecay", "dEtaDecay", "2d_dRDecay_pt"}, GenParticleId(GenParticleDaughterId(25, 5, 5)), "_to_bb");
            v_hists.back().push_back(shared_ptr<CustomizableGenHists>(gen_hists));
            v_hists.back().emplace_back(new RecoGenVarComp<double>(ctx, cat+"/NoSelection/RecoGenComparisons", "HT", "parton_ht", "HT_parton")); 
            v_hists.back().emplace_back(new RecoGenVarComp<double>(ctx, cat+"/NoSelection/RecoGenComparisons", "HT", "gen_ht", "HT_gen")); 
            // v_hists.back().emplace_back(new TTbarGenHists(ctx, cat+"/NoSelection/TTGenHists"));
        }

            // v_hists_after_sel.back().emplace_back(new TagEffHists<TopJet>(ctx, cat+"/HiggsTagEfficiencyPost", "all_ak8_1b", "topjets",
            //     TopJetId(JetClosestGenPartId(25, 5, 0.8)), TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)))));
            // v_hists_after_sel.back().emplace_back(new TagEffHists<TopJet>(ctx, cat+"/HiggsTagEfficiencyPost", "all_ak8_2b", "topjets",
            //     TopJetId(JetClosestGenPartId(25, 5, 0.8)), TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)))));
            // v_hists.back().emplace_back(new TagEffHists<TopJet>(ctx, cat+"/MisTagRateOtherHiggsPre", "all_ak8_1b", "topjets",
            //     TopJetId(AndId<TopJet>(VetoId<TopJet>(JetClosestGenPartId(25, 5)), JetClosestGenPartId(25, ))), TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)))));
            // v_hists.back().emplace_back(new TagEffHists<TopJet>(ctx, cat+"/MisTagRateOtherHiggsPre", "all_ak8_2b", "topjets",
            //     TopJetId(AndId<TopJet>(VetoId<TopJet>(JetClosestGenPartId(25, 5)), JetClosestGenPartId(25, ))), TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)))));
            // v_hists_after_sel.back().emplace_back(new TagEffHists<TopJet>(ctx, cat+"/MisTagRateOtherHiggsPost", "all_ak8_1b", "topjets",
            //     TopJetId(AndId<TopJet>(VetoId<TopJet>(JetClosestGenPartId(25, 5)), JetClosestGenPartId(25, ))), TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)))));
            // v_hists_after_sel.back().emplace_back(new TagEffHists<TopJet>(ctx, cat+"/MisTagRateOtherHiggsPost", "all_ak8_2b", "topjets",
            //     TopJetId(AndId<TopJet>(VetoId<TopJet>(JetClosestGenPartId(25, 5)), JetClosestGenPartId(25, ))), TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)))));
            // v_hists.back().emplace_back(new TagEffHists<TopJet>(ctx, cat+"/MisTagRateNoHiggsPre", "all_ak8_1b", "topjets",
            //     TopJetId(VetoId<TopJet>(JetClosestGenPartId(25, ))), TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)))));
            // v_hists.back().emplace_back(new TagEffHists<TopJet>(ctx, cat+"/MisTagRateNoHiggsPre", "all_ak8_2b", "topjets",
            //     TopJetId(VetoId<TopJet>(JetClosestGenPartId(25, ))), TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)))));
            // v_hists_after_sel.back().emplace_back(new TagEffHists<TopJet>(ctx, cat+"/MisTagRateNoHiggsPost", "all_ak8_1b", "topjets",
            //     TopJetId(VetoId<TopJet>(JetClosestGenPartId(25, ))), TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)))));
            // v_hists_after_sel.back().emplace_back(new TagEffHists<TopJet>(ctx, cat+"/MisTagRateNoHiggsPost", "all_ak8_2b", "topjets",
            //     TopJetId(VetoId<TopJet>(JetClosestGenPartId(25, ))), TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)))));
        
        ///////// MISTAG RATES FOR VARIOUS PROCESSES AS FUNCTION OF RECO VARIABLES

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateWtoAll", "ak8_1b", "topjets",
            TopJetId(JetClosestGenPartDaughterRangeId(24, 1, 4, 0.8, 0., true)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateWtoAll", "ak8_2b", "topjets",
            TopJetId(JetClosestGenPartDaughterRangeId(24, 1, 4, 0.8, 0., true)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateWtoC", "ak8_1b", "topjets",
            TopJetId(JetClosestGenPartId(24, 4, 0.8, 0., true)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateWtoC", "ak8_2b", "topjets",
            TopJetId(JetClosestGenPartId(24, 4, 0.8, 0., true)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateWtoLight", "ak8_1b", "topjets",
            TopJetId(JetClosestGenPartId(24, 2, 0.8, 0., true)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateWtoLight", "ak8_2b", "topjets",
            TopJetId(JetClosestGenPartId(24, 2, 0.8, 0., true)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateWtoAllNoTop", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8)), JetClosestGenPartDaughterRangeId(24, 1, 4, 0.8, 0., true))), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateWtoAllNoTop", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8)), JetClosestGenPartDaughterRangeId(24, 1, 4, 0.8, 0., true))), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateWtoCNoTop", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8)), JetClosestGenPartId(24, 4, 0.8, 0., true))), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateWtoCNoTop", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8)), JetClosestGenPartId(24, 4, 0.8, 0., true))), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateWtoLightNoTop", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8)), JetClosestGenPartId(24, 2, 0.8, 0., true))), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateWtoLightNoTop", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8)), JetClosestGenPartId(24, 2, 0.8, 0., true))), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateWtoAllNoHeavy", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(VetoId<TopJet>(JetClosestGenPartRangeId(5, 6, 0.8, 0.)), JetClosestGenPartDaughterRangeId(24, 1, 4, 0.8, 0., true))), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateWtoAllNoHeavy", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(VetoId<TopJet>(JetClosestGenPartRangeId(5, 6, 0.8, 0.)), JetClosestGenPartDaughterRangeId(24, 1, 4, 0.8, 0., true))), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
        
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateWtoCNoHeavy", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(VetoId<TopJet>(JetClosestGenPartRangeId(5, 6, 0.8, 0.)), JetClosestGenPartId(24, 4, 0.8, 0., true))), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateWtoCNoHeavy", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(VetoId<TopJet>(JetClosestGenPartRangeId(5, 6, 0.8, 0.)), JetClosestGenPartId(24, 4, 0.8, 0., true))), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateWtoLightNoHeavy", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(VetoId<TopJet>(JetClosestGenPartRangeId(5, 6, 0.8, 0.)), JetClosestGenPartId(24, 2, 0.8, 0., true))), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateWtoLightNoHeavy", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(VetoId<TopJet>(JetClosestGenPartRangeId(5, 6, 0.8, 0.)), JetClosestGenPartId(24, 2, 0.8, 0., true))), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateZtoBB", "ak8_1b", "topjets",
            TopJetId(JetClosestGenPartId(23, 5, 0.8, 0., true)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateZtoBB", "ak8_2b", "topjets",
            TopJetId(JetClosestGenPartId(23, 5, 0.8, 0., true)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateZtoOther", "ak8_1b", "topjets",
            TopJetId(JetClosestGenPartDaughterRangeId(23, 1, 4, 0.8, 0., true)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateZtoOther", "ak8_2b", "topjets",
            TopJetId(JetClosestGenPartDaughterRangeId(23, 1, 4, 0.8, 0., true)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));



        // top quark mistag rate

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateHadronicTopAll", "ak8_1b", "topjets",
            TopJetId(HadronicTopId(0.8, 0.)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateHadronicTopAll", "ak8_2b", "topjets",
            TopJetId(HadronicTopId(0.8, 0.)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateHadronicTopFullMerged", "ak8_1b", "topjets",
            TopJetId(HadronicTopId(0.8, 0., 3)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateHadronicTopFullMerged", "ak8_2b", "topjets",
            TopJetId(HadronicTopId(0.8, 0., 3)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateHadronicTopPartMergedTwo", "ak8_1b", "topjets",
            TopJetId(HadronicTopId(0.8, 0., 2)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateHadronicTopPartMergedTwo", "ak8_2b", "topjets",
            TopJetId(HadronicTopId(0.8, 0., 2)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateHadronicTopPartMergedTwoB", "ak8_1b", "topjets",
            TopJetId(HadronicTopId(0.8, 0., 2, true)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateHadronicTopPartMergedTwoB", "ak8_2b", "topjets",
            TopJetId(HadronicTopId(0.8, 0., 2, true)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateHadronicTopPartMergedOne", "ak8_1b", "topjets",
            TopJetId(HadronicTopId(0.8, 0., 1)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateHadronicTopPartMergedOne", "ak8_2b", "topjets",
            TopJetId(HadronicTopId(0.8, 0., 1)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateHadronicTopPartMergedOneB", "ak8_1b", "topjets",
            TopJetId(HadronicTopId(0.8, 0., 1, true)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateHadronicTopPartMergedOneB", "ak8_2b", "topjets",
            TopJetId(HadronicTopId(0.8, 0., 1, true)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));






        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateGluonNoTop", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8)), JetClosestGenPartId(21, 0, 0.8, 300.))), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateGluonNoTop", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8)), JetClosestGenPartId(21, 0, 0.8, 300.))), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateHeavyQuarkNoTop", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8)), JetClosestGenPartRangeId(4, 5, 0.8, 300.))), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateHeavyQuarkNoTop", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8)), JetClosestGenPartRangeId(4, 5, 0.8, 300.))), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateLightQuarkNoTop", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8)), JetClosestGenPartRangeId(1, 3, 0.8, 300.))), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateLightQuarkNoTop", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8)), JetClosestGenPartRangeId(1, 3, 0.8, 300.))), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateGluonToBBMerged", "ak8_1b", "topjets",
            TopJetId(GluonToBBId(0.8, 0., true)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateGluonToBBMerged", "ak8_2b", "topjets",
            TopJetId(GluonToBBId(0.8, 0., true)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateGluonToBBAll", "ak8_1b", "topjets",
            TopJetId(GluonToBBId(0.8)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/MistagRateGluonToBBAll", "ak8_2b", "topjets",
            TopJetId(GluonToBBId(0.8)), TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.)))));




        ///////// FRACTIONS OF PROCESSES IN TAGGED PARTICLES

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionNoPartInclMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(VetoId<TopJet>(JetClosestGenPartRangeId(1, 25, 0.8)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionNoPartInclMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(VetoId<TopJet>(JetClosestGenPartRangeId(1, 25, 0.8)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionNoPartHighPtMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(VetoId<TopJet>(JetClosestGenPartRangeId(1, 25, 0.8, 200.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionNoPartHighPtMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(VetoId<TopJet>(JetClosestGenPartRangeId(1, 25, 0.8, 200.)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionNoHadronicTopMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(VetoId<TopJet>(HadronicTopId(0.8)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionNoHadronicTopMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(VetoId<TopJet>(HadronicTopId(0.8)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionNoTopInclMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(VetoId<TopJet>(JetClosestGenPartId(6, 0, 0.8)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionNoTopInclMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(VetoId<TopJet>(JetClosestGenPartId(6, 0, 0.8)))));


        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionWtoAllMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(JetClosestGenPartDaughterRangeId(24, 1, 4, 0.8, 0.))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionWtoAllMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(JetClosestGenPartDaughterRangeId(24, 1, 4, 0.8, 0.))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionWtoAllNoTopMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8)), JetClosestGenPartDaughterRangeId(24, 1, 4, 0.8, 0.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionWtoAllNoTopMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8)), JetClosestGenPartDaughterRangeId(24, 1, 4, 0.8, 0.)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionWtoCMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(JetClosestGenPartDaughterRangeId(24, 3, 4, 0.8, 0.))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionWtoCMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(JetClosestGenPartDaughterRangeId(24, 3, 4, 0.8, 0.))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionWtoCNoTopMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8)), JetClosestGenPartDaughterRangeId(24, 3, 4, 0.8, 0.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionWtoCNoTopMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8)), JetClosestGenPartDaughterRangeId(24, 3, 4, 0.8, 0.)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionWtoLightMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(JetClosestGenPartDaughterRangeId(24, 1, 2, 0.8, 0.))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionWtoLightMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(JetClosestGenPartDaughterRangeId(24, 1, 2, 0.8, 0.))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionWtoLightNoTopMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8)), JetClosestGenPartDaughterRangeId(24, 1, 2, 0.8, 0.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionWtoLightNoTopMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8)), JetClosestGenPartDaughterRangeId(24, 1, 2, 0.8, 0.)))));

        // v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionWtoCMergedMistag", "ak8_1b", "topjets",
        //     TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(JetClosestGenPartId(24, 4, 0.8, 0., true))));
        // v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionWtoCMergedMistag", "ak8_2b", "topjets",
        //     TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(JetClosestGenPartId(24, 4, 0.8, 0., true))));

        // v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionWtoLightMergedMistag", "ak8_1b", "topjets",
        //     TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(JetClosestGenPartId(24, 2, 0.8, 0., true))));
        // v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionWtoLightMergedMistag", "ak8_2b", "topjets",
        //     TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(JetClosestGenPartId(24, 2, 0.8, 0., true))));

        // v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionWtoCNoTopMergedMistag", "ak8_1b", "topjets",
        //     TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8)), JetClosestGenPartId(24, 4, 0.8, 0., true)))));
        // v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionWtoCNoTopMergedMistag", "ak8_2b", "topjets",
        //     TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8)), JetClosestGenPartId(24, 4, 0.8, 0., true)))));

        // v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionZtoBBMistag", "ak8_1b", "topjets",
        //     TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(JetClosestGenPartId(23, 5, 0.8, 0., true))));
        // v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionZtoBBMistag", "ak8_2b", "topjets",
        //     TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(JetClosestGenPartId(23, 5, 0.8, 0., true))));

        // v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionHadronicZMistag", "ak8_1b", "topjets",
        //     TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(JetClosestGenPartDaughterRangeId(23, 1, 4, 0.8, 0., true))));
        // v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionHadronicZMistag", "ak8_2b", "topjets",
        //     TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(JetClosestGenPartDaughterRangeId(23, 1, 4, 0.8, 0., true))));



        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionHadronicTopAllMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(HadronicTopId(0.8, 0.))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionHadronicTopAllMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(HadronicTopId(0.8, 0.))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionHadronicTop1MergedMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(HadronicTopId(0.8, 0., 1))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionHadronicTop1MergedMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(HadronicTopId(0.8, 0., 1))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionHadronicTop2MergedMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(HadronicTopId(0.8, 0., 2))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionHadronicTop2MergedMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(HadronicTopId(0.8, 0., 2))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionHadronicTop3MergedMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(HadronicTopId(0.8, 0., 3))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionHadronicTop3MergedMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(HadronicTopId(0.8, 0., 3))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionLeptonicTopAllMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8)), JetClosestGenPartId(6, 0, 0.8)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionLeptonicTopAllMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8)), JetClosestGenPartId(6, 0, 0.8)))));




        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionHadronicTopExactly1MergedMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8, 0., 2)), HadronicTopId(0.8, 0., 1)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionHadronicTopExactly1MergedMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8, 0., 2)), HadronicTopId(0.8, 0., 1)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionHadronicTopExactly2MergedMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8, 0., 3)), HadronicTopId(0.8, 0., 2)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionHadronicTopExactly2MergedMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8, 0., 3)), HadronicTopId(0.8, 0., 2)))));


        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionHadronicTopExactly2MergedWithBMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8, 0., 3)), HadronicTopId(0.8, 0., 2, true)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionHadronicTopExactly2MergedWithBMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8, 0., 3)), HadronicTopId(0.8, 0., 2, true)))));






        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionGluonMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(JetClosestGenPartId(21, 0, 0.8, 300.))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionGluonMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(JetClosestGenPartId(21, 0, 0.8, 300.))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionGluonNoQuarkMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(AndId<TopJet>(VetoId<TopJet>(JetClosestGenPartRangeId(1, 5, 0.8)), JetClosestGenPartId(21, 0, 0.8, 300.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionGluonNoQuarkMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(AndId<TopJet>(VetoId<TopJet>(JetClosestGenPartRangeId(1, 5, 0.8)), JetClosestGenPartId(21, 0, 0.8, 300.)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionHeavyQuarkMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(JetClosestGenPartRangeId(4, 5, 0.8, 300.))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionHeavyQuarkMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(JetClosestGenPartRangeId(4, 5, 0.8, 300.))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionLightQuarkMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(JetClosestGenPartRangeId(1, 3, 0.8, 300.))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionLightQuarkMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(JetClosestGenPartRangeId(1, 3, 0.8, 300.))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionHeavyQuarkNoGluonMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(AndId<TopJet>(VetoId<TopJet>(JetClosestGenPartId(21, 0, 0.8)), JetClosestGenPartRangeId(4, 5, 0.8, 300.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionHeavyQuarkNoGluonMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(AndId<TopJet>(VetoId<TopJet>(JetClosestGenPartId(21, 0, 0.8)), JetClosestGenPartRangeId(4, 5, 0.8, 300.)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionLightQuarkNoGluonMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(AndId<TopJet>(VetoId<TopJet>(JetClosestGenPartId(21, 0, 0.8)), JetClosestGenPartRangeId(1, 3, 0.8, 300.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionLightQuarkNoGluonMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(AndId<TopJet>(VetoId<TopJet>(JetClosestGenPartId(21, 0, 0.8)), JetClosestGenPartRangeId(1, 3, 0.8, 300.)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionHeavyQuarkNoTopMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8)), JetClosestGenPartRangeId(4, 5, 0.8, 300.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionHeavyQuarkNoTopMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8)), JetClosestGenPartRangeId(4, 5, 0.8, 300.)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionLightQuarkNoTopMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8)), JetClosestGenPartRangeId(1, 3, 0.8, 300.)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionLightQuarkNoTopMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(AndId<TopJet>(VetoId<TopJet>(HadronicTopId(0.8)), JetClosestGenPartRangeId(1, 3, 0.8, 300.)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionGluonToBBMergedMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(GluonToBBId(0.8, 0., true))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionGluonToBBMergedMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(GluonToBBId(0.8, 0., true))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionGluonToBBAllMistag", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(GluonToBBId(0.8))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/FractionGluonToBBAllMistag", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(GluonToBBId(0.8))));        


        ///////// EFFICIENCIES OF HIGGS TAGGING CUTS
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/NoGenPtCutEfficiencyPre", "ak8_1b", "topjets",
            TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM))), TopJetId(PtEtaCut(300., 3.))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/NoGenPtCutEfficiencyPre", "ak8_2b", "topjets",
            TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM))), TopJetId(PtEtaCut(300., 3.))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/NoGenMassCutEfficiencyPre", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(0., 999999., CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/NoGenMassCutEfficiencyPre", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(0., 999999., CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)), PtEtaCut(300., 3.))), TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)))));

        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/NoGenSubjetBtagCutEfficiencyPre", "ak8_1b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS), PtEtaCut(300., 3.))), TopJetId(HiggsFlexBTag(0., 999999., CSVBTag(CSVBTag::WP_MEDIUM)))));
        v_hists.back().emplace_back(new AK8TagEffHists(ctx, cat+"/NoGenSubjetBtagCutEfficiencyPre", "ak8_2b", "topjets",
            TopJetId(AndId<TopJet>(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS), PtEtaCut(300., 3.))), TopJetId(HiggsFlexBTag(0., 999999., CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)))));
    }


}


bool TpTpHiggsTagEfficiency::process(Event & event) {

    // std::cout << "NEW EVENT 0" << std::endl;

    common_module->process(event);

    // std::cout << "NEW EVENT 1" << std::endl;

    for (auto & mod : pre_modules) {
        mod->process(event);
    }

    // std::cout << "NEW EVENT 2" << std::endl;

    assert(event.topjets);
    sort_by_pt(*event.topjets);

    for (auto & mod : common_modules) {
        mod->process(event);
    }

    // std::cout << "NEW EVENT 3" << std::endl;

    for (auto & mod : other_modules) {
        mod->process(event);
    }

    // std::cout << "NEW EVENT 4" << std::endl;

    sel_modules_passed.clear();

    // int base_el_ind = -1;
    // for (unsigned i = 0; i < categories.size(); ++i) {
    //     if (categories[i] == "El45_Baseline")
    //         base_el_ind = i;
    // }

    // index 0 corresponds to combined
    for (unsigned i = 0; i < sel_modules.size(); ++i) {
    
        bool all_accepted = sel_modules[i]->process(event);
        sel_modules_passed.push_back(all_accepted);

    }

    // std::cout << "NEW EVENT 5" << std::endl;

    // btag_sf_cr->process(event);

    // all hists
    for (auto & hist_vec : v_hists) {
        for (auto & hist : hist_vec) {
            hist->fill(event);
        }
    }

    // std::cout << "NEW EVENT 6" << std::endl;

    // if (sel_modules_passed[2] || sel_modules_passed[3]) {
    //     btag_sf_sr->process(event);
        // event.set(use_sr_sf_hndl, 1);
    // }
    // else {
    // }
    // event.set(use_sr_sf_hndl, 0);
    
    event.set(weight_hndl, event.weight);


    for (unsigned i = 0; i < sel_modules.size(); ++i) {

        bool all_accepted = sel_modules_passed[i];
        if (all_accepted) {
            for (auto & hist : v_hists_after_sel[i]) {
                hist->fill(event);
            }
        }

    }

    // std::cout << "NEW EVENT 7" << std::endl;

    // if (base_el_ind >= 0 && sel_modules_passed[base_el_ind]) {
    //     ele_trg_sf->process(event);
    // }
    // else
    //     ele_trg_nosf->process(event);



    // std::cout << "NEW EVENT 8" << std::endl;

    // if (version.find("TpTp") == string::npos && type == "MC")
    //     event.weight *= event.get(jetpt_weight_hndl);

    // for (unsigned i = 0; i < sel_modules.size(); ++i) {
    
    //     bool all_accepted = sel_modules_passed[i];
    //     if (all_accepted) {

    //         for (auto & hist : v_reweighted_hists_after_sel[i]) {
    //             hist->fill(event);
    //         }
    //     }

    // }



    // run all modules
    // for (bool pass_sel : sel_modules_passed) {
    //     if (pass_sel) return true;
    // }

    return false;
}

UHH2_REGISTER_ANALYSIS_MODULE(TpTpHiggsTagEfficiency)
