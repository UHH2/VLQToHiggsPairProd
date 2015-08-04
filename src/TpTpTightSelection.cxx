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


using namespace std;
using namespace uhh2;

using namespace vlqToHiggsPair;

typedef VectorAndSelection MyAndSelection;

class TpTpTightSelection: public AnalysisModule {
public:

    explicit TpTpTightSelection(Context & ctx);
    virtual bool process(Event & event);

private:
    string version;
    // modules for setting up collections and cleaning
    vector<unique_ptr<AnalysisModule>> v_pre_modules;
    unique_ptr<AnalysisModule> sel_module;
    // unique_ptr<AnalysisModule> writer_module; // for TMVA stuff

    // store the Hists collection
    unique_ptr<Hists> gen_hists;
    vector<unique_ptr<Hists>> v_hists;
    vector<unique_ptr<Hists>> v_hists_after_sel;

    vector<shared_ptr<SelectionItem>> SEL_ITEMS_VLQPair_tight;

    // check category
    // unique_ptr<Selection> cat_check_module;

    Event::Handle<int> h_ngenleps;
};


TpTpTightSelection::TpTpTightSelection(Context & ctx) {

    // If needed, access the configuration of the module here, e.g.:
    // string testvalue = ctx.get("TestKey", "<not set>");
    // cout << "TestKey in the configuration was: " << testvalue << endl;
    version = ctx.get("dataset_version", "");
    
    // If running in SFrame, the keys "dataset_version", "dataset_type" and "dataset_lumi"
    // are set to the according values in the xml file. For CMSSW, these are
    // not set automatically, but can be set in the python config file.
    for(auto & kv : ctx.get_all()){
        cout << " " << kv.first << " = " << kv.second << endl;
    }
    
    // 1. setup modules to prepare the event.

    // EventWeightOutputHandle only needed for TMVA studies
    // v_pre_modules.emplace_back(new EventWeightOutputHandle(ctx));

    bool mclumiweight = true;
    bool mcpileupreweight = true;

    if(mclumiweight)  v_pre_modules.emplace_back(new MCLumiWeight(ctx));
    if(mcpileupreweight) v_pre_modules.emplace_back(new MCPileupReweight(ctx));
    // v_pre_modules.emplace_back(new BJetsProducer(ctx, CSVBTag::WP_MEDIUM, "b_jets"));


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
    // v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
    //             "topjets",
    //             "boosted_topjets",
    //             TopJetId(PtEtaCut(400., 2.4))
    //             ));
    // v_pre_modules.emplace_back(new PtSorter<TopJet>(ctx, "boosted_topjets"));

    // cms top tags
    v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "topjets",
                "toptags",
                TopJetId(AndId<TopJet>(PtEtaCut(400., 2.4), CMSTopTag()))
                ));
    v_pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "topjets",
                "n_toptags",
                TopJetId(AndId<TopJet>(PtEtaCut(400., 2.4), CMSTopTag()))
                ));

    // check if there is exactly 1 Top Tag; if yes, make sure that all higgs tags are
    // well separated from it by making a dR requirement of 1.5
    v_pre_modules.emplace_back(new XTopTagProducer(ctx, "toptags", "min_dr_higgs", "one_top", 1.5, 1));
    v_pre_modules.emplace_back(new XTopTagProducer(ctx, "toptags", "dummy_dr", "two_top", -999., 2));

    // higgs tags, no top separation
    v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "patJetsCa15CHSJetsFilteredPacked",
                "higgs_tags_ca15",
                TopJetId(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)))
                ));
    v_pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "patJetsCa15CHSJetsFilteredPacked",
                "n_higgs_tags_ca15",
                TopJetId(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)))
                ));
    v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "patJetsCa8CHSJetsPrunedPacked",
                "higgs_tags_ca8",
                TopJetId(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)))
                ));
    v_pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "patJetsCa8CHSJetsPrunedPacked",
                "n_higgs_tags_ca8",
                TopJetId(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)))
                ));

    // higgs tags, with top separation
    v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "patJetsCa15CHSJetsFilteredPacked",
                "higgs_tags_ca15_notop",
                TopJetId(AndId<TopJet>(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)),
                    MinMaxDeltaRId<TopJet>(ctx, "toptags", "min_dr_higgs")))
                ));
    v_pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "patJetsCa15CHSJetsFilteredPacked",
                "n_higgs_tags_ca15_notop",
                TopJetId(AndId<TopJet>(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)),
                    MinMaxDeltaRId<TopJet>(ctx, "toptags", "min_dr_higgs")))
                ));
    v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "patJetsCa8CHSJetsPrunedPacked",
                "higgs_tags_ca8_notop",
                TopJetId(AndId<TopJet>(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)),
                    MinMaxDeltaRId<TopJet>(ctx, "toptags", "min_dr_higgs")))
                ));
    v_pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "patJetsCa8CHSJetsPrunedPacked",
                "n_higgs_tags_ca8_notop",
                TopJetId(AndId<TopJet>(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)),
                    MinMaxDeltaRId<TopJet>(ctx, "toptags", "min_dr_higgs")))
                ));

    // check if, in case there is only one top, the dR to the closest higgs is really 1.5
    v_pre_modules.emplace_back(new MinDeltaRProducer<TopJet, TopJet>(ctx, "one_top", "higgs_tags_ca15_notop", "min_deltaR_top_higgsca8notop"));
    v_pre_modules.emplace_back(new MinDeltaRProducer<TopJet, TopJet>(ctx, "one_top", "higgs_tags_ca15", "min_deltaR_top_higgsca8"));
    v_pre_modules.emplace_back(new MinDeltaRProducer<TopJet, TopJet>(ctx, "two_top", "higgs_tags_ca15_notop", "min_deltaR_top_higgsca8notop_twotop"));
    v_pre_modules.emplace_back(new MinDeltaRProducer<TopJet, TopJet>(ctx, "two_top", "higgs_tags_ca15", "min_deltaR_top_higgsca8_twotop"));


    

    // additional b-tags
    v_pre_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
                "b_jets",
                "n_additional_btags",
                JetId(AndId<Jet>(MinMaxDeltaRId<TopJet>(ctx, "higgs_tags_ca8_notop", 1.0, true),
                                    MinMaxDeltaRId<TopJet>(ctx, "toptags", 1.0, true)))
                ));

    // mass producers
    v_pre_modules.emplace_back(new LeadingPartMassProducer<TopJet>(ctx,
                "higgs_tags_ca15",
                "mass_ld_higgs_tag_ca15"
                ));
    v_pre_modules.emplace_back(new LeadingPartMassProducer<TopJet>(ctx,
                "higgs_tags_ca8",
                "mass_ld_higgs_tag_ca8"
                ));
    v_pre_modules.emplace_back(new LeadingPartMassProducer<TopJet>(ctx,
                "higgs_tags_ca15_notop",
                "mass_ld_higgs_tag_ca15_notop"
                ));
    v_pre_modules.emplace_back(new LeadingPartMassProducer<TopJet>(ctx,
                "higgs_tags_ca8_notop",
                "mass_ld_higgs_tag_ca8_notop"
                ));
    v_pre_modules.emplace_back(new LeadingPartMassProducer<TopJet>(ctx,
                "toptags",
                "mass_ld_toptag"
                ));


    const string & category = ctx.get("category", "");

    // make copy of base sel vector to avoid inserting the same selection
    // multiple times in different runs (since the base vector is static it is not
    // deleted at the end of one cycle)
    SEL_ITEMS_VLQPair_tight = SEL_ITEMS_VLQPair_tight_base;

    unsigned pos_cut = 4;
    // higgs tag with filtered jets
    if (category == "PrunedCat1htag0btag") {
        // cat_check_module.reset(new MyAndSelection({
        //     new HandleSelection<int>(ctx, "n_higgs_tags_ca8_notop", 1),
        //     new HandleSelection<int>(ctx, "n_additional_btags", 0, 0)
        // }));
        SEL_ITEMS_VLQPair_tight.insert(SEL_ITEMS_VLQPair_tight.begin()+pos_cut, 
            shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_ca8_notop", "N_{H Tags (CA8), no top}", 11, -.5, 10.5,
                1)));
        SEL_ITEMS_VLQPair_tight.insert(SEL_ITEMS_VLQPair_tight.begin()+pos_cut+1, 
            shared_ptr<SelectionItem>(new SelDatI("n_additional_btags", "N_{additional b-tags}", 11, -.5, 10.5,
                0, 0)));
        // v_cat_modules.emplace_back(new CollectionProducer<Jet>(ctx, AndId<Jet>(PtEtaCut(30., 2.4), CSVBTag(CSVBTag::WP_MEDIUM)), "jets", "b_jets"));
        // v_cat_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx, HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_MEDIUM)), "patJetsCa15CHSJetsFilteredPacked", "n_htags"));
        // v_cat_modules.emplace_back(new CollectionProducer<TopJet>(ctx, HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_MEDIUM)), "patJetsCa15CHSJetsFilteredPacked", "h_jets"));
    } else if (category == "PrunedCat1htag1btag") {
        SEL_ITEMS_VLQPair_tight.insert(SEL_ITEMS_VLQPair_tight.begin()+pos_cut, 
            shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_ca8_notop", "N_{H Tags (CA8), no top}", 11, -.5, 10.5,
                1)));
        SEL_ITEMS_VLQPair_tight.insert(SEL_ITEMS_VLQPair_tight.begin()+pos_cut+1, 
            shared_ptr<SelectionItem>(new SelDatI("n_additional_btags", "N_{additional b-tags}", 11, -.5, 10.5,
                1, 1)));
        // v_cat_modules.emplace_back(new CollectionProducer<Jet>(ctx, AndId<Jet>(PtEtaCut(30., 2.4), CSVBTag(CSVBTag::WP_MEDIUM)), "jets", "b_jets"));
    } else if (category == "PrunedCat1htag2plusbtag") {
        SEL_ITEMS_VLQPair_tight.insert(SEL_ITEMS_VLQPair_tight.begin()+pos_cut, 
            shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_ca8_notop", "N_{H Tags (CA8), no top}", 11, -.5, 10.5,
                1)));
        SEL_ITEMS_VLQPair_tight.insert(SEL_ITEMS_VLQPair_tight.begin()+pos_cut+1, 
            shared_ptr<SelectionItem>(new SelDatI("n_additional_btags", "N_{additional b-tags}", 11, -.5, 10.5,
                2)));
        // v_cat_modules.emplace_back(new CollectionProducer<Jet>(ctx, AndId<Jet>(PtEtaCut(30., 2.4), CSVBTag(CSVBTag::WP_LOOSE)), "jets", "b_jets"));
    } else if (category == "PrunedCat0htag2plusbtag") {
        SEL_ITEMS_VLQPair_tight.insert(SEL_ITEMS_VLQPair_tight.begin()+pos_cut, 
            shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_ca8_notop", "N_{H Tags (CA8), no top}", 11, -.5, 10.5,
                0, 0)));
        SEL_ITEMS_VLQPair_tight.insert(SEL_ITEMS_VLQPair_tight.begin()+pos_cut+1, 
            shared_ptr<SelectionItem>(new SelDatI("n_additional_btags", "N_{additional b-tags}", 11, -.5, 10.5,
                2)));
        // v_cat_modules.emplace_back(new CollectionProducer<Jet>(ctx, AndId<Jet>(PtEtaCut(30., 2.4), CSVBTag(CSVBTag::WP_LOOSE)), "jets", "b_jets"));
    } 
    else if (category == "PrunedCat2htag") {
        SEL_ITEMS_VLQPair_tight.insert(SEL_ITEMS_VLQPair_tight.begin()+pos_cut, 
            shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_ca8_notop", "N_{H Tags (CA8), no top}", 11, -.5, 10.5,
                2)));
        SEL_ITEMS_VLQPair_tight.insert(SEL_ITEMS_VLQPair_tight.begin()+pos_cut+1, 
            shared_ptr<SelectionItem>(new SelDatI("n_additional_btags", "N_{additional b-tags}", 11, -.5, 10.5
                )));
        // v_cat_modules.emplace_back(new CollectionProducer<Jet>(ctx, AndId<Jet>(PtEtaCut(30., 2.4), CSVBTag(CSVBTag::WP_LOOSE)), "jets", "b_jets"));
    }
    else if (category == "Test1HTag") {
        SEL_ITEMS_VLQPair_tight.insert(SEL_ITEMS_VLQPair_tight.begin()+pos_cut, 
            shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_ca8_notop", "N_{H Tags (CA8), no top}", 11, -.5, 10.5,
                1)));
        // v_cat_modules.emplace_back(new CollectionProducer<Jet>(ctx, AndId<Jet>(PtEtaCut(30., 2.4), CSVBTag(CSVBTag::WP_LOOSE)), "jets", "b_jets"));
    } else {
        assert(false);  // a category must be given
    }




    // Other CutProducers
    v_pre_modules.emplace_back(new NLeptonsProducer(ctx, "n_leptons"));
    v_pre_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx, "jets", "n_jets"));

    v_pre_modules.emplace_back(new PartPtProducer<Jet>(ctx, "jets", "leading_jet_pt", 1));
    v_pre_modules.emplace_back(new PartPtProducer<Jet>(ctx, "jets", "subleading_jet_pt", 2));
    v_pre_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "topjets", "leading_topjet_pt", 1));
    v_pre_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "patJetsCa8CHSJetsPrunedPacked", "leading_ca8jet_pt", 1));
    v_pre_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "patJetsCa15CHSJetsFilteredPacked", "leading_ca15jet_pt", 1));

    // get pt of the top tagged jet with smallest pt, just to see if PtEtaCut Id is working
    v_pre_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "toptags", "smallest_pt_toptags", -1));

    v_pre_modules.emplace_back(new LeptonPtProducer(ctx, "PrimaryLepton", "primary_lepton_pt"));
    // v_pre_modules.emplace_back(new NeutrinoParticleProducer(ctx, NeutrinoReconstruction, "neutrino_part_vec", "PrimaryLepton"));
    // v_pre_modules.emplace_back(new MinDeltaRProducer<FlavorParticle, LorentzVector>(ctx, "PrimaryLepton", "neutrino_part_vec", "min_deltaR_lep_nu"));
    // v_pre_modules.emplace_back(new TwoParticleCollectionProducer<Jet>(ctx, "b_jets", "leading_b_jets"));
    // v_pre_modules.emplace_back(new MinDeltaRProducer<FlavorParticle, Jet>(ctx, "PrimaryLepton", "leading_b_jets", "min_deltaR_lep_bjets"));
    // v_pre_modules.emplace_back(new DeltaRTwoLeadingParticleProducer<Jet>(ctx, "leading_b_jets", "deltaR_leading_bjets"));

    // N Gen Leptons Producer

    v_pre_modules.emplace_back(new CollectionSizeProducer<GenParticle>(ctx, "genparticles", "n_genleptons",
                GenParticleId(GenParticlePdgId({-11, 11, -13, 13}))));
    // v_pre_modules.emplace_back(new GenParticlesPrinter(ctx));

    

    // Selection Producer
    SelItemsHelper sel_helper(SEL_ITEMS_VLQPair_tight, ctx);
    sel_helper.declare_items_for_output();
    sel_module.reset(new SelectionProducer(ctx, sel_helper));

    // 3. Set up Hists classes:

    // TODO: set up and fill other histogram classes, e.g. your own HistCollector stuff

    sel_helper.fill_hists_vector(v_hists, "NoSelection");
    auto nm1_hists = new Nm1SelHists(ctx, "Nm1Selection", sel_helper);
    auto cf_hists = new VLQ2HTCutflow(ctx, "Cutflow", sel_helper);
    v_hists.emplace_back(nm1_hists);
    v_hists.emplace_back(cf_hists);
    // v_hists.emplace_back(new HistCollector(ctx, "EventHistsPre"));

    sel_helper.fill_hists_vector(v_hists_after_sel, "PostSelection");
    // v_hists_after_sel.emplace_back(new HistCollector(ctx, "EventHistsPost"));

    // unsigned pos_cat_cut = 4;
    // sel_module->insert_selection(pos_cat_cut, cat_check_module.release());
    // nm1_hists->insert_hists(pos_cat_cut, new HandleHist<DATATYPE>(ctx, dir, name_, title_.c_str(), n_bins_, x_min_, x_max_));
    // cf_hists->insert_step(pos_cat_cut, "2D cut");
    // v_hists.insert(v_hists.begin() + pos_cat_cut, move(unique_ptr<Hists>(new TwoDCutHist(ctx, "NoSelection"))));

    h_ngenleps = ctx.get_handle<int>("n_genleptons");


    // v_hists.emplace_back(new SingleLepTrigHists(ctx, "SingleLepTrig", "HLT_Ele95_CaloIdVT_GsfTrkIdT_v", true));
    // v_hists.emplace_back(new SingleLepTrigHists(ctx, "SingleLepTrig", "HLT_Mu40_v", false));

    // if (version.substr(version.size() - 5, 100) == "_Tlep") {
    //     gen_hists.reset(new VLQ2HTGenHists(ctx, "GenHists"));
    // }

    // if (version.substr(version.size() - 4, 100) == "Tlep") {
    //     v_hists_after_sel.emplace_back(new VLQ2HTRecoGenComparison(ctx, "GenRecoHists"));
    // }

    // writer_module.reset(sel_helper.make_tree_writer(version)); // for TMVA stuff


}


bool TpTpTightSelection::process(Event & event) {

    // cout << "TpTpTightSelection: Starting to process event (runid, eventid) = (" << event.run << ", " << event.event << ")" << endl;

    // TEST STUFF HERE



    // FIRST RUN PRE_MODULES THAT NEED TO RUN AT THE BEGINNING (e.g. MC lumi re-weighting)

    // if (gen_hists) {
    //     gen_hists->fill(event);
    // }

    // run all modules
    for (auto & mod : v_pre_modules) {
        mod->process(event);
    }

    if (version.substr(version.size() - 6, 100) == "onelep") {
        if (event.is_valid(h_ngenleps)) {
            int n_leptons = event.get(h_ngenleps);
            if (n_leptons != 1)
                return false;
        }
        else {
            std::cout << "WARNING: h_ngenleps is not valid!\n";
            return false;
        }
    }

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

UHH2_REGISTER_ANALYSIS_MODULE(TpTpTightSelection)
