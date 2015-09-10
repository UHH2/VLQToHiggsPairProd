#pragma once

#include "UHH2/core/include/Hists.h"
#include "UHH2/core/include/Event.h"
#include "UHH2/core/include/GenParticle.h"
#include "UHH2/common/include/PrintingModules.h"

using namespace uhh2;
using namespace std;

/**
 *   Example class for booking and filling histograms, the new version using AnalysisModule mechanisms.
 */

template <typename T>
class RecoGenHists: public uhh2::Hists {
public:

    // use the same constructor arguments as Hists for forwarding:
    RecoGenHists(uhh2::Context & ctx, const std::string & dirname) : Hists(ctx, dirname), dirname_(dirname) {}

    virtual void fill(const uhh2::Event & ev) override {
        for (auto & i_hist : all_hists_) {
            i_hist->fill(ev);
        }
    }

    // template<class T>
    void add_genhistcoll(Context & ctx, string const & coll_name, float dr = 0.2) {
        all_hists_.emplace_back(new GenHistColl(ctx, dirname_+"/"+coll_name, coll_name, dr));
    }

    // void fill_genhistcoll(const uhh2::Event & ev, GenHistColl & gen_histcoll);

private:

    // template<typename T>
    class GenHistColl : public Hists {
    public:
        GenHistColl(Context & ctx, const string & dirname, const string & coll_name, float dr = 0.2) :
            Hists(ctx, dirname),
            hndl_in_(ctx.get_handle<vector<T>>(coll_name)),
            dr_(dr) {
                h_ind_sort_id_1 = book<TH1F>("particle_ind_sort_id_1", "particle ind sort id 1", 61, -30.5, 30.5);
                h_ind_sort_id_2 = book<TH1F>("particle_ind_sort_id_2", "particle ind sort id 2", 61, -30.5, 30.5);
                h_ind_sort_id_3 = book<TH1F>("particle_ind_sort_id_3", "particle ind sort id 3", 61, -30.5, 30.5);
                h_ind_sort_dptrel_1 = book<TH1F>("particle_ind_sort_dptrel_1", "particle ind sort dptrel 1", 100, -.5, .5);
                h_ind_sort_dptrel_2 = book<TH1F>("particle_ind_sort_dptrel_2", "particle ind sort dptrel 2", 100, -.5, .5);
                h_ind_sort_dptrel_3 = book<TH1F>("particle_ind_sort_dptrel_3", "particle ind sort dptrel 3", 100, -.5, .5);
                h_ind_sort_dr_1 = book<TH1F>("particle_ind_sort_dr_1", "particle ind sort_dr 1", 20, 0., 0.2);
                h_ind_sort_dr_2 = book<TH1F>("particle_ind_sort_dr_2", "particle ind sort_dr 2", 20, 0., 0.2);
                h_ind_sort_dr_3 = book<TH1F>("particle_ind_sort_dr_3", "particle ind sort_dr 3", 20, 0., 0.2);
                h_dr_sort_id_1 = book<TH1F>("particle_dr_sort_id_1", "particle dr sort id 1", 61, -30.5, 30.5);
                h_dr_sort_id_2 = book<TH1F>("particle_dr_sort_id_2", "particle dr sort id 2", 61, -30.5, 30.5);
                h_dr_sort_id_3 = book<TH1F>("particle_dr_sort_id_3", "particle dr sort id 3", 61, -30.5, 30.5);
                h_dr_sort_dptrel_1 = book<TH1F>("particle_dr_sort_dptrel_1", "particle dr sort dptrel 1", 100, -.5, .5);
                h_dr_sort_dptrel_2 = book<TH1F>("particle_dr_sort_dptrel_2", "particle dr sort dptrel 2", 100, -.5, .5);
                h_dr_sort_dptrel_3 = book<TH1F>("particle_dr_sort_dptrel_3", "particle dr sort dptrel 3", 100, -.5, .5);
                h_dr_sort_dr_1 = book<TH1F>("particle_dr_sort_dr_1", "particle dr sort_dr 1", 20, 0., 0.2);
                h_dr_sort_dr_2 = book<TH1F>("particle_dr_sort_dr_2", "particle dr sort_dr 2", 20, 0., 0.2);
                h_dr_sort_dr_3 = book<TH1F>("particle_dr_sort_dr_3", "particle dr sort_dr 3", 20, 0., 0.2);
                h_pt_sort_id_1 = book<TH1F>("particle_pt_sort_id_1", "particle pt sort id 1", 61, -30.5, 30.5);
                h_pt_sort_id_2 = book<TH1F>("particle_pt_sort_id_2", "particle pt sort id 2", 61, -30.5, 30.5);
                h_pt_sort_id_3 = book<TH1F>("particle_pt_sort_id_3", "particle pt sort id 3", 61, -30.5, 30.5);
                h_pt_sort_dptrel_1 = book<TH1F>("particle_pt_sort_dptrel_1", "particle pt sort dptrel 1", 100, -.5, .5);
                h_pt_sort_dptrel_2 = book<TH1F>("particle_pt_sort_dptrel_2", "particle pt sort dptrel 2", 100, -.5, .5);
                h_pt_sort_dptrel_3 = book<TH1F>("particle_pt_sort_dptrel_3", "particle pt sort dptrel 3", 100, -.5, .5);
                h_pt_sort_dr_1 = book<TH1F>("particle_pt_sort_dr_1", "particle pt sort_dr 1", 20, 0., 0.2);
                h_pt_sort_dr_2 = book<TH1F>("particle_pt_sort_dr_2", "particle pt sort_dr 2", 20, 0., 0.2);
                h_pt_sort_dr_3 = book<TH1F>("particle_pt_sort_dr_3", "particle pt sort_dr 3", 20, 0., 0.2);

                h_categories = book<TH1F>("decay_categories", "decay categories", 25, -0.5, 24.5);

                h_n_matched_genparticles = book<TH1F>("matched_genparticles", "number matched genparticles", 10, 0., 10.);

                genp_printer.reset(new GenParticlesPrinter(ctx));
            }

        void fill(const uhh2::Event & event) {
            double w = event.weight;
            if (event.is_valid(hndl_in_)) {
                vector<T> const & coll = event.get(hndl_in_);
                if (coll.size()) {
                    genp_printer->process(event);

                    T const & ld_part = coll[0];

                    cout << "\nLEADING TAGGED PARTICLE E/PT/ETA/PHI: " << ld_part.energy() << " "
                         << ld_part.pt() << " " << ld_part.eta() << " " << ld_part.phi() << "\n\n"; 
                    vector<GenParticle> matched_genparticles;
                    for (GenParticle const & genp : *event.genparticles) {
                        if (deltaR(ld_part, genp) < dr_) {
                            matched_genparticles.push_back(genp);
                        }
                    }
                    h_n_matched_genparticles->Fill(matched_genparticles.size(), w);
                    if (matched_genparticles.size()) {
                        h_ind_sort_id_1->Fill(matched_genparticles[0].pdgId(), w);
                        h_ind_sort_dr_1->Fill(deltaR(matched_genparticles[0], ld_part), w);
                        h_ind_sort_dptrel_1->Fill((matched_genparticles[0].pt()-ld_part.pt())/ld_part.pt(), w);

                        if (matched_genparticles.size() > 1) {
                            h_ind_sort_id_2->Fill(matched_genparticles[1].pdgId(), w);
                            h_ind_sort_dr_2->Fill(deltaR(matched_genparticles[1], ld_part), w);
                            h_ind_sort_dptrel_2->Fill((matched_genparticles[1].pt()-ld_part.pt())/ld_part.pt(), w);
                            if (matched_genparticles.size() > 2) {
                                h_ind_sort_id_3->Fill(matched_genparticles[2].pdgId(), w);
                                h_ind_sort_dr_3->Fill(deltaR(matched_genparticles[2], ld_part), w);
                                h_ind_sort_dptrel_3->Fill((matched_genparticles[2].pt()-ld_part.pt())/ld_part.pt(), w);
                            }
                        }
                    }
                    std::sort(matched_genparticles.begin(), matched_genparticles.end(), [&](const GenParticle & p1, const GenParticle & p2){
                        return deltaR(p1, ld_part) < deltaR(p2, ld_part);});
                    if (matched_genparticles.size()) {
                        h_dr_sort_id_1->Fill(matched_genparticles[0].pdgId(), w);
                        h_dr_sort_dr_1->Fill(deltaR(matched_genparticles[0], ld_part), w);
                        h_dr_sort_dptrel_1->Fill((matched_genparticles[0].pt()-ld_part.pt())/ld_part.pt(), w);

                        if (matched_genparticles.size() > 1) {
                            h_dr_sort_id_2->Fill(matched_genparticles[1].pdgId(), w);
                            h_dr_sort_dr_2->Fill(deltaR(matched_genparticles[1], ld_part), w);
                            h_dr_sort_dptrel_2->Fill((matched_genparticles[1].pt()-ld_part.pt())/ld_part.pt(), w);
                            if (matched_genparticles.size() > 2) {
                                h_dr_sort_id_3->Fill(matched_genparticles[2].pdgId(), w);
                                h_dr_sort_dr_3->Fill(deltaR(matched_genparticles[2], ld_part), w);
                                h_dr_sort_dptrel_3->Fill((matched_genparticles[2].pt()-ld_part.pt())/ld_part.pt(), w);
                            }
                        }
                    }
                    std::sort(matched_genparticles.begin(), matched_genparticles.end(), [&](const GenParticle & p1, const GenParticle & p2){
                        return abs(p1.pt()-ld_part.pt()/ld_part.pt()) < abs(p2.pt()-ld_part.pt()/ld_part.pt());});
                    if (matched_genparticles.size()) {
                        h_pt_sort_id_1->Fill(matched_genparticles[0].pdgId(), w);
                        h_pt_sort_dr_1->Fill(deltaR(matched_genparticles[0], ld_part), w);
                        h_pt_sort_dptrel_1->Fill((matched_genparticles[0].pt()-ld_part.pt())/ld_part.pt(), w);

                        if (matched_genparticles.size() > 1) {
                            h_pt_sort_id_2->Fill(matched_genparticles[1].pdgId(), w);
                            h_pt_sort_dr_2->Fill(deltaR(matched_genparticles[1], ld_part), w);
                            h_pt_sort_dptrel_2->Fill((matched_genparticles[1].pt()-ld_part.pt())/ld_part.pt(), w);
                            if (matched_genparticles.size() > 2) {
                                h_pt_sort_id_3->Fill(matched_genparticles[2].pdgId(), w);
                                h_pt_sort_dr_3->Fill(deltaR(matched_genparticles[2], ld_part), w);
                                h_pt_sort_dptrel_3->Fill((matched_genparticles[2].pt()-ld_part.pt())/ld_part.pt(), w);
                            }
                        }
                    }

                    int n_tops = 0;
                    int n_had_w = 0;
                    int n_lep_w = 0;
                    int n_b_from_top = 0;
                    int n_b_from_w = 0;
                    int n_b_from_g = 0;
                    int n_lq_from_w = 0;
                    int n_lq_from_g = 0;
                    int n_g_to_hq = 0;
                    int n_g_to_lq = 0;
                    int n_lep = 0;
                    int n_other = 0;
                    int n_weird_decay = 0;

                    for (auto const & matched_part : matched_genparticles) {
                        if (abs(matched_part.pdgId()) == 6 )
                            n_tops++;
                        else if (abs(matched_part.pdgId()) == 24) {
                            GenParticle const *daughter1 = matched_part.daughter(event.genparticles, 1);
                            if (daughter1) {
                                if (daughter1->pdgId() > 10 && daughter1->pdgId() < 17)
                                    n_lep_w++;
                                else
                                    n_had_w++;
                            }
                            else {n_weird_decay++;}
                        }
                        else if (abs(matched_part.pdgId()) == 5) {
                            GenParticle const *mother = findMother(matched_part, event.genparticles);
                            if (mother) {
                                if (abs(mother->pdgId()) == 6)
                                    n_b_from_top++;
                                else if (abs(mother->pdgId()) == 24)
                                    n_b_from_w++;
                                else if (abs(mother->pdgId()) == 21)
                                    n_b_from_g++;
                                else {n_weird_decay++;}
                            }
                            else {n_weird_decay++;}
                        }
                        else if (abs(matched_part.pdgId()) < 5) {
                            GenParticle const *mother = findMother(matched_part, event.genparticles);
                            if (mother) {
                                if (abs(mother->pdgId()) == 24)
                                    n_lq_from_w++;
                                else if (abs(mother->pdgId()) == 21)
                                    n_lq_from_g++;
                                else {n_weird_decay++;}
                            }
                            else {n_weird_decay++;}
                        }
                        else if (abs(matched_part.pdgId()) > 10 && abs(matched_part.pdgId()) < 17)
                            n_lep++;
                        else if (abs(matched_part.pdgId()) == 21) {
                            GenParticle const *daughter1 = matched_part.daughter(event.genparticles, 1);
                            if (daughter1) {
                                if (daughter1->pdgId() == 5 || daughter1->pdgId() == 4)
                                    n_g_to_hq++;
                                else if (daughter1->pdgId() < 4)
                                    n_g_to_lq++;
                                else {n_weird_decay++;}
                            }
                            else {n_weird_decay++;}
                        }
                        else {n_other++;}
                    }

                    int category = 0;
                    if (n_tops == 1) {
                        category = 0;
                        if (n_had_w == 1 && !n_lep_w) {
                            category += 0;
                        }
                        else if (n_lep_w == 1 && !n_had_w) {
                            category += 4;
                        }
                        else if (!n_had_w && !n_lep_w) {
                            category += 8;
                        }
                        else {
                            category = 24;
                        }

                        if (n_b_from_top == 0) {
                            category += 0;
                        }
                        else if (n_b_from_top == 1) {
                            category += 2;
                        }
                        else {
                            category = 24;
                        }

                        if (n_g_to_hq == 0) {
                            category += 0;
                        }
                        else {
                            category += 1;
                        }
                    } 
                    else if (n_tops == 0) {
                        category = 12;
                        if (n_had_w == 1 && !n_lep_w) {
                            category += 0;
                        }
                        else if (n_lep_w == 1 && !n_had_w) {
                            category += 4;
                        }
                        else if (!n_had_w && !n_lep_w) {
                            category += 8;
                        }
                        else {
                            category = 24;
                        }

                        if (n_b_from_top == 0) {
                            category += 0;
                        }
                        else if (n_b_from_top == 1) {
                            category += 2;
                        }
                        else {
                            category = 24;
                        }

                        if (n_g_to_hq == 0) {
                            category += 0;
                        }
                        else {
                            category += 1;
                        }
                    }
                    else {category = 24;}

                    h_categories->Fill(category, w);
                }
            }
        }

        virtual ~GenHistColl() {
        }

    private:
        Event::Handle<vector<T>> hndl_in_;
        float dr_;
        // TH1F *h_pt, *h_eta, *h_phi, *h_n, *h_mass, *h_charge;
        TH1F *h_ind_sort_id_1, *h_ind_sort_id_2, *h_ind_sort_id_3;
        TH1F *h_ind_sort_dr_1, *h_ind_sort_dr_2, *h_ind_sort_dr_3;
        TH1F *h_ind_sort_dptrel_1, *h_ind_sort_dptrel_2, *h_ind_sort_dptrel_3;
        TH1F *h_dr_sort_id_1, *h_dr_sort_id_2, *h_dr_sort_id_3;
        TH1F *h_dr_sort_dr_1, *h_dr_sort_dr_2, *h_dr_sort_dr_3;
        TH1F *h_dr_sort_dptrel_1, *h_dr_sort_dptrel_2, *h_dr_sort_dptrel_3;
        TH1F *h_pt_sort_id_1, *h_pt_sort_id_2, *h_pt_sort_id_3;
        TH1F *h_pt_sort_dr_1, *h_pt_sort_dr_2, *h_pt_sort_dr_3;
        TH1F *h_pt_sort_dptrel_1, *h_pt_sort_dptrel_2, *h_pt_sort_dptrel_3;
        // TH1F *h_decay_1, *h_decay_2;
        // TH1F *h_mother_1, *h_mother_2;
        TH1F *h_categories;
        TH1F *h_n_matched_genparticles;
        // boost::optional<GenParticleId> genp_id;
        unique_ptr<GenParticlesPrinter> genp_printer;
    };

    string dirname_;

    // static std::map<int, std::pair<float, float> > minmax_pts_;
    // static std::map<int, std::pair<float, float> > minmax_masses_;

    std::vector<unique_ptr<GenHistColl>> all_hists_;

  // TH1F *spec_parton_ht, *spec_deltaR_bb_h, *spec_deltaR_bb_min, *spec_max_deltaR_topprod;
  // TH2F *spec_top_pt_vs_max_dR;
};