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
#include "UHH2/VLQToHiggsPairProd/include/TpTpCommonModules.h"
#include "UHH2/VLQToHiggsPairProd/include/TpTpAnalysisModule.h"

using namespace std;
using namespace uhh2;

// using namespace vlqToHiggsPair;

// typedef VectorAndSelection MyAndSelection;

class TpTpFinalSelectionV2: public TpTpAnalysisModule {
public:

    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_BASELINE_SEL {
        // shared_ptr<SelectionItem>(new SelDatD("ST", "ST", 45, 0, 4500, 700)),
        // shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 8, -.5, 7.5, 3)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak8_jet", "Pt leading Ak8 Jet", 60, 0., 1500., 300.))

        // shared_ptr<SelectionItem>(new SelDatD("HT", "HT", 25, 0, 4500));
        // shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 8, -.5, 7.5, 3)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak8_jet", "Pt leading Ak8 Jet", 60, 0., 1500., 300.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak8_jet_cleaned", "Pt leading Ak8 Jet", 60, 0., 1500.)),
        // shared_ptr<SelectionItem>(new SelDatF("primary_muon_pt_dRak8", "Primary Muon (dRak8) p_T", 90, 0., 900.))
    };

    explicit TpTpFinalSelectionV2(Context & ctx);
    virtual bool process(Event & event) override;

private:
    unique_ptr<AnalysisModule> common_module;
    unique_ptr<NParticleMultiHistProducerHelper<TopJet>> ak8jet_hists/*, ca15jet_hists*/;

};




TpTpFinalSelectionV2::TpTpFinalSelectionV2(Context & ctx) : TpTpAnalysisModule(ctx) {

    CommonModules* commonObjectCleaning = new CommonModules();
    // commonObjectCleaning->set_jet_id(AndId<Jet>(JetPFID(JetPFID::WP_LOOSE), PtEtaCut(30.0,2.4)));
    commonObjectCleaning->disable_jersmear();
    // commonObjectCleaning->disable_mcpileupreweight();
    // commonObjectCleaning->set_electron_id(AndId<Electron>(ElectronID_Spring15_25ns_medium_noIso,PtEtaCut(20.0, 2.4)));
    // commonObjectCleaning->set_muon_id(AndId<Muon>(MuonIDTight(),PtEtaCut(20.0, 2.1)));
    // commonObjectCleaning->switch_jetlepcleaner(true);
    // commonObjectCleaning->switch_jetPtSorter(true);
    // commonObjectCleaning->disable_lumisel();
    commonObjectCleaning->init(ctx);
    common_module.reset(commonObjectCleaning);
    
    // check if there is exactly 1 Top Tag; if yes, make sure that all higgs tags are
    // well separated from it by making a dR requirement of 1.5
    other_modules.emplace_back(new TriggerAcceptProducer(ctx, {"HLT_Mu45_eta2p1_v*"}, "trigger_accept"));other_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "topjets", "pt_ld_ak8_jet", 1));
    other_modules.emplace_back(new PartPtProducer<TopJet>(ctx, "topjets", "pt_ld_ak8_jet", 1));
    other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "topjets",
                "n_ak8"
                ));
    
    ak8jet_hists.reset(new NParticleMultiHistProducerHelper<TopJet>("Ak8SoftDropSlimmed", "topjets", vector<string>{"n", "pt", "eta", "phi", "mass_sj", "n_subjets"}));

    // boosted Ak8 jets
    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "topjets",
                "ak8_boost",
                TopJetId(PtEtaCut(300., 2.4))
                ));
    ak8jet_hists->add_level("Boosted_second", "ak8_boost", vector<string>{"pt", "eta", "mass_sj", "tau21", "tau32", "n_sjbtags-loose", "n_sjbtags-medium"}, 2);
    ak8jet_hists->add_level("Boosted_first", "ak8_boost", vector<string>{"n", "pt", "eta", "mass_sj", "tau21", "tau32", "n_sjbtags-loose", "n_sjbtags-medium"}, 1);

    // CMSTopTagsV2
    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost",
                "ak8_tau32",
                TopJetId(Tau32(0.86))
                ));
    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_tau32",
                "cmstoptagsv2",
                TopJetId(Type2TopTag(110., 210., Type2TopTag::MassType::groomed))
                ));
    // ak8jet_hists->at("Boosted_first").add_level("tau32_cut", "ak8_tau32", vector<string>{"n", "pt", "eta", "mass_sj", "tau21", "tau32", "csv_max_sj"});
    // ak8jet_hists->at("Boosted_first").add_level("cmstoptagsv2", "cmstoptagsv2", vector<string>{"n", "pt", "eta", "mass_sj", "tau21", "tau32", "csv_max_sj"});

    // HepTopTagsV2
    // other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
    //             "patJetsHepTopTagCHSPacked_daughters",
    //             "ca15_boost",
    //             TopJetId(PtEtaCut(400., 2.4))
    //             ));
    // other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
    //             "ca15_boost",
    //             "ca15_tau32",
    //             TopJetId(Tau32(0.92))
    //             ));
    // other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
    //             "ca15_tau32",
    //             "heptoptagsv2",
    //             TopJetId(HEPTopTagV2(60., 200., 0.5))
    //             ));
    // ca15jet_hists.reset(new NParticleMultiHistProducerHelper<TopJet>("Ca15HepTopTagJets", "patJetsHepTopTagCHSPacked_daughters", vector<string>{"pt", "eta", "phi", "mass_sj", "n_subjets"}));
    // ca15jet_hists->at("Ca15HepTopTagJets").add_level("Boosted_second", "ca15_boost", vector<string>{"pt", "eta", "mass_sj", "tau21", "tau32", "n_sjbtags-loose", "n_sjbtags-medium"}, 2);
    // ca15jet_hists->at("Ca15HepTopTagJets").add_level("Boosted_first", "ca15_boost", vector<string>{"pt", "eta", "mass_sj", "tau21", "tau32", "n_sjbtags-loose", "n_sjbtags-medium"}, 1);
    // ca15jet_hists->at("Ca15HepTopTagJets").at("Boosted_first").add_level("tau32_cut", "ca15_tau32", vector<string>{"pt", "eta", "mass_sj", "tau21", "tau32", "csv_max_sj"});
    // ca15jet_hists->at("Ca15HepTopTagJets").at("Boosted_first").add_level("heptoptagsv2", "heptoptagsv2", vector<string>{"pt", "eta", "mass_sj", "tau21", "tau32", "csv_max_sj"});

    // b-tagged Ak8 jets
    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost",
                "ak8_boost_1b_med",
                TopJetId(HiggsFlexBTag(0., 99999., CSVBTag(CSVBTag::WP_MEDIUM)))
                ));
    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost",
                "ak8_boost_2b_med",
                TopJetId(HiggsFlexBTag(0., 99999., CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)))
                ));
    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost",
                "ak8_boost_2b_loose",
                TopJetId(HiggsFlexBTag(0., 99999., CSVBTag(CSVBTag::WP_LOOSE), CSVBTag(CSVBTag::WP_LOOSE)))
                ));
    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost",
                "ak8_boost_higgsmass",
                TopJetId(HiggsFlexBTag(60., 150.))
                ));
    ak8jet_hists->at("Boosted_first").add_level("one_subjet_btags_med", "ak8_boost_1b_med", vector<string>{"n", "pt", "eta", "mass_sj", "tau21"});
    ak8jet_hists->at("Boosted_first").add_level("two_subjet_btags_med", "ak8_boost_2b_med", vector<string>{"n", "pt", "eta", "mass_sj", "tau21"});
    ak8jet_hists->at("Boosted_first").add_level("two_subjet_btags_loose", "ak8_boost_2b_loose", vector<string>{"n", "pt", "eta", "mass_sj", "tau21"});
    ak8jet_hists->at("Boosted_first").add_level("higgs_mass", "ak8_boost_higgsmass", vector<string>{"n", "pt", "eta", "mass_sj", "tau21", "n_sjbtags-loose", "n_sjbtags-medium"});

    // higgs tags, with mass cuts
    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost_1b_med",
                "higgs_tags_1b_med",
                TopJetId(HiggsFlexBTag(60., 150.))
                ));
    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost_2b_med",
                "higgs_tags_2b_med",
                TopJetId(HiggsFlexBTag(60., 150.))
                ));
    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost_2b_loose",
                "higgs_tags_2b_loose",
                TopJetId(HiggsFlexBTag(60., 150.))
                ));
    // ak8jet_hists->at("Boosted_first").at("one_subjet_btags_med").add_level("Higgs-Tags", "higgs_tags_1b_med", vector<string>{"n", "pt", "eta", "mass_sj", "tau21", "n_sjbtags-medium"});
    // ak8jet_hists->at("Boosted_first").at("two_subjet_btags_med").add_level("Higgs-Tags", "higgs_tags_2b_med", vector<string>{"n", "pt", "eta", "mass_sj", "tau21", "n_sjbtags-medium"});
    // ak8jet_hists->at("Boosted_first").at("two_subjet_btags_loose").add_level("Higgs-Tags", "higgs_tags_2b_loose", vector<string>{"n", "pt", "eta", "mass_sj", "tau21", "n_sjbtags-medium"});
    

    // CollectionSizeProducer for cutting
    other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "topjets",
                "n_ak8"
                ));
    other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "higgs_tags_1b_med",
                "n_higgs_tags_1b_med"
                ));
    other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "higgs_tags_2b_med",
                "n_higgs_tags_2b_med"
                ));
    other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "higgs_tags_2b_loose",
                "n_higgs_tags_2b_loose"
                ));
    other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "cmstoptagsv2",
                "n_cmstoptagsv2"
                ));



    // check if there is exactly 1 Higgs Tag; if yes, make sure that all higgs tags are
    // well separated from it by making a dR requirement of 1.5
    other_modules.emplace_back(new XTopTagProducer(ctx, "toptags_boost", "min_dr_higgs", "one_top", 1.5, 1));
    other_modules.emplace_back(new XTopTagProducer(ctx, "toptags_boost", "dummy_dr", "two_top", -999., 2));
    
    other_modules.emplace_back(new MinDeltaRProducer<TopJet, TopJet>(ctx, "one_top", "ak8_boost_loose_2b_m60-150", "min_deltaR_top_higgs_ak8"));

    vector<string> final_states;
    if (version.find("TpTp") != string::npos)
        final_states = {"thth", "thtz", "thbw", "noH_tztz", "noH_tzbw", "noH_bwbw"};
    else
        final_states = {"All"};
        
    // vector<string> categories = split(ctx.get("category", ""));
    std::vector<string> categories = {"NoSelection", "HiggsTag0",
        "HiggsTag1bMed", "HiggsTag2bMed", "HiggsTag2bLoose",
        // "HiggsTag1bMed-1Top", "HiggsTag2bMed-1Top", "HiggsTag2bLoose-1Top"
        }; // "NoSelection"

    for (auto const & fs : final_states) {
        for (auto const & cat : categories) {

            SEL_ITEMS_FULL_SEL.push_back(SEL_ITEMS_BASELINE_SEL);

            if (fs ==  "All") {
                other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept_"+fs,
                    GenParticleId(TrueId<GenParticle>::is_true), GenParticleId(TrueId<GenParticle>::is_true)));
            }
            else if (fs ==  "thth") {
                other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept_"+fs,
                    GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::TopID, ParticleID::HiggsID)),
                    GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::TopID, ParticleID::HiggsID))
                    ));
            }
            else if (fs ==  "thtz") {
                other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept_"+fs,
                    GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::TopID, ParticleID::HiggsID)),
                    GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::TopID, ParticleID::ZID))
                    ));
            }
            else if (fs ==  "thbw") {
                other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept_"+fs,
                    GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::TopID, ParticleID::HiggsID)),
                    GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::BottomID, ParticleID::WID))
                    ));
            }
            else if (fs ==  "noH_tztz") {
                other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept_"+fs,
                    GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::TopID, ParticleID::ZID)),
                    GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::TopID, ParticleID::ZID))
                    ));
            }
            else if (fs ==  "noH_tzbw") {
                other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept_"+fs,
                    GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::TopID, ParticleID::ZID)),
                    GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::BottomID, ParticleID::WID))
                    ));
            }
            else if (fs ==  "noH_bwbw") {
                other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept_"+fs,
                    GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::BottomID, ParticleID::WID)),
                    GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::BottomID, ParticleID::WID))
                    ));
            }

            // if (split(cat, "-")[0] == "NoSelection") 
            //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("gendecay_accept_"+fs, "GenDecay Accept", 2, -.5, 1.5));
            // else
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("gendecay_accept_"+fs, "GenDecay Accept", 2, -.5, 1.5, 1));

            // if (split(cat, "-").size() > 1) {
            //     if (split(cat, "-")[1] == "1Top") {
            //         SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_cmstoptagsv2", "N(TopTagsV2)", 5, -.5, 4.5, 1));
            //     }
            //     else {
            //         SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_cmstoptagsv2", "N(TopTagsV2)", 5, -.5, 4.5, 0, 0));
            //     }
            // }

            string cut_collection = "higgs_tags_2b_loose";

            if (split(cat, "-")[0] == "NoSelection") {
                SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_ak8", "N(Ak8 Jets)", 8, -.5, 7.5));
            }
            else {
                SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_ak8", "N(Ak8 Jets)", 8, -.5, 7.5, 3));
            }


            // split(cat, "-")[0]
            if (split(cat, "-")[0] == "NoSelection") {
                SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 5, -.5, 4.5));
                SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 5, -.5, 4.5));
                SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_loose", "N(Higgs-Tags, 2 loose b)", 5, -.5, 4.5));
            }
            else if (split(cat, "-")[0] == "HiggsTag0") {
                SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_loose", "N(Higgs-Tags, 2 loose b)", 5, -.5, 4.5, 0, 0));
                SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 5, -.5, 4.5, 0, 0));
                SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 5, -.5, 4.5));
            }
            else if (split(cat, "-")[0] == "HiggsTag1bMed") {
                cut_collection = "higgs_tags_1b_med";
                SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 5, -.5, 4.5, 0, 0));
                SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 5, -.5, 4.5, 1));
                SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_loose", "N(Higgs-Tags, 2 loose b)", 5, -.5, 4.5));
            }
            else if (split(cat, "-")[0] == "HiggsTag2bMed") {
                cut_collection = "higgs_tags_2b_med";
                SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 5, -.5, 4.5, 1));
                SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 5, -.5, 4.5));
                SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_loose", "N(Higgs-Tags, 2 loose b)", 5, -.5, 4.5));
            }
            else if (split(cat, "-")[0] == "HiggsTag2bLoose") {
                SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_loose", "N(Higgs-Tags, 2 loose b)", 5, -.5, 4.5, 1));
                SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 5, -.5, 4.5));
                SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 5, -.5, 4.5));
            }

            // check if there is exactly 1 Higgs Tag; if yes, make sure that all higgs tags are
            // well separated from it by making a dR requirement of 0.6
            other_modules.emplace_back(new XTopTagProducer(ctx, cut_collection, "min_dr_"+cut_collection, "one_higgs_"+cut_collection, 0.6, 1));
            other_modules.emplace_back(new XTopTagProducer(ctx, cut_collection, "dummy_dr_"+cut_collection, "two_higgs_"+cut_collection, -999., 2));

            other_modules.emplace_back(new MinDeltaRProducer<TopJet, TopJet>(ctx, "one_higgs_"+cut_collection, "cmstoptagsv2", "min_dR_top_1_"+cut_collection));
            other_modules.emplace_back(new MinDeltaRProducer<TopJet, TopJet>(ctx, "two_higgs_"+cut_collection, "cmstoptagsv2", "min_dR_top_2_"+cut_collection));

            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("min_dR_top_1_"+cut_collection, "min deltaR(top, higgs)", 20, 0, 5.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("min_dR_top_2_"+cut_collection, "min deltaR(top, higgs)", 20, 0, 5.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_cmstoptagsv2", "N(Top Tags)", 5, -.5, 4.5));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatD("ST", "ST", 45, 0, 4500));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept", "Trigger Accept", 2, -.5, 1.5));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_muon_pt_noIso", "Primary Muon p_T", 90, 0., 900.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_ld_ak8_jet", "Pt leading Ak8 Jet", 60, 0., 1500.));

            vector<string> item_names;
            for (auto const & seli : SEL_ITEMS_FULL_SEL.back()) 
                item_names.push_back(seli->name());

            sel_helpers.emplace_back(new SelItemsHelper(SEL_ITEMS_FULL_SEL.back(), ctx, item_names, cat+"_sel_accept", cat+"_sel_all_accepted"));
            // sel_helper.declare_items_for_output();
            sel_modules.emplace_back(new SelectionProducer(ctx, *sel_helpers.back()));

            // 3. Set up Hists classes:

            // TODO: set up and fill other histogram classes, e.g. your own HistCollector stuff

            v_hists.emplace_back(vector<unique_ptr<Hists>>());
            v_hists_after_sel.emplace_back(vector<unique_ptr<Hists>>());

            // if (split(cat, "-")[0] == "NoSelection") {
            //     sel_helpers.back()->fill_hists_vector(v_hists_nosel, "NoSelection");
            //     // v_hists_nosel.emplace_back(new TwoDCutHist(ctx, "NoSelection", "TwoDcut_Dr_iso", "TwoDcut_Dpt_iso", "twod_cut_hist_iso"));
            //     // v_hists_nosel.emplace_back(new TwoDCutHist(ctx, "NoSelection", "TwoDcut_Dr_noIso", "TwoDcut_Dpt_noIso", "twod_cut_hist_noIso"));
            //     // for (auto const & hist_helper : ak8jet_hists)
            //     v_hists_nosel.emplace_back(ak8jet_hists->book_histograms(ctx, "NoSelection"));
            //     v_hists_nosel.emplace_back(new OwnHistCollector(ctx, "NoSelection", type == "MC", CSVBTag(CSVBTag::WP_MEDIUM), {"ev"}));
            //     continue;
            // }

            string directory = fs+"/"+cat;

            auto nm1_hists = new Nm1SelHists(ctx, directory+"/Nm1Selection", *sel_helpers.back());
            auto cf_hists = new VLQ2HTCutflow(ctx, directory+"/Cutflow", *sel_helpers.back());

            map<string, SelectedSelHists*> selected_sel_hists;
            // selected_sel_hists["NoTopTagCut"] = new SelectedSelHists(ctx, directory+"/NoTopTagCut", *sel_helpers.back(), {}, {"n_cmstoptagsv2"});
            // selected_sel_hists["OnlyTopTagCut"] = new SelectedSelHists(ctx, directory+"/OnlyTopTagCut", *sel_helpers.back(), {"n_cmstoptagsv2"});
            // selected_sel_hists["OnlyPreselectionCut"] = new SelectedSelHists(ctx, directory+"/OnlyPreselectionCut", *sel_helpers.back(), {}, {"n_higgs_tags_1b", "n_higgs_tags_2b"});


            
            for (auto hist : selected_sel_hists) {
                // hist.second->insert_hist_and_sel(pos_2d_cut, new TwoDCutHist(ctx, directory+"/"+hist.first, "TwoDcut_Dr_noIso", "TwoDcut_Dpt_noIso", "twod_cut_hist_noIso"), "twoD_cut");
                // for (auto const & hist_helper : ak8jet_hists) {
                // hist.second->insert_additional_hist(ak8jet_hists->book_histograms(ctx, directory+"/"+hist.first));
                // }
                hist.second->insert_additional_hist(new OwnHistCollector(ctx, directory+"/"+hist.first, type == "MC", CSVBTag(CSVBTag::WP_MEDIUM), {"ev"}));
                v_hists.back().emplace_back(hist.second);
            }

            v_hists.back().emplace_back(nm1_hists);
            v_hists.back().emplace_back(cf_hists);
            sel_helpers.back()->fill_hists_vector(v_hists_after_sel.back(), directory+"/PostSelection");
            // for (auto const & hist_helper : ak8jet_hists) {
            v_hists_after_sel.back().emplace_back(ak8jet_hists->book_histograms(ctx, directory+"/PostSelection"));
                // selected_sel_hists["NoHiggsTagCut"]->insert_additional_hist(hist_helper.book_histograms(ctx, directory+"/NoHiggsTagCut"));
            // }
            v_hists_after_sel.back().emplace_back(new OwnHistCollector(ctx, directory+"/PostSelection", type == "MC", CSVBTag(CSVBTag::WP_MEDIUM), {"ev"}));

            // v_hists_after_sel.emplace_back(new HistCollector(ctx, "EventHistsPost"));

        }
    }


}


bool TpTpFinalSelectionV2::process(Event & event) {

    common_module->process(event);

    TpTpAnalysisModule::process(event);

    // run all modules

    for (bool pass_sel : sel_modules_passed) {
        if (pass_sel) return true;
    }

    return false;
}

UHH2_REGISTER_ANALYSIS_MODULE(TpTpFinalSelectionV2)
