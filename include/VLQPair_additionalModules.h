#pragma once

#include <iostream>
#include <vector>

#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Event.h"

#include "UHH2/common/include/TTbarReconstruction.h"
#include "UHH2/common/include/Utils.h"

using namespace std;
using namespace uhh2;

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


class GenParticlePdgId
{
public:
    GenParticlePdgId(const std::vector<int> & pdgids) :
        pdgids_(pdgids)
        {}

    bool operator()(const GenParticle & genp, const Event & event) const
    {
        for (int id : pdgids_) {
            if (genp.pdgId() == id)
            {
                return true;
            }
        }

        // cout << "  Found right mother!\n";
        return false;
    }

private:
    std::vector<int> pdgids_;
};



