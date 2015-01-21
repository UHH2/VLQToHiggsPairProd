#include <iostream>
#include <memory>

#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Event.h"
#include "UHH2/common/include/CleaningModules.h"
#include "UHH2/common/include/ElectronIds.h"
#include "UHH2/common/include/MuonIds.h"
#include "UHH2/common/include/EventHists.h"
#include "UHH2/common/include/EventVariables.h"
#include "UHH2/common/include/ElectronHists.h"
#include "UHH2/common/include/MuonHists.h"
#include "UHH2/common/include/JetHists.h"
#include "UHH2/common/include/NSelections.h"
#include "UHH2/VLQToHiggsPairProd/include/VLQToHiggsPairProdHists.h"
#include "UHH2/VLQToHiggsPairProd/include/VLQToHiggsPairProdSelections.h"
#include "UHH2/VLQToHiggsPairProd/include/GenHists.h"

using namespace std;
using namespace uhh2;

/** \brief Basic analysis example of an AnalysisModule (formerly 'cycle') in UHH2
 * 
 * This is the central class which calls other AnalysisModules, Hists or Selection classes.
 * This AnalysisModule, in turn, is called (via AnalysisModuleRunner) by SFrame.
 */
class VLQToHiggsPairProdAnalysis: public AnalysisModule {
public:
    
    explicit VLQToHiggsPairProdAnalysis(Context & ctx);
    virtual bool process(Event & event);

private:

    // // declare the Selections to use.
    // std::vector<std::unique_ptr<Selection> > v_sel;
    
    // store the Hists collection as member variables.
    std::unique_ptr<Hists>  h_SC_Ele,
                            h_SC_Mu,
                            h_SC_Evt,
                            h_SC_Jet,
                            h_SC_FwdJet;
    std::vector<std::unique_ptr<Hists> > vh_nocuts;
                                         // vh_nm1;
    
    std::vector<std::unique_ptr<AnalysisModule> > modules;
   
    // declare the Selections to use. Use unique_ptr to ensure automatic call of delete in the destructor,
    // to avoid memory leaks.
    // std::unique_ptr<Selection> njet_sel, bsel;
    // std::unique_ptr<AndSelection> final_selection;
};


VLQToHiggsPairProdAnalysis::VLQToHiggsPairProdAnalysis(Context & ctx){
    
    // If running in SFrame, the keys "dataset_version", "dataset_type" and "dataset_lumi"
    // are set to the according values in the xml file. For CMSSW, these are
    // not set automatically, but can be set in the python config file.
    for(auto kv : ctx.get_all()){
        cout << " " << kv.first << " = " << kv.second << endl;
    }
    
    // 1. setup other modules. Here, only the jet cleaner
    // nbtagprod.reset(new NBTagProducer(ctx));
    // fwdjetswitch.reset(new FwdJetSwitch(ctx));
    // jetcleaner.reset(new JetCleaner(30.0, 7.0));

    modules.emplace_back(new JetCleaner(30.0, 2.4));
    modules.emplace_back(new ElectronCleaner(
        AndId<Electron>(
            ElectronID_CSA14_50ns_medium,
            PtEtaCut(20.0, 2.4)
        )
    ));

    modules.emplace_back(new MuonCleaner(
        AndId<Muon>(
            MuonIDTight(),
            PtEtaCut(20.0, 2.1)
        )
    ));

    modules.emplace_back(new HTCalculator(ctx));

    
    // set up selections:
    // njet_sel.reset(new NJetSelection(2));
    // bsel.reset(new NBTagSelection(1));
    // use AndSelection to create cutflow of both selections.
    // NOTE: adding selections to AndSelection via add constructs them in-place;
    // the first argument to add is a description (to be used as name of the selection
    // in tables or histograms), followed by the constructor arguments of that Selection
    // class.
    // final_selection.reset(new AndSelection(ctx, "final"));
    // final_selection->add<NJetSelection>("n_jets >= 2", 2);
    // final_selection->add<NBTagSelection>("nb >= 1", 1);

    // 3. Set up Hists classes:
    // vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::Trigger (ctx, "SelNone")));
    // vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NJets   (ctx, "SelNone")));
    // vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NBTags  (ctx, "SelNone")));
    // vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NFwdJets(ctx, "SelNone")));
    // vh_nocuts.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NLeptons(ctx, "SelNone")));

    // // vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::Trigger (ctx, "SelNm1")));
    // vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NJets   (ctx, "SelNm1")));
    // vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NBTags  (ctx, "SelNm1")));
    // vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NFwdJets(ctx, "SelNm1")));
    // vh_nm1.push_back(std::unique_ptr<Hists>(new vlq2hl_hist::NLeptons(ctx, "SelNm1")));

    h_SC_Ele.reset(new ElectronHists(ctx, "SanityCheckEle", true));
    h_SC_Mu.reset(new MuonHists(ctx, "SanityCheckMu"));
    h_SC_Evt.reset(new EventHists(ctx, "SanityCheckEvent"));
    h_SC_Jet.reset(new JetHists(ctx, "SanityCheckJets"));
    h_SC_FwdJet.reset(new JetHists(ctx, "SanityCheckFwdJets", "fwd_jets"));

    // Set up Hists classes:
    // h_nocuts.reset(new GenHists(ctx, "NoCuts"));
    // h_njet.reset(new VLQToHiggsPairProdHists(ctx, "Njet"));
    // h_bsel.reset(new VLQToHiggsPairProdHists(ctx, "Bsel"));
}


bool VLQToHiggsPairProdAnalysis::process(Event & event) {
    // This is the main procedure, called for each event. Typically, do some pre-processing,
    // such as filtering objects (applying jet pt cuts, lepton selections, etc.),
    // then test which selection(s) the event passes and fill according histograms.
    
    cout << "VLQToHiggsPairProdAnalysis: Starting to process event (runid, eventid) = (" << event.run << ", " << event.event << ")" << endl;
    
    // run all modules (here: only jet cleaning).
    for(auto & m: modules){
        m->process(event);
    }
    

    // 2.b fill histograms
    h_SC_Ele->fill(event);
    h_SC_Mu->fill(event);
    h_SC_Evt->fill(event);
    h_SC_Jet->fill(event);
    h_SC_FwdJet->fill(event);

    // h_nocuts->fill(event);
//     
//     bool njet_selection = njet_sel->passes(event);
//     if(njet_selection){
//         h_njet->fill(event);
//     }
//     bool bjet_selection = bsel->passes(event);
//     if(bjet_selection){
//         h_bsel->fill(event);
//     }
    return false;
}

// as we want to run the ExampleCycleNew directly with AnalysisModuleRunner,
// make sure the VLQToHiggsPairProdAnalysis is found by class name. This is ensured by this macro:
UHH2_REGISTER_ANALYSIS_MODULE(VLQToHiggsPairProdAnalysis)
