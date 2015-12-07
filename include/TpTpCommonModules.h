#pragma once

#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/common/include/CommonModules.h"
#include "UHH2/common/include/PrimaryLepton.h"
#include "UHH2/common/include/CollectionProducer.h"
#include "UHH2/common/include/ObjectIdUtils.h"

#include "UHH2/VLQSemiLepPreSel/include/VLQCommonModules.h"

#include "UHH2/VLQToHiggsPairProd/include/VLQPair_additionalModules.h"


using namespace uhh2;
using namespace std;



class TpTpCommonModules : public AnalysisModule {
public:
    TpTpCommonModules(Context & ctx) {
        // CommonModules* commonObjectCleaning = new CommonModules();
        // // commonObjectCleaning->set_jet_id(AndId<Jet>(JetPFID(JetPFID::WP_LOOSE), PtEtaCut(30.0,2.4)));
        // commonObjectCleaning->disable_jersmear();
        // // commonObjectCleaning->disable_mcpileupreweight();
        // // commonObjectCleaning->set_electron_id(AndId<Electron>(ElectronID_Spring15_25ns_medium_noIso,PtEtaCut(20.0, 2.4)));
        // // commonObjectCleaning->set_muon_id(AndId<Muon>(MuonIDTight(),PtEtaCut(20.0, 2.1)));
        // // commonObjectCleaning->switch_jetlepcleaner(true);
        // // commonObjectCleaning->switch_jetPtSorter(true);
        // // commonObjectCleaning->disable_lumisel();
        // commonObjectCleaning->init(ctx);
        // common_module.reset(commonObjectCleaning);

        // modules.emplace_back(new CollectionProducer<TopJet>(ctx,
        //     "topjets",
        //     "ak8jets_uncleaned"
        //     ));
        // if (ctx.get("dataset_type", "") == "MC") {
        //     modules.emplace_back(new GenericTopJetCorrector(ctx, JERFiles::Summer15_25ns_L123_AK8PFchs_MC, "topjets"));
        //     modules.emplace_back(new GenericTopJetCorrector(ctx, JERFiles::Summer15_25ns_L123_AK8PFchs_MC, "patJetsAk8CHSJetsSoftDropPacked_daughters"));
        //     modules.emplace_back(new GenericTopJetCorrector(ctx, JERFiles::Summer15_25ns_L123_AK8PFchs_MC, "patJetsHepTopTagCHSPacked_daughters"));
        //     modules.emplace_back(new GenericSubJetCorrector(ctx, JERFiles::Summer15_25ns_L123_AK4PFchs_MC, "topjets"));
        //     modules.emplace_back(new GenericSubJetCorrector(ctx, JERFiles::Summer15_25ns_L123_AK4PFchs_MC, "patJetsAk8CHSJetsSoftDropPacked_daughters"));
        //     modules.emplace_back(new GenericSubJetCorrector(ctx, JERFiles::Summer15_25ns_L123_AK4PFchs_MC, "patJetsHepTopTagCHSPacked_daughters"));
        //     modules.emplace_back(new TopJetLeptonCleaner(ctx, JERFiles::Summer15_25ns_L123_AK8PFchs_MC, "topjets"));
        //     // modules.emplace_back(new TopJetLeptonCleaner(ctx, JERFiles::Summer15_25ns_L123_AK8PFchs_MC, "ak8jets_cleaned"));
        //     // modules.emplace_back(new TopJetLeptonCleaner(ctx, JERFiles::Summer15_25ns_L123_AK8PFchs_MC, "patJetsHepTopTagCHSPacked_daughters"));
        //     modules.emplace_back(new GenericTopJetCleaner(ctx, PtEtaCut(150., 2.4), "topjets"));
        //     // modules.emplace_back(new GenericTopJetCleaner(ctx, PtEtaCut(150., 2.4), "ak8jets_cleaned"));
        //     // modules.emplace_back(new GenericTopJetCleaner(ctx, PtEtaCut(150., 2.4), "patJetsHepTopTagCHSPacked_daughters"));
        // }
        // else {
        //     modules.emplace_back(new GenericTopJetCorrector(ctx, JERFiles::Summer15_25ns_L123_AK8PFchs_DATA, "topjets"));
        //     modules.emplace_back(new GenericTopJetCorrector(ctx, JERFiles::Summer15_25ns_L123_AK8PFchs_DATA, "patJetsAk8CHSJetsSoftDropPacked_daughters"));
        //     modules.emplace_back(new GenericTopJetCorrector(ctx, JERFiles::Summer15_25ns_L123_AK8PFchs_DATA, "patJetsHepTopTagCHSPacked_daughters"));
        //     modules.emplace_back(new GenericSubJetCorrector(ctx, JERFiles::Summer15_25ns_L123_AK4PFchs_DATA, "topjets"));
        //     modules.emplace_back(new GenericSubJetCorrector(ctx, JERFiles::Summer15_25ns_L123_AK4PFchs_DATA, "patJetsAk8CHSJetsSoftDropPacked_daughters"));
        //     modules.emplace_back(new GenericSubJetCorrector(ctx, JERFiles::Summer15_25ns_L123_AK4PFchs_DATA, "patJetsHepTopTagCHSPacked_daughters"));
        //     modules.emplace_back(new TopJetLeptonCleaner(ctx, JERFiles::Summer15_25ns_L123_AK8PFchs_DATA, "topjets"));
        //     // modules.emplace_back(new TopJetLeptonCleaner(ctx, JERFiles::Summer15_25ns_L123_AK8PFchs_MC, "ak8jets_cleaned"));
        //     // modules.emplace_back(new TopJetLeptonCleaner(ctx, JERFiles::Summer15_25ns_L123_AK8PFchs_MC, "patJetsHepTopTagCHSPacked_daughters"));
        //     modules.emplace_back(new GenericTopJetCleaner(ctx, PtEtaCut(125., 2.4), "topjets"));
        //     // modules.emplace_back(new GenericTopJetCleaner(ctx, PtEtaCut(150., 2.4), "ak8jets_cleaned"));
        //     // modules.emplace_back(new GenericTopJetCleaner(ctx, PtEtaCut(150., 2.4), "patJetsHepTopTagCHSPacked_daughters"));
        // }

        // h_ak8softdrop_ = ctx.get_handle<vector<TopJet>>("ak8jets_cleaned");
        // h_htt_ = ctx.get_handle<vector<TopJet>>("patJetsHepTopTagCHSPacked_daughters");

        // if(ctx.) modules.emplace_back(new JetLeptonCleaner(JERFiles::Summer15_25ns_L123_AK4PFchs_MC));
        // else modules.emplace_back(new JetLeptonCleaner(JERFiles::Summer15_25ns_L123_AK4PFchs_DATA));
        modules.emplace_back(new PrimaryLepton(ctx, "PrimaryLepton", 9999.f, 10.f)); 
        modules.emplace_back(new PrimaryLeptonOwn<Muon>(ctx, "muons", "PrimaryMuon_noIso"));
        // modules.emplace_back(new PrimaryLeptonOwn<Muon>(ctx, "muons", "PrimaryMuon_dRak8", MuonId(MinMaxDeltaRId<TopJet>(ctx, "topjets", 0.1))));
        modules.emplace_back(new HTCalculator(ctx, boost::none, "HT"));
        modules.emplace_back(new STCalculator(ctx, "ST"));
        modules.emplace_back(new CollectionProducer<Jet>(ctx,
            "jets",
            "b_jets_loose",
            JetId(CSVBTag(CSVBTag::WP_LOOSE))
            ));
        modules.emplace_back(new CollectionProducer<Jet>(ctx,
            "jets",
            "b_jets_medium",
            JetId(CSVBTag(CSVBTag::WP_MEDIUM))
            ));
        modules.emplace_back(new CollectionProducer<Jet>(ctx,
            "jets",
            "b_jets_tight",
            JetId(CSVBTag(CSVBTag::WP_TIGHT))
            ));
        modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
            "b_jets_loose",
            "n_btags_loose"
            // JetId(CSVBTag(CSVBTag::WP_LOOSE))
            ));
        modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
            "b_jets_medium",
            "n_btags_medium"
            // JetId(CSVBTag(CSVBTag::WP_MEDIUM))
            ));
        modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
            "b_jets_tight",
            "n_btags_tight"
            // JetId(CSVBTag(CSVBTag::WP_TIGHT))
            ));


        // Other CutProducers
        modules.emplace_back(new NLeptonsProducer(ctx, "n_leptons"));
        modules.emplace_back(new CollectionSizeProducer<Jet>(ctx, "jets", "n_jets"));
        modules.emplace_back(new METProducer(ctx, "met"));
        modules.emplace_back(new PartPtProducer<Jet>(ctx, "jets", "leading_jet_pt", 1));
        modules.emplace_back(new PartPtProducer<Jet>(ctx, "jets", "subleading_jet_pt", 2));
        modules.emplace_back(new PartPtProducer<Muon>(ctx, "muons", "leading_mu_pt", 1));
        modules.emplace_back(new PartPtProducer<Electron>(ctx, "electrons", "leading_ele_pt", 1));

        // get pt of the top tagged jet with smallest pt, just to see if PtEtaCut Id is working
        // modules.emplace_back(new PartPtProducer<TopJet>(ctx, "toptags", "smallest_pt_toptags", -1));

        modules.emplace_back(new PrimaryLeptonInfoProducer(ctx, "PrimaryLepton", "primary_lepton_pt"));
        modules.emplace_back(new PrimaryLeptonInfoProducer(ctx, "PrimaryMuon_noIso", "primary_muon_pt_noIso", "primary_muon_eta_noIso", "primary_muon_charge_noIso"));
        // modules.emplace_back(new PrimaryLeptonInfoProducer(ctx, "PrimaryMuon_dRak8", "primary_muon_pt_dRak8", "primary_muon_eta_dRak8", "primary_muon_charge_dRak8"));
    }

    virtual bool process(Event & event) override {
        for (auto & mod : modules)
            mod->process(event);
        // if (event.is_valid(h_ak8softdrop_))
        //     sort_by_pt(event.get(h_ak8softdrop_));
        // if (event.is_valid(h_htt_))
        //     sort_by_pt(event.get(h_htt_));
        return true;
    }

private:
    vector<unique_ptr<AnalysisModule>> modules;
    // Event::Handle<vector<TopJet>> h_ak8softdrop_, h_htt_;

};