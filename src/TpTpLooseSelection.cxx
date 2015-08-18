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



#include "UHH2/VLQSemiLepPreSel/include/EventHists.h"
#include "UHH2/VLQSemiLepPreSel/include/CustomizableGenHists.h"
#include "UHH2/VLQSemiLepPreSel/include/VLQCommonModules.h"
#include "UHH2/VLQSemiLepPreSel/include/SelectionHists.h"
#include "UHH2/VLQSemiLepPreSel/include/SelectionItem.h"
#include "UHH2/VLQSemiLepPreSel/include/VLQSLPS_selectionItems.h"
#include "UHH2/VLQToHiggsPairProd/include/VLQToHiggsPairProdSelections.h"
// // #include "UHH2/VLQToHiggsPairProd/include/VLQToHiggsPairProdHists.h"
#include "UHH2/VLQToHiggsPairProd/include/VLQPair_selectionItems.h"
#include "UHH2/VLQToHiggsPairProd/include/VLQPair_additionalModules.h"



using namespace std;
using namespace uhh2;

using namespace vlqToHiggsPair;

enum ParticleID {
    BottomID = 5,
    TopID = 6,
    TprimeID = 8,
    ElectronID = 11,
    MuonID = 13,
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
    unique_ptr<SelectionProducer> sel_module;
    // unique_ptr<AnalysisModule> writer_module; // for TMVA stuff

    // store the Hists collection
    unique_ptr<Hists> gen_hists;
    vector<unique_ptr<Hists>> v_hists;
    vector<unique_ptr<Hists>> v_hists_after_sel;
};


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
    
    // 1. setup modules to prepare the event.

    // EventWeightOutputHandle only needed for TMVA studies
    // v_pre_modules.emplace_back(new EventWeightOutputHandle(ctx));


    // =====DISABLED FOR RUN II=====:
    // don't do stuff like mclumiweight manually, instead run an instance of
    // CommonModules which is regularly maintained and takes care of data as well
    // 
    // bool mclumiweight = true;
    // bool mcpileupreweight = true;

    // if(mclumiweight)  v_pre_modules.emplace_back(new MCLumiWeight(ctx));
    // if(mcpileupreweight) v_pre_modules.emplace_back(new MCPileupReweight(ctx));
    // v_pre_modules.emplace_back(new ElectronCleaner(PtEtaCut(105.0, 2.4)));
    // v_pre_modules.emplace_back(new MuonCleaner(PtEtaCut(50.0, 2.1))); // TODO: put the eta cut to 2.1???
    // v_pre_modules.emplace_back(new JetCleaner(PtEtaCut(30.0, 2.4))); // get rid of fwd jets from preselection
    // v_pre_modules.emplace_back(new PtSorter<Jet>(ctx, "jets"));
    // v_pre_modules.emplace_back(new PtSorter<Muon>(ctx, "muons"));
    // v_pre_modules.emplace_back(new PtSorter<Electron>(ctx, "electrons"));

    // =====ADDED FOR RUN II======:
    // what CommonModules now does:
    // * remove forward jets (eta > 2.4) and sort jets again
    // * apply MC pileupreweight and lumiweight
    // * apply JEC and JER smearing (if not already done, should throw warning if that's the case)
    // * does LumiSelection, so only allows good events

    CommonModules* commonObjectCleaning = new CommonModules();
    commonObjectCleaning->set_jet_id(PtEtaCut(30.0,2.4));
    commonObjectCleaning->disable_jersmear();
    // commonObjectCleaning->set_electron_id(AndId<Electron>(ElectronID_PHYS14_25ns_medium_noIso,PtEtaCut(20.0, 2.4)));
    // commonObjectCleaning->set_muon_id(AndId<Muon>(MuonIDTight(),PtEtaCut(20.0, 2.4)));
    // commonObjectCleaning->switch_jetlepcleaner(true);
    commonObjectCleaning->switch_jetPtSorter(true);
    commonObjectCleaning->init(ctx);
    v_pre_modules.emplace_back(commonObjectCleaning);

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
                "patJetsCa15CHSJetsFilteredPacked_daughters",
                "higgs_tags_ca15",
                TopJetId(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)))
                ));
    v_pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "patJetsCa15CHSJetsFilteredPacked_daughters",
                "n_higgs_tags_ca15",
                TopJetId(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)))
                ));
    v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "patJetsAk8CHSJetsSoftDropPacked_daughters",
                "higgs_tags_ak8",
                TopJetId(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)))
                ));
    v_pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "patJetsAk8CHSJetsSoftDropPacked_daughters",
                "n_higgs_tags_ak8",
                TopJetId(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)))
                ));

    // higgs tags, with top separation
    v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "patJetsCa15CHSJetsFilteredPacked_daughters",
                "higgs_tags_ca15_notop",
                TopJetId(AndId<TopJet>(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)),
                    MinMaxDeltaRId<TopJet>(ctx, "toptags", "min_dr_higgs")))
                ));
    v_pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "patJetsCa15CHSJetsFilteredPacked_daughters",
                "n_higgs_tags_ca15_notop",
                TopJetId(AndId<TopJet>(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)),
                    MinMaxDeltaRId<TopJet>(ctx, "toptags", "min_dr_higgs")))
                ));
    v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "patJetsAk8CHSJetsSoftDropPacked_daughters",
                "higgs_tags_ak8_notop",
                TopJetId(AndId<TopJet>(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)),
                    MinMaxDeltaRId<TopJet>(ctx, "toptags", "min_dr_higgs")))
                ));
    v_pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "patJetsAk8CHSJetsSoftDropPacked_daughters",
                "n_higgs_tags_ak8_notop",
                TopJetId(AndId<TopJet>(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)),
                    MinMaxDeltaRId<TopJet>(ctx, "toptags", "min_dr_higgs")))
                ));

    // check if, in case there is only one top, the dR to the closest higgs is really 1.5
    v_pre_modules.emplace_back(new MinDeltaRProducer<TopJet, TopJet>(ctx, "one_top", "higgs_tags_ca15_notop", "min_deltaR_top_higgsak8notop"));
    v_pre_modules.emplace_back(new MinDeltaRProducer<TopJet, TopJet>(ctx, "one_top", "higgs_tags_ca15", "min_deltaR_top_higgsak8"));
    v_pre_modules.emplace_back(new MinDeltaRProducer<TopJet, TopJet>(ctx, "two_top", "higgs_tags_ca15_notop", "min_deltaR_top_higgsak8notop_twotop"));
    v_pre_modules.emplace_back(new MinDeltaRProducer<TopJet, TopJet>(ctx, "two_top", "higgs_tags_ca15", "min_deltaR_top_higgsak8_twotop"));


    

    // additional b-tags
    v_pre_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
                "b_jets",
                "n_additional_btags",
                JetId(AndId<Jet>(MinMaxDeltaRId<TopJet>(ctx, "higgs_tags_ak8_notop", 1.0, true),
                                    MinMaxDeltaRId<TopJet>(ctx, "toptags", 1.0, true)))
                ));

    // mass producers
    v_pre_modules.emplace_back(new LeadingPartMassProducer<TopJet>(ctx,
                "higgs_tags_ca15",
                "mass_ld_higgs_tag_ca15"
                ));
    v_pre_modules.emplace_back(new LeadingPartMassProducer<TopJet>(ctx,
                "higgs_tags_ak8",
                "mass_ld_higgs_tag_ak8"
                ));
    v_pre_modules.emplace_back(new LeadingPartMassProducer<TopJet>(ctx,
                "higgs_tags_ca15_notop",
                "mass_ld_higgs_tag_ca15_notop"
                ));
    v_pre_modules.emplace_back(new LeadingPartMassProducer<TopJet>(ctx,
                "higgs_tags_ak8_notop",
                "mass_ld_higgs_tag_ak8_notop"
                ));
    v_pre_modules.emplace_back(new LeadingPartMassProducer<TopJet>(ctx,
                "toptags",
                "mass_ld_toptag"
                ));

    v_pre_modules.emplace_back(new LeadingTopjetMassProducer(ctx,
                "higgs_tags_ca15",
                "mass_sj_ld_higgs_tag_ca15"
                ));
    v_pre_modules.emplace_back(new LeadingTopjetMassProducer(ctx,
                "higgs_tags_ak8",
                "mass_sj_ld_higgs_tag_ak8"
                ));
    v_pre_modules.emplace_back(new LeadingTopjetMassProducer(ctx,
                "higgs_tags_ca15_notop",
                "mass_sj_ld_higgs_tag_ca15_notop"
                ));
    v_pre_modules.emplace_back(new LeadingTopjetMassProducer(ctx,
                "higgs_tags_ak8_notop",
                "mass_sj_ld_higgs_tag_ak8_notop"
                ));
    v_pre_modules.emplace_back(new LeadingTopjetMassProducer(ctx,
                "toptags",
                "mass_sj_ld_toptag"
                ));




    // Other CutProducers
    v_pre_modules.emplace_back(new NLeptonsProducer(ctx, "n_leptons"));
    v_pre_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx, "jets", "n_jets"));

    v_pre_modules.emplace_back(new PartPtProducer<Jet>(ctx, "jets", "leading_jet_pt", 1));
    v_pre_modules.emplace_back(new PartPtProducer<Jet>(ctx, "jets", "subleading_jet_pt", 2));
    v_pre_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "topjets", "leading_topjet_pt", 1));
    v_pre_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "patJetsAk8CHSJetsSoftDropPacked_daughters", "leading_ak8jet_pt", 1));
    v_pre_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "patJetsCa15CHSJetsFilteredPacked_daughters", "leading_ca15jet_pt", 1));

    // get pt of the top tagged jet with smallest pt, just to see if PtEtaCut Id is working
    v_pre_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "toptags", "smallest_pt_toptags", -1));

    v_pre_modules.emplace_back(new LeptonPtProducer(ctx, "PrimaryLepton", "primary_lepton_pt"));
    v_pre_modules.emplace_back(new TwoDCutProducer(ctx));

    // v_pre_modules.emplace_back(new NeutrinoParticleProducer(ctx, NeutrinoReconstruction, "neutrino_part_vec", "PrimaryLepton"));
    // v_pre_modules.emplace_back(new MinDeltaRProducer<FlavorParticle, LorentzVector>(ctx, "PrimaryLepton", "neutrino_part_vec", "min_deltaR_lep_nu"));
    // v_pre_modules.emplace_back(new TwoParticleCollectionProducer<Jet>(ctx, "b_jets", "leading_b_jets"));
    // v_pre_modules.emplace_back(new MinDeltaRProducer<FlavorParticle, Jet>(ctx, "PrimaryLepton", "leading_b_jets", "min_deltaR_lep_bjets"));
    // v_pre_modules.emplace_back(new DeltaRTwoLeadingParticleProducer<Jet>(ctx, "leading_b_jets", "deltaR_leading_bjets"));

    // N Gen Leptons Producer

    // v_pre_modules.emplace_back(new CollectionSizeProducer<GenParticle>(ctx, "genparticles", "n_genleptons",
    //             GenParticleId(GenParticlePdgIdId({-11, 11, -13, 13}))));
    // v_pre_modules.emplace_back(new GenParticlesPrinter(ctx));

    
    // Selection Producer
    SelItemsHelper sel_helper(SEL_ITEMS_VLQPair_loose, ctx);
    sel_helper.declare_items_for_output();
    sel_module.reset(new SelectionProducer(ctx, sel_helper));

    // 3. Set up Hists classes:

    // TODO: set up and fill other histogram classes, e.g. your own HistCollector stuff

    sel_helper.fill_hists_vector(v_hists, "NoSelection");
    auto nm1_hists = new Nm1SelHists(ctx, "Nm1Selection", sel_helper);
    auto cf_hists = new VLQ2HTCutflow(ctx, "Cutflow", sel_helper);
    v_hists.emplace_back(nm1_hists);
    v_hists.emplace_back(cf_hists);
    sel_helper.fill_hists_vector(v_hists_after_sel, "PostSelection");

    if (type == "MC") {
        v_hists.emplace_back(new HistCollector(ctx, "EventHistsPre"));
        v_hists_after_sel.emplace_back(new HistCollector(ctx, "EventHistsPost"));
    } else {
        v_hists.emplace_back(new HistCollector(ctx, "EventHistsPre", false));
        v_hists_after_sel.emplace_back(new HistCollector(ctx, "EventHistsPost", false));
    }

    // append 2D cut
    unsigned pos_2d_cut = 4;
    // sel_module->insert_selection(pos_2d_cut, new TwoDCutSel(ctx, DR_2D_CUT_PRESEL, DPT_2D_CUT_PRESEL));
    // nm1_hists->insert_hists(pos_2d_cut, new TwoDCutHist(ctx, "Nm1Selection"));
    // cf_hists->insert_step(pos_2d_cut, "2D cut");
    v_hists.insert(v_hists.begin() + pos_2d_cut, move(unique_ptr<Hists>(new TwoDCutHist(ctx, "NoSelection"))));
    v_hists_after_sel.insert(v_hists_after_sel.begin() + pos_2d_cut, move(unique_ptr<Hists>(new TwoDCutHist(ctx, "PostSelection"))));

    // h_ngenleps = ctx.get_handle<int>("n_genleptons");

    //=====FOR RUN II=====:
    // implement:
    // * 2d-cut hists
    // * trigger efficiency hists (?)

    // v_pre_modules.emplace_back(new TriggerAcceptProducer(ctx,
    //                 PRESEL_TRIGGER_PATHS,
    //                 "trigger_accept"));
    // v_pre_modules.emplace_back(new NeutrinoParticleProducer(ctx, NeutrinoReconstruction, "neutrino_part_vec", "PrimaryLepton"));
    // v_pre_modules.emplace_back(new MinDeltaRProducer<FlavorParticle, LorentzVector>(ctx, "PrimaryLepton", "neutrino_part_vec", "min_deltaR_lep_nu"));
    // v_pre_modules.emplace_back(new TwoParticleCollectionProducer<Jet>(ctx, "b_jets", "leading_b_jets"));
    // v_pre_modules.emplace_back(new MinDeltaRProducer<FlavorParticle, Jet>(ctx, "PrimaryLepton", "leading_b_jets", "min_deltaR_lep_bjets"));
    // v_pre_modules.emplace_back(new DeltaRTwoLeadingParticleProducer<Jet>(ctx, "leading_b_jets", "deltaR_leading_bjets"));


}


bool TpTpLooseSelection::process(Event & event) {

    // cout << "TpTpLooseSelection: Starting to process event (runid, eventid) = (" << event.run << ", " << event.event << ")" << endl;

    // TEST STUFF HERE
 
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
    for (auto & mod : v_pre_modules) {
        mod->process(event);
    }

    // run selection
    bool all_accepted = sel_module->process(event);

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

    // all hists
    for (auto & hist : v_hists) {
        hist->fill(event);
    }

    // decide whether or not to keep the current event in the output:
    return all_accepted;
    // return true;
}

UHH2_REGISTER_ANALYSIS_MODULE(TpTpLooseSelection)
