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


#include "UHH2/VLQToHiggsPairProd/include/VLQToHiggsPairProdHists.h"
#include "UHH2/VLQToHiggsPairProd/include/VLQToHiggsPairProdSelections.h"
#include "UHH2/VLQToHiggsPairProd/include/GenHists.h"
#include "UHH2/VLQToHiggsPairProd/include/AdditionalModules.h"


using namespace std;
using namespace uhh2;

using namespace vlqToHiggsPair;

// static int event_count = 0;

/** \brief Basic analysis example of an AnalysisModule (formerly 'cycle') in UHH2
 * 
 * This is the central class which calls other AnalysisModules, Hists or Selection classes.
 * This AnalysisModule, in turn, is called (via AnalysisModuleRunner) by SFrame.
 */

class PreSelection: public AnalysisModule {
public:

    enum ParticleID {
        BottomID = 5,
        TopID = 6,
        TprimeID = 8,
        ElectronID = 11,
        MuonID = 13,
        HiggsID = 25
    };
    
    explicit PreSelection(Context & ctx);
    virtual bool process(Event & event);

private:

    std::string version;

    // // declare the Selections to use.
    // std::vector<std::unique_ptr<Selection> > v_sel;

    std::map<const char *, std::shared_ptr<Selection> > reco_cuts;

    // with/without gen selection, final reco selection, only reco plots
    std::pair<std::unique_ptr<Hists> , std::unique_ptr<AndSelection> >
            preselection
            // gensel_fin_onemu
            ;
    
    std::vector<std::unique_ptr<AnalysisModule> > pre_modules, post_modules;



    // handles
    // Event::Handle<bool> pass_gensel_;
    Event::Handle<double> parton_ht;
   
    // internal function to fill all histograms
};


PreSelection::PreSelection(Context & ctx) {

    
    // If running in SFrame, the keys "dataset_version", "dataset_type" and "dataset_lumi"
    // are set to the according values in the xml file. For CMSSW, these are
    // not set automatically, but can be set in the python config file.
    // for(auto kv : ctx.get_all()){
    //     cout << " " << kv.first << " = " << kv.second << endl;
    // }

    
    // 1. define handles and other stuff here for later call in PreSelection::process

    version = ctx.get("dataset_version");

    CSVBTag::wp btag_wp = CSVBTag::WP_MEDIUM;

    // btag = CSVBTag(btag_wp);
    // toptag =CMSTopTag();

    // pass_gensel_ = ctx.get_handle<bool>("pass_gensel");
    parton_ht = ctx.get_handle<double>("parton_ht");
    





    // 2. setup other modules


    // all the reweighting and jet correction modules
    bool mclumiweight = true;
    bool mcpileupreweight = true;
    bool jec = true;
    bool jersmear = true;

    bool is_mc = ctx.get("dataset_type") == "MC";
    if(is_mc){
        // calculate gen variables
        pre_modules.emplace_back(new NGenParticleCalculator(ctx, "n_gen_bfromtop", ParticleID::BottomID, ParticleID::TopID));
        pre_modules.emplace_back(new NGenParticleCalculator(ctx, "n_gen_higgs", ParticleID::HiggsID));
        pre_modules.emplace_back(new NGenParticleCalculator(ctx, "n_gen_electron", ParticleID::ElectronID, ParticleID::TopID));
        pre_modules.emplace_back(new NGenParticleCalculator(ctx, "n_gen_muon", ParticleID::MuonID, ParticleID::TopID));
        pre_modules.emplace_back(new PartonHT(parton_ht));
        if(mclumiweight)  pre_modules.emplace_back(new MCLumiWeight(ctx));
        if(mcpileupreweight) pre_modules.emplace_back(new MCPileupReweight(ctx));
        if(jec) post_modules.emplace_back(new JetCorrector(JERFiles::PHYS14_L123_MC));
        if(jersmear) post_modules.emplace_back(new JetResolutionSmearer(ctx));
    }
    else{
        if(jec) post_modules.emplace_back(new JetCorrector(JERFiles::PHYS14_L123_DATA));
    }

    //cleaning modules
    post_modules.emplace_back(new ElectronCleaner(AndId<Electron>(ElectronID_PHYS14_25ns_medium, PtEtaCut(20.0, 2.4))));
    post_modules.emplace_back(new MuonCleaner(AndId<Muon>(MuonIDTight(), PtEtaCut(20.0, 2.1))));
    post_modules.emplace_back(new JetLeptonCleaner(JERFiles::PHYS14_L123_MC));
    post_modules.emplace_back(new JetCleaner(PtEtaCut(30.0, 2.4)));
    post_modules.emplace_back(new JetPtSorter());

    // calculate values like HT, number of b-tags, top-tags etc.
    post_modules.emplace_back(new HTCalculator(ctx));
    post_modules.emplace_back(new PrimaryLepton(ctx));
    // post_modules.emplace_back(new HTLepCalculator(ctx));
    post_modules.emplace_back(new JetTagCalculator(ctx, "n_btags", CSVBTag(btag_wp)));
    post_modules.emplace_back(new TopTagCalculator(ctx.get_handle<int>("n_toptags"), CMSTopTag()));



    // 3. set up no-cuts histograms

    // 4. set final reco selections (and the gen selection)


    // DEFINE RECO SELECTIONS HERE
    reco_cuts["PrimLepCut"] = std::shared_ptr<Selection>(new PrimaryLeptonPtSelection(ctx.get_handle<FlavorParticle>("PrimaryLepton"), 50.));
    reco_cuts["STCut"] = std::shared_ptr<Selection>(new STSelection(ctx.get_handle<double>("HT"), ctx.get_handle<FlavorParticle>("PrimaryLepton"), 500.));
    // REMOVE BTAG CUT FROM PRESELECTION
    // reco_cuts["BTagCut"] = std::shared_ptr<Selection>(new NJetSelection(1, -1, JetId(CSVBTag(btag_wp))));
    reco_cuts["JetPtCut"] = std::shared_ptr<Selection>(new JetPtSelection(200.));



    // // 5. set up hists and selections


    preselection.first.reset(new HistCollector(ctx, "PreSelection"));
    preselection.second.reset(new AndSelection(ctx, "preselection"));

    // gensel_fin_onemu.first.reset(new HistCollector(ctx, "GenSel-AllCuts"));
    // gensel_fin_onemu.second.reset(new AndSelection(ctx, "gensel_allcuts"));
    // gensel_fin_onemu.second->add<BoolSelection>("gen_finalstate_sel", pass_gensel_);

    preselection.second->add("PrimLepCut", reco_cuts["PrimLepCut"]);
    preselection.second->add("STCut", reco_cuts["STCut"]);
    preselection.second->add("JetPtCut", reco_cuts["JetPtCut"]);


}


bool PreSelection::process(Event & event) {

    // cout << "PreSelection: Starting to process event (runid, eventid) = (" << event.run << ", " << event.event << ")" << endl;

    // TEST STUFF HERE



    // FIRST RUN PRE_MODULES THAT NEED TO RUN AT THE BEGINNING (e.g. MC lumi re-weighting)

    for(auto & m: pre_modules){
        m->process(event);
    }

    // differentiate between pre_modules and post_modules if you want to make some plots before cleaning the histograms

    for (auto & m: post_modules){
        m->process(event);
    }

    if (preselection.second->passes(event))
    {
        preselection.first->fill(event);
        return true;
    }

    
    return false;
}

UHH2_REGISTER_ANALYSIS_MODULE(PreSelection)
