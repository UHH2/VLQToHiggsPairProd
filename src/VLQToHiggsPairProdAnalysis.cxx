#include <iostream>
#include <memory>

#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Event.h"
#include "UHH2/common/include/CleaningModules.h"
#include "UHH2/common/include/CommonModules.h"
#include "UHH2/common/include/ElectronIds.h"
#include "UHH2/common/include/MuonIds.h"
#include "UHH2/common/include/EventHists.h"
#include "UHH2/common/include/EventVariables.h"
#include "UHH2/common/include/ElectronHists.h"
#include "UHH2/common/include/MuonHists.h"
#include "UHH2/common/include/JetHists.h"
#include "UHH2/common/include/JetIds.h"
#include "UHH2/common/include/NSelections.h"
#include "UHH2/VLQToHiggsPairProd/include/VLQToHiggsPairProdHists.h"
#include "UHH2/VLQToHiggsPairProd/include/VLQToHiggsPairProdSelections.h"
#include "UHH2/VLQToHiggsPairProd/include/GenHists.h"

using namespace std;
using namespace uhh2;

namespace vlqToHiggsPair {
    const size_t number_selections = 7;

    const char* selection_names[] = {
        "OneElectronCut",
        "OneMuonCut",
        "ElectronCut",
        "MuonCut",
        "BTagCut",
        "JetPtCut",
        "HTCut"
    };
}

using namespace vlqToHiggsPair;

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
    std::unique_ptr<Hists> 
            nocuts_hists,
            allsel_el_hists,
            allsel_mu_hists,
            allsel_oneel_hists,
            allsel_onemu_hists;
    std::map<const char*, std::unique_ptr<Hists> >
            onecut_hists,
            nm1_oneel_hists,
            nm1_onemu_hists,
            nm1_el_hists,
            nm1_mu_hists;

                           // vh_nm1;

    JetId btag;
    
    std::vector<std::unique_ptr<AnalysisModule> > modules;

    // std::unique_ptr<CommonModules> cm;

    // std::unique_ptr<Selection> ele_selection, mu_selection;
    std::map<const char*, std::unique_ptr<Selection> > all_selections;
   
    // internal function to fill all histograms
};


VLQToHiggsPairProdAnalysis::VLQToHiggsPairProdAnalysis(Context & ctx){
    
    // If running in SFrame, the keys "dataset_version", "dataset_type" and "dataset_lumi"
    // are set to the according values in the xml file. For CMSSW, these are
    // not set automatically, but can be set in the python config file.
    for(auto kv : ctx.get_all()){
        cout << " " << kv.first << " = " << kv.second << endl;
    }
    
    // 1. setup other modules. Here, only the jet cleaner

    // cm.reset(new CommonModules);

    // cm->set_jet_id(PtEtaCut(30.0, 2.4));
    // cm->set_electron_id(AndId<Electron>(ElectronID_PHYS14_25ns_medium, PtEtaCut(20.0, 2.4)));
    // cm->set_muon_id(AndId<Muon>(MuonIDTight(), PtEtaCut(20.0, 2.1)));
    // cm.set_tau_id(PtEtaCut(30.0, 2.4));

    
    // cm->init(ctx);
    
    // nbtagprod.reset(new NBTagProducer(ctx));
    // fwdjetswitch.reset(new FwdJetSwitch(ctx));
    // jetcleaner.reset(new JetCleaner(30.0, 7.0));

    modules.emplace_back(new JetCleaner(30.0, 2.4));
    modules.emplace_back(new ElectronCleaner(
        AndId<Electron>(
            ElectronID_PHYS14_25ns_medium,
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

    
    // 2. set up selections:
    btag = CSVBTag(CSVBTag::WP_MEDIUM);

    // ele_selection.reset(new NElectronSelection(1,1));
    // mu_selection.reset(new NMuonSelection(1,1));

    all_selections["OneElectronCut"] = std::unique_ptr<Selection>(new AndSelection(ctx, "ele"));
    all_selections["OneMuonCut"] = std::unique_ptr<Selection>(new AndSelection(ctx, "muon"));
    all_selections["ElectronCut"] = std::unique_ptr<Selection>(new NElectronSelection(1, -1));
    all_selections["MuonCut"] = std::unique_ptr<Selection>(new NMuonSelection(1, -1));
    all_selections["BTagCut"] = std::unique_ptr<Selection>(new NJetSelection(1, -1, btag));
    all_selections["JetPtCut"] = std::unique_ptr<Selection>(new JetPtSelection(200.));
    all_selections["HTCut"] = std::unique_ptr<Selection>(new HTSelection(ctx, 900.));

    ((AndSelection*)all_selections["OneElectronCut"].get())->add<NElectronSelection>("n_el = 1", 1, 1);
    ((AndSelection*)all_selections["OneElectronCut"].get())->add<NMuonSelection>("n_mu = 0", 0, 0);
    ((AndSelection*)all_selections["OneMuonCut"].get())->add<NMuonSelection>("n_mu = 1", 1, 1);
    ((AndSelection*)all_selections["OneMuonCut"].get())->add<NElectronSelection>("n_el = 1", 0, 0);


    // 3. Set up Hists classes:

    // no cuts histogram
    nocuts_hists.reset(new VLQToHiggsPairProdHists(ctx, "NoCuts"));

    // one-cut histograms
    onecut_hists["OneElectronCut"] = std::unique_ptr<Hists>(new VLQToHiggsPairProdHists(ctx, "OneElectronCut"));
    onecut_hists["OneMuonCut"] = std::unique_ptr<Hists>(new VLQToHiggsPairProdHists(ctx, "OneMuonCut"));
    onecut_hists["ElectronCut"] = std::unique_ptr<Hists>(new VLQToHiggsPairProdHists(ctx, "ElectronCut"));
    onecut_hists["MuonCut"] = std::unique_ptr<Hists>(new VLQToHiggsPairProdHists(ctx, "MuonCut"));
    onecut_hists["BTagCut"] = std::unique_ptr<Hists>(new VLQToHiggsPairProdHists(ctx, "BTagCut"));
    onecut_hists["JetPtCut"] = std::unique_ptr<Hists>(new VLQToHiggsPairProdHists(ctx, "JetPtCut"));
    onecut_hists["HTCut"] = std::unique_ptr<Hists>(new VLQToHiggsPairProdHists(ctx, "HTCut"));

    // Nminus1 histograms
    nm1_oneel_hists["OneElectronCut"] = std::unique_ptr<Hists>(new VLQToHiggsPairProdHists(ctx, "OneElNminusOneElectronCut"));
    nm1_oneel_hists["BTagCut"] = std::unique_ptr<Hists>(new VLQToHiggsPairProdHists(ctx, "OneElNminusBTagCut"));
    nm1_oneel_hists["JetPtCut"] = std::unique_ptr<Hists>(new VLQToHiggsPairProdHists(ctx, "OneElNminusJetPtCut"));
    nm1_oneel_hists["HTCut"] = std::unique_ptr<Hists>(new VLQToHiggsPairProdHists(ctx, "OneElNminusHTCut"));
    
    nm1_el_hists["ElectronCut"] = std::unique_ptr<Hists>(new VLQToHiggsPairProdHists(ctx, "ElNminusElectronCut"));
    nm1_el_hists["BTagCut"] = std::unique_ptr<Hists>(new VLQToHiggsPairProdHists(ctx, "ElNminusBTagCut"));
    nm1_el_hists["JetPtCut"] = std::unique_ptr<Hists>(new VLQToHiggsPairProdHists(ctx, "ElNminusJetPtCut"));
    nm1_el_hists["HTCut"] = std::unique_ptr<Hists>(new VLQToHiggsPairProdHists(ctx, "ElNminusHTCut"));
    
    nm1_onemu_hists["OneMuonCut"] = std::unique_ptr<Hists>(new VLQToHiggsPairProdHists(ctx, "OneMuNminusOneMuonCut"));
    nm1_onemu_hists["BTagCut"] = std::unique_ptr<Hists>(new VLQToHiggsPairProdHists(ctx, "OneMuNminusBTagCut"));
    nm1_onemu_hists["JetPtCut"] = std::unique_ptr<Hists>(new VLQToHiggsPairProdHists(ctx, "OneMuNminusJetPtCut"));
    nm1_onemu_hists["HTCut"] = std::unique_ptr<Hists>(new VLQToHiggsPairProdHists(ctx, "OneMuNminusHTCut"));

    nm1_mu_hists["MuonCut"] = std::unique_ptr<Hists>(new VLQToHiggsPairProdHists(ctx, "MuNminusMuonCut"));
    nm1_mu_hists["BTagCut"] = std::unique_ptr<Hists>(new VLQToHiggsPairProdHists(ctx, "MuNminusBTagCut"));
    nm1_mu_hists["JetPtCut"] = std::unique_ptr<Hists>(new VLQToHiggsPairProdHists(ctx, "MuNminusJetPtCut"));
    nm1_mu_hists["HTCut"] = std::unique_ptr<Hists>(new VLQToHiggsPairProdHists(ctx, "MuNminusHTCut"));

    // final selection (preliminary) histograms
    allsel_oneel_hists.reset(new VLQToHiggsPairProdHists(ctx, "OneElectronFinalSelection"));
    allsel_onemu_hists.reset(new VLQToHiggsPairProdHists(ctx, "OneMuonFinalSelection"));
    allsel_el_hists.reset(new VLQToHiggsPairProdHists(ctx, "ElectronFinalSelection"));
    allsel_mu_hists.reset(new VLQToHiggsPairProdHists(ctx, "MuonFinalSelection"));

    // Set up Hists classes:
    // nocuts_hists.reset(new GenHists(ctx, "NoCuts"));
    // h_njet.reset(new VLQToHiggsPairProdHists(ctx, "Njet"));
    // h_bsel.reset(new VLQToHiggsPairProdHists(ctx, "Bsel"));
}


bool VLQToHiggsPairProdAnalysis::process(Event & event) {
    // This is the main procedure, called for each event. Typically, do some pre-processing,
    // such as filtering objects (applying jet pt cuts, lepton selections, etc.),
    // then test which selection(s) the event passes and fill according histograms.
    
    cout << "VLQToHiggsPairProdAnalysis: Starting to process event (runid, eventid) = (" << event.run << ", " << event.event << ")" << endl;
    
    // run all modules (here: only jet cleaning).

    // cm->process(event);

    for(auto & m: modules){
        m->process(event);
    }
    

    // 2.b fill histograms
    nocuts_hists->fill(event);

    std::map<const char *, bool> 
            pass_oneel_selection,
            pass_onemu_selection,
            pass_el_selection,
            pass_mu_selection;

    // std::cout << "Passed selections:" << std::endl;
    for (size_t i = 0; i < number_selections; ++i)
    {
        try
        {
            const char * sel_name = selection_names[i];
            bool pass = all_selections.at(sel_name)->passes(event);

            if (string(sel_name) == "OneElectronCut")
                pass_oneel_selection[sel_name] = pass;
            else if (string(sel_name) == "OneMuonCut")
                pass_onemu_selection[sel_name] = pass;
            else if (string(sel_name) == "ElectronCut")
                pass_el_selection[sel_name] = pass;
            else if (string(sel_name) == "MuonCut")
                pass_mu_selection[sel_name] = pass;
            else
            {
                pass_oneel_selection[sel_name] = pass;
                pass_onemu_selection[sel_name] = pass;
                pass_el_selection[sel_name] = pass;
                pass_mu_selection[sel_name] = pass;
            }

            // std::cout << "  " << sel_name << " " << pass << std::endl;
        }
        catch (const std::out_of_range & e)
        {
            std::cerr << "WARNING: Selection name not defined!" << std::endl;
            throw e;
        }
    }

    // std::cout << std::endl;

    bool pass_all_oneel = true;

    // std::cout << "Fill Histograms:" << std::endl;

    for (std::map<const char *, bool>::const_iterator iSel = pass_oneel_selection.begin();
        iSel != pass_oneel_selection.end(); ++iSel)
    {
        const char * sel_name = iSel->first;
        bool pass_sel = iSel->second;

        // std::cout << "  " << sel_name << " " << pass_sel << std::endl;

        if (pass_sel)
        {
            onecut_hists[sel_name]->fill(event);
        }
        else pass_all_oneel = false;

        bool pass_nm1 = true;

        // std::cout << std::endl << "  Fill nm1 histograms:" << std::endl;

        for (size_t iName = 0; iName < number_selections; ++iName)
        {
            try
            {
                // std::cout << "    " << sel_name << " " << selection_names[iName] << " "
                    // << pass_oneel_selection.at(selection_names[iName]) << std::endl;
                if (string(sel_name) != selection_names[iName]
                    && !pass_oneel_selection.at(selection_names[iName]))
                    pass_nm1 = false;
            }
            catch (const std::out_of_range & e)
            {
                continue;
            }
        }

        // std::cout << "    Bool pass_nm1: " << pass_nm1 << std::endl << std::endl;

        if (pass_nm1)
            nm1_oneel_hists[sel_name]->fill(event);
    }

    // std::cout << "Bool pass_all_oneel: " << pass_all_oneel << std::endl << std::endl;

    if (pass_all_oneel)
        allsel_oneel_hists->fill(event);



    // nocuts_hists->fill(event);
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
