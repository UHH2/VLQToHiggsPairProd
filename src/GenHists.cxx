#include "UHH2/VLQToHiggsPairProd/include/GenHists.h"
#include "UHH2/core/include/Event.h"

#include "UHH2/common/include/GenTools.h"
#include "UHH2/common/include/Utils.h"

#include "UHH2/VLQToHiggsPairProd/include/AdditionalModules.h"

#include "TH1F.h"
#include "TH2F.h"
#include <iostream>

using namespace std;
using namespace uhh2;
// using namespace vlqToHiggsPair;

namespace
{
    std::string mapPdgidToString(int id)
    {
        switch (id)
        {
            case 0:
                return "genjet";
            case 5:
                return "b";
            case 6:
                return "t";
            case 8:
                return "tprime";
            case 11:
                return "el";
            case 13:
                return "mu";
            case 24:
                return "W";
            case 25:
                return "higgs";
            default:
                std::cout << "WARNING: string conversion for this type not supported!\n";
                throw; 
        }

        return "";

    }

    void findTopProducts(std::vector<GenParticle> const * genparticles, GenParticle const * top_daughter, GenParticle const * & top_b, GenParticle const * & top_Wq1, GenParticle const * & top_Wq2)
    {
        int decayId = top_daughter->pdgId();
        if (abs(decayId) == 5)
            top_b = top_daughter;
        else if (abs(decayId) == 24)
        {
            GenParticle const * w_daughter1 = top_daughter->daughter(genparticles, 1);
            GenParticle const * w_daughter2 = top_daughter->daughter(genparticles, 2);
            if (w_daughter1 && (abs(w_daughter1->pdgId()) < 5 && abs(w_daughter1->pdgId()) > 0))
                top_Wq1 = w_daughter1;
            if (w_daughter2 && (abs(w_daughter2->pdgId()) < 5 && abs(w_daughter2->pdgId()) > 0))
                top_Wq2 = w_daughter2;
        }
        else if (abs(decayId) < 5 && abs(decayId) > 0)
        {
            std::cout << "WARNING: top decays directly into light quarks, no intermediate W boson!" << std::endl;
            top_Wq1 = top_daughter;
        }
    }

    double calcMaxDR(GenParticle const * p1, GenParticle const * p2, GenParticle const * p3)
    {
        double maxDR = 0;
        if (p1 && p2)
            maxDR = (uhh2::deltaR(*p1, *p2) > maxDR) ? uhh2::deltaR(*p1, *p2) : maxDR;
        if (p1 && p3)
            maxDR = (uhh2::deltaR(*p1, *p3) > maxDR) ? uhh2::deltaR(*p1, *p3) : maxDR;
        if (p2 && p3)
            maxDR = (uhh2::deltaR(*p2, *p3) > maxDR) ? uhh2::deltaR(*p2, *p3) : maxDR;

        return maxDR;

    }
}

std::map<int, std::pair<float, float> > GenHists::minmax_masses_ = {
        {6, std::make_pair(150.f, 250.f)}, 
        {8, std::make_pair(950.f, 1050.f)}, 
        {25, std::make_pair(110.f, 140.f)}
    };

std::map<int, std::pair<float, float> > GenHists::minmax_pts_ = {};



// using namespace genhists;

void GenHists::add_genhistcoll(int pdgid, int order_num, int mother_id, int veto_mother_id,
                            bool mass, bool charge, bool decay, bool mother)
{
    GenHistColl new_genhistcoll;
    new_genhistcoll.pdgid = pdgid;
    new_genhistcoll.mother_id = mother_id;
    new_genhistcoll.veto_mother_id = veto_mother_id;
    new_genhistcoll.order_num = order_num;

    float minpt = 0.f, maxpt, minmass, maxmass;

    try {
        minmass = minmax_masses_.at(pdgid).first;
        maxmass = minmax_masses_.at(pdgid).second;
    }
    catch (const out_of_range& e) {
        minmass = 0.f;
        maxmass = 1000.f;
    }

    try {
        minpt = minmax_pts_.at(pdgid).first;
        maxpt = minmax_pts_.at(pdgid).second;   
    }
    catch (const out_of_range& e) {
        if (pdgid < 10 || pdgid == 25)
            maxpt = 2000.f; 
        else
            maxpt = 400.f;
    }

    int n_ptbins = (maxpt-minpt)*0.1;
    int n_massbins = (maxmass-minmass)*0.2;

    std::string particle = mapPdgidToString(pdgid);
    std::string order_str = "all";
    if (order_num > 0)
        order_str = to_string(order_num);

    new_genhistcoll.h_pt = book<TH1F>(particle+"_pt_"+order_str, particle+" p_{T} "+order_str, n_ptbins, minpt, maxpt);
    new_genhistcoll.h_eta = book<TH1F>(particle+"_eta_"+order_str, particle+" eta "+order_str, 40, -2.5, 2.5);
    new_genhistcoll.h_phi = book<TH1F>(particle+"_phi_"+order_str, particle+" phi "+order_str, 64, -M_PI, M_PI);
    new_genhistcoll.h_n = order_num == 1 ? book<TH1F>(particle+"_n", particle+" number", 40, -2.5, 2.5) : NULL;
    new_genhistcoll.h_mass = mass ? book<TH1F>(particle+"_mass_"+order_str, particle+" mass "+order_str, n_massbins, minmass, maxmass) : NULL;
    new_genhistcoll.h_charge = charge ? book<TH1F>(particle+"_charge_"+order_str, particle+" charge "+order_str, 3, -1.5, 1.5) : NULL;
    new_genhistcoll.h_decay = decay ? book<TH1F>(particle+"_decay_"+order_str, particle+" decay "+order_str, 60, -30.5, 30.5) : NULL;
    new_genhistcoll.h_mother = mother ? book<TH1F>(particle+"_mother_"+order_str, particle+" mother "+order_str, 60, -30.5, 30.5) : NULL;

    all_hists_.push_back(new_genhistcoll);


}

void GenHists::fill_hists(const Particle * ipart, const std::vector<GenParticle> & genparticles,
    GenHistColl & gen_histcoll, double w)
{
    gen_histcoll.h_pt->Fill(ipart->pt(), w);
    gen_histcoll.h_eta->Fill(ipart->pt(), w);
    gen_histcoll.h_phi->Fill(ipart->pt(), w);
    if (gen_histcoll.h_mass) gen_histcoll.h_mass->Fill(ipart->v4().mass(), w);
    if (gen_histcoll.h_charge) gen_histcoll.h_charge->Fill(ipart->charge(), w);
    if (gen_histcoll.h_charge) gen_histcoll.h_charge->Fill(ipart->charge(), w);
    if (gen_histcoll.h_decay)
    {
        const GenParticle * daughter1 = ((GenParticle*)ipart)->daughter(&genparticles, 1);
        const GenParticle * daughter2 = ((GenParticle*)ipart)->daughter(&genparticles, 2);
        if (daughter1) gen_histcoll.h_decay->Fill(daughter1->pdgId(), w);
        if (daughter2) gen_histcoll.h_decay->Fill(daughter2->pdgId(), w);     
    }
    if (gen_histcoll.h_mother)
    {
        const GenParticle * mother = findMother(*((GenParticle*)ipart), &genparticles);
        if (mother) gen_histcoll.h_mother->Fill(mother->pdgId(), w);
    }
}

void GenHists::fill_genhistcoll(const uhh2::Event & event, GenHistColl & gen_histcoll)
{

    // CONTINUE HERE: enable running on genjets as well by applying some awesome casting shit

    double w = event.weight;
    const auto & genparticles = gen_histcoll > 0 ? *event.genparticles : *event.genjets;

    std::vector<const Particle*> plot_particles;

    for (const auto & genp : genparticles)
    {
        if (gen_histcoll.pdgid == 0 || std::abs(((GenParticle*)genp).pdgId()) == gen_histcoll.pdgid)
        {
            if (mother_id_ > 0 || veto_mother_id_ > 0)
            {
                bool right_mother = mother_id_ > 0 ? false : true;
                GenParticle const * gen_mother = findMother(((GenParticle*)genp), event.genparticles);
                while (gen_mother)
                {
                    if (mother_id_ > 0 && abs(gen_mother->pdgId()) == mother_id_)
                    {
                        right_mother = true;
                    }
                    else if (veto_mother_id_ > 0 && abs(gen_mother->pdgId()) == veto_mother_id_)
                    {
                        right_mother = false;
                        break;
                    }
                    gen_mother = findMother(*gen_mother, event.genparticles);
                }
                if (!right_mother)
                    continue;
            }
            plot_particles.push_back(&genp);
        }
    }

    sort_by_pt(plot_particles);

    if (gen_histcoll.h_n)
        gen_histcoll.h_n->Fill(plot_particles.size(), w);

    if (gen_histcoll.order_num < 1)
    {
        for (auto ipart : plot_particles)
        {
            fill_hists(ipart, genparticles, gen_histcoll, w);
        }
    }
    else
    {
        fill_hists(plot_particles[order_num-1], genparticles, gen_histcoll, w);
    }

}

GenHists::GenHists(Context & ctx, const string & dirname, const std::string & h_part_ht):
    Hists(ctx, dirname), ctx_(ctx), dirname_(dirname), h_part_ht_(ctx.get_handle<double>(h_part_ht))
{
    // parton ht
    spec_parton_ht = book<TH1F>("spec_parton_ht", "HT (partons)", 100, 0, 3500);

    // dR variables
    spec_deltaR_bb_h = book<TH1F>("spec_deltaR_bb_h", "#Delta R_{bb}(Higgs)", 50, 0, 5);
    spec_deltaR_bb_min = book<TH1F>("spec_deltaR_bb_min", "#Delta R_{bb}(Min)", 50, 0, 5);
    spec_max_deltaR_topprod = book<TH1F>("spec_max_deltaR_topprod", "max #Delta R(top products)", 50, 0, 5);

    spec_top_pt_vs_max_dR = book<TH2F>("spec_top_pt_vs_max_dR", ";p_{T}(t);max #Delta R(t decay products)", 150, 0, 1500, 50, 0., 5.);
}


void GenHists::fill(const Event & event){
    // // fill the histograms. Don't forget to always use the weight when filling:
    // double weight = event.weight;

    // typedef map<double, GenParticle const *> ptsort_parts;
    
    // std::vector<GenParticle> const * genparticles = event.genparticles;
    
    // GenParticle const * tp1 = 0;
    // GenParticle const * tp2 = 0;
    // GenParticle const * t1 = 0;
    // GenParticle const * t2 = 0;
    // GenParticle const * h1 = 0;
    // GenParticle const * h2 = 0;
        
    // vector<GenParticle> bs;
    // ptsort_parts electrons;
    // ptsort_parts muons;
    // ptsort_parts electrons_from_top;
    // ptsort_parts muons_from_top;
    
    // if (event.is_valid(h_part_ht_))
    //     spec_parton_ht->Fill(event.get(h_part_ht_));
    
    // for (GenParticle const & igenp : *genparticles)
    // {
    //     if (abs(igenp.pdgId()) == 8)
    //     {
    //         if (!tp1) tp1 = &igenp;
    //         else if (igenp.pt() > tp1->pt()) {tp2 = tp1; tp1 = &igenp;}
    //         else if (!tp2) tp2 = &igenp;
    //     }
    //     if (abs(igenp.pdgId()) == 6)
    //     {
    //         if (!t1) t1 = &igenp;
    //         else if (igenp.pt() > t1->pt()) {t2 = t1; t1 = &igenp;}
    //         else if (!t2) t2 = &igenp;
    //     }
    //     if (abs(igenp.pdgId()) == 25)
    //     {
    //         if (!h1) h1 = &igenp;
    //         else if (igenp.pt() > h1->pt()) {h2 = h1; h1 = &igenp;}
    //         else if (!h2) h2 = &igenp;
    //     }
    //     if (abs(igenp.pdgId()) == 5)
    //     {
    //         bs.push_back(igenp);
    //     }
    //     if (abs(igenp.pdgId()) == 11)
    //     { // electron
    //         electrons[igenp.pt()] = &igenp;
    //         GenParticle const * this_particle = &igenp;
    //         GenParticle const * mother = findMother(igenp, genparticles);
    //         while (mother)
    //         {
    //             if (abs(mother->pdgId()) == 6)
    //             {
    //                 electrons_from_top[this_particle->pt()] = this_particle;
    //                 break;
    //             }
    //             this_particle = mother;
    //             mother = findMother(*this_particle, genparticles);
    //         }
    //     }
    //     if (abs(igenp.pdgId()) == 13)
    //     { // muon
    //         muons[igenp.pt()] = &igenp;
    //         GenParticle const * this_particle = &igenp;
    //         GenParticle const * mother = findMother(igenp, genparticles);
    //         while (mother)
    //         {
    //             if (abs(mother->pdgId()) == 6)
    //             {
    //                 muons_from_top[this_particle->pt()] = this_particle;
    //                 break;
    //             }
    //             this_particle = mother;
    //             mother = findMother(*this_particle, genparticles);
    //         }
    //     }
    //     if (abs(igenp.pdgId()) == 23)
    //     {
    //         GenParticle const * daughter1 = igenp.daughter(genparticles);
    //         GenParticle const * daughter2 = igenp.daughter(genparticles, 2);
    //         int decay1 = 0;
    //         int decay2 = 0;
    //         if (daughter1) decay1 = abs(daughter1->pdgId());
    //         if (daughter2) decay2 = abs(daughter2->pdgId());
    //         z_decay->Fill(decay1, weight);
    //         z_decay->Fill(decay2, weight);
    //     }
    //     if (abs(igenp.pdgId()) == 24)
    //     {
    //         GenParticle const * daughter1 = igenp.daughter(genparticles);
    //         GenParticle const * daughter2 = igenp.daughter(genparticles, 2);
    //         int decay1 = 0;
    //         int decay2 = 0;
    //         if (daughter1) decay1 = abs(daughter1->pdgId());
    //         if (daughter2) decay2 = abs(daughter2->pdgId());
    //         w_decay->Fill(decay1, weight);
    //         w_decay->Fill(decay2, weight);
    //     }
    // }

    // genjet_N->Fill(event.genjets->size(), weight);

    // for (size_t iGenJet = 0; iGenJet < event.genjets->size(); ++iGenJet)
    // {
    //     Particle const & gen_jet = (*event.genjets)[iGenJet];
    //     if (iGenJet == 0)
    //     {
    //         genjet_pt_lead->Fill(gen_jet.pt(), weight);
    //         genjet_eta_lead->Fill(gen_jet.eta(), weight);
    //         genjet_phi_lead->Fill(gen_jet.phi(), weight);
    //     }
    //     else if (iGenJet == 1)
    //     {
    //         genjet_pt_subl->Fill(gen_jet.pt(), weight);
    //         genjet_eta_subl->Fill(gen_jet.eta(), weight);
    //         genjet_phi_subl->Fill(gen_jet.phi(), weight);
    //     }
    //     genjet_pt_all->Fill(gen_jet.pt(), weight);
    //     genjet_eta_all->Fill(gen_jet.eta(), weight);
    //     genjet_phi_all->Fill(gen_jet.phi(), weight);
    // }
    
    // t_N->Fill((bool)t1+(bool)t2, weight);
    // h_N->Fill((bool)h1+(bool)h2, weight);
    // b_N->Fill(bs.size(), weight);
    // l_N->Fill(electrons.size()+muons.size(), weight);
    // mu_N->Fill(muons.size(), weight);
    // el_N->Fill(electrons.size(), weight);
    // ltop_N->Fill(electrons_from_top.size()+muons_from_top.size(), weight);
    // mutop_N->Fill(muons_from_top.size(), weight);
    // eltop_N->Fill(electrons_from_top.size(), weight);
    
    // if (tp1) 
    // {
    //     tp_pt_lead->Fill(tp1->pt(), weight);
    //     tp_eta_lead->Fill(tp1->eta(), weight);
    //     tp_phi_lead->Fill(tp1->phi(), weight);
    //     tp_m->Fill(tp1->v4().mass(), weight);
    //     GenParticle const * daughter1 = tp1->daughter(genparticles);
    //     GenParticle const * daughter2 = tp1->daughter(genparticles, 2);
    //     int decay1 = 0;
    //     int decay2 = 0;
    //     if (daughter1) decay1 = abs(daughter1->pdgId());
    //     if (daughter2) decay2 = abs(daughter2->pdgId());
    //     tp_decay->Fill(decay1, weight);
    //     tp_decay->Fill(decay2, weight);
    // }
    
    // if (tp2) 
    // {
    //     tp_pt_subl->Fill(tp2->pt(), weight);
    //     tp_eta_subl->Fill(tp2->eta(), weight);
    //     tp_phi_subl->Fill(tp2->phi(), weight);
    //     tp_m->Fill(tp2->v4().mass(), weight);
    //     GenParticle const * daughter1 = tp2->daughter(genparticles);
    //     GenParticle const * daughter2 = tp2->daughter(genparticles, 2);
    //     int decay1 = 0;
    //     int decay2 = 0;
    //     if (daughter1) decay1 = abs(daughter1->pdgId());
    //     if (daughter2) decay2 = abs(daughter2->pdgId());
    //     tp_decay->Fill(decay1, weight);
    //     tp_decay->Fill(decay2, weight);
    // }
    
    // if (t1) 
    // {
    //     t_pt_lead->Fill(t1->pt(), weight);
    //     t_eta_lead->Fill(t1->eta(), weight);
    //     t_phi_lead->Fill(t1->phi(), weight);
    //     t_m->Fill(t1->v4().mass(), weight);
    //     GenParticle const * daughter1 = t1->daughter(genparticles, 1);
    //     GenParticle const * daughter2 = t1->daughter(genparticles, 2);
    //     GenParticle const * top_b = 0;
    //     GenParticle const * top_Wq1 = 0;
    //     GenParticle const * top_Wq2 = 0;
    //     int decay1 = 0;
    //     int decay2 = 0;
    //     if (daughter1)
    //     {
    //         decay1 = daughter1->pdgId();
    //         findTopProducts(genparticles, daughter1, top_b, top_Wq1, top_Wq2);
    //     }
    //     if (daughter2)
    //     {
    //         decay2 = daughter2->pdgId();
    //         findTopProducts(genparticles, daughter2, top_b, top_Wq1, top_Wq2);
    //     }

    //     double max_deltaR_topprod = calcMaxDR(top_b, top_Wq1, top_Wq2);

    //     if (max_deltaR_topprod)
    //     {
    //         spec_max_deltaR_topprod->Fill(max_deltaR_topprod, weight);
    //         spec_top_pt_vs_max_dR->Fill(t1->pt(), max_deltaR_topprod, weight);
    //     }

    //     t_decay->Fill(decay1, weight);
    //     t_decay->Fill(decay2, weight);
    // }
    
    // if (t2) 
    // {
    //     t_pt_subl->Fill(t2->pt(), weight);
    //     t_eta_subl->Fill(t2->eta(), weight);
    //     t_phi_subl->Fill(t2->phi(), weight);
    //     t_m->Fill(t2->v4().mass(), weight);
    //     GenParticle const * daughter1 = t2->daughter(genparticles, 1);
    //     GenParticle const * daughter2 = t2->daughter(genparticles, 2);
    //     GenParticle const * top_b = 0;
    //     GenParticle const * top_Wq1 = 0;
    //     GenParticle const * top_Wq2 = 0;
    //     int decay1 = 0;
    //     int decay2 = 0;
    //     if (daughter1)
    //     {
    //         decay1 = daughter1->pdgId();
    //         findTopProducts(genparticles, daughter1, top_b, top_Wq1, top_Wq2);
    //     }
    //     if (daughter2)
    //     {
    //         decay2 = daughter2->pdgId();
    //         findTopProducts(genparticles, daughter2, top_b, top_Wq1, top_Wq2);
    //     }

    //     double max_deltaR_topprod = calcMaxDR(top_b, top_Wq1, top_Wq2);

    //     if (max_deltaR_topprod)
    //     {
    //         spec_max_deltaR_topprod->Fill(max_deltaR_topprod, weight);
    //     }

    //     t_decay->Fill(decay1, weight);
    //     t_decay->Fill(decay2, weight);
    // }
    
    // if (h1)
    // {
    //     h_pt_lead->Fill(h1->pt(), weight);
    //     h_eta_lead->Fill(h1->eta(), weight);
    //     h_phi_lead->Fill(h1->phi(), weight);
    //     h_m->Fill(h1->v4().mass(), weight);
    //     GenParticle const * daughter1 = h1->daughter(genparticles);
    //     GenParticle const * daughter2 = h1->daughter(genparticles, 2);
    //     int decay1 = 0;
    //     int decay2 = 0;
    //     if (daughter1) decay1 = daughter1->pdgId();
    //     if (daughter2) decay2 = daughter2->pdgId();
    //     h_decay->Fill(decay1, weight);
    //     h_decay->Fill(decay2, weight);
    // }
    
    // if (h2)
    // {
    //     h_pt_subl->Fill(h2->pt(), weight);
    //     h_eta_subl->Fill(h2->eta(), weight);
    //     h_phi_subl->Fill(h2->phi(), weight);
    //     h_m->Fill(h2->v4().mass(), weight);
    //     GenParticle const * daughter1 = h2->daughter(genparticles);
    //     GenParticle const * daughter2 = h2->daughter(genparticles, 2);
    //     int decay1 = 0;
    //     int decay2 = 0;
    //     if (daughter1) decay1 = daughter1->pdgId();
    //     if (daughter2) decay2 = daughter2->pdgId();
    //     h_decay->Fill(decay1, weight);
    //     h_decay->Fill(decay2, weight);
    // }

    // if (electrons.size())
    // {
    //     std::reverse_iterator<ptsort_parts::iterator> sort_part = electrons.rbegin();
    //     el_pt_lead->Fill(sort_part->second->pt(), weight);
    //     el_pt_lead2->Fill(sort_part->second->pt(), weight);
    //     el_eta_lead->Fill(sort_part->second->eta(), weight);
    //     el_phi_lead->Fill(sort_part->second->phi(), weight);
    //     if (electrons.size() > 1)
    //     {
    //         sort_part++;
    //         el_pt_subl->Fill(sort_part->second->pt(), weight);
    //         el_pt_subl2->Fill(sort_part->second->pt(), weight);
    //         el_eta_subl->Fill(sort_part->second->eta(), weight);
    //         el_phi_subl->Fill(sort_part->second->phi(), weight);
    //     }
    // }

    // if (muons.size())
    // {
    //     std::reverse_iterator<ptsort_parts::iterator> sort_part = muons.rbegin();
    //     mu_pt_lead->Fill(sort_part->second->pt(), weight);
    //     mu_pt_lead2->Fill(sort_part->second->pt(), weight);
    //     mu_eta_lead->Fill(sort_part->second->eta(), weight);
    //     mu_phi_lead->Fill(sort_part->second->phi(), weight);
    //     if (muons.size() > 1)
    //     {
    //         sort_part++;
    //         mu_pt_subl->Fill(sort_part->second->pt(), weight);
    //         mu_pt_subl2->Fill(sort_part->second->pt(), weight);
    //         mu_eta_subl->Fill(sort_part->second->eta(), weight);
    //         mu_phi_subl->Fill(sort_part->second->phi(), weight);
    //     }
    // }

    // if (electrons_from_top.size())
    // {
    //     std::reverse_iterator<ptsort_parts::iterator> sort_part = electrons_from_top.rbegin();
    //     eltop_pt_lead->Fill(sort_part->second->pt(), weight);
    //     eltop_pt_lead2->Fill(sort_part->second->pt(), weight);
    //     eltop_eta_lead->Fill(sort_part->second->eta(), weight);
    //     eltop_phi_lead->Fill(sort_part->second->phi(), weight);
    //     if (electrons_from_top.size() > 1)
    //     {
    //         sort_part++;
    //         eltop_pt_subl->Fill(sort_part->second->pt(), weight);
    //         eltop_pt_subl2->Fill(sort_part->second->pt(), weight);
    //         eltop_eta_subl->Fill(sort_part->second->eta(), weight);
    //         eltop_phi_subl->Fill(sort_part->second->phi(), weight);
    //     }
    // }

    // if (muons_from_top.size())
    // {
    //     std::reverse_iterator<ptsort_parts::iterator> sort_part = muons_from_top.rbegin();
    //     mutop_pt_lead->Fill(sort_part->second->pt(), weight);
    //     mutop_pt_lead2->Fill(sort_part->second->pt(), weight);
    //     mutop_eta_lead->Fill(sort_part->second->eta(), weight);
    //     mutop_phi_lead->Fill(sort_part->second->phi(), weight);
    //     if (muons_from_top.size() > 1)
    //     {
    //         sort_part++;
    //         mutop_pt_subl->Fill(sort_part->second->pt(), weight);
    //         mutop_pt_subl2->Fill(sort_part->second->pt(), weight);
    //         mutop_eta_subl->Fill(sort_part->second->eta(), weight);
    //         mutop_phi_subl->Fill(sort_part->second->phi(), weight);
    //     }
    // }

    // // fill all b-related histograms
    
    // double bTpPt_lead = 0.;
    // double bTpPt_subl = 0.;
    // double bHPt_lead = 0.;
    // double bHPt_subl = 0.;
    
    // for (vector<GenParticle>::const_iterator it = bs.begin(); it != bs.end(); ++it)
    // {
    //     GenParticle const * ib = &*it;
    //     GenParticle const * daughter1 = ib->daughter(genparticles, 1);
    //     GenParticle const * daughter2 = ib->daughter(genparticles, 2);
    //     int decay1 = 0;
    //     int decay2 = 0;
    //     if (daughter1) decay1 = daughter1->pdgId();
    //     if (daughter2) decay2 = daughter2->pdgId();
    //     b_decay->Fill(decay1, weight);
    //     b_decay->Fill(decay2, weight);
    //     GenParticle const * closestB = closestParticle(*ib, bs);
    //     if (closestB)
    //         spec_deltaR_bb_min->Fill(deltaR(*ib, *closestB), weight);
    //     GenParticle const * imother = findMother(*ib, genparticles);
    //     if (!imother) continue;
    //     if (abs(imother->pdgId()) == 8)
    //     {
    //         if (ib->pt() > bTpPt_lead) {bTpPt_subl = bTpPt_lead; bTpPt_lead = ib->pt();}
    //         else if (ib->pt() > bTpPt_subl) bTpPt_subl = ib->pt();
    //     }
    //     else if (abs(imother->pdgId()) == 25)
    //     {
    //         if (ib->pt() > bHPt_lead) {bHPt_subl = bHPt_lead; bHPt_lead = ib->pt();}
    //         else if (ib->pt() > bHPt_subl) bHPt_subl = ib->pt();
    //         for (vector<GenParticle>::const_iterator iit = it+1; iit != bs.end(); ++iit)
    //         {
    //             GenParticle const * ib2 = &*iit;
    //             GenParticle const * imother2 = findMother(*ib2, genparticles);
    //             if (!imother2) continue;
    //             if (imother->index() == imother2->index())
    //             {
    //                 double dR = deltaR(*ib, *ib2);
    //                 spec_deltaR_bb_h->Fill(dR, weight);
    //                 break;
    //             }
    //         }
    //     }
    // }
    
    // if (bTpPt_lead) bTp_pt_lead->Fill(bTpPt_lead, weight);
    // if (bTpPt_subl) bTp_pt_subl->Fill(bTpPt_subl, weight);
    // if (bHPt_lead) bH_pt_lead->Fill(bHPt_lead, weight);
    // if (bHPt_subl) bH_pt_subl->Fill(bHPt_subl, weight);
    
//     if (b1 && b2){
//         double deltaR = b1->deltaR(*b2);
// //         cout << "Test2" << endl;
//         DeltaR_bb->Fill(deltaR, weight);
// //         cout << "Test3" << endl;
//     }
    
//     cout << "Test4" << endl;
  
  
}

GenHists::~GenHists(){}
