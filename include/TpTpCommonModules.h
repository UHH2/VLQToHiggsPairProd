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
        CommonModules* commonObjectCleaning = new CommonModules();
        commonObjectCleaning->set_jet_id(AndId<Jet>(JetPFID(JetPFID::WP_LOOSE), PtEtaCut(30.0,7.0)));
        commonObjectCleaning->disable_jersmear();
        // commonObjectCleaning->disable_mcpileupreweight();
        commonObjectCleaning->set_electron_id(AndId<Electron>(ElectronID_Spring15_25ns_medium_noIso,PtEtaCut(20.0, 2.4)));
        commonObjectCleaning->set_muon_id(AndId<Muon>(MuonIDTight(),PtEtaCut(20.0, 2.1)));
        commonObjectCleaning->switch_jetlepcleaner(true);
        commonObjectCleaning->switch_jetPtSorter(true);
        commonObjectCleaning->init(ctx);
        common_module.reset(commonObjectCleaning);


        modules.emplace_back(new PrimaryLepton(ctx, "PrimaryLepton", 9999.f, 10.f)); 
        modules.emplace_back(new PrimaryLeptonOwn<Muon>(ctx, "muons", "PrimaryMuon_iso", MuonId(MuonIso())));
        modules.emplace_back(new PrimaryLeptonOwn<Muon>(ctx, "muons", "PrimaryMuon_noIso"));
        modules.emplace_back(new HTCalculator(ctx, boost::none, "HT"));
        modules.emplace_back(new STCalculator(ctx, "ST"));
        modules.emplace_back(new CollectionProducer<Jet>(ctx,
            "jets",
            "b_jets",
            JetId(CSVBTag(CSVBTag::WP_MEDIUM))
            ));
        modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
            "jets",
            "n_btags_loose",
            JetId(CSVBTag(CSVBTag::WP_LOOSE))
            ));
        modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
            "jets",
            "n_btags_medium",
            JetId(CSVBTag(CSVBTag::WP_MEDIUM))
            ));
        modules.emplace_back(new CollectionSizeProducer<Jet>(ctx,
            "jets",
            "n_btags_tight",
            JetId(CSVBTag(CSVBTag::WP_TIGHT))
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
        modules.emplace_back(new PartPtProducer<TopJet>(ctx, "toptags", "smallest_pt_toptags", -1));

        modules.emplace_back(new PrimaryLeptonInfoProducer(ctx, "PrimaryLepton", "primary_lepton_pt"));
        modules.emplace_back(new PrimaryLeptonInfoProducer(ctx, "PrimaryMuon_iso", "primary_muon_pt_iso", "primary_muon_eta_iso", "primary_muon_charge_iso"));
        modules.emplace_back(new PrimaryLeptonInfoProducer(ctx, "PrimaryMuon_noIso", "primary_muon_pt_noIso", "primary_muon_eta_noIso", "primary_muon_charge_noIso"));
    }

    virtual bool process(Event & event) override {
        if (!common_module->process(event))
            return false;
        for (auto & mod : modules)
            mod->process(event);
        return true;
    }

private:
    vector<unique_ptr<AnalysisModule>> modules;
    unique_ptr<AnalysisModule> common_module;

};