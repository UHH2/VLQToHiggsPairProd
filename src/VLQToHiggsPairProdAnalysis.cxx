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

    // // declare the Selections to use.
    // std::vector<std::unique_ptr<Selection> > v_sel;

    std::map<const char *, std::shared_ptr<Selection> > reco_cuts;

    // no gen selection, no reco selection, both gen and reco plots
    std::unique_ptr<Hists>
            nogensel_nocuts,
            nogensel_noclean,
            h_muonid_iso
            ;

    // gen selection, no reco selection, both gen and reco plots
    // std::pair< std::unique_ptr<Hists>, std::unique_ptr<AndSelection> >
    //         gensel_nocuts;

    // with/without gen selection, final reco selection, only reco plots
    std::pair<std::unique_ptr<Hists> , std::unique_ptr<AndSelection> >
            nogensel_fin_onemu
            // gensel_fin_onemu
            ;

    // with/without gen selection, one-cut and n-minus-1 reco selections, only reco plots
    std::map<const char*, std::pair< std::unique_ptr<Hists>, std::unique_ptr<AndSelection> > >
            nogensel_onecut,
            // gensel_onecut,
            nogensel_nm1_onemu
            // gensel_nm1_onemu
            ;
    
    std::vector<std::unique_ptr<AnalysisModule> > pre_modules, post_modules, muonid_iso;

    // std::unique_ptr<Selection> ele_selection, mu_selection;
    std::unique_ptr<AndSelection>
            // gen_el_finalselection;
            reco_mu_finalselection
            // ,gen_mu_finalselection
            ;


    // handles
    // Event::Handle<bool> pass_gensel_;
    Event::Handle<double> parton_ht;
   
    // internal function to fill all histograms
};


VLQToHiggsPairProdAnalysis::VLQToHiggsPairProdAnalysis(Context & ctx) {

    
    // If running in SFrame, the keys "dataset_version", "dataset_type" and "dataset_lumi"
    // are set to the according values in the xml file. For CMSSW, these are
    // not set automatically, but can be set in the python config file.
    // for(auto kv : ctx.get_all()){
    //     cout << " " << kv.first << " = " << kv.second << endl;
    // }

    
    // 1. define handles and other stuff here for later call in VLQToHiggsPairProdAnalysis::process

    version = ctx.get("dataset_version");

    CSVBTag::wp btag_wp = CSVBTag::WP_MEDIUM;

    // btag = CSVBTag(btag_wp);
    // toptag =CMSTopTag();

    // pass_gensel_ = ctx.get_handle<bool>("pass_gensel");
    parton_ht = ctx.get_handle<double>("parton_ht");
    





    // 2. setup other modules

    // calculate gen variables
    pre_modules.emplace_back(new NGenParticleCalculator(ctx, "n_gen_bfromtop", ParticleId::BottomId, ParticleId::TopId));
    pre_modules.emplace_back(new NGenParticleCalculator(ctx, "n_gen_higgs", ParticleId::HiggsId));
    pre_modules.emplace_back(new NGenParticleCalculator(ctx, "n_gen_electron", ParticleId::ElectronId, ParticleId::TopId));
    pre_modules.emplace_back(new NGenParticleCalculator(ctx, "n_gen_muon", ParticleId::MuonId, ParticleId::TopId));
    pre_modules.emplace_back(new PartonHT(parton_ht));

    pre_modules.emplace_back(new HTCalculator(ctx));
    pre_modules.emplace_back(new PrimaryLepton(ctx));
    // pre_modules.emplace_back(new HTLepCalculator(ctx));
    pre_modules.emplace_back(new BTagCalculator(ctx, "n_btags", CSVBTag(btag_wp)));
    pre_modules.emplace_back(new CMSTopTagCalculator(ctx, "n_toptags", CMSTopTag()));

    // all the reweighting and jet correction modules
    bool mclumiweight = true;
    bool mcpileupreweight = true;
    bool jec = true;
    bool jersmear = true;

    bool is_mc = ctx.get("dataset_type") == "MC";
    if(is_mc){
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
    post_modules.emplace_back(new BTagCalculator(ctx, "n_btags", CSVBTag(btag_wp)));
    post_modules.emplace_back(new CMSTopTagCalculator(ctx, "n_toptags", CMSTopTag()));

    muonid_iso.emplace_back(new MuonCleaner(AndId<Muon>(MuonIDTight(), MuonIso(), PtEtaCut(20.0, 2.1))));



    // 3. set up no-cuts histograms
    nogensel_nocuts.reset(new HistCollector(ctx, "NoGenSel-NoCuts"));
    nogensel_noclean.reset(new HistCollector(ctx, "NoGenSel-NoCleaning"));
    h_muonid_iso.reset(new ExtendedMuonHists(ctx, "NoGenSel-NoCuts/MuonIsoHists"));

    // 4. set up gen selection and the final reco selections

    // GENSELECTION
    // gen_mu_finalselection.reset(new AndSelection(ctx, "final_gen_sel_cutflow"));
    // gen_mu_finalselection->add<NGenParticleSelection>("n_gen_mu = 1", ctx.get_handle<int>("n_gen_muon"), 1, 1);
    // gen_mu_finalselection->add<NGenParticleSelection>("n_gen_el = 0", ctx.get_handle<int>("n_gen_electron"), 0, 0);
    // gen_mu_finalselection->add<NGenParticleSelection>("n_gen_b >= 1", ctx.get_handle<int>("n_gen_bfromtop"), 1);
    // gen_mu_finalselection->add<NGenParticleSelection>("n_gen_higgs >= 1", ctx.get_handle<int>("n_gen_higgs"), 1);



    // DEFINE RECO SELECTIONS HERE
    // reco_cuts["OneMuonCut"] = std::shared_ptr<Selection>(new AndSelection(ctx, "one_muon"));
    reco_cuts["MinOneMuon"] = std::shared_ptr<Selection>(new NMuonSelection(1, -1));
    reco_cuts["MuonPtCut"] = std::shared_ptr<Selection>(new MuonPtSelection(50.));
    reco_cuts["HTCut"] = std::shared_ptr<Selection>(new HTSelection(ctx.get_handle<double>("HT"), 700.));
    // REMOVE BTAG CUT FROM PRESELECTION
    // reco_cuts["BTagCut"] = std::shared_ptr<Selection>(new NJetSelection(1, -1, JetId(CSVBTag(btag_wp))));
    reco_cuts["JetPtCut"] = std::shared_ptr<Selection>(new JetPtSelection(200.));
    // reco_cuts["JetPtCut2"] = std::shared_ptr<Selection>(new JetPtSelection(50.));

    // ((AndSelection*)reco_cuts["OneMuonCut"].get())->add<NMuonSelection>("n_mu = 1", 1, 1);
    // ((AndSelection*)reco_cuts["OneMuonCut"].get())->add<NElectronSelection>("n_el = 0", 0, 0);






    // // 5. set up hists and selections with gen selection only
    // gensel_nocuts.first.reset(new HistCollector(ctx, "GenSel-NoCuts"));
    // // gensel_nocuts.second.reset(new GenHists(ctx, "GenSel-NoCuts-Gen"));

    // gensel_nocuts.second.reset(new AndSelection(ctx, "gensel_nocuts"));
    // gensel_nocuts.second->add<BoolSelection>("gen_finalstate_sel", pass_gensel_);



    nogensel_fin_onemu.first.reset(new HistCollector(ctx, "NoGenSel-AllCuts"));
    nogensel_fin_onemu.second.reset(new AndSelection(ctx, "nogensel_allcuts"));

    // gensel_fin_onemu.first.reset(new HistCollector(ctx, "GenSel-AllCuts"));
    // gensel_fin_onemu.second.reset(new AndSelection(ctx, "gensel_allcuts"));
    // gensel_fin_onemu.second->add<BoolSelection>("gen_finalstate_sel", pass_gensel_);

    for (auto const & selection : reco_cuts)
    {
        const char * sel_name = selection.first;
        std::string sel_str = selection.first;

        // append AndSelections for AllCuts selections
        nogensel_fin_onemu.second->add(sel_str, reco_cuts[sel_name]);
        // gensel_fin_onemu.second->add(sel_str, reco_cuts[sel_name]);

        // create histograms and selections for the onecut-only case
        nogensel_onecut[sel_name] = std::make_pair(std::unique_ptr<Hists>(new HistCollector(ctx, "NoGenSel-OneCut-"+sel_str)),
                                                   std::unique_ptr<AndSelection>(new AndSelection(ctx, "nogensel_onecut_"+sel_str+"_cutflow")));
        nogensel_onecut[sel_name].second->add(sel_str, reco_cuts[sel_name]);

        // gensel_onecut[sel_name] = std::make_pair(std::unique_ptr<Hists>(new HistCollector(ctx, "GenSel-OneCut-"+sel_str)),
        //                                            std::unique_ptr<AndSelection>(new AndSelection(ctx, "gensel_onecut_"+sel_str+"_cutflow")));
        // gensel_onecut[sel_name].second->add<BoolSelection>("gen_finalstate_sel", pass_gensel_);
        // gensel_onecut[sel_name].second->add(sel_str, reco_cuts[sel_name]);

        // create n-minus-1 selections and histograms

        nogensel_nm1_onemu[sel_name] = std::make_pair(std::unique_ptr<Hists>(new HistCollector(ctx, "NoGenSel-Nminus1-"+sel_str)),
                                                   std::unique_ptr<AndSelection>(new AndSelection(ctx, "nogensel_nminus1_"+sel_str+"_cutflow")));
        // gensel_nm1_onemu[sel_name] = std::make_pair(std::unique_ptr<Hists>(new HistCollector(ctx, "GenSel-Nminus1-"+sel_str)),
        //                                            std::unique_ptr<AndSelection>(new AndSelection(ctx, "gensel_nminus1_"+sel_str+"_cutflow")));
        // gensel_nm1_onemu[sel_name].second->add<BoolSelection>("gen_finalstate_sel", pass_gensel_);


        for (auto const selection2 : reco_cuts)
        {
            const char * sel_name2 = selection2.first;
            std::string sel_str2 = selection2.first;

            if (sel_str2 != sel_str)
            {
                nogensel_nm1_onemu[sel_name].second->add(sel_str2, reco_cuts[sel_name2]);
                // gensel_nm1_onemu[sel_name].second->add(sel_str2, reco_cuts[sel_name2]);
            }
        }


    }

}


bool VLQToHiggsPairProdAnalysis::process(Event & event) {

    // cout << "VLQToHiggsPairProdAnalysis: Starting to process event (runid, eventid) = (" << event.run << ", " << event.event << ")" << endl;

    // TEST STUFF HERE
    // if (event_count == 0) {
    //     std::vector<std::string> const & trig_names = event.get_current_triggernames();
    //     for (auto const & name : trig_names)
    //         std::cout << name << std::endl;
    // }

    // event_count++;


    // FIRST RUN PRE_MODULES THAT NEED TO RUN AT THE BEGINNING (e.g. MC lumi re-weighting)

    for(auto & m: pre_modules){
        m->process(event);
    }

    float part_ht = event.get(parton_ht);

    if ((version == "ZJets" || version == "WJets") && part_ht > 100.)
        return false;
    
    nogensel_noclean->fill(event);

    // NOW RUN POST_MODULES AND DO THE REST

    for (auto & m: post_modules){
        m->process(event);
    }

    nogensel_nocuts->fill(event);

    // bool passes_any_gensel = (
    //     // gen_el_finalselection->passes(event) ||
    //     gen_mu_finalselection->passes(event)
    //     );

    bool passes_preselection = false;

    // event.set(pass_gensel_, passes_any_gensel);

    // if (gensel_nocuts.second->passes(event))
    // {
    //     gensel_nocuts.first->fill(event);
    //     // gensel_nocuts.first.second->fill(event);
    // }

    if (nogensel_fin_onemu.second->passes(event))
    {
        nogensel_fin_onemu.first->fill(event);
    }

    // if (gensel_fin_onemu.second->passes(event))
    //     gensel_fin_onemu.first->fill(event);

    for (auto const & selection : reco_cuts)
    {
        const char * sel_name = selection.first;
        if (nogensel_onecut[sel_name].second->passes(event))
            nogensel_onecut[sel_name].first->fill(event);

        // if (gensel_onecut[sel_name].second->passes(event))
        //     gensel_onecut[sel_name].first->fill(event);

        if (nogensel_nm1_onemu[sel_name].second->passes(event))
        {
            if ((std::string)selection.first == "MuonPtCut")
            {
                passes_preselection = true;
            }
            nogensel_nm1_onemu[sel_name].first->fill(event);
        }

        // if (gensel_nm1_onemu[sel_name].second->passes(event))
        //     gensel_nm1_onemu[sel_name].first->fill(event);
    }

    // TEST EFFECT OF MUON ISOLATION ON JETLEPTONCLEANER AND RELISO HERE
    
    return passes_preselection;
}

UHH2_REGISTER_ANALYSIS_MODULE(VLQToHiggsPairProdAnalysis)
