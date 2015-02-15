#pragma once

#include "UHH2/core/include/Hists.h"
#include "UHH2/core/include/Event.h"

#include "UHH2/common/include/ElectronHists.h"
#include "UHH2/common/include/EventHists.h"
#include "UHH2/common/include/JetHists.h"
#include "UHH2/common/include/MuonHists.h"
#include "UHH2/common/include/TauHists.h"
#include "UHH2/VLQToHiggsPairProd/include/GenHists.h"

#include "TH1F.h"


using namespace uhh2;

class ExtendedEventHists : public EventHists {
public:
    ExtendedEventHists(uhh2::Context & ctx, const std::string & dirname) : 
        EventHists(ctx, dirname), h_btags_(ctx.get_handle<int>("n_btags")),
        h_toptags_(ctx.get_handle<int>("n_toptags"))
        {
            h_n_btags = book<TH1F>("jets_Nbs", "N_{b-tags}", 20, 0, 20);
            h_n_toptags = book<TH1F>("jets_Ntops", "N_{top jets}", 20, 0, 20);

        }

    virtual void fill(const uhh2::Event & event) override {
        EventHists::fill(event);
        double w = event.weight;
        int n_btags = event.get(h_btags_);
        int n_toptags = event.get(h_toptags_);

        h_n_btags->Fill(n_btags, w);
        h_n_toptags->Fill(n_toptags, w);

    }

private:
    TH1F *h_n_btags, *h_n_toptags;
    uhh2::Event::Handle<int> h_btags_, h_toptags_;
};


class HistCollector : public uhh2::Hists {
public:
    HistCollector(uhh2::Context & ctx, const std::string & dirname, bool gen_plots = true);
    virtual ~HistCollector();

    virtual void fill(const uhh2::Event & ev) override;

private:
    ElectronHists * el_hists;
    MuonHists * mu_hists;
    TauHists * tau_hists;
    ExtendedEventHists * ev_hists;
    JetHists * jet_hists;
    TopJetHists * topjet_hists;
    GenHists * gen_hists;


};


class VLQToHiggsPairProdHists : public uhh2::Hists {
public:
    // use the same constructor arguments as Hists for forwarding:
    VLQToHiggsPairProdHists(uhh2::Context & ctx, const std::string & dirname, bool gen_plots = true);

    virtual void fill(const uhh2::Event & ev) override;
    virtual ~VLQToHiggsPairProdHists();

private:
    // jets
    TH1F *n_jets, *n_bjets, *n_topjets, *eta_jets, *pt_jets, *csv_jets, *pt_jet1, *pt_jet2, *csv_jet1, *csv_jet2, *drmin_jet1, *drmin_jet2;

    // electron
    TH1F *number_el, *pt_el, *eta_el, *isolation_el, *ptrel_el, *deltaRmin_el;
    TH1F *pt_1_el, *eta_1_el, *isolation_1_el, *ptrel_1_el, *deltaRmin_1_el;
    TH1F *pt_2_el, *eta_2_el, *isolation_2_el, *ptrel_2_el, *deltaRmin_2_el;
    TH1F *eff_sub_el, *eff_tot_el, *pt_response_el;

    TH2F *deltaRmin_ptrel_el, *deltaRmin_ptrel_1_el, *deltaRmin_ptrel_2_el;
    // muon
    TH1F *number_mu, *pt_mu, *eta_mu, *isolation_mu, *ptrel_mu, *deltaRmin_mu;
    TH1F *pt_1_mu, *eta_1_mu, *isolation_1_mu, *ptrel_1_mu, *deltaRmin_1_mu;
    TH1F *pt_2_mu, *eta_2_mu, *isolation_2_mu, *ptrel_2_mu, *deltaRmin_2_mu;
    TH1F *eff_sub_mu, *eff_tot_mu, *pt_response_mu;

    TH2F *deltaRmin_ptrel_mu, *deltaRmin_ptrel_1_mu, *deltaRmin_ptrel_2_mu;


    //event
    TH1F *N_PrimVertices, *MET, *HT;
    bool gen_plots_;
    uhh2::Event::Handle<double> h_ht_;
    uhh2::Event::Handle<int> h_btags_, h_toptags_;



};
