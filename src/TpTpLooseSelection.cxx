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
#include "UHH2/VLQSemiLepPreSel/include/VLQSLPS_selectionItems.h"
#include "UHH2/VLQToHiggsPairProd/include/VLQPair_selectionItems.h"
#include "UHH2/VLQToHiggsPairProd/include/VLQPair_additionalModules.h"
#include "UHH2/VLQToHiggsPairProd/include/VLQPair_triggerPaths.h"



using namespace std;
using namespace uhh2;

using namespace vlqToHiggsPair;

enum ParticleID {
    BottomID = 5,
    TopID = 6,
    TprimeID = 8000001,
    ElID = 11,
    MuID = 13,
    ZID = 23,
    WID = 24,
    HiggsID = 25
};

static bool checkDecayMode(const Event & event, int id_tp1d1,
            int id_tp1d2, int id_tp2d1, int id_tp2d2) {
    GenParticleDaughterId tp1d(ParticleID::TprimeID, id_tp1d1, id_tp1d2);
    GenParticleDaughterId tp2d(ParticleID::TprimeID, id_tp2d1, id_tp2d2);

    for (vector<GenParticle>::const_iterator gp1 = event.genparticles->begin();
            gp1 != event.genparticles->end(); ++gp1) {
        if (tp1d(*gp1, event)) {
            for (vector<GenParticle>::const_iterator gp2 = gp1+1;
                    gp2 != event.genparticles->end(); ++gp2) {
                if (tp2d(*gp2, event)) {
                    return true;
                }
            }
            return false;
        }
        else if (tp2d(*gp1, event)) {
            for (vector<GenParticle>::const_iterator gp2 = gp1+1;
                    gp2 != event.genparticles->end(); ++gp2) {
                if (tp1d(*gp2, event)) {
                    return true;
                }
            }
            return false;
        }
    }
    return false;
}

class TpTpLooseSelection: public AnalysisModule {
public:

    explicit TpTpLooseSelection(Context & ctx);
    virtual bool process(Event & event);

private:
    string version, type;
    // modules for setting up collections and cleaning
    vector<unique_ptr<AnalysisModule>> v_pre_modules;
    vector<unique_ptr<AnalysisModule>> v_modules;
    unique_ptr<SelectionProducer> sel_module;
    // unique_ptr<AnalysisModule> writer_module; // for TMVA stuff

    // store the Hists collection
    unique_ptr<Hists> gen_hists;
    vector<unique_ptr<Hists>> v_hists;
    vector<unique_ptr<Hists>> v_hists_after_sel;
    vector<shared_ptr<SelectionItem>> SEL_ITEMS_VLQPair_loose;
    // unique_ptr<AnalysisModule> gen_printer;

    static int event_count;
};

int TpTpLooseSelection::event_count = 0;


TpTpLooseSelection::TpTpLooseSelection(Context & ctx) {

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

    // EventWeightOutputHandle only needed for TMVA studies
    // v_modules.emplace_back(new EventWeightOutputHandle(ctx));


    /* +++++
     * CommonModules from UHH2/common, does stuff like jet-lepton-cleaning, applying JECs etc.
     * +++++
     */

    CommonModules* commonObjectCleaning = new CommonModules();
    commonObjectCleaning->set_jet_id(PtEtaCut(30.0,2.4));
    commonObjectCleaning->disable_jersmear();
    // commonObjectCleaning->set_electron_id(AndId<Electron>(ElectronID_PHYS14_25ns_medium_noIso,PtEtaCut(20.0, 2.4)));
    // commonObjectCleaning->set_muon_id(AndId<Muon>(MuonIDTight(),PtEtaCut(20.0, 2.4)));
    // commonObjectCleaning->switch_jetlepcleaner(true);
    commonObjectCleaning->switch_jetPtSorter(true);
    commonObjectCleaning->init(ctx);
    v_modules.emplace_back(commonObjectCleaning);


    /* +++++
     * Several modules that usually take the name of a standard collection (e.g. "jets", "electrons") or self-produced collection
     * (e.g. "toptags", "b_jets") and produce a handle on either a simple type or a newly produced collection.
     * 
     * Example: - STCalculator (below) produces a handle on a float with handle name "ST"
     *          - CollectionProducer<TYPE> takes a collection of TYPE as input (e.g. "jets") and produces a new collection of the
     *            same type filtering out certain elements based on an ID (e.g. JetId)
     *          - CollectionSizeProducer<TYPE> does the same as CollectionProducer but instead of producing a handle to a new
     *            collection it just produces a handle to an int with the number of elements from the input collection that passed
     *            the ID criterion (this can later be used to make a cut on)
     * +++++
     */

    v_modules.emplace_back(new PrimaryLepton(ctx, "PrimaryLepton", 99999., 50.)); 
    v_modules.emplace_back(new HTCalculator(ctx, boost::none, "HT"));
    v_modules.emplace_back(new STCalculator(ctx, "ST"));
    v_modules.emplace_back(new CollectionProducer<Jet>(ctx,
                "jets",
                "b_jets",
                JetId(CSVBTag(CSVBTag::WP_MEDIUM))
                ));
    v_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
                "jets",
                "n_btags",
                JetId(CSVBTag(CSVBTag::WP_MEDIUM))
                ));
    // cms top tags
    v_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "topjets",
                "toptags",
                TopJetId(AndId<TopJet>(PtEtaCut(400., 2.4), CMSTopTag()))
                ));

    // check if there is exactly 1 Top Tag; if yes, make sure that all higgs tags are
    // well separated from it by making a dR requirement of 1.5
    v_modules.emplace_back(new XTopTagProducer(ctx, "toptags", "min_dr_higgs", "one_top", 1.5, 1));
    v_modules.emplace_back(new XTopTagProducer(ctx, "toptags", "dummy_dr", "two_top", -999., 2));

    // higgs tags, no top separation
    v_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "patJetsCa15CHSJetsFilteredPacked_daughters",
                "higgs_tags_ca15",
                TopJetId(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)))
                ));
    v_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "patJetsAk8CHSJetsSoftDropPacked_daughters",
                "higgs_tags_ak8",
                TopJetId(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)))
                ));

    // higgs tags, with top separation
    v_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "patJetsCa15CHSJetsFilteredPacked_daughters",
                "higgs_tags_ca15_notop",
                TopJetId(AndId<TopJet>(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)),
                    MinMaxDeltaRId<TopJet>(ctx, "toptags", "min_dr_higgs")))
                ));
    v_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "patJetsAk8CHSJetsSoftDropPacked_daughters",
                "higgs_tags_ak8_notop",
                TopJetId(AndId<TopJet>(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)),
                    MinMaxDeltaRId<TopJet>(ctx, "toptags", "min_dr_higgs")))
                ));

    // check if, in case there is only one top, the dR to the closest higgs is really 1.5
    // ---> THIS IS JUST FOR TESTING PURPOSES AND NOT NECESSARY FOR THE ACTUAL ANALYSIS!
    v_modules.emplace_back(new MinDeltaRProducer<TopJet, TopJet>(ctx, "one_top", "higgs_tags_ca15_notop", "min_deltaR_top_higgsak8notop"));
    v_modules.emplace_back(new MinDeltaRProducer<TopJet, TopJet>(ctx, "one_top", "higgs_tags_ca15", "min_deltaR_top_higgsak8"));
    v_modules.emplace_back(new MinDeltaRProducer<TopJet, TopJet>(ctx, "two_top", "higgs_tags_ca15_notop", "min_deltaR_top_higgsak8notop_twotop"));
    v_modules.emplace_back(new MinDeltaRProducer<TopJet, TopJet>(ctx, "two_top", "higgs_tags_ca15", "min_deltaR_top_higgsak8_twotop"));
    
    

    // additional b-tags
    v_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
                "b_jets",
                "n_additional_btags",
                JetId(AndId<Jet>(MinMaxDeltaRId<TopJet>(ctx, "higgs_tags_ak8_notop", 1.0, true),
                                    MinMaxDeltaRId<TopJet>(ctx, "toptags", 1.0, true)))
                ));

    // Other CutProducers
    v_modules.emplace_back(new NLeptonsProducer(ctx, "n_leptons"));
    v_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx, "jets", "n_jets"));

    v_modules.emplace_back(new PartPtProducer<Jet>(ctx, "jets", "leading_jet_pt", 1));
    v_modules.emplace_back(new PartPtProducer<Jet>(ctx, "jets", "subleading_jet_pt", 2));

    // get pt of the top tagged jet with smallest pt, just to see if PtEtaCut Id is working
    // ---> THIS IS JUST FOR TESTING PURPOSES AND NOT NECESSARY FOR THE ACTUAL ANALYSIS!
    v_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "toptags", "smallest_pt_toptags", -1));

    v_modules.emplace_back(new LeptonPtProducer(ctx, "PrimaryLepton", "primary_lepton_pt"));

    // produces handles on the values relevant for the 2D-cut i.e. dR(lep, closest jet), pt_rel(lep, closest jet)
    v_modules.emplace_back(new TwoDCutProducer(ctx));

    // produces a handle with 0/1 corresponding to whether event passed trigger requirements (see VLQ_triggerPaths.h) or not
    if (version == "Run2015B_Mu") {
        v_modules.emplace_back(new TriggerAcceptProducer(ctx, QCDTEST_MUON_TRIGGER_PATHS_DATA, "trigger_accept"));
    } else if (version == "Run2015B_Ele") {
        v_modules.emplace_back(new TriggerAcceptProducer(ctx, {}, "trigger_accept"));
    } else if (version == "Run2015B_Had") {
        v_modules.emplace_back(new TriggerAcceptProducer(ctx, {}, "trigger_accept"));
    } else {
        v_modules.emplace_back(new TriggerAcceptProducer(ctx, QCDTEST_MUON_TRIGGER_PATHS, "trigger_accept"));
    }

    /* +++++
     * make_modules_and_selitem (from VLQToHiggsPairProd/include/VLQPair_additionalModules.h) makes CollectionProducers,
     * CollectionSizeProducers and puts a corresponding SelItem into the SelItem vector, here SEL_ITEMS_VLQPair_loose
     * (see VLQPair_selectionItems.h)
     * +++++
     */

    SEL_ITEMS_VLQPair_loose = SEL_ITEMS_VLQPair_loose_base;
    
    unsigned insert_sel = 8;

    make_modules_and_selitem("higgs_tags_ca15", ctx, v_modules, SEL_ITEMS_VLQPair_loose, insert_sel);
    make_modules_and_selitem("higgs_tags_ca15_notop", ctx, v_modules, SEL_ITEMS_VLQPair_loose, insert_sel);
    make_modules_and_selitem("higgs_tags_ak8", ctx, v_modules, SEL_ITEMS_VLQPair_loose, insert_sel);
    make_modules_and_selitem("higgs_tags_ak8_notop", ctx, v_modules, SEL_ITEMS_VLQPair_loose, insert_sel);
    make_modules_and_selitem("toptags", ctx, v_modules, SEL_ITEMS_VLQPair_loose, insert_sel);
    make_modules_and_selitem("patJetsCa15CHSJetsFilteredPacked_daughters", ctx, v_modules, SEL_ITEMS_VLQPair_loose, insert_sel);
    make_modules_and_selitem("patJetsAk8CHSJetsSoftDropPacked_daughters", ctx, v_modules, SEL_ITEMS_VLQPair_loose, insert_sel);
    make_modules_and_selitem("topjets", ctx, v_modules, SEL_ITEMS_VLQPair_loose, insert_sel);
    
    /* +++++
     * Set up the SelItemsHelper which takes as input the SelItems vector (SEL_ITEMS_VLQPair_loose) and is needed by several
     * other modules to make selection and histogram producers
     * +++++
     */

    SelItemsHelper sel_helper(SEL_ITEMS_VLQPair_loose, ctx);
    sel_helper.declare_items_for_output();
    sel_module.reset(new SelectionProducer(ctx, sel_helper));


    // Set up Hists classes:

    sel_helper.fill_hists_vector(v_hists, "NoSelection");
    auto nm1_hists = new Nm1SelHists(ctx, "Nm1Selection", sel_helper);
    auto cf_hists = new VLQ2HTCutflow(ctx, "Cutflow", sel_helper);
    auto stsel_hists = new SelectedSelHists(ctx, "OnlySTCut", sel_helper, {"ST"});
    auto trigsel_hists = new SelectedSelHists(ctx, "OnlyTriggerCut", sel_helper, {"trigger_accept"});
    auto btagsel_hists = new SelectedSelHists(ctx, "OnlyBTagCut", sel_helper, {"n_btags"});
    v_hists.emplace_back(nm1_hists);
    v_hists.emplace_back(cf_hists);
    v_hists.emplace_back(stsel_hists);
    v_hists.emplace_back(trigsel_hists);
    v_hists.emplace_back(btagsel_hists);
    sel_helper.fill_hists_vector(v_hists_after_sel, "PostSelection");

    if (type == "MC") {
        v_hists.emplace_back(new HistCollector(ctx, "EventHistsPre"));
        v_hists_after_sel.emplace_back(new HistCollector(ctx, "EventHistsPost"));
    } else {
        v_hists.emplace_back(new HistCollector(ctx, "EventHistsPre", false));
        v_hists_after_sel.emplace_back(new HistCollector(ctx, "EventHistsPost", false));
    }

    // append 2D cut
    unsigned pos_2d_cut = 5;
    // sel_module->insert_selection(pos_2d_cut, new TwoDCutSel(ctx, DR_2D_CUT_PRESEL, DPT_2D_CUT_PRESEL));
    // nm1_hists->insert_hists(pos_2d_cut, new TwoDCutHist(ctx, "Nm1Selection"));
    // cf_hists->insert_step(pos_2d_cut, "2D cut");
    v_hists.insert(v_hists.begin() + pos_2d_cut, move(unique_ptr<Hists>(new TwoDCutHist(ctx, "NoSelection"))));
    v_hists_after_sel.insert(v_hists_after_sel.begin() + pos_2d_cut, move(unique_ptr<Hists>(new TwoDCutHist(ctx, "PostSelection"))));


}


bool TpTpLooseSelection::process(Event & event) {
 
    /* +++++
     * Check the final state i.e. the decay mode of the T' pair; in order to split up your sample according to the final state,
     * you have to specify (for each mass point) six InputData items in your xml config file, each with a different version according
     * to the possible final states. Then, using the code below, the event is only processed further (and written out) if it
     * corresponds to the version given in the InputData element.
     * +++++
     */

    if (version.substr(version.size() - 5, 100) == "_thth") {
        if (!checkDecayMode(event, ParticleID::TopID, ParticleID::HiggsID,
                    ParticleID::TopID, ParticleID::HiggsID)) {
            return false;
        }
    }
    if (version.substr(version.size() - 5, 100) == "_thtz") {
        if (!checkDecayMode(event, ParticleID::TopID, ParticleID::HiggsID,
                    ParticleID::TopID, ParticleID::ZID)) {
            return false;
        }
    }
    if (version.substr(version.size() - 5, 100) == "_thbw") {
        if (!checkDecayMode(event, ParticleID::TopID, ParticleID::HiggsID,
                    ParticleID::BottomID, ParticleID::WID)) {
            return false;
        }
    }
    if (version.substr(version.size() - 5, 100) == "_tztz") {
        if (!checkDecayMode(event, ParticleID::TopID, ParticleID::ZID,
                    ParticleID::TopID, ParticleID::ZID)) {
            return false;
        }
    }
    if (version.substr(version.size() - 5, 100) == "_tzbw") {
        if (!checkDecayMode(event, ParticleID::TopID, ParticleID::ZID,
                    ParticleID::BottomID, ParticleID::WID)) {
            return false;
        }
    }
    if (version.substr(version.size() - 5, 100) == "_bwbw") {
        if (!checkDecayMode(event, ParticleID::BottomID, ParticleID::WID,
                    ParticleID::BottomID, ParticleID::WID)) {
            return false;
        }
    }

    // run all modules
    for (auto & mod : v_modules) {
        mod->process(event);
    }

    // run selection
    bool all_accepted = sel_module->process(event);

    // fill histograms
    if (all_accepted) {
        for (auto & hist : v_hists_after_sel) {
            hist->fill(event);
        }
    }

    // all hists
    for (auto & hist : v_hists) {
        hist->fill(event);
    }

    // decide whether or not to keep the current event in the output:
    return all_accepted;
    // return true;
}

UHH2_REGISTER_ANALYSIS_MODULE(TpTpLooseSelection)
