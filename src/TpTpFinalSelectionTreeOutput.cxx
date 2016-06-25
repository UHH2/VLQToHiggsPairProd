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

// typedef VectorAndSelection MyAndSelection;

class TpTpFinalSelectionTreeOutput: public TpTpAnalysisModule {
public:

    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_BASELINE_SEL {
        shared_ptr<SelectionItem>(new SelDatI("gendecay_accept", "GenDecay Accept", 2, -.5, 1.5, 1)),
        shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 10, -.5, 9.5, 2)),
        shared_ptr<SelectionItem>(new SelDatI("n_ak4", "N(Ak4 Jets)", 20, -.5, 19.5, 3)),
        shared_ptr<SelectionItem>(new SelDatD("ST", "ST", 65, 0, 6500, 800.)),
        // shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 10, -.5, 9.5, 2)),
        };
    
    const vector<shared_ptr<SelectionItem>> ADDITIONAL_SEL_ITEMS {
        shared_ptr<SelectionItem>(new SelDatI("is_muon", "Prim Lep is Muon", 2, -.5, 1.5)),
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_isoMu20", "Trigger Accept IsoMu20", 2, -.5, 1.5)),
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_isoEl27", "Trigger Accept IsoEl27", 2, -.5, 1.5)),
        // shared_ptr<SelectionItem>(new SelDatI("is_muon", "Prim Lep is Muon", 2, -.5, 1.5)),
        // shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt", "Primary Lepton p_T", 90, 0., 900.)),
        shared_ptr<SelectionItem>(new SelDatI("n_leptons", "N(Leptons)", 6, -.5, 5.5)),
        shared_ptr<SelectionItem>(new SelDatI("n_btags_medium", "N(medium AK4 b-tags)", 10, -.5, 9.5)),
        shared_ptr<SelectionItem>(new SelDatD("HT", "HT", 65, 0, 6500)),
        // shared_ptr<SelectionItem>(new SelDatD("parton_ht", "Parton HT", 45, 0, 4500)),
        // shared_ptr<SelectionItem>(new SelDatF("met", "MET", 50, 0, 1000)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_third_ak4_jet", "Pt third Ak4 Jet", 50, 0., 1000.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_fourth_ak4_jet", "Pt fourth Ak4 Jet", 30, 0., 600.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_fifth_ak4_jet", "Pt fifth Ak4 Jet", 25, 0., 500.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_sixth_ak4_jet", "Pt sixth Ak4 Jet", 20, 0., 400.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak8_jet", "Pt leading Ak8 Jet", 100, 0., 2000.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_subld_ak8_jet", "Pt subld Ak8 Jet", 40, 0., 1600.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_third_ak8_jet", "Pt third Ak8 Jet", 50, 0., 1000.)),
        // shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt", "Primary Lepton p_T", 90, 0., 900.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 100, 0., 2000.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_subld_ak4_jet", "Pt leading Ak4 Jet", 40, 0., 1600.)),
        shared_ptr<SelectionItem>(new SelDatI("n_ak8_higgs_cand", "N(Higgs Candidates)", 10, -.5, 9.5)),
        // shared_ptr<SelectionItem>(new SelDatI("n_jets_no_overlap", "N(non-overlapping Ak4 jets)", 12, -.5, 11.5)),
        // shared_ptr<SelectionItem>(new SelDatF("dR_ak4_btagged_higgs_tags_1b_med", "dR(b-tag ak4, htag)", 50, 0., 5.)),
        shared_ptr<SelectionItem>(new SelDatI("n_toptags", "N(t-tags)", 6, -.5, 5.5)),
        // shared_ptr<SelectionItem>(new SelDatI("n_wtags", "N(W-tags)", 6, -.5, 5.5)),
        // shared_ptr<SelectionItem>(new SelDatI("n_wtags_sm10", "N(W-tags, sm10)", 6, -.5, 5.5)),
        // shared_ptr<SelectionItem>(new SelDatI("n_wtags_sm20", "N(W-tags, sm20)", 6, -.5, 5.5)),
        // shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_1b_med", "N(H-tags, 1b)", 6, -.5, 5.5)),
        // shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_2b_med", "N(H-tags, 2b)", 6, -.5, 5.5)),
        shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_1b_med_sm10", "N(H-tags, 1b, sm10)", 6, -.5, 5.5)),
        shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_2b_med_sm10", "N(H-tags, 2b, sm10)", 6, -.5, 5.5)),
        shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_1b_med_sm20", "N(H-tags, 1b, sm20)", 6, -.5, 5.5)),
        shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_2b_med_sm20", "N(H-tags, 2b, sm20)", 6, -.5, 5.5)),
        // shared_ptr<SelectionItem>(new SelDatI("n_ak8_cleaned", "N(Ak8 Jets, cleaned)", 10, -.5, 9.5)),
        // shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt_tight", "Primary Lepton p_T", 100, 0., 1200.)),
        // shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt_mva_loose", "Primary Lepton p_T", 100, 0., 1200.)),
        // shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt_mva_tight", "Primary Lepton p_T", 100, 0., 1200.)),
        // shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt_el105", "Primary Lepton p_T", 100, 0., 1200.)),
        // shared_ptr<SelectionItem>(new SelDatF("wtags_mass", "mass sj", 100, 0., 300.)),
        // shared_ptr<SelectionItem>(new SelDatF("wtags_sm10_mass", "mass sj", 100, 0., 300.)),
        // shared_ptr<SelectionItem>(new SelDatF("wtags_sm20_mass", "mass sj", 100, 0., 300.)),
        shared_ptr<SelectionItem>(new SelDatF("ak8_boost_gen_mass", "gen mass", 100, 0., 300.)),
        shared_ptr<SelectionItem>(new SelDatF("ak8_boost_diff_before", "diff before", 50, -1., 1.)),
        shared_ptr<SelectionItem>(new SelDatF("ak8_boost_diff_10", "diff 10", 50, -1., 1.)),
        shared_ptr<SelectionItem>(new SelDatF("ak8_boost_diff_20", "diff 20", 50, -1., 1.)),
        shared_ptr<SelectionItem>(new SelDatF("ak8_boost_diff_before_sj", "diff before sj", 50, -1., 1.)),
        // shared_ptr<SelectionItem>(new SelDatF("ak8_boost_diff_10_sj", "diff 10 sj", 50, -1., 1.)),
        // shared_ptr<SelectionItem>(new SelDatF("ak8_boost_diff_20_sj", "diff 20 sj", 50, -1., 1.)),
        shared_ptr<SelectionItem>(new SelDatF("nomass_boost_1b_gen_mass", "gen mass", 100, 0., 300.)),
        shared_ptr<SelectionItem>(new SelDatF("nomass_boost_1b_diff_before", "diff before", 50, -1., 1.)),
        shared_ptr<SelectionItem>(new SelDatF("nomass_boost_1b_diff_10", "diff 10", 50, -1., 1.)),
        shared_ptr<SelectionItem>(new SelDatF("nomass_boost_1b_diff_20", "diff 20", 50, -1., 1.)),
        shared_ptr<SelectionItem>(new SelDatF("nomass_boost_1b_diff_before_sj", "diff before sj", 50, -1., 1.)),
        // shared_ptr<SelectionItem>(new SelDatF("nomass_boost_1b_diff_10_sj", "diff 10 sj", 50, -1., 1.)),
        // shared_ptr<SelectionItem>(new SelDatF("nomass_boost_1b_diff_20_sj", "diff 20 sj", 50, -1., 1.)),
        shared_ptr<SelectionItem>(new SelDatF("nomass_boost_2b_gen_mass", "gen mass", 100, 0., 300.)),
        shared_ptr<SelectionItem>(new SelDatF("nomass_boost_2b_diff_before", "diff before", 50, -1., 1.)),
        shared_ptr<SelectionItem>(new SelDatF("nomass_boost_2b_diff_10", "diff 10", 50, -1., 1.)),
        shared_ptr<SelectionItem>(new SelDatF("nomass_boost_2b_diff_20", "diff 20", 50, -1., 1.)),
        shared_ptr<SelectionItem>(new SelDatF("nomass_boost_2b_diff_before_sj", "diff before sj", 50, -1., 1.)),
        // shared_ptr<SelectionItem>(new SelDatF("nomass_boost_2b_diff_10_sj", "diff 10 sj", 50, -1., 1.)),
        // shared_ptr<SelectionItem>(new SelDatF("nomass_boost_2b_diff_20_sj", "diff 20 sj", 50, -1., 1.)),
        shared_ptr<SelectionItem>(new SelDatF("nobtag_boost_mass_nsjbtags", "N sjbtags medium", 6, -0.5, 5.5)),
        // shared_ptr<SelectionItem>(new SelDatF("dR_ak8_higgs_cand_1_ak4_jets_btagged_cl", "dR_ak8_higgs_cand_1_ak4_jets_btagged_cl", 50, 0., 5.)),
        // shared_ptr<SelectionItem>(new SelDatF("dR_jets_1_PrimaryLepton_cl", "dR_jets_1_PrimaryLepton_cl", 50, 0., 5.)),
        // shared_ptr<SelectionItem>(new SelDatF("dR_jets_2_PrimaryLepton_cl", "dR_jets_2_PrimaryLepton_cl", 50, 0., 5.)),
        // shared_ptr<SelectionItem>(new SelDatF("dR_higgs_tags_1b_med_1_PrimaryLepton_cl", "dR_higgs_tags_1b_med_1_PrimaryLepton_cl", 50, 0., 5.)),
        // shared_ptr<SelectionItem>(new SelDatF("dR_higgs_tags_1b_med_1_jets_cl", "dR_higgs_tags_1b_med_1_jets_cl", 50, 0., 5.)),
        // shared_ptr<SelectionItem>(new SelDatF("dR_higgs_tags_1b_med_1_jets_1", "dR_higgs_tags_1b_med_1_jets_1", 50, 0., 5.)),
        // shared_ptr<SelectionItem>(new SelDatF("dR_higgs_tags_1b_med_1_jets_2", "dR_higgs_tags_1b_med_1_jets_2", 50, 0., 5.)),
        // shared_ptr<SelectionItem>(new SelDatF("dR_topjets_1_jets_cl", "dR_topjets_1_jets_cl", 50, 0., 5.)),
        // shared_ptr<SelectionItem>(new SelDatF("dR_topjets_1_jets_1", "dR_topjets_1_jets_1", 50, 0., 5.)),
        // shared_ptr<SelectionItem>(new SelDatF("dR_topjets_1_jets_2", "dR_topjets_1_jets_2", 50, 0., 5.)),
        // shared_ptr<SelectionItem>(new SelDatF("higgs_tags_1b_med_mass_softdrop", "higgs_tags_1b_med_mass", 100, 0., 300.)),
        // shared_ptr<SelectionItem>(new SelDatF("higgs_tags_1b_med_mass_sj", "higgs_tags_1b_med_mass", 100, 0., 300.)),
        // shared_ptr<SelectionItem>(new SelDatF("higgs_tags_1b_med_sm20_mass_softdrop", "higgs_tags_1b_med_sm20_mass", 100, 0., 300.)),
        // shared_ptr<SelectionItem>(new SelDatF("higgs_tags_2b_med_mass_softdrop", "higgs_tags_2b_med_mass", 100, 0., 300.)),
        // shared_ptr<SelectionItem>(new SelDatF("higgs_tags_2b_med_sm20_mass_softdrop", "higgs_tags_2b_med_sm20_mass", 100, 0., 300.)),
        shared_ptr<SelectionItem>(new SelDatF("wtags_mass_softdrop", "wtags_mass", 100, 0., 300.)),
        shared_ptr<SelectionItem>(new SelDatF("wtags_mass_sj", "wtags_mass_sj", 100, 0., 300.)),
        shared_ptr<SelectionItem>(new SelDatF("wtags_sm10_mass_softdrop", "wtags_sm10_mass", 100, 0., 300.)),
        shared_ptr<SelectionItem>(new SelDatF("wtags_sm20_mass_softdrop", "wtags_sm20_mass", 100, 0., 300.)),
        shared_ptr<SelectionItem>(new SelDatF("nomass_boost_1b_mass_softdrop", "nomass_boost_1b_med_mass", 100, 0., 300.)),
        shared_ptr<SelectionItem>(new SelDatF("nomass_boost_1b_mass_sj", "nomass_boost_1b_med_mass_sj", 100, 0., 300.)),
        shared_ptr<SelectionItem>(new SelDatF("nomass_boost_1b_sm10_mass_softdrop", "nomass_boost_1b_med_sm10_mass", 100, 0., 300.)),
        shared_ptr<SelectionItem>(new SelDatF("nomass_boost_1b_sm20_mass_softdrop", "nomass_boost_1b_med_sm20_mass", 100, 0., 300.)),
        shared_ptr<SelectionItem>(new SelDatF("nomass_boost_2b_mass_softdrop", "nomass_boost_2b_med_mass", 100, 0., 300.)),
        shared_ptr<SelectionItem>(new SelDatF("nomass_boost_2b_mass_sj", "nomass_boost_2b_med_mass_sj", 100, 0., 300.)),
        shared_ptr<SelectionItem>(new SelDatF("nomass_boost_2b_sm10_mass_softdrop", "nomass_boost_2b_med_sm10_mass", 100, 0., 300.)),
        shared_ptr<SelectionItem>(new SelDatF("nomass_boost_2b_sm20_mass_softdrop", "nomass_boost_2b_med_sm20_mass", 100, 0., 300.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_reco_gen_ld_ak4_jet", "Pt first Ak4 Jet (reco-gen)", 40, 0., 1600.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_reco_gen_subld_ak4_jet", "Pt second Ak4 Jet (reco-gen)", 40, 0., 1600.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_reco_gen_third_ak4_jet", "Pt third Ak4 Jet (reco-gen)", 40, 0., 1600.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_reco_gen_fourth_ak4_jet", "Pt fourth Ak4 Jet (reco-gen)", 40, 0., 1600.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_reco_gen_fifth_ak4_jet", "Pt fifth Ak4 Jet (reco-gen)", 40, 0., 1600.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_reco_gen_sixth_ak4_jet", "Pt sixth Ak4 Jet (reco-gen)", 40, 0., 1600.)),
        // shared_ptr<SelectionItem>(new SelDatD("parton_ht_gen_reco", "HT (reco-gen)", 45, 0, 4500)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak4_genjet", "Pt first Ak4 GenJet", 100, 0., 2000.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_subld_ak4_genjet", "Pt second Ak4 GenJet", 40, 0., 1600.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_third_ak4_genjet", "Pt third Ak4 GenJet", 50, 0., 1000.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_fourth_ak4_genjet", "Pt fourth Ak4 GenJet", 30, 0., 600.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_fifth_ak4_genjet", "Pt fifth Ak4 GenJet", 25, 0., 500.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_sixth_ak4_genjet", "Pt sixth Ak4 GenJet", 20, 0., 400.)),
        shared_ptr<SelectionItem>(new SelDatI("n_prim_vertices", "N(Primary Vertices)", 35, -.5, 34.5)),
    
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
        // shared_ptr<SelectionItem>(new SelDatF("primary_electron_pt_tight", "Primary Lepton p_T", 100, 0., 1200.)),
        // shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 10, -.5, 9.5, 2)),
        };

    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_COMB_SEL {
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_lep_comb", "Trigger Accept", 2, -.5, 1.5, 1)),
        shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt", "Primary Lepton p_T", 100, 0., 1200., 47.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 100, 0., 2000.)),
        // shared_ptr<SelectionItem>(new SelDatF("pt_subld_ak4_jet", "Pt leading Ak4 Jet", 40, 0., 1600.)),
        shared_ptr<SelectionItem>(new SelDatF("primary_muon_pt", "Primary Lepton p_T", 100, 0., 1200.)),
        shared_ptr<SelectionItem>(new SelDatF("primary_electron_pt", "Primary Lepton p_T", 100, 0., 1200.)),
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_el45", "Trigger Accept", 2, -.5, 1.5)),
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_mu45", "Trigger Accept", 2, -.5, 1.5)),
        // shared_ptr<SelectionItem>(new SelDatF("primary_electron_pt_tight", "Primary Lepton p_T", 100, 0., 1200.)),
        // shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 10, -.5, 9.5, 2)),
        };

    const vector<shared_ptr<SelectionItem>> SEL_ITEMS_EL45TIGHT_SEL {
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_el45", "Trigger Accept", 2, -.5, 1.5, 1)),
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_mu45", "Trigger Accept Mu45", 2, -.5, 1.5, 0, 0)),
        // shared_ptr<SelectionItem>(new SelDatF("primary_electron_pt_tight", "Primary Lepton p_T", 100, 0., 1200., 50.)),
        shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 100, 0., 2000., 250.)),
        shared_ptr<SelectionItem>(new SelDatF("pt_subld_ak4_jet", "Pt subleading Ak4 Jet", 40, 0., 1600., 70.)),
        shared_ptr<SelectionItem>(new SelDatF("primary_muon_pt", "Primary Lepton p_T", 100, 0., 1200.)),
        shared_ptr<SelectionItem>(new SelDatI("trigger_accept_lep_comb", "Trigger Accept", 2, -.5, 1.5)),
        shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt", "Primary Lepton p_T", 100, 0., 1200.)),
        // shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 10, -.5, 9.5, 2)),
        };

    // const vector<shared_ptr<SelectionItem>> SEL_ITEMS_EL45MVALOOSE_SEL {
    //     shared_ptr<SelectionItem>(new SelDatI("trigger_accept_el45", "Trigger Accept", 2, -.5, 1.5, 1)),
    //     shared_ptr<SelectionItem>(new SelDatI("trigger_accept_mu45", "Trigger Accept Mu45", 2, -.5, 1.5, 0, 0)),
    //     shared_ptr<SelectionItem>(new SelDatF("primary_electron_pt_mva_loose", "Primary Lepton p_T", 100, 0., 1200., 50.)),
    //     shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 100, 0., 2000., 250.)),
    //     shared_ptr<SelectionItem>(new SelDatF("pt_subld_ak4_jet", "Pt leading Ak4 Jet", 40, 0., 1600., 65.)),
    //     shared_ptr<SelectionItem>(new SelDatF("primary_muon_pt", "Primary Lepton p_T", 100, 0., 1200.)),
    //     shared_ptr<SelectionItem>(new SelDatI("trigger_accept_lep_comb", "Trigger Accept", 2, -.5, 1.5)),
    //     shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt", "Primary Lepton p_T", 100, 0., 1200.)),
    //     // shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 10, -.5, 9.5, 2)),
    //     };

    // const vector<shared_ptr<SelectionItem>> SEL_ITEMS_EL45MVATIGHT_SEL {
    //     shared_ptr<SelectionItem>(new SelDatI("trigger_accept_el45", "Trigger Accept", 2, -.5, 1.5, 1)),
    //     shared_ptr<SelectionItem>(new SelDatI("trigger_accept_mu45", "Trigger Accept Mu45", 2, -.5, 1.5, 0, 0)),
    //     shared_ptr<SelectionItem>(new SelDatF("primary_electron_pt_mva_tight", "Primary Lepton p_T", 100, 0., 1200., 50.)),
    //     shared_ptr<SelectionItem>(new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 100, 0., 2000., 250.)),
    //     shared_ptr<SelectionItem>(new SelDatF("pt_subld_ak4_jet", "Pt leading Ak4 Jet", 40, 0., 1600., 65.)),
    //     shared_ptr<SelectionItem>(new SelDatF("primary_muon_pt", "Primary Lepton p_T", 100, 0., 1200.)),
    //     shared_ptr<SelectionItem>(new SelDatI("trigger_accept_lep_comb", "Trigger Accept", 2, -.5, 1.5)),
    //     shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt", "Primary Lepton p_T", 100, 0., 1200.)),
    //     // shared_ptr<SelectionItem>(new SelDatI("n_ak8", "N(Ak8 Jets)", 10, -.5, 9.5, 2)),
    //     };


    explicit TpTpFinalSelectionTreeOutput(Context & ctx);
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

};



TpTpFinalSelectionTreeOutput::TpTpFinalSelectionTreeOutput(Context & ctx) : TpTpAnalysisModule(ctx) {

    auto data_dir_path = ctx.get("data_dir_path");
    ctx.undeclare_all_event_output();
    // jetpt_weight_hndl = ctx.declare_event_output<float>("weight_ak4_jetpt");
    // ctx.declare_event_output<float>("weight_ak4_jetpt_up");
    // ctx.declare_event_output<float>("weight_ak4_jetpt_down");
    // ctx.declare_event_output<float>("weight_ak8_jetpt");

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

    if (version.find("TT") != string::npos) {
        other_modules.emplace_back(new TTbarGenProducer(ctx, "ttbargen", false));
        other_modules.emplace_back(new TopPtWeight(ctx, "ttbargen", 0.159, -0.00141));
    }
    if (version.find("WJets") != string::npos) {
        other_modules.emplace_back(new HTReweighting(ctx, 1.146709, -0.00026451, 3000., "weight_htrew_wjets"));
        other_modules.emplace_back(new HTReweighting(ctx, 1.201648, -0.000250984, 3000., "weight_htrew_wjets_toppt"));
    }
    if (version.find("TT") != string::npos || version.find("TpTp") != string::npos || version.find("BpBp") != string::npos) {
        other_modules.emplace_back(new HTReweighting(ctx, 1.268084, -0.000390272, 3000., "weight_htrew_tt"));
        other_modules.emplace_back(new HTReweighting(ctx, 1.424121, -0.000352462, 3000., "weight_htrew_tt_toppt"));
    }


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

    // pre_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
    //             "topjets",
    //             "topjets_cleaned"
    //             ));
    // pre_modules.emplace_back(new TopJetCleaner(ctx, MinMaxDeltaRId<Electron>(ctx, "electrons", 0.2), "topjets_cleaned"));
    // pre_modules.emplace_back(new TopJetCleaner(ctx, MinMaxDeltaRId<Muon>(ctx, "muons", 0.2), "topjets_cleaned"));
    // pre_modules.emplace_back(new TopJetCleaner(ctx, PtEtaCut(200., 2.4), "topjets_cleaned"));
    // pre_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
    //     "topjets_cleaned",
    //     "n_ak8_cleaned"
    //     ));


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
    //             "electrons_mva_loose"
    //             ));
    // pre_modules.emplace_back(new CollectionProducer<Electron>(ctx,
    //             "electrons",
    //             "electrons_mva_tight"
    //             ));
    
    // other_modules.emplace_back(new ParticleCleaner<Muon>(ctx, MuonIDTight(), "muons_tight"));
    // pre_modules.emplace_back(new ParticleCleaner<Electron>(ctx, ElectronID_Spring15_25ns_tight_noIso, "electrons_tight"));
    // other_modules.emplace_back(new ParticleCleaner<Electron>(ctx, ElectronID_MVAnotrig_Spring15_25ns_tight, "electrons_mva_tight"));

    // common_modules.emplace_back(new PrimaryLeptonOwn<Electron>(ctx, "electrons_tight", "PrimaryElectronTight"));
    // common_modules.emplace_back(new PrimaryLeptonOwn<Electron>(ctx, "electrons_mva_tight", "PrimaryElectronMVATight"));
    // other_modules.emplace_back(new TriggerAwarePrimaryLepton(ctx, "PrimaryLeptonTight", "trigger_accept_el45", "trigger_accept_mu45", "prim_ele_coll_tight", "prim_mu_coll_tight", 50., 47., "electrons_tight", "muons"));
    // other_modules.emplace_back(new TriggerAwarePrimaryLepton(ctx, "PrimaryLeptonMVATight", "trigger_accept_el45", "trigger_accept_mu45", "prim_ele_coll_mva_tight", "prim_ele_coll_mva_tight", 50., 47., "electrons_mva_tight", "muons"));
    // other_modules.emplace_back(new TwoDCutProducer(ctx, "PrimaryLeptonTight", "TwoDcut_Dr_noIso_el105", "TwoDcut_Dpt_noIso_el105", true));

    // other_modules.emplace_back(new PrimaryLeptonPtProducer(ctx, "PrimaryElectronTight", "primary_electron_pt_tight"));
    // other_modules.emplace_back(new PrimaryLeptonPtProducer(ctx, "PrimaryElectronMVATight", "primary_electron_pt_mva_tight"));
    // other_modules.emplace_back(new PrimaryLeptonPtProducer(ctx, "PrimaryLeptonTight", "primary_lepton_pt_tight"));
    // other_modules.emplace_back(new PrimaryLeptonPtProducer(ctx, "PrimaryLeptonMVATight", "primary_lepton_pt_mva_tight"));


    if (type == "MC") {
        pre_modules.emplace_back(new JetResolutionSmearer(ctx));
        ctx.declare_event_output<double>("gen_ht");
        ctx.declare_event_output<double>("parton_ht");
    }
    pre_modules.emplace_back(new JetCleaner(ctx, AndId<Jet>(JetPFID(JetPFID::WP_LOOSE), PtEtaCut(30.0,2.4))));
    other_modules.emplace_back(new MCMuonScaleFactor(ctx, 
        data_dir_path + "MuonID_Z_RunCD_Reco76X_Feb15.root", 
        "MC_NUM_MediumID_DEN_genTracks_PAR_pt_spliteta_bin1", 1., "id", "nominal", "prim_mu_coll"));
    other_modules.emplace_back(new MCMuonScaleFactor(ctx, 
        data_dir_path + "SingleMuonTrigger_Z_RunCD_Reco76X_Feb15.root", 
        "runD_Mu45_eta2p1_PtEtaBins", 0.5, "trg", "nominal", "prim_mu_coll"));
    // other_modules.emplace_back(new MCElectronScaleFactor(ctx, 
    //     ctx.get("ele_sf_trg_file"), 
    //     "CutBasedMedium", 0., "id", "nominal", "prim_ele_coll"));
    other_modules.emplace_back(new MCElectronScaleFactor(ctx, 
        ctx.get("ele_sf_trg_file"), 
        "EGamma_SF2D", 0., "id", "nominal", "prim_ele_coll", true));
    ele_trg_sf.reset(new MCConstantScalefactor(ctx, 
                0.99, 0.02, "sfel_trg", true));
    ele_trg_nosf.reset(new MCConstantScalefactor(ctx, 
                1., 0., "sfel_trg", true));
    if (version.find("TpTp") != string::npos || version.find("BpBp") != string::npos) {
        other_modules.emplace_back(new PDFWeightBranchCreator(ctx, 110, false));
        other_modules.emplace_back(new ScaleVariationWeightBranchCreator(ctx));
    }
    else if (version.find("DYJets") != string::npos ||
        version.find("SingleTop_t-channel") != string::npos ||
        version.find("SingleTop_s-channel") != string::npos ||
        version.find("WJets") != string::npos ||
        version.find("TTbar") != string::npos
        ) {
            other_modules.emplace_back(new PDFWeightBranchCreator(ctx, 9, false));
            other_modules.emplace_back(new ScaleVariationWeightBranchCreator(ctx));
        }
    else {
        other_modules.emplace_back(new PDFWeightBranchCreator(ctx, -1, false));
        other_modules.emplace_back(new ScaleVariationWeightBranchCreator(ctx, true));   
    }

    weight_ele_hndl = ctx.get_handle<float>("weight_el_trg");

    // =====PRODUCERS========

    // other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
    //             "topjets",
    //             "ak8_nonoverlap",
    //             TopJetId(MinMaxDeltaRId<TopJet>(ctx, "higgs_tags_1b_med", 1.))
    //             ));

    other_modules.emplace_back(new PrimVertProducer(ctx));

    other_modules.emplace_back(new CollectionProducer<Jet>(ctx,
                "jets",
                "ak4_jets_btagged",
                JetId(CSVBTag(CSVBTag::WP_MEDIUM))
                ));

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
    other_modules.emplace_back(new HiggsMassSmear(ctx,
                "nomass_boost_1b",
                false, false
                ));
    other_modules.emplace_back(new HiggsMassSmear(ctx,
                "nomass_boost_2b",
                false, false
                ));

    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "topjets",
                "toptags",
                TopJetId(AndId<TopJet>(PtEtaCut(400., 2.4), Type2TopTag(140, 250, Type2TopTag::MassType::groomed), Tau32(0.74)))
                // true
                ));

    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost",
                "wtags",
                TopJetId(Tau21(0.4))
                // true
                ));
    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost_sm10",
                "wtags_sm10",
                TopJetId(Tau21(0.4))
                // true
                ));
    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost_sm20",
                "wtags_sm20",
                TopJetId(Tau21(0.4))
                // true
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
    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost_sm20",
                "higgs_tags_1b_med_sm20",
                TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM)))
                ));
    other_modules.emplace_back(new CollectionProducer<TopJet>(ctx,
                "ak8_boost_sm20",
                "higgs_tags_2b_med_sm20",
                TopJetId(HiggsFlexBTag(HIGGS_MIN_MASS, HIGGS_MAX_MASS, CSVBTag(CSVBTag::WP_MEDIUM), CSVBTag(CSVBTag::WP_MEDIUM)))
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
    other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "toptags",
                "n_toptags"
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
                "higgs_tags_1b_med",
                "n_higgs_tags_1b_med"
                ));
    other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "higgs_tags_2b_med",
                "n_higgs_tags_2b_med"
                ));
    other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "higgs_tags_1b_med_sm10",
                "n_higgs_tags_1b_med_sm10"
                ));
    other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "higgs_tags_2b_med_sm10",
                "n_higgs_tags_2b_med_sm10"
                ));
    other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "higgs_tags_1b_med_sm20",
                "n_higgs_tags_1b_med_sm20"
                ));
    other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                "higgs_tags_2b_med_sm20",
                "n_higgs_tags_2b_med_sm20"
                ));



    // other_modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
    //             "jets_no_overlap",
    //             "n_jets_no_overlap"
    //             ));



    // other_modules.emplace_back(new JetVarProducer<TopJet>(ctx,
    //             "topjets",
    //             "first_ak8jet",
    //             "PrimaryLepton",
    //             CSVBTag(CSVBTag::WP_MEDIUM),
    //             1
    //             ));
    // other_modules.emplace_back(new JetVarProducer<TopJet>(ctx,
    //             "topjets",
    //             "second_ak8jet",
    //             "PrimaryLepton",
    //             CSVBTag(CSVBTag::WP_MEDIUM),
    //             2
    //             ));

    // other_modules.emplace_back(new HiggsMassSmear(ctx,
    //             "higgs_tags_1b_med",
    //             false
    //             ));
    // other_modules.emplace_back(new HiggsMassSmear(ctx,
    //             "higgs_tags_2b_med",
    //             false
    //             ));
    // other_modules.emplace_back(new HiggsMassSmear(ctx,
    //             "topjets"
    //             ));
    // other_modules.emplace_back(new HiggsMassSmear(ctx,
    //             "ak8_boost"
    //             ));
    // other_modules.emplace_back(new HiggsMassSmear(ctx,
    //             "wtags",
    //             false,
    //             false
    //             ));

    // other_modules.emplace_back(new LeadingTopjetMassProducer(ctx,
    //             "higgs_tags_1b_med",
    //             "higgs_tags_1b_med_mass"
    //             ));
    // other_modules.emplace_back(new LeadingTopjetMassProducer(ctx,
    //             "higgs_tags_1b_med_sm10",
    //             "higgs_tags_1b_med_sm10_mass"
    //             ));
    // other_modules.emplace_back(new LeadingTopjetMassProducer(ctx,
    //             "higgs_tags_1b_med_sm20",
    //             "higgs_tags_1b_med_sm20_mass"
    //             ));
    // other_modules.emplace_back(new LeadingTopjetMassProducer(ctx,
    //             "higgs_tags_2b_med",
    //             "higgs_tags_2b_med_mass"
    //             ));
    // other_modules.emplace_back(new LeadingTopjetMassProducer(ctx,
    //             "higgs_tags_2b_med_sm10",
    //             "higgs_tags_2b_med_sm10_mass"
    //             ));
    // other_modules.emplace_back(new LeadingTopjetMassProducer(ctx,
    //             "higgs_tags_2b_med_sm20",
    //             "higgs_tags_2b_med_sm20_mass"
    //             ));
    other_modules.emplace_back(new LeadingTopjetMassProducer(ctx,
                "nomass_boost_1b",
                "nomass_boost_1b_mass"
                ));
    other_modules.emplace_back(new LeadingTopjetMassProducer(ctx,
                "nomass_boost_1b_sm10",
                "nomass_boost_1b_sm10_mass"
                ));
    other_modules.emplace_back(new LeadingTopjetMassProducer(ctx,
                "nomass_boost_1b_sm20",
                "nomass_boost_1b_sm20_mass"
                ));
    other_modules.emplace_back(new LeadingTopjetMassProducer(ctx,
                "nomass_boost_2b",
                "nomass_boost_2b_mass"
                ));
    other_modules.emplace_back(new LeadingTopjetMassProducer(ctx,
                "nomass_boost_2b_sm10",
                "nomass_boost_2b_sm10_mass"
                ));
    other_modules.emplace_back(new LeadingTopjetMassProducer(ctx,
                "nomass_boost_2b_sm20",
                "nomass_boost_2b_sm20_mass"
                ));
    other_modules.emplace_back(new LeadingTopjetMassProducer(ctx,
                "wtags",
                "wtags_mass"
                ));
    other_modules.emplace_back(new LeadingTopjetMassProducer(ctx,
                "wtags_sm10",
                "wtags_sm10_mass"
                ));
    other_modules.emplace_back(new LeadingTopjetMassProducer(ctx,
                "wtags_sm20",
                "wtags_sm20_mass"
                ));


    other_modules.emplace_back(new NSubjetBtagProducer(ctx,
                "nobtag_boost_mass",
                "nobtag_boost_mass",
                CSVBTag(CSVBTag::WP_MEDIUM),
                1
                ));

    // other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
    //             "higgs_tags_1b_med_sm10",
    //             "n_higgs_tags_1b_med_sm10"
    //             ));

    // other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
    //             "higgs_tags_1b_med_sm20",
    //             "n_higgs_tags_1b_med_sm20"
    //             ));

    // other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
    //             "higgs_tags_2b_med_sm10",
    //             "n_higgs_tags_2b_med_sm10"
    //             ));

    // other_modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
    //             "higgs_tags_2b_med_sm20",
    //             "n_higgs_tags_2b_med_sm20"
    //             ));

    vector<string> deltaR_plots;

    other_modules.emplace_back(new DeltaRProducer<TopJet, Jet>(ctx,
                "ak8_higgs_cand",
                "ak4_jets_btagged",
                1, -1, 0.
                ));
    deltaR_plots.push_back("dR_ak8_higgs_cand_1_ak4_jets_btagged_cl");

    other_modules.emplace_back(new DeltaRProducer<Jet, FlavorParticle>(ctx,
                "jets",
                "PrimaryLepton",
                1, -1, 0.4
                ));
    deltaR_plots.push_back("dR_jets_1_PrimaryLepton_cl");

    other_modules.emplace_back(new DeltaRProducer<Jet, FlavorParticle>(ctx,
                "jets",
                "PrimaryLepton",
                2, -1, 0.4
                ));
    deltaR_plots.push_back("dR_jets_2_PrimaryLepton_cl");

    other_modules.emplace_back(new DeltaRProducer<TopJet, FlavorParticle>(ctx,
                "higgs_tags_1b_med",
                "PrimaryLepton",
                1
                ));
    deltaR_plots.push_back("dR_higgs_tags_1b_med_1_PrimaryLepton_cl");

    other_modules.emplace_back(new DeltaRProducer<TopJet, Jet>(ctx,
                "higgs_tags_1b_med",
                "jets",
                1
                ));
    deltaR_plots.push_back("dR_higgs_tags_1b_med_1_jets_cl");

    // other_modules.emplace_back(new DeltaRProducer<TopJet, Jet>(ctx,
    //             "higgs_tags_1b_med",
    //             "jets",
    //             1, 1
    //             ));
    // deltaR_plots.push_back("dR_higgs_tags_1b_med_1_jets_1");

    // other_modules.emplace_back(new DeltaRProducer<TopJet, Jet>(ctx,
    //             "higgs_tags_1b_med",
    //             "jets",
    //             1, 2
    //             ));
    // deltaR_plots.push_back("dR_higgs_tags_1b_med_1_jets_2");

    other_modules.emplace_back(new DeltaRProducer<TopJet, TopJet>(ctx,
                "higgs_tags_1b_med",
                "topjets",
                1
                ));
    deltaR_plots.push_back("dR_higgs_tags_1b_med_1_topjets_cl");

    other_modules.emplace_back(new DeltaRProducer<TopJet, TopJet>(ctx,
                "topjets",
                "topjets",
                1
                ));
    deltaR_plots.push_back("dR_topjets_1_topjets_cl");

    // other_modules.emplace_back(new DeltaRProducer<TopJet, TopJet>(ctx,
    //             "higgs_tags_1b_med",
    //             "topjets",
    //             1, 1
    //             ));
    // deltaR_plots.push_back("dR_higgs_tags_1b_med_1_topjets_1");

    // other_modules.emplace_back(new DeltaRProducer<TopJet, TopJet>(ctx,
    //             "higgs_tags_1b_med",
    //             "topjets",
    //             1, 2
    //             ));
    // deltaR_plots.push_back("dR_higgs_tags_1b_med_1_topjets_2");

    // other_modules.emplace_back(new DeltaRProducer<TopJet, Jet>(ctx,
    //             "topjets",
    //             "jets",
    //             1
    //             ));
    // deltaR_plots.push_back("dR_topjets_1_jets_cl");

    // other_modules.emplace_back(new DeltaRProducer<TopJet, Jet>(ctx,
    //             "topjets",
    //             "jets",
    //             1, 1
    //             ));
    // deltaR_plots.push_back("dR_topjets_1_jets_1");

    // other_modules.emplace_back(new DeltaRProducer<TopJet, Jet>(ctx,
    //             "topjets",
    //             "jets",
    //             1, 2
    //             ));
    // deltaR_plots.push_back("dR_topjets_1_jets_2");




    //////////// SOON DEPRECATED??

    // other_modules.emplace_back(new JetVarProducer<TopJet>(ctx,
    //             "noboost_mass_1b",
    //             "noboost_mass_1b",
    //             "PrimaryLepton",
    //             CSVBTag(CSVBTag::WP_MEDIUM),
    //             1
    //             ));
    // other_modules.emplace_back(new JetVarProducer<TopJet>(ctx,
    //             "noboost_mass_2b",
    //             "noboost_mass_2b",
    //             "PrimaryLepton",
    //             CSVBTag(CSVBTag::WP_MEDIUM),
    //             1
    //             ));
    // other_modules.emplace_back(new JetVarProducer<TopJet>(ctx,
    //             "topjets",
    //             "topjets",
    //             "PrimaryLepton",
    //             CSVBTag(CSVBTag::WP_MEDIUM),
    //             1
    //             ));
    // other_modules.emplace_back(new JetVarProducer<TopJet>(ctx,
    //             "topjets_sm10",
    //             "topjets_sm10",
    //             "PrimaryLepton",
    //             CSVBTag(CSVBTag::WP_MEDIUM),
    //             1
    //             ));
    // other_modules.emplace_back(new JetVarProducer<TopJet>(ctx,
    //             "topjets_sm20",
    //             "topjets_sm20",
    //             "PrimaryLepton",
    //             CSVBTag(CSVBTag::WP_MEDIUM),
    //             1
    //             ));
    // other_modules.emplace_back(new JetVarProducer<TopJet>(ctx,
    //             "wtags",
    //             "wtags",
    //             "PrimaryLepton",
    //             CSVBTag(CSVBTag::WP_MEDIUM),
    //             1
    //             ));
    // other_modules.emplace_back(new JetVarProducer<TopJet>(ctx,
    //             "wtags_sm10",
    //             "wtags_sm10",
    //             "PrimaryLepton",
    //             CSVBTag(CSVBTag::WP_MEDIUM),
    //             1
    //             ));
    // other_modules.emplace_back(new JetVarProducer<TopJet>(ctx,
    //             "wtags_sm20",
    //             "wtags_sm20",
    //             "PrimaryLepton",
    //             CSVBTag(CSVBTag::WP_MEDIUM),
    //             1
    //             ));
    // other_modules.emplace_back(new JetVarProducer<TopJet>(ctx,
    //             "nobtag_boost_mass",
    //             "nobtag_boost_mass",
    //             "PrimaryLepton",
    //             CSVBTag(CSVBTag::WP_MEDIUM),
    //             1
    //             ));
    // other_modules.emplace_back(new JetVarProducer<TopJet>(ctx,
    //             "higgs_tags_1b_med",
    //             "higgs_tags_1b_med",
    //             "PrimaryLepton",
    //             CSVBTag(CSVBTag::WP_MEDIUM),
    //             1
    //             ));
    // other_modules.emplace_back(new JetVarProducer<TopJet>(ctx,
    //             "higgs_tags_2b_med",
    //             "higgs_tags_2b_med",
    //             "PrimaryLepton",
    //             CSVBTag(CSVBTag::WP_MEDIUM),
    //             1
    //             ));

    // other_modules.emplace_back(new JetVarProducer<Jet>(ctx,
    //             "ak4_jets_btagged",
    //             "ak4_jets_btagged",
    //             "higgs_tags_1b_med",
    //             "PrimaryLepton",
    //             CSVBTag(CSVBTag::WP_MEDIUM),
    //             1
    //             ));

    // other_modules.emplace_back(new TopJetDeltaRProducer(ctx,
    //             "topjets",
    //             1
    //             ));
    // other_modules.emplace_back(new TopJetDeltaRProducer(ctx,
    //             "topjets",
    //             2
    //             ));
    // other_modules.emplace_back(new TopJetDeltaRProducer(ctx,
    //             "higgs_tags_1b_med",
    //             1
    //             ));
    // other_modules.emplace_back(new TopJetDeltaRProducer(ctx,
    //             "higgs_tags_2b_med",
    //             1
    //             ));

    
    // other_modules.emplace_back(new GenRecoPtProducer(ctx, "pt_reco_gen_ld_ak4_jet", 1, "pt_ld_ak4_genjet"));
    // other_modules.emplace_back(new GenRecoPtProducer(ctx, "pt_reco_gen_subld_ak4_jet", 2, "pt_subld_ak4_genjet"));
    // other_modules.emplace_back(new GenRecoPtProducer(ctx, "pt_reco_gen_third_ak4_jet", 3, "pt_third_ak4_genjet"));
    // other_modules.emplace_back(new GenRecoPtProducer(ctx, "pt_reco_gen_fourth_ak4_jet", 4, "pt_fourth_ak4_genjet"));
    // other_modules.emplace_back(new GenRecoPtProducer(ctx, "pt_reco_gen_fifth_ak4_jet", 5, "pt_fifth_ak4_genjet"));
    // other_modules.emplace_back(new GenRecoPtProducer(ctx, "pt_reco_gen_sixth_ak4_jet", 6, "pt_sixth_ak4_genjet"));

    





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
    for (auto const & cat : categories) {


        SEL_ITEMS_FULL_SEL.push_back(SEL_ITEMS_BASELINE_SEL);

        if (version.find("thth") != string::npos) {
            other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
                GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::TopID, ParticleID::HiggsID)),
                GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::TopID, ParticleID::HiggsID))
                ));
        }
        else if (version.find("thtz") != string::npos) {
            other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
                GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::TopID, ParticleID::HiggsID)),
                GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::TopID, ParticleID::ZID))
                ));
        }
        else if (version.find("thbw") != string::npos) {
            other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
                GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::TopID, ParticleID::HiggsID)),
                GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::BottomID, ParticleID::WID))
                ));
        }
        else if (version.find("noH_tztz") != string::npos) {
            other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
                GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::TopID, ParticleID::ZID)),
                GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::TopID, ParticleID::ZID))
                ));
        }
        else if (version.find("noH_tzbw") != string::npos) {
            other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
                GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::TopID, ParticleID::ZID)),
                GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::BottomID, ParticleID::WID))
                ));
        }
        else if (version.find("noH_bwbw") != string::npos) {
            other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
                GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::BottomID, ParticleID::WID)),
                GenParticleId(GenParticleDaughterId(ParticleID::TprimeID, ParticleID::BottomID, ParticleID::WID))
                ));
        }
        else if (version.find("bhbh") != string::npos) {
            other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
                GenParticleId(GenParticleDaughterId(ParticleID::BprimeID, ParticleID::BottomID, ParticleID::HiggsID)),
                GenParticleId(GenParticleDaughterId(ParticleID::BprimeID, ParticleID::BottomID, ParticleID::HiggsID))
                ));
        }
        else if (version.find("bhbz") != string::npos) {
            other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
                GenParticleId(GenParticleDaughterId(ParticleID::BprimeID, ParticleID::BottomID, ParticleID::HiggsID)),
                GenParticleId(GenParticleDaughterId(ParticleID::BprimeID, ParticleID::BottomID, ParticleID::ZID))
                ));
        }
        else if (version.find("bhtw") != string::npos) {
            other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
                GenParticleId(GenParticleDaughterId(ParticleID::BprimeID, ParticleID::BottomID, ParticleID::HiggsID)),
                GenParticleId(GenParticleDaughterId(ParticleID::BprimeID, ParticleID::TopID, ParticleID::WID))
                ));
        }
        else if (version.find("noH_bzbz") != string::npos) {
            other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
                GenParticleId(GenParticleDaughterId(ParticleID::BprimeID, ParticleID::BottomID, ParticleID::ZID)),
                GenParticleId(GenParticleDaughterId(ParticleID::BprimeID, ParticleID::BottomID, ParticleID::ZID))
                ));
        }
        else if (version.find("noH_bztw") != string::npos) {
            other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
                GenParticleId(GenParticleDaughterId(ParticleID::BprimeID, ParticleID::BottomID, ParticleID::ZID)),
                GenParticleId(GenParticleDaughterId(ParticleID::BprimeID, ParticleID::TopID, ParticleID::WID))
                ));
        }
        else if (version.find("noH_twtw") != string::npos) {
            other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
                GenParticleId(GenParticleDaughterId(ParticleID::BprimeID, ParticleID::TopID, ParticleID::WID)),
                GenParticleId(GenParticleDaughterId(ParticleID::BprimeID, ParticleID::TopID, ParticleID::WID))
                ));
        }
        else {
            other_modules.emplace_back(new GenSelectionAcceptProducer(ctx, "gendecay_accept",
                GenParticleId(TrueId<GenParticle>::is_true), GenParticleId(TrueId<GenParticle>::is_true)));
        }



        if (split(cat, "-")[0] == "CombinedElMu") {
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_el45", "Trigger Accept El45", 2, -.5, 1.5));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("trigger_accept_mu45", "Trigger Accept Mu45", 2, -.5, 1.5));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_muon_pt", "Primary Lepton p_T", 90, 0., 900.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_electron_pt", "Primary Lepton p_T", 90, 0., 900.));
            // SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("primary_lepton_pt", "Primary Lepton p_T", 90, 0., 900.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_ld_ak4_jet", "Pt leading Ak4 Jet", 100, 0., 2000.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_subld_ak4_jet", "Pt leading Ak4 Jet", 40, 0., 1600.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 6, -.5, 5.5));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 6, -.5, 5.5));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 10, -.5, 9.5));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("met", "MET", 50, 0, 1000));
            // SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 6, -.5, 5.5));
            // SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 6, -.5, 5.5));
            // SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 10, -.5, 9.5));
            
        }
        if (split(cat, "_")[0] == "Mu45") {
            for (auto const & sel_item : SEL_ITEMS_Mu45_SEL)
                SEL_ITEMS_FULL_SEL.back().push_back(sel_item);
        }
        else if (split(cat, "_")[0] == "El45") {
            for (auto const & sel_item : SEL_ITEMS_EL45_SEL)
                SEL_ITEMS_FULL_SEL.back().push_back(sel_item);
        }
        else if (split(cat, "_")[0] == "MuElComb") {
            for (auto const & sel_item : SEL_ITEMS_COMB_SEL)
                SEL_ITEMS_FULL_SEL.back().push_back(sel_item);
        }
        else if (split(cat, "_")[0] == "El45Tight") {
            for (auto const & sel_item : SEL_ITEMS_EL45TIGHT_SEL)
                SEL_ITEMS_FULL_SEL.back().push_back(sel_item);
        }
        // else if (split(cat, "_")[0] == "El45MVALoose") {
        //     for (auto const & sel_item : SEL_ITEMS_EL45MVALOOSE_SEL)
        //         SEL_ITEMS_FULL_SEL.back().push_back(sel_item);
        // }
        // else if (split(cat, "_")[0] == "El45MVATight") {
        //     for (auto const & sel_item : SEL_ITEMS_EL45MVATIGHT_SEL)
        //         SEL_ITEMS_FULL_SEL.back().push_back(sel_item);
        // }

        if (split(cat, "_")[1] == "Baseline") {
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("met", "MET", 50, 0, 1000));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 6, -.5, 5.5));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 6, -.5, 5.5));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 10, -.5, 9.5));
        }
        else if (split(cat, "_")[1] == "H2B") {
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 10, -.5, 9.5, 1));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 6, -.5, 5.5, 1));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 6, -.5, 5.5));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("met", "MET", 50, 0, 1000));
        }
        else if (split(cat, "_")[1] == "H1B") {
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 10, -.5, 9.5, 1));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 6, -.5, 5.5, 1));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 6, -.5, 5.5, 0, 0));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("met", "MET", 50, 0, 1000));
        }
        else if (split(cat, "_")[1] == "Sideband") {
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("met", "MET", 50, 0, 1000, 100.));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 10, -.5, 9.5, 1));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 6, -.5, 5.5, 0, 0));
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 6, -.5, 5.5));
        }

        // if (split(cat, "-")[0] == "Mu45_Baseline") {
        //     for (auto const & sel_item : SEL_ITEMS_Mu45_SEL)
        //         SEL_ITEMS_FULL_SEL.back().push_back(sel_item);
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("met", "MET", 50, 0, 1000));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 6, -.5, 5.5));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 6, -.5, 5.5));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 10, -.5, 9.5));
        // }
        // if (split(cat, "-")[0] == "El45_Baseline") {
        //     for (auto const & sel_item : SEL_ITEMS_EL45_SEL)
        //         SEL_ITEMS_FULL_SEL.back().push_back(sel_item);
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("met", "MET", 50, 0, 1000));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 6, -.5, 5.5));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 6, -.5, 5.5));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 10, -.5, 9.5));
        // }
        // else if (split(cat, "-")[0] == "El45_H2B") {
        //     for (auto const & sel_item : SEL_ITEMS_EL45_SEL)
        //         SEL_ITEMS_FULL_SEL.back().push_back(sel_item);
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 10, -.5, 9.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 6, -.5, 5.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 6, -.5, 5.5));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("met", "MET", 50, 0, 1000));
        // }
        // else if (split(cat, "-")[0] == "El45_H1B") {
        //     for (auto const & sel_item : SEL_ITEMS_EL45_SEL)
        //         SEL_ITEMS_FULL_SEL.back().push_back(sel_item);
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 10, -.5, 9.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 6, -.5, 5.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 6, -.5, 5.5, 0, 0));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("met", "MET", 50, 0, 1000));
        // }
        // else if (split(cat, "-")[0] == "El45_Sideband") {
        //     for (auto const & sel_item : SEL_ITEMS_EL45_SEL)
        //         SEL_ITEMS_FULL_SEL.back().push_back(sel_item);
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("met", "MET", 50, 0, 1000, 100.));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 10, -.5, 9.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 6, -.5, 5.5, 0, 0));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 6, -.5, 5.5));
        // }
        // else if (split(cat, "-")[0] == "Mu45_H2B") {
        //     for (auto const & sel_item : SEL_ITEMS_Mu45_SEL)
        //         SEL_ITEMS_FULL_SEL.back().push_back(sel_item);
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 10, -.5, 9.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 6, -.5, 5.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 6, -.5, 5.5));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("met", "MET", 50, 0, 1000));
        // }
        // else if (split(cat, "-")[0] == "Mu45_H1B") {
        //     for (auto const & sel_item : SEL_ITEMS_Mu45_SEL)
        //         SEL_ITEMS_FULL_SEL.back().push_back(sel_item);
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 10, -.5, 9.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 6, -.5, 5.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 6, -.5, 5.5, 0, 0));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("met", "MET", 50, 0, 1000));
        // }
        // else if (split(cat, "-")[0] == "Mu45_Sideband") {
        //     for (auto const & sel_item : SEL_ITEMS_Mu45_SEL)
        //         SEL_ITEMS_FULL_SEL.back().push_back(sel_item);
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("met", "MET", 50, 0, 1000, 100.));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 10, -.5, 9.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 6, -.5, 5.5, 0, 0));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 6, -.5, 5.5));
        // }
        // else if (split(cat, "-")[0] == "Mu45_H2B") {
        //     for (auto const & sel_item : SEL_ITEMS_Mu45_SEL)
        //         SEL_ITEMS_FULL_SEL.back().push_back(sel_item);
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 10, -.5, 9.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 6, -.5, 5.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 6, -.5, 5.5));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("met", "MET", 50, 0, 1000));
        // }
        // else if (split(cat, "-")[0] == "Mu45_H1B") {
        //     for (auto const & sel_item : SEL_ITEMS_Mu45_SEL)
        //         SEL_ITEMS_FULL_SEL.back().push_back(sel_item);
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 10, -.5, 9.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 6, -.5, 5.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 6, -.5, 5.5, 0, 0));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("met", "MET", 50, 0, 1000));
        // }
        // else if (split(cat, "-")[0] == "Mu45_Sideband") {
        //     for (auto const & sel_item : SEL_ITEMS_Mu45_SEL)
        //         SEL_ITEMS_FULL_SEL.back().push_back(sel_item);
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("met", "MET", 50, 0, 1000, 100.));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_additional_btags_medium", "N(non-overlapping medium b-tags)", 10, -.5, 9.5, 1));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_1b_med", "N(Higgs-Tags, 1 med b)", 6, -.5, 5.5, 0, 0));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatI("n_higgs_tags_2b_med", "N(Higgs-Tags, 2 med b)", 6, -.5, 5.5));
        // }


        for (auto const & sel_item : ADDITIONAL_SEL_ITEMS)
            SEL_ITEMS_FULL_SEL.back().push_back(sel_item);

        for (auto const & dr_plot : deltaR_plots)
            SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF(dr_plot, dr_plot, 50, 0., 5.));

        // if (type == "MC") {
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatD("parton_ht", "Parton HT", 45, 0, 4500));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_ld_ak4_genjet", "Pt first Ak4 GenJet", 100, 0., 2000.));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_subld_ak4_genjet", "Pt second Ak4 GenJet", 40, 0., 1600.));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_third_ak4_genjet", "Pt third Ak4 GenJet", 50, 0., 1000.));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_fourth_ak4_genjet", "Pt fourth Ak4 GenJet", 30, 0., 600.));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_fifth_ak4_genjet", "Pt fifth Ak4 GenJet", 25, 0., 500.));
        //     SEL_ITEMS_FULL_SEL.back().emplace_back(new SelDatF("pt_sixth_ak4_genjet", "Pt sixth Ak4 GenJet", 20, 0., 400.));
        // }


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


        if (split(cat, "-")[0] == "CombinedElMu") {
            sel_helpers.back()->fill_hists_vector(v_lep_combined_hists, "CombinedElMu");
            v_lep_combined_hists.emplace_back(new OwnHistCollector(ctx, "CombinedElMu", type == "MC", CSVBTag(CSVBTag::WP_MEDIUM), {"ev", "mu", "el", "jet", "lumi", "cmstopjet"}));
            v_lep_combined_hists.emplace_back(new ExtendedTopJetHists(ctx, "CombinedElMu/HTags", CSVBTag(CSVBTag::WP_MEDIUM), 2, "higgs_tags_1b_med"));
            v_lep_combined_hists.emplace_back(ak8jet_hists->book_histograms(ctx, "CombinedElMu"));
            continue;
        }

        if (split(cat, "_")[0] == "MuElComb") {
            sel_modules.back()->insert_selection(1, new TriggerAwareHandleSelection<float>(ctx, "pt_subld_ak4_jet", "trigger_accept_el45", 65., 0.));
            sel_modules.back()->insert_selection(1, new TriggerAwareHandleSelection<float>(ctx, "pt_ld_ak4_jet", "trigger_accept_el45", 250., 0.));
            nm1_hists->insert_hists(1, new HandleHist<float>(ctx, cat+"/Nm1Selection", "pt_subld_ak4_jet", "Pt subleading Ak4 Jet", 40, 0., 1600.));
            nm1_hists->insert_hists(1, new HandleHist<float>(ctx, cat+"/Nm1Selection", "pt_ld_ak4_jet", "Pt leading Ak4 Jet", 100, 0., 2000.));
            cf_hists->insert_step(1, "pt_subld_ak4_jet");
            cf_hists->insert_step(1, "pt_ld_ak4_jet");
            v_hists_after_sel.back().emplace_back(new HandleHist<float>(ctx, cat+"/PostSelection", "pt_subld_ak4_jet", "Pt subleading Ak4 Jet", 40, 0., 1600.));
            v_hists_after_sel.back().emplace_back(new HandleHist<float>(ctx, cat+"/PostSelection", "pt_ld_ak4_jet", "Pt leading Ak4 Jet", 100, 0., 2000.));
        }
        
        for (auto hist : selected_sel_hists) {
            // hist.second->insert_hist_and_sel(pos_2d_cut, new TwoDCutHist(ctx, cat+"/"+hist.first, "TwoDcut_Dr_noIso", "TwoDcut_Dpt_noIso", "twod_cut_hist_noIso"), "twoD_cut");
            // for (auto const & hist_helper : ak8jet_hists) {
            hist.second->insert_additional_hist(new OwnHistCollector(ctx, cat+"/"+hist.first, type == "MC", CSVBTag(CSVBTag::WP_MEDIUM), {"el", "cmstopjet"}));
            hist.second->insert_additional_hist(new ExtendedTopJetHists(ctx, cat+"/"+hist.first+"/HTags", CSVBTag(CSVBTag::WP_MEDIUM), 2, "higgs_tags_1b_med"));
            if (split(cat, "_")[0] == "MuElComb") {
                hist.second->insert_hist_and_sel(1, new HandleHist<float>(ctx, cat+"/"+hist.first, "pt_ld_ak4_jet", "Pt leading Ak4 Jet", 100, 0., 2000.), "pt_ld_ak4_jet");
                hist.second->insert_hist_and_sel(1, new HandleHist<float>(ctx, cat+"/"+hist.first, "pt_subld_ak4_jet", "Pt subleading Ak4 Jet", 40, 0., 1600.), "pt_subld_ak4_jet");
            }
            // }
            v_hists.back().emplace_back(hist.second);
        }

        v_hists.back().emplace_back(nm1_hists);
        v_hists.back().emplace_back(cf_hists);
        sel_helpers.back()->fill_hists_vector(v_hists.back(), cat+"/NoSelection");
        sel_helpers.back()->fill_hists_vector(v_hists_after_sel.back(), cat+"/PostSelection");
        // sel_helpers.back()->fill_hists_vector(v_reweighted_hists_after_sel.back(), cat+"/PostSelectionReweighted");
        // for (auto const & hist_helper : ak8jet_hists) {
        // if (version.find("thth") != string::npos) {
        //     v_genhist_2h_after_sel.back().emplace_back(new HiggsGenHist(ctx, cat+"/PostSelection/HiggsGen2Higgs/HiggsGenAllAk8", "topjets", "2h"));
        //     v_genhist_2h_after_sel.back().emplace_back(new HiggsGenHist(ctx, cat+"/PostSelection/HiggsGen2Higgs/HiggsGenHiggsCands", "ak8_higgs_cand", "2h"));
        //     v_genhist_2h_after_sel.back().emplace_back(new HiggsGenHist(ctx, cat+"/PostSelection/HiggsGen2Higgs/HiggsGenHiggsTags1b", "higgs_tags_1b_med", "2h"));
        //     v_genhist_2h_after_sel.back().emplace_back(new HiggsGenHist(ctx, cat+"/PostSelection/HiggsGen2Higgs/HiggsGenHiggsTags2b", "higgs_tags_2b_med", "2h"));
        // }
        // if (version.find("thtz") != string::npos || version.find("thbw") != string::npos) {
        //     v_genhist_1h_after_sel.back().emplace_back(new HiggsGenHist(ctx, cat+"/PostSelection/HiggsGen1Higgs/HiggsGenAllAk8", "topjets", "1h"));
        //     v_genhist_1h_after_sel.back().emplace_back(new HiggsGenHist(ctx, cat+"/PostSelection/HiggsGen1Higgs/HiggsGenHiggsCands", "ak8_higgs_cand", "1h"));
        //     v_genhist_1h_after_sel.back().emplace_back(new HiggsGenHist(ctx, cat+"/PostSelection/HiggsGen1Higgs/HiggsGenHiggsTags1b", "higgs_tags_1b_med", "1h"));
        //     v_genhist_1h_after_sel.back().emplace_back(new HiggsGenHist(ctx, cat+"/PostSelection/HiggsGen1Higgs/HiggsGenHiggsTags2b", "higgs_tags_2b_med", "1h"));
        // }
        v_hists_after_sel.back().emplace_back(ak8jet_hists->book_histograms(ctx, cat+"/PostSelection"));
        v_hists_after_sel.back().emplace_back(new OwnHistCollector(ctx, cat+"/PostSelection", type == "MC", CSVBTag(CSVBTag::WP_MEDIUM), {"ev", "mu", "el", "jet", "lumi", "cmstopjet"}));
        if (type == "MC") {
            CustomizableGenHists * gen_hists = new CustomizableGenHists(ctx, cat+"/PostSelection/GenHists");
            gen_hists->add_genhistcoll(8000001, 0, {"mass", "decay", "dRDecay", "dPhiDecay", "dEtaDecay"});
            gen_hists->add_genhistcoll(8000001, 0, {"mass", "decay", "dRDecay", "dPhiDecay", "dEtaDecay"}, GenParticleId(GenParticleDaughterId(8000001, 6, 25)), "_to_tH");
            gen_hists->add_genhistcoll(6, 0, {"decay", "dRDecay", "dPhiDecay", "dEtaDecay"});
            gen_hists->add_genhistcoll(25, 0, {"decay", "dRDecay", "dPhiDecay", "dEtaDecay"});
            gen_hists->add_genhistcoll(25, 0, {"decay", "dRDecay", "dPhiDecay", "dEtaDecay"}, GenParticleId(GenParticleDaughterId(25, 5, 5)), "_to_bb");
            v_hists_after_sel.back().push_back(unique_ptr<CustomizableGenHists>(gen_hists)); 
            v_hists_after_sel.back().emplace_back(new RecoGenVarComp<double>(ctx, cat+"/PostSelection/RecoGenComparisons", "HT", "parton_ht", "HT_parton")); 
            v_hists_after_sel.back().emplace_back(new RecoGenVarComp<double>(ctx, cat+"/PostSelection/RecoGenComparisons", "HT", "gen_ht", "HT_gen")); 
            // v_hists_after_sel.back().emplace_back(new RecoGenVarComp<float>(ctx, cat+"/PostSelection/RecoGenComparisons", "pt_ld_ak4_jet", "pt_ld_ak4_genjet", "pt_ld_ak4_jet")); 
            // v_hists_after_sel.back().emplace_back(new RecoGenVarComp<float>(ctx, cat+"/PostSelection/RecoGenComparisons", "pt_subld_ak4_jet", "pt_subld_ak4_genjet", "pt_subld_ak4_jet")); 
            // v_hists_after_sel.back().emplace_back(new RecoGenVarComp<float>(ctx, cat+"/PostSelection/RecoGenComparisons", "pt_third_ak4_jet", "pt_third_ak4_genjet", "pt_third_ak4_jet")); 
            // v_hists_after_sel.back().emplace_back(new RecoGenVarComp<float>(ctx, cat+"/PostSelection/RecoGenComparisons", "pt_fourth_ak4_jet", "pt_fourth_ak4_genjet", "pt_fourth_ak4_jet")); 
            // v_hists_after_sel.back().emplace_back(new RecoGenVarComp<float>(ctx, cat+"/PostSelection/RecoGenComparisons", "pt_fifth_ak4_jet", "pt_fifth_ak4_genjet", "pt_fifth_ak4_jet")); 
            // v_hists_after_sel.back().emplace_back(new RecoGenVarComp<float>(ctx, cat+"/PostSelection/RecoGenComparisons", "pt_sixth_ak4_jet", "pt_sixth_ak4_genjet", "pt_sixth_ak4_jet")); 
            
            if (version.find("TT") != string::npos)
                v_hists_after_sel.back().emplace_back(new TTbarGenHists(ctx, cat+"/PostSelection/TTGenHists"));
            if (create_btag_eff)
                v_hists_after_sel.back().emplace_back(new BTagMCEfficiencyHists(ctx, cat+"/BTagMCEfficiencyHists", CSVBTag::WP_MEDIUM, "tj_btag_sf_coll"));
        }
        v_hists_after_sel.back().emplace_back(new ExtendedTopJetHists(ctx, cat+"/PostSelection/HTags", CSVBTag(CSVBTag::WP_MEDIUM), 2, "higgs_tags_1b_med"));
        for (auto const & dr_plot : deltaR_plots) {
            v_hists_after_sel.back().emplace_back(new VarSTComparison(ctx, cat+"/PostSelection/STDeltaRComparisons", dr_plot));
        }
        // v_hists_after_sel.back().emplace_back(new ExtendedTopJetHists(ctx, cat+"/PostSelection/Ak8JetsUnCleaned", CSVBTag(CSVBTag::WP_MEDIUM), 2, "topjets"));
        // v_hists_after_sel.back().emplace_back(new ExtendedTopJetHists(ctx, cat+"/PostSelection/Ak8JetsCleaned", CSVBTag(CSVBTag::WP_MEDIUM), 2, "topjets_cleaned"));
        // v_reweighted_hists_after_sel.back().emplace_back(new OwnHistCollector(ctx, cat+"/PostSelectionReweighted", type == "MC", CSVBTag(CSVBTag::WP_MEDIUM), {"ev", "mu", "el", "jet", "lumi", "cmstopjet"}));
        // v_hists_after_sel.back().emplace_back(new JetCleaningControlPlots(ctx, cat+"/PostSelection/JetCleaningControlPlots", "weight_ak4_jetpt", "weight_ak8_jetpt"));
        // v_hists_after_sel.back().emplace_back(new JetCleaningControlPlots(ctx, cat+"/PostSelection/JetCleaningControlPlotsUp", "weight_ak4_jetpt_up"));
        // v_hists_after_sel.back().emplace_back(new JetCleaningControlPlots(ctx, cat+"/PostSelection/JetCleaningControlPlotsDown", "weight_ak4_jetpt_down"));

            // v_hists_after_sel.emplace_back(new HistCollector(ctx, "EventHistsPost"));

        // }
    }


}


bool TpTpFinalSelectionTreeOutput::process(Event & event) {

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

    int base_el_ind = -1;
    for (unsigned i = 0; i < categories.size(); ++i) {
        if (categories[i] == "El45_Baseline")
            base_el_ind = i;
    }

    // index 0 corresponds to combined
    for (unsigned i = 0; i < sel_modules.size(); ++i) {
    
        bool all_accepted = sel_modules[i]->process(event);
        sel_modules_passed.push_back(all_accepted);

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

    if (base_el_ind >= 0 && sel_modules_passed[base_el_ind]) {
        ele_trg_sf->process(event);
    }
    else
        ele_trg_nosf->process(event);


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

UHH2_REGISTER_ANALYSIS_MODULE(TpTpFinalSelectionTreeOutput)
