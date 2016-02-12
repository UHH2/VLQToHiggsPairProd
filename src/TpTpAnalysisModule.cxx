#include <iostream>
#include <memory>

#include "UHH2/VLQToHiggsPairProd/include/TpTpAnalysisModule.h"
#include "UHH2/common/test/TestJetLeptonCleaner.cpp"

using namespace std;
using namespace uhh2;   

TpTpAnalysisModule::TpTpAnalysisModule(Context & ctx) {
    // If needed, access the configuration of the module here, e.g.:
    // string testvalue = ctx.get("TestKey", "<not set>");
    // cout << "TestKey in the configuration was: " << testvalue << endl;
    version = ctx.get("dataset_version",}{} "");
    type = ctx.get("dataset_type", "");
    double target_lumi = string2double(ctx.get("target_lumi"));
    // type = ctx.get("cycle_type", "PreSelection");

    if (version == "Run2015D_Ele") {
        ctx.set("lumi_file", "/nfs/dust/cms/user/nowatsd/sFrameNew/RunII-25ns-v2/CMSSW_7_4_15_patch1/src/UHH2/common/data/Cert_246908-260627_13TeV_PromptReco_Collisions15_25ns_JSON_Silver_NoBadBSRuns.root");
    } else if (version == "Run2015D_Mu") {
        ctx.set("lumi_file", "/nfs/dust/cms/user/nowatsd/sFrameNew/RunII-25ns-v2/CMSSW_7_4_15_patch1/src/UHH2/common/data/Latest_2015_Silver_JSON.root");
    }
    
    // If running in SFrame, the keys "dataset_version", "dataset_type" and "dataset_lumi"
    // are set to the according values in the xml file. For CMSSW, these are
    // not set automatically, but can be set in the python config file.
    for(auto & kv : ctx.get_all()){
        cout << " " << kv.first << " = " << kv.second << endl;
    }

    common_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_IsoMu20_v*", "HLT_IsoTkMu20_v*"}, "trigger_accept_isoMu20"));
    if (type == "MC")
        common_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_Ele27_eta2p1_WP75_Gsf_v*"}, {"HLT_IsoMu20_v*", "HLT_IsoTkMu20_v*"}, "trigger_accept_isoEl27"));
        // common_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_IsoMu20_v*", "HLT_IsoTkMu20_v*"}, "trigger_accept_isoMu"));
    else
        common_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_Ele27_eta2p1_WPLoose_Gsf_v*"}, {"HLT_IsoMu20_v*", "HLT_IsoTkMu20_v*"}, "trigger_accept_isoEl27"));
        // common_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_IsoMu27_v*"}, "trigger_accept_isoMu"));
    common_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_Mu45_eta2p1_v*"}, "trigger_accept_mu45"));
    common_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v*"}, {"HLT_Mu45_eta2p1_v*"}, "trigger_accept_el45"));

    common_modules.emplace_back(new TriggerAwarePrimaryLepton(ctx, "PrimaryLepton", "trigger_accept_el45", "trigger_accept_mu45", 50., 47.));
    // keep the following module mainly for cross-checks, to see whether e.g. your primary lepton in the muon channel is really a muon
    common_modules.emplace_back(new PrimaryLeptonFlavInfo(ctx, "LeadingLepton", 50., 47., "is_muon"));
    // common_modules.emplace_back(new PrimaryLeptonOwn<Muon>(ctx, "muons", "PrimaryMuon_noIso"));
    // common_modules.emplace_back(new PrimaryLeptonOwn<Muon>(ctx, "muons", "PrimaryMuon_dRak8", MuonId(MinMaxDeltaRId<TopJet>(ctx, "topjets", 0.1))));
    common_modules.emplace_back(new HTCalculator(ctx, boost::none, "HT"));
    common_modules.emplace_back(new STCalculator(ctx, "ST"));
    common_modules.emplace_back(new NLeptonsProducer(ctx, "n_leptons"));
    common_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx, "jets", "n_ak4"));
    common_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx, "topjets", "n_ak8"));
    common_modules.emplace_back(new METProducer(ctx, "met"));
    common_modules.emplace_back(new PartPtProducer<Jet>(ctx, "jets", "pt_ld_ak4_jet", 1));
    common_modules.emplace_back(new PartPtProducer<Jet>(ctx, "jets", "pt_subld_ak4_jet", 2));
    common_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "topjets", "pt_ld_ak8_jet", 1));
    common_modules.emplace_back(new PartPtProducer<Muon>(ctx, "muons", "leading_mu_pt", 1));
    common_modules.emplace_back(new PartPtProducer<Electron>(ctx, "electrons", "leading_ele_pt", 1));
    common_modules.emplace_back(new PrimaryLeptonInfoProducer(ctx, "PrimaryLepton", "primary_lepton_pt", "primary_lepton_eta", "primary_lepton_charge"));
    // common_modules.emplace_back(new PrimaryLeptonInfoProducer(ctx, "LeadingLepton", "leading_lepton_pt", "leading_lepton_eta", "leading_lepton_charge"));
    // common_modules.emplace_back(new PrimaryLeptonInfoProducer(ctx, "PrimaryMuon_noIso", "primary_muon_pt_noIso", "primary_muon_eta_noIso", "primary_muon_charge_noIso"));

    // ====APPLY JULIES JET PT REWEIGHTING METHOD=====

    // values below taken from Julie, recaluculate them yourself?
    //////////////////////////////////////////
    /*
      Minimizer is Linear
      Chi2                      =      9.97134
      NDf                       =            9
      p0                        =      1.09771   +/-   0.0384644   
      p1                        = -0.000517529   +/-   9.94895e-05 
      covariance p0-p0 = 0.0014795109823
      covariance p0-p1 = -3.6104869696e-06
      covariance p1-p1 = 9.89815635815e-09
    */
    //////////////////////////////////////////
    float jetsf_p0 = 1.09771;
    float jetsf_p1 = -0.000517529;

    // get error from covariance matrix, again, values are taken from Julie
    float cov_p0_p0 = 0.0014795109823;
    float cov_p0_p1 = -3.6104869696e-06;
    float cov_p1_p1 = 9.89815635815e-09;

    common_modules.emplace_back(new JetPtAndMultFixerWeight<Jet>(ctx, "jets", jetsf_p0, jetsf_p1, cov_p0_p0, cov_p0_p1, cov_p1_p1, "weight_ak4_jetpt"));
    // common_modules.emplace_back(new JetPtAndMultFixerWeight<Jet>(ctx, "jets", 1.13617, -0.000418040, "weight_ak4_jetpt_up"));
    // common_modules.emplace_back(new JetPtAndMultFixerWeight<Jet>(ctx, "jets", 1.05925, -0.000617018, "weight_ak4_jetpt_down"));

    // WHERE DID YOU GET THE VALUES BELOW FROM??
    // common_modules.emplace_back(new JetPtAndMultFixerWeight<TopJet>(ctx, "topjets", 1.10875, -0.000594446, "weight_ak8_jetpt"));
    

    if (type == "MC") {
        common_modules.emplace_back(new TriggerAwareEventWeight(ctx, "trigger_accept_el45", (target_lumi - 86.)/target_lumi));
    }

    ak8jet_hists.reset(new NParticleMultiHistProducerHelper<TopJet>("FirstAk8SoftDropSlimmed", "topjets", vector<string>{"n", "pt", "eta", "phi", "mass_sj", "tau21", "n_subjets", "dRlepton", "dRak4", "dRak8"}));
    ak8jet_hists->add_level("SecondAk8SoftDropSlimmed", "topjets", vector<string>{"n", "pt", "eta", "phi", "mass_sj", "tau21", "n_subjets", "dRlepton", "dRak4", "dRak8"}, 2);

    // boosted Ak8 jets
    common_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "topjets",
                "ak8_boost",
                TopJetId(PtEtaCut(300., 2.4))
                ));

    // =====HIGGS TAGS AND STUFF======

    // higgs tags, with mass cuts
    common_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "topjets",
                "higgs_tags_1b_med",
                TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)))
                ));
    common_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "topjets",
                "higgs_tags_2b_med",
                TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)))
                ));
    ak8jet_hists->add_level("Higgs_tags_1b_med", "higgs_tags_1b_med", vector<string>{"n", "pt", "eta", "mass_sj", "tau21", "n_sjbtags-medium", "dRlepton", "dRak4", "dRak8"}, 1);
    ak8jet_hists->add_level("Higgs_tags_2b_med", "higgs_tags_2b_med", vector<string>{"n", "pt", "eta", "mass_sj", "tau21", "n_sjbtags-medium", "dRlepton", "dRak4", "dRak8"}, 1);

    // =====HIGGS TAG QUANTITIES======

    // higgs-tags without pt cut
    common_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "topjets",
                "noboost_mass_1b",
                TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)))
                ));
    common_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "topjets",
                "noboost_mass_2b",
                TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)))
                ));
    ak8jet_hists->add_level("Noboost_mass_1b", "noboost_mass_1b", vector<string>{"n", "pt", "mass_sj", "tau21", "n_sjbtags-medium"}, 1);
    ak8jet_hists->add_level("Noboost_mass_2b", "noboost_mass_2b", vector<string>{"n", "pt", "mass_sj", "tau21", "n_sjbtags-medium"}, 1);

    // higgs tags without mass cuts
    common_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost",
                "nomass_boost_1b",
                TopJetId(HiggsFlexBTag(0.,999999., CSVBTag(CSVBTag::WP_MEDIUM)))
                ));
    common_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost",
                "nomass_boost_2b",
                TopJetId(HiggsFlexBTag(0.,999999., CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)))
                ));
    ak8jet_hists->add_level("Nomass_boost_1b", "nomass_boost_1b", vector<string>{"n", "pt", "mass_sj", "tau21", "n_sjbtags-medium"}, 1);
    ak8jet_hists->add_level("Nomass_boost_2b", "nomass_boost_2b", vector<string>{"n", "pt", "mass_sj", "tau21", "n_sjbtags-medium"}, 1);

    // higgs tags without b-tag cuts
    common_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost",
                "nobtag_boost_mass",
                TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS))
                ));
    ak8jet_hists->add_level("Nobtag_boost_mass", "nobtag_boost_mass", vector<string>{"n", "pt", "mass_sj", "tau21", "n_sjbtags-loose", "n_sjbtags-medium"}, 1);
    
    common_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "higgs_tags_1b_med",
                "n_higgs_tags_1b_med"
                ));
    common_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "higgs_tags_2b_med",
                "n_higgs_tags_2b_med"
                ));

    common_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
        "jets",
        "n_btags_loose",
        JetId(CSVBTag(CSVBTag::WP_LOOSE))
        ));
    common_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
        "jets",
        "n_btags_medium",
        JetId(CSVBTag(CSVBTag::WP_MEDIUM))
        ));
    common_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
        "jets",
        "n_btags_tight",
        JetId(CSVBTag(CSVBTag::WP_TIGHT))
        ));

    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost",
                "ak8_higgs_cand",
                TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS))
                ));

    // ak4 jets not overlapping with higgs-candidates, collected together with higgs-candidates in one TopJet collection for applying b-tag scale factors
    other_modules.emplace_back(new CollectionProducer<Jet>(ctx,
                "jets",
                "jets_no_overlap",
                JetId(MinMaxDeltaRId<TopJet>(ctx, "ak8_higgs_cand", 0.8, false))
                ));

    other_modules.emplace_back(new BTagSFJetCollectionProducer(ctx,
                "ak8_higgs_cand",
                "jets_no_overlap",
                "tj_btag_sf_coll"
                ));


    // get pt of the top tagged jet with smallest pt, just to see if PtEtaCut Id is working
    // common_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "toptags", "smallest_pt_toptags", -1));

    // common_modules.emplace_back(new PrimaryLeptonInfoProducer(ctx, "PrimaryLepton", "primary_lepton_pt"));

    // class that takes care of applying CommonModules (with JEC, jet-lepton-cleaning, MCWeight etc.),
    // produces all handles for generic quantities like n_jets, met, etc.
    // tptp_commonModules.reset(new TpTpCommonModules(ctx));

    // EventWeightOutputHandle only needed for TMVA studies
    // other_common_modules.emplace_back(new EventWeightOutputHandle(ctx));

    // ========TEST STUFF HERE=======
    

    // pre_modules.emplace_back(new ElectronCleaner(AndId<Electron>(ElectronID_Spring15_25ns_medium_noIso,PtEtaCut(20.0, 2.4))));
    // pre_modules.emplace_back(new MuonCleaner(AndId<Muon>(MuonIDTight(),PtEtaCut(20.0, 2.1))));
    // pre_modules.emplace_back(new JetCleaner(ctx, AndId<Jet>(JetPFID(JetPFID::WP_LOOSE), PtEtaCut(30.0,2.4)), "jets"));
    // pre_modules.emplace_back(new TopJetCleaner(ctx, PtEtaCut(150., 2.4), "topjets"));
    // pre_modules.emplace_back(new TopJetCleaner(ctx, PtEtaCut(150., 2.4), "patJetsAk8CHSJetsSoftDropPacked_daughters"));

    // pre_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
    //             "jets",
    //             "n_ak4_before"
    //             ));
    // pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
    //             "topjets",
    //             "n_ak8_slimmed_before"
    //             ));
    // pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
    //             "patJetsAk8CHSJetsSoftDropPacked_daughters",
    //             "n_ak8_packed_before"
    //             ));
    // pre_modules.emplace_back(new PartPtProducer<Jet>(ctx, "jets", "pt_ld_ak4_jet_before", 1));
    // pre_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "topjets", "pt_ld_ak8_jet_slimmed_before", 1));
    // pre_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "patJetsAk8CHSJetsSoftDropPacked_daughters", "pt_ld_ak8_jet_packed_before", 1));

    // // pre_modules.emplace_back(new TestJetLeptonCleaner(ctx));

    // pre_modules.emplace_back(new JetLeptonCleaner_by_KEYmatching(ctx, JERFiles::Summer15_25ns_L123_AK8PFchs_MC, "jets"));
    // pre_modules.emplace_back(new JetLeptonCleaner_by_KEYmatching(ctx, JERFiles::Summer15_25ns_L123_AK8PFchs_MC, "topjets"));
    // pre_modules.emplace_back(new JetLeptonCleaner_by_KEYmatching(ctx, JERFiles::Summer15_25ns_L123_AK8PFchs_MC, "patJetsAk8CHSJetsSoftDropPacked_daughters"));

    // pre_modules.emplace_back(new JetCleaner(ctx, AndId<Jet>(JetPFID(JetPFID::WP_LOOSE), PtEtaCut(30.0,2.4)), "jets"));
    // pre_modules.emplace_back(new TopJetCleaner(ctx, PtEtaCut(150., 2.4), "topjets"));
    // pre_modules.emplace_back(new TopJetCleaner(ctx, PtEtaCut(150., 2.4), "patJetsAk8CHSJetsSoftDropPacked_daughters"));

    // patjets_ = ctx.get_handle<std::vector<TopJet>>("patJetsAk8CHSJetsSoftDropPacked_daughters");


    // common_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
    //             "jets",
    //             "n_ak4_after"
    //             ));
    // common_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
    //             "topjets",
    //             "n_ak8_slimmed_after"
    //             ));
    // common_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
    //             "patJetsAk8CHSJetsSoftDropPacked_daughters",
    //             "n_ak8_packed_after"
    //             ));
    // common_modules.emplace_back(new PartPtProducer<Jet>(ctx, "jets", "pt_ld_ak4_jet_after", 1));
    // common_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "topjets", "pt_ld_ak8_jet_slimmed_after", 1));
    // common_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "patJetsAk8CHSJetsSoftDropPacked_daughters", "pt_ld_ak8_jet_packed_after", 1));

    // const vector<shared_ptr<SelectionItem>> TEST_SEL {
    //     shared_ptr<SelectionItem>(new SelDatF("primary_muon_pt_noIso", "Primary Muon p_T", 90, 0., 900.)),
    //     // shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 8, -.5, 7.5, 3)),
    //     // shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 8, -.5,)),
    //     // shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 8, -.5, 7.5, 3)),
    //     // shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 8, -.5, 7.5, 3)),
    //     // shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak8_jet", "Pt leading Ak8 Jet", 60, 0., 1500., 300.))
    //     // shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak8_jet", "Pt leading Ak8 Jet", 60, 0., 1500., 300.))
    //     // shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak8_jet", "Pt leading Ak8 Jet", 60, 0., 1500., 300.))
    //     // shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak8_jet", "Pt leading Ak8 Jet", 60, 0., 1500., 300.))
    // };

    // SEL_ITEMS_FULL_SEL.push_back(TEST_SEL);
    // SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+1, new SelDatI("n_ak4_before", "N(Ak4 Jets)", 8, -.5, 7.5));
    // SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+2, new SelDatF("pt_ld_ak4_jet_before", "Pt leading Ak4 Jet", 60, 0., 1500., 100.));

    // vector<string> item_names;
    // for (auto const & seli : SEL_ITEMS_FULL_SEL.back()) 
    //     item_names.push_back(seli->name());    

    // sel_helpers.emplace_back(new SelItemsHelper(SEL_ITEMS_FULL_SEL.back(), ctx, item_names, "sel_accept", "sel_all_accepted"));
    // sel_modules.emplace_back(new SelectionProducer(ctx, *sel_helpers.back()));
    // v_hists_after_sel.emplace_back(vector<unique_ptr<Hists>>());
    // sel_helpers.back()->fill_hists_vector(v_hists_after_sel.back(), "Ak4Before");
    
    // SEL_ITEMS_FULL_SEL.push_back(TEST_SEL);
    // SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+1, new SelDatI("n_ak4_after", "N(Ak4 Jets)", 8, -.5, 7.5));
    // SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+2, new SelDatF("pt_ld_ak4_jet_after", "Pt leading Ak4 Jet", 60, 0., 1500., 100.));

    // item_names.clear();
    // for (auto const & seli : SEL_ITEMS_FULL_SEL.back()) 
    //     item_names.push_back(seli->name());

    // sel_helpers.emplace_back(new SelItemsHelper(SEL_ITEMS_FULL_SEL.back(), ctx, item_names, "sel_accept", "sel_all_accepted"));
    // sel_modules.emplace_back(new SelectionProducer(ctx, *sel_helpers.back()));
    // v_hists_after_sel.emplace_back(vector<unique_ptr<Hists>>());
    // sel_helpers.back()->fill_hists_vector(v_hists_after_sel.back(), "Ak4After");

    // SEL_ITEMS_FULL_SEL.push_back(TEST_SEL);
    // SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+1, new SelDatI("n_ak8_slimmed_before", "N(Ak8 Jets)", 8, -.5, 7.5, 3));
    // SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+2, new SelDatF("pt_ld_ak8_jet_slimmed_before", "Pt leading Ak8 Jet", 60, 0., 1500.));

    // item_names.clear();
    // for (auto const & seli : SEL_ITEMS_FULL_SEL.back()) 
    //     item_names.push_back(seli->name());    

    // sel_helpers.emplace_back(new SelItemsHelper(SEL_ITEMS_FULL_SEL.back(), ctx, item_names, "sel_accept", "sel_all_accepted"));
    // sel_modules.emplace_back(new SelectionProducer(ctx, *sel_helpers.back()));
    // v_hists_after_sel.emplace_back(vector<unique_ptr<Hists>>());
    // sel_helpers.back()->fill_hists_vector(v_hists_after_sel.back(), "SlimmedBefore");

    // SEL_ITEMS_FULL_SEL.push_back(TEST_SEL);
    // SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+1, new SelDatI("n_ak8_packed_before", "N(Ak8 Jets)", 8, -.5, 7.5, 3));
    // SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+2, new SelDatF("pt_ld_ak8_jet_packed_before", "Pt leading Ak8 Jet", 60, 0., 1500.));

    // item_names.clear();
    // for (auto const & seli : SEL_ITEMS_FULL_SEL.back()) 
    //     item_names.push_back(seli->name()); 

    // sel_helpers.emplace_back(new SelItemsHelper(SEL_ITEMS_FULL_SEL.back(), ctx, item_names, "sel_accept", "sel_all_accepted"));
    // sel_modules.emplace_back(new SelectionProducer(ctx, *sel_helpers.back()));
    // v_hists_after_sel.emplace_back(vector<unique_ptr<Hists>>());
    // sel_helpers.back()->fill_hists_vector(v_hists_after_sel.back(), "PackedBefore");
    
    // SEL_ITEMS_FULL_SEL.push_back(TEST_SEL);
    // SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+1, new SelDatI("n_ak8_slimmed_after", "N(Ak8 Jets)", 8, -.5, 7.5, 3));
    // SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+2, new SelDatF("pt_ld_ak8_jet_slimmed_after", "Pt leading Ak8 Jet", 60, 0., 1500.));

    // item_names.clear();
    // for (auto const & seli : SEL_ITEMS_FULL_SEL.back()) 
    //     item_names.push_back(seli->name());

    // sel_helpers.emplace_back(new SelItemsHelper(SEL_ITEMS_FULL_SEL.back(), ctx, item_names, "sel_accept", "sel_all_accepted"));
    // sel_modules.emplace_back(new SelectionProducer(ctx, *sel_helpers.back()));
    // v_hists_after_sel.emplace_back(vector<unique_ptr<Hists>>());
    // sel_helpers.back()->fill_hists_vector(v_hists_after_sel.back(), "SlimmedAfter");

    // SEL_ITEMS_FULL_SEL.push_back(TEST_SEL);
    // SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+1, new SelDatI("n_ak8_packed_after", "N(Ak8 Jets)", 8, -.5, 7.5, 3));
    // SEL_ITEMS_FULL_SEL.back().emplace(SEL_ITEMS_FULL_SEL.back().begin()+2, new SelDatF("pt_ld_ak8_jet_packed_after", "Pt leading Ak8 Jet", 60, 0., 1500.));

    // item_names.clear();
    // for (auto const & seli : SEL_ITEMS_FULL_SEL.back()) 
    //     item_names.push_back(seli->name());

    // sel_helpers.emplace_back(new SelItemsHelper(SEL_ITEMS_FULL_SEL.back(), ctx, item_names, "sel_accept", "sel_all_accepted"));
    // sel_modules.emplace_back(new SelectionProducer(ctx, *sel_helpers.back()));
    // v_hists_after_sel.emplace_back(vector<unique_ptr<Hists>>());
    // sel_helpers.back()->fill_hists_vector(v_hists_after_sel.back(), "PackedAfter");
}


bool TpTpAnalysisModule::process(Event & event) {

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

        // fill histograms
        if (all_accepted) {
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

    // fill histograms without selection
    // for (auto & hist : v_hists_nosel) {
    //     hist->fill(event);
    // }

    // decide whether or not to keep the current event in the output:
    return true;
}

UHH2_REGISTER_ANALYSIS_MODULE(TpTpAnalysisModule)
