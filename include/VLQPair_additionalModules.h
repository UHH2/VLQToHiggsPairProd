#pragma once

#include <iostream>
#include <vector>

#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Event.h"

#include "UHH2/common/include/TTbarReconstruction.h"
#include "UHH2/common/include/Utils.h"

using namespace std;
using namespace uhh2;

namespace vlqToHiggsPair {

inline void make_modules_and_selitem(const string & name, Context & ctx, vector<unique_ptr<AnalysisModule>> & modules,
                              vector<shared_ptr<SelectionItem>> & sel_items, unsigned pos_cut,
                              int cut_min=-999., int cut_max=999.) {
    modules.emplace_back(new CollectionSizeProducer<TopJet>(ctx,
                name,
                "n_"+name
                ));
    modules.emplace_back(new LeadingPartMassProducer<TopJet>(ctx,
                name,
                "mass_ld_"+name
                ));
    modules.emplace_back(new LeadingTopjetMassProducer(ctx,
                name,
                "mass_sj_ld_"+name
                ));
    modules.emplace_back(new LeadingTopjetNSubjettinessProducer(ctx,
                name,
                "tau21_ld_"+name
                ));
    modules.emplace_back(new LeadingTopjetNSubjettinessProducer(ctx,
                name,
                "tau32_ld_"+name,
                false
                ));
    modules.emplace_back(new PartPtProducer<TopJet>(ctx,
                name,
                "pt_ld_"+name,
                1));
    sel_items.insert(sel_items.begin()+pos_cut, 
            shared_ptr<SelectionItem>(new SelDatI("n_"+name, "N_"+name, 11, -.5, 10.5,
                cut_min, cut_max)));
    sel_items.insert(sel_items.begin()+pos_cut, 
            shared_ptr<SelectionItem>(new SelDatF("mass_ld_"+name, "Mass_leading_"+name, 60, 0., 300.)));
    sel_items.insert(sel_items.begin()+pos_cut, 
            shared_ptr<SelectionItem>(new SelDatF("mass_sj_ld_"+name, "Mass_subjets_leading_"+name, 60, 0., 300.)));
    sel_items.insert(sel_items.begin()+pos_cut, 
            shared_ptr<SelectionItem>(new SelDatF("tau21_ld_"+name, "Tau21_leading_"+name, 50, 0., 1.)));
    sel_items.insert(sel_items.begin()+pos_cut, 
            shared_ptr<SelectionItem>(new SelDatF("tau32_ld_"+name, "Tau32_leading_"+name, 50, 0., 1.)));
    sel_items.insert(sel_items.begin()+pos_cut, 
            shared_ptr<SelectionItem>(new SelDatF("pt_ld_"+name, "Pt_leading_"+name, 15, 0., 1500.)));
}

}

class NeutrinoParticleProducer: public AnalysisModule {
public:
    explicit NeutrinoParticleProducer(Context & ctx,
                            const NeutrinoReconstructionMethod & neutrinofunc,
                            const string & h_out = "neutrino_part_vec",
                            const string & h_primlep = "PrimaryLepton") :
        neutrinofunc_(neutrinofunc),
        h_out_(ctx.get_handle<vector<LorentzVector>>(h_out)),
        h_primlep_(ctx.get_handle<FlavorParticle>(h_primlep)) {}

    virtual bool process(Event & event) override {
        assert(event.jets);
        assert(event.met);
        
        if (!event.is_valid(h_primlep_)) {
            return false;
        }
        const Particle & lepton = event.get(h_primlep_);
        vector<LorentzVector> neutrino_hyps = neutrinofunc_(lepton.v4(), event.met->v4());
        // vector<FlavorParticle> neutrino_parts;
        // for (LorentzVector const & i_v4 : neutrino_hyps) {
        //     FlavorParticle neutrino_part;
        //     neutrino_part.set_v4(i_v4);
        //     neutrino_part.set_pdgId(12); // set to dummy value of electron neutrino, not important anyway
        //     neutrino_parts.push_back(neutrino_part); 
        // }

        event.set(h_out_, neutrino_hyps);

        return true;
    }

private:
    NeutrinoReconstructionMethod neutrinofunc_;
    Event::Handle<vector<LorentzVector>> h_out_;
    Event::Handle<FlavorParticle> h_primlep_;
};


template<typename TYPE1, typename TYPE2>
class MinDeltaRProducer: public AnalysisModule {
public:
    explicit MinDeltaRProducer(Context & ctx,
                            const string & h_p1,
                            const string & h_p2,
                            const string & h_out) :
        h_p1_(ctx.get_handle<TYPE1>(h_p1)),
        h_p2_(ctx.get_handle<vector<TYPE2>>(h_p2)),
        h_out_(ctx.get_handle<float>(h_out)) {}

    virtual bool process(Event & e) override {
        float min_dr = -1.;
        if (e.is_valid(h_p1_) && e.is_valid(h_p2_)) {
            const TYPE1 & ref_part = e.get(h_p1_);
            const vector<TYPE2> & comp_parts = e.get(h_p2_);

            double deltarmin = std::numeric_limits<double>::infinity();
            const TYPE2* closest_part=0;
            for(unsigned int i=0; i<comp_parts.size(); ++i) {
                const TYPE2 & pi = comp_parts[i];
                double dr = uhh2::deltaR(pi, ref_part);
                if(dr < deltarmin) {
                    deltarmin = dr;
                    closest_part = &pi;
                }
            }

            if (closest_part) {
                min_dr = uhh2::deltaR(ref_part, *closest_part);
            }
            
        }

        e.set(h_out_, min_dr);

        return true;
    }

private:
    Event::Handle<TYPE1> h_p1_;
    Event::Handle<vector<TYPE2>> h_p2_;
    Event::Handle<float> h_out_;
};

template<typename T>
class TwoParticleCollectionProducer: public AnalysisModule {
public:
    explicit TwoParticleCollectionProducer(Context & ctx,
                            const string & h_in,
                            const string & h_out):
        h_in_(ctx.get_handle<vector<T>>(h_in)),
        h_out_(ctx.get_handle<vector<T>>(h_out)) {}

    virtual bool process(Event & event) override {
        
        if (!event.is_valid(h_in_)) {
            return false;
        }
        const vector<T> & in_coll = event.get(h_in_);
        if (in_coll.size() > 1) {
            vector<T> out_coll = {in_coll[0], in_coll[1]};

            event.set(h_out_, out_coll);

            return true;
        } else {
            return false;
        }
    }

private:
    Event::Handle<vector<T>> h_in_;
    Event::Handle<vector<T>> h_out_;
};


template<typename T>
class DeltaRTwoLeadingParticleProducer: public AnalysisModule {
public:
    explicit DeltaRTwoLeadingParticleProducer(Context & ctx,
                            const string & h_in,
                            const string & h_dr) :
        h_in_(ctx.get_handle<vector<T>>(h_in)),
        h_dr_(ctx.get_handle<float>(h_dr)) {}

    virtual bool process(Event & e) override {
        if (e.is_valid(h_in_)) {
            const vector<T> & parts = e.get(h_in_);

            if (parts.size() > 1) {
                float dr = deltaR(parts[0], parts[1]);
                e.set(h_dr_, dr);

                return true;
            }  
            
        }

        e.set(h_dr_, -1.);

        return false;

    }

private:
    Event::Handle<vector<T>> h_in_;
    Event::Handle<float> h_dr_;
};


class XTopTagProducer: public AnalysisModule {
public:
    explicit XTopTagProducer(Context & ctx,
                               const string & h_in,
                               const string & h_dr_out,
                               const string & h_x_top_out,
                               float dr_higgs = 1.5,
                               unsigned number_top = 1):
        h_in_(ctx.get_handle<vector<TopJet>>(h_in)),
        h_dr_out_(ctx.get_handle<float>(h_dr_out)),
        h_x_top_out_(ctx.get_handle<TopJet>(h_x_top_out)),
        dr_higgs_(dr_higgs),
        number_top_(number_top) {}

    virtual bool process(Event & event) override {
        float dyn_dr_higgs = -999.;
        if (event.is_valid(h_in_)) {
            const vector<TopJet> & topjet_coll = event.get(h_in_);
            if (topjet_coll.size() == number_top_) {
                dyn_dr_higgs = dr_higgs_;
                event.set(h_x_top_out_, topjet_coll[0]);
            }
        }
        // std::cout << dyn_dr_higgs << std::endl;
        event.set(h_dr_out_, dyn_dr_higgs);

        return true;
    }

private:
    Event::Handle<std::vector<TopJet>> h_in_;
    Event::Handle<float> h_dr_out_;
    Event::Handle<TopJet> h_x_top_out_;
    float dr_higgs_;
    unsigned number_top_;
};


// template<typename TYPE>
// class SizeOneId
// {
// public:
//     SizeOneId(Context & ctx,
//                 const string & h_comp_coll,
//                 bool size_equal_one = true) :
//         h_comp_coll_(ctx.get_handle<vector<TYPE>>(h_comp_coll)),
//         size_equal_one_(size_equal_one)
//         {}

//     bool operator()(const Particle & part, const Event & event) const
//     {
//         if (event.is_valid(h_comp_coll_)){
//             const vector<TYPE> & comp_coll = event.get(h_comp_coll_);
//             if (size_equal_one_ ? comp_coll.size() == 1 : comp_coll.size() > 1)
//                 return true;
//             else return false;
//         }

//         std::cout << "WARNING: in SizeOneId: handle to h_comp_coll_ is not valid!\n";
//         return true;
//     }

// private:
//     Event::Handle<vector<TYPE>> h_comp_coll_;
//     bool size_equal_one_;
// };
