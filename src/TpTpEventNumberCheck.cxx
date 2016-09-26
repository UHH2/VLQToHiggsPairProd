#include <iostream>
#include <fstream>
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


class TpTpEventNumberCheck: public TpTpAnalysisModule {
public:

    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_BASELINE_SEL {
        shared_ptr<SelectionItem>(new SelDatD("ST", "ST", 65, 0, 6500, 800.)),
        shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 10, -.5, 9.5, 2)),
        shared_ptr<SelectionItem>(new SelDatI("n_ak4", "N(Ak4 Jets)", 20, -.5, 19.5, 3)),
        shared_ptr<SelectionItem>(new SelDatI("n_additional_btags_medium", "N(AK4 b-tags)", 10, -.5, 9.5, 1)),
        shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_1b_med_sm10", "N(Higgs-Tags, 1 subjet b-tags)", 6, -.5, 5.5, 1)),
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
        shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_2b_med_sm10", "N(Higgs-Tags, 2 subjet b-tags)", 6, -.5, 5.5)),
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
        shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_2b_med_sm10", "N(Higgs-Tags, 2 subjet b-tags)", 6, -.5, 5.5)),
        // shared_ptr<SelectionItem>(new SelDatF("primary_electron_pt_tight", "Primary Lepton p_T", 100, 0., 1200.)),
        // shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 10, -.5, 9.5, 2)),
        };


    explicit TpTpEventNumberCheck(Context & ctx);
    ~TpTpEventNumberCheck();
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
    vector<unique_ptr<Hists>> v_lep_combined_hists;
    vector<string> categories;
    ofstream event_file;

};



TpTpEventNumberCheck::TpTpEventNumberCheck(Context & ctx) : TpTpAnalysisModule(ctx) {

    auto data_dir_path = ctx.get("data_dir_path");
    ctx.undeclare_all_event_output();
    // jetpt_weight_hndl = ctx.declare_event_output<float>("weight_ak4_jetpt");
    // ctx.declare_event_output<float>("weight_ak4_jetpt_up");
    // ctx.declare_event_output<float>("weight_ak4_jetpt_down");
    // ctx.declare_event_output<float>("weight_ak8_jetpt");
    ctx.declare_event_output<int>("run");
    ctx.declare_event_output<int>("luminosityBlock");
    ctx.declare_event_output<int>("event");

    ctx.declare_event_output<vector<TopJet>>("higgs_tags_1b_med");
    ctx.declare_event_output<vector<TopJet>>("higgs_tags_2b_med");
    ctx.declare_event_output<vector<TopJet>>("noboost_mass_1b");
    ctx.declare_event_output<vector<TopJet>>("noboost_mass_2b");
    ctx.declare_event_output<vector<TopJet>>("nomass_boost_1b");
    ctx.declare_event_output<vector<TopJet>>("nomass_boost_2b");
    // ctx.declare_event_output<vector<TopJet>>("nobtag_boost_mass");
    ctx.declare_event_output<vector<TopJet>>("ak8_higgs_cand");
    ctx.declare_event_output<vector<Jet>>("jets");
    ctx.declare_event_output<vector<TopJet>>("topjets");
    ctx.declare_event_output<FlavorParticle>("PrimaryLepton");
    if (version.find("TTbar_split") == string::npos) 
        ctx.declare_event_output<vector<Electron>>("electrons_mva_loose");
    // ctx.declare_event_output<FlavorParticle>("PrimaryMuon");
    // ctx.declare_event_output<FlavorParticle>("PrimaryElectron");
    // ctx.declare_event_output<vector<TopJet>>("ak8_boost");

    weight_hndl = ctx.declare_event_output<double>("weight");
    // use_sr_sf_hndl = ctx.declare_event_output<int>("use_sr_sf");
    // ctx.declare_event_output<std::vector<Jet>>("jets");
    // ctx.declare_event_output<std::vector<TopJet>>("ak8_boost");

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
    

    // Top-pt reweighting (see https://twiki.cern.ch/twiki/bin/view/CMS/TopPtReweighting#Eventweight):
    // a and b parameters from the 8 TeV l+jets channel (see twiki) are used, these are
    // a = 0.159, b = -0.00141
    // the overall event weight ratio between not applying and applying the top pt reweighting is
    // 9.910819e-01 = 0.9910819 as calculated with TpTpTTbarWeight.cxx
    // In the end, the overall weight that you apply thus needs to be multiplied by 1./0.9919819


    auto ak8_corr_bef = (type == "MC") ? JERFiles::Fall15_25ns_L23_AK8PFchs_MC 
    : JERFiles::Fall15_25ns_L23_AK8PFchs_DATA;
    auto ak8_corr_aft = (type == "MC") ? JERFiles::Fall15_25ns_L123_AK8PFchs_MC 
    : JERFiles::Fall15_25ns_L123_AK8PFchs_DATA;
    auto ak4_corr = (type == "MC") ? JERFiles::Fall15_25ns_L123_AK4PFchs_MC 
    : JERFiles::Fall15_25ns_L123_AK4PFchs_DATA;
    // if (ctx.get("jecsmear_direction", "nominal") != "nominal") {
    pre_modules.emplace_back(new GenericTopJetCorrector(ctx,
        ak8_corr_bef, "topjets"));
    pre_modules.emplace_back(new GenericSubJetCorrector(ctx,
        ak4_corr, "topjets"));
    pre_modules.emplace_back(new AK8SoftDropCorr(ctx, "topjets"));
    pre_modules.emplace_back(new GenericTopJetCorrector(ctx,
        ak8_corr_aft, "topjets"));
    pre_modules.emplace_back(new JetCorrector(ctx, ak4_corr));
    // }


    // btag_sf_sr.reset(new MCBTagScaleFactor(ctx, CSVBTag::WP_MEDIUM, "ak8_higgs_cand"));

    // DISABLE WHEN CALCULATING PRODUCING THE BTAG EFFICIENCY HISTS!
    bool create_btag_eff = string2bool(ctx.get("create_btag_eff", "false"));
    if (!create_btag_eff)
        other_modules.emplace_back(new MCBTagScaleFactor(ctx, CSVBTag::WP_MEDIUM, "tj_btag_sf_coll"));
        // btag_sf_cr.reset(new MCBTagScaleFactor(ctx, CSVBTag::WP_MEDIUM, "tj_btag_sf_coll"));



    other_modules.emplace_back(new HiggsMassSmear(ctx,
                "ak8_boost",
                false, false
                ));

    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost_sm10",
                "higgs_tags_1b_med_sm10",
                TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)))
                // true
                ));
    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost_sm10",
                "higgs_tags_2b_med_sm10",
                TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)))
                // true
                ));


    other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "ak8_higgs_cand",
                "n_ak8_higgs_cand"
                ));
    other_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
                "jets_no_overlap",
                "n_additional_btags_medium",
                JetId(CSVBTag(CSVBTag::WP_MEDIUM))
                ));
    // other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
    //             "wtags",
    //             "n_wtags"
    //             ));
    // other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
    //             "wtags_sm10",
    //             "n_wtags_sm10"
    //             ));
    // other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
    //             "wtags_sm20",
    //             "n_wtags_sm20"
    //             ));
    other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "higgs_tags_1b_med_sm10",
                "n_higgs_tags_1b_med_sm10"
                ));
    other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "higgs_tags_2b_med_sm10",
                "n_higgs_tags_2b_med_sm10"
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
        
    categories = split(ctx.get("category", ""));
    // std::vector<string> categories = {"CombinedElMu",
    //     "HiggsTag0Med-Control", //"HiggsTag0Med-Control-2Ak8", "HiggsTag0Med-Control-3Ak8", "HiggsTag0Med-Control-4Ak8", 
    //     "HiggsTag1bMed-Signal", //"HiggsTag1bMed-Signal-1addB", "HiggsTag1bMed-Signal-2addB", "HiggsTag1bMed-Signal-3addB",
    //     "HiggsTag2bMed-Signal", 
    //     }; // "CombinedElMu", "HiggsTag2bLoose-Signal", "AntiHiggsTagLoose-Control", "AntiHiggsTagMed-Control", "HiggsTag0Loose-Control", 

    // for (auto const & fs : final_states) {

    other_modules.emplace_back(new TrueFalseProducer(ctx, "chan_accept", false));

    for (auto const & cat : categories) {


        SEL_ITEMS_FULL_SEL.push_back(SEL_ITEMS_BASELINE_SEL);


        if (version.find("SingleEle") != string::npos && split(cat, "_")[0] == "Mu45") {
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("chan_accept", "GenDecay Accept", 2, -.5, 1.5, 1));
        }
        else if (version.find("SingleMuon") != string::npos && split(cat, "_")[0] == "El45") {
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("chan_accept", "GenDecay Accept", 2, -.5, 1.5, 1));
        }
        else {
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("chan_accept", "GenDecay Accept", 2, -.5, 1.5, 0));
        }




        if (split(cat, "_")[0] == "Mu45") {
            for (auto const & sel_item : SEL_ITEMS_Mu45_SEL)
                SEL_ITEMS_FULL_SEL.back().push_back(sel_item);
        }
        else if (split(cat, "_")[0] == "El45") {
            for (auto const & sel_item : SEL_ITEMS_EL45_SEL)
                SEL_ITEMS_FULL_SEL.back().push_back(sel_item);
        }

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
        // v_reweighted_hists_after_sel.emplace_back(vector<unique_ptr<Hists>>());
        // v_genhist_2h_after_sel.emplace_back(vector<unique_ptr<Hists>>());
        // v_genhist_1h_after_sel.emplace_back(vector<unique_ptr<Hists>>());


        auto nm1_hists = new Nm1SelHists(ctx, cat+"/Nm1Selection", *sel_helpers.back());
        auto cf_hists = new VLQ2HTCutflow(ctx, cat+"/Cutflow", *sel_helpers.back());

        map<string, SelectedSelHists*> selected_sel_hists;
        // selected_sel_hists["NoNAk8Cut"] = new SelectedSelHists(ctx, cat+"/NoNAk8Cut", *sel_helpers.back(), {}, {"n_ak8"});
        // selected_sel_hists["OnlyTopTagCut"] = new SelectedSelHists(ctx, cat+"/OnlyTopTagCut", *sel_helpers.back(), {"n_cmstoptagsv2"});
        // selected_sel_hists["OnlyNAk8JetsCut"] = new SelectedSelHists(ctx, cat+"/OnlyNAk8JetsCut", *sel_helpers.back(), {"n_ak8"});


        v_hists.back().emplace_back(nm1_hists);
        v_hists.back().emplace_back(cf_hists);
        sel_helpers.back()->fill_hists_vector(v_hists.back(), cat+"/NoSelection");
        sel_helpers.back()->fill_hists_vector(v_hists_after_sel.back(), cat+"/PostSelection");

        v_hists_after_sel.back().emplace_back(new ExtendedTopJetHists(ctx, cat+"/PostSelection/HTags", CSVBTag(CSVBTag::WP_MEDIUM), 2, "higgs_tags_1b_med"));

        // v_hists_after_sel.back().emplace_back(new ExtendedTopJetHists(ctx, cat+"/PostSelection/Ak8JetsUnCleaned", CSVBTag(CSVBTag::WP_MEDIUM), 2, "topjets"));
        // v_hists_after_sel.back().emplace_back(new ExtendedTopJetHists(ctx, cat+"/PostSelection/Ak8JetsCleaned", CSVBTag(CSVBTag::WP_MEDIUM), 2, "topjets_cleaned"));
        // v_reweighted_hists_after_sel.back().emplace_back(new OwnHistCollector(ctx, cat+"/PostSelectionReweighted", type == "MC", CSVBTag(CSVBTag::WP_MEDIUM), {"ev", "mu", "el", "jet", "lumi", "cmstopjet"}));
        // v_hists_after_sel.back().emplace_back(new JetCleaningControlPlots(ctx, cat+"/PostSelection/JetCleaningControlPlots", "weight_ak4_jetpt", "weight_ak8_jetpt"));
        // v_hists_after_sel.back().emplace_back(new JetCleaningControlPlots(ctx, cat+"/PostSelection/JetCleaningControlPlotsUp", "weight_ak4_jetpt_up"));
        // v_hists_after_sel.back().emplace_back(new JetCleaningControlPlots(ctx, cat+"/PostSelection/JetCleaningControlPlotsDown", "weight_ak4_jetpt_down"));

            // v_hists_after_sel.emplace_back(new HistCollector(ctx, "EventHistsPost"));

        // }
    }

    if (version.find("SingleEle") != string::npos)
        event_file.open("el_events.txt");
    else if (version.find("SingleMuon") != string::npos)
        event_file.open("mu_events.txt");


}


bool TpTpEventNumberCheck::process(Event & event) {

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

    // int base_el_ind = -1;
    // for (unsigned i = 0; i < categories.size(); ++i) {
    //     if (categories[i] == "El45_Baseline")
    //         base_el_ind = i;
    // }

    // index 0 corresponds to combined
    for (unsigned i = 0; i < sel_modules.size(); ++i) {
    
        bool all_accepted = sel_modules[i]->process(event);
        sel_modules_passed.push_back(all_accepted);
        if (all_accepted) {
            event_file << event.run << " " << event.luminosityBlock << " " << event.event << endl;
        }
        // if (categories[i] == "Mu45" && all_accepted) {
        //     event_file << event.run << " " << event.luminosityBlock << " " << event.event << endl;
        //     cout << "Mu45: " << event.run << " " << event.luminosityBlock << " " << event.event << endl;
        // }

    }

    // btag_sf_cr->process(event);
    
    // all hists
    for (auto & hist_vec : v_hists) {
        for (auto & hist : hist_vec) {
            hist->fill(event);
        }
    }
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

    // if (base_el_ind >= 0 && sel_modules_passed[base_el_ind]) {
    //     ele_trg_sf->process(event);
    // }
    // else
    //     ele_trg_nosf->process(event);


    if (write_out) {
        // ak8jet_hists->process(event);
        for (auto & hist : v_lep_combined_hists) {
            hist->fill(event);
        }
    }

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

    return write_out;
}

TpTpEventNumberCheck::~TpTpEventNumberCheck() {
    event_file.close();
}

UHH2_REGISTER_ANALYSIS_MODULE(TpTpEventNumberCheck)
