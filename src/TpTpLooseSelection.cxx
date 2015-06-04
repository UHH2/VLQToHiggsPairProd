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
#include "UHH2/VLQToHiggsPairProd/include/VLQToHiggsPairProdSelections.h"
#include "UHH2/VLQToHiggsPairProd/include/VLQPair_selectionItems.h"


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
    string version;
    // modules for setting up collections and cleaning
    vector<unique_ptr<AnalysisModule>> v_pre_modules;
    unique_ptr<AnalysisModule> sel_module;
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
    v_pre_modules.emplace_back(new ElectronCleaner(PtEtaCut(105.0, 2.4)));
    v_pre_modules.emplace_back(new MuonCleaner(PtEtaCut(50.0, 2.4)));
    v_pre_modules.emplace_back(new JetCleaner(PtEtaCut(30.0, 2.4))); // get rid of fwd jets from preselection
    // v_pre_modules.emplace_back(new BJetsProducer(ctx, CSVBTag::WP_MEDIUM, "b_jets"));
    v_pre_modules.emplace_back(new PrimaryLepton(ctx)); // TODO: put PrimaryLepton module (currently in TTbarReconstruction) into own file; current handle name is "PrimaryLepton"
    v_pre_modules.emplace_back(new HTCalculator(ctx, boost::none, "HT"));
    v_pre_modules.emplace_back(new STCalculator(ctx, "ST"));
    // v_pre_modules.emplace_back(new CollectionProducer<Jet>(ctx,
    //             CSVBTag(CSVBTag::WP_MEDIUM),
    //             "jets",
    //             "b_jets"));
    // v_pre_modules.emplace_back(new NBTagProducer(ctx, CSVBTag::WP_MEDIUM, "n_btags"));
    v_pre_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
                "jets",
                "n_btags",
                JetId(CSVBTag(CSVBTag::WP_MEDIUM))
                ));
    v_pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "topjets",
                "h_boost_topjets",
                TopJetId(PtEtaCut(400., 2.4))
                ));
    v_pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "patJetsCa15CHSJetsFilteredPacked",
                "n_higgs_tags_ca15",
                TopJetId(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)))
                ));
    v_pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "patJetsCa8CHSJetsPrunedPacked",
                "n_higgs_tags_ca8",
                TopJetId(HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)))
                ));
    v_pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "h_boost_topjets",
                "n_toptags",
                TopJetId(CMSTopTag())
                ));
    // v_pre_modules.emplace_back(new NTaggedTopJetProducer(ctx, HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)),
    //                                                      "n_higgs_tags", "patJetsCa15CHSJetsFilteredPacked"));
    // v_pre_modules.emplace_back(new TaggedTopJetProducer(ctx, HiggsTag(60.f, 99999., CSVBTag(CSVBTag::WP_LOOSE)),
    //                                                     "h_jets", "patJetsCa15CHSJetsFilteredPacked"));
    // v_pre_modules.emplace_back(new NLeadingBTagProducer(ctx, CSVBTag::WP_MEDIUM, "n_leading_btags"));
    // TODO : 2d-cut

    // Other CutProducers
    v_pre_modules.emplace_back(new TriggerAcceptProducer(ctx,
                    {"HLT_Ele95_CaloIdVT_GsfTrkIdT_v*", "HLT_Mu40_v*"},
                    "trigger_accept"));
    v_pre_modules.emplace_back(new NLeptonsProducer(ctx, "n_leptons"));
    v_pre_modules.emplace_back(new LeadingJetPtProducer(ctx, "leading_jet_pt"));

    v_pre_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx, "jets", "n_jets"));
    // v_pre_modules.emplace_back(new NFwdJetsProducer(ctx));
    // v_pre_modules.emplace_back(new SubleadingJetPtProducer(ctx));
    v_pre_modules.emplace_back(new LeptonPtProducer(ctx, "primary_lepton_pt"));

    // v_pre_modules.emplace_back(new LorentzVectorInfoProducer(ctx, "tlep"));
    // v_pre_modules.emplace_back(new LorentzVectorInfoProducer(ctx, "h"));
    // v_pre_modules.emplace_back(new LorentzVectorInfoProducer(ctx, "vlq"));

    // Selection Producer
    SelItemsHelper sel_helper(SEL_ITEMS_VLQPair, ctx);
    sel_helper.declare_items_for_output();
    sel_module.reset(new SelectionProducer(ctx, sel_helper));

    // 3. Set up Hists classes:

    // TODO: set up and fill other histogram classes, e.g. your own HistCollector stuff

    sel_helper.fill_hists_vector(v_hists, "SelNone");
    v_hists.emplace_back(new Nm1SelHists(ctx, "SelNm1", sel_helper));
    v_hists.emplace_back(new VLQ2HTCutflow(ctx, "Cutflow", sel_helper));
    v_hists.emplace_back(new HistCollector(ctx, "EventHistsPre"));

    v_hists_after_sel.emplace_back(new HistCollector(ctx, "EventHistsPost"));


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


bool TpTpLooseSelection::process(Event & event) {

    // cout << "TpTpLooseSelection: Starting to process event (runid, eventid) = (" << event.run << ", " << event.event << ")" << endl;

    // TEST STUFF HERE



    // FIRST RUN PRE_MODULES THAT NEED TO RUN AT THE BEGINNING (e.g. MC lumi re-weighting)

    // if (gen_hists) {
    //     gen_hists->fill(event);
    // }
 
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
}

UHH2_REGISTER_ANALYSIS_MODULE(TpTpLooseSelection)
