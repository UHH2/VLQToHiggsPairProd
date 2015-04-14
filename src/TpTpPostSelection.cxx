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
#include "UHH2/common/include/AdditionalSelections.h"



#include "UHH2/VLQSemiLepPreSel/include/EventHists.h"
#include "UHH2/VLQToHiggsPairProd/include/VLQToHiggsPairProdSelections.h"
#include "UHH2/VLQSemiLepPreSel/include/CustomizableGenHists.h"
#include "UHH2/VLQSemiLepPreSel/include/VLQCommonModules.h"


using namespace std;
using namespace uhh2;

using namespace vlqToHiggsPair;

// static int event_count = 0;

/** \brief Basic analysis example of an AnalysisModule (formerly 'cycle') in UHH2
 * 
 * This is the central class which calls other AnalysisModules, Hists or Selection classes.
 * This AnalysisModule, in turn, is called (via AnalysisModuleRunner) by SFrame.
 */

class TpTpPostSelection: public AnalysisModule {
public:

    enum ParticleID {
        GenJetID = 0,
        BottomID = 5,
        TopID = 6,
        TprimeID = 8,
        ElectronID = 11,
        MuonID = 13,
        ZID = 23,
        WID = 24,
        HiggsID = 25
    };
    
    explicit TpTpPostSelection(Context & ctx);
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

    // with/without gen selection, final reco selection, only reco plots
    std::pair<std::unique_ptr<Hists> , std::unique_ptr<AndSelection> >
            wgensel_afterpresel
            // gensel_fin_onemu
            ;

    // with/without gen selection, one-cut and n-minus-1 reco selections, only reco plots
    std::map<const char*, std::pair< std::unique_ptr<Hists>, std::unique_ptr<AndSelection> > >
            nogensel_onecut,
            gensel_onecut
            // nogensel_nm1cut
            // gensel_nm1_onemu
            ;
    
    std::vector<std::unique_ptr<AnalysisModule> > pre_modules, post_modules;



    // handles
    Event::Handle<bool> pass_gensel_;
    Event::Handle<double> parton_ht;


    bool gensel_;
   
    // internal function to fill all histograms
};


TpTpPostSelection::TpTpPostSelection(Context & ctx) {

    
    // If running in SFrame, the keys "dataset_version", "dataset_type" and "dataset_lumi"
    // are set to the according values in the xml file. For CMSSW, these are
    // not set automatically, but can be set in the python config file.
    // for(auto kv : ctx.get_all()){
    //     cout << " " << kv.first << " = " << kv.second << endl;
    // }

    
    // 1. define handles and other stuff here for later call in TpTpPostSelection::process

    version = ctx.get("dataset_version");
    event_count = 0;
    double dataset_lumi = string2double(ctx.get("dataset_lumi"));
    double reweight_to_lumi = string2double(ctx.get("target_lumi"));
    lumi_factor = reweight_to_lumi / dataset_lumi;

    CSVBTag::wp btag_wp = CSVBTag::WP_MEDIUM;

    // btag = CSVBTag(btag_wp);
    // toptag =CMSTopTag();

    pass_gensel_ = ctx.get_handle<bool>("pass_gensel");
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
        pre_modules.emplace_back(new NGenParticleCalculator(ctx, "n_gen_electron_top", ParticleID::ElectronID, ParticleID::TopID));
        pre_modules.emplace_back(new NGenParticleCalculator(ctx, "n_gen_electron_wtprime", ParticleID::ElectronID, ParticleID::TprimeID, ParticleID::TopID));
        pre_modules.emplace_back(new NGenParticleCalculator(ctx, "n_gen_muon_top", ParticleID::MuonID, ParticleID::TopID));
        pre_modules.emplace_back(new NGenParticleCalculator(ctx, "n_gen_muon_wtprime", ParticleID::MuonID, ParticleID::TprimeID, ParticleID::TopID));
        pre_modules.emplace_back(new PartonHT(parton_ht));
        if(mclumiweight)  pre_modules.emplace_back(new MCLumiWeight(ctx));
        if(mcpileupreweight) pre_modules.emplace_back(new MCPileupReweight(ctx));
        if(jec) post_modules.emplace_back(new JetCorrector(JERFiles::PHYS14_L123_MC));
        if(jersmear) post_modules.emplace_back(new JetResolutionSmearer(ctx));
    }
    else{
        if(jec) post_modules.emplace_back(new JetCorrector(JERFiles::PHYS14_L123_DATA));
    }

    // calculate values like HT, number of b-tags, top-tags etc.
    post_modules.emplace_back(new HTCalculator(ctx));
    post_modules.emplace_back(new PrimaryLepton(ctx));
    // post_modules.emplace_back(new HTLepCalculator(ctx));
    post_modules.emplace_back(new JetTagCalculator(ctx, "n_btags", CSVBTag(btag_wp)));
    post_modules.emplace_back(new TopTagCalculator(ctx.get_handle<int>("n_toptags"), TopJetId(CMSTopTag())));



    // 3. set up no-cuts histograms

    // 4. set final reco selections (and the gen selection)


    // DEFINE RECO SELECTIONS HERE
    
    reco_cuts["ZeroHiggsTagCut"] = std::shared_ptr<Selection>(new NTopJetSelection(0, 0, TopJetId(HiggsTag()), ctx.get_handle<std::vector<TopJet> >("patJetsCa15CHSJetsFilteredPacked")));
    reco_cuts["OneHiggsTagCut"] = std::shared_ptr<Selection>(new NTopJetSelection(1, 1, TopJetId(HiggsTag()), ctx.get_handle<std::vector<TopJet> >("patJetsCa15CHSJetsFilteredPacked")));
    reco_cuts["TwoHiggsTagCut"] = std::shared_ptr<Selection>(new NTopJetSelection(2, 2, TopJetId(HiggsTag()), ctx.get_handle<std::vector<TopJet> >("patJetsCa15CHSJetsFilteredPacked")));





    // // 5. set up hists and selections

    if (version == "TpTp_M1000_thth" || version == "TpTp_M1000_thbw" ||
        version == "TpTp_M1000_bwbw" || version == "TpTp_M1000_other")
        gensel_ = true;
    else gensel_ = false;

    // gen selections

    std::shared_ptr<Selection> thth_sel(new GenParticleIdSelection(GenParticleId(GenParticleDaughterId(8, 6, 25)), 2, 2));
    std::shared_ptr<AndSelection> thbw_sel(new AndSelection(ctx));
    thbw_sel->add<GenParticleIdSelection>("gen_finalstate_sel", GenParticleId(GenParticleDaughterId(8, 6, 25)), 1, 1);   
    thbw_sel->add<GenParticleIdSelection>("gen_finalstate_sel", GenParticleId(GenParticleDaughterId(8, 5, 24)), 1, 1);
    std::shared_ptr<Selection> bwbw_sel(new GenParticleIdSelection(GenParticleId(GenParticleDaughterId(8, 5, 24)), 2, 2));

    std::shared_ptr<OrSelection> comb_sel(new OrSelection());
    comb_sel->add(thth_sel);
    comb_sel->add(thbw_sel);
    comb_sel->add(bwbw_sel);

    std::shared_ptr<Selection> other_sel(new VetoSelection(comb_sel));

    if (!gensel_)
        nogensel_afterpresel.reset(new HistCollector(ctx, "AfterPresel"));
    else
    {
        wgensel_afterpresel.first.reset(new HistCollector(ctx, "AfterPresel"));
        wgensel_afterpresel.second.reset(new AndSelection(ctx, "gensel_afterpresel"));

        if (version == "TpTp_M1000_thth")
            wgensel_afterpresel.second->add("gen_finalstate_sel", thth_sel);   
        else if (version == "TpTp_M1000_thbw")
            wgensel_afterpresel.second->add("gen_finalstate_sel", thbw_sel);
        else if (version == "TpTp_M1000_bwbw")
            wgensel_afterpresel.second->add("gen_finalstate_sel", bwbw_sel);   
        else
            wgensel_afterpresel.second->add("gen_finalstate_sel", other_sel);

    }

    
    for (auto const & selection : reco_cuts)
    {
        const char * sel_name = selection.first;
        std::string sel_str = selection.first;

        // create histograms and selections for the onecut-only case
        nogensel_onecut[sel_name] = std::make_pair(std::unique_ptr<Hists>(new HistCollector(ctx, "OneCut-"+sel_str)),
                                                   std::unique_ptr<AndSelection>(new AndSelection(ctx, "nogensel_onecut_"+sel_str+"_cutflow")));
        if (!gensel_)
        {
            nogensel_onecut[sel_name].second->add("gen_finalstate_sel", std::shared_ptr<Selection>(new BoolSelection(pass_gensel_)));
        }
        else
        {
            if (version == "TpTp_M1000_thth")
                nogensel_onecut[sel_name].second->add("gen_finalstate_sel", thth_sel);   
            else if (version == "TpTp_M1000_thbw")
                nogensel_onecut[sel_name].second->add("gen_finalstate_sel", thbw_sel);
            else if (version == "TpTp_M1000_bwbw")
                nogensel_onecut[sel_name].second->add("gen_finalstate_sel", bwbw_sel);   
            else
                nogensel_onecut[sel_name].second->add("gen_finalstate_sel", other_sel);
        }

        nogensel_onecut[sel_name].second->add(sel_str, reco_cuts[sel_name]);


    }


}


bool TpTpPostSelection::process(Event & event) {

    // cout << "TpTpPostSelection: Starting to process event (runid, eventid) = (" << event.run << ", " << event.event << ")" << endl;

    // TEST STUFF HERE

    event.set(pass_gensel_, true);

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

    if (!gensel_)
        nogensel_afterpresel->fill(event);
    else if (wgensel_afterpresel.second->passes(event))
        wgensel_afterpresel.first->fill(event);

    bool passes_fullselection = false;

    for (auto const & selection : reco_cuts)
    {
        const char * sel_name = selection.first;
        if (nogensel_onecut[sel_name].second->passes(event))
            nogensel_onecut[sel_name].first->fill(event);
    }

    
    return passes_fullselection;
}

UHH2_REGISTER_ANALYSIS_MODULE(TpTpPostSelection)
