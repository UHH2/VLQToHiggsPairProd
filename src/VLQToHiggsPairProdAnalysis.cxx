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

    std::string version;

    Event::Handle<vector<TopJet> > h_hepTopTagJets_in;
    Event::Handle<vector<TopJet> > h_ca8prunedJets_in;
    Event::Handle<vector<TopJet> > h_hepTopTagJets_out;
    Event::Handle<vector<TopJet> > h_ca8prunedJets_out;

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

    // JetId btag;
    // TopJetId toptag;
    
    std::vector<std::unique_ptr<AnalysisModule> > modules;

    std::unique_ptr<CommonModules> cm;

    // std::unique_ptr<Selection> ele_selection, mu_selection;
    std::unique_ptr<AndSelection>
            // gen_el_finalselection;
            reco_mu_finalselection,
            gen_mu_finalselection;


    // handles
    Event::Handle<bool> pass_gensel_;
    Event::Handle<double> parton_ht;
   
    // internal function to fill all histograms
};


VLQToHiggsPairProdAnalysis::VLQToHiggsPairProdAnalysis(Context & ctx) {

    
    // If running in SFrame, the keys "dataset_version", "dataset_type" and "dataset_lumi"
    // are set to the according values in the xml file. For CMSSW, these are
    // not set automatically, but can be set in the python config file.
    for(auto kv : ctx.get_all()){
        cout << " " << kv.first << " = " << kv.second << endl;
    }

    h_hepTopTagJets_in = ctx.declare_event_input<std::vector<TopJet> >("patJetsHEPTopTagCHSPacked");
    h_ca8prunedJets_in = ctx.declare_event_input<std::vector<TopJet> >("patJetsCA8CHSprunedPacked");
    h_hepTopTagJets_out = ctx.declare_event_output<std::vector<TopJet> >("patJetsHEPTopTagCHSPacked");
    h_ca8prunedJets_out = ctx.declare_event_output<std::vector<TopJet> >("patJetsCA8CHSprunedPacked");


    version = ctx.get("dataset_version");


    // 1. define handles and other stuff here for later call in VLQToHiggsPairProdAnalysis::process

    CSVBTag::wp btag_wp = CSVBTag::WP_MEDIUM;

    // btag = CSVBTag(btag_wp);
    // toptag =CMSTopTag();

    pass_gensel_ = ctx.get_handle<bool>("pass_gensel");
    parton_ht = ctx.get_handle<double>("parton_ht");
    





    // 2. setup other modules. Here, only the jet cleaner

    cm.reset(new CommonModules);

    // cm->set_jet_id(PtEtaCut(30.0, 2.4));
    // cm->set_electron_id(AndId<Electron>(ElectronID_PHYS14_25ns_medium, PtEtaCut(20.0, 2.4)));
    // cm->set_muon_id(AndId<Muon>(MuonIDTight(), PtEtaCut(20.0, 2.1)));
    // cm.set_tau_id(PtEtaCut(30.0, 2.4));
    
    cm->init(ctx);

    // TODO: for BTag-, TopTag- and NGenParticleCalculator, use handle as input argument for the constructor instead
    // of a string and declare these handles as private members of the analysis module
    modules.emplace_back(new BTagCalculator(ctx, "n_btags", CSVBTag(btag_wp)));
    modules.emplace_back(new CMSTopTagCalculator(ctx, "n_toptags", CMSTopTag()));

    modules.emplace_back(new NGenParticleCalculator(ctx, "n_gen_bfromtop", ParticleId::BottomId, ParticleId::TopId));
    modules.emplace_back(new NGenParticleCalculator(ctx, "n_gen_higgs", ParticleId::HiggsId));
    modules.emplace_back(new NGenParticleCalculator(ctx, "n_gen_electron", ParticleId::ElectronId, ParticleId::TopId));
    modules.emplace_back(new NGenParticleCalculator(ctx, "n_gen_muon", ParticleId::MuonId, ParticleId::TopId));
    modules.emplace_back(new PartonHT(parton_ht));

    modules.emplace_back(new ElectronCleaner(AndId<Electron>(ElectronID_PHYS14_25ns_medium, PtEtaCut(20.0, 2.4))));
    modules.emplace_back(new MuonCleaner(AndId<Muon>(MuonIDTight(), PtEtaCut(20.0, 2.1))));
    modules.emplace_back(new JetLeptonCleaner(JERFiles::PHYS14_L123_MC));
    modules.emplace_back(new JetCleaner(PtEtaCut(30.0, 2.4)));
    modules.emplace_back(new JetPtSorter());




    // 3. set up no-cuts histograms
    nogensel_nocuts.reset(new HistCollector(ctx, "NoGenSel-NoCuts"));

    // 4. set up gen selection and the final reco selections

    gen_mu_finalselection.reset(new AndSelection(ctx, "final_gen_sel_cutflow"));
    gen_mu_finalselection->add<NGenParticleSelection>("n_gen_mu = 1", ctx.get_handle<int>("n_gen_muon"), 1, 1);
    gen_mu_finalselection->add<NGenParticleSelection>("n_gen_el = 0", ctx.get_handle<int>("n_gen_electron"), 0, 0);
    gen_mu_finalselection->add<NGenParticleSelection>("n_gen_b >= 1", ctx.get_handle<int>("n_gen_bfromtop"), 1);
    gen_mu_finalselection->add<NGenParticleSelection>("n_gen_higgs >= 1", ctx.get_handle<int>("n_gen_higgs"), 1);

    // DEFINE SELECTION HERE
    // reco_cuts["OneMuonCut"] = std::shared_ptr<Selection>(new AndSelection(ctx, "one_muon"));
    reco_cuts["MinOneMuon"] = std::shared_ptr<Selection>(new NMuonSelection(1, -1));
    reco_cuts["BTagCut"] = std::shared_ptr<Selection>(new NJetSelection(1, -1, JetId(CSVBTag(btag_wp))));
    reco_cuts["JetPtCut1"] = std::shared_ptr<Selection>(new JetPtSelection(200.));
    // reco_cuts["JetPtCut2"] = std::shared_ptr<Selection>(new JetPtSelection(50.));
    reco_cuts["HTCut"] = std::shared_ptr<Selection>(new HTSelection(ctx.get_handle<double>("HT"), 700.));

    // ((AndSelection*)reco_cuts["OneMuonCut"].get())->add<NMuonSelection>("n_mu = 1", 1, 1);
    // ((AndSelection*)reco_cuts["OneMuonCut"].get())->add<NElectronSelection>("n_el = 0", 0, 0);






    // 5. set up hists and selections with gen selection only
    gensel_nocuts.first.reset(new HistCollector(ctx, "GenSel-NoCuts"));
    // gensel_nocuts.second.reset(new GenHists(ctx, "GenSel-NoCuts-Gen"));

    gensel_nocuts.second.reset(new AndSelection(ctx, "gensel_nocuts"));
    gensel_nocuts.second->add<BoolSelection>("gen_finalstate_sel", pass_gensel_);



    nogensel_fin_onemu.first.reset(new HistCollector(ctx, "NoGenSel-AllCuts"));
    nogensel_fin_onemu.second.reset(new AndSelection(ctx, "nogensel_allcuts"));

    gensel_fin_onemu.first.reset(new HistCollector(ctx, "GenSel-AllCuts"));
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
        nogensel_onecut[sel_name] = std::make_pair(std::unique_ptr<Hists>(new HistCollector(ctx, "NoGenSel-OneCut-"+sel_str)),
                                                   std::unique_ptr<AndSelection>(new AndSelection(ctx, "nogensel_onecut_"+sel_str+"_cutflow")));
        nogensel_onecut[sel_name].second->add(sel_str, reco_cuts[sel_name]);

        gensel_onecut[sel_name] = std::make_pair(std::unique_ptr<Hists>(new HistCollector(ctx, "GenSel-OneCut-"+sel_str)),
                                                   std::unique_ptr<AndSelection>(new AndSelection(ctx, "gensel_onecut_"+sel_str+"_cutflow")));
        gensel_onecut[sel_name].second->add<BoolSelection>("gen_finalstate_sel", pass_gensel_);
        gensel_onecut[sel_name].second->add(sel_str, reco_cuts[sel_name]);

        // create n-minus-1 selections and histograms

        nogensel_nm1_onemu[sel_name] = std::make_pair(std::unique_ptr<Hists>(new HistCollector(ctx, "NoGenSel-Nminus1-"+sel_str)),
                                                   std::unique_ptr<AndSelection>(new AndSelection(ctx, "nogensel_nminus1_"+sel_str+"_cutflow")));
        gensel_nm1_onemu[sel_name] = std::make_pair(std::unique_ptr<Hists>(new HistCollector(ctx, "GenSel-Nminus1-"+sel_str)),
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

    const std::vector<TopJet> & hepTopTagJets = event.get(h_hepTopTagJets_in);
    const std::vector<TopJet> & ca8prunedJets = event.get(h_ca8prunedJets_in);

    event.set(h_hepTopTagJets_out, std::move(hepTopTagJets));
    event.set(h_ca8prunedJets_out, std::move(ca8prunedJets));

    // use the following lines if you want to run over the inclusive Z/W+Jets samples but want to combine this with the ht-binned samples
    // float part_ht = event.get(parton_ht);

    // if ((version == "ZJets" || version == "WJets") && part_ht > 100.)
    //     return false;


    

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
    
    return passes_preselection;
}

// as we want to run the ExampleCycleNew directly with AnalysisModuleRunner,
// make sure the VLQToHiggsPairProdAnalysis is found by class name. This is ensured by this macro:
UHH2_REGISTER_ANALYSIS_MODULE(VLQToHiggsPairProdAnalysis)
