#include "UHH2/VLQToHiggsPairProd/include/GenHists.h"
#include "UHH2/core/include/Event.h"

#include "UHH2/common/include/GenTools.h"
#include "UHH2/common/include/Utils.h"

#include "UHH2/VLQToHiggsPairProd/include/AdditionalModules.h"

#include "TH1F.h"
#include "TH2F.h"

#include <iostream>
#include <typeinfo>

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

void GenHists::add_genhistcoll(int pdgid, int order_num, bool mass, bool charge, bool decay,
                            bool mother, const boost::optional<GenParticleId> & genp_id,
                            std::string suffix)
{
    GenHistColl new_genhistcoll;
    new_genhistcoll.pdgid = pdgid;
    new_genhistcoll.order_num = order_num;
    new_genhistcoll.genp_id = genp_id;

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

    std::string particle = mapPdgidToString(pdgid)+suffix;

    std::string order_str = "all";
    if (order_num > 0)
        order_str = to_string(order_num);

    new_genhistcoll.h_pt = book<TH1F>(particle+"_pt_"+order_str, particle+" p_{T} "+order_str, n_ptbins, minpt, maxpt);
    new_genhistcoll.h_eta = book<TH1F>(particle+"_eta_"+order_str, particle+" eta "+order_str, 40, -2.5, 2.5);
    new_genhistcoll.h_phi = book<TH1F>(particle+"_phi_"+order_str, particle+" phi "+order_str, 64, -M_PI, M_PI);
    new_genhistcoll.h_n = order_num <= 1 ? book<TH1F>(particle+"_n", particle+" number", 40, -2.5, 2.5) : NULL;
    new_genhistcoll.h_mass = mass ? book<TH1F>(particle+"_mass_"+order_str, particle+" mass "+order_str, n_massbins, minmass, maxmass) : NULL;
    new_genhistcoll.h_charge = charge ? book<TH1F>(particle+"_charge_"+order_str, particle+" charge "+order_str, 3, -1.5, 1.5) : NULL;
    new_genhistcoll.h_decay = decay ? book<TH1F>(particle+"_decay_"+order_str, particle+" decay "+order_str, 60, -30.5, 30.5) : NULL;
    new_genhistcoll.h_mother = mother ? book<TH1F>(particle+"_mother_"+order_str, particle+" mother "+order_str, 60, -30.5, 30.5) : NULL;

    all_hists_.push_back(new_genhistcoll);


}

template<class T>
void GenHists::fill_hists(const T * ipart, const std::vector<GenParticle> & genparticles,
    GenHistColl & gen_histcoll, double w)
{
    gen_histcoll.h_pt->Fill(ipart->pt(), w);
    gen_histcoll.h_eta->Fill(ipart->pt(), w);
    gen_histcoll.h_phi->Fill(ipart->pt(), w);
    if (gen_histcoll.h_mass) gen_histcoll.h_mass->Fill(ipart->v4().mass(), w);
    if (gen_histcoll.h_charge) gen_histcoll.h_charge->Fill(ipart->charge(), w);
    if (gen_histcoll.h_charge) gen_histcoll.h_charge->Fill(ipart->charge(), w);
    GenParticle const * genpart = typeid(T) == typeid(GenParticle) ? (GenParticle*)ipart : NULL;
    if (gen_histcoll.h_decay && genpart)
    {
        const GenParticle * daughter1 = genpart->daughter(&genparticles, 1);
        const GenParticle * daughter2 = genpart->daughter(&genparticles, 2);
        if (daughter1) gen_histcoll.h_decay->Fill(daughter1->pdgId(), w);
        if (daughter2) gen_histcoll.h_decay->Fill(daughter2->pdgId(), w);     
    }
    if (gen_histcoll.h_mother && genpart)
    {
        const GenParticle * mother = findMother(*genpart, &genparticles);
        if (mother) gen_histcoll.h_mother->Fill(mother->pdgId(), w);
    }
}

template<class T>
void GenHists::fill_wrapper(std::vector<const T*> plot_particles, const uhh2::Event & event,
                    GenHistColl & gen_histcoll)
{
    double w = event.weight;

    sort_by_pt(plot_particles);

    if (gen_histcoll.h_n)
        gen_histcoll.h_n->Fill(plot_particles.size(), w);

    if (gen_histcoll.order_num < 1)
    {
        for (auto ipart : plot_particles)
        {
            fill_hists(ipart, *event.genparticles, gen_histcoll, w);
        }
    }
    else
    {
        if (plot_particles.size() >= gen_histcoll.order_num)
            fill_hists(plot_particles[gen_histcoll.order_num-1], *event.genparticles, gen_histcoll, w);
    }
}

void GenHists::fill_genhistcoll(const uhh2::Event & event, GenHistColl & gen_histcoll)
{
    if (gen_histcoll.pdgid)
    {
        std::vector<const GenParticle*> plot_particles;

        // std::cout << "Fill particles with id " << gen_histcoll.pdgid << "\n";

        for (const auto & genp : *event.genparticles)
        {
            if (std::abs(genp.pdgId()) == gen_histcoll.pdgid)
            {
                // std::cout << " Found one instance, check for right mother\n";
                if (gen_histcoll.genp_id && !(*gen_histcoll.genp_id)(genp, event))
                    continue;

                // std::cout << " Has right mother!\n";
                plot_particles.push_back(&genp);
            }
        }

        fill_wrapper(plot_particles, event, gen_histcoll);
    }
    else
    {
        std::vector<const Particle*> plot_particles;

        for (const auto & genp : *event.genjets)
            plot_particles.push_back(&genp);

        fill_wrapper(plot_particles, event, gen_histcoll);
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

    // std::cout << "NEXT SELECTION, event " << event.event << "\nGenParticles:\n";

    // for (auto const & genp : *event.genparticles)
        // std::cout << " " << genp.pdgId() << "\n";

    for (auto & gen_histcoll : all_hists_ )
        fill_genhistcoll(event, gen_histcoll);

    double weight = event.weight;

    
    std::vector<GenParticle> const * genparticles = event.genparticles;
    
    GenParticle const * t1 = 0;
    GenParticle const * t2 = 0;
        
    vector<GenParticle> bs;
    
    if (event.is_valid(h_part_ht_))
        spec_parton_ht->Fill(event.get(h_part_ht_));
    
    for (GenParticle const & igenp : *genparticles)
    {
        if (abs(igenp.pdgId()) == 6)
        {
            if (!t1) t1 = &igenp;
            else if (igenp.pt() > t1->pt()) {t2 = t1; t1 = &igenp;}
            else if (!t2) t2 = &igenp;
        }
        if (abs(igenp.pdgId()) == 5)
        {
            bs.push_back(igenp);
        }
    }
    
    if (t1) 
    {
        GenParticle const * daughter1 = t1->daughter(genparticles, 1);
        GenParticle const * daughter2 = t1->daughter(genparticles, 2);
        GenParticle const * top_b = 0;
        GenParticle const * top_Wq1 = 0;
        GenParticle const * top_Wq2 = 0;
        if (daughter1)
        {
            findTopProducts(genparticles, daughter1, top_b, top_Wq1, top_Wq2);
        }
        if (daughter2)
        {
            findTopProducts(genparticles, daughter2, top_b, top_Wq1, top_Wq2);
        }

        double max_deltaR_topprod = calcMaxDR(top_b, top_Wq1, top_Wq2);

        if (max_deltaR_topprod)
        {
            spec_max_deltaR_topprod->Fill(max_deltaR_topprod, weight);
            spec_top_pt_vs_max_dR->Fill(t1->pt(), max_deltaR_topprod, weight);
        }

    }
    
    if (t2) 
    {
        GenParticle const * daughter1 = t2->daughter(genparticles, 1);
        GenParticle const * daughter2 = t2->daughter(genparticles, 2);
        GenParticle const * top_b = 0;
        GenParticle const * top_Wq1 = 0;
        GenParticle const * top_Wq2 = 0;
        if (daughter1)
        {
            findTopProducts(genparticles, daughter1, top_b, top_Wq1, top_Wq2);
        }
        if (daughter2)
        {
            findTopProducts(genparticles, daughter2, top_b, top_Wq1, top_Wq2);
        }

        double max_deltaR_topprod = calcMaxDR(top_b, top_Wq1, top_Wq2);

        if (max_deltaR_topprod)
        {
            spec_max_deltaR_topprod->Fill(max_deltaR_topprod, weight);
        }
    }
    
    for (vector<GenParticle>::const_iterator it = bs.begin(); it != bs.end(); ++it)
    {
        GenParticle const * ib = &*it;
        GenParticle const * closestB = closestParticle(*ib, bs);
        if (closestB)
            spec_deltaR_bb_min->Fill(deltaR(*ib, *closestB), weight);
        GenParticle const * imother = findMother(*ib, genparticles);
        if (!imother) continue;
        if (abs(imother->pdgId()) == 25)
        {
            for (vector<GenParticle>::const_iterator iit = it+1; iit != bs.end(); ++iit)
            {
                GenParticle const * ib2 = &*iit;
                GenParticle const * imother2 = findMother(*ib2, genparticles);
                if (!imother2) continue;
                if (imother->index() == imother2->index())
                {
                    double dR = deltaR(*ib, *ib2);
                    spec_deltaR_bb_h->Fill(dR, weight);
                    break;
                }
            }
        }
    }
      
  
}

GenHists::~GenHists(){}
