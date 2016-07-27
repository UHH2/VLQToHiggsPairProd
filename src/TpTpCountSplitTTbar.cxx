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

class TpTpCountSplitTTbar: public AnalysisModule {
public:

    explicit TpTpCountSplitTTbar(Context & ctx);
    virtual bool process(Event & event) override;

private:
    unique_ptr<AnalysisModule> common_module, gensel_0to700, gensel_700to1000, gensel_1000toInf;
    vector<unique_ptr<AnalysisModule>> other_modules;
    // unique_ptr<NParticleMultiHistProducerHelper<TopJet>> ak8jet_hists/*, ca15jet_hists*/;
    // Event::Handle<float> jetpt_weight_hndl;
    // vector<vector<unique_ptr<Hists>>> v_reweighted_hists_after_sel;
    vector<vector<unique_ptr<Hists>>> v_hists;
    unique_ptr<Hists> count_total, count_0to700, count_700to1000, count_1000toInf;
    // int count_total, count_0to700, count_700to1000, count_1000toInf;

};


class CountHist: public Hists {
public:
    explicit CountHist(Context & ctx,
                             const string & dirname,
                             const string & histname):
        Hists(ctx, dirname),
        hist(book<TH1F>(histname,
                        "count events",
                        1, -.5, .5)) {}

    virtual void fill(const Event &) override {
        hist->Fill(0.);
    }

private:
    TH1F * hist;
};



TpTpCountSplitTTbar::TpTpCountSplitTTbar(Context & ctx) {

    // bool is_background = (version.find("TpTp") == string::npos && type == "MC") ;
    string version = ctx.get("dataset_version", "");
    string type = ctx.get("dataset_type", "");

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

    // count_total = 0;
    // count_0to700 = 0;
    // count_700to1000 = 0;
    // count_1000toInf = 0;
    count_total.reset(new CountHist(ctx, "CountEvents", "count_total"));
    count_0to700.reset(new CountHist(ctx, "CountEvents", "count_0to700"));
    count_700to1000.reset(new CountHist(ctx, "CountEvents", "count_700to1000"));
    count_1000toInf.reset(new CountHist(ctx, "CountEvents", "count_1000toInf"));


    gensel_0to700.reset(new GenMassTTbarSelection(ctx, 0., 700.));
    gensel_700to1000.reset(new GenMassTTbarSelection(ctx, 700., 1000.));
    gensel_1000toInf.reset(new GenMassTTbarSelection(ctx, 1000.));

    

    // Top-pt reweighting (see https://twiki.cern.ch/twiki/bin/view/CMS/TopPtReweighting#Eventweight):
    // a and b parameters from the 8 TeV l+jets channel (see twiki) are used, these are
    // a = 0.159, b = -0.00141
    // the overall event weight ratio between not applying and applying the top pt reweighting is
    // 9.910819e-01 = 0.9910819 as calculated with TpTpTTbarWeight.cxx
    // In the end, the overall weight that you apply thus needs to be multiplied by 1./0.9919819

    if (version.find("TT") != string::npos) {
        other_modules.emplace_back(new TTbarGenProducer(ctx, "ttbargen", false));
    }


    v_hists.emplace_back(vector<unique_ptr<Hists>>());

    if (type == "MC") {
        CustomizableGenHists * gen_hists = new CustomizableGenHists(ctx, "GenHists");
        gen_hists->add_genhistcoll(8000001, 0, {"mass", "decay", "dRDecay", "dPhiDecay", "dEtaDecay"});
        gen_hists->add_genhistcoll(8000001, 0, {"mass", "decay", "dRDecay", "dPhiDecay", "dEtaDecay"}, GenParticleId(GenParticleDaughterId(8000001, 6, 25)), "_to_tH");
        gen_hists->add_genhistcoll(6, 0, {"decay", "dRDecay", "dPhiDecay", "dEtaDecay"});
        gen_hists->add_genhistcoll(25, 0, {"decay", "dRDecay", "dPhiDecay", "dEtaDecay"});
        gen_hists->add_genhistcoll(25, 0, {"decay", "dRDecay", "dPhiDecay", "dEtaDecay"}, GenParticleId(GenParticleDaughterId(25, 5, 5)), "_to_bb");
        v_hists.back().push_back(unique_ptr<CustomizableGenHists>(gen_hists)); 
       
        if (version.find("TT") != string::npos)
            v_hists.back().emplace_back(new TTbarGenHists(ctx, "TTGenHists"));
    }


}


bool TpTpCountSplitTTbar::process(Event & event) {

    common_module->process(event);

    for (auto & mod : other_modules) {
        mod->process(event);
    }

    // count_total++;
    count_total->fill(event);

    if (gensel_0to700->process(event))
        // count_0to700++;
        count_0to700->fill(event);
    if (gensel_700to1000->process(event))
        // count_700to1000++;
        count_700to1000->fill(event);
    if (gensel_1000toInf->process(event))
        // count_1000toInf++;
        count_1000toInf->fill(event);

    
    // all hists
    for (auto & hist_vec : v_hists) {
        for (auto & hist : hist_vec) {
            hist->fill(event);
        }
    }




    return false;
}

UHH2_REGISTER_ANALYSIS_MODULE(TpTpCountSplitTTbar)
