#pragma once

#include "UHH2/core/include/Hists.h"
#include "UHH2/core/include/Event.h"
#include "UHH2/core/include/GenParticle.h"
#include "UHH2/common/include/JetIds.h"
// #include "UHH2/common/include/PrintingModules.h"

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

                // genp_printer.reset(new GenParticlesPrinter(ctx));
            }

        void fill(const uhh2::Event & event) {
            double w = event.weight;
            if (event.is_valid(hndl_in_)) {
                vector<T> const & coll = event.get(hndl_in_);
                if (coll.size()) {
                    // genp_printer->process(event);

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
        // unique_ptr<GenParticlesPrinter> genp_printer;
    };

    string dirname_;

    // static std::map<int, std::pair<float, float> > minmax_pts_;
    // static std::map<int, std::pair<float, float> > minmax_masses_;

    std::vector<unique_ptr<GenHistColl>> all_hists_;

  // TH1F *spec_parton_ht, *spec_deltaR_bb_h, *spec_deltaR_bb_min, *spec_max_deltaR_topprod;
  // TH2F *spec_top_pt_vs_max_dR;
};


template<typename T>
class NParticleMultiHistProducer : public Hists {
public:

    explicit NParticleMultiHistProducer(Context & ctx,
                        const string & dirname,
                        const string & h_in,
                        const vector<string> & variables = {"n", "pt", "eta", "phi"},
                        unsigned part_ind = 1) :
        Hists(ctx, dirname),
        h_in_(ctx.get_handle<vector<T>>(h_in)),
        part_ind_(part_ind)
        {
            for (string const & var : variables) {
                if (var == "n") hists_[var] = book<TH1F>("n_"+h_in, "n", 10, -.5, 9.5);
                if (var == "n_subjets") hists_[var] = book<TH1F>("n_subjets_"+h_in, "n_subjets", 10, -.5, 9.5);
                if (var == "pt") hists_[var] = book<TH1F>("pt_"+h_in, "pt", 60, 0., 1500.);
                if (var == "eta") hists_[var] = book<TH1F>("eta_"+h_in, "eta", 50, -3., 3.);
                if (var == "phi") hists_[var] = book<TH1F>("phi_"+h_in, "phi", 50, -3.14, 3.14);
                if (var == "mass") hists_[var] = book<TH1F>("mass_"+h_in, "mass", 60, 0., 300.);
                if (var == "mass_sj") hists_[var] = book<TH1F>("mass_sj_"+h_in, "mass sj", 60, 0., 300.);
                if (var == "tau21") hists_[var] = book<TH1F>("tau21_"+h_in, "tau21", 50, 0., 1.);
                if (var == "tau32") hists_[var] = book<TH1F>("tau32_"+h_in, "tau32", 50, 0., 1.);
                if (var == "csv_first_sj") hists_[var] = book<TH1F>("csv_first_sj_"+h_in, "csv_first_sj", 50, 0., 1.);
                if (var == "csv_second_sj") hists_[var] = book<TH1F>("csv_second_sj_"+h_in, "csv_second_sj", 50, 0., 1.);
                if (split(var, "-")[0] == "n_sjbtags") hists_[var] = book<TH1F>("n_sjbtags_"+h_in+"_"+split(var, "-")[1], "N sjbtags "+split(var, "-")[1], 5, -.5, 4.5);
            }  
        }

    virtual void fill(Event const & event) override {
        bool is_topjet = std::is_same<T, TopJet>::value;
        double w = event.weight;
        // double w = 1.;
        if (!event.is_valid(h_in_)) {
            cout << "WARNING: handle in NParticleMultiHistProducer not valid!\n";
            return;
        }
        vector<T> const & coll = event.get(h_in_);
        for (map<string, TH1F*>::const_iterator it = hists_.begin(); it != hists_.end(); ++it) {
            if (it->first == "n") it->second->Fill(coll.size(), w);
            if (coll.size() >= part_ind_) {
                T const & particle = coll[part_ind_-1];
                if (it->first == "pt") it->second->Fill(particle.pt(), w);
                if (it->first == "eta") it->second->Fill(particle.eta(), w);
                if (it->first == "phi") it->second->Fill(particle.phi(), w);
                if (it->first == "mass") it->second->Fill(particle.v4().M(), w);
                if (it->first == "n_subjets") {
                        // assert(false);
                    assert(is_topjet);
                    it->second->Fill(particle.subjets().size());
                };
                if (it->first == "mass_sj") {
                        // assert(false);
                    assert(is_topjet);
                    if (particle.subjets().size()){
                        LorentzVector sum_subjets;
                        for (Jet const & subjet : particle.subjets())
                            sum_subjets += subjet.v4();
                        it->second->Fill(sum_subjets.M(), w);
                    } else {
                        it->second->Fill(-1., w);
                    }
                };
                if (it->first == "tau21") {
                    assert(is_topjet);
                    it->second->Fill(particle.tau2()/particle.tau1(), w);
                }
                if (it->first == "tau32") {
                    assert(is_topjet);
                    it->second->Fill(particle.tau3()/particle.tau2(), w);
                }
                if (it->first == "csv_first_sj") {
                    assert(is_topjet);
                    if (particle.subjets().size() >= 1){
                        it->second->Fill(particle.subjets()[0].btag_combinedSecondaryVertex(), w);
                    } else {
                        it->second->Fill(-1., w);
                    }
                }
                if (it->first == "csv_second_sj") {
                    assert(is_topjet);
                    if (particle.subjets().size() >= 2){
                        it->second->Fill(particle.subjets()[1].btag_combinedSecondaryVertex(), w);
                    } else {
                        it->second->Fill(-1., w);
                    }
                }
                if (split(it->first, "-")[0] == "n_sjbtags") {
                    CSVBTag::wp wp_;
                    if (split(it->first, "-")[1] == "loose")
                        wp_ = CSVBTag::WP_LOOSE;
                    else if (split(it->first, "-")[1] == "tight")
                        wp_ = CSVBTag::WP_TIGHT;
                    else
                        wp_ = CSVBTag::WP_MEDIUM;
                    CSVBTag btag_(wp_);
                    int n_sj = 0;
                    for (auto const & sj : particle.subjets()) {
                        if (btag_(sj, event))
                            n_sj++;
                    }
                    it->second->Fill(n_sj, w);
                }
            }
        }

        for (auto sub_hist : sub_hists_)
            sub_hist->fill(event);
    }

    // template<TYPE> void fill_dr_hist(T const & part, const string & coll, Hists * hist) {
    //     float min_dr = -1.;
    //     if (e.is_valid(h_p1_) && e.is_valid(h_p2_)) {
    //         const T & ref_part = e.get(h_p1_);
    //         const vector<TYPE> & comp_parts = e.get(h_p2_);

    //         double deltarmin = std::numeric_limits<double>::infinity();
    //         const TYPE* closest_part=0;
    //         for(unsigned int i=0; i<comp_parts.size(); ++i) {
    //             const TYPE & pi = comp_parts[i];
    //             double dr = uhh2::deltaR(pi, ref_part);
    //             if(dr < deltarmin) {
    //                 deltarmin = dr;
    //                 closest_part = &pi;
    //             }
    //         }

    //         if (closest_part) {
    //             min_dr = uhh2::deltaR(ref_part, *closest_part);
    //         }

    //     }
    // }


    void set_subhists(Hists * sub_hist) {
        sub_hists_.emplace_back(sub_hist);
    }


private:
    Event::Handle<vector<T>> h_in_;
    unsigned part_ind_;
    map<string, TH1F*> hists_;
    vector<shared_ptr<Hists>> sub_hists_;
};


template<typename T>
class NParticleMultiHistProducerHelper {
public:
    explicit NParticleMultiHistProducerHelper(
                        const string & rel_dirname,
                        const string & h_name,
                        const vector<string> & variables = {"n", "pt", "eta", "phi", "mass_sj", "csv_first_sj", "csv_second_sj", "n_subjets"},
                        unsigned part_ind = 1) :
        rel_dirname_(rel_dirname),
        h_name_(h_name),
        variables_(variables),
        part_ind_(part_ind) {
        }

    // ~NParticleMultiHistProducerHelper() {
    //     cout << "destroying dir " << rel_dirname_ << " for handle " << h_name_ << endl;
    // }

    void add_level(const string & rel_dirname,
                    const string & h_name,
                    const vector<string> & variables = {"n", "pt", "eta", "phi", "mass_sj", "csv_first_sj", "csv_second_sj", "n_subjets"},
                    unsigned part_ind = 1) {
        sub_levels_.emplace_back(rel_dirname, h_name, variables, part_ind);
        indizes_[rel_dirname] = sub_levels_.size()-1;
        // return &sub_levels_.end()-1;
    }

    NParticleMultiHistProducer<T>* book_histograms(Context & ctx, const string & dirname) const {
        NParticleMultiHistProducer<T> * new_hist = new NParticleMultiHistProducer<T>(ctx, dirname+"/"+rel_dirname_,
            h_name_, variables_, part_ind_);
        for (auto const & sub_level : sub_levels_)
            new_hist->set_subhists(sub_level.book_histograms(ctx, dirname+"/"+rel_dirname_));
        return new_hist;
    }

    NParticleMultiHistProducerHelper<T> & operator[](const string & rel_dirname) {
        unsigned ind = indizes_[rel_dirname];
        return sub_levels_[ind];
    }

    NParticleMultiHistProducerHelper<T> & back() {
        unsigned ind = sub_levels_.size()-1;
        return sub_levels_[ind];
    }

    // vector<NParticleMultiHistProducerHelper<T>> const & get_sublevels() const {
    //     return sub_levels_;
    // }

    void print_name() {
        cout << "rel_dirname_: " << rel_dirname_ << " h_name_: " << h_name_ << " address: " << this << endl;
    }

private:
    string rel_dirname_;
    string h_name_;
    vector<string> variables_;
    std::map<string, unsigned> indizes_;
    vector<NParticleMultiHistProducerHelper<T>> sub_levels_;
    unsigned part_ind_;
};

class OwnHistCollector : public uhh2::Hists {
public:
    OwnHistCollector(Context & ctx, const string & dirname, bool gen_plots = false, JetId const & btag_id = CSVBTag(CSVBTag::WP_LOOSE)) :
    Hists(ctx, dirname),
    lumi_hist(new LuminosityHists(ctx, dirname+"/LuminosityHists")),
    // el_hists(new ExtendedElectronHists(ctx, dirname+"/ElectronHists", gen_plots)),
    mu_hists(new ExtendedMuonHists(ctx, dirname+"/MuonHists", gen_plots)),
    // tau_hists(new TauHists(ctx, dirname+"/TauHists")),
    ev_hists(new ExtendedEventHists(ctx, dirname+"/EventHists", "n_btags_medium")),
    jet_hists(new ExtendedJetHists(ctx, dirname+"/JetHists", 3)),
    // cmstopjet_hists(new ExtendedTopJetHists(ctx, dirname+"/CMSTopJetHists", btag_id, 4)),
    // heptopjet_hists(new ExtendedTopJetHists(ctx, dirname+"/HEPTopJetHists", btag_id, 4, "patJetsHepTopTagCHSPacked_daughters")),
    ak8softdroptopjet_hists(new ExtendedTopJetHists(ctx, dirname+"/Ak8SoftDropTopJetHists", btag_id, 3, "patJetsAk8CHSJetsSoftDropPacked_daughters"))
    // ca15filteredtopjet_hists(new ExtendedTopJetHists(ctx, dirname+"/CA15FilteredTopJetHists", btag_id, 4, "patJetsCa15CHSJetsFilteredPacked_daughters")),
    // gen_hists(gen_plots ? new CustomizableGenHists(ctx, dirname+"/GenHists", "parton_ht") : NULL)
    {
        // if (gen_hists)
        // {
        //     gen_hists->add_genhistcoll(8000001, 1, true, true, true, true);
        //     gen_hists->add_genhistcoll(8000001, 2, true, true, true, true);
        //     gen_hists->add_genhistcoll(6, 1, true, true, true, true);
        //     gen_hists->add_genhistcoll(6, 2, true, true, true, true);
        //     gen_hists->add_genhistcoll(25, 1, true, true, true, true);
        //     gen_hists->add_genhistcoll(25, 2, true, true, true, true);
        //     gen_hists->add_genhistcoll(0, 0);
        //     // gen_hists->add_genhistcoll(0, 1);
        //     // gen_hists->add_genhistcoll(0, 2);
        //     gen_hists->add_genhistcoll(11, 1, false, true, false, false, GenParticleId(GenParticleMotherId(6)), "_from_top");
        //     gen_hists->add_genhistcoll(11, 2, false, true, false, false, GenParticleId(GenParticleMotherId(6)), "_from_top");
        //     gen_hists->add_genhistcoll(13, 1, false, true, false, false, GenParticleId(GenParticleMotherId(6)), "_from_top");
        //     gen_hists->add_genhistcoll(13, 2, false, true, false, false, GenParticleId(GenParticleMotherId(6)), "_from_top");
        //     gen_hists->add_genhistcoll(11, 1, false, true, false, false, GenParticleId(AndId<GenParticle>(GenParticleMotherId(24,6),GenParticleMotherId(24,25))), "_from_tpW");
        //     gen_hists->add_genhistcoll(11, 2, false, true, false, false, GenParticleId(AndId<GenParticle>(GenParticleMotherId(24,6),GenParticleMotherId(24,25))), "_from_tpW");
        //     gen_hists->add_genhistcoll(13, 1, false, true, false, false, GenParticleId(AndId<GenParticle>(GenParticleMotherId(24,6),GenParticleMotherId(24,25))), "_from_tpW");
        //     gen_hists->add_genhistcoll(13, 2, false, true, false, false, GenParticleId(AndId<GenParticle>(GenParticleMotherId(24,6),GenParticleMotherId(24,25))), "_from_tpW");

        // }
    } 

    virtual void fill(const Event & event) {
        lumi_hist->fill(event);
        // el_hists->fill(event);
        mu_hists->fill(event);
    // tau_hists->fill(event);
        ev_hists->fill(event);
        jet_hists->fill(event);
    // cmstopjet_hists->fill(event);
    // heptopjet_hists->fill(event);
    ak8softdroptopjet_hists->fill(event);
    // ca15filteredtopjet_hists->fill(event);
    // if (gen_hists) gen_hists->fill(event);
    }

    ~OwnHistCollector(){
        delete lumi_hist;
        // delete el_hists;
        delete mu_hists;
    // delete tau_hists;
        delete ev_hists;
        delete jet_hists;
    // delete cmstopjet_hists;
    // delete heptopjet_hists;
    delete ak8softdroptopjet_hists;
    // delete ca15filteredtopjet_hists;
    // delete gen_hists;
    }

private:
    LuminosityHists * lumi_hist;
    // ExtendedElectronHists * el_hists;
    ExtendedMuonHists * mu_hists;
    // TauHists * tau_hists;
    ExtendedEventHists * ev_hists;
    ExtendedJetHists * jet_hists;
    // ExtendedTopJetHists * cmstopjet_hists;
    // ExtendedTopJetHists * heptopjet_hists;
    ExtendedTopJetHists * ak8softdroptopjet_hists;
    // ExtendedTopJetHists * ca15filteredtopjet_hists;
    // CustomizableGenHists * gen_hists;
};