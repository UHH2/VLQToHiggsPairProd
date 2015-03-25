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
#include "UHH2/common/include/ObjectIdUtils.h"



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

class TpTpCycle: public AnalysisModule {
public:

    enum ParticleID {
        BottomID = 5,
        TopID = 6,
        TprimeID = 8,
        ElectronID = 11,
        MuonID = 13,
        HiggsID = 25
    };
    
    explicit TpTpCycle(Context & ctx);
    virtual bool process(Event & event);

private:

    std::string version;
    size_t event_count;
    double lumi_factor;

    // // declare the Selections to use.
    // std::vector<std::unique_ptr<Selection> > v_sel;

    std::map<const char *, std::shared_ptr<Selection> > reco_cuts;

    // no gen selection, no reco selection, both gen and reco plots
    std::unique_ptr<Hists>
            nogensel_afterpresel
            ;

    // with/without gen selection, one-cut and n-minus-1 reco selections, only reco plots
    std::map<const char*, std::pair< std::unique_ptr<Hists>, std::unique_ptr<AndSelection> > >
            nogensel_onecut,
            // gensel_onecut,
            nogensel_nm1cut
            // gensel_nm1_onemu
            ;

    // with/without gen selection, final reco selection, only reco plots
    std::pair<std::unique_ptr<Hists> , std::unique_ptr<AndSelection> >
            nogensel_fullselection
            // gensel_fin_onemu
            ;
    
    std::vector<std::unique_ptr<AnalysisModule> > pre_modules, post_modules;



    // handles
    // Event::Handle<bool> pass_gensel_;
    Event::Handle<double> parton_ht;
   
    // internal function to fill all histograms
};


TpTpCycle::TpTpCycle(Context & ctx) {

    
    // If running in SFrame, the keys "dataset_version", "dataset_type" and "dataset_lumi"
    // are set to the according values in the xml file. For CMSSW, these are
    // not set automatically, but can be set in the python config file.
    // for(auto kv : ctx.get_all()){
    //     cout << " " << kv.first << " = " << kv.second << endl;
    // }

    
    // 1. define handles and other stuff here for later call in TpTpCycle::process

    version = ctx.get("dataset_version");
    event_count = 0;
    double dataset_lumi = string2double(ctx.get("dataset_lumi"));
    double reweight_to_lumi = string2double(ctx.get("target_lumi"));
    lumi_factor = reweight_to_lumi / dataset_lumi;

    CSVBTag::wp btag_wp = CSVBTag::WP_MEDIUM;

    // btag = CSVBTag(btag_wp);
    // toptag =CMSTopTag();

    // pass_gensel_ = ctx.get_handle<bool>("pass_gensel");
    parton_ht = ctx.get_handle<double>("parton_ht");
    





    // 2. setup other modules


    // all the reweighting and jet correction modules
    bool mclumiweight = true;
    bool mcpileupreweight = true;
    bool jec = false;
    bool jersmear = false;

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
    // post_modules.emplace_back(new ElectronCleaner(AndId<Electron>(ElectronID_PHYS14_25ns_medium, PtEtaCut(20.0, 2.4))));
    // post_modules.emplace_back(new MuonCleaner(AndId<Muon>(MuonIDTight(), PtEtaCut(20.0, 2.1))));
    // post_modules.emplace_back(new JetLeptonCleaner(JERFiles::PHYS14_L123_MC));
    // post_modules.emplace_back(new JetCleaner(PtEtaCut(30.0, 2.4)));
    // post_modules.emplace_back(new JetPtSorter());

    // calculate values like HT, number of b-tags, top-tags etc.
    post_modules.emplace_back(new HTCalculator(ctx));
    post_modules.emplace_back(new PrimaryLepton(ctx));
    // post_modules.emplace_back(new HTLepCalculator(ctx));
    post_modules.emplace_back(new JetTagCalculator(ctx, "n_btags", CSVBTag(btag_wp)));
    post_modules.emplace_back(new TopTagCalculator(ctx.get_handle<int>("n_toptags"), TopJetId(CMSTopTag())));



    // 3. set up no-cuts histograms

    // 4. set final reco selections (and the gen selection)


    // DEFINE RECO SELECTIONS HERE
    // reco_cuts["PrimLepCut"] = std::shared_ptr<Selection>(new PrimaryLeptonPtSelection(ctx.get_handle<FlavorParticle>("PrimaryLepton"), 50.));
    // reco_cuts["STCut"] = std::shared_ptr<Selection>(new STSelection(ctx.get_handle<double>("HT"), ctx.get_handle<FlavorParticle>("PrimaryLepton"), 500.));
    // // REMOVE BTAG CUT FROM TpTpCycle
    // // reco_cuts["BTagCut"] = std::shared_ptr<Selection>(new NJetSelection(1, -1, JetId(CSVBTag(btag_wp))));
    // reco_cuts["JetPtCut"] = std::shared_ptr<Selection>(new JetPtSelection(200.));

    // std::shared_ptr<Selection> min_1el(new NElectronSelection(1, -1, ElectronId(AndId<Electron>(ElectronID_PHYS14_25ns_medium, PtEtaCut(20.0, 2.4)))));
    // reco_cuts["1ElectronVeto"] = std::shared_ptr<Selection>(new VetoSelection(min_1el));
    // reco_cuts["2OneMuonCut"] = std::shared_ptr<Selection>(new NMuonSelection(1, 1, MuonId(AndId<Muon>(MuonIDTight(), PtEtaCut(50.0, 2.1)))));
    // reco_cuts["3HTCut"] = std::shared_ptr<Selection>(new HTSelection(ctx.get_handle<double>("HT"), 700.));
    reco_cuts["4BTagCut"] = std::shared_ptr<Selection>(new NJetSelection(1, -1, JetId(CSVBTag(btag_wp))));
    reco_cuts["5OneTopTagCut"] = std::shared_ptr<Selection>(new NTopJetSelection(1, -1, TopJetId(CMSTopTag())));
    reco_cuts["6OneHiggsTagCut"] = std::shared_ptr<Selection>(new NTopJetSelection(1, -1, TopJetId(HiggsTag()), ctx.get_handle<std::vector<TopJet> >("patJetsCa15CHSJetsFilteredPacked")));




    nogensel_afterpresel.reset(new HistCollector(ctx, "NoGenSel-AfterPresel"));


    // // 5. set up hists and selections


    nogensel_fullselection.first.reset(new HistCollector(ctx, "NoGenSel-FullSelection"));
    nogensel_fullselection.second.reset(new AndSelection(ctx, "nogensel_fullselection"));

    // gensel_fin_onemu.first.reset(new HistCollector(ctx, "GenSel-AllCuts"));
    // gensel_fin_onemu.second.reset(new AndSelection(ctx, "gensel_allcuts"));
    // gensel_fin_onemu.second->add<BoolSelection>("gen_finalstate_sel", pass_gensel_);

    for (auto const & selection : reco_cuts)
    {
        const char * sel_name = selection.first;
        std::string sel_str = selection.first;

        // append AndSelections for AllCuts selections
        nogensel_fullselection.second->add(sel_str, reco_cuts[sel_name]);
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

        nogensel_nm1cut[sel_name] = std::make_pair(std::unique_ptr<Hists>(new HistCollector(ctx, "NoGenSel-Nminus1-"+sel_str)),
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
                nogensel_nm1cut[sel_name].second->add(sel_str2, reco_cuts[sel_name2]);
                // gensel_nm1_onemu[sel_name].second->add(sel_str2, reco_cuts[sel_name2]);
            }
        }


    }


}


bool TpTpCycle::process(Event & event) {

    // cout << "TpTpCycle: Starting to process event (runid, eventid) = (" << event.run << ", " << event.event << ")" << endl;

    // TEST STUFF HERE



    // FIRST RUN PRE_MODULES THAT NEED TO RUN AT THE BEGINNING (e.g. MC lumi re-weighting)

    for(auto & m: pre_modules){
        m->process(event);
    }

    // differentiate between pre_modules and post_modules if you want to make some plots before cleaning the histograms

    for (auto & m: post_modules){
        m->process(event);
    }

    if (!event_count)
    {
        // std::cout << version << " " << event.weight << " " << lumi_factor << std::endl;
        if (event.weight != lumi_factor)
            std::cout << "WARNING: re-weighting for lumi for the second time!!" << std::endl;
        event_count++;
    }

    nogensel_afterpresel->fill(event);

    if (nogensel_fullselection.second->passes(event))
    {
        nogensel_fullselection.first->fill(event);
        // return true;
    }

    for (auto const & selection : reco_cuts)
    {
        const char * sel_name = selection.first;
        if (nogensel_onecut[sel_name].second->passes(event))
            nogensel_onecut[sel_name].first->fill(event);

        // if (gensel_onecut[sel_name].second->passes(event))
        //     gensel_onecut[sel_name].first->fill(event);

        if (nogensel_nm1cut[sel_name].second->passes(event))
        {
            nogensel_nm1cut[sel_name].first->fill(event);
        }

        // if (gensel_nm1_onemu[sel_name].second->passes(event))
        //     gensel_nm1_onemu[sel_name].first->fill(event);
    }

    
    return false;
}

UHH2_REGISTER_ANALYSIS_MODULE(TpTpCycle)
