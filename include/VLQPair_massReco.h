#pragma once

#include <algorithm>

#include "TVector3.h"

#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Event.h"
#include "UHH2/core/include/Utils.h"

#include "UHH2/common/include/TTbarReconstruction.h"

class TPrimeMassProducer: public AnalysisModule {
public:

    explicit TPrimeMassProducer(Context & ctx,
                                std::string const & h_htags,
                                std::string const & h_tops,
                                // std::string const & h_primlep,
                                float min_dR,
                                std::string const & h_out
                                ) :
        h_htags_(ctx.get_handle<std::vector<TopJet>>(h_htags)),
        h_tops_(ctx.get_handle<std::vector<TopJet>>(h_tops)),
        min_dR_(min_dR),
        // h_primlep_(ctx.get_handle<FlavorParticle>(h_primlep)),
        h_mHLep_(ctx.declare_event_output<float>(h_out+"_mass_HLep")),
        h_mHtop_(ctx.declare_event_output<float>(h_out+"_mass_Htop")),
        h_mMax_(ctx.declare_event_output<float>(h_out+"_mass_Max")),
        h_mMin_(ctx.declare_event_output<float>(h_out+"_mass_Min")) {}

    bool process(Event & event) override {
        if (!event.is_valid(h_htags_) || !event.is_valid(h_tops_)) {
            std::cout << "Error in TPrimeMassProducer: input handle not valid!\n";
            assert(false);
        }
        float hlep_mass = -1.;
        float htop_mass = -1.;
        float max_mass = -1.;
        float min_mass = -1.;
        vector<TopJet> const & htags = event.get(h_htags_);
        if (htags.size()) {
            TopJet const & ld_htag = htags[0];

            vector<TopJet> const & htops = event.get(h_tops_);
            assert(event.muons || event.electrons);
            double ptmax = -infinity;
            Particle const * primlep = nullptr;
            if(event.electrons) {
                for(auto const & ele : *event.electrons) {
                    float ele_pt = ele.pt();
                    if(ele_pt > ptmax && uhh2::deltaR(ele, ld_htag) > min_dR_) {
                        ptmax = ele_pt;
                        primlep = &ele;
                    }
                }
            }
            if(event.muons) {
                for(auto const & mu : *event.muons) {
                    float mu_pt = mu.pt();
                    if(mu_pt > ptmax && uhh2::deltaR(mu, ld_htag) > min_dR_) {
                        ptmax = mu_pt;
                        primlep = &mu;
                    }
                }
            }
            if (primlep) {
                LorentzVector htag_lep = ld_htag.v4() + primlep->v4();
                hlep_mass = htag_lep.M();
            }
            if (htops.size()) {
                TopJet const * ld_top = nullptr;
                for (auto const & tj : htops) {
                    if (uhh2::deltaR(tj, ld_htag) > min_dR_) {
                        ld_top = &tj;
                        break;
                    }
                }
                if (ld_top) {
                    LorentzVector htag_had = ld_htag.v4() + ld_top->v4();
                    htop_mass = htag_had.M();
                }
            }
            if (htop_mass > 0. && hlep_mass > 0.) {
                min_mass = std::min(hlep_mass, htop_mass);
                max_mass = std::max(hlep_mass, htop_mass);
            }
            else if (hlep_mass > 0.) {
                min_mass = hlep_mass;
                max_mass = hlep_mass;
            }
            else {
                min_mass = htop_mass;
                max_mass = htop_mass;
            }
        }
        event.set(h_mHLep_, hlep_mass);
        event.set(h_mHtop_, htop_mass);
        event.set(h_mMax_, max_mass);
        event.set(h_mMin_, min_mass);
        return true;

    }

private:
    uhh2::Event::Handle<std::vector<TopJet>> h_htags_;
    uhh2::Event::Handle<std::vector<TopJet>> h_tops_;
    // uhh2::Event::Handle<FlavorParticle> h_primlep_;
    float min_dR_;
    uhh2::Event::Handle<float> h_mHLep_;
    uhh2::Event::Handle<float> h_mHtop_;
    uhh2::Event::Handle<float> h_mMax_;
    uhh2::Event::Handle<float> h_mMin_;
};


// class TopReconstruction: public uhh2::AnalysisModule {
// public:

//     explicit TopReconstruction(Context & ctx, const NeutrinoReconstructionMethod & neutrinofunction, const string & label):
//     m_neutrinofunction(neutrinofunction) {
//         h_recohyps = ctx.declare_event_output<vector<TopJet>>(label);
//         h_primlep = ctx.get_handle<PrimaryLepton>("PrimaryLepton");
//     }

//     virtual bool process(uhh2::Event & event) override{
//         assert(event.jets);
//         assert(event.met);
//         //find primary charged lepton
//         std::vector<TopJet> recoHyps;
//         //reconstruct neutrino
//         const Particle & lepton = event.get(h_primlep);
//         std::vector<LorentzVector> neutrinos = m_neutrinofunction( lepton.v4(), event.met->v4());
//         unsigned int n_jets = event.jets->size();
//         // if(n_jets>10) n_jets=10; //avoid crashes in events with many jets
//         // idea: loop over 3^Njet possibilities and write the current loop
//         // index j in the 3-base system. The Njets digits represent whether
//         // to assign each jet to the hadronic side (0), leptonic side (1),
//         // or none of them (2).
//         const unsigned int max_j = pow(2, n_jets);

//         //=====CONTINUE HERE!!========
//         //loop over neutrino solutions and jet assignments to fill hyotheses
//         for(const auto & neutrino_p4 : neutrinos) {
//             const LorentzVector wlep_v4 = lepton.v4() + neutrino_p4;
//             for (unsigned int j=0; j < max_j; j++) {
//                 LorentzVector toplep_v4 = wlep_v4;
//                 int lepjets=0;
//                 int num = j;
//                 for (unsigned int k=0; k<n_jets; k++) {

//                     if(num%2==0) {
//                         toplep_v4 = toplep_v4 + event.jets->at(k).v4();
//                         TopJet hyp;
//                         hyp.set_v4(toplep_v4);
//                         lepjets++;
//                     }
//                     if (lepjets) recoHyps.emplace_back(move(hyp));
//                     //in case num%3==2 do not take this jet at all
//                     //shift the trigits of num to the right:
//                     num /= 2;
//                 }

//             //search jet with highest pt assigned to leptonic top
//                 int blep_idx(-1);
//                 float maxpt(-1.);
//                 for(unsigned int i=0; i<hyp.toplep_jets().size(); ++i){
//                   if(maxpt< hyp.toplep_jets().at(i).pt()){
//                     maxpt = hyp.toplep_jets().at(i).pt();
//                     blep_idx = i;
//                   }
//                 }
//                 if(blep_idx != -1) hyp.set_blep_v4(hyp.toplep_jets().at(blep_idx).v4());

//                 //fill only hypotheses with at least one jet assigned to each top quark
//                 if(lepjets>0) {
//                     hyp.set_tophad_v4(tophad_v4);
//                     hyp.set_toplep_v4(toplep_v4);
//                 }
//             } // 3^n_jets jet combinations
//         } // neutrinos
//         event.set(h_recohyps, move(recoHyps));
//         return true;
//     }

// private:
//     NeutrinoReconstructionMethod m_neutrinofunction;
//     uhh2::Event::Handle<std::vector<TopJet>> h_recohyps;
//     uhh2::Event::Handle<FlavorParticle> h_primlep;
// };