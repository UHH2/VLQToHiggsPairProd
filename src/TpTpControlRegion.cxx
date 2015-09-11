#include <iostream>
#include <memory>

#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Event.h"
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
#include "UHH2/VLQToHiggsPairProd/include/VLQToHiggsPairProdSelections.h"
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
    string version, type;
    // modules for setting up collections and cleaning
    vector<unique_ptr<AnalysisModule>> v_pre_modules;
    unique_ptr<AnalysisModule> sel_module;
    // unique_ptr<AnalysisModule> writer_module; // for TMVA stuff

    // store the Hists collection
    unique_ptr<Hists> gen_hists;
    vector<unique_ptr<Hists>> v_hists;
    vector<unique_ptr<Hists>> v_hists_after_sel;

    vector<shared_ptr<SelectionItem>> SEL_ITEMS_VLQPair_controlregion;

    // check category
    // unique_ptr<Selection> cat_check_module;

    // Event::Handle<int> h_ngenleps;
};




TpTpControlRegion::TpTpControlRegion(Context & ctx) {


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


    v_pre_modules.emplace_back(new PrimaryLepton(ctx, "PrimaryLepton")); 
    v_pre_modules.emplace_back(new HTCalculator(ctx, boost::none, "HT"));
    v_pre_modules.emplace_back(new STCalculator(ctx, "ST"));
    v_pre_modules.emplace_back(new CollectionProducer<Jet>(ctx,
                "jets",
                "b_jets",
                JetId(CSVBTag(CSVBTag::WP_MEDIUM))
                ));
    v_pre_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
                "jets",
                "n_btags",
                JetId(CSVBTag(CSVBTag::WP_MEDIUM))
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

    // higgs tags, no top separation
    v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "patJetsCa15CHSJetsFilteredPacked_daughters",
                "higgs_tags_ca15",
                TopJetId(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_MEDIUM)))
                ));
    v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "patJetsAk8CHSJetsSoftDropPacked_daughters",
                "higgs_tags_med_ak8",
                TopJetId(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_MEDIUM)))
                ));
    v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "patJetsAk8CHSJetsSoftDropPacked_daughters",
                "higgs_tags_loose_ak8",
                TopJetId(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)))
                ));

    // higgs tags, with top separation
    v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "patJetsCa15CHSJetsFilteredPacked_daughters",
                "higgs_tags_ca15_notop",
                TopJetId(AndId<TopJet>(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_MEDIUM)),
                    MinMaxDeltaRId<TopJet>(ctx, "toptags", "min_dr_higgs")))
                ));
    v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "patJetsAk8CHSJetsSoftDropPacked_daughters",
                "higgs_tags_med_ak8_notop",
                TopJetId(AndId<TopJet>(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_MEDIUM)),
                    MinMaxDeltaRId<TopJet>(ctx, "toptags", "min_dr_higgs")))
                ));
    v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "patJetsAk8CHSJetsSoftDropPacked_daughters",
                "higgs_tags_loose_ak8_notop",
                TopJetId(AndId<TopJet>(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)),
                    MinMaxDeltaRId<TopJet>(ctx, "toptags", "min_dr_higgs")))
                ));

    // check if, in case there is only one top, the dR to the closest higgs is really 1.5
    v_pre_modules.emplace_back(new MinDeltaRProducer<TopJet, TopJet>(ctx, "one_top", "higgs_tags_med_ak8_notop", "min_deltaR_top_higgsak8notop"));
    v_pre_modules.emplace_back(new MinDeltaRProducer<TopJet, TopJet>(ctx, "one_top", "higgs_tags_med_ak8", "min_deltaR_top_higgsak8"));
    v_pre_modules.emplace_back(new MinDeltaRProducer<TopJet, TopJet>(ctx, "two_top", "higgs_tags_med_ak8_notop", "min_deltaR_top_higgsak8notop_twotop"));
    v_pre_modules.emplace_back(new MinDeltaRProducer<TopJet, TopJet>(ctx, "two_top", "higgs_tags_med_ak8", "min_deltaR_top_higgsak8_twotop"));


    

    // additional b-tags
    v_pre_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
                "b_jets",
                "n_additional_btags",
                JetId(AndId<Jet>(MinMaxDeltaRId<TopJet>(ctx, "higgs_tags_med_ak8_notop", 1.0, true),
                                    MinMaxDeltaRId<TopJet>(ctx, "toptags", 1.0, true)))
                ));


    // Anti-Higgstags producer: BVeto

    v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "patJetsAk8CHSJetsSoftDropPacked_daughters",
                "bveto_higgs_tags_med_ak8",
                TopJetId(AntiHiggsBVetoTag(60.f, 99999., CSVBTag(CSVBTag::WP_MEDIUM)))
                ));
    v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "patJetsAk8CHSJetsSoftDropPacked_daughters",
                "bveto_higgs_tags_med_ak8_notop",
                TopJetId(AndId<TopJet>(AntiHiggsBVetoTag(60.f, 99999., CSVBTag(CSVBTag::WP_MEDIUM)),
                    MinMaxDeltaRId<TopJet>(ctx, "toptags", "min_dr_higgs")))
                ));

    // Anti-Higgstags producer: MassInvert

    v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "patJetsAk8CHSJetsSoftDropPacked_daughters",
                "massinvert_higgs_tags_med_ak8",
                TopJetId(HiggsTag(0.f, 60.f, CSVBTag(CSVBTag::WP_MEDIUM)))
                ));
    v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "patJetsAk8CHSJetsSoftDropPacked_daughters",
                "massinvert_higgs_tags_med_ak8_notop",
                TopJetId(AndId<TopJet>(HiggsTag(0.f, 60.f, CSVBTag(CSVBTag::WP_MEDIUM)),
                    MinMaxDeltaRId<TopJet>(ctx, "toptags", "min_dr_higgs")))
                ));


    // Anti-Higgstags producer: Tau21

    v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "patJetsAk8CHSJetsSoftDropPacked_daughters",
                "bigTau21_higgs_tags_med_ak8",
                TopJetId(AndId<TopJet>(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_MEDIUM)),
                    VetoId<TopJet>(Tau21(0.6))))
                ));
    v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "patJetsAk8CHSJetsSoftDropPacked_daughters",
                "bigTau21_higgs_tags_med_ak8_notop",
                TopJetId(AndId<TopJet>(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_MEDIUM)),
                    VetoId<TopJet>(Tau21(0.6)),
                    MinMaxDeltaRId<TopJet>(ctx, "toptags", "min_dr_higgs")))
                ));
    


    SEL_ITEMS_VLQPair_controlregion = SEL_ITEMS_VLQPair_controlregion_base;

    unsigned insert_sel = 11;
    unsigned insert_cut = 1;

    make_modules_and_selitem("topjets", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel);
    make_modules_and_selitem("toptags", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel);
    make_modules_and_selitem("patJetsCa15CHSJetsFilteredPacked_daughters", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel);
    make_modules_and_selitem("higgs_tags_ca15", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel);
    make_modules_and_selitem("patJetsAk8CHSJetsSoftDropPacked_daughters", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel);
    make_modules_and_selitem("higgs_tags_med_ak8", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel);
    make_modules_and_selitem("higgs_tags_loose_ak8", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel);
    make_modules_and_selitem("higgs_tags_ca15_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel);
    // make_modules_and_selitem("higgs_tags_med_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel);
    make_modules_and_selitem("bveto_higgs_tags_med_ak8", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel);
    // make_modules_and_selitem("bveto_higgs_tags_med_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel);
    make_modules_and_selitem("massinvert_higgs_tags_med_ak8", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel);
    // make_modules_and_selitem("massinvert_higgs_tags_med_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel);
    make_modules_and_selitem("bigTau21_higgs_tags_med_ak8", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel);
    // make_modules_and_selitem("bigTau21_higgs_tags_med_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel);

    const string & category = ctx.get("category", "");

    // make copy of base sel vector to avoid inserting the same selection
    // multiple times in different runs (since the base vector is static it is not
    // deleted at the end of one cycle)

    // unsigned pos_cut = 1;
    // higgs tag with filtered jets
    if (category == "0HiggsTags1AntiHTBVeto") {
        make_modules_and_selitem("bveto_higgs_tags_med_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel, insert_cut+1, 1);
        make_modules_and_selitem("higgs_tags_med_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel, insert_cut+2, 0, 0);
        make_modules_and_selitem("massinvert_higgs_tags_med_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel, insert_cut+2, 0, 0);
        make_modules_and_selitem("bigTau21_higgs_tags_med_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel, insert_cut+2, 0, 0);
        make_modules_and_selitem("higgs_tags_loose_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel);
    } else if (category == "0HiggsTags1AntiHTMassInvert") {
        make_modules_and_selitem("massinvert_higgs_tags_med_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel, insert_cut+1, 1);
        make_modules_and_selitem("higgs_tags_med_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel, insert_cut+2, 0, 0);
        make_modules_and_selitem("bveto_higgs_tags_med_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel, insert_cut+2, 0, 0);
        make_modules_and_selitem("bigTau21_higgs_tags_med_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel, insert_cut+2, 0, 0);
        make_modules_and_selitem("higgs_tags_loose_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel);
        // v_cat_modules.emplace_back(new CollectionProducer<Jet>(ctx, AndId<Jet>(PtEtaCut(30., 2.4), CSVBTag(CSVBTag::WP_MEDIUM)), "jets", "b_jets"));
    } else if (category == "0HiggsTags1AntiHTBigTau21") {
        make_modules_and_selitem("bigTau21_higgs_tags_med_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel, insert_cut+1, 1);
        make_modules_and_selitem("higgs_tags_med_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel, insert_cut+2, 0, 0);
        make_modules_and_selitem("bveto_higgs_tags_med_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel, insert_cut+2, 0, 0);
        make_modules_and_selitem("massinvert_higgs_tags_med_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel, insert_cut+2, 0, 0);
        make_modules_and_selitem("higgs_tags_loose_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel);
        // v_cat_modules.emplace_back(new CollectionProducer<Jet>(ctx, AndId<Jet>(PtEtaCut(30., 2.4), CSVBTag(CSVBTag::WP_LOOSE)), "jets", "b_jets"));
    } else if (category == "1HiggsMedTagSignalRegion") {
        make_modules_and_selitem("higgs_tags_med_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel, insert_cut+1, 1);
        make_modules_and_selitem("bveto_higgs_tags_med_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel, insert_cut+2, 0, 0);
        make_modules_and_selitem("massinvert_higgs_tags_med_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel, insert_cut+2, 0, 0);
        make_modules_and_selitem("bigTau21_higgs_tags_med_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel, insert_cut+2, 0, 0);
        make_modules_and_selitem("higgs_tags_loose_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel);
        // v_cat_modules.emplace_back(new CollectionProducer<Jet>(ctx, AndId<Jet>(PtEtaCut(30., 2.4), CSVBTag(CSVBTag::WP_LOOSE)), "jets", "b_jets"));
    } else if (category == "1HiggsLooseTagSignalRegion") {
        make_modules_and_selitem("higgs_tags_loose_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel, insert_cut+1, 1);
        make_modules_and_selitem("higgs_tags_med_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel);
        make_modules_and_selitem("bveto_higgs_tags_med_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel, insert_cut+2, 0, 0);
        make_modules_and_selitem("massinvert_higgs_tags_med_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel, insert_cut+2, 0, 0);
        make_modules_and_selitem("bigTau21_higgs_tags_med_ak8_notop", ctx, v_pre_modules, SEL_ITEMS_VLQPair_controlregion, insert_sel, insert_cut+2, 0, 0);
        // v_cat_modules.emplace_back(new CollectionProducer<Jet>(ctx, AndId<Jet>(PtEtaCut(30., 2.4), CSVBTag(CSVBTag::WP_LOOSE)), "jets", "b_jets"));
    } else {
        assert(false);  // a category must be given
    }

    // TODO: continue with making SelectionItems vector, insert other selections (top tag, b tags etc...)?

    // Other CutProducers
    v_pre_modules.emplace_back(new NLeptonsProducer(ctx, "n_leptons"));
    v_pre_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx, "jets", "n_jets"));

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
    if (version == "Run2015B_Mu") {
        v_pre_modules.emplace_back(new TriggerAcceptProducer(ctx, QCDTEST_MUON_TRIGGER_PATHS_DATA, "trigger_accept"));
    } else if (version == "Run2015B_Ele") {
        v_pre_modules.emplace_back(new TriggerAcceptProducer(ctx, {}, "trigger_accept"));
    } else if (version == "Run2015B_Had") {
        v_pre_modules.emplace_back(new TriggerAcceptProducer(ctx, {}, "trigger_accept"));
    } else {
        v_pre_modules.emplace_back(new TriggerAcceptProducer(ctx, QCDTEST_MUON_TRIGGER_PATHS, "trigger_accept"));
    }


    

    // Selection Producer
    SelItemsHelper sel_helper(SEL_ITEMS_VLQPair_controlregion, ctx);
    sel_helper.declare_items_for_output();
    sel_module.reset(new SelectionProducer(ctx, sel_helper));

    // 3. Set up Hists classes:

    // TODO: set up and fill other histogram classes, e.g. your own HistCollector stuff

    sel_helper.fill_hists_vector(v_hists, "NoSelection");
    auto nm1_hists = new Nm1SelHists(ctx, "Nm1Selection", sel_helper);
    auto cf_hists = new VLQ2HTCutflow(ctx, "Cutflow", sel_helper);
    // auto stsel_hists = new SelectedSelHists(ctx, "OnlySTCut", sel_helper, {"ST"});
    v_hists.emplace_back(nm1_hists);
    v_hists.emplace_back(cf_hists);
    // v_hists.emplace_back(stsel_hists);
    sel_helper.fill_hists_vector(v_hists_after_sel, "PostSelection");
    
    // if (type == "MC") {
    //     v_hists.emplace_back(new HistCollector(ctx, "EventHistsPre"));
    //     v_hists_after_sel.emplace_back(new HistCollector(ctx, "EventHistsPost"));
    //     // auto recogen_hits_pre = new RecoGenHists<TopJet>(ctx, "EventHistsPre");
    //     // auto recogen_hits_post = new RecoGenHists<TopJet>(ctx, "EventHistsPost");
    //     // recogen_hits_pre->add_genhistcoll(ctx, "toptags", 0.5);
    //     // recogen_hits_pre->add_genhistcoll(ctx, "higgs_tags_ca15_notop", 0.5);
    //     // recogen_hits_post->add_genhistcoll(ctx, "toptags", 0.5);
    //     // recogen_hits_post->add_genhistcoll(ctx, "higgs_tags_ca15_notop", 0.5);
    //     // v_hists.push_back(std::move(unique_ptr<Hists>(recogen_hits_pre)));
    //     // v_hists_after_sel.push_back(std::move(unique_ptr<Hists>(recogen_hits_post)));
    // } else {
    //     v_hists.emplace_back(new HistCollector(ctx, "EventHistsPre", false));
    //     v_hists_after_sel.emplace_back(new HistCollector(ctx, "EventHistsPost", false));
    // }

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

    // h_ngenleps = ctx.get_handle<int>("n_genleptons");


    // writer_module.reset(sel_helper.make_tree_writer(version)); // for TMVA stuff


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

    // if (version.substr(version.size() - 6, 100) == "onelep") {
    //     if (event.is_valid(h_ngenleps)) {
    //         int n_leptons = event.get(h_ngenleps);
    //         if (n_leptons != 1)
    //             return false;
    //     }
    //     else {
    //         std::cout << "WARNING: h_ngenleps is not valid!\n";
    //         return false;
    //     }
    // }

    // run selection
    bool all_accepted = sel_module->process(event);

    // all hists
    for (auto & hist : v_hists) {
        hist->fill(event);
    }

    // if (!cat_check_module->passes(event)) {
    //     return false;
    // }

    // fill histograms
    if (all_accepted) {
        for (auto & hist : v_hists_after_sel) {
            hist->fill(event);
        }

        // for TMVA stuff
        // if (writer_module.get()) {
        //     writer_module->process(event);
        // }
    }

    // decide whether or not to keep the current event in the output:
    return all_accepted;
}

UHH2_REGISTER_ANALYSIS_MODULE(TpTpControlRegion)
