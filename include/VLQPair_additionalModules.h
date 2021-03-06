#pragma once

#include <iostream>
#include <vector>
#include <stdlib.h>
#include <time.h>
#include <boost/type_traits.hpp>

#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Event.h"

#include "UHH2/common/include/TTbarReconstruction.h"
#include "UHH2/common/include/Utils.h"

#include "UHH2/VLQSemiLepPreSel/include/VLQCommonModules.h"
#include "UHH2/VLQSemiLepPreSel/include/SelectionItem.h"

using namespace std;
using namespace uhh2;

typedef SelectionItemData<int>      SelDatI;
typedef SelectionItemData<float>    SelDatF;
typedef SelectionItemData<double>   SelDatD;

enum ParticleID {
    BottomID = 5,
    TopID = 6,
    TprimeID = 8000001,
    BprimeID = 8000002,
    ElID = 11,
    MuID = 13,
    ZID = 23,
    WID = 24,
    HiggsID = 25
};

template <typename T>
class TrueId {
public:
    static bool is_true(const T &, const Event &) {
        return true;
    }
    static bool is_false(const T &, const Event &) {
        return false;
    }
};

class PrimaryLeptonPtProducer: public AnalysisModule {
public:
    explicit PrimaryLeptonPtProducer(Context & ctx,
                              const string & prim_lep_hndl = "PrimaryLepton",
                              const string & h_pt = "primary_lepton_pt"):
        h_pt(ctx.get_handle<float>(h_pt)),
        h_prim_lep(ctx.get_handle<FlavorParticle>(prim_lep_hndl)) {}

    virtual bool process(Event & e) override {
        float pt = -1.;
        if (e.is_valid(h_prim_lep)) {
            auto prim_lep = e.get(h_prim_lep);
            if (prim_lep.pt() > 0.001) {
                pt = prim_lep.pt();
            }

        }
        e.set(h_pt, pt);
        return true;
    }

private:
    Event::Handle<float> h_pt;
    Event::Handle<FlavorParticle> h_prim_lep;
};  // PrimaryLeptonPtProducer

// class NeutrinoParticleProducer: public AnalysisModule {
// public:
//     explicit NeutrinoParticleProducer(Context & ctx,
//                             const NeutrinoReconstructionMethod & neutrinofunc,
//                             const string & h_out = "neutrino_part_vec",
//                             const string & h_primlep = "PrimaryLepton") :
//         neutrinofunc_(neutrinofunc),
//         h_out_(ctx.get_handle<vector<LorentzVector>>(h_out)),
//         h_primlep_(ctx.get_handle<FlavorParticle>(h_primlep)) {}

//     virtual bool process(Event & event) override {
//         assert(event.jets);
//         assert(event.met);
        
//         if (!event.is_valid(h_primlep_)) {
//             return false;
//         }
//         const Particle & lepton = event.get(h_primlep_);
//         vector<LorentzVector> neutrino_hyps = neutrinofunc_(lepton.v4(), event.met->v4());
//         // vector<FlavorParticle> neutrino_parts;
//         // for (LorentzVector const & i_v4 : neutrino_hyps) {
//         //     FlavorParticle neutrino_part;
//         //     neutrino_part.set_v4(i_v4);
//         //     neutrino_part.set_pdgId(12); // set to dummy value of electron neutrino, not important anyway
//         //     neutrino_parts.push_back(neutrino_part); 
//         // }

//         event.set(h_out_, neutrino_hyps);

//         return true;
//     }

// private:
//     NeutrinoReconstructionMethod neutrinofunc_;
//     Event::Handle<vector<LorentzVector>> h_out_;
//     Event::Handle<FlavorParticle> h_primlep_;
// };


// template<typename TYPE1, typename TYPE2>
// class MinDeltaRProducer: public AnalysisModule {
// public:
//     explicit MinDeltaRProducer(Context & ctx,
//                             const string & h_p1,
//                             const string & h_p2,
//                             const string & h_out) :
//         h_p1_(ctx.get_handle<TYPE1>(h_p1)),
//         h_p2_(ctx.get_handle<vector<TYPE2>>(h_p2)),
//         h_out_(ctx.get_handle<float>(h_out)) {}

//     virtual bool process(Event & e) override {
//         float min_dr = -1.;
//         if (e.is_valid(h_p1_) && e.is_valid(h_p2_)) {
//             const TYPE1 & ref_part = e.get(h_p1_);
//             const vector<TYPE2> & comp_parts = e.get(h_p2_);

//             double deltarmin = std::numeric_limits<double>::infinity();
//             const TYPE2* closest_part=0;
//             for(unsigned int i=0; i<comp_parts.size(); ++i) {
//                 const TYPE2 & pi = comp_parts[i];
//                 double dr = uhh2::deltaR(pi, ref_part);
//                 if(dr < deltarmin) {
//                     deltarmin = dr;
//                     closest_part = &pi;
//                 }
//             }

//             if (closest_part) {
//                 min_dr = uhh2::deltaR(ref_part, *closest_part);
//             }
            
//         }

//         e.set(h_out_, min_dr);

//         return true;
//     }

// private:
//     Event::Handle<TYPE1> h_p1_;
//     Event::Handle<vector<TYPE2>> h_p2_;
//     Event::Handle<float> h_out_;
// };

// template<typename T>
// class TwoParticleCollectionProducer: public AnalysisModule {
// public:
//     explicit TwoParticleCollectionProducer(Context & ctx,
//                             const string & h_in,
//                             const string & h_out):
//         h_in_(ctx.get_handle<vector<T>>(h_in)),
//         h_out_(ctx.get_handle<vector<T>>(h_out)) {}

//     virtual bool process(Event & event) override {
        
//         if (!event.is_valid(h_in_)) {
//             return false;
//         }
//         const vector<T> & in_coll = event.get(h_in_);
//         if (in_coll.size() > 1) {
//             vector<T> out_coll = {in_coll[0], in_coll[1]};

//             event.set(h_out_, out_coll);

//             return true;
//         } else {
//             return false;
//         }
//     }

// private:
//     Event::Handle<vector<T>> h_in_;
//     Event::Handle<vector<T>> h_out_;
// };


// template<typename T>
// class DeltaRTwoLeadingParticleProducer: public AnalysisModule {
// public:
//     explicit DeltaRTwoLeadingParticleProducer(Context & ctx,
//                             const string & h_in,
//                             const string & h_dr) :
//         h_in_(ctx.get_handle<vector<T>>(h_in)),
//         h_dr_(ctx.get_handle<float>(h_dr)) {}

//     virtual bool process(Event & e) override {
//         if (e.is_valid(h_in_)) {
//             const vector<T> & parts = e.get(h_in_);

//             if (parts.size() > 1) {
//                 float dr = deltaR(parts[0], parts[1]);
//                 e.set(h_dr_, dr);

//                 return true;
//             }  
            
//         }

//         e.set(h_dr_, -1.);

//         return false;

//     }

// private:
//     Event::Handle<vector<T>> h_in_;
//     Event::Handle<float> h_dr_;
// };


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


// class HiggsXBTag {
// public:
//     explicit HiggsXBTag(float minmass = 60.f, float maxmass = std::numeric_limits<float>::infinity(), 
//                                JetId const & id = CSVBTag(CSVBTag::WP_MEDIUM),
//                                unsigned n_higgs_tags = 2) :
//         minmass_(minmass), maxmass_(maxmass), btagid_(id), n_higgs_tags_(n_higgs_tags) {}

//     bool operator()(TopJet const & topjet, uhh2::Event const & event) const {
//         auto subjets = topjet.subjets();
//         if(subjets.size() < 2) return false;
//         unsigned n_sj_btags = 0;
//         // unsigned n_sj_btagvetos = 0;
//         for (const auto & sj : subjets) {
//             if (btagid_(sj, event))
//                 n_sj_btags++;
//         }

//         if (n_sj_btags < n_higgs_tags_)
//             return false;

//         LorentzVector firsttwosubjets = subjets[0].v4() + subjets[1].v4();
//         if(!firsttwosubjets.isTimelike()) {
//             return false;
//         }
//         auto mjet = firsttwosubjets.M();
//         if(mjet < minmass_) return false;
//         if(mjet > maxmass_) return false;
//         return true;
//     }

// private:
//     float minmass_, maxmass_;
//     JetId btagid_;
//     unsigned n_higgs_tags_;

// };


// class SubjetCSVProducer: public AnalysisModule {
// public:
//     explicit SubjetCSVProducer(Context & ctx,
//                                const string & h_in,
//                                const string & h_out,
//                                unsigned ind_sj = 1):
//         h_in_(ctx.get_handle<std::vector<TopJet>>(h_in)),
//         h_out_(ctx.get_handle<float>(h_out)),
//         ind_sj_(ind_sj-1) {}

//     virtual bool process(Event & e) override {
//         if (e.is_valid(h_in_)) {
//             std::vector<TopJet> const & coll = e.get(h_in_);
//             if (coll.size()) {
//                 std::vector<Jet> const & subjets = coll[0].subjets();
//                 if (subjets.size() > ind_sj_) {
//                     // if (abs(subjets[ind_sj_].btag_combinedSecondaryVertex()) > 10)
//                     //     std::cout << subjets[ind_sj_].btag_combinedSecondaryVertex() << std::endl;
//                     e.set(h_out_, subjets[ind_sj_].btag_combinedSecondaryVertex());
//                 }
//                 else {
//                     e.set(h_out_, -1.);
//                     return true;
//                 }
//             } else {
//                 e.set(h_out_, -1.);
//             }
//             return true;
//         } else {
//             e.set(h_out_, -1.);
//             return false;
//         }

//     }

// private:
//     Event::Handle<std::vector<TopJet>> h_in_;
//     Event::Handle<float> h_out_;
//     unsigned ind_sj_;
// };

// template<typename T>
// class LeadingPartEtaProducer : public AnalysisModule {
// public:
//     explicit LeadingPartEtaProducer(Context & ctx,
//                         const string & h_in,
//                         const string & h_out):
//         h_in_(ctx.get_handle<vector<T>>(h_in)),
//         h_out_(ctx.get_handle<float>(h_out)) {}

//     virtual bool process(Event & event) override {
//         if (event.is_valid(h_in_)) {
//             vector<T> & coll = event.get(h_in_);
//             if (coll.size()) {
//                 event.set(h_out_, coll[0].eta());
//             } else {
//                 event.set(h_out_, -1.);
//             }

//             return true;
//         } else {
//             event.set(h_out_, -1.);
//             return false;
//         }
//     }
// private:
//     Event::Handle<vector<T>> h_in_;
//     Event::Handle<float> h_out_;
// };


class HiggsFlexBTag {
public:
    explicit HiggsFlexBTag(float minmass = 60.f, float maxmass = std::numeric_limits<float>::infinity(), 
                               JetId const & id1 = TrueId<Jet>::is_true,
                               JetId const & id2 = TrueId<Jet>::is_true,
                               bool require_id2_all = false) :
        minmass_(minmass), maxmass_(maxmass), btagid_1_(id1), btagid_2_(id2), require_id2_all_(require_id2_all) {}

    bool operator()(TopJet const & topjet, uhh2::Event const & event) const {
        auto const & subjets = topjet.subjets();
        if(subjets.size() < 2) return false;
        bool pass_sj_btag = false;
        // unsigned n_sj_btagvetos = 0;
        for (unsigned i = 0; i < subjets.size(); ++i) {
            if (btagid_1_(subjets[i], event)) {
                for (unsigned ii = 0; ii < subjets.size(); ++ii) {
                    if (ii == i)
                        continue;
                    if (!require_id2_all_ && btagid_2_(subjets[ii], event)) {
                        pass_sj_btag = true;
                        break;
                    } 
                    else if (require_id2_all_ && !btagid_2_(subjets[ii], event)) {
                        return false;
                    }
                }
                if (require_id2_all_) pass_sj_btag = true;
            }
        }

        if (!pass_sj_btag)
            return false;

        // LorentzVector firsttwosubjets = subjets[0].v4() + subjets[1].v4();
        // if(!firsttwosubjets.isTimelike()) {
        //     return false;
        // }
        auto mjet = topjet.softdropmass();
        if(mjet < minmass_) return false;
        if(mjet > maxmass_) return false;
        return true;
    }

private:
    float minmass_, maxmass_;
    JetId btagid_1_, btagid_2_;
    bool require_id2_all_;

};

template <typename T>
class PrimaryLeptonOwn: public uhh2::AnalysisModule {
public:
    typedef std::function<bool (const T &, const uhh2::Event &)> TYPE_ID;

    explicit PrimaryLeptonOwn(uhh2::Context & ctx, 
                           const std::string & h_in,
                           const std::string & h_out="PrimaryLepton",
                           boost::optional<TYPE_ID> const & id = boost::none) :
            h_in_(ctx.get_handle<vector<T>>(h_in)),
            h_out_(ctx.get_handle<FlavorParticle>(h_out)),
            id_(id) {}

    virtual bool process(uhh2::Event & event) override {
        if (!event.is_valid(h_in_))
            return false;
        FlavorParticle prim_part;
        vector<T> const & coll = event.get(h_in_);
        if (id_) {
            for (auto const & part : coll) {
                if ((*id_)(part, event)) {
                    prim_part = part;
                    break;
                }
            }
        }
        else {
            if (coll.size())
                prim_part = coll[0];
        }
        event.set(h_out_, move(prim_part));
        return true;
    }

private:
    uhh2::Event::Handle<vector<T>> h_in_;
    uhh2::Event::Handle<FlavorParticle> h_out_;
    boost::optional<TYPE_ID> id_; 
};

template <typename T>
class LeadingPartInvMassproducer: public uhh2::AnalysisModule {
public:
    typedef std::function<bool (const T &, const uhh2::Event &)> TYPE_ID;

    explicit LeadingPartInvMassproducer(uhh2::Context & ctx, 
                           const std::string & h_in,
                           const std::string & h_out,
                           boost::optional<TYPE_ID> const & id = boost::none) :
            h_in_(ctx.get_handle<vector<T>>(h_in)),
            h_out_(ctx.get_handle<float>(h_out)),
            id_(id) {}

    virtual bool process(uhh2::Event & event) override {

        if (!event.is_valid(h_in_))
            throw;

        float inv_mass = -1.;

        vector<T> const & coll = event.get(h_in_);
        vector<LorentzVector> coll_ld_part;

        if (id_) {
            for (auto const & part : coll) {
                if ((*id_)(part, event)) {
                    coll_ld_part.push_back(part.v4());
                }
            }
        }
        else {
            for (auto const & part : coll) {
                coll_ld_part.push_back(part.v4());
            }
        }

        if (coll_ld_part.size() >= 2) {
            LorentzVector sum_v4 = coll_ld_part[0]+coll_ld_part[1];
            if (sum_v4.isTimelike())
                inv_mass = sum_v4.M();
        }
        event.set(h_out_, inv_mass);
        return true;
    }

private:
    uhh2::Event::Handle<vector<T>> h_in_;
    uhh2::Event::Handle<float> h_out_;
    boost::optional<TYPE_ID> id_; 
};



// static bool checkDecayMode(const Event & event, int id_tp1d1,
//             int id_tp1d2, int id_tp2d1, int id_tp2d2) {
//     GenParticleDaughterId tp1d(ParticleID::TprimeID, id_tp1d1, id_tp1d2);
//     GenParticleDaughterId tp2d(ParticleID::TprimeID, id_tp2d1, id_tp2d2);

//     for (vector<GenParticle>::const_iterator gp1 = event.genparticles->begin();
//             gp1 != event.genparticles->end(); ++gp1) {
//         if (tp1d(*gp1, event)) {
//             for (vector<GenParticle>::const_iterator gp2 = gp1+1;
//                     gp2 != event.genparticles->end(); ++gp2) {
//                 if (tp2d(*gp2, event)) {
//                     return true;
//                 }
//             }
//             return false;
//         }
//         else if (tp2d(*gp1, event)) {
//             for (vector<GenParticle>::const_iterator gp2 = gp1+1;
//                     gp2 != event.genparticles->end(); ++gp2) {
//                 if (tp1d(*gp2, event)) {
//                     return true;
//                 }
//             }
//             return false;
//         }
//     }
//     return false;
// }

class GenSelectionAcceptProducer : public AnalysisModule {
public:
    explicit GenSelectionAcceptProducer(Context & ctx,
            string const & h_accept = "gendecay_accept",
            GenParticleId const & tp1d = TrueId<GenParticle>::is_true,
            GenParticleId const & tp2d = TrueId<GenParticle>::is_true) :
    h_accept_(ctx.get_handle<int>(h_accept)),
    tp1d_(tp1d),
    tp2d_(tp2d) {}

    virtual bool process(Event & event) override {
        if (event.isRealData) {
            event.set(h_accept_, 1);
            return true;
        }

        assert(event.genparticles);
        for (vector<GenParticle>::const_iterator gp1 = event.genparticles->begin();
            gp1 != event.genparticles->end(); ++gp1) {
            if (tp1d_(*gp1, event)) {
                for (vector<GenParticle>::const_iterator gp2 = gp1+1;
                    gp2 != event.genparticles->end(); ++gp2) {
                    if (tp2d_(*gp2, event)) {
                        event.set(h_accept_, 1);
                        return true;
                    }
                }
                event.set(h_accept_, 0);
                return false;
            }
            else if (tp2d_(*gp1, event)) {
                for (vector<GenParticle>::const_iterator gp2 = gp1+1;
                    gp2 != event.genparticles->end(); ++gp2) {
                    if (tp1d_(*gp2, event)) {
                        event.set(h_accept_, 1);
                        return true;
                    }
                }
                event.set(h_accept_, 0);
                return false;
            }
        }

        event.set(h_accept_, 0);
        return false;
    }

private:
    Event::Handle<int> h_accept_;
    GenParticleId tp1d_, tp2d_;
};  // GenSelectionAcceptProducer


class TrueFalseProducer : public AnalysisModule {
public:
    explicit TrueFalseProducer(Context & ctx,
            string const & h_accept = "gendecay_accept",
            bool true_false = false) :
    h_accept_(ctx.get_handle<int>(h_accept)),
    true_false_(true_false) {}

    virtual bool process(Event & event) override {
        if (true_false_)
            event.set(h_accept_, 1);
        else 
            event.set(h_accept_, 0);


        return true;
    }

private:
    Event::Handle<int> h_accept_;
    bool true_false_;
};  // TrueFalseProducer


class GenMassTTbarSelection : public AnalysisModule {
public:
    explicit GenMassTTbarSelection(Context & ctx,
            float min_mass,
            float max_mass = std::numeric_limits<float>::infinity(),
            string const & h_accept = "gendecay_accept",
            string const & ttbargen = "ttbargen") :
    min_mass_(min_mass),
    max_mass_(max_mass),
    h_accept_(ctx.get_handle<int>(h_accept)),
    h_ttbargen_(ctx.get_handle<TTbarGen>(ttbargen)) {}

    virtual bool process(Event & event) override {
        if (event.isRealData) {
            event.set(h_accept_, 1);
            return true;
        }

        const auto & ttbargen = event.get(h_ttbargen_);

        LorentzVector top = ttbargen.Top().v4();
        LorentzVector antitop = ttbargen.Antitop().v4();


        double mttbar_gen = (top+antitop).M();

        bool pass = mttbar_gen >= min_mass_ && mttbar_gen < max_mass_;

        event.set(h_accept_, (int)pass);
        return pass;
    }

private:
    float min_mass_, max_mass_;
    Event::Handle<int> h_accept_;
    Event::Handle<TTbarGen> h_ttbargen_;

};  // GenMassTTbarSelection



class BTagSFJetCollectionProducer: public AnalysisModule {
public:

    explicit BTagSFJetCollectionProducer(Context & ctx,
                                std::string const & in_tj_name,
                                std::string const & in_jet_name,
                                std::string const & out_name):
        in_tj_hndl(ctx.get_handle<vector<TopJet>>(in_tj_name)),
        in_jet_hndl(ctx.get_handle<vector<Jet>>(in_jet_name)),
        out_hndl(ctx.get_handle<vector<TopJet>>(out_name)) {}

    bool process(Event & event) override {
        if (!event.is_valid(in_tj_hndl) || !event.is_valid(in_jet_hndl))
            return false;
        vector<TopJet> out_coll = event.get(in_tj_hndl);
        TopJet temp_tj;
        temp_tj.set_subjets(event.get(in_jet_hndl));
        out_coll.push_back(temp_tj);
        event.set(out_hndl, out_coll);
        return true;
    }

private:
    Event::Handle<vector<TopJet>> in_tj_hndl;
    Event::Handle<vector<Jet>> in_jet_hndl;
    Event::Handle<vector<TopJet>> out_hndl;
};


class PrimVertProducer: public AnalysisModule {
public:
    explicit PrimVertProducer(Context & ctx,
                                  const string & h_name = "n_prim_vertices"):
        h(ctx.get_handle<int>(h_name)) {}

    virtual bool process(Event & e) override {
        if (e.pvs) {
            e.set(h, e.pvs->size());
            return true;
        } else {
            e.set(h, -1.);
            return false;
        }
    }

private:
    Event::Handle<int> h;
};  // PrimVertProducer


// class MaxNSubjetBtagProducer: public AnalysisModule {
// public:

//     explicit MaxNSubjetBtagProducer(Context & ctx,
//                                 std::string const & in_name,
//                                 std::string const & out_n_name,
//                                 std::string const & out_coll_name,
//                                 JetId const & jet_id = CSVBTag(CSVBTag::WP_MEDIUM)):
//         in_hndl(ctx.get_handle<vector<TopJet>>(in_name)),
//         out_n_hndl(ctx.get_handle<int>(out_n_name)),
//         out_coll_hndl(ctx.get_handle<vector<TopJet>>(out_coll_name)),
//         jet_id_(jet_id) {}

//     bool process(Event & event) override {
//         assert(event.is_valid(in_hndl));
//         vector<TopJet> const & coll = event.get(in_hndl);
//         int max_n_sj_btags = 0;
//         for (TopJet const & tj : coll) {
//             int n_sj_btags = 0;
//             for (Jet const & j : tj.subjets()) {
//                 if (jet_id_(j, event)) 
//                     n_sj_btags++;
//             }
//             if (n_sj_btags > max_n_sj_btags)
//                 max_n_sj_btags = n_sj_btags;
//         }
//         event.set(out_n_hndl, max_n_sj_btags);
//         vector<TopJet> out_coll;
//         for (TopJet const & tj : coll) {
//             int n_sj_btags = 0;
//             for (Jet const & j : tj.subjets()) {
//                 if (jet_id_(j, event)) 
//                     n_sj_btags++;
//             }
//             if (n_sj_btags == max_n_sj_btags)
//                 out_coll.push_back(tj);
//         }
//         event.set(out_coll_hndl, out_coll);
//         return true;
//     }

// private:
//     Event::Handle<vector<TopJet>> in_hndl;
//     Event::Handle<int> out_n_hndl;
//     Event::Handle<vector<TopJet>> out_coll_hndl;
//     JetId jet_id_;
// };


// class LdMassSjProducer: public AnalysisModule {
// public:

//     explicit LdMassSjProducer(Context & ctx,
//                                 std::string const & in_name,
//                                 std::string const & out_name):
//         in_hndl(ctx.get_handle<vector<TopJet>>(in_name)),
//         out_hndl(ctx.get_handle<float>(out_name)) {}

//     bool process(Event & event) override {
//         assert(event.is_valid(in_hndl));
//         vector<TopJet> const & coll = event.get(in_hndl);
//         float mass_sj = 0.;
//         for (TopJet const & tj : coll) {
//             if (tj.subjets().size() < 2)
//                 continue;
//             LorentzVector sj_v4;
//             for (Jet const & j : tj.subjets()) {
//                 sj_v4 += j.v4();
//             }
//             if (!sj_v4.isTimelike())
//                 continue;
//             mass_sj = sj_v4.M();
//             break;
//         }
//         event.set(out_hndl, mass_sj);
//         return true;
//     }

// private:
//     Event::Handle<vector<TopJet>> in_hndl;
//     Event::Handle<float> out_hndl;
// };


// class TopJetDeltaRProducer: public AnalysisModule {
// public:

//     explicit TopJetDeltaRProducer(Context & ctx,
//                                 std::string const & in_name,
//                                 unsigned part_ind = 1,
//                                 std::string const & h_primlep = "PrimaryLepton"):
//         in_hndl(ctx.get_handle<vector<TopJet>>(in_name)),
//         part_ind_(part_ind),
//         h_primlep_(ctx.get_handle<FlavorParticle>(h_primlep)),
//         h_deltaRlep_(ctx.get_handle<float>("deltaRlep_"+in_name+"_"+std::to_string(part_ind))),
//         h_deltaRak4_(ctx.get_handle<float>("deltaRak4_"+in_name+"_"+std::to_string(part_ind))),
//         h_deltaRak8_(ctx.get_handle<float>("deltaRak8_"+in_name+"_"+std::to_string(part_ind))) {}

//     bool process(Event & event) override {
//         if (!event.is_valid(in_hndl)) {
//             std::cout << "Error in TopJetDeltaRProducer: input handle not valid!\n";
//             assert(false);
//         }
//         vector<TopJet> const & coll = event.get(in_hndl);
//         float dRlep = -1.f;
//         float dRak4 = -1.f;
//         float dRak8 = -1.f;
//         if (coll.size() >= part_ind_ ) {
//             TopJet const & tj = coll[part_ind_-1];
//             if (event.is_valid(h_primlep_)) {
//                 dRlep = deltaR(tj, event.get(h_primlep_));
//             }
//             auto const * closest_ak4 = closestParticle(tj, *event.jets);
//             if (closest_ak4) {
//                 dRak4 = deltaR(tj, *closest_ak4);
//             }
//             auto const * closest_ak8 = closestParticle(tj, *event.topjets);
//             if (closest_ak8) {
//                 dRak8 = deltaR(tj, *closest_ak8);
//             }
//         }
//         event.set(h_deltaRlep_, dRlep);
//         event.set(h_deltaRak4_, dRak4);
//         event.set(h_deltaRak8_, dRak8);
//         return true;

//     }

// private:
//     Event::Handle<vector<TopJet>> in_hndl;
//     unsigned part_ind_;
//     Event::Handle<FlavorParticle> h_primlep_;
//     Event::Handle<float> h_deltaRlep_, h_deltaRak4_, h_deltaRak8_;
// };


template<typename T>
const T * closestParticleMod(const Particle  & p, const std::vector<T> & particles, double overlap){
    double deltarmin = std::numeric_limits<double>::infinity();
    const T* next=0;
    for(unsigned int i=0; i<particles.size(); ++i) {
        const T & pi = particles[i];
        double dr = uhh2::deltaR(pi, p);
        if(dr < deltarmin && dr > overlap) {
            deltarmin = dr;
            next = &pi;
        }
    }
    return next;
}

template<typename T>
inline std::pair<float, float> set_mass_and_nsubjets(Event &, T const & part, JetId const &) {
    return std::make_pair(part.v4().M(), -1.);
}

template<>  
inline std::pair<float, float> set_mass_and_nsubjets(Event & event, TopJet const & part, JetId const & id) {
    float mass = -1., nsjbtags = 0.;
    // if (part.subjets().size() >= 2) {
        // LorentzVector sj_v4;
        // nsjbtags = 0.;
    for (Jet const & j : part.subjets()) {
        // sj_v4 += j.v4();
        if (id(j, event)) nsjbtags += 1.;
    }
        // if (sj_v4.isTimelike()) 
        //     mass = sj_v4.M();
    // }
    mass = part.softdropmass();
    return std::make_pair(mass, nsjbtags);
}


template<typename T>
class JetVarProducer: public AnalysisModule {
public:

    explicit JetVarProducer(Context & ctx,
                                std::string const & in_name,
                                std::string const & out_name,
                                std::string const & prim_lep = "PrimaryMuon_noIso",
                                JetId const & id = CSVBTag(CSVBTag::WP_MEDIUM),
                                unsigned ind = 1):
        in_hndl(ctx.get_handle<vector<T>>(in_name)),
        out_hndl_mass(ctx.declare_event_output<float>(out_name+"_mass")),
        out_hndl_pt(ctx.declare_event_output<float>(out_name+"_pt")),
        // out_hndl_eta(ctx.declare_event_output<float>(out_name+"_eta")),
        out_hndl_nsjbtags(ctx.declare_event_output<float>(out_name+"_nsjbtags")),
        out_hndl_dRlep(ctx.declare_event_output<float>(out_name+"_dRlep")),
        // out_hndl_dRak4(ctx.declare_event_output<float>(out_name+"_dRak4")),
        out_hndl_dRak8(ctx.declare_event_output<float>(out_name+"_dRak8")),
        h_primlep_(ctx.get_handle<FlavorParticle>(prim_lep)),
        id_(id),
        ind_(ind) {
            tj_comp_hndl = ctx.get_handle<std::vector<TopJet>>("");
            j_comp_hndl = ctx.get_handle<std::vector<Jet>>("");
            out_hndl_dRcompcoll = ctx.declare_event_output<float>("dummy");
        }

    explicit JetVarProducer(Context & ctx,
                                std::string const & in_name,
                                std::string const & out_name,
                                std::string const & comp_coll,
                                std::string const & prim_lep = "PrimaryMuon_noIso",
                                JetId const & id = CSVBTag(CSVBTag::WP_MEDIUM),
                                unsigned ind = 1):
        JetVarProducer(ctx, in_name, out_name, prim_lep, id, ind) {
            tj_comp_hndl = ctx.get_handle<std::vector<TopJet>>(comp_coll);
            j_comp_hndl = ctx.get_handle<std::vector<Jet>>(comp_coll);
            out_hndl_dRcompcoll = ctx.declare_event_output<float>(out_name+"_dR_"+comp_coll);
        }



        

    bool process(Event & event) override {
        assert(event.is_valid(in_hndl));
        // bool is_topjet = std::is_same<T, TopJet>::value;
        float mass = -1.;
        float pt = -1.;
        // float eta = -1.;
        float nsjbtags = -1.;
        float dRlep = -1.;
        // float dRak4 = -1.;
        float dRak8 = -1.;
        float dRcomp = -1.;
        vector<T> const & coll = event.get(in_hndl);
        if (coll.size() >= ind_) {
            T const & tj = coll[ind_-1];
            pt = tj.pt();
            // eta = tj.eta();
            std::tie(mass, nsjbtags) = set_mass_and_nsubjets(event, tj, id_);
            if (event.is_valid(h_primlep_))
                dRlep = deltaR(tj, event.get(h_primlep_));
            // auto const * closest_ak4 = closestParticleMod(tj, *event.jets);
            auto const * closest_ak8 = closestParticleMod(tj, *event.topjets);
            // if (closest_ak4)
                // dRak4 = deltaR(tj, *closest_ak4);
            if (closest_ak8)
                dRak8 = deltaR(tj, *closest_ak8);
            if (event.is_valid(tj_comp_hndl)) {
                auto const closest_comp_part = closestParticleMod(tj, event.get(tj_comp_hndl));
                if (closest_comp_part)
                    dRcomp = deltaR(tj, *closest_comp_part);
            } 
            else if (event.is_valid(j_comp_hndl)) {
                auto const closest_comp_part = closestParticleMod(tj, event.get(j_comp_hndl));
                if (closest_comp_part)
                    dRcomp = deltaR(tj, *closest_comp_part);
            } 
        }
        event.set(out_hndl_mass, mass);
        event.set(out_hndl_pt, pt);
        // event.set(out_hndl_eta, eta);
        event.set(out_hndl_nsjbtags, nsjbtags);
        event.set(out_hndl_dRlep, dRlep);
        // event.set(out_hndl_dRak4, dRak4);
        event.set(out_hndl_dRak8, dRak8);
        event.set(out_hndl_dRcompcoll, dRcomp);
        return true;
    }

private:
    Event::Handle<vector<T>> in_hndl;
    Event::Handle<float> out_hndl_mass, out_hndl_pt, out_hndl_nsjbtags, out_hndl_dRlep, out_hndl_dRak8;
    Event::Handle<FlavorParticle> h_primlep_;
    JetId id_;
    unsigned int ind_;
    Event::Handle<vector<TopJet>> tj_comp_hndl;
    Event::Handle<vector<Jet>> j_comp_hndl;
    Event::Handle<float> out_hndl_dRcompcoll;
};


class NSubjetBtagProducer: public AnalysisModule {
public:

    explicit NSubjetBtagProducer(Context & ctx,
                                std::string const & in_name,
                                std::string const & out_name,
                                JetId const & id = CSVBTag(CSVBTag::WP_MEDIUM),
                                unsigned ind = 1):
        in_hndl(ctx.get_handle<vector<TopJet>>(in_name)),
        out_hndl_nsjbtags(ctx.declare_event_output<float>(out_name+"_nsjbtags")),
        id_(id),
        ind_(ind) {}

    bool process(Event & event) override {
        assert(event.is_valid(in_hndl));
        float nsjbtags = -1.;
        vector<TopJet> const & coll = event.get(in_hndl);
        if (coll.size() >= ind_) {
            TopJet const & tj = coll[ind_-1];
            // eta = tj.eta();
            nsjbtags = 0.;
            for (Jet const & j : tj.subjets()) {
                // sj_v4 += j.v4();
                if (id_(j, event)) nsjbtags += 1.;
            }
        }
        event.set(out_hndl_nsjbtags, nsjbtags);
        return true;
    }

private:
    Event::Handle<vector<TopJet>> in_hndl;
    Event::Handle<float> out_hndl_nsjbtags;
    JetId id_;
    unsigned int ind_;
};


template<typename T1, typename T2>
class DeltaRProducer: public AnalysisModule {
public:

    typedef std::function<bool (const T2 &, const uhh2::Event &)> ID;

    explicit DeltaRProducer(Context & ctx,
                                std::string const & in_name,
                                std::string const & comp_coll,
                                int ind1 = 1,
                                int ind2 = -1,
                                double overlap = 0.8) :
        in_hndl(ctx.get_handle<vector<T1>>(in_name)),
        comp_hndl_vec(ctx.get_handle<vector<T2>>(comp_coll)),
        comp_hndl_sing(ctx.get_handle<T2>(comp_coll)),
        ind1_(ind1),
        ind2_(ind2),
        overlap_(overlap)
        // out_hndl_dR_ind(ctx.declare_event_output<float>(in_name+"_"+to_string(ind1)+"_"+comp_coll+"_dR_"+to_string(ind2)))
        {
            out_hndl_dR = (ind2 < 0) ? ctx.declare_event_output<float>("dR_"+in_name+"_"+to_string(ind1)+"_"+comp_coll+"_cl") :
                                       ctx.declare_event_output<float>("dR_"+in_name+"_"+to_string(ind1)+"_"+comp_coll+"_"+to_string(ind2));
        }

        

    bool process(Event & event) override {
        assert(event.is_valid(in_hndl));
        // bool is_topjet = std::is_same<T, TopJet>::value;
        float dR = -1.;
        vector<T1> const & in_coll = event.get(in_hndl);
        if (in_coll.size() >= (size_t)ind1_) {
            T1 const & part = in_coll[(size_t)ind1_-1];
            if (!part.energy()) {
                event.set(out_hndl_dR, -1.);
                return false;
            }
            if (event.is_valid(comp_hndl_vec)) {
                vector<T2> const & comp_coll = event.get(comp_hndl_vec);
                if (ind2_ < 0) {
                    auto const * closest_comp_part = closestParticleMod(part, comp_coll, overlap_);
                    if (closest_comp_part && closest_comp_part->energy())
                        dR = deltaR(part, *closest_comp_part);
                }
                else {
                    vector<T2> clean_comp_coll = comp_coll;
                    clean_collection(clean_comp_coll, event, ID(MinMaxDeltaRId<T1>(in_hndl, overlap_, false)));
                    if (clean_comp_coll.size() >= (size_t)ind2_) {
                        T2 const & comp_part = clean_comp_coll[ind2_-1];
                        if (comp_part.energy())
                            dR = deltaR(part, comp_part);
                    }
                }
            } else if (event.is_valid(comp_hndl_sing)) {
                T2 const & comp_part = event.get(comp_hndl_sing);
                if (comp_part.energy())
                    dR = deltaR(part, comp_part);

                if (std::isnan(dR))
                    std::cout << part.pt() << " " << part.eta() << " " << part.phi() << " "
                        << part.energy() << " " << part.v4().M() << " " << comp_part.pt() << " "
                        << comp_part.eta() << " " << comp_part.phi() << " " << comp_part.energy() << " "
                        << comp_part.v4().M() << " " << std::endl;
            }
        }
        event.set(out_hndl_dR, dR);
        return true;
    }

private:
    Event::Handle<vector<T1>> in_hndl;
    Event::Handle<vector<T2>> comp_hndl_vec;
    Event::Handle<T2> comp_hndl_sing;
    int ind1_, ind2_;
    Event::Handle<float> out_hndl_dR;
    double overlap_;
};


class NSubjetID
{
public:

    NSubjetID(Context &,
                unsigned min_n_sj = 2) :
        min_n_sj_(min_n_sj)
        {}

    bool operator()(const TopJet & part, const Event &) const
    {
        if (part.subjets().size() < min_n_sj_)
            return false;

        return true;
    }

private:
    unsigned min_n_sj_;
};  // NSubjetID


class GenRecoPtProducer: public AnalysisModule {
public:
    explicit GenRecoPtProducer(Context & ctx,
                            const string & h_out,
                            int part_num,
                            const string & gen_jet_out):
        h_out_(ctx.get_handle<float>(h_out)),
        part_num_(part_num),
        h_gen_jet_out_(ctx.get_handle<float>(gen_jet_out)) {}

    virtual bool process(Event & e) override {
        if (e.isRealData) {
            const vector<Jet> & jets = *e.jets;
            if (part_num_ < 0) {
                if (jets.size() > 0) {
                    e.set(h_out_, jets.back().pt());
                    return true;
                } else {
                    e.set(h_out_, -1.);
                    return false;
                }
            } else if (part_num_ > 0){
                if (int(jets.size()) >= part_num_) {
                    e.set(h_out_, jets[part_num_-1].pt());
                    return true;
                } else {
                    e.set(h_out_, -1.);
                    return false;
                }
            } else {
                std::cout << "In GenRecoPtProducer: to calculate pt of the pt leading particle, give 1 as argument!\n";
                assert(false);
            }
        } else {
            const vector<Jet> & jets = *e.jets;
            const vector<Particle> & genjets = *e.genjets;
            if (part_num_ < 0) {
                if (jets.size() > 0) {
                    e.set(h_out_, jets.back().pt());
                    return true;
                } else {
                    e.set(h_out_, -1.);
                    return false;
                }
            } else if (part_num_ > 0){
                if (int(jets.size()) >= part_num_) {
                    const Jet & jet = jets[part_num_-1];
                    const Particle * genjet = closestParticle(jet, genjets);
                    if (genjet) {
                        e.set(h_out_, genjet->pt());
                        e.set(h_gen_jet_out_, genjet->pt());
                        return true;
                    }
                    else {
                        e.set(h_out_, -1.);
                        return false;
                    }
                } else {
                    e.set(h_out_, -1.);
                    return false;
                }
            } else {
                std::cout << "In GenRecoPtProducer: to calculate pt of the pt leading particle, give 1 as argument!\n";
                assert(false);
            }

        }

        e.set(h_out_, -1.);
        return false;

    }

private:
    Event::Handle<float> h_out_;
    int part_num_;
    Event::Handle<float> h_gen_jet_out_;
};  // GenRecoPtProducer


class GenRecoHTProducer: public AnalysisModule {
public:
    explicit GenRecoHTProducer(Context & ctx,
                            const string & h_in,
                            const string & h_out):
        h_in_(ctx.get_handle<double>(h_in)),
        h_out_(ctx.get_handle<double>(h_out)) {}

    virtual bool process(Event & event) override {
        if (!event.is_valid(h_in_)) {
            std::cout << "WARNING: ht handle not valid!" << std::endl;
            return false;
        }

        double ht = event.get(h_in_);
        
        event.set(h_out_, ht);
        return false;

    }

private:
    Event::Handle<double> h_in_;
    Event::Handle<double> h_out_;
};  // GenRecoHTProducer


class GenHTCalculator: public AnalysisModule {
public:
    explicit GenHTCalculator(Context & ctx,
                          string const & h_name = "gen_ht"):
        h_ht(ctx.get_handle<double>(h_name)) {}

    virtual bool process(Event & event) override {
        double gen_ht = 0.;
        for (const auto & j : *event.genjets) {
            if (j.pt() > 30 && abs(j.eta()) < 2.4){
                gen_ht += j.pt();
            }
        }
        event.set(h_ht, gen_ht);
        return true;
    }

private:
    Event::Handle<double> h_ht;
    Event::Handle<FlavorParticle> h_primlep;
};  // class GenHTCalculator


class MCConstantScalefactor : public AnalysisModule {
public:
    MCConstantScalefactor(uhh2::Context & ctx,
                                    float sf,
                                    float sf_uncert,
                                    const std::string & weight_postfix = "",
                                    bool multiply_weight = true): 
      sf_(sf),
      sf_uncert_(sf_uncert),
      h_weight_      (ctx.declare_event_output<float>("weight_" + weight_postfix)),
      h_weight_up_   (ctx.declare_event_output<float>("weight_" + weight_postfix + "_up")),
      h_weight_down_ (ctx.declare_event_output<float>("weight_" + weight_postfix + "_down")),
      multiply_weight_(multiply_weight)
    {
        auto dataset_type = ctx.get("dataset_type");
        is_mc_ = dataset_type == "MC";
        if (!is_mc_) {
            cout << "Warning: MCConstantScalefactor will not have an effect on "
                 <<" this non-MC sample (dataset_type = '" + dataset_type + "')" << endl;
            return;
        }
    }

    bool process(uhh2::Event & event) {

        if (!is_mc_) {  
            event.set(h_weight_,       1.);
            event.set(h_weight_up_,    1.);
            event.set(h_weight_down_,  1.);
            return true;
        }
        float weight = sf_, weight_up = sf_+sf_uncert_, weight_down = sf_-sf_uncert_;
        event.set(h_weight_,       weight);
        event.set(h_weight_up_,    weight_up);
        event.set(h_weight_down_,  weight_down);
        if (multiply_weight_)  {
            event.weight *= weight;
        }
        return true;
    }

private:
    float sf_, sf_uncert_;
    uhh2::Event::Handle<float> h_weight_;
    uhh2::Event::Handle<float> h_weight_up_;
    uhh2::Event::Handle<float> h_weight_down_;
    bool multiply_weight_;
    bool is_mc_;
};


template<typename T>
class ParticleCleaner : public AnalysisModule {
public:

    typedef std::function<bool (const T &, const uhh2::Event &)> ID;

    ParticleCleaner(Context & ctx, const ID & part_id_, std::string const & label_):
        part_id_(part_id_), hndl_(ctx.get_handle<std::vector<T>>(label_)) {}
      

    bool process(uhh2::Event & event) {
        if (!event.is_valid(hndl_)) {
            return false;
        }
        vector<T> & part_collection = event.get(hndl_);
        clean_collection(part_collection, event, part_id_);
        return true;
    }

private:
    ID part_id_;
    uhh2::Event::Handle<std::vector<T>> hndl_;
};


class HiggsMassSmear: public AnalysisModule {
public:
    explicit HiggsMassSmear(Context & ctx,
                            const std::string & htags,
                            bool write_out2 = true,
                            bool write_out1 = true,
                            float smear_fct = 1.,
                            float unc = 0.,
                            const std::string & gentopjets = "gentopjets"
                            ):
        h_htags    (ctx.get_handle<vector<TopJet>>(htags)),
        // h_sm_down    (ctx.get_handle<vector<TopJet>>(htags+"_sm_down")),
        h_sm_down    (ctx.get_handle<vector<TopJet>>(htags+"_sm_down")),
        h_sm_up    (ctx.get_handle<vector<TopJet>>(htags+"_sm_up")),
        h_gen_mass    (ctx.get_handle<float>(htags+"_gen_mass")),
        h_gen_diff_before    (ctx.get_handle<float>(htags+"_diff_before")),
        h_gen_diff_smeared    (ctx.get_handle<float>(htags+"_diff_smeared")),
        h_gen_diff_before_sj    (ctx.get_handle<float>(htags+"_diff_before_sj")),
        h_gen_diff_down    (ctx.get_handle<float>(htags+"_diff_down")),
        // h_gen_diff_down_sj    (ctx.get_handle<float>(htags+"_diff_down_sj")),
        h_gen_diff_up    (ctx.get_handle<float>(htags+"_diff_up")),
        // h_gen_diff_up_sj    (ctx.get_handle<float>(htags+"_diff_up_sj")),
        smear_fct_(smear_fct),
        unc_(unc),
        h_genjets(ctx.get_handle<vector<GenTopJet>>(gentopjets))
        {
            if (write_out1)
                h_sm_down = ctx.declare_event_output<vector<TopJet>>(htags+"_sm_down");
            if (write_out2)
                h_sm_up = ctx.declare_event_output<vector<TopJet>>(htags+"_sm_up");
        }

    virtual bool process(Event & e) override {
        assert(e.is_valid(h_htags));

        if (e.isRealData) {
            e.set(h_sm_down, e.get(h_htags));
            e.set(h_sm_up, e.get(h_htags));
            e.set(h_gen_mass, -1.);
            e.set(h_gen_diff_before, -1000.);
            e.set(h_gen_diff_smeared, -1000.);
            e.set(h_gen_diff_down, -1000.);
            e.set(h_gen_diff_up, -1000.);
            e.set(h_gen_diff_before_sj, -1000.);
            // e.set(h_gen_diff_down_sj, -1000.);
            // e.set(h_gen_diff_up_sj, -1000.);
            return true;
        }
        float gen_mass = -1.;
        float gen_diff_before = -1000.;
        float gen_diff_smeared = -1000.;
        float gen_diff_down = -1000.;
        float gen_diff_up = -1000.;
        float gen_diff_before_sj = -1000.;
        // float gen_diff_down_sj = -1000.;
        // float gen_diff_up_sj = -1000.;

        vector<TopJet> new_ak8jets;
        vector<TopJet> new_ak8jets_down;
        vector<TopJet> new_ak8jets_up;
        vector<TopJet> & htags = e.get(h_htags);
        for (size_t i = 0; i < htags.size(); ++i) {
            auto const & hj = htags[i];
            auto closest_genjet = closestParticle(hj, e.get(h_genjets));
            if (closest_genjet == nullptr || deltaR(*closest_genjet, hj) > 0.3) {
                new_ak8jets.push_back(hj);
                new_ak8jets_down.push_back(hj);
                new_ak8jets_up.push_back(hj);
                continue;
            }
            TopJet new_hj = hj;  // hj is a jet, not vector
            TopJet new_hj_down = hj;  // hj is a jet, not vector
            TopJet new_hj_up = hj;  // hj is a jet, not vector
            float hm = hj.softdropmass();
            float hm_sj = hj.softdropmass();
            if (hj.subjets().size()){
                LorentzVector sum_subjets;
                for (Jet const & subjet : hj.subjets())
                    sum_subjets += subjet.v4();
                hm_sj = sum_subjets.M();
            }

            const auto & gen_sj = closest_genjet->subjets();
            float gen_sj_mass = (gen_sj.size() > 1) ?
                                (gen_sj[0].v4() + gen_sj[1].v4()).mass() : hm;

            auto mass_sm = gen_sj_mass + smear_fct_ * (hm - gen_sj_mass);
            auto mass_sm_down = gen_sj_mass + (smear_fct_ - unc_) * (hm - gen_sj_mass);
            auto mass_sm_up = gen_sj_mass + (smear_fct_ + unc_) * (hm - gen_sj_mass);

            // auto mass_sm_down_sj = max(0.0f, gen_sj_mass + 1.1f * (hm_sj - gen_sj_mass));  // - 9.1998f
            // auto mass_sm_up_sj = max(0.0f, gen_sj_mass + 1.2f * (hm_sj - gen_sj_mass));  // - 9.1998f
            new_hj.set_softdropmass(mass_sm);
            new_hj_down.set_softdropmass(mass_sm_down);
            new_hj_up.set_softdropmass(mass_sm_up);
            new_ak8jets.push_back(new_hj);
            new_ak8jets_down.push_back(new_hj_down);
            new_ak8jets_up.push_back(new_hj_up);
            if (!i) {
                gen_mass = gen_sj_mass;
                gen_diff_before = (hm - gen_sj_mass)/gen_sj_mass;
                gen_diff_smeared = (mass_sm - gen_sj_mass)/gen_sj_mass;
                gen_diff_down = (mass_sm_down - gen_sj_mass)/gen_sj_mass;
                gen_diff_up = (mass_sm_up - gen_sj_mass)/gen_sj_mass;
                gen_diff_before_sj = (hm_sj - gen_sj_mass)/gen_sj_mass;
                // gen_diff_down_sj = (mass_sm_down_sj - gen_sj_mass)/gen_sj_mass;
                // gen_diff_up_sj = (mass_sm_up_sj - gen_sj_mass)/gen_sj_mass;
            }

        }
        htags = new_ak8jets;
        // e.set(h_sm_nom, new_ak8jets);
        e.set(h_sm_down, new_ak8jets_down);
        e.set(h_sm_up, new_ak8jets_up);
        e.set(h_gen_mass, gen_mass);
        e.set(h_gen_diff_before, gen_diff_before);
        e.set(h_gen_diff_smeared, gen_diff_smeared);
        e.set(h_gen_diff_down, gen_diff_down);
        e.set(h_gen_diff_up, gen_diff_up);
        e.set(h_gen_diff_before_sj, gen_diff_before_sj);
        // e.set(h_gen_diff_down_sj, gen_diff_down_sj);
        // e.set(h_gen_diff_up_sj, gen_diff_up_sj);

        return true;


    }
private:
    Event::Handle<vector<TopJet>> h_htags;
    Event::Handle<vector<TopJet>> h_sm_down, h_sm_up;
    Event::Handle<float> h_gen_mass;
    Event::Handle<float> h_gen_diff_before, h_gen_diff_smeared, h_gen_diff_before_sj;
    Event::Handle<float> h_gen_diff_down; // , h_gen_diff_down_sj
    Event::Handle<float> h_gen_diff_up; // , h_gen_diff_up_sj
    float smear_fct_, unc_;
    Event::Handle<vector<GenTopJet>> h_genjets;
    // Event::Handle<float> h_mass;
    // Event::Handle<float> h_mass_gen;
    // Event::Handle<float> h_mass_gen_sd;
    // Event::Handle<float> h_mass_diff;
    // Event::Handle<float> h_mass_sm_down;
    // Event::Handle<float> h_mass_sm_up;
};


class AK8SoftDropCorr: public AnalysisModule {
public:
    explicit AK8SoftDropCorr(Context & ctx,
                            const std::string & ak8jets,
                            float dir = 0.
                            ):
        h_ak8jets (ctx.get_handle<vector<TopJet>>(ak8jets)),
        dir_(dir)
        {}

    virtual bool process(Event & e) override {
        assert(e.is_valid(h_ak8jets));

        for (auto & ak8jet : e.get(h_ak8jets)) {
            // float old_mass = ak8jet.softdropmass();
            // float sj_mass = -1.;
            // if (ak8jet.subjets().size()){
            //     LorentzVector sum_subjets;
            //     for (Jet const & subjet : ak8jet.subjets())
            //         sum_subjets += subjet.v4();
            //     sj_mass = sum_subjets.M();
            // }
            if (!dir_) {
                // float old_mass = ak8jet.softdropmass();
                // float jec_corr = abs(1 - 1/ak8jet.JEC_factor_raw());
                // float corr_fct = 1 + sqrt(jec_corr*jec_corr);
                float new_mass = ak8jet.softdropmass()*1/ak8jet.JEC_factor_raw();
                // std::cout << "Nominal old_mass/jec_corr_fct/corr_fct/new_mass:  " << old_mass << " / " << 1/ak8jet.JEC_factor_raw() << " / " << corr_fct << " / " << new_mass << std::endl;
                ak8jet.set_softdropmass(new_mass);
            }
            else if (dir_ < 0.) {
                // float old_mass = ak8jet.softdropmass();
                float jec_corr = 1/ak8jet.JEC_factor_raw() - 1;
                float corr_fct = jec_corr < 0 ? 1 - sqrt(jec_corr*jec_corr + dir_*dir_) : 1 + sqrt(jec_corr*jec_corr - dir_*dir_);
                float new_mass = ak8jet.softdropmass()*corr_fct;
                // std::cout << "Down old_mass/jec_corr_fct/corr_fct/new_mass:  " << old_mass << " / " << 1/ak8jet.JEC_factor_raw() << " / " << corr_fct << " / " << new_mass << std::endl;
                ak8jet.set_softdropmass(new_mass);
            }
            else {
                // float old_mass = ak8jet.softdropmass();
                float jec_corr = 1/ak8jet.JEC_factor_raw() - 1;
                float corr_fct = jec_corr < 0 ? 1 - sqrt(jec_corr*jec_corr - dir_*dir_) : 1 + sqrt(jec_corr*jec_corr + dir_*dir_);
                float new_mass = ak8jet.softdropmass()*corr_fct;
                // std::cout << "Up old_mass/jec_corr_fct/corr_fct/new_mass:  " << old_mass << " / " << 1/ak8jet.JEC_factor_raw() << " / " << corr_fct << " / " << new_mass << std::endl;
                ak8jet.set_softdropmass(new_mass);
            }
            // cout << "Old/Subjet/New: " << old_mass << " " << sj_mass << " " << ak8jet.softdropmass() << endl;
        }

        return true;


    }
private:
    Event::Handle<vector<TopJet>> h_ak8jets;
    float dir_;
};


class LeptonicWProducer: public uhh2::AnalysisModule {
public:

    explicit LeptonicWProducer(uhh2::Context & ctx, 
                           const std::string & h_primlep,
                           const std::string & h_out) :
            h_primlep_(ctx.get_handle<FlavorParticle>(h_primlep)),
            h_out_(ctx.declare_event_output<Particle>(h_out)) {}

    virtual bool process(uhh2::Event & event) override {

        if (!event.is_valid(h_primlep_))
            throw;

        FlavorParticle const & lepton = event.get(h_primlep_);
        Particle lep_w;
        if (!lepton.energy()) {
            event.set(h_out_, lep_w);
            return false;
        }
        std::vector<LorentzVector> neutrinos = NeutrinoReconstruction( lepton.v4(), event.met->v4());

        for(const auto & neutrino_p4 : neutrinos) {
            LorentzVector w_hyp = lepton.v4() + neutrino_p4;
            if (w_hyp.pt() > lep_w.v4().pt())
                lep_w.set_v4(w_hyp);
        }
        event.set(h_out_, lep_w);
        return true;
    }

private:
    uhh2::Event::Handle<FlavorParticle> h_primlep_;
    uhh2::Event::Handle<Particle> h_out_;
};

// template<typename TYPE>
// class JetPtAndMultFixer {
// public:
//     explicit JetPtAndMultFixer(double offset, double gradient) :
//         offset_(offset), gradient_(gradient) {}

//     bool operator()(TYPE const & part, uhh2::Event const &) const {
//         double part_pt = part.pt();
//         double sf = offset_ + part_pt * gradient_;
        
//         srand(part.eta());

//         double rand_num = rand() % 1000000;
//         rand_num /= 1000000.;

//         if (rand_num > sf)
//             return false;

//         return true;
//     }

// private:
//     double offset_, gradient_;

// };

// template<typename T>
// class NParticleMultiVarProducer : public AnalysisModule {
// public:

//     explicit NParticleMultiVarProducer(Context & ctx,
//                         const string & h_in,
//                         const vector<string> & variables = {"n", "pt", "eta", "phi"},
//                         unsigned part_ind = 1,
//                         const string & h_primlep = "PrimaryLepton") :
//         h_name_(h_in),
//         h_in_(ctx.get_handle<vector<T>>(h_in)),
//         part_ind_(part_ind),
//         h_primlep_(ctx.get_handle<FlavorParticle>(h_primlep))
//         {
//             // === TEST: test if it's possible to make hist names without handle names
//             for (string const & var : variables) {
//                 if (var == "n") hists_[var] = book<TH1F>("n", "n", 10, -.5, 9.5);
//                 if (var == "n_subjets") hists_[var] = book<TH1F>("n_subjets", "n_subjets", 10, -.5, 9.5);
//                 if (var == "pt") hists_[var] = book<TH1F>("pt", "pt", 60, 0., 1500.);
//                 if (var == "eta") hists_[var] = book<TH1F>("eta", "eta", 50, -3., 3.);
//                 if (var == "phi") hists_[var] = book<TH1F>("phi", "phi", 50, -3.14, 3.14);
//                 if (var == "mass") hists_[var] = book<TH1F>("mass", "mass", 60, 0., 300.);
//                 if (var == "mass_sj") hists_[var] = book<TH1F>("mass_sj", "mass sj", 60, 0., 300.);
//                 if (var == "tau21") hists_[var] = book<TH1F>("tau21", "tau21", 50, 0., 1.);
//                 if (var == "tau32") hists_[var] = book<TH1F>("tau32", "tau32", 50, 0., 1.);
//                 if (var == "csv_first_sj") hists_[var] = book<TH1F>("csv_first_sj", "csv_first_sj", 50, 0., 1.);
//                 if (var == "csv_second_sj") hists_[var] = book<TH1F>("csv_second_sj", "csv_second_sj", 50, 0., 1.);
//                 if (var == "csv_max_sj") hists_[var] = book<TH1F>("csv_max_sj", "csv_max_sj", 50, 0., 1.);
//                 if (var == "dRlepton") hists_[var] = book<TH1F>("dRlepton", "dR(ak8 jet, lepton)", 50, 0., 5.);
//                 if (var == "dRak4") hists_[var] = book<TH1F>("dRak4", "dR(Ak8 jet, closest Ak4 jet)", 50, 0., 5.);
//                 if (var == "dRak8") hists_[var] = book<TH1F>("dRak8", "dR(Ak8 jet, closest Ak8 jet)", 50, 0., 5.);
//                 if (split(var, "-")[0] == "n_sjbtags") hists_[var] = book<TH1F>("n_sjbtags_"+split(var, "-")[1], "N sjbtags "+split(var, "-")[1], 5, -.5, 4.5);
//             }  
//         }

//     bool process(Event & event) override {
//         bool is_topjet = std::is_same<T, TopJet>::value;
//         double w = event.weight;
//         // double w = 1.;
//         if (!event.is_valid(h_in_)) {
//             cout << "WARNING: handle " << h_name_ <<" in NParticleMultiHistProducer not valid!\n";
//             return;
//         }
//         vector<T> const & coll = event.get(h_in_);
//         for (map<string, TH1F*>::const_iterator it = hists_.begin(); it != hists_.end(); ++it) {
//             if (it->first == "n") it->second->Fill(coll.size(), w);
//             if (coll.size() >= part_ind_) {
//                 T const & particle = coll[part_ind_-1];
//                 if (it->first == "pt") it->second->Fill(particle.pt(), w);
//                 if (it->first == "eta") it->second->Fill(particle.eta(), w);
//                 if (it->first == "phi") it->second->Fill(particle.phi(), w);
//                 if (it->first == "mass") it->second->Fill(particle.v4().M(), w);
//                 if (it->first == "n_subjets") {
//                         // assert(false);
//                     assert(is_topjet);
//                     it->second->Fill(particle.subjets().size(), w);
//                 };
//                 if (it->first == "mass_sj") {
//                         // assert(false);
//                     assert(is_topjet);
//                     if (particle.subjets().size()){
//                         LorentzVector sum_subjets;
//                         for (Jet const & subjet : particle.subjets())
//                             sum_subjets += subjet.v4();
//                         it->second->Fill(sum_subjets.M(), w);
//                     } else {
//                         it->second->Fill(-1., w);
//                     }
//                 };
//                 if (it->first == "tau21") {
//                     assert(is_topjet);
//                     it->second->Fill(particle.tau2()/particle.tau1(), w);
//                 }
//                 if (it->first == "tau32") {
//                     assert(is_topjet);
//                     it->second->Fill(particle.tau3()/particle.tau2(), w);
//                 }
//                 if (it->first == "csv_first_sj") {
//                     assert(is_topjet);
//                     if (particle.subjets().size() >= 1){
//                         it->second->Fill(particle.subjets()[0].btag_combinedSecondaryVertex(), w);
//                     } else {
//                         it->second->Fill(-1., w);
//                     }
//                 }
//                 if (it->first == "csv_second_sj") {
//                     assert(is_topjet);
//                     if (particle.subjets().size() >= 2){
//                         it->second->Fill(particle.subjets()[1].btag_combinedSecondaryVertex(), w);
//                     } else {
//                         it->second->Fill(-1., w);
//                     }
//                 }
//                 if (it->first == "csv_max_sj") {
//                     assert(is_topjet);
//                     double csv_max = -1.;
//                     for (Jet const & subjet : particle.subjets()){
//                         if (subjet.btag_combinedSecondaryVertex() > csv_max)
//                             csv_max = subjet.btag_combinedSecondaryVertex();
//                     }
//                     it->second->Fill(csv_max, w);
//                 }
//                 if (it->first == "dRlepton") {
//                     if (event.is_valid(h_primlep_)) {
//                         float dRlep = deltaR(particle, event.get(h_primlep_));
//                         it->second->Fill(dRlep, w);
//                     }
//                     else {it->second->Fill(-1., w);}
//                 }
//                 if (it->first == "dRak4") {
//                     auto const * closest_ak4 = closestParticle(particle, *event.jets);
//                     if (closest_ak4) {
//                         float dRak4 = deltaR(particle, *closest_ak4);
//                         it->second->Fill(dRak4, w);
//                     }
//                     else {it->second->Fill(-1., w);}
//                 }
//                 if (it->first == "dRak8") {
//                     auto const * closest_ak8 = closestParticle(particle, *event.topjets);
//                     if (closest_ak8) {
//                         float dRak8 = deltaR(particle, *closest_ak8);
//                         it->second->Fill(dRak8, w);
//                     }
//                     else {it->second->Fill(-1., w);}
//                 }
//                 if (split(it->first, "-")[0] == "n_sjbtags") {
//                     CSVBTag::wp wp_;
//                     if (split(it->first, "-")[1] == "loose")
//                         wp_ = CSVBTag::WP_LOOSE;
//                     else if (split(it->first, "-")[1] == "tight")
//                         wp_ = CSVBTag::WP_TIGHT;
//                     else
//                         wp_ = CSVBTag::WP_MEDIUM;
//                     CSVBTag btag_(wp_);
//                     int n_sj = 0;
//                     for (auto const & sj : particle.subjets()) {
//                         if (btag_(sj, event))
//                             n_sj++;
//                     }
//                     it->second->Fill(n_sj, w);
//                 }
//             }
//         }

//         for (auto sub_hist : sub_hists_)
//             sub_hist->fill(event);
//     }


//     void set_subhists(Hists * sub_hist) {
//         sub_hists_.emplace_back(sub_hist);
//     }


// private:
//     string h_name_;
//     Event::Handle<vector<T>> h_in_;
//     unsigned part_ind_;
//     Event::Handle<FlavorParticle> h_primlep_;
//     map<string, TH1F*> hists_;
//     vector<shared_ptr<Hists>> sub_hists_;
//     vector<Event::Handle>
// };

class JetClosestGenPartId
{
public:
    JetClosestGenPartId(int id, int daughter_id = 0, float dR = 0.4, float pt_cut = 0., bool d_in_tj = false) :
        id_(id), daughter_id_(daughter_id), dR_(dR), pt_cut_(pt_cut), d_in_tj_(d_in_tj)
        {}

    bool operator()(const TopJet & tj, const Event & event) const
    {
        for (const GenParticle & gp : *event.genparticles) {
            if (deltaR(tj, gp) <= dR_ && abs(gp.pdgId()) == id_ && gp.pt() >= pt_cut_) {
                if (daughter_id_) {
                    GenParticle const * daughter1 = gp.daughter(event.genparticles, 1);
                    GenParticle const * daughter2 = gp.daughter(event.genparticles, 2);
                    if (daughter1 && daughter2 && (abs(daughter1->pdgId()) == daughter_id_ || abs(daughter2->pdgId()) == daughter_id_)) {
                        float dR_d1 = deltaR(tj, *daughter1);
                        float dR_d2 = deltaR(tj, *daughter2);
                        if (d_in_tj_ && (dR_d1 > dR_ || dR_d2 > dR_))
                            continue;
                        // std::cout << "    particle pt/eta/phi/pdgid/daughter pdgId: " << gp.pt() << "/" << gp.eta() << "/" << gp.phi() << "/" << gp.pdgId() << "/" << daughter1->pdgId() << std::endl;
                        return true;
                    }
                }
                else
                    return true;
            }
        }
        // cout << "  Found right mother!\n";
        return false;
    }

private:
    int id_, daughter_id_;
    float dR_, pt_cut_;
    bool d_in_tj_;
};  // JetClosestGenPartId


class JetClosestGenPartDaughterRangeId
{
public:
    JetClosestGenPartDaughterRangeId(int id, int daughter_id_min = 0, int daughter_id_max = 25, float dR = 0.4, float pt_cut = 0., bool d_in_tj = false) :
        id_(id), daughter_id_min_(daughter_id_min), daughter_id_max_(daughter_id_max), dR_(dR), pt_cut_(pt_cut), d_in_tj_(d_in_tj)
        {}

    bool operator()(const TopJet & tj, const Event & event) const
    {
        for (const GenParticle & gp : *event.genparticles) {
            if (deltaR(tj, gp) <= dR_ && abs(gp.pdgId()) == id_ && gp.pt() >= pt_cut_) {
                GenParticle const * daughter1 = gp.daughter(event.genparticles, 1);
                GenParticle const * daughter2 = gp.daughter(event.genparticles, 2);
                if (daughter1 && abs(daughter1->pdgId()) >= daughter_id_min_ && abs(daughter1->pdgId()) <= daughter_id_max_ &&
                    daughter2 && abs(daughter2->pdgId()) >= daughter_id_min_ && abs(daughter2->pdgId()) <= daughter_id_max_) {
                    float dR_d1 = deltaR(tj, *daughter1);
                    float dR_d2 = deltaR(tj, *daughter2);
                    if (d_in_tj_ && (dR_d1 > dR_ || dR_d2 > dR_))
                        continue;
                    // std::cout << "    particle pt/eta/phi/pdgid/daughter pdgId: " << gp.pt() << "/" << gp.eta() << "/" << gp.phi() << "/" << gp.pdgId() << "/" << daughter1->pdgId() << std::endl;
                    return true;
                }
                else
                    return false;
            }
        }
        // cout << "  Found right mother!\n";
        return false;
    }

private:
    int id_, daughter_id_min_, daughter_id_max_;
    float dR_, pt_cut_;
    bool d_in_tj_;
};  // JetClosestGenPartDaughterRangeId


class JetClosestGenPartRangeId
{
public:
    JetClosestGenPartRangeId(int id_min, int id_max, float dR = 0.4, float pt_cut = 0.) :
        id_min_(id_min), id_max_(id_max), dR_(dR), pt_cut_(pt_cut)
        {}

    bool operator()(const TopJet & tj, const Event & event) const
    {
        for (const GenParticle & gp : *event.genparticles) {
            if (deltaR(tj, gp) <= dR_ && abs(gp.pdgId()) >= id_min_ && abs(gp.pdgId()) <= id_max_ && gp.pt() >= pt_cut_) {
                return true;
            }
        }
        // cout << "  Found right mother!\n";
        return false;
    }

private:
    int id_min_, id_max_;
    float dR_, pt_cut_;
};  // JetClosestGenPartRangeId


class HadronicTopId
{
public:
    HadronicTopId(float dR = 0.4, float pt_cut = 0., int d_in_tj = 0, bool b_merged = false) :
        dR_(dR), pt_cut_(pt_cut), d_in_tj_(d_in_tj), b_merged_(b_merged)
        {}

    bool operator()(const TopJet & tj, const Event & event)
    {
        bool found = false;
        for (const GenParticle & gp : *event.genparticles) {
            // GenParticle const * mother1 = gp.mother(event.genparticles, 1);
            // GenParticle const * mother2 = gp.mother(event.genparticles, 2);
            // if (abs(gp.pdgId()) == 5 && mother1 && abs(mother1->pdgId()) != 6) {
            //     std::cout << "occurence " << ++counter << std::endl;
            //     std::cout << gp.pdgId();
            //     if (mother1)
            //         std::cout << " " << mother1->pdgId();
            //     if (mother2)
            //         std::cout << " " << mother2->pdgId();
            //     // if (daughter1)
            //     //     std::cout << " " << daughter1->pdgId();
            //     // if (daughter2)
            //     //     std::cout << " " << daughter2->pdgId();
            //     std::cout << std::endl;
            // }
            if (deltaR(tj, gp) <= dR_ && abs(gp.pdgId()) == 6 && gp.pt() >= pt_cut_) {
                GenParticle const * daughter1 = gp.daughter(event.genparticles, 1);
                GenParticle const * daughter2 = gp.daughter(event.genparticles, 2);
                GenParticle const * daughterW1 = NULL;
                GenParticle const * daughterW2 = NULL;
                GenParticle const * daughterB = NULL;
                if (abs(daughter1->pdgId()) ==  24) {
                    daughterW1 = daughter1->daughter(event.genparticles, 1);
                    daughterW2 = daughter1->daughter(event.genparticles, 2);
                    daughterB = daughter2;
                }
                else if (abs(daughter2->pdgId()) ==  24) {
                    daughterW1 = daughter2->daughter(event.genparticles, 1);
                    daughterW2 = daughter2->daughter(event.genparticles, 2);
                    daughterB = daughter1;
                }
                if (daughterB && daughterW1 && daughterW2 && abs(daughterW1->pdgId()) >= 1 && abs(daughterW1->pdgId()) <= 5 &&
                    abs(daughterW2->pdgId()) >= 1 && abs(daughterW2->pdgId()) <= 5) {
                    float dR_d1 = deltaR(tj, *daughterW1);
                    float dR_d2 = deltaR(tj, *daughterW2);
                    float dR_B = deltaR(tj, *daughterB);
                    if (d_in_tj_ == 1 && (dR_d1 > dR_ && dR_d2 > dR_ && dR_B > dR_))
                        continue;
                    else if (d_in_tj_ == 2 && !((dR_d1 <= dR_ && dR_d2 <= dR_) || (dR_d1 <= dR_ && dR_B <= dR_) || (dR_d2 <= dR_ && dR_B <= dR_)))
                        continue;
                    else if (d_in_tj_ == 3 && (dR_d1 > dR_ || dR_d2 > dR_ || dR_B > dR_))
                        continue;
                    if (b_merged_ && dR_B > dR_)
                        continue;
                    // std::cout << "    particle pt/eta/phi/pdgid/daughter pdgId: " << gp.pt() << "/" << gp.eta() << "/" << gp.phi() << "/" << gp.pdgId() << "/" << daughter1->pdgId() << std::endl;
                    // return true;
                    found = true;
                }
            }
        }
        // cout << "  Found right mother!\n";
        // return false;
        return found;
    }

private:
    float dR_, pt_cut_;
    int d_in_tj_;
    bool b_merged_;
    int counter = 0;
};  // HadronicTopId


class GluonToBBId
{
public:
    GluonToBBId(float dR = 0.4, float pt_cut = 0., bool d_in_tj = false) :
        dR_(dR), pt_cut_(pt_cut), d_in_tj_(d_in_tj)
        {}

    bool operator()(const TopJet & tj, const Event & event) const
    {
        int n_g_to_bb = 0;
        bool found = false;
        std::vector<GenParticle const *> bs;

        for (const GenParticle & gp : *event.genparticles) {
            if (abs(gp.pdgId()) == 5) {
                GenParticle const * mother1 = gp.mother(event.genparticles, 1);
                GenParticle const * mother2 = gp.mother(event.genparticles, 2);
                if (((mother1 && abs(mother1->pdgId()) != 6 && mother2 && abs(mother2->pdgId()) != 6)) ||
                    ((mother1 && !mother2 && abs(mother1->pdgId()) != 6) || (mother2 && !mother1 && abs(mother2->pdgId()) != 6)))
                    bs.push_back(&gp);
            }
        }
        if (bs.size() >= 2) {
            std::vector<LorentzVector> g_hyps;
            std::vector<std::pair<GenParticle const *, GenParticle const *>> b_hyps;

            for (unsigned i = 0; i < bs.size() - 1; ++i) {
                for (unsigned ii = i + 1; ii < bs.size(); ++ii) {
                    LorentzVector g_hyp(bs[i]->v4());
                    g_hyp += bs[ii]->v4();
                    g_hyps.push_back(g_hyp);
                    b_hyps.push_back(std::make_pair(bs[i], bs[ii]));
                }
            }

            for (unsigned i = 0; i < g_hyps.size(); ++i) {
                if (deltaR(tj, g_hyps[i]) <= dR_ && g_hyps[i].pt() >= pt_cut_) {
                    float dR_db1 = deltaR(tj, *(b_hyps[i].first));
                    float dR_db2 = deltaR(tj, *(b_hyps[i].second));
                    if (d_in_tj_ && (dR_db1 > dR_ || dR_db2 > dR_))
                        continue;
                    std::cout << "    Gluon splitting to BB found!" << std::endl;
                    found = true;
                    n_g_to_bb++;
                }
            }
        }
        // cout << "  Found right mother!\n";
        if (n_g_to_bb > 1)
            std::cout << "More than one gluon splitting case found, n_g_to_bb/n_bs: " << n_g_to_bb << "/" << bs.size() << std::endl;
        return found;
    }

private:
    float dR_, pt_cut_;
    bool d_in_tj_;
};  // GluonToBBId




template<typename T>
class GenPartClosestJetID
{
public:
    typedef std::function<bool (const T &, const uhh2::Event &)> TYPE_ID;

    GenPartClosestJetID(Context & ctx, string const & h_in, int id = 25, int daughter_id = 0, float dR = 0.4, float pt_cut = 0., bool d_in_tj = false,
           boost::optional<TYPE_ID> const & type_id = boost::none) :
        h_in_(ctx.get_handle<std::vector<T>>(h_in)), id_(id), daughter_id_(daughter_id), dR_(dR), pt_cut_(pt_cut), d_in_tj_(d_in_tj),
        type_id_(type_id)
        {}

    bool operator()(const GenParticle & gp, const Event & event) const
    {
        std::vector<T> const & in_coll = event.get(h_in_);
        // for (const GenParticle & gp : *event.genparticles) {
        GenParticle const * daughter1 = NULL;
        GenParticle const * daughter2 = NULL;
        if (abs(gp.pdgId()) == id_) {
            if (gp.pt() < pt_cut_)
                return false;
            if (daughter_id_) {
                daughter1 = gp.daughter(event.genparticles, 1);
                daughter2 = gp.daughter(event.genparticles, 2);
                if (!(daughter1 && abs(daughter1->pdgId()) == daughter_id_ && daughter2 && abs(daughter2->pdgId()) == daughter_id_)) {
                    // std::cout << "    particle pt/eta/phi/pdgid/daughter pdgId: " << gp.pt() << "/" << gp.eta() << "/" << gp.phi() << "/" << gp.pdgId() << "/" << daughter1->pdgId() << std::endl;
                    return false;
                }
            }
            // std::cout << "    particle pt/eta/phi/pdgid/daughter pdgId: " << gp.pt() << "/" << gp.eta() << "/" << gp.phi() << "/" << gp.pdgId() << "/" << daughter1->pdgId() << std::endl;
            for (const T & p : in_coll) {
                if (deltaR(p, gp) <= dR_) {
                    if (type_id_ && !((*type_id_)(p, event))) {
                        continue;
                    }
                    float dR_d1 = deltaR(p, *daughter1);
                    float dR_d2 = deltaR(p, *daughter2);
                    if (d_in_tj_ && (dR_d1 > dR_ || dR_d2 > dR_))
                        continue;
                    // std::cout << "    topjet pt/eta/phi/mass/csv1/csv2: " << p.pt() << "/" << p.eta() << "/" << p.phi() << "/" << p.softdropmass();
                    // if (p.subjets().size())
                    //     std::cout << "/" << p.subjets()[0].btag_combinedSecondaryVertex();
                    // if (p.subjets().size() > 1)
                    //     std::cout << "/" << p.subjets()[1].btag_combinedSecondaryVertex();
                    // std::cout << std::endl;
                    return true;
                }
            }
        }
        // }
        // cout << "  Found right mother!\n";
        return false;
    }

private:
    Event::Handle<std::vector<T>> h_in_;
    int id_, daughter_id_;
    float dR_, pt_cut_;
    bool d_in_tj_;
    boost::optional<TYPE_ID> type_id_; 
};  // GenPartClosestJetID





