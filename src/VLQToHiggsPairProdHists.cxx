#include "UHH2/VLQToHiggsPairProd/include/VLQToHiggsPairProdHists.h"

#include "UHH2/core/include/Event.h"

#include "UHH2/common/include/Utils.h"
#include "UHH2/core/include/LorentzVector.h"

#include "TH1F.h"
#include "TH2F.h"
#include <iostream>

using namespace std;
using namespace uhh2;

HistCollector::HistCollector(Context & ctx, const string & dirname, bool gen_plots) :
    Hists(ctx, dirname),
    el_hists(new ElectronHists(ctx, dirname+"/ElectronHists", gen_plots)),
    mu_hists(new MuonHists(ctx, dirname+"/MuonHists", gen_plots)),
    tau_hists(new TauHists(ctx, dirname+"/TauHists")),
    ev_hists(new ExtendedEventHists(ctx, dirname+"/EventHists")),
    jet_hists(new JetHists(ctx, dirname+"/JetHists")),
    topjet_hists(new TopJetHists(ctx, dirname+"/TopJetHists")),
    gen_hists(gen_plots ? new GenHists(ctx, dirname+"/GenHists") : NULL)

    {
        // if (gen_plots) gen_hists = new GenHists(ctx, dirname+"/GenHists");
        // else gen_hists = 0;
    } 

void HistCollector::fill(const Event & event) {
    el_hists->fill(event);
    mu_hists->fill(event);
    tau_hists->fill(event);
    ev_hists->fill(event);
    jet_hists->fill(event);
    topjet_hists->fill(event);
    if (gen_hists) gen_hists->fill(event);
}

HistCollector::~HistCollector(){
    delete el_hists;
    delete mu_hists;
    delete tau_hists;
    delete ev_hists;
    delete jet_hists;
    delete topjet_hists;
    delete gen_hists;

}

VLQToHiggsPairProdHists::VLQToHiggsPairProdHists(Context & ctx, const string & dirname, bool gen_plots):
    Hists(ctx, dirname), gen_plots_(gen_plots), h_ht_(ctx.get_handle<double>("HT")),
    h_btags_(ctx.get_handle<int>("n_btags")), h_toptags_(ctx.get_handle<int>("n_toptags"))
{
	// book all histograms here
    // jets
    n_jets          = book<TH1F>("jets_N", "N_{jets}", 20, 0, 20);     
    n_bjets         = book<TH1F>("jets_Nbs", "N_{b-tags}", 20, 0, 20);
    n_topjets       = book<TH1F>("jets_Ntops", "N_{top jets}", 20, 0, 20);
    eta_jets        = book<TH1F>("jets_eta", "#eta^{jets}", 40, -2.5, 2.5);
    pt_jets         = book<TH1F>("jets_pt", "#pt^{jets}", 60, 0, 1500);
    csv_jets        = book<TH1F>("jets_csv","csv-disriminator all jets",50,0,1);
    pt_jet1         = book<TH1F>("jet_1_pt", "#pt^{jet 1}", 60, 0, 1500);
    pt_jet2         = book<TH1F>("jet_2_pt", "#pt^{jet 2}", 60, 0, 1500);
    csv_jet1        = book<TH1F>("jet_1_csv","csv-disriminator first jet",50,0,1);
    csv_jet2        = book<TH1F>("jet_2_csv","csv-disriminator second jet",50,0,1);
    drmin_jet1      = book<TH1F>("jet_1_dR_closestJ", "#Delta R_{min}(First jet,nearest jet)", 40, 0, 2.0);
    drmin_jet2      = book<TH1F>("jet_2_dR_closestJ", "#Delta R_{min}(Second jet,nearest jet)", 40, 0, 2.0);

    // electrons
    number_el      = book<TH1F>("el_N",      "number of electrons",7,-0.5,6.5);

    pt_el          = book<TH1F>("el_pt",          "p_{T} electron",           100,0,500);
    eta_el         = book<TH1F>("el_eta",         "#eta electron",            100,-3,3);
    isolation_el   = book<TH1F>("el_isolation",   "relIso electron",          100,0,0.5);
    ptrel_el       = book<TH1F>("el_ptrel",       "p_{T}^{rel}(e,jet)",       40, 0, 200.);
    deltaRmin_el   = book<TH1F>("el_deltaRmin",   "#Delta R_{min}(e,jet)",    40, 0, 2.0);
    deltaRmin_ptrel_el
                = book<TH2F>("el_deltaRmin_ptrel",
                                            ";#Delta R_{min}(e,jet);p_{T}^{rel}(e,jet)",
                                                                        40, 0, 2.0, 40, 0, 200.);
    
    pt_1_el        = book<TH1F>("el_1_pt",        "p_{T} electron 1",         100,0,500);
    eta_1_el       = book<TH1F>("el_1_eta",       "#eta electron 1",          100,-3,3);
    isolation_1_el = book<TH1F>("el_1_isolation", "relIso electron 1",        100,0,0.5);
    ptrel_1_el     = book<TH1F>("el_1_ptrel",     "p_{T}^{rel}(e 1,jet)",     40, 0, 200.);
    deltaRmin_1_el = book<TH1F>("el_1_deltaRmin", "#Delta R_{min}(e 1,jet)",  40, 0, 2.0);
    deltaRmin_ptrel_1_el
                = book<TH2F>("el_1_deltaRmin_ptrel",
                                            ";#Delta R_{min}(e 1,jet);p_{T}^{rel}(e 1,jet)",
                                                                        40, 0, 2.0, 40, 0, 200.);
    
    pt_2_el        = book<TH1F>("el_2_pt",        "p_{T} electron 2",         100,0,500);
    eta_2_el       = book<TH1F>("el_2_eta",       "#eta electron 2",          100,-3,3);
    isolation_2_el = book<TH1F>("el_2_isolation", "relIso electron 2",        100,0,0.5);
    ptrel_2_el     = book<TH1F>("el_2_ptrel",     "p_{T}^{rel}(e 2,jet)",     40, 0, 200.);
    deltaRmin_2_el = book<TH1F>("el_2_deltaRmin", "#Delta R_{min}(e 2,jet)",  40, 0, 2.0);
    deltaRmin_ptrel_2_el
                = book<TH2F>("el_2_deltaRmin_ptrel",
                                            ";#Delta R_{min}(e 2,jet);p_{T}^{rel}(e 2,jet)",
                                                                        40, 0, 2.0, 40, 0, 200.);
    if (gen_plots_) {
        eff_sub_el     = book<TH1F>("el_eff_sub",     "p_{T}",                100,0,500);
        eff_tot_el     = book<TH1F>("el_eff_tot",     "p_{T}",                100,0,500);
        pt_response_el = book<TH1F>("el_pt_response", "(p_{T, gen} - p_{T, reco}) / p_{T, gen}",
                                                                        800,-1.,1.);
    } else {
        eff_sub_el     = 0;
        eff_tot_el     = 0;
        pt_response_el = 0;
    }

    // muons
    number_mu      = book<TH1F>("mu_N",      "number of muons",7,-0.5,6.5);

    pt_mu          = book<TH1F>("mu_pt",          "p_{T} muon",           100,0,500);
    eta_mu         = book<TH1F>("mu_eta",         "#eta muon",            100,-3,3);
    isolation_mu   = book<TH1F>("mu_isolation",   "relIso muon",          100,0,0.5);
    ptrel_mu       = book<TH1F>("mu_ptrel",       "p_{T}^{rel}(mu,jet)",       40, 0, 200.);
    deltaRmin_mu   = book<TH1F>("mu_deltaRmin",   "#Delta R_{min}(mu,jet)",    40, 0, 2.0);
    deltaRmin_ptrel_mu
                = book<TH2F>("mu_deltaRmin_ptrel",
                                            ";#Delta R_{min}(mu,jet);p_{T}^{rel}(mu,jet)",
                                                                        40, 0, 2.0, 40, 0, 200.);
    
    pt_1_mu        = book<TH1F>("mu_1_pt",        "p_{T} muon 1",         100,0,500);
    eta_1_mu       = book<TH1F>("mu_1_eta",       "#eta muon 1",          100,-3,3);
    isolation_1_mu = book<TH1F>("mu_1_isolation", "relIso muon 1",        100,0,0.5);
    ptrel_1_mu     = book<TH1F>("mu_1_ptrel",     "p_{T}^{rel}(mu 1,jet)",     40, 0, 200.);
    deltaRmin_1_mu = book<TH1F>("mu_1_deltaRmin", "#Delta R_{min}(mu 1,jet)",  40, 0, 2.0);
    deltaRmin_ptrel_1_mu
                = book<TH2F>("mu_1_deltaRmin_ptrel",
                                            ";#Delta R_{min}(mu 1,jet);p_{T}^{rel}(mu 1,jet)",
                                                                        40, 0, 2.0, 40, 0, 200.);
    
    pt_2_mu        = book<TH1F>("mu_2_pt",        "p_{T} muon 2",         100,0,500);
    eta_2_mu       = book<TH1F>("mu_2_eta",       "#eta muon 2",          100,-3,3);
    isolation_2_mu = book<TH1F>("mu_2_isolation", "relIso muon 2",        100,0,0.5);
    ptrel_2_mu     = book<TH1F>("mu_2_ptrel",     "p_{T}^{rel}(mu 2,jet)",     40, 0, 200.);
    deltaRmin_2_mu = book<TH1F>("mu_2_deltaRmin", "#Delta R_{min}(mu 2,jet)",  40, 0, 2.0);
    deltaRmin_ptrel_2_mu
                = book<TH2F>("mu_2_deltaRmin_ptrel",
                                            ";#Delta R_{min}(mu 2,jet);p_{T}^{rel}(mu 2,jet)",
                                                                        40, 0, 2.0, 40, 0, 200.);
    if (gen_plots_) {
        eff_sub_mu     = book<TH1F>("mu_eff_sub",     "p_{T}",                100,0,500);
        eff_tot_mu     = book<TH1F>("mu_eff_tot",     "p_{T}",                100,0,500);
        pt_response_mu = book<TH1F>("mu_pt_response", "(p_{T, gen} - p_{T, reco}) / p_{T, gen}",
                                                                        800,-1.,1.);
    } else {
        eff_sub_mu     = 0;
        eff_tot_mu     = 0;
        pt_response_mu = 0;
    }

    // event variables
    N_PrimVertices = book<TH1F>("event_N_pv", "N^{PV}", 50, 0, 50);
    MET = book<TH1F>("event_MET", "missing E_{T}", 200,0,1000);
    HT = book<TH1F>("event_HT", "H_{T} Jets", 100, 0, 3500);


}


void VLQToHiggsPairProdHists::fill(const Event & event){
    // fill the histograms. Don't forget to always use the weight when filling:
    double w = event.weight;

    // fill jets histograms

    assert(event.jets);
    n_jets->Fill(event.jets->size(), w);

    int n_btags = event.get(h_btags_);
    n_bjets->Fill(n_btags, w);
    int n_toptags = event.get(h_toptags_);
    n_topjets->Fill(n_toptags, w);
    
    for(const auto & jet : *event.jets){
        pt_jets->Fill(jet.pt(), w);
        eta_jets->Fill(jet.eta(), w);
        csv_jets->Fill(jet.btag_combinedSecondaryVertex(), w);
    }

    if(event.jets->size() > 0){
        const auto & jet = (*event.jets)[0];
        pt_jet1->Fill(jet.pt(), w);
        csv_jet1->Fill(jet.btag_combinedSecondaryVertex(), w);
        auto next_jet = nextJet(jet, *event.jets);
        auto drmin = next_jet ? deltaR(jet, *next_jet) : numeric_limits<float>::infinity();
        drmin_jet1->Fill(drmin, w);
    }
    if(event.jets->size() > 1){
        const auto & jet = (*event.jets)[1];
        pt_jet2->Fill(jet.pt(), w);
        csv_jet2->Fill(jet.btag_combinedSecondaryVertex(), w);
        auto next_jet = nextJet(jet, *event.jets);
        auto drmin = next_jet ? deltaR(jet, *next_jet) : numeric_limits<float>::infinity();
        drmin_jet2->Fill(drmin, w);
    }
    
    // fill electrons histogram
    assert(event.electrons);
    number_el->Fill(event.electrons->size(), w);

    if (eff_sub_el && event.genparticles) {
        for (const auto & gp: *event.genparticles) {
            if (abs(gp.pdgId()) == 11) {
                auto gp_pt = gp.pt();
                eff_tot_el->Fill(gp_pt, w);
                auto ele = closestParticle(gp, *event.electrons);
                if (ele && deltaR(gp, *ele) < 0.1) {
                    eff_sub_el->Fill(gp_pt, w);
                    pt_response_el->Fill((gp_pt - ele->pt()) / gp_pt, w);
                }
            }
        }
    }

    // buffer values for ptrel and drmin to avoid recomputation:
    vector<float> drmin_buf;
    vector<float> ptrel_buf;
    for(const auto & ele : *event.electrons){
        pt_el->Fill(ele.pt(), w);
        eta_el->Fill(ele.eta(), w);
        isolation_el->Fill(ele.relIso(), w);
        
        if(event.jets){
            auto nj = nextJet(ele, *event.jets);
            auto drmin_val = nj ? deltaR(ele, *nj) : numeric_limits<float>::infinity();
            drmin_buf.push_back(drmin_val);
            ptrel_buf.push_back(pTrel(ele, nj));
            ptrel_el->Fill(ptrel_buf.back(), w);
            deltaRmin_el->Fill(drmin_buf.back(), w);
            deltaRmin_ptrel_el->Fill(drmin_buf.back(), ptrel_buf.back(), w);
        }
    }
    
    if(event.electrons->size() > 0){
        const auto & ele = (*event.electrons)[0];
        pt_1_el->Fill(ele.pt(), w);
        eta_1_el->Fill(ele.eta(), w);
        isolation_1_el->Fill(ele.relIso(), w);
        if(event.jets){
            ptrel_1_el->Fill(ptrel_buf[0], w);
            deltaRmin_1_el->Fill(drmin_buf[0], w);
            deltaRmin_ptrel_1_el->Fill(drmin_buf[0], ptrel_buf[0], w);
        }
    }
    if(event.electrons->size() > 1){
        const auto & ele = (*event.electrons)[1];
        pt_2_el->Fill(ele.pt(), w);
        eta_2_el->Fill(ele.eta(), w);
        isolation_2_el->Fill(ele.relIso(), w);
        if(event.jets){
            ptrel_2_el->Fill(ptrel_buf[1], w);
            deltaRmin_2_el->Fill(drmin_buf[1], w);
            deltaRmin_ptrel_2_el->Fill(drmin_buf[1], ptrel_buf[1], w);
        }
    }
    
    // fill muons histogram
    assert(event.muons);
    number_mu->Fill(event.muons->size(), w);

    if (eff_sub_mu && event.genparticles) {
        for (const auto & gp: *event.genparticles) {
            if (abs(gp.pdgId()) == 13) {
                auto gp_pt = gp.pt();
                eff_tot_mu->Fill(gp_pt, w);
                auto ele = closestParticle(gp, *event.muons);
                if (ele && deltaR(gp, *ele) < 0.1) {
                    eff_sub_mu->Fill(gp_pt, w);
                    pt_response_mu->Fill((gp_pt - ele->pt()) / gp_pt, w);
                }
            }
        }
    }

    // buffer values for ptrel and drmin to avoid recomputation:
    drmin_buf.clear();
    ptrel_buf.clear();
    for(const auto & muon : *event.muons){
        pt_mu->Fill(muon.pt(), w);
        eta_mu->Fill(muon.eta(), w);
        isolation_mu->Fill(muon.relIso(), w);
        
        if(event.jets){
            auto nj = nextJet(muon, *event.jets);
            auto drmin_val = nj ? deltaR(muon, *nj) : numeric_limits<float>::infinity();
            drmin_buf.push_back(drmin_val);
            ptrel_buf.push_back(pTrel(muon, nj));
            ptrel_mu->Fill(ptrel_buf.back(), w);
            deltaRmin_mu->Fill(drmin_buf.back(), w);
            deltaRmin_ptrel_mu->Fill(drmin_buf.back(), ptrel_buf.back(), w);
        }
    }
    
    if(event.muons->size() > 0){
        const auto & muon = (*event.muons)[0];
        pt_1_mu->Fill(muon.pt(), w);
        eta_1_mu->Fill(muon.eta(), w);
        isolation_1_mu->Fill(muon.relIso(), w);
        if(event.jets){
            ptrel_1_mu->Fill(ptrel_buf[0], w);
            deltaRmin_1_mu->Fill(drmin_buf[0], w);
            deltaRmin_ptrel_1_mu->Fill(drmin_buf[0], ptrel_buf[0], w);
        }
    }
    if(event.muons->size() > 1){
        const auto & muon = (*event.muons)[1];
        pt_2_mu->Fill(muon.pt(), w);
        eta_2_mu->Fill(muon.eta(), w);
        isolation_2_mu->Fill(muon.relIso(), w);
        if(event.jets){
            ptrel_2_mu->Fill(ptrel_buf[1], w);
            deltaRmin_2_mu->Fill(drmin_buf[1], w);
            deltaRmin_ptrel_2_mu->Fill(drmin_buf[1], ptrel_buf[1], w);
        }
    }

    // event hists
    assert(event.met);
    assert(event.pvs);
    N_PrimVertices->Fill(event.pvs->size(), w);
    MET->Fill(event.met->pt(), w);
    if(event.is_valid(h_ht_)){
        float ht = event.get(h_ht_);
        HT->Fill(ht, w);
    }
  
  
}

VLQToHiggsPairProdHists::~VLQToHiggsPairProdHists(){}
