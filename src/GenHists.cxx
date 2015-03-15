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
using namespace vlqToHiggsPair;

namespace genhists
{
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

using namespace genhists;

GenHists::GenHists(Context & ctx, const string & dirname): Hists(ctx, dirname){
    
    // TODO: pass handle when constructing the histogram to avoid hard coding handle names here
    h_part_ht_ = ctx.get_handle<double>("parton_ht");

    tp_pt_lead = book<TH1F>("tp_pt_lead", "p_{T, T'}(lead) [GeV/c]", 200, 0, 2000);
    tp_pt_subl = book<TH1F>("tp_pt_subl", "p_{T, T'}(sublead) [GeV/c]", 200, 0, 2000);
    tp_eta_lead = book<TH1F>("tp_eta_lead", "#eta_{T'}(lead)", 40, -2.5, 2.5);
    tp_eta_subl = book<TH1F>("tp_eta_subl", "#eta_{T'}(sublead)", 40, -2.5, 2.5);
    tp_phi_lead = book<TH1F>("tp_phi_lead", "#phi_{T'}(lead)", 64, -3.2, 3.2);
    tp_phi_subl = book<TH1F>("tp_phi_subl", "#phi_{T'}(sublead)", 64, -3.2, 3.2);

    t_pt_lead = book<TH1F>("t_pt_lead", "p_{T, top}(lead) [GeV/c]", 200, 0, 2000);
    t_pt_subl = book<TH1F>("t_pt_subl", "p_{T, top}(sublead) [GeV/c]", 200, 0, 2000);
    t_eta_lead = book<TH1F>("t_eta_lead", "#eta_{top}(lead)", 40, -2.5, 2.5);
    t_eta_subl = book<TH1F>("t_eta_subl", "#eta_{top}(sublead)", 40, -2.5, 2.5);
    t_phi_lead = book<TH1F>("t_phi_lead", "#phi_{top}(lead)", 64, -3.2, 3.2);
    t_phi_subl = book<TH1F>("t_phi_subl", "#phi_{top}(sublead)", 64, -3.2, 3.2);

    h_pt_lead = book<TH1F>("h_pt_lead", "p_{T, H}(lead) [GeV/c]", 200, 0, 2000);
    h_pt_subl = book<TH1F>("h_pt_subl", "p_{T, H}(sublead) [GeV/c]", 200, 0, 2000);
    h_eta_lead = book<TH1F>("h_eta_lead", "#eta_{H}(lead)", 40, -2.5, 2.5);
    h_eta_subl = book<TH1F>("h_eta_subl", "#eta_{H}(sublead)", 40, -2.5, 2.5);
    h_phi_lead = book<TH1F>("h_phi_lead", "#phi_{H}(lead)", 64, -3.2, 3.2);
    h_phi_subl = book<TH1F>("h_phi_subl", "#phi_{H}(sublead)", 64, -3.2, 3.2);

    bTp_pt_lead = book<TH1F>("bTp_pt_lead", "p_{T, b(T')}(lead) [GeV/c]", 200, 0, 2000);
    bTp_pt_subl = book<TH1F>("bTp_pt_subl", "p_{T, b(T')}(sublead) [GeV/c]", 200, 0, 2000);
    bH_pt_lead = book<TH1F>("bH_pt_lead", "p_{T, b(H)}(lead) [GeV/c]", 200, 0, 2000);
    bH_pt_subl = book<TH1F>("bH_pt_subl", "p_{T, b(H)}(sublead) [GeV/c]", 200, 0, 2000);

    mu_pt_lead = book<TH1F>("mu_pt_lead", "p_{T, mu}(lead) [GeV/c]", 50, 0, 500);
    mu_pt_subl = book<TH1F>("mu_pt_subl", "p_{T, mu}(sublead) [GeV/c]", 50, 0, 500);
    mu_eta_lead = book<TH1F>("mu_eta_lead", "#eta_{mu}(lead)", 40, -2.5, 2.5);
    mu_eta_subl = book<TH1F>("mu_eta_subl", "#eta_{mu}(sublead)", 40, -2.5, 2.5);
    mu_phi_lead = book<TH1F>("mu_phi_lead", "#phi_{mu}(lead)", 64, -3.2, 3.2);
    mu_phi_subl = book<TH1F>("mu_phi_subl", "#phi_{mu}(sublead)", 64, -3.2, 3.2);

    el_pt_lead = book<TH1F>("el_pt_lead", "p_{T, el}(lead) [GeV/c]", 50, 0, 500);
    el_pt_subl = book<TH1F>("el_pt_subl", "p_{T, el}(sublead) [GeV/c]", 50, 0, 500);
    el_eta_lead = book<TH1F>("el_eta_lead", "#eta_{el}(lead)", 40, -2.5, 2.5);
    el_eta_subl = book<TH1F>("el_eta_subl", "#eta_{el}(sublead)", 40, -2.5, 2.5);
    el_phi_lead = book<TH1F>("el_phi_lead", "#phi_{el}(lead)", 64, -3.2, 3.2);
    el_phi_subl = book<TH1F>("el_phi_subl", "#phi_{el}(sublead)", 64, -3.2, 3.2);

    mutop_pt_lead = book<TH1F>("mutop_pt_lead", "p_{T, mutop}(lead) [GeV/c]", 60, 0, 600);
    mutop_pt_subl = book<TH1F>("mutop_pt_subl", "p_{T, mutop}(sublead) [GeV/c]", 60, 0, 600);
    mutop_eta_lead = book<TH1F>("mutop_eta_lead", "#eta_{mutop}(lead)", 40, -2.5, 2.5);
    mutop_eta_subl = book<TH1F>("mutop_eta_subl", "#eta_{mutop}(sublead)", 40, -2.5, 2.5);
    mutop_phi_lead = book<TH1F>("mutop_phi_lead", "#phi_{mutop}(lead)", 64, -3.2, 3.2);
    mutop_phi_subl = book<TH1F>("mutop_phi_subl", "#phi_{mutop}(sublead)", 64, -3.2, 3.2);

    eltop_pt_lead = book<TH1F>("eltop_pt_lead", "p_{T, eltop}(lead) [GeV/c]", 60, 0, 600);
    eltop_pt_subl = book<TH1F>("eltop_pt_subl", "p_{T, eltop}(sublead) [GeV/c]", 60, 0, 600);
    eltop_eta_lead = book<TH1F>("eltop_eta_lead", "#eta_{eltop}(lead)", 40, -2.5, 2.5);
    eltop_eta_subl = book<TH1F>("eltop_eta_subl", "#eta_{eltop}(sublead)", 40, -2.5, 2.5);
    eltop_phi_lead = book<TH1F>("eltop_phi_lead", "#phi_{eltop}(lead)", 64, -3.2, 3.2);
    eltop_phi_subl = book<TH1F>("eltop_phi_subl", "#phi_{eltop}(sublead)", 64, -3.2, 3.2);

    tp_m = book<TH1F>("tp_m", "m_{T'} [GeV]", 200, 950, 1050);
    t_m = book<TH1F>("t_m", "m_{t} [GeV]", 200, 150, 250);
    h_m = book<TH1F>("h_m", "m_{H} [GeV]", 60, 110, 140);


      //  number plots
    t_N = book<TH1F>("t_N", "Number of tops", 5, 0, 5);
    h_N = book<TH1F>("h_N", "Number of Higgses", 5, 0, 5);
    b_N = book<TH1F>("b_N", "Number of bs", 8, 0, 8);
    l_N = book<TH1F>("l_N", "Number of leptons", 15, 0, 15);
    mu_N = book<TH1F>("mu_N", "Number of muons", 15, 0, 15);
    el_N = book<TH1F>("el_N", "Number of electrons", 15, 0, 15);
    ltop_N = book<TH1F>("ltop_N", "Number of leptons from top", 15, 0, 15);
    mutop_N = book<TH1F>("mutop_N", "Number of muons from top", 15, 0, 15);
    eltop_N = book<TH1F>("eltop_N", "Number of electrons from top", 15, 0, 15);


    // decay modes
    tp_decay = book<TH1F>("tp_decay", "Tprime decay modes", 30, 0, 30);
    h_decay = book<TH1F>("h_decay", "Higgs decay modes", 30, 0, 30);
    t_decay = book<TH1F>("t_decay", "Top decay modes", 30, 0, 30);
    b_decay = book<TH1F>("b_decay", "B decay modes", 30, 0, 30);
    w_decay = book<TH1F>("w_decay", "W decay modes", 30, 0, 30);
    z_decay = book<TH1F>("z_decay", "Z decay modes", 30, 0, 30);

    // parton ht
    spec_parton_ht = book<TH1F>("spec_parton_ht", "HT (partons)", 100, 0, 3500);

    // dR variables
    spec_deltaR_bb_h = book<TH1F>("spec_deltaR_bb_h", "#Delta R_{bb}(Higgs)", 50, 0, 5);
    spec_deltaR_bb_min = book<TH1F>("spec_deltaR_bb_min", "#Delta R_{bb}(Min)", 50, 0, 5);
    spec_max_deltaR_topprod = book<TH1F>("spec_max_deltaR_topprod", "max #Delta R(top products)", 50, 0, 5);

    spec_top_pt_vs_max_dR = book<TH2F>("spec_top_pt_vs_max_dR", ";p_{T}(t);max #Delta R(t decay products)", 150, 0, 1500, 50, 0., 5.);
}


void GenHists::fill(const Event & event){
    // fill the histograms. Don't forget to always use the weight when filling:
    //     double weight = event.weight;

    typedef map<double, GenParticle const *> ptsort_parts;
    
    std::vector<GenParticle> const * genparticles = event.genparticles;
    
    GenParticle const * tp1 = 0;
    GenParticle const * tp2 = 0;
    GenParticle const * t1 = 0;
    GenParticle const * t2 = 0;
    GenParticle const * h1 = 0;
    GenParticle const * h2 = 0;
        
    vector<GenParticle> bs;
    ptsort_parts electrons;
    ptsort_parts muons;
    ptsort_parts electrons_from_top;
    ptsort_parts muons_from_top;
    
    if (event.is_valid(h_part_ht_))
        spec_parton_ht->Fill(event.get(h_part_ht_));
    
    for (GenParticle const & igenp : *genparticles)
    {
        if (abs(igenp.pdgId()) == 8)
        {
            if (!tp1) tp1 = &igenp;
            else if (igenp.pt() > tp1->pt()) {tp2 = tp1; tp1 = &igenp;}
            else if (!tp2) tp2 = &igenp;
        }
        if (abs(igenp.pdgId()) == 6)
        {
            if (!t1) t1 = &igenp;
            else if (igenp.pt() > t1->pt()) {t2 = t1; t1 = &igenp;}
            else if (!t2) t2 = &igenp;
        }
        if (abs(igenp.pdgId()) == 25)
        {
            if (!h1) h1 = &igenp;
            else if (igenp.pt() > h1->pt()) {h2 = h1; h1 = &igenp;}
            else if (!h2) h2 = &igenp;
        }
        if (abs(igenp.pdgId()) == 5)
        {
            bs.push_back(igenp);
        }
        if (abs(igenp.pdgId()) == 11)
        { // electron
            electrons[igenp.pt()] = &igenp;
            GenParticle const * this_particle = &igenp;
            GenParticle const * mother = findMother(igenp, genparticles);
            while (mother)
            {
                if (abs(mother->pdgId()) == 6)
                {
                    electrons_from_top[this_particle->pt()] = this_particle;
                    break;
                }
                this_particle = mother;
                mother = findMother(*this_particle, genparticles);
            }
        }
        if (abs(igenp.pdgId()) == 13)
        { // muon
            muons[igenp.pt()] = &igenp;
            GenParticle const * this_particle = &igenp;
            GenParticle const * mother = findMother(igenp, genparticles);
            while (mother)
            {
                if (abs(mother->pdgId()) == 6)
                {
                    muons_from_top[this_particle->pt()] = this_particle;
                    break;
                }
                this_particle = mother;
                mother = findMother(*this_particle, genparticles);
            }
        }
        if (abs(igenp.pdgId()) == 23)
        {
            GenParticle const * daughter1 = igenp.daughter(genparticles);
            GenParticle const * daughter2 = igenp.daughter(genparticles, 2);
            int decay1 = 0;
            int decay2 = 0;
            if (daughter1) decay1 = abs(daughter1->pdgId());
            if (daughter2) decay2 = abs(daughter2->pdgId());
            z_decay->Fill(decay1);
            z_decay->Fill(decay2);
        }
        if (abs(igenp.pdgId()) == 24)
        {
            GenParticle const * daughter1 = igenp.daughter(genparticles);
            GenParticle const * daughter2 = igenp.daughter(genparticles, 2);
            int decay1 = 0;
            int decay2 = 0;
            if (daughter1) decay1 = abs(daughter1->pdgId());
            if (daughter2) decay2 = abs(daughter2->pdgId());
            w_decay->Fill(decay1);
            w_decay->Fill(decay2);
        }
    }
    
    t_N->Fill((bool)t1+(bool)t2);
    h_N->Fill((bool)h1+(bool)h2);
    b_N->Fill(bs.size());
    l_N->Fill(electrons.size()+muons.size());
    mu_N->Fill(muons.size());
    el_N->Fill(electrons.size());
    ltop_N->Fill(electrons_from_top.size()+muons_from_top.size());
    mutop_N->Fill(muons_from_top.size());
    eltop_N->Fill(electrons_from_top.size());
    
    if (tp1) 
    {
        tp_pt_lead->Fill(tp1->pt());
        tp_eta_lead->Fill(tp1->eta());
        tp_phi_lead->Fill(tp1->phi());
        tp_m->Fill(tp1->v4().mass());
        GenParticle const * daughter1 = tp1->daughter(genparticles);
        GenParticle const * daughter2 = tp1->daughter(genparticles, 2);
        int decay1 = 0;
        int decay2 = 0;
        if (daughter1) decay1 = abs(daughter1->pdgId());
        if (daughter2) decay2 = abs(daughter2->pdgId());
        tp_decay->Fill(decay1);
        tp_decay->Fill(decay2);
    }
    
    if (tp2) 
    {
        tp_pt_subl->Fill(tp2->pt());
        tp_eta_subl->Fill(tp2->eta());
        tp_phi_subl->Fill(tp2->phi());
        tp_m->Fill(tp2->v4().mass());
        GenParticle const * daughter1 = tp2->daughter(genparticles);
        GenParticle const * daughter2 = tp2->daughter(genparticles, 2);
        int decay1 = 0;
        int decay2 = 0;
        if (daughter1) decay1 = abs(daughter1->pdgId());
        if (daughter2) decay2 = abs(daughter2->pdgId());
        tp_decay->Fill(decay1);
        tp_decay->Fill(decay2);
    }
    
    if (t1) 
    {
        t_pt_lead->Fill(t1->pt());
        t_eta_lead->Fill(t1->eta());
        t_phi_lead->Fill(t1->phi());
        t_m->Fill(t1->v4().mass());
        GenParticle const * daughter1 = t1->daughter(genparticles, 1);
        GenParticle const * daughter2 = t1->daughter(genparticles, 2);
        GenParticle const * top_b = 0;
        GenParticle const * top_Wq1 = 0;
        GenParticle const * top_Wq2 = 0;
        int decay1 = 0;
        int decay2 = 0;
        if (daughter1)
        {
            decay1 = daughter1->pdgId();
            findTopProducts(genparticles, daughter1, top_b, top_Wq1, top_Wq2);
        }
        if (daughter2)
        {
            decay2 = daughter2->pdgId();
            findTopProducts(genparticles, daughter2, top_b, top_Wq1, top_Wq2);
        }

        double max_deltaR_topprod = calcMaxDR(top_b, top_Wq1, top_Wq2);

        if (max_deltaR_topprod)
        {
            spec_max_deltaR_topprod->Fill(max_deltaR_topprod);
            spec_top_pt_vs_max_dR->Fill(t1->pt(), max_deltaR_topprod);
        }

        t_decay->Fill(decay1);
        t_decay->Fill(decay2);
    }
    
    if (t2) 
    {
        t_pt_subl->Fill(t2->pt());
        t_eta_subl->Fill(t2->eta());
        t_phi_subl->Fill(t2->phi());
        t_m->Fill(t2->v4().mass());
        GenParticle const * daughter1 = t2->daughter(genparticles, 1);
        GenParticle const * daughter2 = t2->daughter(genparticles, 2);
        GenParticle const * top_b = 0;
        GenParticle const * top_Wq1 = 0;
        GenParticle const * top_Wq2 = 0;
        int decay1 = 0;
        int decay2 = 0;
        if (daughter1)
        {
            decay1 = daughter1->pdgId();
            findTopProducts(genparticles, daughter1, top_b, top_Wq1, top_Wq2);
        }
        if (daughter2)
        {
            decay2 = daughter2->pdgId();
            findTopProducts(genparticles, daughter2, top_b, top_Wq1, top_Wq2);
        }

        double max_deltaR_topprod = calcMaxDR(top_b, top_Wq1, top_Wq2);

        if (max_deltaR_topprod)
        {
            spec_max_deltaR_topprod->Fill(max_deltaR_topprod);
        }

        t_decay->Fill(decay1);
        t_decay->Fill(decay2);
    }
    
    if (h1)
    {
        h_pt_lead->Fill(h1->pt());
        h_eta_lead->Fill(h1->eta());
        h_phi_lead->Fill(h1->phi());
        h_m->Fill(h1->v4().mass());
        GenParticle const * daughter1 = h1->daughter(genparticles);
        GenParticle const * daughter2 = h1->daughter(genparticles, 2);
        int decay1 = 0;
        int decay2 = 0;
        if (daughter1) decay1 = daughter1->pdgId();
        if (daughter2) decay2 = daughter2->pdgId();
        h_decay->Fill(decay1);
        h_decay->Fill(decay2);
    }
    
    if (h2)
    {
        h_pt_subl->Fill(h2->pt());
        h_eta_subl->Fill(h2->eta());
        h_phi_subl->Fill(h2->phi());
        h_m->Fill(h2->v4().mass());
        GenParticle const * daughter1 = h2->daughter(genparticles);
        GenParticle const * daughter2 = h2->daughter(genparticles, 2);
        int decay1 = 0;
        int decay2 = 0;
        if (daughter1) decay1 = daughter1->pdgId();
        if (daughter2) decay2 = daughter2->pdgId();
        h_decay->Fill(decay1);
        h_decay->Fill(decay2);
    }

    if (electrons.size())
    {
        std::reverse_iterator<ptsort_parts::iterator> sort_part = electrons.rbegin();
        el_pt_lead->Fill(sort_part->second->pt());
        el_eta_lead->Fill(sort_part->second->eta());
        el_phi_lead->Fill(sort_part->second->phi());
        if (electrons.size() > 1)
        {
            sort_part++;
            el_pt_subl->Fill(sort_part->second->pt());
            el_eta_subl->Fill(sort_part->second->eta());
            el_phi_subl->Fill(sort_part->second->phi());
        }
    }

    if (muons.size())
    {
        std::reverse_iterator<ptsort_parts::iterator> sort_part = muons.rbegin();
        mu_pt_lead->Fill(sort_part->second->pt());
        mu_eta_lead->Fill(sort_part->second->eta());
        mu_phi_lead->Fill(sort_part->second->phi());
        if (muons.size() > 1)
        {
            sort_part++;
            mu_pt_subl->Fill(sort_part->second->pt());
            mu_eta_subl->Fill(sort_part->second->eta());
            mu_phi_subl->Fill(sort_part->second->phi());
        }
    }

    if (electrons_from_top.size())
    {
        std::reverse_iterator<ptsort_parts::iterator> sort_part = electrons_from_top.rbegin();
        eltop_pt_lead->Fill(sort_part->second->pt());
        eltop_eta_lead->Fill(sort_part->second->eta());
        eltop_phi_lead->Fill(sort_part->second->phi());
        if (electrons_from_top.size() > 1)
        {
            sort_part++;
            eltop_pt_subl->Fill(sort_part->second->pt());
            eltop_eta_subl->Fill(sort_part->second->eta());
            eltop_phi_subl->Fill(sort_part->second->phi());
        }
    }

    if (muons_from_top.size())
    {
        std::reverse_iterator<ptsort_parts::iterator> sort_part = muons_from_top.rbegin();
        mutop_pt_lead->Fill(sort_part->second->pt());
        mutop_eta_lead->Fill(sort_part->second->eta());
        mutop_phi_lead->Fill(sort_part->second->phi());
        if (muons_from_top.size() > 1)
        {
            sort_part++;
            mutop_pt_subl->Fill(sort_part->second->pt());
            mutop_eta_subl->Fill(sort_part->second->eta());
            mutop_phi_subl->Fill(sort_part->second->phi());
        }
    }

    // fill all b-related histograms
    
    double bTpPt_lead = 0.;
    double bTpPt_subl = 0.;
    double bHPt_lead = 0.;
    double bHPt_subl = 0.;
    
    for (vector<GenParticle>::const_iterator it = bs.begin(); it != bs.end(); ++it)
    {
        GenParticle const * ib = &*it;
        GenParticle const * daughter1 = ib->daughter(genparticles, 1);
        GenParticle const * daughter2 = ib->daughter(genparticles, 2);
        int decay1 = 0;
        int decay2 = 0;
        if (daughter1) decay1 = daughter1->pdgId();
        if (daughter2) decay2 = daughter2->pdgId();
        b_decay->Fill(decay1);
        b_decay->Fill(decay2);
        GenParticle const * closestB = closestParticle(*ib, bs);
        if (closestB)
            spec_deltaR_bb_min->Fill(deltaR(*ib, *closestB));
        GenParticle const * imother = findMother(*ib, genparticles);
        if (!imother) continue;
        if (abs(imother->pdgId()) == 8)
        {
            if (ib->pt() > bTpPt_lead) {bTpPt_subl = bTpPt_lead; bTpPt_lead = ib->pt();}
            else if (ib->pt() > bTpPt_subl) bTpPt_subl = ib->pt();
        }
        else if (abs(imother->pdgId()) == 25)
        {
            if (ib->pt() > bHPt_lead) {bHPt_subl = bHPt_lead; bHPt_lead = ib->pt();}
            else if (ib->pt() > bHPt_subl) bHPt_subl = ib->pt();
            for (vector<GenParticle>::const_iterator iit = it+1; iit != bs.end(); ++iit)
            {
                GenParticle const * ib2 = &*iit;
                GenParticle const * imother2 = findMother(*ib2, genparticles);
                if (!imother2) continue;
                if (imother->index() == imother2->index())
                {
                    double dR = deltaR(*ib, *ib2);
                    spec_deltaR_bb_h->Fill(dR);
                    break;
                }
            }
        }
    }
    
    if (bTpPt_lead) bTp_pt_lead->Fill(bTpPt_lead);
    if (bTpPt_subl) bTp_pt_subl->Fill(bTpPt_subl);
    if (bHPt_lead) bH_pt_lead->Fill(bHPt_lead);
    if (bHPt_subl) bH_pt_subl->Fill(bHPt_subl);
    
//     if (b1 && b2){
//         double deltaR = b1->deltaR(*b2);
// //         cout << "Test2" << endl;
//         DeltaR_bb->Fill(deltaR);
// //         cout << "Test3" << endl;
//     }
    
//     cout << "Test4" << endl;
  
  
}

GenHists::~GenHists(){}
