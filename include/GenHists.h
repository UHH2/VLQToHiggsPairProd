#pragma once

#include "UHH2/core/include/Hists.h"
#include "UHH2/core/include/Event.h"


/**
 *   Example class for booking and filling histograms, the new version using AnalysisModule mechanisms.
 */

class GenHists: public uhh2::Hists {
public:
    // use the same constructor arguments as Hists for forwarding:
    GenHists(uhh2::Context & ctx, const std::string & dirname);

    virtual void fill(const uhh2::Event & ev) override;
    virtual ~GenHists();
private:
	uhh2::Event::Handle<double> h_part_ht_;

	TH1F *tp_pt_lead, *tp_pt_subl, *tp_eta_lead, *tp_eta_subl, *tp_phi_lead, *tp_phi_subl;
	TH1F *t_pt_lead, *t_pt_subl, *t_eta_lead, *t_eta_subl, *t_phi_lead, *t_phi_subl;
	TH1F *h_pt_lead, *h_pt_subl, *h_eta_lead, *h_eta_subl, *h_phi_lead, *h_phi_subl;
	TH1F *bTp_pt_lead, *bTp_pt_subl, *bH_pt_lead, *bH_pt_subl;
	TH1F *genjet_pt_lead, *genjet_pt_subl, *genjet_pt_all, *genjet_eta_lead, *genjet_eta_subl, *genjet_eta_all, *genjet_phi_lead, *genjet_phi_subl, *genjet_phi_all;
	TH1F *mu_pt_lead, *mu_pt_lead2, *mu_pt_subl, *mu_pt_subl2, *mu_eta_lead, *mu_eta_subl, *mu_phi_lead, *mu_phi_subl;
	TH1F *el_pt_lead, *el_pt_lead2, *el_pt_subl, *el_pt_subl2, *el_eta_lead, *el_eta_subl, *el_phi_lead, *el_phi_subl;
	TH1F *mutop_pt_lead, *mutop_pt_lead2, *mutop_pt_subl, *mutop_pt_subl2, *mutop_eta_lead, *mutop_eta_subl, *mutop_phi_lead, *mutop_phi_subl;
	TH1F *eltop_pt_lead, *eltop_pt_lead2, *eltop_pt_subl, *eltop_pt_subl2, *eltop_eta_lead, *eltop_eta_subl, *eltop_phi_lead, *eltop_phi_subl;
	TH1F *tp_m, *t_m, *h_m, *t_N, *h_N, *b_N, *l_N, *mu_N, *el_N, *ltop_N, *mutop_N, *eltop_N;
	TH1F *tp_decay, *h_decay, *t_decay, *b_decay, *w_decay, *z_decay;
	TH1F *spec_parton_ht, *spec_deltaR_bb_h, *spec_deltaR_bb_min, *spec_max_deltaR_topprod;
	TH2F *spec_top_pt_vs_max_dR;
};
