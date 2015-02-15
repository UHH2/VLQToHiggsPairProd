#include <iostream>
#include <memory>

#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Event.h"
#include "UHH2/common/include/CleaningModules.h"
#include "UHH2/common/include/CommonModules.h"
#include "UHH2/common/include/ElectronIds.h"
#include "UHH2/common/include/MuonIds.h"
// #include "UHH2/common/include/EventHists.h"
#include "UHH2/common/include/EventVariables.h"
// #include "UHH2/common/include/ElectronHists.h"
// #include "UHH2/common/include/MuonHists.h"
// #include "UHH2/common/include/JetHists.h"
#include "UHH2/common/include/JetIds.h"
#include "UHH2/common/include/TopJetIds.h"
#include "UHH2/common/include/NSelections.h"
#include "UHH2/common/include/GenTools.h"

#include "UHH2/VLQToHiggsPairProd/include/VLQToHiggsPairProdHists.h"
#include "UHH2/VLQToHiggsPairProd/include/VLQToHiggsPairProdSelections.h"
#include "UHH2/VLQToHiggsPairProd/include/GenHists.h"
#include "UHH2/VLQToHiggsPairProd/include/AdditionalModules.h"


using namespace std;
using namespace uhh2;

using namespace vlqToHiggsPair;

/** \brief Basic analysis example of an AnalysisModule (formerly 'cycle') in UHH2
 * 
 * This is the central class which calls other AnalysisModules, Hists or Selection classes.
 * This AnalysisModule, in turn, is called (via AnalysisModuleRunner) by SFrame.
 */

class VLQToHiggsPairProdAnalysis: public AnalysisModule {
public:

    enum ParticleId {
        BottomId = 5,
        TopId = 6,
        TprimeId = 8,
        ElectronId = 11,
        MuonId = 13,
        HiggsId = 25
    };
    
    explicit VLQToHiggsPairProdAnalysis(Context & ctx);
    virtual bool process(Event & event);

private:

    // // declare the Selections to use.
    // std::vector<std::unique_ptr<Selection> > v_sel;

    std::map<const char *, std::shared_ptr<Selection> > reco_cuts;

    // no gen selection, no reco selection, both gen and reco plots
    std::unique_ptr<Hists>
            nogensel_nocuts
            ;

    // gen selection, no reco selection, both gen and reco plots
    std::pair< std::unique_ptr<Hists>, std::unique_ptr<AndSelection> >
            gensel_nocuts;

    // with/without gen selection, final reco selection, only reco plots
    std::pair<std::unique_ptr<Hists> , std::unique_ptr<AndSelection> >
            // allsel_el_hists,
            // allsel_mu_hists,
            // allsel_oneel_hists,
            nogensel_fin_onemu,
            // allsel_oneel_gensel_hists,
            gensel_fin_onemu
            ;

    // with/without gen selection, one-cut and n-minus-1 reco selections, only reco plots
    std::map<const char*, std::pair< std::unique_ptr<Hists>, std::unique_ptr<AndSelection> > >
            nogensel_onecut,
            gensel_onecut,
            // nm1_el_hists,
            // nm1_mu_hists,
            // nm1_oneel_hists,
            nogensel_nm1_onemu,
            // nm1_oneel_gensel_hists,
            gensel_nm1_onemu
            ;

                           // vh_nm1;

    JetId btag;
    TopJetId toptag;
    
    std::vector<std::unique_ptr<AnalysisModule> > modules;

    std::unique_ptr<CommonModules> cm;

    // std::unique_ptr<Selection> ele_selection, mu_selection;
    std::unique_ptr<AndSelection>
            // gen_el_finalselection;
            reco_mu_finalselection,
            gen_mu_finalselection;

    Event::Handle<bool> pass_gensel_;
    // std::map<const char*, std::unique_ptr<Selection> > all_selections;
   
    // internal function to fill all histograms
};


VLQToHiggsPairProdAnalysis::VLQToHiggsPairProdAnalysis(Context & ctx) {

    CSVBTag::wp btag_wp = CSVBTag::WP_MEDIUM;

    btag = CSVBTag(btag_wp);
    toptag =CMSTopTag();

    
    // If running in SFrame, the keys "dataset_version", "dataset_type" and "dataset_lumi"
    // are set to the according values in the xml file. For CMSSW, these are
    // not set automatically, but can be set in the python config file.
    for(auto kv : ctx.get_all()){
        cout << " " << kv.first << " = " << kv.second << endl;
    }
    
    // 1. setup other modules. Here, only the jet cleaner

    cm.reset(new CommonModules);

    cm->set_jet_id(PtEtaCut(30.0, 2.4));
    cm->set_electron_id(AndId<Electron>(ElectronID_PHYS14_25ns_medium, PtEtaCut(20.0, 2.4)));
    cm->set_muon_id(AndId<Muon>(MuonIDTight(), PtEtaCut(20.0, 2.1)));
    // cm.set_tau_id(PtEtaCut(30.0, 2.4));

    
    cm->init(ctx);

    modules.emplace_back(new BTagCalculator(ctx, "n_btags", CSVBTag(btag_wp)));
    modules.emplace_back(new CMSTopTagCalculator(ctx, "n_toptags", CMSTopTag()));

    modules.emplace_back(new NGenParticleCalculator(ctx, "n_gen_bfromtop", ParticleId::BottomId, ParticleId::TopId));
    modules.emplace_back(new NGenParticleCalculator(ctx, "n_gen_higgs", ParticleId::HiggsId));
    modules.emplace_back(new NGenParticleCalculator(ctx, "n_gen_electron", ParticleId::ElectronId, ParticleId::TopId));
    modules.emplace_back(new NGenParticleCalculator(ctx, "n_gen_muon", ParticleId::MuonId, ParticleId::TopId));



    // std::pair<std::unique_ptr<Hists> , std::unique_ptr<AndSelection> >
    //         gensel_hists, gensel_gen_hists,
    //         // allsel_el_hists,
    //         // allsel_mu_hists,
    //         // allsel_oneel_hists,
    //         allsel_onemu_hists,
    //         // allsel_oneel_gensel_hists,
    //         allsel_onemu_gensel_hists
    //         ;
    // std::map<const char*, std::pair<std::unique_ptr<Hists>, std::unique_ptr<AndSelection> >
    //         onecut_hists,
    //         onecut_gensel_hists,
    //         // nm1_el_hists,
    //         // nm1_mu_hists,
    //         // nm1_oneel_hists,
    //         nm1_onemu_hists,
    //         // nm1_oneel_gensel_hists,
    //         nm1_onemu_gensel_hists
    //         ;


    // 2. set up no-cuts histograms
    nogensel_nocuts.reset(new HistCollector(ctx, "NoGenSel-NoCuts-Reco"));
    // nogensel_nocuts.second.reset(new GenHists(ctx, "NoGenSel-NoCuts-Gen"));

    // 3. set up gen selection and the final reco selections

    gen_mu_finalselection.reset(new AndSelection(ctx, "final_gen_sel_cutflow"));
    gen_mu_finalselection->add<NGenParticleSelection>("n_gen_mu = 1", ctx.get_handle<int>("n_gen_muon"), 1, 1);
    gen_mu_finalselection->add<NGenParticleSelection>("n_gen_el = 0", ctx.get_handle<int>("n_gen_electron"), 0, 0);
    gen_mu_finalselection->add<NGenParticleSelection>("n_gen_b >= 1", ctx.get_handle<int>("n_gen_bfromtop"), 1);
    gen_mu_finalselection->add<NGenParticleSelection>("n_gen_higgs >= 1", ctx.get_handle<int>("n_gen_higgs"), 1);

    // DEFINE SELECTION HERE
    // reco_cuts["OneMuonCut"] = std::shared_ptr<Selection>(new AndSelection(ctx, "one_muon"));
    reco_cuts["MinOneMuon"] = std::shared_ptr<Selection>(new NMuonSelection(1, -1));
    reco_cuts["BTagCut"] = std::shared_ptr<Selection>(new NJetSelection(1, -1, btag));
    reco_cuts["JetPtCut1"] = std::shared_ptr<Selection>(new JetPtSelection(200.));
    // reco_cuts["JetPtCut2"] = std::shared_ptr<Selection>(new JetPtSelection(50.));
    reco_cuts["HTCut"] = std::shared_ptr<Selection>(new HTSelection(ctx.get_handle<double>("HT"), 700.));

    // ((AndSelection*)reco_cuts["OneMuonCut"].get())->add<NMuonSelection>("n_mu = 1", 1, 1);
    // ((AndSelection*)reco_cuts["OneMuonCut"].get())->add<NElectronSelection>("n_el = 0", 0, 0);

    // set handle here for later call in VLQToHiggsPairProdAnalysis::process
    pass_gensel_ = ctx.get_handle<bool>("pass_gensel");

    // 4. set up hists and selections with gen selection only
    gensel_nocuts.first.reset(new HistCollector(ctx, "GenSel-NoCuts-Reco"));
    // gensel_nocuts.second.reset(new GenHists(ctx, "GenSel-NoCuts-Gen"));

    gensel_nocuts.second.reset(new AndSelection(ctx, "gensel_nocuts"));
    gensel_nocuts.second->add<BoolSelection>("gen_finalstate_sel", pass_gensel_);



    nogensel_fin_onemu.first.reset(new HistCollector(ctx, "NoGenSel-AllCuts-Reco"));
    nogensel_fin_onemu.second.reset(new AndSelection(ctx, "nogensel_allcuts"));

    gensel_fin_onemu.first.reset(new HistCollector(ctx, "GenSel-AllCuts-Reco"));
    gensel_fin_onemu.second.reset(new AndSelection(ctx, "gensel_allcuts"));
    gensel_fin_onemu.second->add<BoolSelection>("gen_finalstate_sel", pass_gensel_);

    for (auto const & selection : reco_cuts)
    {
        const char * sel_name = selection.first;
        std::string sel_str = selection.first;

        // append AndSelections for AllCuts selections
        nogensel_fin_onemu.second->add(sel_str, reco_cuts[sel_name]);
        gensel_fin_onemu.second->add(sel_str, reco_cuts[sel_name]);

        // create histograms and selections for the onecut-only case
        nogensel_onecut[sel_name] = std::make_pair(std::unique_ptr<Hists>(new HistCollector(ctx, "NoGenSel-OneCut-"+sel_str+"-Reco")),
                                                   std::unique_ptr<AndSelection>(new AndSelection(ctx, "nogensel_onecut_"+sel_str+"_cutflow")));
        nogensel_onecut[sel_name].second->add(sel_str, reco_cuts[sel_name]);

        gensel_onecut[sel_name] = std::make_pair(std::unique_ptr<Hists>(new HistCollector(ctx, "GenSel-OneCut-"+sel_str+"-Reco")),
                                                   std::unique_ptr<AndSelection>(new AndSelection(ctx, "gensel_onecut_"+sel_str+"_cutflow")));
        gensel_onecut[sel_name].second->add<BoolSelection>("gen_finalstate_sel", pass_gensel_);
        gensel_onecut[sel_name].second->add(sel_str, reco_cuts[sel_name]);

        // create n-minus-1 selections and histograms

        nogensel_nm1_onemu[sel_name] = std::make_pair(std::unique_ptr<Hists>(new HistCollector(ctx, "NoGenSel-Nminus1-"+sel_str+"-Reco")),
                                                   std::unique_ptr<AndSelection>(new AndSelection(ctx, "nogensel_nminus1_"+sel_str+"_cutflow")));
        gensel_nm1_onemu[sel_name] = std::make_pair(std::unique_ptr<Hists>(new HistCollector(ctx, "GenSel-Nminus1-"+sel_str+"-Reco")),
                                                   std::unique_ptr<AndSelection>(new AndSelection(ctx, "gensel_nminus1_"+sel_str+"_cutflow")));
        gensel_nm1_onemu[sel_name].second->add<BoolSelection>("gen_finalstate_sel", pass_gensel_);


        for (auto const selection2 : reco_cuts)
        {
            const char * sel_name2 = selection2.first;
            std::string sel_str2 = selection2.first;

            if (sel_str2 != sel_str)
            {
                nogensel_nm1_onemu[sel_name].second->add(sel_str2, reco_cuts[sel_name2]);
                gensel_nm1_onemu[sel_name].second->add(sel_str2, reco_cuts[sel_name2]);
            }
        }


    }


    // // 4. set up final selection with hists (with and without gen selection)
    // allsel_onemu_hists.first.reset(new VLQToHiggsPairProdHists(ctx, "OneMuon-FinalSelection"));
    // allsel_onemu_gensel_hists.first.reset(new VLQToHiggsPairProdHists(ctx, "GenSel-OneMuon-FinalSelection"));

    // allsel_onemu_hists.second.reset(new AndSelection(ctx, ));
    // allsel_onemu_gensel_hists.second.reset(new AndSelection(ctx, ));



    // reco_mu_finalselection.reset(new AndSelection(ctx, "reco_mu_final"));
    // reco_mu_finalselection->add<NMuonSelection>("n_mu = 1", 1, 1);
    // reco_mu_finalselection->add<NElectronSelection>("n_el = 0", 0, 0);
    // reco_mu_finalselection->add<NJetSelection>("n_btag >= 1", 1, -1, btag);
    // reco_mu_finalselection->add<JetPtSelection>("ld_jet_pt >= 200", 200.);
    // reco_mu_finalselection->add<HTSelection>("ht >= 900", ctx, 900.);
    
    // 2. set up selections:

    // ele_selection.reset(new NElectronSelection(1,1));
    // mu_selection.reset(new NMuonSelection(1,1));

    // gen_el_finalselection.reset(new AndSelection(ctx, "gen_el_final"));

    // gen_el_finalselection->add<NGenParticleSelection>("n_gen_el = 1", ctx.get_handle<int>("n_gen_electron"), 1, 1);
    // gen_el_finalselection->add<NGenParticleSelection>("n_gen_mu = 0", ctx.get_handle<int>("n_gen_muon"), 0, 0);
    // gen_el_finalselection->add<NGenParticleSelection>("n_gen_b >= 1", ctx.get_handle<int>("n_gen_bfromtop"), 1);
    // gen_el_finalselection->add<NGenParticleSelection>("n_gen_higgs >= 1", ctx.get_handle<int>("n_gen_higgs"), 1);

    


    // all_selections["OneElectronCut"] = std::unique_ptr<Selection>(new AndSelection(ctx, "ele"));
    // all_selections["OneMuonCut"] = std::unique_ptr<Selection>(new AndSelection(ctx, "muon"));
    // // all_selections["ElectronCut"] = std::unique_ptr<Selection>(new NElectronSelection(1, -1));
    // // all_selections["MuonCut"] = std::unique_ptr<Selection>(new NMuonSelection(1, -1));
    // all_selections["BTagCut"] = std::unique_ptr<Selection>(new NJetSelection(1, -1, btag));
    // all_selections["JetPtCut"] = std::unique_ptr<Selection>(new JetPtSelection(200.));
    // all_selections["HTCut"] = std::unique_ptr<Selection>(new HTSelection(ctx, 900.));

    // // ((AndSelection*)all_selections["OneElectronCut"].get())->add<NElectronSelection>("n_el = 1", 1, 1);
    // // ((AndSelection*)all_selections["OneElectronCut"].get())->add<NMuonSelection>("n_mu = 0", 0, 0);
    // ((AndSelection*)all_selections["OneMuonCut"].get())->add<NMuonSelection>("n_mu = 1", 1, 1);
    // ((AndSelection*)all_selections["OneMuonCut"].get())->add<NElectronSelection>("n_el = 1", 0, 0);


    // 3. Set up Hists classes:




    // one-cut histograms
    // for (auto & iSelName : all_selections)
    // {
    //     std::string sel_str =  string(iSelName.first);
    //     onecut_hists[iSelName.first] = std::unique_ptr<Hists>(new VLQToHiggsPairProdHists(ctx, sel_str));

    //     sel_str =  "GenSel-"+string(iSelName.first);
    //     onecut_gensel_hists[iSelName.first] = std::unique_ptr<Hists>(new VLQToHiggsPairProdHists(ctx, sel_str));

    //     sel_str =  "OneMuNminus1-"+string(iSelName.first);
    //     nm1_onemu_hists[iSelName.first] = std::unique_ptr<Hists>(new VLQToHiggsPairProdHists(ctx, sel_str));

    //     sel_str =  "GenSel-OneMuNminus1-"+string(iSelName.first);
    //     nm1_onemu_gensel_hists[iSelName.first] = std::unique_ptr<Hists>(new VLQToHiggsPairProdHists(ctx, sel_str));
    // }

    // // final selection (preliminary) histograms
    // allsel_onemu_hists.reset(new VLQToHiggsPairProdHists(ctx, "OneMuon-FinalSelection"));

    // allsel_onemu_gensel_hists.reset(new VLQToHiggsPairProdHists(ctx, "GenSel-OneMuon-FinalSelection"));

}


bool VLQToHiggsPairProdAnalysis::process(Event & event) {
    // This is the main procedure, called for each event. Typically, do some pre-processing,
    // such as filtering objects (applying jet pt cuts, lepton selections, etc.),
    // then test which selection(s) the event passes and fill according histograms.
    
    cout << "VLQToHiggsPairProdAnalysis: Starting to process event (runid, eventid) = (" << event.run << ", " << event.event << ")" << endl;
    
    // run all modules (here: only jet cleaning).

    cm->process(event);

    for(auto & m: modules){
        m->process(event);
    }
    

    // 2.b fill histograms
    nogensel_nocuts->fill(event);
    // nogensel_nocuts.second->fill(event);

    bool passes_any_gensel = (
        // gen_el_finalselection->passes(event) ||
        gen_mu_finalselection->passes(event)
        );

    bool passes_preselection = false;

    event.set(pass_gensel_, passes_any_gensel);

    if (gensel_nocuts.second->passes(event))
    {
        gensel_nocuts.first->fill(event);
        // gensel_nocuts.first.second->fill(event);
    }

    if (nogensel_fin_onemu.second->passes(event))
    {
        passes_preselection = true;
        nogensel_fin_onemu.first->fill(event);
    }

    if (gensel_fin_onemu.second->passes(event))
        gensel_fin_onemu.first->fill(event);

    for (auto const & selection : reco_cuts)
    {
        const char * sel_name = selection.first;
        if (nogensel_onecut[sel_name].second->passes(event))
            nogensel_onecut[sel_name].first->fill(event);

        if (gensel_onecut[sel_name].second->passes(event))
            gensel_onecut[sel_name].first->fill(event);

        if (nogensel_nm1_onemu[sel_name].second->passes(event))
            nogensel_nm1_onemu[sel_name].first->fill(event);

        if (gensel_nm1_onemu[sel_name].second->passes(event))
            gensel_nm1_onemu[sel_name].first->fill(event);
    }
    // if (passes_any_gensel)
    // {
    //     gensel_hists->fill(event);
    //     gensel_gen_hists->fill(event);
    // }

    // std::map<const char *, bool> 
    //         // pass_oneel_selection,
    //         pass_onemu_selection
    //         // pass_el_selection,
    //         // pass_mu_selection
    //         ;

    // // std::cout << "Passed selections:" << std::endl;
    // for (size_t i = 0; i < number_selections; ++i)
    // {
    //     try
    //     {
    //         const char * sel_name = selection_names[i];
    //         bool pass = all_selections.at(sel_name)->passes(event);

    //         // std::cout << "Selection: " << sel_name << " ";

    //         try
    //         {
    //             if (pass)
    //             {
    //                 onecut_hists.at(sel_name)->fill(event);
    //                 // if (string(sel_name) == "OneElectronCut" && gen_el_finalselection->passes(event))
    //                 //     onecut_gensel_hists.at(sel_name)->fill(event);
    //                 if (string(sel_name) == "OneMuonCut" && gen_mu_finalselection->passes(event))
    //                     onecut_gensel_hists.at(sel_name)->fill(event);
    //                 else if (passes_any_gensel)
    //                     onecut_gensel_hists.at(sel_name)->fill(event);
    //             }
    //         }
    //         catch (const std::out_of_range & e)
    //         {
    //             // std::cout << "NOT a valid selection: " << std::endl;
    //             continue;
    //         }

    //         // if (string(sel_name) == "OneElectronCut")
    //         // {
    //         //     // std::cout << "passed" << std::endl;
    //         //     pass_oneel_selection[sel_name] = pass;
    //         // }
    //         if (string(sel_name) == "OneMuonCut")
    //         {
    //             // std::cout << "passed" << std::endl;
    //             pass_onemu_selection[sel_name] = pass;
    //         }
    //         // else if (string(sel_name) == "ElectronCut")
    //         //     pass_el_selection[sel_name] = pass;
    //         // else if (string(sel_name) == "MuonCut")
    //         //     pass_mu_selection[sel_name] = pass;
    //         else
    //         {
    //             // std::cout << "passed" << std::endl;
    //             // pass_oneel_selection[sel_name] = pass;
    //             pass_onemu_selection[sel_name] = pass;
    //             // pass_el_selection[sel_name] = pass;
    //             // pass_mu_selection[sel_name] = pass;
    //         }

    //         // std::cout << "  " << sel_name << " " << pass << std::endl;
    //     }
    //     catch (const std::out_of_range & e)
    //     {
    //         // std::cerr << "WARNING: Selection name not defined!" << std::endl;
    //         continue;
    //     }
    // }

    // // std::cout << std::endl;

    // // fill_hists(event, pass_oneel_selection, nm1_oneel_hists, allsel_oneel_hists);
    // fill_hists(event, pass_onemu_selection, nm1_onemu_hists, allsel_onemu_hists);

    // // if (gen_el_finalselection->passes(event))
    // //     fill_hists(event, pass_oneel_selection, nm1_oneel_gensel_hists, allsel_oneel_gensel_hists);
    // if (gen_mu_finalselection->passes(event))
    //     fill_hists(event, pass_onemu_selection, nm1_onemu_gensel_hists, allsel_onemu_gensel_hists);
    // fill_hists(event, pass_el_selection, nm1_el_hists, allsel_el_hists);
    // fill_hists(event, pass_mu_selection, nm1_mu_hists, allsel_mu_hists);




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
    return passes_preselection;
}

// as we want to run the ExampleCycleNew directly with AnalysisModuleRunner,
// make sure the VLQToHiggsPairProdAnalysis is found by class name. This is ensured by this macro:
UHH2_REGISTER_ANALYSIS_MODULE(VLQToHiggsPairProdAnalysis)
