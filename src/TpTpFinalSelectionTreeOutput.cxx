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
        shared_ptr<SelectionItem>(new SelDatF("deltaRlep_topjets_1", "dR(Ak8 jet, prim. lepton)", 50, 0., 5., 0.8)),
        shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 5, -.5, 4.5)),
        shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 5, -.5, 4.5)),
        shared_ptr<SelectionItem>(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 8, -.5, 7.5)),
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_mu45", "Trigger Accept", 2, -.5, 1.5)),
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_el40", "Trigger Accept", 2, -.5, 1.5)),
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_isoMu", "Trigger Accept", 2, -.5, 1.5)),
        // shared_ptr<SelectionItem>(new SelDatI("is_muon", "Prim Lep is Muon", 2, -.5, 1.5)),
        shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt", "Primary Lepton p_T", 90, 0., 900.)),
        // shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 8, -.5, 7.5, 3)),
        shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 8, -.5, 7.5)),
        // shared_ptr<SelectionItem>(new SelDatI("n_ak8_pt_cleaned", "N(Ak8 Jets cleaned)", 8, -.5, 7.5)),
        shared_ptr<SelectionItem>(new SelDatI("n_ak4", "N(Ak4 Jets)", 12, -.5, 11.5)),
        // shared_ptr<SelectionItem>(new SelDatI("n_ak4_pt_cleaned", "N(Ak4 Jets cleaned)", 12, -.5, 11.5)),

        shared_ptr<SelectionItem>(new SelDatD("ST", "ST", 45, 0, 4500)),
        // shared_ptr<SelectionItem>(new SelDatD("ST_cleaned", "ST cleaned", 45, 0, 4500)),
        shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak8_jet", "Pt leading Ak8 Jet", 60, 0., 1500.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak8_jet_cleaned", "Pt leading Ak8 Jet cleaned", 60, 0., 1500.)),
        shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 60, 0., 1500.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak4_jet_cleaned", "Pt leading Ak4 Jet cleaned", 60, 0., 1500.)),

        // shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_1b_med", "N(Higgs Tags, 1 b)", 8, -.5, 7.5)),
        // shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_2b_med", "N(Higgs Tags, 2 b)", 8, -.5, 7.5)),
        shared_ptr<SelectionItem>(new SelDatI("n_ak8_higgs_cand", "N(Higgs Candidates)", 8, -.5, 7.5)),
        shared_ptr<SelectionItem>(new SelDatI("n_jets_no_overlap", "N(non-overlapping Ak4 jets)", 12, -.5, 11.5)),
        // shared_ptr<SelectionItem>(new SelDatI("max_n_subjet_btags", "max N(medium sj b-tags)", 4, -.5, 3.5)),
        // shared_ptr<SelectionItem>(new SelDatF("mass_higgs_cands_max_btag", "N(non-overlapping Ak4 jets)", 30, 0., 300.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak8_jet", "Pt leading Ak8 Jet", 60, 0., 1500., 300.)),
        // shared_ptr<SelectionItem>(new SelDatF("primary_muon_pt_dRak8", "Primary Muon (dRak8) p_T", 90, 0., 900.))
        shared_ptr<SelectionItem>(new SelDatF("deltaRak4_topjets_1", "dR(Ak8 jet, closest Ak4 jet)", 50, 0., 5.)),
        shared_ptr<SelectionItem>(new SelDatF("deltaRak8_topjets_1", "dR(Ak8 jet, closest Ak8 jet)", 50, 0., 5.)),
        shared_ptr<SelectionItem>(new SelDatF("deltaRlep_topjets_2", "dR(Ak8 jet, prim. lepton)", 50, 0., 5.)),
        shared_ptr<SelectionItem>(new SelDatF("deltaRak4_topjets_2", "dR(Ak8 jet, closest Ak4 jet)", 50, 0., 5.)),
        shared_ptr<SelectionItem>(new SelDatF("deltaRak8_topjets_2", "dR(Ak8 jet, closest Ak8 jet)", 50, 0., 5.)),
        shared_ptr<SelectionItem>(new SelDatF("deltaRlep_higgs_tags_1b_med_1", "dR(Ak8 jet, prim. lepton)", 50, 0., 5.)),
        shared_ptr<SelectionItem>(new SelDatF("deltaRak4_higgs_tags_1b_med_1", "dR(Ak8 jet, closest Ak4 jet)", 50, 0., 5.)),
        shared_ptr<SelectionItem>(new SelDatF("deltaRak8_higgs_tags_1b_med_1", "dR(Ak8 jet, closest Ak8 jet)", 50, 0., 5.)),
        shared_ptr<SelectionItem>(new SelDatF("deltaRlep_higgs_tags_2b_med_1", "dR(Ak8 jet, prim. lepton)", 50, 0., 5.)),
        shared_ptr<SelectionItem>(new SelDatF("deltaRak4_higgs_tags_2b_med_1", "dR(Ak8 jet, closest Ak4 jet)", 50, 0., 5.)),
        shared_ptr<SelectionItem>(new SelDatF("deltaRak8_higgs_tags_2b_med_1", "dR(Ak8 jet, closest Ak8 jet)", 50, 0., 5.)),
    };



    explicit TpTpFinalSelectionTreeOutput(Context & ctx);
    virtual bool process(Event & event) override;

private:
    unique_ptr<AnalysisModule> common_module;
    unique_ptr<NParticleMultiHistProducerHelper<TopJet>> ak8jet_hists/*, ca15jet_hists*/;
    unique_ptr<AnalysisModule> btag_sf_sr, btag_sf_cr;
    Event::Handle<double> weight_hndl;
    Event::Handle<int> use_sr_sf_hndl;
    vector<vector<unique_ptr<Hists>>> v_genhist_1h_after_sel, v_genhist_2h_after_sel;

};




TpTpFinalSelectionTreeOutput::TpTpFinalSelectionTreeOutput(Context & ctx) : TpTpAnalysisModule(ctx) {

    auto data_dir_path = ctx.get("data_dir_path");

    ctx.undeclare_all_event_output();
    ctx.declare_event_output<float>("ak4_jetpt_weight");
    ctx.declare_event_output<float>("ak4_jetpt_weight_up");
    ctx.declare_event_output<float>("ak4_jetpt_weight_down");
    ctx.declare_event_output<float>("ak8_jetpt_weight");

    weight_hndl = ctx.declare_event_output<double>("weight");
    use_sr_sf_hndl = ctx.declare_event_output<int>("use_sr_sf");

    // bool is_background = (version.find("TpTp") == string::npos && type == "MC") ;

    CommonModules* commonObjectCleaning = new CommonModules();
    // commonObjectCleaning->set_jet_id(AndId<Jet>(JetPFID(JetPFID::WP_LOOSE), PtEtaCut(30.0,2.4)));
    commonObjectCleaning->disable_jersmear();
    commonObjectCleaning->disable_jec();
    // commonObjectCleaning->disable_mcpileupreweight();
    // commonObjectCleaning->set_electron_id(AndId<Electron>(ElectronID_Spring15_25ns_medium_noIso,PtEtaCut(20.0, 2.4)));
    // commonObjectCleaning->set_muon_id(AndId<Muon>(MuonIDTight(),PtEtaCut(20.0, 2.1)));
    // commonObjectCleaning->switch_jetlepcleaner(true);
    // commonObjectCleaning->switch_jetPtSorter(true);
    // commonObjectCleaning->disable_lumisel();
    commonObjectCleaning->init(ctx);
    common_module.reset(commonObjectCleaning);

    if (ctx.get("jecsmear_direction", "nominal") != "nominal") {
        auto ak8_corr = (type == "MC") ? JERFiles::Summer15_25ns_L123_AK8PFchs_MC 
                                       : JERFiles::Summer15_25ns_L123_AK8PFchs_DATA;
        auto ak4_corr = (type == "MC") ? JERFiles::Summer15_25ns_L123_AK8PFchs_MC 
                                       : JERFiles::Summer15_25ns_L123_AK8PFchs_DATA;
        pre_modules.emplace_back(new GenericTopJetCorrector(ctx,
            ak8_corr, "topjets"));
        pre_modules.emplace_back(new GenericSubJetCorrector(ctx,
            ak4_corr, "topjets"));
        pre_modules.emplace_back(new JetCorrector(ctx, ak4_corr));
    }

    // if (type == "MC") {
    //     pre_modules.emplace_back(new JetResolutionSmearer(ctx));    
    // }
    other_modules.emplace_back(new MCMuonScaleFactor(ctx, 
        data_dir_path + "MuonID_Z_RunD_Reco74X_Nov20.root", 
        "NUM_TightIDandIPCut_DEN_genTracks_PAR_pt_spliteta_bin1", 1., "id"));
    other_modules.emplace_back(new MCMuonScaleFactor(ctx, 
        data_dir_path + "SingleMuonTrigger_Z_RunD_Reco74X_Nov20.root", 
        "Mu45_eta2p1_PtEtaBins", 1., "trg"));





    // =====PRODUCERS========

    
    ak8jet_hists.reset(new NParticleMultiHistProducerHelper<TopJet>("FirstAk8SoftDropSlimmed", "topjets", vector<string>{"n", "pt", "eta", "phi", "mass_sj", "n_subjets", "dRlepton", "dRak4", "dRak8"}));
    ak8jet_hists->add_level("SecondAk8SoftDropSlimmed", "topjets", vector<string>{"n", "pt", "eta", "phi", "mass_sj", "n_subjets", "dRlepton", "dRak4", "dRak8"}, 2);

    // boosted Ak8 jets
    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "topjets",
                "ak8_boost",
                TopJetId(PtEtaCut(300., 2.4))
                ));

    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost",
                "ak8_higgs_cand",
                TopJetId(HiggsFlexBTag(60., 99999.))
                ));

    // ak4 jets not overlapping with higgs-candidates, collected together with higgs-candidates in one TopJet collection for applying b-tag scale factors
    other_modules.emplace_back(new CollectionProducer<Jet>(ctx,
                "jets",
                "jets_no_overlap",
                JetId(MinMaxDeltaRId<TopJet>(ctx, "ak8_higgs_cand", 0.5, false))
                ));

    other_modules.emplace_back(new BTagSFJetCollectionProducer(ctx,
                "ak8_higgs_cand",
                "jets_no_overlap",
                "tj_btag_sf_coll"
                ));


    btag_sf_sr.reset(new MCBTagScaleFactor(ctx, CSVBTag::WP_MEDIUM, "ak8_higgs_cand"));
    btag_sf_cr.reset(new MCBTagScaleFactor(ctx, CSVBTag::WP_MEDIUM, "tj_btag_sf_coll"));


    // // =====CLEAN JETS BASED ON JULIES SCRIPT======
    // other_modules.emplace_back(new CollectionProducer<Jet>(ctx,
    //             "jets",
    //             "jets_pt_cleaned",
                // type == "MC" ? JetId(JetPtAndMultFixer<Jet>(1.09771, -0.000517529)) : JetId(TrueId<Jet>::is_true)
    //             ));
    // other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
    //             "topjets",
    //             "topjets_pt_cleaned",
                // type == "MC" ? TopJetId(JetPtAndMultFixer<TopJet>(1.10875, -0.000594446)) : TopJetId(TrueId<TopJet>::is_true)
    //             ));
    // other_modules.emplace_back(new STCalculator(ctx, "ST_cleaned",
    //     type == "MC" ? JetId(JetPtAndMultFixer<Jet>(1.09771, -0.000517529)) : JetId(TrueId<Jet>::is_true)
    //     ));


    // =====HIGGS TAGS AND STUFF======

    // higgs tags, with mass cuts
    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_higgs_cand",
                "higgs_tags_1b_med",
                TopJetId(HiggsFlexBTag(60., 150., CSVBTag(CSVBTag::WP_MEDIUM)))
                ));
    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_higgs_cand",
                "higgs_tags_2b_med",
                TopJetId(HiggsFlexBTag(60., 150., CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)))
                ));
    ak8jet_hists->add_level("Higgs_tags_1b_med", "higgs_tags_1b_med", vector<string>{"n", "pt", "eta", "mass_sj", "tau21",  "n_sjbtags-medium", "dRlepton", "dRak4", "dRak8"}, 1);
    ak8jet_hists->add_level("Higgs_tags_2b_med", "higgs_tags_2b_med", vector<string>{"n", "pt", "eta", "mass_sj", "tau21",  "n_sjbtags-medium", "dRlepton", "dRak4", "dRak8"}, 1);

    // =====HIGGS TAG QUANTITIES======

    // higgs-tags without pt cut
    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "topjets",
                "noboost_mass_1b",
                TopJetId(HiggsFlexBTag(60., 150., CSVBTag(CSVBTag::WP_MEDIUM)))
                ));
    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "topjets",
                "noboost_mass_2b",
                TopJetId(HiggsFlexBTag(60., 150., CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)))
                ));
    ak8jet_hists->add_level("Noboost_mass_1b", "noboost_mass_1b", vector<string>{"n", "pt", "mass_sj", "n_sjbtags-medium"}, 1);
    ak8jet_hists->add_level("Noboost_mass_2b", "noboost_mass_2b", vector<string>{"n", "pt", "mass_sj", "n_sjbtags-medium"}, 1);

    // higgs tags without mass cuts
    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost",
                "nomass_boost_1b",
                TopJetId(HiggsFlexBTag(0.,999999., CSVBTag(CSVBTag::WP_MEDIUM)))
                ));
    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost",
                "nomass_boost_2b",
                TopJetId(HiggsFlexBTag(0.,999999., CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)))
                ));
    ak8jet_hists->add_level("Nomass_boost_1b", "nomass_boost_1b", vector<string>{"n", "pt", "mass_sj", "n_sjbtags-medium"}, 1);
    ak8jet_hists->add_level("Nomass_boost_2b", "nomass_boost_2b", vector<string>{"n", "pt", "mass_sj", "n_sjbtags-medium"}, 1);

    // higgs tags without b-tag cuts
    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_higgs_cand",
                "nobtag_boost_mass",
                TopJetId(HiggsFlexBTag(60., 150.))
                ));
    ak8jet_hists->add_level("Nobtag_boost_mass", "nobtag_boost_mass", vector<string>{"n", "pt", "mass_sj", "n_sjbtags-medium", "n_sjbtags-loose"}, 1);
    

    // Handleproducer for cutting later on
    other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "higgs_tags_1b_med",
                "n_higgs_tags_1b_med"
                ));
    other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "higgs_tags_2b_med",
                "n_higgs_tags_2b_med"
                ));
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
    // other_modules.emplace_back(new MaxNSubjetBtagProducer(ctx,
    //             "ak8_higgs_cand",
    //             "max_n_subjet_btags",
    //             "higgs_cands_max_btag",
    //             CSVBTag(CSVBTag::WP_MEDIUM)
    //             ));
    // other_modules.emplace_back(new LdMassSjProducer(ctx,
    //             "higgs_cands_max_btag",
    //             "mass_higgs_cands_max_btag"
    //             ));

    // other_modules.emplace_back(new TopJetVarProducer(ctx,
    //             "topjets",
    //             "topjet",
    //             "PrimaryLepton",
    //             CSVBTag(CSVBTag::WP_MEDIUM)
    //             ));

    other_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_Mu45_eta2p1_v*"}, "trigger_accept_mu45"));
    other_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v*"}, {"HLT_Mu45_eta2p1_v*"}, "trigger_accept_el40"));
    if (type == "MC")
        other_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_IsoMu24_eta2p1_v*"}, "trigger_accept_isoMu"));
    else
        other_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_IsoMu27_v*"}, "trigger_accept_isoMu"));
    // other_modules.emplace_back(new PartPtProducer<Jet>(ctx, "jets", "pt_ld_ak4_jet", 1));
    // other_modules.emplace_back(new PartPtProducer<Jet>(ctx, "jets_pt_cleaned", "pt_ld_ak4_jet_cleaned", 1));
    // other_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "topjets", "pt_ld_ak8_jet", 1));
    // other_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "topjets_pt_cleaned", "pt_ld_ak8_jet_cleaned", 1));

    // other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
    //             "topjets",
    //             "n_ak8"
    //             ));
    // other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
    //             "topjets_pt_cleaned",
    //             "n_ak8_pt_cleaned"
    //             ));
    // other_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
    //             "jets",
    //             "n_ak4"
    //             ));
    // other_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
    //             "jets_pt_cleaned",
    //             "n_ak4_pt_cleaned"
    //             ));

    other_modules.emplace_back(new TopJetDeltaRProducer(ctx,
                "topjets",
                1
                ));
    other_modules.emplace_back(new TopJetDeltaRProducer(ctx,
                "topjets",
                2
                ));
    other_modules.emplace_back(new TopJetDeltaRProducer(ctx,
                "higgs_tags_1b_med",
                1
                ));
    other_modules.emplace_back(new TopJetDeltaRProducer(ctx,
                "higgs_tags_2b_med",
                1
                ));

    





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

        std::cout << "Category/split: " << cat << " " << split(cat, "-")[0] << std::endl;

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
            SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+2, new SelDatI("is_muon", "Prim Lep is Muon", 2, -.5, 1.5));
        }
        else if (split(cat, "-")[0] == "EleChannel") {
            SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+2, new SelDatI("is_muon", "Prim Lep is Muon", 2, -.5, 1.5, 0, 0));
        }
        else if (split(cat, "-")[0] == "MuonChannel") {
            SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+2, new SelDatI("is_muon", "Prim Lep is Muon", 2, -.5, 1.5, 1));
        }
        // else if (split(cat, "-")[0] == "HiggsTag0Med") {
        //     SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+2, new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 5, -.5, 4.5, 0, 0));
        //     SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+3, new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 8, -.5, 7.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+4, new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 5, -.5, 4.5));
        // }
        // else if (split(cat, "-")[0] == "HiggsTag1bMed") {
        //     // cut_collection = "higgs_tags_1b_med";
        //     SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+2, new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 5, -.5, 4.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+3, new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 5, -.5, 4.5, 0, 0));
        //     SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+4, new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 8, -.5, 7.5));
        // }
        // else if (split(cat, "-")[0] == "HiggsTag2bMed") {
        //     // cut_collection = "higgs_tags_2b_med";
        //     SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+2, new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 5, -.5, 4.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+3, new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 5, -.5, 4.5));
        //     SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+4, new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 8, -.5, 7.5));
        // }

        // gendecay_accept_hndl = ctx.get_handle<int>("gendecay_accept");

        // if (split(cat, "-")[0] == "NoSelection") 
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("gendecay_accept_"+fs, "GenDecay Accept", 2, -.5, 1.5));
        // else
        // SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("gendecay_accept", "GenDecay Accept", 2, -.5, 1.5, 1));


        // check for b tags that do not overlap with higgs tags
        // other_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
        //     "b_jets_medium",
        //     "n_additional_btags_medium",
        //     JetId(MinMaxDeltaRId<TopJet>(ctx, cut_collection, 0.6, false))
        //     ));

        // SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("min_dR_top_1_"+cut_collection, "min deltaR(top, higgs)", 20, 0, 5.));
        // SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("min_dR_top_2_"+cut_collection, "min deltaR(top, higgs)", 20, 0, 5.));
        // SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("min_dR_top_cleaned_1_"+cut_collection, "min deltaR(top, higgs) cleaned", 20, 0, 5.));
        // SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("min_dR_top_cleaned_2_"+cut_collection, "min deltaR(top, higgs) cleaned", 20, 0, 5.));
        // SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_cmstoptagsv2", "N(Top Tags)", 5, -.5, 4.5));
        // SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_cmstoptagsv2_dR_"+cut_collection, "N(Top Tags)", 5, -.5, 4.5));
        // SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatD("ST", "ST", 45, 0, 4500));
        // SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_muon_pt_noIso", "Primary Muon p_T", 90, 0., 900.));

        vector<string> item_names;
        for (auto const & seli : SEL_ITEMS_FULL_SEL.back()) 
            item_names.push_back(seli->name());

        sel_helpers.emplace_back(new SelItemsHelper(SEL_ITEMS_FULL_SEL.back(), ctx, item_names, "sel_accept", "sel_all_accepted"));
        // sel_helper.declare_items_for_output();
        sel_modules.emplace_back(new SelectionProducer(ctx, *sel_helpers.back()));

        // if (split(cat, "-")[0] == "HiggsTag0Med") {
        sel_helpers.back()->declare_items_for_output();
        // }
        // 3. Set up Hists classes:

        // TODO: set up and fill other histogram classes, e.g. your own HistCollector stuff

        v_hists.emplace_back(vector<unique_ptr<Hists>>());
        v_hists_after_sel.emplace_back(vector<unique_ptr<Hists>>());
        v_genhist_2h_after_sel.emplace_back(vector<unique_ptr<Hists>>());
        v_genhist_1h_after_sel.emplace_back(vector<unique_ptr<Hists>>());


        // auto nm1_hists = new Nm1SelHists(ctx, cat+"/Nm1Selection", *sel_helpers.back());
        auto cf_hists = new VLQ2HTCutflow(ctx, cat+"/Cutflow", *sel_helpers.back());

        map<string, SelectedSelHists*> selected_sel_hists;
        selected_sel_hists["NoDRCut"] = new SelectedSelHists(ctx, cat+"/NoDRCut", *sel_helpers.back(), {}, {"deltaRlep_topjets_1"});
        // selected_sel_hists["OnlyTopTagCut"] = new SelectedSelHists(ctx, cat+"/OnlyTopTagCut", *sel_helpers.back(), {"n_cmstoptagsv2"});
        // selected_sel_hists["OnlyNAk8JetsCut"] = new SelectedSelHists(ctx, cat+"/OnlyNAk8JetsCut", *sel_helpers.back(), {"n_ak8"});


        
        for (auto hist : selected_sel_hists) {
            // hist.second->insert_hist_and_sel(pos_2d_cut, new TwoDCutHist(ctx, cat+"/"+hist.first, "TwoDcut_Dr_noIso", "TwoDcut_Dpt_noIso", "twod_cut_hist_noIso"), "twoD_cut");
            // for (auto const & hist_helper : ak8jet_hists) {
            // hist.second->insert_additional_hist(ak8jet_hists->book_histograms(ctx, cat+"/"+hist.first));
            // }
            v_hists.back().emplace_back(hist.second);
        }

        // v_hists.back().emplace_back(nm1_hists);
        v_hists.back().emplace_back(cf_hists);
        if (split(cat, "-")[0] == "NoSelection") {
            // sel_helpers.back()->fill_hists_vector(v_hists.back(), cat+"/NoSelection");
            // v_hists.back().emplace_back(new OwnHistCollector(ctx, cat+"/NoSelection", type == "MC", CSVBTag(CSVBTag::WP_MEDIUM), {"ev", "jet"}));
            v_hists_after_sel.back().emplace_back(new BTagMCEfficiencyHists(ctx, cat+"/BTagMCEfficiencyHists", CSVBTag::WP_MEDIUM, "tj_btag_sf_coll"));
        }
        sel_helpers.back()->fill_hists_vector(v_hists_after_sel.back(), cat+"/PostSelection");
        // for (auto const & hist_helper : ak8jet_hists) {
        if (version.find("thth") != string::npos) {
            v_genhist_2h_after_sel.back().emplace_back(new HiggsGenHist(ctx, cat+"/PostSelection/HiggsGen2Higgs/HiggsGenAllAk8", "topjets", "2h"));
            v_genhist_2h_after_sel.back().emplace_back(new HiggsGenHist(ctx, cat+"/PostSelection/HiggsGen2Higgs/HiggsGenHiggsCands", "ak8_higgs_cand", "2h"));
            v_genhist_2h_after_sel.back().emplace_back(new HiggsGenHist(ctx, cat+"/PostSelection/HiggsGen2Higgs/HiggsGenHiggsTags1b", "higgs_tags_1b_med", "2h"));
            v_genhist_2h_after_sel.back().emplace_back(new HiggsGenHist(ctx, cat+"/PostSelection/HiggsGen2Higgs/HiggsGenHiggsTags2b", "higgs_tags_2b_med", "2h"));
        }
        if (version.find("thtz") != string::npos || version.find("thbw") != string::npos) {
            v_genhist_1h_after_sel.back().emplace_back(new HiggsGenHist(ctx, cat+"/PostSelection/HiggsGen1Higgs/HiggsGenAllAk8", "topjets", "1h"));
            v_genhist_1h_after_sel.back().emplace_back(new HiggsGenHist(ctx, cat+"/PostSelection/HiggsGen1Higgs/HiggsGenHiggsCands", "ak8_higgs_cand", "1h"));
            v_genhist_1h_after_sel.back().emplace_back(new HiggsGenHist(ctx, cat+"/PostSelection/HiggsGen1Higgs/HiggsGenHiggsTags1b", "higgs_tags_1b_med", "1h"));
            v_genhist_1h_after_sel.back().emplace_back(new HiggsGenHist(ctx, cat+"/PostSelection/HiggsGen1Higgs/HiggsGenHiggsTags2b", "higgs_tags_2b_med", "1h"));
        }
        v_hists_after_sel.back().emplace_back(ak8jet_hists->book_histograms(ctx, cat+"/PostSelection"));
        v_hists_after_sel.back().emplace_back(new OwnHistCollector(ctx, cat+"/PostSelection", type == "MC", CSVBTag(CSVBTag::WP_MEDIUM), {"ev", "jet", "cmstopjet"}));
        v_hists_after_sel.back().emplace_back(new JetCleaningControlPlots(ctx, cat+"/PostSelection/JetCleaningControlPlots", "ak4_jetpt_weight", "ak8_jetpt_weight"));
        v_hists_after_sel.back().emplace_back(new JetCleaningControlPlots(ctx, cat+"/PostSelection/JetCleaningControlPlotsUp", "ak4_jetpt_weight_up", "ak8_jetpt_weight"));
        v_hists_after_sel.back().emplace_back(new JetCleaningControlPlots(ctx, cat+"/PostSelection/JetCleaningControlPlotsDown", "ak4_jetpt_weight_down", "ak8_jetpt_weight"));

            // v_hists_after_sel.emplace_back(new HistCollector(ctx, "EventHistsPost"));

        // }
    }


}


bool TpTpFinalSelectionTreeOutput::process(Event & event) {

    common_module->process(event);

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

    }

    // all hists
    for (auto & hist_vec : v_hists) {
        for (auto & hist : hist_vec) {
            hist->fill(event);
        }
    }


    // if (sel_modules_passed[2] || sel_modules_passed[3]) {
    //     btag_sf_sr->process(event);
    //     event.set(use_sr_sf_hndl, 1);
    // }
    // else {
    // }
    btag_sf_cr->process(event);
    event.set(use_sr_sf_hndl, 0);

    for (unsigned i = 0; i < sel_modules.size(); ++i) {
    
        bool all_accepted = sel_modules_passed[i];
        if (all_accepted) {
            for (auto & hist : v_hists_after_sel[i]) {
                hist->fill(event);
            }
            if (version.find("thth") != string::npos) {
                for (auto & hist : v_genhist_2h_after_sel[i]) {
                    hist->fill(event);
                }   
            }
            if (version.find("thtz") != string::npos || version.find("thbw") != string::npos) {
                for (auto & hist : v_genhist_1h_after_sel[i]) {
                    hist->fill(event);
                }   
            }
        }

    }


    event.set(weight_hndl, event.weight);


    // run all modules
    // for (bool pass_sel : sel_modules_passed) {
    //     if (pass_sel) return true;
    // }

    return true;
}

UHH2_REGISTER_ANALYSIS_MODULE(TpTpFinalSelectionTreeOutput)
