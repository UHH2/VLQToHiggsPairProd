#pragma once

#include "UHH2/core/include/Hists.h"
#include "UHH2/core/include/Event.h"


/**
 *   Example class for booking and filling histograms, the new version using AnalysisModule mechanisms.
 */

class GenHists: public uhh2::Hists {
public:

    struct GenHistColl
    {
        int pdgid, mother_id, veto_mother_id, order_num;
        TH1F *h_pt, *h_eta, *h_phi, *h_n, *h_mass, *charge, *decay, *mother;
    };

    // use the same constructor arguments as Hists for forwarding:
    GenHists(uhh2::Context & ctx, const std::string & dirname, const std::string & h_part_ht = "parton_ht");
    virtual void fill(const uhh2::Event & ev) override;
    void add_genhistcoll(int pdgid, int mother_id, int veto_mother_id, int order_num = -1,
                            bool mass = true, bool charge = true, bool decay = true, bool mother = true);
    void fill_genhistcoll(const uhh2::Event & ev, GenHistColl & gen_histcoll);


    virtual ~GenHists();
private:
    uhh2::Context & ctx_;
    std::string dirname_;
	uhh2::Event::Handle<double> h_part_ht_;

    std::vector<GenHistColl> all_hists;

	TH1F *tp_decay, *h_decay, *t_decay, *b_decay, *w_decay, *z_decay;
	TH1F *spec_parton_ht, *spec_deltaR_bb_h, *spec_deltaR_bb_min, *spec_max_deltaR_topprod;
	TH2F *spec_top_pt_vs_max_dR;
};
