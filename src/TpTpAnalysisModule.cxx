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
    // type = ctx.get("cycle_type", "PreSelection");
    
    // If running in SFrame, the keys "dataset_version", "dataset_type" and "dataset_lumi"
    // are set to the according values in the xml file. For CMSSW, these are
    // not set automatically, but can be set in the python config file.
    for(auto & kv : ctx.get_all()){
        cout << " " << kv.first << " = " << kv.second << endl;
    }

    common_modules.emplace_back(new PrimaryLepton(ctx, "PrimaryLepton", 9999.f, 10.f)); 
    common_modules.emplace_back(new PrimaryLeptonOwn<Muon>(ctx, "muons", "PrimaryMuon_noIso"));
    // common_modules.emplace_back(new PrimaryLeptonOwn<Muon>(ctx, "muons", "PrimaryMuon_dRak8", MuonId(MinMaxDeltaRId<TopJet>(ctx, "topjets", 0.1))));
    common_modules.emplace_back(new HTCalculator(ctx, boost::none, "HT"));
    common_modules.emplace_back(new STCalculator(ctx, "ST"));
    common_modules.emplace_back(new CollectionProducer<Jet>(ctx,
        "jets",
        "b_jets_loose",
        JetId(CSVBTag(CSVBTag::WP_LOOSE))
        ));
    common_modules.emplace_back(new CollectionProducer<Jet>(ctx,
        "jets",
        "b_jets_medium",
        JetId(CSVBTag(CSVBTag::WP_MEDIUM))
        ));
    common_modules.emplace_back(new CollectionProducer<Jet>(ctx,
        "jets",
        "b_jets_tight",
        JetId(CSVBTag(CSVBTag::WP_TIGHT))
        ));
    common_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
        "b_jets_loose",
        "n_btags_loose"
        // JetId(CSVBTag(CSVBTag::WP_LOOSE))
        ));
    common_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
        "b_jets_medium",
        "n_btags_medium"
        // JetId(CSVBTag(CSVBTag::WP_MEDIUM))
        ));
    common_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
        "b_jets_tight",
        "n_btags_tight"
        // JetId(CSVBTag(CSVBTag::WP_TIGHT))
        ));


    // Other CutProducers
    common_modules.emplace_back(new NLeptonsProducer(ctx, "n_leptons"));
    common_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx, "jets", "n_jets"));
    common_modules.emplace_back(new METProducer(ctx, "met"));
    common_modules.emplace_back(new PartPtProducer<Jet>(ctx, "jets", "leading_jet_pt", 1));
    common_modules.emplace_back(new PartPtProducer<Jet>(ctx, "jets", "subleading_jet_pt", 2));
    common_modules.emplace_back(new PartPtProducer<Muon>(ctx, "muons", "leading_mu_pt", 1));
    common_modules.emplace_back(new PartPtProducer<Electron>(ctx, "electrons", "leading_ele_pt", 1));

    // get pt of the top tagged jet with smallest pt, just to see if PtEtaCut Id is working
    // common_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "toptags", "smallest_pt_toptags", -1));

    common_modules.emplace_back(new PrimaryLeptonInfoProducer(ctx, "PrimaryLepton", "primary_lepton_pt"));
    common_modules.emplace_back(new PrimaryLeptonInfoProducer(ctx, "PrimaryMuon_noIso", "primary_muon_pt_noIso", "primary_muon_eta_noIso", "primary_muon_charge_noIso"));

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
