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
#include "UHH2/VLQToHiggsPairProd/include/VLQPair_selectionItems.h"
#include "UHH2/VLQToHiggsPairProd/include/VLQPair_additionalModules.h"
#include "UHH2/VLQToHiggsPairProd/include/VLQPair_additionalHists.h"
#include "UHH2/VLQToHiggsPairProd/include/VLQPair_triggerPaths.h"

using namespace std;
using namespace uhh2;

using namespace vlqToHiggsPair;

typedef VectorAndSelection MyAndSelection;

class TpTpControlRegion: public AnalysisModule {
public:

    explicit TpTpControlRegion(Context & ctx);
    virtual bool process(Event & event);

private:

    void swap_selitems(vector<shared_ptr<SelectionItem>> & sel_items,
                       SelectionItem * new_item, int new_pos = -1) {
        unsigned insert_pos = new_pos >= 0 ? new_pos : 0;
        for (unsigned i = 0; i < sel_items.size(); ++i) {
            if (sel_items[i]->name() == new_item->name()) {
                sel_items.erase(sel_items.begin()+i);
                insert_pos = new_pos >= 0 ? new_pos : i;
            }
        }
        sel_items.insert(sel_items.begin()+insert_pos, shared_ptr<SelectionItem>(move(new_item)));
    }

    string version, type;
    // modules for setting up collections and cleaning
    vector<unique_ptr<AnalysisModule>> v_pre_modules;
    vector<unique_ptr<AnalysisModule>> sel_modules;
    vector<unique_ptr<SelItemsHelper>> sel_helpers;
    // unique_ptr<AnalysisModule> writer_module; // for TMVA stuff

    // store the Hists collection
    unique_ptr<Hists> gen_hists;
    vector<unique_ptr<Hists>> v_hists_nosel;
    vector<vector<unique_ptr<Hists>>> v_hists;
    vector<vector<unique_ptr<Hists>>> v_hists_after_sel;

    vector<vector<shared_ptr<SelectionItem>>> SEL_ITEMS_controlregion_vec;

    // check category
    // unique_ptr<Selection> cat_check_module;

    // Event::Handle<int> h_ngenleps;
};




TpTpControlRegion::TpTpControlRegion(Context & ctx) {

    const float MIN_HIGGS_MASS = 60.f;
    const float MAX_HIGGS_MASS = 150.f;


    // If needed, access the configuration of the module here, e.g.:
    // string testvalue = ctx.get("TestKey", "<not set>");
    // cout << "TestKey in the configuration was: " << testvalue << endl;
    version = ctx.get("dataset_version", "");
    type = ctx.get("dataset_type", "");
    
    // If running in SFrame, the keys "dataset_version", "dataset_type" and "dataset_lumi"
    // are set to the according values in the xml file. For CMSSW, these are
    // not set automatically, but can be set in the python config file.
    for(auto & kv : ctx.get_all()){
        cout << " " << kv.first << " = " << kv.second << endl;
    }
    
    // 1. setup modules to prepare the event.

    // EventWeightOutputHandle only needed for TMVA studies
    // v_pre_modules.emplace_back(new EventWeightOutputHandle(ctx));

    CommonModules* commonObjectCleaning = new CommonModules();
    // commonObjectCleaning->set_jet_id(PtEtaCut(30.0,2.4));
    commonObjectCleaning->disable_jersmear();
    // commonObjectCleaning->set_electron_id(AndId<Electron>(ElectronID_PHYS14_25ns_medium_noIso,PtEtaCut(20.0, 2.4)));
    // commonObjectCleaning->set_muon_id(AndId<Muon>(MuonIDTight(),PtEtaCut(20.0, 2.4)));
    // commonObjectCleaning->switch_jetlepcleaner(true);
    // commonObjectCleaning->switch_jetPtSorter(true);
    commonObjectCleaning->init(ctx);
    v_pre_modules.emplace_back(commonObjectCleaning);


    v_pre_modules.emplace_back(new PrimaryLepton(ctx, "PrimaryLepton", 9999.f, 50.f)); 
    v_pre_modules.emplace_back(new HTCalculator(ctx, boost::none, "HT"));
    v_pre_modules.emplace_back(new STCalculator(ctx, "ST"));
    v_pre_modules.emplace_back(new CollectionProducer<Jet>(ctx,
                "jets",
                "b_jets",
                JetId(CSVBTag(CSVBTag::WP_MEDIUM))
                ));
    v_pre_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
                "jets",
                "n_btags_loose",
                JetId(CSVBTag(CSVBTag::WP_LOOSE))
                ));
    v_pre_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
                "jets",
                "n_btags_medium",
                JetId(CSVBTag(CSVBTag::WP_MEDIUM))
                ));
    v_pre_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
                "jets",
                "n_btags_tight",
                JetId(CSVBTag(CSVBTag::WP_TIGHT))
                ));

    // cms top tags
    v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "topjets",
                "toptags",
                TopJetId(AndId<TopJet>(PtEtaCut(400., 2.4), CMSTopTag()))
                ));

    // check if there is exactly 1 Top Tag; if yes, make sure that all higgs tags are
    // well separated from it by making a dR requirement of 1.5
    v_pre_modules.emplace_back(new XTopTagProducer(ctx, "toptags", "min_dr_higgs", "one_top", 1.5, 1));
    v_pre_modules.emplace_back(new XTopTagProducer(ctx, "toptags", "dummy_dr", "two_top", -999., 2));

    // Other CutProducers
    v_pre_modules.emplace_back(new NLeptonsProducer(ctx, "n_leptons"));
    v_pre_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx, "jets", "n_jets"));
    v_pre_modules.emplace_back(new METProducer(ctx, "met"));
    v_pre_modules.emplace_back(new PartPtProducer<Jet>(ctx, "jets", "leading_jet_pt", 1));
    v_pre_modules.emplace_back(new PartPtProducer<Jet>(ctx, "jets", "subleading_jet_pt", 2));
    v_pre_modules.emplace_back(new PartPtProducer<Muon>(ctx, "muons", "leading_mu_pt", 1));
    v_pre_modules.emplace_back(new PartPtProducer<Electron>(ctx, "electrons", "leading_ele_pt", 1));
    // v_pre_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "topjets", "leading_topjet_pt", 1));
    // v_pre_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "patJetsAk8CHSJetsSoftDropPacked_daughters", "leading_ak8jet_pt", 1));
    // v_pre_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "patJetsCa15CHSJetsFilteredPacked_daughters", "leading_ca15jet_pt", 1));

    // get pt of the top tagged jet with smallest pt, just to see if PtEtaCut Id is working
    v_pre_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "toptags", "smallest_pt_toptags", -1));

    v_pre_modules.emplace_back(new LeptonPtProducer(ctx, "PrimaryLepton", "primary_lepton_pt"));
    v_pre_modules.emplace_back(new TwoDCutProducer(ctx));
    if (version == "Run2015D_Mu") {
        v_pre_modules.emplace_back(new TriggerAcceptProducer(ctx, QCDTEST_MUON_TRIGGER_PATHS_DATA, "trigger_accept"));
    } else if (version == "Run2015D_Ele") {
        v_pre_modules.emplace_back(new TriggerAcceptProducer(ctx, {}, "trigger_accept"));
    } else if (version == "Run2015D_Had") {
        v_pre_modules.emplace_back(new TriggerAcceptProducer(ctx, {}, "trigger_accept"));
    } else {
        v_pre_modules.emplace_back(new TriggerAcceptProducer(ctx, QCDTEST_MUON_TRIGGER_PATHS, "trigger_accept"));
    }

    vector<shared_ptr<SelectionItem>> SEL_ITEMS_VLQPair_control = SEL_ITEMS_VLQPair_final_base;

    unsigned insert_sel = 12;

    // make_modules_and_selitem("patJetsCa15CHSJetsFilteredPacked_daughters", ctx, v_pre_modules, SEL_ITEMS_VLQPair_control, insert_sel);
    make_modules_and_selitem("toptags", ctx, v_pre_modules, SEL_ITEMS_VLQPair_control, insert_sel, -1, true);
    make_modules_and_selitem("topjets", ctx, v_pre_modules, SEL_ITEMS_VLQPair_control, insert_sel, -1, true);
    make_modules_and_selitem("patJetsAk8CHSJetsSoftDropPacked_daughters", ctx, v_pre_modules, SEL_ITEMS_VLQPair_control, insert_sel, -1, true);


    v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "patJetsAk8CHSJetsSoftDropPacked_daughters",
                "ak8_boost",
                TopJetId(PtEtaCut(300., 2.4))
                ));

    for (string coll_name : {"patJetsAk8CHSJetsSoftDropPacked_daughters", "ak8_boost"}) {
        const string & out_name = switch_names(coll_name);
        v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
            coll_name,
            out_name+"_med_2b",
            TopJetId(HiggsTag(0., 99999.f, CSVBTag(CSVBTag::WP_MEDIUM)))
            ));
        v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
            coll_name,
            out_name+"_loose_2b",
            TopJetId(HiggsTag(0., 99999.f, CSVBTag(CSVBTag::WP_LOOSE)))
            ));
        v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
            coll_name,
            out_name+"_med_ex1b",
            TopJetId(AntiHiggsBVetoTag(0., 99999.f, CSVBTag(CSVBTag::WP_MEDIUM)))
            ));
        v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
            coll_name,
            out_name+"_loose_ex1b",
            TopJetId(AntiHiggsBVetoTag(0., 99999.f, CSVBTag(CSVBTag::WP_LOOSE)))
            ));
        v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
            coll_name,
            out_name+"_med_min1b",
            TopJetId(HiggsXBTag(0., 99999.f, CSVBTag(CSVBTag::WP_MEDIUM), 1))
            ));
        v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
            coll_name,
            out_name+"_loose_min1b",
            TopJetId(HiggsXBTag(0., 99999.f, CSVBTag(CSVBTag::WP_LOOSE), 1))
            ));
        v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
            coll_name,
            out_name+"_med_0b_m150_noT",
            TopJetId(AndId<TopJet>(
                HiggsXBTag(MAX_HIGGS_MASS, 99999.f, CSVBTag(CSVBTag::WP_MEDIUM), 0),
                MinMaxDeltaRId<TopJet>(ctx, "toptags", "min_dr_higgs"))
            )));
        v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
            coll_name,
            out_name+"_loose_0b_m150_noT",
            TopJetId(AndId<TopJet>(
                HiggsXBTag(MAX_HIGGS_MASS, 99999.f, CSVBTag(CSVBTag::WP_LOOSE), 0),
                MinMaxDeltaRId<TopJet>(ctx, "toptags", "min_dr_higgs"))
            )));
        make_modules_and_selitem(coll_name, ctx, v_pre_modules, SEL_ITEMS_VLQPair_control, insert_sel);
        make_modules_and_selitem(out_name+"_med_2b", ctx, v_pre_modules, SEL_ITEMS_VLQPair_control, insert_sel);
        make_modules_and_selitem(out_name+"_loose_2b", ctx, v_pre_modules, SEL_ITEMS_VLQPair_control, insert_sel);
        make_modules_and_selitem(out_name+"_med_ex1b", ctx, v_pre_modules, SEL_ITEMS_VLQPair_control, insert_sel);
        make_modules_and_selitem(out_name+"_loose_ex1b", ctx, v_pre_modules, SEL_ITEMS_VLQPair_control, insert_sel);
        make_modules_and_selitem(out_name+"_med_min1b", ctx, v_pre_modules, SEL_ITEMS_VLQPair_control, insert_sel);
        make_modules_and_selitem(out_name+"_loose_min1b", ctx, v_pre_modules, SEL_ITEMS_VLQPair_control, insert_sel);
        make_modules_and_selitem(out_name+"_med_0b_m150_noT", ctx, v_pre_modules, SEL_ITEMS_VLQPair_control, insert_sel);
        make_modules_and_selitem(out_name+"_loose_0b_m150_noT", ctx, v_pre_modules, SEL_ITEMS_VLQPair_control, insert_sel);
        for (string coll_name2 : {
            out_name+"_med_2b", out_name+"_loose_2b",
            out_name+"_med_ex1b", out_name+"_loose_ex1b",
            out_name+"_med_min1b", out_name+"_loose_min1b",
            }) {
            v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                coll_name2,
                coll_name2+"_m60-150",
                TopJetId(HiggsXBTag(MIN_HIGGS_MASS, MAX_HIGGS_MASS, CSVBTag(CSVBTag::WP_LOOSE), 0))
                ));
            v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                coll_name2+"_m60-150",
                coll_name2+"_m60-150_noT",
                TopJetId(MinMaxDeltaRId<TopJet>(ctx, "toptags", "min_dr_higgs"))
                ));
            v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                coll_name2,
                coll_name2+"_m150",
                TopJetId(HiggsXBTag(MAX_HIGGS_MASS, 99999.f, CSVBTag(CSVBTag::WP_LOOSE), 0))
                ));
            v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                coll_name2+"_m150",
                coll_name2+"_m150_noT",
                TopJetId(MinMaxDeltaRId<TopJet>(ctx, "toptags", "min_dr_higgs"))
                ));
            make_modules_and_selitem(coll_name2+"_m60-150", ctx, v_pre_modules, SEL_ITEMS_VLQPair_control, insert_sel);
            make_modules_and_selitem(coll_name2+"_m60-150_noT", ctx, v_pre_modules, SEL_ITEMS_VLQPair_control, insert_sel);
            make_modules_and_selitem(coll_name2+"_m150", ctx, v_pre_modules, SEL_ITEMS_VLQPair_control, insert_sel);
            make_modules_and_selitem(coll_name2+"_m150_noT", ctx, v_pre_modules, SEL_ITEMS_VLQPair_control, insert_sel);
        }

    }


    // check if, in case there is only one top, the dR to the closest higgs is really 1.5
    v_pre_modules.emplace_back(new MinDeltaRProducer<TopJet, TopJet>(ctx, "one_top", "ak8_boost_loose_2b_m60-150_noT", "min_deltaR_top_higgs_ak8_noT"));
    v_pre_modules.emplace_back(new MinDeltaRProducer<TopJet, TopJet>(ctx, "one_top", "ak8_boost_loose_2b_m60-150", "min_deltaR_top_higgs_ak8"));
    v_pre_modules.emplace_back(new MinDeltaRProducer<TopJet, TopJet>(ctx, "two_top", "ak8_boost_loose_2b_m60-150_noT", "min_deltaR_top_higgs_ak8_noT_twotop"));
    v_pre_modules.emplace_back(new MinDeltaRProducer<TopJet, TopJet>(ctx, "two_top", "ak8_boost_loose_2b_m60-150", "min_deltaR_top_higgs_ak8_twotop"));


        // } else if (cat == "BVetoLdJetBoost") {
    

    // additional b-tags
    v_pre_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
                "b_jets",
                "n_additional_btags",
                JetId(AndId<Jet>(MinMaxDeltaRId<TopJet>(ctx, "ak8_all_loose_2b_m60-150_noT", 1.0, true),
                                    MinMaxDeltaRId<TopJet>(ctx, "toptags", 1.0, true)))
                ));



    // general selections here where sel_item was added within this file
    // ++++++TO DO: put them in to VLQPair_selectionItems again and modify
    // your make_modules_and_selitem function so that it doesn't add already
    // existing SelItems again
    
    int insert_cut = 3;

    // swap_selitems(SEL_ITEMS_VLQPair_control, new SelDatF("leading_jet_pt", "leading jet p_{T}", 15, 0, 1500, 200.), insert_cut++);
    // swap_selitems(SEL_ITEMS_VLQPair_control, new SelDatI("n_ak8_all", "N_ak8_all", 11, -.5, 10.5, 3), insert_cut++);
    // swap_selitems(SEL_ITEMS_VLQPair_control, new SelDatI("n_toptags", "N_toptags", 11, -.5, 10.5, 1), insert_cut++);

    // produce more plots for the collections you cut on
    make_modules_and_selitem("ak8_boost_loose_2b_m60-150_noT", ctx, v_pre_modules, SEL_ITEMS_VLQPair_control, insert_sel, -1, true);
    make_modules_and_selitem("ak8_boost_loose_ex1b_m60-150_noT", ctx, v_pre_modules, SEL_ITEMS_VLQPair_control, insert_sel, -1, true);
    make_modules_and_selitem("ak8_boost_loose_min1b_m150_noT", ctx, v_pre_modules, SEL_ITEMS_VLQPair_control, insert_sel, -1, true);
    make_modules_and_selitem("ak8_boost_loose_0b_m150_noT", ctx, v_pre_modules, SEL_ITEMS_VLQPair_control, insert_sel, -1, true);
    make_modules_and_selitem("ak8_boost_med_2b_m60-150_noT", ctx, v_pre_modules, SEL_ITEMS_VLQPair_control, insert_sel, -1, true);
    make_modules_and_selitem("ak8_boost_med_ex1b_m60-150_noT", ctx, v_pre_modules, SEL_ITEMS_VLQPair_control, insert_sel, -1, true);
    make_modules_and_selitem("ak8_boost_med_min1b_m150_noT", ctx, v_pre_modules, SEL_ITEMS_VLQPair_control, insert_sel, -1, true);
    make_modules_and_selitem("ak8_boost_med_0b_m150_noT", ctx, v_pre_modules, SEL_ITEMS_VLQPair_control, insert_sel, -1, true);

    
    vector<string> categories = split(ctx.get("category", ""));

    for (auto const & cat : categories) {
        SEL_ITEMS_controlregion_vec.push_back(SEL_ITEMS_VLQPair_control);

        int insert_new = insert_cut;

        // if (cat == "ControlRegionBVeto") {
        //     swap_selitems(SEL_ITEMS_controlregion_vec.back(), new SelDatI("n_ak8_all_loose_2b_m60-150_noT", "N_ak8_all_loose_2b_m60-150_noT", 11, -.5, 10.5, 0, 0), insert_new++);
        //     swap_selitems(SEL_ITEMS_controlregion_vec.back(), new SelDatI("n_ak8_all_loose_ex1b_m60-150_noT", "N_ak8_all_loose_ex1b_m60-150_noT", 11, -.5, 10.5, 1), insert_new++);
        // } else
        if (cat == "ControlRegionBVetoBoostLoose") {
            swap_selitems(SEL_ITEMS_controlregion_vec.back(), new SelDatI("n_ak8_boost_loose_2b_m60-150_noT", "N_ak8_boost_loose_2b_m60-150_noT", 11, -.5, 10.5, 0, 0), insert_new++);
            swap_selitems(SEL_ITEMS_controlregion_vec.back(), new SelDatI("n_ak8_boost_loose_ex1b_m60-150_noT", "N_ak8_boost_loose_ex1b_m60-150_noT", 11, -.5, 10.5, 1), insert_new++);
        } else if (cat == "ControlRegionMassInvert1BTagBoostLoose") {
            swap_selitems(SEL_ITEMS_controlregion_vec.back(), new SelDatI("n_ak8_boost_loose_2b_m60-150_noT", "N_ak8_boost_loose_2b_m60-150_noT", 11, -.5, 10.5, 0, 0), insert_new++);
            swap_selitems(SEL_ITEMS_controlregion_vec.back(), new SelDatI("n_ak8_boost_loose_min1b_m150_noT", "N_ak8_boost_loose_min1b_m150_noT", 11, -.5, 10.5, 1), insert_new++);
        } else if (cat == "ControlRegionMassInvert0BTagBoostLoose") {
            swap_selitems(SEL_ITEMS_controlregion_vec.back(), new SelDatI("n_ak8_boost_loose_2b_m60-150_noT", "N_ak8_boost_loose_2b_m60-150_noT", 11, -.5, 10.5, 0, 0), insert_new++);
            swap_selitems(SEL_ITEMS_controlregion_vec.back(), new SelDatI("n_ak8_boost_loose_0b_m150_noT", "N_ak8_boost_loose_0b_m150_noT", 11, -.5, 10.5, 1), insert_new++);
        } else if (cat == "ControlRegionBVetoBoostMed") {
            swap_selitems(SEL_ITEMS_controlregion_vec.back(), new SelDatI("n_ak8_boost_med_2b_m60-150_noT", "N_ak8_boost_med_2b_m60-150_noT", 11, -.5, 10.5, 0, 0), insert_new++);
            swap_selitems(SEL_ITEMS_controlregion_vec.back(), new SelDatI("n_ak8_boost_med_ex1b_m60-150_noT", "N_ak8_boost_med_ex1b_m60-150_noT", 11, -.5, 10.5, 1), insert_new++);
        } else if (cat == "ControlRegionMassInvert1BTagBoostMed") {
            swap_selitems(SEL_ITEMS_controlregion_vec.back(), new SelDatI("n_ak8_boost_med_2b_m60-150_noT", "N_ak8_boost_med_2b_m60-150_noT", 11, -.5, 10.5, 0, 0), insert_new++);
            swap_selitems(SEL_ITEMS_controlregion_vec.back(), new SelDatI("n_ak8_boost_med_min1b_m150_noT", "N_ak8_boost_med_min1b_m150_noT", 11, -.5, 10.5, 1), insert_new++);
        } else if (cat == "ControlRegionMassInvert0BTagBoostMed") {
            swap_selitems(SEL_ITEMS_controlregion_vec.back(), new SelDatI("n_ak8_boost_med_2b_m60-150_noT", "N_ak8_boost_med_2b_m60-150_noT", 11, -.5, 10.5, 0, 0), insert_new++);
            swap_selitems(SEL_ITEMS_controlregion_vec.back(), new SelDatI("n_ak8_boost_med_0b_m150_noT", "N_ak8_boost_med_0b_m150_noT", 11, -.5, 10.5, 1), insert_new++);
        // } else if (cat == "ControlRegionMassInvert1BTag") {
        //     swap_selitems(SEL_ITEMS_controlregion_vec.back(), new SelDatI("n_ak8_all_loose_2b_m60-150_noT", "N_ak8_all_loose_2b_m60-150_noT", 11, -.5, 10.5, 0, 0), insert_new++);
        //     swap_selitems(SEL_ITEMS_controlregion_vec.back(), new SelDatI("n_ak8_all_loose_min1b_m150_noT", "N_ak8_all_loose_min1b_m150_noT", 11, -.5, 10.5, 1), insert_new++);
        // } else if (cat == "ControlRegionMassInvert0BTag") {
        //     swap_selitems(SEL_ITEMS_controlregion_vec.back(), new SelDatI("n_ak8_all_loose_2b_m60-150_noT", "N_ak8_all_loose_2b_m60-150_noT", 11, -.5, 10.5, 0, 0), insert_new++);
        //     swap_selitems(SEL_ITEMS_controlregion_vec.back(), new SelDatI("n_ak8_all_loose_0b_m150_noT", "N_ak8_all_loose_0b_m150_noT", 11, -.5, 10.5, 1), insert_new++);
        // } else if (cat == "SignalRegionHLoose") {
        //     swap_selitems(SEL_ITEMS_controlregion_vec.back(), new SelDatI("n_ak8_all_loose_2b_m60-150_noT", "N_ak8_all_loose_2b_m60-150_noT", 11, -.5, 10.5, 1), insert_new++);
        } else if (cat == "SignalRegionHLooseBoost") {
            swap_selitems(SEL_ITEMS_controlregion_vec.back(), new SelDatI("n_ak8_boost_loose_2b_m60-150_noT", "N_ak8_boost_loose_2b_m60-150_noT", 11, -.5, 10.5, 1), insert_new++);
        } else if (cat == "SignalRegionHMedBoost") {
            swap_selitems(SEL_ITEMS_controlregion_vec.back(), new SelDatI("n_ak8_boost_med_2b_m60-150_noT", "N_ak8_boost_med_2b_m60-150_noT", 11, -.5, 10.5, 1), insert_new++);
        // } else if (cat == "SignalRegionHMed") {
        //     swap_selitems(SEL_ITEMS_controlregion_vec.back(), new SelDatI("n_ak8_all_med_2b_m60-150_noT", "N_ak8_all_med_2b_m60-150_noT", 11, -.5, 10.5, 1), insert_new++);
        } else {
            assert(false);  // a category must be given
        }

        vector<string> item_names;
        // std::cout << "CATEGORY: " << cat << endl;
        for (auto const & seli : SEL_ITEMS_controlregion_vec.back()) {
            item_names.push_back(seli->name());
            // std::cout << "  VALUE: " << seli->name() << ", MIN/MAX CUT: " << seli->cutvalue_min() << " " << seli->cutvalue_max() << endl;
        } 

        sel_helpers.emplace_back(new SelItemsHelper(SEL_ITEMS_controlregion_vec.back(), ctx, item_names, cat+"_sel_accept", cat+"_sel_all_accepted"));
        // sel_helper.declare_items_for_output();
        sel_modules.emplace_back(new SelectionProducer(ctx, *sel_helpers.back()));


        // 3. Set up Hists classes:

        // TODO: set up and fill other histogram classes, e.g. your own HistCollector stuff

        v_hists.emplace_back(vector<unique_ptr<Hists>>());
        v_hists_after_sel.emplace_back(vector<unique_ptr<Hists>>());

        if (!v_hists_nosel.size())
            sel_helpers.back()->fill_hists_vector(v_hists_nosel, "NoSelection");
        auto nm1_hists = new Nm1SelHists(ctx, cat+"/Nm1Selection", *sel_helpers.back());
        auto cf_hists = new VLQ2HTCutflow(ctx, cat+"/Cutflow", *sel_helpers.back());
        // auto notoptag_hists = new SelectedSelHists(ctx, cat+"/NoTopTagCut", *sel_helpers.back(), {}, {"n_toptags"});
        v_hists.back().emplace_back(nm1_hists);
        v_hists.back().emplace_back(cf_hists);
        // v_hists.back().emplace_back(notoptag_hists);
        sel_helpers.back()->fill_hists_vector(v_hists_after_sel.back(), cat+"/PostSelection");

        // append 2D cut
        // unsigned pos_2d_cut = 5;
        // sel_module->insert_selection(pos_2d_cut, new TwoDCutSel(ctx, DR_2D_CUT_PRESEL, DPT_2D_CUT_PRESEL));
        // nm1_hists->insert_hists(pos_2d_cut, new TwoDCutHist(ctx, "Nm1Selection"));
        // cf_hists->insert_step(pos_2d_cut, "2D cut");
        // v_hists.insert(v_hists.begin() + insert_sel, move(unique_ptr<Hists>(new TwoDCutHist(ctx, "NoSelection"))));
        // v_hists_after_sel.insert(v_hists_after_sel.begin() + insert_sel, move(unique_ptr<Hists>(new TwoDCutHist(ctx, "PostSelection"))));

        // v_hists_after_sel.emplace_back(new HistCollector(ctx, "EventHistsPost"));

        // unsigned pos_cat_cut = 4;
        // sel_module->insert_selection(pos_cat_cut, cat_check_module.release());
        // nm1_hists->insert_hists(pos_cat_cut, new HandleHist<DATATYPE>(ctx, dir, name_, title_.c_str(), n_bins_, x_min_, x_max_));
        // cf_hists->insert_step(pos_cat_cut, "2D cut");
        // v_hists.insert(v_hists.begin() + pos_cat_cut, move(unique_ptr<Hists>(new TwoDCutHist(ctx, "NoSelection"))));
    }

    // if (type == "MC") {
    //     v_hists_nosel.emplace_back(new HistCollector(ctx, "EventHistsPre"));
    //         // v_hists_after_sel.emplace_back(new HistCollector(ctx, "EventHistsPost"));
    //         // auto recogen_hits_pre = new RecoGenHists<TopJet>(ctx, "EventHistsPre");
    //         // auto recogen_hits_post = new RecoGenHists<TopJet>(ctx, "EventHistsPost");
    //         // recogen_hits_pre->add_genhistcoll(ctx, "toptags", 0.5);
    //         // recogen_hits_pre->add_genhistcoll(ctx, "higgs_tags_ca15_notop", 0.5);
    //         // recogen_hits_post->add_genhistcoll(ctx, "toptags", 0.5);
    //         // recogen_hits_post->add_genhistcoll(ctx, "higgs_tags_ca15_notop", 0.5);
    //         // v_hists.push_back(std::move(unique_ptr<Hists>(recogen_hits_pre)));
    //         // v_hists_after_sel.push_back(std::move(unique_ptr<Hists>(recogen_hits_post)));
    // } else {
    //     v_hists_nosel.emplace_back(new HistCollector(ctx, "EventHistsPre", false));
    //         // v_hists_after_sel.emplace_back(new HistCollector(ctx, "EventHistsPost", false));
    // }


}


bool TpTpControlRegion::process(Event & event) {

    // cout << "TpTpControlRegion: Starting to process event (runid, eventid) = (" << event.run << ", " << event.event << ")" << endl;

    // TEST STUFF HERE



    // FIRST RUN PRE_MODULES THAT NEED TO RUN AT THE BEGINNING (e.g. MC lumi re-weighting)

    // if (gen_hists) {
    //     gen_hists->fill(event);
    // }

    // run all modules
    for (auto & mod : v_pre_modules) {
        mod->process(event);
    }

    // run selection

    // if (!cat_check_module->passes(event)) {
    //     return false;
    // }

    for (unsigned i = 0; i < sel_modules.size(); ++i) {
    
        bool all_accepted = sel_modules[i]->process(event);

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

    for (auto & hist : v_hists_nosel) {
        hist->fill(event);
    }

    // decide whether or not to keep the current event in the output:
    return false;
}

UHH2_REGISTER_ANALYSIS_MODULE(TpTpControlRegion)
