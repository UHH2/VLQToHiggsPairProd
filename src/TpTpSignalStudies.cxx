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
#include "UHH2/common/include/HandleSelection.h"


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

class TpTpSignalStudies: public TpTpAnalysisModule {
public:

    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_BASELINE_SEL {
        shared_ptr<SelectionItem>(new SelDatI("gendecay_accept", "GenDecay Accept", 2, -.5, 1.5, 1)),
        // shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 10, -.5, 9.5, 2)),
        };

    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_FULL_SEL {
        shared_ptr<SelectionItem>(new SelDatI("gendecay_accept", "GenDecay Accept", 2, -.5, 1.5, 1)),
        shared_ptr<SelectionItem>(new SelDatD("ST", "ST", 65, 0, 6500, 800)),
        shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 10, -.5, 9.5, 2)),
        shared_ptr<SelectionItem>(new SelDatI("n_ak4", "N(Ak4 Jets)", 20, -.5, 19.5, 3)),
        shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak8_jet", "Pt leading Ak8 Jet", 100, 0., 2000., 300.)),
        };

    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_EL45_BASE_SEL {
        shared_ptr<SelectionItem>(new SelDatI("has_gen_electron", "Gen Electrons", 2, -.5, 1.5, 1)),
        // shared_ptr<SelectionItem>(new SelDatI("n_ak4", "N(Ak4 Jets)", 20, -.5, 19.5, 2)),
        };

    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_Mu45_BASE_SEL {
        shared_ptr<SelectionItem>(new SelDatI("has_gen_muon", "Gen Muons", 2, -.5, 1.5, 1)),
        };

    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_EL45_NOTRG_SEL {
        shared_ptr<SelectionItem>(new SelDatF("primary_electron_pt", "Primary Lepton p_T", 100, 0., 1200., 50.)),
        shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 100, 0., 2000., 250.)),
        shared_ptr<SelectionItem>(new SelDatF("pt_subld_ak4_jet", "Pt subleading Ak4 Jet", 40, 0., 1600., 70.)),
        };

    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_Mu45_NOTRG_SEL {
        shared_ptr<SelectionItem>(new SelDatF("primary_muon_pt", "Primary Lepton p_T", 100, 0., 1200., 47.)),
        };

    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_Mu20_NOTRG_ISO_SEL {
        shared_ptr<SelectionItem>(new SelDatF("primary_muon_pt_iso", "Primary Lepton p_T", 100, 0., 1200., 40.)),
        };

    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_EL27_NOTRG_ISO_SEL {
        shared_ptr<SelectionItem>(new SelDatF("primary_electron_pt_iso", "Primary Lepton p_T", 100, 0., 1200., 40.)),
        };


    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_EL105_NOTRG_SEL {
        shared_ptr<SelectionItem>(new SelDatF("primary_electron_pt", "Primary Lepton p_T", 100, 0., 1200., 115.)),
        };

    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_EL45_TRG_SEL {
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_el45", "Trigger Accept", 2, -.5, 1.5, 1)),
        // shared_ptr<SelectionItem>(new SelDatI("trigger_accept_mu45", "Trigger Accept Mu45", 2, -.5, 1.5, 0, 0)),
        };

    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_Mu45_TRG_SEL {
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_mu45", "Trigger Accept", 2, -.5, 1.5, 1)),
        };

    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_EL27_TRG_ISO_SEL {
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_isoEl27", "Trigger Accept", 2, -.5, 1.5, 1)),
        // shared_ptr<SelectionItem>(new SelDatI("trigger_accept_mu45", "Trigger Accept Mu45", 2, -.5, 1.5, 0, 0)),
        };

    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_Mu20_TRG_ISO_SEL {
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_isoMu20", "Trigger Accept", 2, -.5, 1.5, 1)),
        };

    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_EL105_TRG_SEL {
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_el105", "Trigger Accept", 2, -.5, 1.5, 1)),
        // shared_ptr<SelectionItem>(new SelDatI("trigger_accept_mu45", "Trigger Accept Mu45", 2, -.5, 1.5, 0, 0)),
        };


    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_ALL {
        shared_ptr<SelectionItem>(new SelDatI("gendecay_accept", "GenDecay Accept", 2, -.5, 1.5)),
        shared_ptr<SelectionItem>(new SelDatD("ST", "ST", 65, 0, 6500)),
        shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 10, -.5, 9.5)),
        shared_ptr<SelectionItem>(new SelDatI("n_ak4", "N(Ak4 Jets)", 20, -.5, 19.5)),
        shared_ptr<SelectionItem>(new SelDatI("n_muons", "N(Muons)", 10, -.5, 9.5)),
        shared_ptr<SelectionItem>(new SelDatI("n_electrons", "N(Electrons)", 10, -.5, 9.5)),
        shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak8_jet", "Pt leading Ak8 Jet", 100, 0., 2000.)),
        shared_ptr<SelectionItem>(new SelDatF("primary_muon_pt", "Primary Lepton p_T", 100, 0., 1200.)),
        shared_ptr<SelectionItem>(new SelDatF("primary_electron_pt", "Primary Lepton p_T", 100, 0., 1200.)),
        shared_ptr<SelectionItem>(new SelDatF("primary_muon_pt_iso", "Primary Lepton p_T", 100, 0., 1200., 40.)),
        shared_ptr<SelectionItem>(new SelDatF("primary_electron_pt_iso", "Primary Lepton p_T", 100, 0., 1200., 40.)),
        shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 100, 0., 2000.)),
        shared_ptr<SelectionItem>(new SelDatF("pt_subld_ak4_jet", "Pt subleading Ak4 Jet", 40, 0., 1600.)),
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_el45", "Trigger Accept", 2, -.5, 1.5)),
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_mu45", "Trigger Accept", 2, -.5, 1.5)),
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_isoEl27", "Trigger Accept", 2, -.5, 1.5)),
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_isoMu20", "Trigger Accept", 2, -.5, 1.5)),
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_el105", "Trigger Accept", 2, -.5, 1.5)),
        shared_ptr<SelectionItem>(new SelDatI("has_gen_electron", "Gen Electrons", 2, -.5, 1.5, 1)),
        shared_ptr<SelectionItem>(new SelDatI("has_gen_muon", "Gen Muons", 2, -.5, 1.5, 1)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 100, 0., 2000.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_subld_ak4_jet", "Pt subleading Ak4 Jet", 40, 0., 1600.)),
        // shared_ptr<SelectionItem>(new SelDatI("trigger_accept_el45", "Trigger Accept El45", 2, -.5, 1.5)),
        // shared_ptr<SelectionItem>(new SelDatF("primary_electron_pt", "Primary Lepton p_T", 100, 0., 1200.)),
        // shared_ptr<SelectionItem>(new SelDatI("trigger_accept_lep_comb", "Trigger Accept", 2, -.5, 1.5)),
        // shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt", "Primary Lepton p_T", 100, 0., 1200.)),
        // shared_ptr<SelectionItem>(new SelDatF("primary_electron_pt_tight", "Primary Lepton p_T", 100, 0., 1200.)),
        // shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 10, -.5, 9.5, 2)),
        };

    explicit TpTpSignalStudies(Context & ctx);
    virtual bool process(Event & event) override;

private:
    unique_ptr<AnalysisModule> common_module;
    // unique_ptr<NParticleMultiHistProducerHelper<TopJet>> ak8jet_hists/*, ca15jet_hists*/;
    // unique_ptr<AnalysisModule> btag_sf_sr, btag_sf_cr, ele_trg_sf, ele_trg_nosf;
    Event::Handle<bool> h_base_sel;
    Event::Handle<double> weight_hndl;
    Event::Handle<float> weight_ele_hndl;
    // Event::Handle<float> jetpt_weight_hndl;
    // Event::Handle<int> use_sr_sf_hndl;
    // vector<vector<unique_ptr<Hists>>> v_reweighted_hists_after_sel;
    // vector<unique_ptr<Hists>> v_lep_combined_hists;
    vector<string> categories;
    shared_ptr<SelItemsHelper> sel_helpers_base, sel_helpers_full, sel_helpers_el_base, sel_helpers_mu_base,
        sel_helpers_el_lep, sel_helpers_mu_lep, sel_helpers_el_trg, sel_helpers_mu_trg, sel_helpers_all,
        sel_helpers_el_iso_lep, sel_helpers_mu_iso_lep, sel_helpers_el_105_lep, sel_helpers_el_iso_trg,
        sel_helpers_mu_iso_trg, sel_helpers_el_105_trg;
    shared_ptr<SelectionProducer> sel_modules_base, sel_modules_full, sel_modules_el_base, sel_modules_mu_base,
        sel_modules_el_lep, sel_modules_mu_lep, sel_modules_el_trg, sel_modules_mu_trg, sel_modules_all,
        sel_modules_el_iso_lep, sel_modules_mu_iso_lep, sel_modules_el_105_lep, sel_modules_el_iso_trg,
        sel_modules_mu_iso_trg, sel_modules_el_105_trg;

};



TpTpSignalStudies::TpTpSignalStudies(Context & ctx) : TpTpAnalysisModule(ctx) {

    auto data_dir_path = ctx.get("data_dir_path");
    CommonModules* commonObjectCleaning = new CommonModules();
    commonObjectCleaning->set_jet_id(AndId<Jet>(JetPFID(JetPFID::WP_LOOSE), PtEtaCut(30.0,2.4)));
    commonObjectCleaning->set_electron_id(AndId<Electron>(ElectronID_Spring15_25ns_medium_noIso,PtEtaCut(10., 2.4)));
    commonObjectCleaning->set_muon_id(AndId<Muon>(MuonIDMedium(),PtEtaCut(10., 2.1)));
    commonObjectCleaning->disable_jersmear();
    commonObjectCleaning->disable_jec();
    commonObjectCleaning->disable_mcpileupreweight();
    commonObjectCleaning->switch_jetlepcleaner(true);
    commonObjectCleaning->switch_jetPtSorter(true);
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
    else if (version.find("lep_T") != string::npos) {
        other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
            GenParticleId(
                AndId<GenParticle>(
                    GenParticlePdgIdId({-13, -11, 11, 13}),
                    AndId<GenParticle>(GenParticleMotherId(0, 6), GenParticleMotherId(0, 25), GenParticleMotherId(0, 23))
                    )
            )));
    }
    else if (version.find("lep_top") != string::npos) {
        other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
            GenParticleId(
                AndId<GenParticle>(
                    GenParticlePdgIdId({-13, -11, 11, 13}),
                    GenParticleMotherId(6)
                    )
            )
            ));
    }
    else if (version.find("lep_other") != string::npos) {
        other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
            GenParticleId(
                AndId<GenParticle>(
                    GenParticlePdgIdId({-13, -11, 11, 13}),
                    OrId<GenParticle>(GenParticleMotherId(25), GenParticleMotherId(23))
                    )
            )
            ));
    }

    else {
        other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
            GenParticleId(TrueId<GenParticle>::is_true), GenParticleId(TrueId<GenParticle>::is_true)));
    }

    other_modules.emplace_back(new TrueFalseProducer(ctx, "chan_accept", false));

    other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "has_gen_electron",
            GenParticleId(
                    GenParticlePdgIdId({-11, 11})
            )
            ));
    other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "has_gen_muon",
            GenParticleId(
                    GenParticlePdgIdId({-13, 13})
            )
            ));
    // categories = split(ctx.get("category", ""));

    // for (auto const & fs : final_states) {
    // for (auto const & cat : categories) {


        // SEL_ITEMS_FULL_SEL.push_back(SEL_ITEMS_BASELINE_SEL);


        // if (split(cat, "_")[0] == "Mu45") {
        //     for (auto const & sel_item : SEL_ITEMS_Mu45_SEL)
        //         SEL_ITEMS_FULL_SEL.back().push_back(sel_item);
        // }
        // else if (split(cat, "_")[0] == "El45") {
        //     for (auto const & sel_item : SEL_ITEMS_EL45_SEL)
        //         SEL_ITEMS_FULL_SEL.back().push_back(sel_item);
        // }
        
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

    // vector<shared_ptr<SelectionItem>> sel_items_only_trg_mu = SEL_ITEMS_BASELINE_SEL;
    // vector<shared_ptr<SelectionItem>> sel_items_only_trg_el = SEL_ITEMS_BASELINE_SEL;
    // vector<shared_ptr<SelectionItem>> sel_items_full_mu = SEL_ITEMS_FULL_SEL;
    // vector<shared_ptr<SelectionItem>> sel_items_full_el = SEL_ITEMS_FULL_SEL;
    // sel_items_only_trg_mu.insert(sel_items_only_trg_mu.end(), SEL_ITEMS_EL45_NOTRG_SEL.begin(), SEL_ITEMS_EL45_NOTRG_SEL.end())
    // sel_items_only_trg_el.insert(sel_items_only_trg_el.end(), SEL_ITEMS_Mu45_NOTRG_SEL.begin(), SEL_ITEMS_Mu45_NOTRG_SEL.end())
    // sel_items_full_mu.insert(sel_items_full_mu.end(), SEL_ITEMS_EL45_TRG_SEL.begin(), SEL_ITEMS_EL45_TRG_SEL.end())
    // sel_items_full_el.insert(sel_items_full_el.end(), SEL_ITEMS_Mu45_TRG_SEL.begin(), SEL_ITEMS_Mu45_TRG_SEL.end())

    sel_helpers_base.reset(new SelItemsHelper(SEL_ITEMS_BASELINE_SEL, ctx, vector<string>(), "sel_accept_base", "sel_all_accepted_base"));
    sel_helpers_full.reset(new SelItemsHelper(SEL_ITEMS_FULL_SEL, ctx, vector<string>(), "sel_accept_full", "sel_all_accepted_full"));
    sel_helpers_el_base.reset(new SelItemsHelper(SEL_ITEMS_EL45_BASE_SEL, ctx, vector<string>(), "sel_accept_el_base", "sel_all_accepted_el_base"));
    sel_helpers_mu_base.reset(new SelItemsHelper(SEL_ITEMS_Mu45_BASE_SEL, ctx, vector<string>(), "sel_accept_mu_base", "sel_all_accepted_mu_base"));

    sel_helpers_el_lep.reset(new SelItemsHelper(SEL_ITEMS_EL45_NOTRG_SEL, ctx, vector<string>(), "sel_accept_el_lep", "sel_all_accepted_el_lep"));
    sel_helpers_mu_lep.reset(new SelItemsHelper(SEL_ITEMS_Mu45_NOTRG_SEL, ctx, vector<string>(), "sel_accept_mu_lep", "sel_all_accepted_mu_lep"));
    sel_helpers_el_iso_lep.reset(new SelItemsHelper(SEL_ITEMS_EL27_NOTRG_ISO_SEL, ctx, vector<string>(), "sel_accept_el_iso_lep", "sel_all_accepted_el_iso_lep"));
    sel_helpers_mu_iso_lep.reset(new SelItemsHelper(SEL_ITEMS_Mu20_NOTRG_ISO_SEL, ctx, vector<string>(), "sel_accept_mu_iso_lep", "sel_all_accepted_mu_iso_lep"));
    sel_helpers_el_105_lep.reset(new SelItemsHelper(SEL_ITEMS_EL105_NOTRG_SEL, ctx, vector<string>(), "sel_accept_el_105_lep", "sel_all_accepted_el_105_lep"));

    sel_helpers_el_trg.reset(new SelItemsHelper(SEL_ITEMS_EL45_TRG_SEL, ctx, vector<string>(), "sel_accept_el_trg", "sel_all_accepted_el_trg"));
    sel_helpers_mu_trg.reset(new SelItemsHelper(SEL_ITEMS_Mu45_TRG_SEL, ctx, vector<string>(), "sel_accept_mu_trg", "sel_all_accepted_mu_trg"));
    sel_helpers_el_iso_trg.reset(new SelItemsHelper(SEL_ITEMS_EL27_TRG_ISO_SEL, ctx, vector<string>(), "sel_accept_el_iso_trg", "sel_all_accepted_el_iso_trg"));
    sel_helpers_mu_iso_trg.reset(new SelItemsHelper(SEL_ITEMS_Mu20_TRG_ISO_SEL, ctx, vector<string>(), "sel_accept_mu_iso_trg", "sel_all_accepted_mu_iso_trg"));
    sel_helpers_el_105_trg.reset(new SelItemsHelper(SEL_ITEMS_EL105_TRG_SEL, ctx, vector<string>(), "sel_accept_el_105_trg", "sel_all_accepted_el_105_trg"));

    sel_helpers_all.reset(new SelItemsHelper(SEL_ITEMS_ALL, ctx, vector<string>(), "sel_accept_all", "sel_all_accepted_all"));

    // sel_helpers_base->declare_items_for_output();
    // sel_helpers_full->declare_items_for_output();
    // sel_helpers_el_lep->declare_items_for_output();
    // sel_helpers_mu_lep->declare_items_for_output();
    // sel_helpers_el_trg->declare_items_for_output();
    // sel_helpers_mu_trg->declare_items_for_output();

    sel_modules_base.reset(new SelectionProducer(ctx, *sel_helpers_base));
    sel_modules_full.reset(new SelectionProducer(ctx, *sel_helpers_full));
    sel_modules_el_base.reset(new SelectionProducer(ctx, *sel_helpers_el_base));
    sel_modules_mu_base.reset(new SelectionProducer(ctx, *sel_helpers_mu_base));

    sel_modules_el_lep.reset(new SelectionProducer(ctx, *sel_helpers_el_lep));
    sel_modules_mu_lep.reset(new SelectionProducer(ctx, *sel_helpers_mu_lep));
    sel_modules_el_iso_lep.reset(new SelectionProducer(ctx, *sel_helpers_el_iso_lep));
    sel_modules_mu_iso_lep.reset(new SelectionProducer(ctx, *sel_helpers_mu_iso_lep));
    sel_modules_el_105_lep.reset(new SelectionProducer(ctx, *sel_helpers_el_105_lep));

    sel_modules_el_trg.reset(new SelectionProducer(ctx, *sel_helpers_el_trg));
    sel_modules_mu_trg.reset(new SelectionProducer(ctx, *sel_helpers_mu_trg));
    sel_modules_el_iso_trg.reset(new SelectionProducer(ctx, *sel_helpers_el_iso_trg));
    sel_modules_mu_iso_trg.reset(new SelectionProducer(ctx, *sel_helpers_mu_iso_trg));
    sel_modules_el_105_trg.reset(new SelectionProducer(ctx, *sel_helpers_el_105_trg));
    // sel_modules_all.reset(new SelectionProducer(ctx, *sel_helpers_all));

    
    other_modules.emplace_back(new TwoDCutProducer(ctx, "PrimaryMuon", "TwoDcut_Dr_mu", "TwoDcut_Dpt_mu"));
    other_modules.emplace_back(new TwoDCutProducer(ctx, "PrimaryElectron", "TwoDcut_Dr_el", "TwoDcut_Dpt_el"));
    other_modules.emplace_back(new TwoDCutProducer(ctx, "PrimaryMuonIso", "TwoDcut_Dr_mu_iso", "TwoDcut_Dpt_mu_iso"));
    other_modules.emplace_back(new TwoDCutProducer(ctx, "PrimaryElectronIso", "TwoDcut_Dr_el_iso", "TwoDcut_Dpt_el_iso"));
    sel_modules_mu_lep->push_back_selection(new TwoDCutSel(ctx, 0.4, 40.0, "TwoDcut_Dr_mu", "TwoDcut_Dpt_mu"));
    sel_modules_el_lep->push_back_selection(new TwoDCutSel(ctx, 0.4, 40.0, "TwoDcut_Dr_el", "TwoDcut_Dpt_el"));



    // vector<string> item_names;
    // for (auto const & seli : SEL_ITEMS_FULL_SEL.back()) 
    //     item_names.push_back(seli->name());

    // sel_helpers.emplace_back(new SelItemsHelper(SEL_ITEMS_FULL_SEL.back(), ctx, item_names, "sel_accept_"+cat, "sel_all_accepted_"+cat));
    // sel_helper.declare_items_for_output();
    // sel_modules.emplace_back(new SelectionProducer(ctx, *sel_helpers.back()));

    // if (split(cat, "-")[0] == "HiggsTag0Med") {
    // sel_helpers.back()->declare_items_for_output();
    // }
    // 3. Set up Hists classes:

    // TODO: set up and fill other histogram classes, e.g. your own HistCollector stuff

    v_hists.emplace_back(vector<shared_ptr<Hists>>());
    v_hists_after_sel.emplace_back(vector<shared_ptr<Hists>>());
    // v_reweighted_hists_after_sel.emplace_back(vector<shared_ptr<Hists>>());
    // v_genhist_2h_after_sel.emplace_back(vector<shared_ptr<Hists>>());
    // v_genhist_1h_after_sel.emplace_back(vector<shared_ptr<Hists>>());


    // auto nm1_hists = new Nm1SelHists(ctx, "Nm1Selection", *sel_helpers.back());
    // auto cf_hists = new VLQ2HTCutflow(ctx, "Cutflow", *sel_helpers.back());

    

    // v_hists.back().emplace_back(nm1_hists);
    // v_hists.back().emplace_back(cf_hists);
    // sel_helpers.back()->fill_hists_vector(v_hists.back(), "NoSelection");
    // sel_helpers.back()->fill_hists_vector(v_hists_after_sel.back(), "PostSelection");

    Selection* base_selection = new HandleSelection<bool>(ctx, "sel_all_accepted_base", 1);
    Selection* full_selection = new HandleSelection<bool>(ctx, "sel_all_accepted_full", 1);
    Selection* el_base_selection = new HandleSelection<bool>(ctx, "sel_all_accepted_el_base", 1);
    Selection* mu_base_selection = new HandleSelection<bool>(ctx, "sel_all_accepted_mu_base", 1);

    Selection* el_lep_selection = new HandleSelection<bool>(ctx, "sel_all_accepted_el_lep", 1);
    Selection* mu_lep_selection = new HandleSelection<bool>(ctx, "sel_all_accepted_mu_lep", 1);
    Selection* el_iso_lep_selection = new HandleSelection<bool>(ctx, "sel_all_accepted_el_iso_lep", 1);
    Selection* mu_iso_lep_selection = new HandleSelection<bool>(ctx, "sel_all_accepted_mu_iso_lep", 1);
    Selection* el_105_lep_selection = new HandleSelection<bool>(ctx, "sel_all_accepted_el_105_lep", 1);

    Selection* el_trg_selection = new HandleSelection<bool>(ctx, "sel_all_accepted_el_trg", 1);
    Selection* mu_trg_selection = new HandleSelection<bool>(ctx, "sel_all_accepted_mu_trg", 1);
    Selection* el_iso_trg_selection = new HandleSelection<bool>(ctx, "sel_all_accepted_el_iso_trg", 1);
    Selection* mu_iso_trg_selection = new HandleSelection<bool>(ctx, "sel_all_accepted_mu_iso_trg", 1);
    Selection* el_105_trg_selection = new HandleSelection<bool>(ctx, "sel_all_accepted_el_105_trg", 1);

    Selection* base_el_selection = new VectorAndSelection({base_selection, el_base_selection});
    Selection* base_mu_selection = new VectorAndSelection({base_selection, mu_base_selection});
    Selection* full_el_selection = new VectorAndSelection({full_selection, el_base_selection});
    Selection* full_mu_selection = new VectorAndSelection({full_selection, mu_base_selection});

    Selection* comb_el_selection = new VectorAndSelection({el_lep_selection, el_trg_selection});
    Selection* comb_mu_selection = new VectorAndSelection({mu_lep_selection, mu_trg_selection});
    Selection* comb_el_iso_selection = new VectorAndSelection({el_iso_lep_selection, el_iso_trg_selection});
    Selection* comb_mu_iso_selection = new VectorAndSelection({mu_iso_lep_selection, mu_iso_trg_selection});
    Selection* comb_el_105_selection = new VectorAndSelection({el_105_lep_selection, el_105_trg_selection});
    // shared_ptr<Selection> full_el_selection(new VectorAndSelection(vector<Selection*>(base_selection, el_lep_selection, full_selection)));
    // shared_ptr<Selection> full_mu_selection(new VectorAndSelection(vector<Selection*>(base_selection, mu_lep_selection, full_selection)));

    //////////////////////////////////
    ///////// BASE SELECTIONS ////////
    //////////////////////////////////

    SelEffHists<float> * muon_pt_base = new SelEffHists<float>(ctx, "NoSelection/BaseSelection", "primary_muon_pt", "muon_pt_base", base_mu_selection, mu_trg_selection, 100, 0., 1200., 47.);
    sel_helpers_all->fill_hists_vector(muon_pt_base->get_add_hists_den(), "NoSelection/BaseSelection/MuonPtFullTot");
    sel_helpers_all->fill_hists_vector(muon_pt_base->get_add_hists_num(), "NoSelection/BaseSelection/MuonPtFullCut");
    muon_pt_base->get_add_hists_den().emplace_back(new TwoDCutHist(ctx, "NoSelection/BaseSelection/MuonPtFullTot", "TwoDcut_Dr_mu", "TwoDcut_Dpt_mu", "twod_cut_hist"));
    muon_pt_base->get_add_hists_num().emplace_back(new TwoDCutHist(ctx, "NoSelection/BaseSelection/MuonPtFullCut", "TwoDcut_Dr_mu", "TwoDcut_Dpt_mu", "twod_cut_hist"));
    v_hists.back().emplace_back(muon_pt_base);

    SelEffHists<float> * electron_pt_base = new SelEffHists<float>(ctx, "NoSelection/BaseSelection", "primary_electron_pt", "electron_pt_base", base_el_selection, el_trg_selection, 100, 0., 1200., 50.);
    sel_helpers_all->fill_hists_vector(electron_pt_base->get_add_hists_den(), "NoSelection/BaseSelection/ElectronPtFullTot");
    sel_helpers_all->fill_hists_vector(electron_pt_base->get_add_hists_num(), "NoSelection/BaseSelection/ElectronPtFullCut");
    electron_pt_base->get_add_hists_den().emplace_back(new TwoDCutHist(ctx, "NoSelection/BaseSelection/ElectronPtFullTot", "TwoDcut_Dr_el", "TwoDcut_Dpt_el", "twod_cut_hist"));
    electron_pt_base->get_add_hists_num().emplace_back(new TwoDCutHist(ctx, "NoSelection/BaseSelection/ElectronPtFullCut", "TwoDcut_Dr_el", "TwoDcut_Dpt_el", "twod_cut_hist"));
    v_hists.back().emplace_back(electron_pt_base);

    //////////////////////////////////
    ///////// FULL SELECTIONS ////////
    //////////////////////////////////

    SelEffHists<float> * muon_pt_full = new SelEffHists<float>(ctx, "NoSelection/FullSelection", "primary_muon_pt", "muon_pt_full", full_mu_selection, comb_mu_selection, 100, 0., 1200., 1.);
    sel_helpers_all->fill_hists_vector(muon_pt_full->get_add_hists_den(), "NoSelection/FullSelection/MuonPtFullTot");
    sel_helpers_all->fill_hists_vector(muon_pt_full->get_add_hists_num(), "NoSelection/FullSelection/MuonPtFullCut");
    muon_pt_full->get_add_hists_den().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelection/MuonPtFullTot", "TwoDcut_Dr_mu", "TwoDcut_Dpt_mu", "twod_cut_hist"));
    muon_pt_full->get_add_hists_num().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelection/MuonPtFullCut", "TwoDcut_Dr_mu", "TwoDcut_Dpt_mu", "twod_cut_hist"));
    v_hists.back().emplace_back(muon_pt_full);

    SelEffHists<float> * electron_pt_full = new SelEffHists<float>(ctx, "NoSelection/FullSelection", "primary_electron_pt", "electron_pt_full", full_el_selection, comb_el_selection, 100, 0., 1200., 1.);
    sel_helpers_all->fill_hists_vector(electron_pt_full->get_add_hists_den(), "NoSelection/FullSelection/ElectronPtFullTot");
    sel_helpers_all->fill_hists_vector(electron_pt_full->get_add_hists_num(), "NoSelection/FullSelection/ElectronPtFullCut");
    electron_pt_full->get_add_hists_den().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelection/ElectronPtFullTot", "TwoDcut_Dr_el", "TwoDcut_Dpt_el", "twod_cut_hist"));
    electron_pt_full->get_add_hists_num().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelection/ElectronPtFullCut", "TwoDcut_Dr_el", "TwoDcut_Dpt_el", "twod_cut_hist"));
    v_hists.back().emplace_back(electron_pt_full);

    SelEffHists<float> * muon_pt_iso_full = new SelEffHists<float>(ctx, "NoSelection/FullSelection", "primary_muon_pt", "muon_pt_iso_full", full_mu_selection, comb_mu_iso_selection, 100, 0., 1200., 1.);
    sel_helpers_all->fill_hists_vector(muon_pt_iso_full->get_add_hists_den(), "NoSelection/FullSelection/MuonPtIsoFullTot");
    sel_helpers_all->fill_hists_vector(muon_pt_iso_full->get_add_hists_num(), "NoSelection/FullSelection/MuonPtIsoFullCut");
    muon_pt_iso_full->get_add_hists_den().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelection/MuonPtIsoFullTot", "TwoDcut_Dr_mu_iso", "TwoDcut_Dpt_mu_iso", "twod_cut_hist"));
    muon_pt_iso_full->get_add_hists_num().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelection/MuonPtIsoFullCut", "TwoDcut_Dr_mu_iso", "TwoDcut_Dpt_mu_iso", "twod_cut_hist"));
    v_hists.back().emplace_back(muon_pt_iso_full);

    SelEffHists<float> * electron_pt_iso_full = new SelEffHists<float>(ctx, "NoSelection/FullSelection", "primary_electron_pt", "electron_pt_iso_full", full_el_selection, comb_el_iso_selection, 100, 0., 1200., 1.);
    sel_helpers_all->fill_hists_vector(electron_pt_iso_full->get_add_hists_den(), "NoSelection/FullSelection/ElectronPtIsoFullTot");
    sel_helpers_all->fill_hists_vector(electron_pt_iso_full->get_add_hists_num(), "NoSelection/FullSelection/ElectronPtIsoFullCut");
    electron_pt_iso_full->get_add_hists_den().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelection/ElectronPtIsoFullTot", "TwoDcut_Dr_el_iso", "TwoDcut_Dpt_el_iso", "twod_cut_hist"));
    electron_pt_iso_full->get_add_hists_num().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelection/ElectronPtIsoFullCut", "TwoDcut_Dr_el_iso", "TwoDcut_Dpt_el_iso", "twod_cut_hist"));
    v_hists.back().emplace_back(electron_pt_iso_full);

    SelEffHists<float> * electron_pt_105_full = new SelEffHists<float>(ctx, "NoSelection/FullSelection", "primary_electron_pt", "electron_pt_105_full", full_el_selection, comb_el_105_selection, 100, 0., 1200., 1.);
    sel_helpers_all->fill_hists_vector(electron_pt_105_full->get_add_hists_den(), "NoSelection/FullSelection/ElectronPt105FullTot");
    sel_helpers_all->fill_hists_vector(electron_pt_105_full->get_add_hists_num(), "NoSelection/FullSelection/ElectronPt105FullCut");
    electron_pt_105_full->get_add_hists_den().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelection/ElectronPt105FullTot", "TwoDcut_Dr_el_iso", "TwoDcut_Dpt_el_iso", "twod_cut_hist"));
    electron_pt_105_full->get_add_hists_num().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelection/ElectronPt105FullCut", "TwoDcut_Dr_el_iso", "TwoDcut_Dpt_el_iso", "twod_cut_hist"));
    v_hists.back().emplace_back(electron_pt_105_full);

    //////////////////////////////////////////////////////
    ///////// FULL SELECTIONS, WITH ST, MIN 1 LEP ////////
    //////////////////////////////////////////////////////


    SelEffHists<double> * muon_st_full = new SelEffHists<double>(ctx, "NoSelection/FullSelectionST", "ST", "muon_st_full", full_mu_selection, comb_mu_selection, 65, 0., 6500., 1.);
    sel_helpers_all->fill_hists_vector(muon_st_full->get_add_hists_den(), "NoSelection/FullSelectionST/MuonPtFullTot");
    sel_helpers_all->fill_hists_vector(muon_st_full->get_add_hists_num(), "NoSelection/FullSelectionST/MuonPtFullCut");
    muon_st_full->get_add_hists_den().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelectionST/MuonPtFullTot", "TwoDcut_Dr_mu", "TwoDcut_Dpt_mu", "twod_cut_hist"));
    muon_st_full->get_add_hists_num().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelectionST/MuonPtFullCut", "TwoDcut_Dr_mu", "TwoDcut_Dpt_mu", "twod_cut_hist"));
    v_hists.back().emplace_back(muon_st_full);

    SelEffHists<double> * electron_st_full = new SelEffHists<double>(ctx, "NoSelection/FullSelectionST", "ST", "electron_st_full", full_el_selection, comb_el_selection, 65, 0., 6500., 1.);
    sel_helpers_all->fill_hists_vector(electron_st_full->get_add_hists_den(), "NoSelection/FullSelectionST/ElectronPtFullTot");
    sel_helpers_all->fill_hists_vector(electron_st_full->get_add_hists_num(), "NoSelection/FullSelectionST/ElectronPtFullCut");
    electron_st_full->get_add_hists_den().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelectionST/ElectronPtFullTot", "TwoDcut_Dr_el", "TwoDcut_Dpt_el", "twod_cut_hist"));
    electron_st_full->get_add_hists_num().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelectionST/ElectronPtFullCut", "TwoDcut_Dr_el", "TwoDcut_Dpt_el", "twod_cut_hist"));
    v_hists.back().emplace_back(electron_st_full);

    SelEffHists<double> * muon_st_iso_full = new SelEffHists<double>(ctx, "NoSelection/FullSelectionST", "ST", "muon_st_iso_full", full_mu_selection, comb_mu_iso_selection, 65, 0., 6500., 1.);
    sel_helpers_all->fill_hists_vector(muon_st_iso_full->get_add_hists_den(), "NoSelection/FullSelectionST/MuonPtIsoFullTot");
    sel_helpers_all->fill_hists_vector(muon_st_iso_full->get_add_hists_num(), "NoSelection/FullSelectionST/MuonPtIsoFullCut");
    muon_st_iso_full->get_add_hists_den().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelectionST/MuonPtIsoFullTot", "TwoDcut_Dr_mu_iso", "TwoDcut_Dpt_mu_iso", "twod_cut_hist"));
    muon_st_iso_full->get_add_hists_num().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelectionST/MuonPtIsoFullCut", "TwoDcut_Dr_mu_iso", "TwoDcut_Dpt_mu_iso", "twod_cut_hist"));
    v_hists.back().emplace_back(muon_st_iso_full);

    SelEffHists<double> * electron_st_iso_full = new SelEffHists<double>(ctx, "NoSelection/FullSelectionST", "ST", "electron_st_iso_full", full_el_selection, comb_el_iso_selection, 65, 0., 6500., 1.);
    sel_helpers_all->fill_hists_vector(electron_st_iso_full->get_add_hists_den(), "NoSelection/FullSelectionST/ElectronPtIsoFullTot");
    sel_helpers_all->fill_hists_vector(electron_st_iso_full->get_add_hists_num(), "NoSelection/FullSelectionST/ElectronPtIsoFullCut");
    electron_st_iso_full->get_add_hists_den().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelectionST/ElectronPtIsoFullTot", "TwoDcut_Dr_el_iso", "TwoDcut_Dpt_el_iso", "twod_cut_hist"));
    electron_st_iso_full->get_add_hists_num().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelectionST/ElectronPtIsoFullCut", "TwoDcut_Dr_el_iso", "TwoDcut_Dpt_el_iso", "twod_cut_hist"));
    v_hists.back().emplace_back(electron_st_iso_full);

    SelEffHists<double> * electron_st_105_full = new SelEffHists<double>(ctx, "NoSelection/FullSelectionST", "ST", "electron_st_105_full", full_el_selection, comb_el_105_selection, 65, 0., 6500., 1.);
    sel_helpers_all->fill_hists_vector(electron_st_105_full->get_add_hists_den(), "NoSelection/FullSelectionST/ElectronPt105FullTot");
    sel_helpers_all->fill_hists_vector(electron_st_105_full->get_add_hists_num(), "NoSelection/FullSelectionST/ElectronPt105FullCut");
    electron_st_105_full->get_add_hists_den().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelectionST/ElectronPt105FullTot", "TwoDcut_Dr_el_iso", "TwoDcut_Dpt_el_iso", "twod_cut_hist"));
    electron_st_105_full->get_add_hists_num().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelectionST/ElectronPt105FullCut", "TwoDcut_Dr_el_iso", "TwoDcut_Dpt_el_iso", "twod_cut_hist"));
    v_hists.back().emplace_back(electron_st_105_full);

    /////////////////////////////////////////////
    ///////// FULL SELECTIONS, MIN 1 LEP ////////
    /////////////////////////////////////////////

    // SelEffHists<float> * muon_pt_full_min1lep = new SelEffHists<float>(ctx, "NoSelection/FullSelectionMin1Lep", "primary_muon_pt", "muon_pt_full", full_mu_selection, comb_mu_selection, 100, 0., 1200., 1.);
    // sel_helpers_all->fill_hists_vector(muon_pt_full_min1lep->get_add_hists_den(), "NoSelection/FullSelectionMin1Lep/MuonPtFullTot");
    // sel_helpers_all->fill_hists_vector(muon_pt_full_min1lep->get_add_hists_num(), "NoSelection/FullSelectionMin1Lep/MuonPtFullCut");
    // muon_pt_full_min1lep->get_add_hists_den().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelectionMin1Lep/MuonPtFullTot", "TwoDcut_Dr_mu", "TwoDcut_Dpt_mu", "twod_cut_hist"));
    // muon_pt_full_min1lep->get_add_hists_num().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelectionMin1Lep/MuonPtFullCut", "TwoDcut_Dr_mu", "TwoDcut_Dpt_mu", "twod_cut_hist"));
    // v_hists.back().emplace_back(muon_pt_full_min1lep);

    // SelEffHists<float> * electron_pt_full_min1lep = new SelEffHists<float>(ctx, "NoSelection/FullSelectionMin1Lep", "primary_electron_pt", "electron_pt_full", full_el_selection, comb_el_selection, 100, 0., 1200., 1.);
    // sel_helpers_all->fill_hists_vector(electron_pt_full_min1lep->get_add_hists_den(), "NoSelection/FullSelectionMin1Lep/ElectronPtFullTot");
    // sel_helpers_all->fill_hists_vector(electron_pt_full_min1lep->get_add_hists_num(), "NoSelection/FullSelectionMin1Lep/ElectronPtFullCut");
    // electron_pt_full_min1lep->get_add_hists_den().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelectionMin1Lep/ElectronPtFullTot", "TwoDcut_Dr_el", "TwoDcut_Dpt_el", "twod_cut_hist"));
    // electron_pt_full_min1lep->get_add_hists_num().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelectionMin1Lep/ElectronPtFullCut", "TwoDcut_Dr_el", "TwoDcut_Dpt_el", "twod_cut_hist"));
    // v_hists.back().emplace_back(electron_pt_full_min1lep);

    // SelEffHists<float> * muon_pt_iso_full_min1lep = new SelEffHists<float>(ctx, "NoSelection/FullSelectionMin1Lep", "primary_muon_pt", "muon_pt_iso_full", full_mu_selection, comb_mu_iso_selection, 100, 0., 1200., 1.);
    // sel_helpers_all->fill_hists_vector(muon_pt_iso_full_min1lep->get_add_hists_den(), "NoSelection/FullSelectionMin1Lep/MuonPtIsoFullTot");
    // sel_helpers_all->fill_hists_vector(muon_pt_iso_full_min1lep->get_add_hists_num(), "NoSelection/FullSelectionMin1Lep/MuonPtIsoFullCut");
    // muon_pt_iso_full_min1lep->get_add_hists_den().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelectionMin1Lep/MuonPtIsoFullTot", "TwoDcut_Dr_mu_iso", "TwoDcut_Dpt_mu_iso", "twod_cut_hist"));
    // muon_pt_iso_full_min1lep->get_add_hists_num().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelectionMin1Lep/MuonPtIsoFullCut", "TwoDcut_Dr_mu_iso", "TwoDcut_Dpt_mu_iso", "twod_cut_hist"));
    // v_hists.back().emplace_back(muon_pt_iso_full_min1lep);

    // SelEffHists<float> * electron_pt_iso_full_min1lep = new SelEffHists<float>(ctx, "NoSelection/FullSelectionMin1Lep", "primary_electron_pt", "electron_pt_iso_full", full_el_selection, comb_el_iso_selection, 100, 0., 1200., 1.);
    // sel_helpers_all->fill_hists_vector(electron_pt_iso_full_min1lep->get_add_hists_den(), "NoSelection/FullSelectionMin1Lep/ElectronPtIsoFullTot");
    // sel_helpers_all->fill_hists_vector(electron_pt_iso_full_min1lep->get_add_hists_num(), "NoSelection/FullSelectionMin1Lep/ElectronPtIsoFullCut");
    // electron_pt_iso_full_min1lep->get_add_hists_den().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelectionMin1Lep/ElectronPtIsoFullTot", "TwoDcut_Dr_el_iso", "TwoDcut_Dpt_el_iso", "twod_cut_hist"));
    // electron_pt_iso_full_min1lep->get_add_hists_num().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelectionMin1Lep/ElectronPtIsoFullCut", "TwoDcut_Dr_el_iso", "TwoDcut_Dpt_el_iso", "twod_cut_hist"));
    // v_hists.back().emplace_back(electron_pt_iso_full_min1lep);

    // SelEffHists<float> * electron_pt_105_full_min1lep = new SelEffHists<float>(ctx, "NoSelection/FullSelectionMin1Lep", "primary_electron_pt", "electron_pt_105_full", full_el_selection, comb_el_105_selection, 100, 0., 1200., 1.);
    // sel_helpers_all->fill_hists_vector(electron_pt_105_full_min1lep->get_add_hists_den(), "NoSelection/FullSelectionMin1Lep/ElectronPt105FullTot");
    // sel_helpers_all->fill_hists_vector(electron_pt_105_full_min1lep->get_add_hists_num(), "NoSelection/FullSelectionMin1Lep/ElectronPt105FullCut");
    // electron_pt_105_full_min1lep->get_add_hists_den().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelectionMin1Lep/ElectronPt105FullTot", "TwoDcut_Dr_el_iso", "TwoDcut_Dpt_el_iso", "twod_cut_hist"));
    // electron_pt_105_full_min1lep->get_add_hists_num().emplace_back(new TwoDCutHist(ctx, "NoSelection/FullSelectionMin1Lep/ElectronPt105FullCut", "TwoDcut_Dr_el_iso", "TwoDcut_Dpt_el_iso", "twod_cut_hist"));
    // v_hists.back().emplace_back(electron_pt_105_full_min1lep);

    

    // if (version.find("TpTp") != string::npos || version.find("BpBp") != string::npos) {
        
    CustomizableGenHists * gen_hists = new CustomizableGenHists(ctx, "NoSelection/GenHists");
    gen_hists->add_genhistcoll(8000001, 0, {"mass", "decay", "dRDecay", "dPhiDecay", "dEtaDecay"});
    gen_hists->add_genhistcoll(8000001, 0, {"mass", "decay", "dRDecay", "dPhiDecay", "dEtaDecay"}, GenParticleId(GenParticleDaughterId(8000001, 6, 25)), "_to_tH");
    gen_hists->add_genhistcoll(6, 0, {"decay", "dRDecay", "dPhiDecay", "dEtaDecay"});
    gen_hists->add_genhistcoll(11, 0, {"charge", "mother", "number"});
    gen_hists->add_genhistcoll(13, 0, {"charge", "mother", "number"});
    gen_hists->add_genhistcoll(11, 0, {"charge", "mother", "number"}, GenParticleId(AndId<GenParticle>(GenParticleMotherId(0, 6), GenParticleMotherId(0, 25), GenParticleMotherId(0, 23))), "_from_T");
    gen_hists->add_genhistcoll(13, 0, {"charge", "mother", "number"}, GenParticleId(AndId<GenParticle>(GenParticleMotherId(0, 6), GenParticleMotherId(0, 25), GenParticleMotherId(0, 23))), "_from_T");
    gen_hists->add_genhistcoll(11, 0, {"charge", "mother", "number"}, GenParticleId(GenParticleMotherId(6)), "_from_top");
    gen_hists->add_genhistcoll(13, 0, {"charge", "mother", "number"}, GenParticleId(GenParticleMotherId(6)), "_from_top");
    gen_hists->add_genhistcoll(25, 0, {"decay", "dRDecay", "dPhiDecay", "dEtaDecay"});
    gen_hists->add_genhistcoll(25, 0, {"decay", "dRDecay", "dPhiDecay", "dEtaDecay", "2d_dRDecay_pt"}, GenParticleId(GenParticleDaughterId(25, 5, 5)), "_to_bb");
    CustomizableGenHists * gen_hists_after = new CustomizableGenHists(ctx, "BaseSelection/GenHists");
    gen_hists_after->add_genhistcoll(8000001, 0, {"mass", "decay", "dRDecay", "dPhiDecay", "dEtaDecay"});
    gen_hists_after->add_genhistcoll(8000001, 0, {"mass", "decay", "dRDecay", "dPhiDecay", "dEtaDecay"}, GenParticleId(GenParticleDaughterId(8000001, 6, 25)), "_to_tH");
    gen_hists_after->add_genhistcoll(6, 0, {"decay", "dRDecay", "dPhiDecay", "dEtaDecay"});
    gen_hists_after->add_genhistcoll(11, 0, {"charge", "mother", "number"});
    gen_hists_after->add_genhistcoll(13, 0, {"charge", "mother", "number"});
    gen_hists_after->add_genhistcoll(11, 0, {"charge", "mother", "number"}, GenParticleId(AndId<GenParticle>(GenParticleMotherId(0, 6), GenParticleMotherId(0, 25), GenParticleMotherId(0, 23))), "_from_T");
    gen_hists_after->add_genhistcoll(13, 0, {"charge", "mother", "number"}, GenParticleId(AndId<GenParticle>(GenParticleMotherId(0, 6), GenParticleMotherId(0, 25), GenParticleMotherId(0, 23))), "_from_T");
    gen_hists_after->add_genhistcoll(11, 0, {"charge", "mother", "number"}, GenParticleId(GenParticleMotherId(6)), "_from_top");
    gen_hists_after->add_genhistcoll(13, 0, {"charge", "mother", "number"}, GenParticleId(GenParticleMotherId(6)), "_from_top");
    gen_hists_after->add_genhistcoll(25, 0, {"decay", "dRDecay", "dPhiDecay", "dEtaDecay"});
    gen_hists_after->add_genhistcoll(25, 0, {"decay", "dRDecay", "dPhiDecay", "dEtaDecay", "2d_dRDecay_pt"}, GenParticleId(GenParticleDaughterId(25, 5, 5)), "_to_bb");
    v_hists.back().push_back(shared_ptr<CustomizableGenHists>(gen_hists));
    v_hists_after_sel.back().push_back(shared_ptr<CustomizableGenHists>(gen_hists_after));
    // v_hists.back().emplace_back(new RecoGenVarComp<double>(ctx, "NoSelection/RecoGenComparisons", "HT", "parton_ht", "HT_parton")); 
    // v_hists.back().emplace_back(new RecoGenVarComp<double>(ctx, "NoSelection/RecoGenComparisons", "HT", "gen_ht", "HT_gen")); 
    // v_hists.back().emplace_back(new TTbarGenHists(ctx, "NoSelection/TTGenHists"));
    // }
    h_base_sel = ctx.get_handle<bool>("sel_all_accepted_base");

    // }


}


bool TpTpSignalStudies::process(Event & event) {

    // std::cout << "NEW EVENT 0" << std::endl;

    if (!common_module->process(event)) {
        return false;
    }
    // common_module->process(event);

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

    // sel_modules_passed.clear();

    // int base_el_ind = -1;
    // for (unsigned i = 0; i < categories.size(); ++i) {
    //     if (categories[i] == "El45_Baseline")
    //         base_el_ind = i;
    // }

    // index 0 corresponds to combined
    // for (unsigned i = 0; i < sel_modules.size(); ++i) {
    
    //     bool all_accepted = sel_modules[i]->process(event);
    //     sel_modules_passed.push_back(all_accepted);

    // }

    sel_modules_base->process(event);
    sel_modules_full->process(event);
    sel_modules_el_base->process(event);
    sel_modules_mu_base->process(event);
    sel_modules_el_lep->process(event);
    sel_modules_mu_lep->process(event);
    sel_modules_el_trg->process(event);
    sel_modules_mu_trg->process(event);
    sel_modules_el_iso_lep->process(event);
    sel_modules_mu_iso_lep->process(event);
    sel_modules_el_105_lep->process(event);
    sel_modules_el_iso_trg->process(event);
    sel_modules_mu_iso_trg->process(event);
    sel_modules_el_105_trg->process(event);



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

    bool all_accepted = event.get(h_base_sel);
    if (all_accepted) {
        for (auto & hist : v_hists_after_sel[0]) {
            hist->fill(event);
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

UHH2_REGISTER_ANALYSIS_MODULE(TpTpSignalStudies)
