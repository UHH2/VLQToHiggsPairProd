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
    version = ctx.get("dataset_version", "");
    type = ctx.get("dataset_type", "");
    bool make_lep_coll = string2bool(ctx.get("make_lep_coll", "false"));
    double target_lumi = string2double(ctx.get("target_lumi"));
    // type = ctx.get("cycle_type", "PreSelection");

    if (version == "SingleEle_Run2015CD") {
        ctx.set("lumi_file", ctx.get("el_lumi_file", ctx.get("lumi_file")));
    } else if (version == "SingleMuon_Run2015CD") {
        ctx.set("lumi_file", ctx.get("mu_lumi_file", ctx.get("lumi_file")));
    }
    
    // If running in SFrame, the keys "dataset_version", "dataset_type" and "dataset_lumi"
    // are set to the according values in the xml file. For CMSSW, these are
    // not set automatically, but can be set in the python config file.
    for(auto & kv : ctx.get_all()){
        cout << " " << kv.first << " = " << kv.second << endl;
    }

    // pre_modules.emplace_back(new CollectionProducer<Muon>(ctx,
    //             "muons",
    //             "muons_tight"
    //             ));
    // pre_modules.emplace_back(new CollectionProducer<Electron>(ctx,
    //             "electrons",
    //             "electrons_tight"
    //             ));
    // pre_modules.emplace_back(new CollectionProducer<Electron>(ctx,
    //             "electrons",
    //             "electrons_mva_tight"
    //             ));
    if (make_lep_coll) {
        common_modules.emplace_back(new CollectionProducer<Electron>(ctx,
                    "electrons",
                    "electrons_mva_loose",
                    boost::none,
                    true
                    ));
        common_modules.emplace_back(new CollectionProducer<Electron>(ctx,
                    "electrons",
                    "electrons_iso",
                    boost::none
                    ));
        common_modules.emplace_back(new CollectionProducer<Muon>(ctx,
                    "muons",
                    "muons_iso",
                    boost::none
                    ));
    }


    common_modules.emplace_back(new ParticleCleaner<Electron>(ctx, AndId<Electron>(ElectronID_MVAnotrig_Spring15_25ns_loose, PtEtaCut(20.0, 2.4)), "electrons_mva_loose"));
    common_modules.emplace_back(new ParticleCleaner<Electron>(ctx, AndId<Electron>(ElectronID_Spring15_25ns_medium, PtEtaCut(20.0, 2.4)), "electrons_iso"));
    common_modules.emplace_back(new ParticleCleaner<Muon>(ctx, AndId<Muon>(MuonIDMedium(), MuonIso(), PtEtaCut(20.0, 2.1)), "muons_iso"));

    common_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_IsoMu20_v*", "HLT_IsoTkMu20_v*"}, "trigger_accept_isoMu20"));
    common_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_Ele27_eta2p1_WPLoose_Gsf_v*"}, "trigger_accept_isoEl27"));
    common_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_Mu45_eta2p1_v*"}, "trigger_accept_mu45"));
    common_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v*"}, "trigger_accept_el45"));
    common_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_Ele105_CaloIdVT_GsfTrkIdT_v*"}, "trigger_accept_el105"));
    common_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_Mu45_eta2p1_v*", "HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v*"}, "trigger_accept_lep_comb"));
    // common_modules.emplace_back(new PrimaryLepton(ctx, "PrimaryLeptonComb", 50., 47.));

    common_modules.emplace_back(new TriggerAwarePrimaryLepton(ctx, "PrimaryLepton", "trigger_accept_el45", "trigger_accept_mu45", 50., 47.));
    common_modules.emplace_back(new TriggerAwarePrimaryLepton(ctx, "PrimaryLeptonEl105", "trigger_accept_el105", "trigger_accept_mu45", "prim_ele_coll_el105", "prim_mu_coll_el105", 115., 47.));
    common_modules.emplace_back(new TriggerAwarePrimaryLepton(ctx, "PrimaryLeptonMVALoose", "trigger_accept_el45", "trigger_accept_mu45", "prim_ele_coll_mva_loose", "prim_ele_coll_mva_loose", 50., 47., "electrons_mva_loose", "muons"));
    common_modules.emplace_back(new TriggerAwarePrimaryLepton(ctx, "PrimaryLeptonIso", "trigger_accept_isoEl27", "trigger_accept_isoMu20", "prim_ele_coll_iso", "prim_mu_coll_iso", 40., 40., "electrons_iso", "muons_iso"));
    common_modules.emplace_back(new PrimaryLeptonOwn<Muon>(ctx, "muons", "PrimaryMuon"));
    common_modules.emplace_back(new PrimaryLeptonOwn<Muon>(ctx, "muons_iso", "PrimaryMuonIso"));
    common_modules.emplace_back(new PrimaryLeptonOwn<Electron>(ctx, "electrons", "PrimaryElectron"));
    common_modules.emplace_back(new PrimaryLeptonOwn<Electron>(ctx, "electrons_mva_loose", "PrimaryElectronMVALoose"));
    common_modules.emplace_back(new PrimaryLeptonOwn<Electron>(ctx, "electrons_iso", "PrimaryElectronIso"));

    common_modules.emplace_back(new TwoDCutProducer(ctx, "PrimaryLepton", "TwoDcut_Dr_noIso", "TwoDcut_Dpt_noIso", true));
    common_modules.emplace_back(new TwoDCutProducer(ctx, "PrimaryLeptonEl105", "TwoDcut_Dr_noIso_el105", "TwoDcut_Dpt_noIso_el105", true));
    common_modules.emplace_back(new TwoDCutProducer(ctx, "PrimaryLeptonMVALoose", "TwoDcut_Dr_noIso_mvaID", "TwoDcut_Dpt_noIso_mvaID", true));
    
    common_modules.emplace_back(new PrimaryLeptonPtProducer(ctx, "PrimaryLepton", "primary_lepton_pt"));
    common_modules.emplace_back(new PrimaryLeptonPtProducer(ctx, "PrimaryLeptonEl105", "primary_lepton_pt_el105"));
    common_modules.emplace_back(new PrimaryLeptonPtProducer(ctx, "PrimaryLeptonMVALoose", "primary_lepton_pt_mva_loose"));
    common_modules.emplace_back(new PrimaryLeptonPtProducer(ctx, "PrimaryLeptonIso", "primary_lepton_pt_iso"));
    common_modules.emplace_back(new PrimaryLeptonPtProducer(ctx, "PrimaryMuon", "primary_muon_pt"));
    common_modules.emplace_back(new PrimaryLeptonPtProducer(ctx, "PrimaryMuonIso", "primary_muon_pt_iso"));
    common_modules.emplace_back(new PrimaryLeptonPtProducer(ctx, "PrimaryElectron", "primary_electron_pt"));
    common_modules.emplace_back(new PrimaryLeptonPtProducer(ctx, "PrimaryElectronMVALoose", "primary_electron_pt_mva_loose"));
    common_modules.emplace_back(new PrimaryLeptonPtProducer(ctx, "PrimaryElectronIso", "primary_electron_pt_iso"));
    // common_modules.emplace_back(new PrimaryLeptonPtProducer(ctx, "PrimaryLeptonComb", "primary_lepton_comb_pt"));
    // keep the following module mainly for cross-checks, to see whether e.g. your primary lepton in the muon channel is really a muon
    common_modules.emplace_back(new PrimaryLeptonFlavInfo(ctx, "LeadingLepton", 50., 47., "is_muon"));
    // common_modules.emplace_back(new PrimaryLeptonFlavInfo(ctx, "LeadingLeptonEl105", 115., 47., "is_muon"));
    
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
    // common_modules.emplace_back(new PartPtProducer<Jet>(ctx, "jets", "pt_third_ak4_jet", 3));
    // common_modules.emplace_back(new PartPtProducer<Jet>(ctx, "jets", "pt_fourth_ak4_jet", 4));
    // common_modules.emplace_back(new PartPtProducer<Jet>(ctx, "jets", "pt_fifth_ak4_jet", 5));
    // common_modules.emplace_back(new PartPtProducer<Jet>(ctx, "jets", "pt_sixth_ak4_jet", 6));
    common_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "topjets", "pt_ld_ak8_jet", 1));
    // common_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "topjets", "pt_subld_ak8_jet", 2));
    // common_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "topjets", "pt_third_ak8_jet", 3));
    // common_modules.emplace_back(new PartPtProducer<Muon>(ctx, "muons", "leading_mu_pt", 1));
    // common_modules.emplace_back(new PartPtProducer<Electron>(ctx, "electrons", "leading_ele_pt", 1));
    if (type == "MC") {
        common_modules.emplace_back(new PartonHT(ctx.get_handle<double>("parton_ht")));
        common_modules.emplace_back(new GenHTCalculator(ctx, "gen_ht"));
    }
    // common_modules.emplace_back(new PrimaryLeptonPtProducer(ctx, "LeadingLepton", "leading_lepton_pt"));
    // common_modules.emplace_back(new PrimaryLeptonPtProducer(ctx, "PrimaryMuon_noIso", "primary_muon_pt_noIso"));

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
    // float jetsf_p0 = 1.09771;
    // float jetsf_p1 = -0.000517529;

    // // get error from covariance matrix, again, values are taken from Julie
    // float cov_p0_p0 = 0.0014795109823;
    // float cov_p0_p1 = -3.6104869696e-06;
    // float cov_p1_p1 = 9.89815635815e-09;

    // common_modules.emplace_back(new JetPtAndMultFixerWeight<Jet>(ctx, "jets", jetsf_p0, jetsf_p1, cov_p0_p0, cov_p0_p1, cov_p1_p1, "weight_ak4_jetpt"));
    // common_modules.emplace_back(new JetPtAndMultFixerWeight<Jet>(ctx, "jets", 1.13617, -0.000418040, "weight_ak4_jetpt_up"));
    // common_modules.emplace_back(new JetPtAndMultFixerWeight<Jet>(ctx, "jets", 1.05925, -0.000617018, "weight_ak4_jetpt_down"));

    // WHERE DID YOU GET THE VALUES BELOW FROM??
    // common_modules.emplace_back(new JetPtAndMultFixerWeight<TopJet>(ctx, "topjets", 1.10875, -0.000594446, "weight_ak8_jetpt"));
    

    if (type == "MC") {
        common_modules.emplace_back(new TriggerAwareEventWeight(ctx, "trigger_accept_el45", (target_lumi - 93)/target_lumi));
    }

    ak8jet_hists.reset(new NParticleMultiHistProducerHelper<TopJet>("FirstAk8SoftDropSlimmed", "topjets", vector<string>{"n", "pt", "eta", "phi", "mass_sj", "tau21", "n_subjets", "dRlepton", "dRak4", "dRak8"}));
    ak8jet_hists->add_level("SecondAk8SoftDropSlimmed", "topjets", vector<string>{"n", "pt", "eta", "phi", "mass_sj", "tau21", "n_subjets", "dRlepton", "dRak4", "dRak8"}, 2);

    // boosted Ak8 jets
    common_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "topjets",
                "ak8_boost",
                TopJetId(PtEtaCut(300., 2.4))
                ));
    common_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "topjets",
                "ak8_less_boost",
                TopJetId(PtEtaCut(200., 2.4))
                ));

    // =====HIGGS TAGS AND STUFF======

    // higgs tags, with mass cuts
    common_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost",
                "higgs_tags_1b_med",
                TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)))
                ));
    common_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost",
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
    
    // common_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
    //             "higgs_tags_1b_med",
    //             "n_higgs_tags_1b_med"
    //             ));
    // common_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
    //             "higgs_tags_2b_med",
    //             "n_higgs_tags_2b_med"
    //             ));

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


    common_modules.emplace_back(new CollectionSizeProducer<Muon>(ctx,
        "muons",
        "n_muons"
        ));
    common_modules.emplace_back(new CollectionSizeProducer<Muon>(ctx,
        "muons",
        "n_muons_iso",
        MuonId(MuonIso())
        ));
    common_modules.emplace_back(new CollectionSizeProducer<Electron>(ctx,
        "electrons",
        "n_electrons"
        ));
    common_modules.emplace_back(new CollectionSizeProducer<Electron>(ctx,
        "electrons",
        "n_electrons_iso",
        ElectronId(ElectronID_Spring15_25ns_medium)
        ));

    common_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
        "jets",
        "n_btags_tight",
        JetId(CSVBTag(CSVBTag::WP_TIGHT))
        ));

    common_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost",
                "ak8_higgs_cand",
                TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS))
                ));

    // ak4 jets not overlapping with higgs-candidates, collected together with higgs-candidates in one TopJet collection for applying b-tag scale factors
    common_modules.emplace_back(new CollectionProducer<Jet>(ctx,
                "jets",
                "jets_no_overlap",
                JetId(MinMaxDeltaRId<TopJet>(ctx, "ak8_higgs_cand", 0.8, false))
                ));

    common_modules.emplace_back(new BTagSFJetCollectionProducer(ctx,
                "ak8_higgs_cand",
                "jets_no_overlap",
                "tj_btag_sf_coll"
                ));


}


bool TpTpAnalysisModule::process(Event & event) {


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
