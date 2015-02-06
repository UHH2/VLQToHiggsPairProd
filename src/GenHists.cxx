#include "UHH2/VLQToHiggsPairProd/include/GenHists.h"
#include "UHH2/core/include/Event.h"

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
    // book all histograms here
    // kinematical variables 
    book<TH1F>("eta_lead", "#eta_{T'}(lead)", 40, -2.5, 2.5);
    book<TH1F>("eta_subl", "#eta_{T'}(sublead)", 40, -2.5, 2.5);

    book<TH1F>("phi_lead", "#phi_{T'}(lead)", 64, -3.2, 3.2);
    book<TH1F>("phi_subl", "#phi_{T'}(sublead)", 64, -3.2, 3.2);

    book<TH1F>("tpPt_lead", "p_{T}^{T'}(lead) [GeV/c]", 200, 0, 2000);
    book<TH1F>("tpPt_subl", "p_{T}^{T'}(sublead) [GeV/c]", 200, 0, 2000);
    book<TH1F>("tPt_lead", "p_{T}^{top}(lead) [GeV/c]", 200, 0, 2000);
    book<TH1F>("tPt_subl", "p_{T}^{top}(sublead) [GeV/c]", 200, 0, 2000);
    book<TH1F>("hPt_lead", "p_{T}^{H}(lead) [GeV/c]", 200, 0, 2000);
    book<TH1F>("hPt_subl", "p_{T}^{H}(sublead) [GeV/c]", 200, 0, 2000);

    book<TH1F>("bTpPt_lead", "p_{T}^{b(T')}(lead) [GeV/c]", 200, 0, 2000);
    book<TH1F>("bTpPt_subl", "p_{T}^{b(T')}(sublead) [GeV/c]", 200, 0, 2000);
    book<TH1F>("bHPt_lead", "p_{T}^{b(H)}(lead) [GeV/c]", 200, 0, 2000);
    book<TH1F>("bHPt_subl", "p_{T}^{b(H)}(sublead) [GeV/c]", 200, 0, 2000);

    book<TH1F>("m_tprime", "m_{T'} [GeV]", 200, 950, 1050);
    book<TH1F>("m_top", "m_{t} [GeV]", 200, 150, 250);
    book<TH1F>("m_higgs", "m_{H} [GeV]", 60, 110, 140);


      //  number plots
    book<TH1F>("Nt", "Number of tops", 5, 0, 5);
    book<TH1F>("NH", "Number of Higgses", 5, 0, 5);
    book<TH1F>("Nb", "Number of bs", 8, 0, 8);
    book<TH1F>("Nlept", "Number of leptons", 15, 0, 15);
    book<TH1F>("Nmu", "Number of muons", 15, 0, 15);
    book<TH1F>("Ne", "Number of electrons", 15, 0, 15);
    book<TH1F>("Nlept_from_top", "Number of leptons from top", 15, 0, 15);
    book<TH1F>("Nmu_from_top", "Number of muons from top", 15, 0, 15);
    book<TH1F>("Ne_from_top", "Number of electrons from top", 15, 0, 15);


    // decay modes
    book<TH1F>("tp_decay", "Tprime decay modes", 30, 0, 30);
    book<TH1F>("h_decay", "Higgs decay modes", 30, 0, 30);
    book<TH1F>("t_decay", "Top decay modes", 30, 0, 30);
    book<TH1F>("b_decay", "B decay modes", 30, 0, 30);
    book<TH1F>("w_decay", "W decay modes", 30, 0, 30);
    book<TH1F>("z_decay", "Z decay modes", 30, 0, 30);

  
    // dR variables
    book<TH1F>("DeltaR_bb", "#Delta R_{bb}", 50, 0, 5);
    book<TH1F>("max_deltaR_topprod", "max #Delta R(top products)", 50, 0, 5);

    book<TH2F>("top_pt_vs_max_dR", ";p_{T}(t);max #Delta R(t decay products)", 150, 0, 1500, 50, 0., 5.);
}


void GenHists::fill(const Event & event){
    // fill the histograms. Don't forget to always use the weight when filling:
    //     double weight = event.weight;
    
    std::vector<GenParticle> const * genparticles = event.genparticles;
    
    GenParticle const * tp1 = 0;
    GenParticle const * tp2 = 0;
    GenParticle const * t1 = 0;
    GenParticle const * t2 = 0;
    GenParticle const * h1 = 0;
    GenParticle const * h2 = 0;
        
    vector<GenParticle const *> bs;
    map<double, GenParticle const *> electrons;
    map<double, GenParticle const *> muons;
    map<double, GenParticle const *> electrons_from_top;
    map<double, GenParticle const *> muons_from_top;
    
    //     int number_mu = 0;
    //     int number_e = 0;
    //     int number_lept = 0;
    
    for (GenParticle const & igenp : *genparticles){
        if (abs(igenp.pdgId()) == 8){
            if (!tp1) tp1 = &igenp;
            else if (igenp.pt() > tp1->pt()) {tp2 = tp1; tp1 = &igenp;}
            else if (!tp2) tp2 = &igenp;
        }
        if (abs(igenp.pdgId()) == 6){
            if (!t1) t1 = &igenp;
            else if (igenp.pt() > t1->pt()) {t2 = t1; t1 = &igenp;}
            else if (!t2) t2 = &igenp;
        }
        if (abs(igenp.pdgId()) == 25){
            if (!h1) h1 = &igenp;
            else if (igenp.pt() > h1->pt()) {h2 = h1; h1 = &igenp;}
            else if (!h2) h2 = &igenp;
        }
        if (abs(igenp.pdgId()) == 5){
            bs.push_back(&igenp);
        }
        if (abs(igenp.pdgId()) == 11){ // electron
            electrons[igenp.pt()] = &igenp;
            GenParticle const * this_particle = &igenp;
            GenParticle const * mother = vlqToHiggsPair::findMother(igenp, genparticles);
            while (mother)
            {
                if (abs(mother->pdgId()) == 6)
                {
                    electrons_from_top[this_particle->pt()] = this_particle;
                    break;
                }
                this_particle = mother;
                mother = vlqToHiggsPair::findMother(*this_particle, genparticles);
            }
        }
        if (abs(igenp.pdgId()) == 13){ // muon
            muons[igenp.pt()] = &igenp;
            GenParticle const * this_particle = &igenp;
            GenParticle const * mother = vlqToHiggsPair::findMother(igenp, genparticles);
            while (mother)
            {
                if (abs(mother->pdgId()) == 6)
                {
                    muons_from_top[this_particle->pt()] = this_particle;
                    break;
                }
                this_particle = mother;
                mother = vlqToHiggsPair::findMother(*this_particle, genparticles);
            }
        }
        if (abs(igenp.pdgId()) == 23){
            GenParticle const * daughter1 = igenp.daughter(genparticles);
            GenParticle const * daughter2 = igenp.daughter(genparticles, 2);
            int decay1 = 0;
            int decay2 = 0;
            if (daughter1) decay1 = abs(daughter1->pdgId());
            if (daughter2) decay2 = abs(daughter2->pdgId());
            hist("z_decay")->Fill(decay1);
            hist("z_decay")->Fill(decay2);
        }
        if (abs(igenp.pdgId()) == 24){
            GenParticle const * daughter1 = igenp.daughter(genparticles);
            GenParticle const * daughter2 = igenp.daughter(genparticles, 2);
            int decay1 = 0;
            int decay2 = 0;
            if (daughter1) decay1 = abs(daughter1->pdgId());
            if (daughter2) decay2 = abs(daughter2->pdgId());
            hist("w_decay")->Fill(decay1);
            hist("w_decay")->Fill(decay2);
        }
    }
    
    hist("Nt")->Fill((bool)t1+(bool)t2);
    hist("NH")->Fill((bool)h1+(bool)h2);
    hist("Nb")->Fill(bs.size());
    hist("Nlept")->Fill(electrons.size()+muons.size());
    hist("Nmu")->Fill(muons.size());
    hist("Ne")->Fill(electrons.size());
    hist("Nlept_from_top")->Fill(electrons_from_top.size()+muons_from_top.size());
    hist("Nmu_from_top")->Fill(muons_from_top.size());
    hist("Ne_from_top")->Fill(electrons_from_top.size());
    
    if (tp1) {
        hist("tpPt_lead")->Fill(tp1->pt());
        hist("eta_lead")->Fill(tp1->eta());
        hist("phi_lead")->Fill(tp1->phi());
        hist("m_tprime")->Fill(tp1->v4().mass());
        GenParticle const * daughter1 = tp1->daughter(genparticles);
        GenParticle const * daughter2 = tp1->daughter(genparticles, 2);
        int decay1 = 0;
        int decay2 = 0;
        if (daughter1) decay1 = abs(daughter1->pdgId());
        if (daughter2) decay2 = abs(daughter2->pdgId());
        hist("tp_decay")->Fill(decay1);
        hist("tp_decay")->Fill(decay2);
    }
    
    if (tp2) {
        hist("tpPt_subl")->Fill(tp2->pt());
        hist("eta_subl")->Fill(tp2->eta());
        hist("phi_subl")->Fill(tp2->phi());
        hist("m_tprime")->Fill(tp2->v4().mass());
        GenParticle const * daughter1 = tp2->daughter(genparticles);
        GenParticle const * daughter2 = tp2->daughter(genparticles, 2);
        int decay1 = 0;
        int decay2 = 0;
        if (daughter1) decay1 = abs(daughter1->pdgId());
        if (daughter2) decay2 = abs(daughter2->pdgId());
        hist("tp_decay")->Fill(decay1);
        hist("tp_decay")->Fill(decay2);
    }
    
    if (t1) {
        hist("tPt_lead")->Fill(t1->pt());
        hist("m_top")->Fill(t1->v4().mass());
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
            hist("max_deltaR_topprod")->Fill(max_deltaR_topprod);
            hist("top_pt_vs_max_dR")->Fill(t1->pt(), max_deltaR_topprod);
        }

        hist("t_decay")->Fill(decay1);
        hist("t_decay")->Fill(decay2);
    }
    
    if (t2) {
        hist("tPt_subl")->Fill(t2->pt());
        hist("m_top")->Fill(t2->v4().mass());
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
            hist("max_deltaR_topprod")->Fill(max_deltaR_topprod);
            hist("top_pt_vs_max_dR")->Fill(t2->pt(), max_deltaR_topprod);
        }

        hist("t_decay")->Fill(decay1);
        hist("t_decay")->Fill(decay2);
    }
    
    if (h1){
        hist("hPt_lead")->Fill(h1->pt());
        hist("m_higgs")->Fill(h1->v4().mass());
        GenParticle const * daughter1 = h1->daughter(genparticles);
        GenParticle const * daughter2 = h1->daughter(genparticles, 2);
        int decay1 = 0;
        int decay2 = 0;
        if (daughter1) decay1 = daughter1->pdgId();
        if (daughter2) decay2 = daughter2->pdgId();
        hist("h_decay")->Fill(decay1);
        hist("h_decay")->Fill(decay2);
    }
    
    if (h2){
        hist("hPt_subl")->Fill(h2->pt());
        hist("m_higgs")->Fill(h2->v4().mass());
        GenParticle const * daughter1 = h2->daughter(genparticles);
        GenParticle const * daughter2 = h2->daughter(genparticles, 2);
        int decay1 = 0;
        int decay2 = 0;
        if (daughter1) decay1 = daughter1->pdgId();
        if (daughter2) decay2 = daughter2->pdgId();
        hist("h_decay")->Fill(decay1);
        hist("h_decay")->Fill(decay2);
    }
    
    double bTpPt_lead = 0.;
    double bTpPt_subl = 0.;
    double bHPt_lead = 0.;
    double bHPt_subl = 0.;
    
    for (vector<GenParticle const *>::const_iterator it = bs.begin(); it != bs.end(); ++it){
        GenParticle const * ib = *it;
        GenParticle const * daughter1 = ib->daughter(genparticles, 1);
        GenParticle const * daughter2 = ib->daughter(genparticles, 2);
        int decay1 = 0;
        int decay2 = 0;
        if (daughter1) decay1 = daughter1->pdgId();
        if (daughter2) decay2 = daughter2->pdgId();
        hist("b_decay")->Fill(decay1);
        hist("b_decay")->Fill(decay2);
        GenParticle const * imother = findMother(*ib, genparticles);
        if (!imother) continue;
        if (abs(imother->pdgId()) == 8){
            if (ib->pt() > bTpPt_lead) {bTpPt_subl = bTpPt_lead; bTpPt_lead = ib->pt();}
            else if (ib->pt() > bTpPt_subl) bTpPt_subl = ib->pt();
        }
        else if (abs(imother->pdgId()) == 25){
            if (ib->pt() > bHPt_lead) {bHPt_subl = bHPt_lead; bHPt_lead = ib->pt();}
            else if (ib->pt() > bHPt_subl) bHPt_subl = ib->pt();
            for (vector<GenParticle const *>::const_iterator iit = it+1; iit != bs.end(); ++iit){
                GenParticle const * ib2 = *iit;
                GenParticle const * imother2 = findMother(*ib2, genparticles);
                if (!imother2) continue;
                if (imother->index() == imother2->index()){
                    double dR = deltaR(*ib, *ib2);
                    hist("DeltaR_bb")->Fill(dR);
                    break;
                }
            }
        }
    }
    
    if (bTpPt_lead) hist("bTpPt_lead")->Fill(bTpPt_lead);
    if (bTpPt_subl) hist("bTpPt_subl")->Fill(bTpPt_subl);
    if (bHPt_lead) hist("bHPt_lead")->Fill(bHPt_lead);
    if (bHPt_subl) hist("bHPt_subl")->Fill(bHPt_subl);
    
//     if (b1 && b2){
//         double deltaR = b1->deltaR(*b2);
// //         cout << "Test2" << endl;
//         hist("DeltaR_bb")->Fill(deltaR);
// //         cout << "Test3" << endl;
//     }
    
//     cout << "Test4" << endl;
  
  
}

GenHists::~GenHists(){}
