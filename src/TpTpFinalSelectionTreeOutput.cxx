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

class TpTpFinalSelectionTreeOutput: public TpTpAnalysisModule {
public:

    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_BASELINE_SEL {
        shared_ptr<SelectionItem>(new SelDatI("gendecay_accept", "GenDecay Accept", 2, -.5, 1.5, 1)),
        shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 8, -.5, 7.5)),
        // shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 8, -.5, 7.5, 2)),
        };
    
    const vector<shared_ptr<SelectionItem>> ADDITIONAL_SEL_ITEMS {
        shared_ptr<SelectionItem>(new SelDatI("is_muon", "Prim Lep is Muon", 2, -.5, 1.5)),
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_isoMu20", "Trigger Accept IsoMu20", 2, -.5, 1.5)),
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_isoEl27", "Trigger Accept IsoEl27", 2, -.5, 1.5)),
        // shared_ptr<SelectionItem>(new SelDatI("is_muon", "Prim Lep is Muon", 2, -.5, 1.5)),
        // shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt", "Primary Lepton p_T", 90, 0., 900.)),
        shared_ptr<SelectionItem>(new SelDatI("n_leptons", "N(Leptons)", 5, -.5, 4.5)),
        shared_ptr<SelectionItem>(new SelDatI("n_btags_medium", "N(medium AK4 b-tags)", 8, -.5, 7.5)),
        shared_ptr<SelectionItem>(new SelDatI("n_ak4", "N(Ak4 Jets)", 12, -.5, 11.5)),
        shared_ptr<SelectionItem>(new SelDatD("ST", "ST", 45, 0, 4500)),
        shared_ptr<SelectionItem>(new SelDatF("pt_third_ak4_jet", "Pt third Ak4 Jet", 60, 0., 1500.)),
        shared_ptr<SelectionItem>(new SelDatF("pt_fourth_ak4_jet", "Pt fourth Ak4 Jet", 60, 0., 1500.)),
        shared_ptr<SelectionItem>(new SelDatF("pt_fifth_ak4_jet", "Pt fifth Ak4 Jet", 60, 0., 1500.)),
        shared_ptr<SelectionItem>(new SelDatF("pt_sixth_ak4_jet", "Pt sixth Ak4 Jet", 60, 0., 1500.)),
        shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak8_jet", "Pt leading Ak8 Jet", 60, 0., 1500.)),
        shared_ptr<SelectionItem>(new SelDatF("pt_subld_ak8_jet", "Pt subld Ak8 Jet", 60, 0., 1500.)),
        shared_ptr<SelectionItem>(new SelDatF("pt_third_ak8_jet", "Pt third Ak8 Jet", 60, 0., 1500.)),
        shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt", "Primary Lepton p_T", 90, 0., 900., 47.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_subld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500.)),
        shared_ptr<SelectionItem>(new SelDatI("n_ak8_higgs_cand", "N(Higgs Candidates)", 8, -.5, 7.5)),
        shared_ptr<SelectionItem>(new SelDatI("n_jets_no_overlap", "N(non-overlapping Ak4 jets)", 12, -.5, 11.5)),
        shared_ptr<SelectionItem>(new SelDatF("ak4_btagged_dR_higgs_tags_1b_med", "dR(b-tag ak4, htag)", 50, 0., 5.)),
        shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 5, -.5, 4.5)),
        shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 5, -.5, 4.5)),
        shared_ptr<SelectionItem>(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 8, -.5, 7.5)),
        shared_ptr<SelectionItem>(new SelDatD("h1b_allAk8_mass_HLep", "Lep mass(H1b, allAk8)", 45, 0, 4500)),
        shared_ptr<SelectionItem>(new SelDatD("h1b_allAk8_mass_Htop", "Had mass(H1b, allAk8)", 45, 0, 4500)),
        shared_ptr<SelectionItem>(new SelDatD("h1b_allAk8_mass_Max", "Max mass(H1b, allAk8)", 45, 0, 4500)),
        shared_ptr<SelectionItem>(new SelDatD("h1b_allAk8_mass_Min", "Min mass(H1b, allAk8)", 45, 0, 4500)),
        shared_ptr<SelectionItem>(new SelDatD("h2b_allAk8_mass_HLep", "Lep mass(H2b, allAk8)", 45, 0, 4500)),
        shared_ptr<SelectionItem>(new SelDatD("h2b_allAk8_mass_Htop", "Had mass(H2b, allAk8)", 45, 0, 4500)),
        shared_ptr<SelectionItem>(new SelDatD("h2b_allAk8_mass_Max", "Max mass(H2b, allAk8)", 45, 0, 4500)),
        shared_ptr<SelectionItem>(new SelDatD("h2b_allAk8_mass_Min", "Min mass(H2b, allAk8)", 45, 0, 4500)),
        shared_ptr<SelectionItem>(new SelDatD("h1b_toptags_mass_HLep", "Lep mass(H1b, toptags)", 45, 0, 4500)),
        shared_ptr<SelectionItem>(new SelDatD("h1b_toptags_mass_Htop", "Had mass(H1b, toptags)", 45, 0, 4500)),
        shared_ptr<SelectionItem>(new SelDatD("h1b_toptags_mass_Max", "Max mass(H1b, toptags)", 45, 0, 4500)),
        shared_ptr<SelectionItem>(new SelDatD("h1b_toptags_mass_Min", "Min mass(H1b, toptags)", 45, 0, 4500)),
        shared_ptr<SelectionItem>(new SelDatD("h2b_toptags_mass_HLep", "Lep mass(H2b, toptags)", 45, 0, 4500)),
        shared_ptr<SelectionItem>(new SelDatD("h2b_toptags_mass_Htop", "Had mass(H2b, toptags)", 45, 0, 4500)),
        shared_ptr<SelectionItem>(new SelDatD("h2b_toptags_mass_Max", "Max mass(H2b, toptags)", 45, 0, 4500)),
        shared_ptr<SelectionItem>(new SelDatD("h2b_toptags_mass_Min", "Min mass(H2b, toptags)", 45, 0, 4500)),
    };



    explicit TpTpFinalSelectionTreeOutput(Context & ctx);
    virtual bool process(Event & event) override;

private:
    unique_ptr<AnalysisModule> common_module;
    // unique_ptr<NParticleMultiHistProducerHelper<TopJet>> ak8jet_hists/*, ca15jet_hists*/;
    unique_ptr<AnalysisModule> btag_sf_sr, btag_sf_cr;
    Event::Handle<double> weight_hndl;
    Event::Handle<float> jetpt_weight_hndl;
    // Event::Handle<int> use_sr_sf_hndl;
    vector<vector<unique_ptr<Hists>>> v_reweighted_hists_after_sel;

};



TpTpFinalSelectionTreeOutput::TpTpFinalSelectionTreeOutput(Context & ctx) : TpTpAnalysisModule(ctx) {

    auto data_dir_path = ctx.get("data_dir_path");

    ctx.undeclare_all_event_output();
    jetpt_weight_hndl = ctx.declare_event_output<float>("weight_ak4_jetpt");
    ctx.declare_event_output<float>("weight_ak4_jetpt_up");
    ctx.declare_event_output<float>("weight_ak4_jetpt_down");
    // ctx.declare_event_output<float>("weight_ak8_jetpt");

    weight_hndl = ctx.declare_event_output<double>("weight");
    // use_sr_sf_hndl = ctx.declare_event_output<int>("use_sr_sf");
    ctx.declare_event_output<std::vector<Jet>>("jets");
    ctx.declare_event_output<std::vector<TopJet>>("ak8_boost");

    // bool is_background = (version.find("TpTp") == string::npos && type == "MC") ;

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

    other_modules.emplace_back(new MCPileupReweight(ctx));


    auto ak8_corr = (type == "MC") ? JERFiles::Summer15_25ns_L23_AK8PFchs_MC 
    : JERFiles::Summer15_25ns_L23_AK8PFchs_DATA;
    auto ak4_corr = (type == "MC") ? JERFiles::Summer15_25ns_L123_AK4PFchs_MC 
    : JERFiles::Summer15_25ns_L123_AK4PFchs_DATA;
    if (ctx.get("jecsmear_direction", "nominal") != "nominal") {
        pre_modules.emplace_back(new GenericTopJetCorrector(ctx,
            ak8_corr, "topjets"));
        // pre_modules.emplace_back(new GenericSubJetCorrector(ctx,
        //     ak4_corr, "topjets"));
        pre_modules.emplace_back(new JetCorrector(ctx, ak4_corr));
    }
    pre_modules.emplace_back(new TopJetCleaner(ctx, MinMaxDeltaRId<Electron>(ctx, "electrons", 0.2), "topjets"));
    pre_modules.emplace_back(new TopJetCleaner(ctx, MinMaxDeltaRId<Muon>(ctx, "muons", 0.2), "topjets"));
    pre_modules.emplace_back(new TopJetCleaner(ctx, PtEtaCut(200., 2.4), "topjets"));


    if (type == "MC") {
        pre_modules.emplace_back(new JetResolutionSmearer(ctx));    
    }
    pre_modules.emplace_back(new JetCleaner(ctx, AndId<Jet>(JetPFID(JetPFID::WP_LOOSE), PtEtaCut(30.0,2.4))));
    other_modules.emplace_back(new MCMuonScaleFactor(ctx, 
        data_dir_path + "MuonID_Z_RunD_Reco74X_Nov20.root", 
        "NUM_TightIDandIPCut_DEN_genTracks_PAR_pt_spliteta_bin1", 1., "id", "nominal", "prim_mu_coll"));
    other_modules.emplace_back(new MCMuonScaleFactor(ctx, 
        data_dir_path + "SingleMuonTrigger_Z_RunD_Reco74X_Nov20.root", 
        "Mu45_eta2p1_PtEtaBins", 1., "trg", "nominal", "prim_mu_coll"));

    if (version.find("TpTp") != string::npos) {
        other_modules.emplace_back(new PDFWeightBranchCreator(ctx, 110, false));
        other_modules.emplace_back(new ScaleVariationWeightBranchCreator(ctx));
    }
    else if (version.find("DYJets") != string::npos ||
        version.find("SingleTop_t-channel") != string::npos ||
        version.find("SingleTop_s-channel") != string::npos ||
        version.find("WJets") != string::npos ||
        version.find("TTbar") != string::npos
        ) {
        other_modules.emplace_back(new PDFWeightBranchCreator(ctx, 9, false));
        other_modules.emplace_back(new ScaleVariationWeightBranchCreator(ctx));
    }
    else {
        other_modules.emplace_back(new PDFWeightBranchCreator(ctx, -1, false));
        other_modules.emplace_back(new ScaleVariationWeightBranchCreator(ctx, true));   
    }


    // =====PRODUCERS========

    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "topjets",
                "toptags",
                TopJetId(AndId<TopJet>(PtEtaCut(400., 2.4), Type2TopTag(140, 250, Type2TopTag::MassType::groomed), Tau32(0.74)))
                ));


    other_modules.emplace_back(new TPrimeMassProducer(ctx,
                "higgs_tags_1b_med",
                "topjets",
                "PrimaryLepton",
                "h1b_allAk8"
                ));

    other_modules.emplace_back(new TPrimeMassProducer(ctx,
                "higgs_tags_2b_med",
                "topjets",
                "PrimaryLepton",
                "h2b_allAk8"
                ));

    other_modules.emplace_back(new TPrimeMassProducer(ctx,
                "higgs_tags_1b_med",
                "topjets",
                "PrimaryLepton",
                "h1b_toptags"
                ));

    other_modules.emplace_back(new TPrimeMassProducer(ctx,
                "higgs_tags_2b_med",
                "topjets",
                "PrimaryLepton",
                "h2b_toptags"
                ));


    other_modules.emplace_back(new CollectionProducer<Jet>(ctx,
                "jets",
                "ak4_jets_btagged",
                JetId(CSVBTag(CSVBTag::WP_MEDIUM))
                ));

    // btag_sf_sr.reset(new MCBTagScaleFactor(ctx, CSVBTag::WP_MEDIUM, "ak8_higgs_cand"));
    btag_sf_cr.reset(new MCBTagScaleFactor(ctx, CSVBTag::WP_MEDIUM, "tj_btag_sf_coll"));

    other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "ak8_higgs_cand",
                "n_ak8_higgs_cand"
                ));

    other_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
                "jets_no_overlap",
                "n_jets_no_overlap"
                ));

    other_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
                "jets_no_overlap",
                "n_additional_btags_medium",
                JetId(CSVBTag(CSVBTag::WP_MEDIUM))
                ));

    other_modules.emplace_back(new JetVarProducer<TopJet>(ctx,
                "topjets",
                "first_ak8jet",
                "PrimaryLepton",
                CSVBTag(CSVBTag::WP_MEDIUM),
                1
                ));
    other_modules.emplace_back(new JetVarProducer<TopJet>(ctx,
                "topjets",
                "second_ak8jet",
                "PrimaryLepton",
                CSVBTag(CSVBTag::WP_MEDIUM),
                2
                ));
    other_modules.emplace_back(new JetVarProducer<TopJet>(ctx,
                "higgs_tags_1b_med",
                "higgs_tag_1b",
                "PrimaryLepton",
                CSVBTag(CSVBTag::WP_MEDIUM),
                1
                ));
    other_modules.emplace_back(new JetVarProducer<TopJet>(ctx,
                "higgs_tags_2b_med",
                "higgs_tag_2b",
                "PrimaryLepton",
                CSVBTag(CSVBTag::WP_MEDIUM),
                1
                ));

    other_modules.emplace_back(new JetVarProducer<Jet>(ctx,
                "ak4_jets_btagged",
                "ak4_btagged",
                "higgs_tags_1b_med",
                "PrimaryLepton",
                CSVBTag(CSVBTag::WP_MEDIUM),
                1
                ));

    // other_modules.emplace_back(new TopJetDeltaRProducer(ctx,
    //             "topjets",
    //             1
    //             ));
    // other_modules.emplace_back(new TopJetDeltaRProducer(ctx,
    //             "topjets",
    //             2
    //             ));
    // other_modules.emplace_back(new TopJetDeltaRProducer(ctx,
    //             "higgs_tags_1b_med",
    //             1
    //             ));
    // other_modules.emplace_back(new TopJetDeltaRProducer(ctx,
    //             "higgs_tags_2b_med",
    //             1
    //             ));

    





    // check if there is exactly 1 Higgs Tag; if yes, make sure that all higgs tags are
    // well separated from it by making a dR requirement of 1.5
    // other_modules.emplace_back(new XTopTagProducer(ctx, "toptags_boost", "min_dr_higgs", "one_top", 1.5, 1));
    // other_modules.emplace_back(new XTopTagProducer(ctx, "toptags_boost", "dummy_dr", "two_top", -999., 2));
    
    // vector<string> final_states;
    // if (version.find("TpTp") != string::npos)
    //     final_states = {"thth", "thtz", "thbw", "noH_tztz", "noH_tzbw", "noH_bwbw"};
    // else
    //     final_states = {"All"};
        
    vector<string> categories = split(ctx.get("category", ""));
    // std::vector<string> categories = {"NoSelection",
    //     "HiggsTag0Med-Control", //"HiggsTag0Med-Control-2Ak8", "HiggsTag0Med-Control-3Ak8", "HiggsTag0Med-Control-4Ak8", 
    //     "HiggsTag1bMed-Signal", //"HiggsTag1bMed-Signal-1addB", "HiggsTag1bMed-Signal-2addB", "HiggsTag1bMed-Signal-3addB",
    //     "HiggsTag2bMed-Signal", 
    //     }; // "NoSelection", "HiggsTag2bLoose-Signal", "AntiHiggsTagLoose-Control", "AntiHiggsTagMed-Control", "HiggsTag0Loose-Control", 

    // for (auto const & fs : final_states) {
    for (auto const & cat : categories) {


        SEL_ITEMS_FULL_SEL.push_back(SEL_ITEMS_BASELINE_SEL);

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
        else {
            other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
                GenParticleId(TrueId<GenParticle>::is_true), GenParticleId(TrueId<GenParticle>::is_true)));
        }



        if (split(cat, "-")[0] == "NoSelection") {
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_el45", "Trigger Accept El45", 2, -.5, 1.5));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_mu45", "Trigger Accept Mu45", 2, -.5, 1.5));
            // SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_lepton_pt", "Primary Lepton p_T", 90, 0., 900.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_subld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500.));
            // SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 5, -.5, 4.5));
            // SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 5, -.5, 4.5));
            // SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 8, -.5, 7.5));
            
        }
        if (split(cat, "-")[0] == "Mu45_Baseline") {
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_mu45", "Trigger Accept", 2, -.5, 1.5, 1));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_muon_pt", "Primary Lepton p_T", 90, 0., 900., 47.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_subld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500.));
            // SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 5, -.5, 4.5));
            // SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 8, -.5, 7.5));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_el45", "Trigger Accept El45", 2, -.5, 1.5));
            
        }
        if (split(cat, "-")[0] == "El45_Baseline") {
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_el45", "Trigger Accept", 2, -.5, 1.5, 1));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_mu45", "Trigger Accept Mu45", 2, -.5, 1.5, 0, 0));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_electron_pt", "Primary Lepton p_T", 90, 0., 900., 50.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500., 250.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_subld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500., 65.));
            // SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 5, -.5, 4.5));
            // SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 5, -.5, 4.5));
            // SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 8, -.5, 7.5));
            
        }
        // else if (split(cat, "-")[0] == "El45_H2B") {
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_el45", "Trigger Accept El45", 2, -.5, 1.5));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 5, -.5, 4.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 8, -.5, 7.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 5, -.5, 4.5));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_mu45", "Trigger Accept Mu45", 2, -.5, 1.5));
        // }
        // else if (split(cat, "-")[0] == "El45_H1B") {
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_el45", "Trigger Accept El45", 2, -.5, 1.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 5, -.5, 4.5, 0, 0));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 5, -.5, 4.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 8, -.5, 7.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_mu45", "Trigger Accept Mu45", 2, -.5, 1.5));
        // }
        // else if (split(cat, "-")[0] == "El45_Control") {
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_el45", "Trigger Accept El45", 2, -.5, 1.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 5, -.5, 4.5, 0, 0));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 8, -.5, 7.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 5, -.5, 4.5));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_mu45", "Trigger Accept Mu45", 2, -.5, 1.5));
        // }
        // else if (split(cat, "-")[0] == "Mu45_H2B") {
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_mu45", "Trigger Accept Mu45", 2, -.5, 1.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 5, -.5, 4.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 8, -.5, 7.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 5, -.5, 4.5));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_el45", "Trigger Accept El45", 2, -.5, 1.5));
        // }
        // else if (split(cat, "-")[0] == "Mu45_H1B") {
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_mu45", "Trigger Accept Mu45", 2, -.5, 1.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 5, -.5, 4.5, 0, 0));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 5, -.5, 4.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 8, -.5, 7.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_el45", "Trigger Accept El45", 2, -.5, 1.5));
        // }
        // else if (split(cat, "-")[0] == "Mu45_Control") {
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_mu45", "Trigger Accept Mu45", 2, -.5, 1.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 5, -.5, 4.5, 0, 0));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 8, -.5, 7.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 5, -.5, 4.5));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_el45", "Trigger Accept El45", 2, -.5, 1.5));
        // }


        for (auto const & sel_item : ADDITIONAL_SEL_ITEMS)
            SEL_ITEMS_FULL_SEL.back().push_back(sel_item);

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

        v_hists.emplace_back(vector<unique_ptr<Hists>>());
        v_hists_after_sel.emplace_back(vector<unique_ptr<Hists>>());
        v_reweighted_hists_after_sel.emplace_back(vector<unique_ptr<Hists>>());
        // v_genhist_2h_after_sel.emplace_back(vector<unique_ptr<Hists>>());
        // v_genhist_1h_after_sel.emplace_back(vector<unique_ptr<Hists>>());


        auto nm1_hists = new Nm1SelHists(ctx, cat+"/Nm1Selection", *sel_helpers.back());
        auto cf_hists = new VLQ2HTCutflow(ctx, cat+"/Cutflow", *sel_helpers.back());

        map<string, SelectedSelHists*> selected_sel_hists;
        selected_sel_hists["NoNAk8Cut"] = new SelectedSelHists(ctx, cat+"/NoNAk8Cut", *sel_helpers.back(), {}, {"n_ak8"});
        // selected_sel_hists["OnlyTopTagCut"] = new SelectedSelHists(ctx, cat+"/OnlyTopTagCut", *sel_helpers.back(), {"n_cmstoptagsv2"});
        // selected_sel_hists["OnlyNAk8JetsCut"] = new SelectedSelHists(ctx, cat+"/OnlyNAk8JetsCut", *sel_helpers.back(), {"n_ak8"});


        
        for (auto hist : selected_sel_hists) {
            // hist.second->insert_hist_and_sel(pos_2d_cut, new TwoDCutHist(ctx, cat+"/"+hist.first, "TwoDcut_Dr_noIso", "TwoDcut_Dpt_noIso", "twod_cut_hist_noIso"), "twoD_cut");
            // for (auto const & hist_helper : ak8jet_hists) {
            hist.second->insert_additional_hist(new OwnHistCollector(ctx, cat+"/"+hist.first, type == "MC", CSVBTag(CSVBTag::WP_MEDIUM), {"el", "cmstopjet"}));
            hist.second->insert_additional_hist(new ExtendedTopJetHists(ctx, cat+"/"+hist.first+"/HTags", CSVBTag(CSVBTag::WP_MEDIUM), 2, "higgs_tags_1b_med"));
            // }
            v_hists.back().emplace_back(hist.second);
        }

        v_hists.back().emplace_back(nm1_hists);
        v_hists.back().emplace_back(cf_hists);
        if (split(cat, "-")[0] == "NoSelection") {
            // sel_helpers.back()->fill_hists_vector(v_hists.back(), cat+"/NoSelection");
            // v_hists.back().emplace_back(new OwnHistCollector(ctx, cat+"/NoSelection", type == "MC", CSVBTag(CSVBTag::WP_MEDIUM), {"ev", "jet"}));
            // v_hists_after_sel.back().emplace_back(new BTagMCEfficiencyHists(ctx, cat+"/BTagMCEfficiencyHists", CSVBTag::WP_MEDIUM, "tj_btag_sf_coll"));
            // v_reweighted_hists_after_sel.back().emplace_back(new BTagMCEfficiencyHists(ctx, cat+"/BTagMCEfficiencyHists", CSVBTag::WP_MEDIUM, "tj_btag_sf_coll"));
        }
        sel_helpers.back()->fill_hists_vector(v_hists_after_sel.back(), cat+"/PostSelection");
        sel_helpers.back()->fill_hists_vector(v_reweighted_hists_after_sel.back(), cat+"/PostSelectionReweighted");
        // for (auto const & hist_helper : ak8jet_hists) {
        // if (version.find("thth") != string::npos) {
        //     v_genhist_2h_after_sel.back().emplace_back(new HiggsGenHist(ctx, cat+"/PostSelection/HiggsGen2Higgs/HiggsGenAllAk8", "topjets", "2h"));
        //     v_genhist_2h_after_sel.back().emplace_back(new HiggsGenHist(ctx, cat+"/PostSelection/HiggsGen2Higgs/HiggsGenHiggsCands", "ak8_higgs_cand", "2h"));
        //     v_genhist_2h_after_sel.back().emplace_back(new HiggsGenHist(ctx, cat+"/PostSelection/HiggsGen2Higgs/HiggsGenHiggsTags1b", "higgs_tags_1b_med", "2h"));
        //     v_genhist_2h_after_sel.back().emplace_back(new HiggsGenHist(ctx, cat+"/PostSelection/HiggsGen2Higgs/HiggsGenHiggsTags2b", "higgs_tags_2b_med", "2h"));
        // }
        // if (version.find("thtz") != string::npos || version.find("thbw") != string::npos) {
        //     v_genhist_1h_after_sel.back().emplace_back(new HiggsGenHist(ctx, cat+"/PostSelection/HiggsGen1Higgs/HiggsGenAllAk8", "topjets", "1h"));
        //     v_genhist_1h_after_sel.back().emplace_back(new HiggsGenHist(ctx, cat+"/PostSelection/HiggsGen1Higgs/HiggsGenHiggsCands", "ak8_higgs_cand", "1h"));
        //     v_genhist_1h_after_sel.back().emplace_back(new HiggsGenHist(ctx, cat+"/PostSelection/HiggsGen1Higgs/HiggsGenHiggsTags1b", "higgs_tags_1b_med", "1h"));
        //     v_genhist_1h_after_sel.back().emplace_back(new HiggsGenHist(ctx, cat+"/PostSelection/HiggsGen1Higgs/HiggsGenHiggsTags2b", "higgs_tags_2b_med", "1h"));
        // }
        v_hists_after_sel.back().emplace_back(ak8jet_hists->book_histograms(ctx, cat+"/PostSelection"));
        v_reweighted_hists_after_sel.back().emplace_back(ak8jet_hists->book_histograms(ctx, cat+"/PostSelectionReweighted"));
        v_hists_after_sel.back().emplace_back(new OwnHistCollector(ctx, cat+"/PostSelection", type == "MC", CSVBTag(CSVBTag::WP_MEDIUM), {"ev", "mu", "el", "jet", "lumi", "cmstopjet"}));
        v_hists_after_sel.back().emplace_back(new ExtendedTopJetHists(ctx, cat+"/PostSelection/HTags", CSVBTag(CSVBTag::WP_MEDIUM), 2, "higgs_tags_1b_med"));
        v_reweighted_hists_after_sel.back().emplace_back(new OwnHistCollector(ctx, cat+"/PostSelectionReweighted", type == "MC", CSVBTag(CSVBTag::WP_MEDIUM), {"ev", "mu", "el", "jet", "lumi", "cmstopjet"}));
        // v_hists_after_sel.back().emplace_back(new JetCleaningControlPlots(ctx, cat+"/PostSelection/JetCleaningControlPlots", "weight_ak4_jetpt", "weight_ak8_jetpt"));
        // v_hists_after_sel.back().emplace_back(new JetCleaningControlPlots(ctx, cat+"/PostSelection/JetCleaningControlPlotsUp", "weight_ak4_jetpt_up"));
        // v_hists_after_sel.back().emplace_back(new JetCleaningControlPlots(ctx, cat+"/PostSelection/JetCleaningControlPlotsDown", "weight_ak4_jetpt_down"));

            // v_hists_after_sel.emplace_back(new HistCollector(ctx, "EventHistsPost"));

        // }
    }


}


bool TpTpFinalSelectionTreeOutput::process(Event & event) {

    common_module->process(event);

    for (auto & mod : pre_modules) {
        mod->process(event);
    }

    assert(event.topjets);
    sort_by_pt(*event.topjets);

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

    }

    btag_sf_cr->process(event);
    
    // all hists
    for (auto & hist_vec : v_hists) {
        for (auto & hist : hist_vec) {
            hist->fill(event);
        }
    }


    // if (sel_modules_passed[2] || sel_modules_passed[3]) {
    //     btag_sf_sr->process(event);
        // event.set(use_sr_sf_hndl, 1);
    // }
    // else {
    // }
    // event.set(use_sr_sf_hndl, 0);
    
    event.set(weight_hndl, event.weight);

    bool write_out = false;

    for (unsigned i = 0; i < sel_modules.size(); ++i) {

        bool all_accepted = sel_modules_passed[i];
        if (all_accepted) {
            write_out = true;
            for (auto & hist : v_hists_after_sel[i]) {
                hist->fill(event);
            }
        }

    }

    if (version.find("TpTp") == string::npos && type == "MC")
        event.weight *= event.get(jetpt_weight_hndl);

    for (unsigned i = 0; i < sel_modules.size(); ++i) {
    
        bool all_accepted = sel_modules_passed[i];
        if (all_accepted) {

            for (auto & hist : v_reweighted_hists_after_sel[i]) {
                hist->fill(event);
            }
        }

    }



    // run all modules
    // for (bool pass_sel : sel_modules_passed) {
    //     if (pass_sel) return true;
    // }

    return write_out;
}

UHH2_REGISTER_ANALYSIS_MODULE(TpTpFinalSelectionTreeOutput)
