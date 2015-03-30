#include "UHH2/VLQToHiggsPairProd/include/VLQToHiggsPairProdSelections.h"
#include "UHH2/core/include/AnalysisModule.h"

#include <stdexcept>

using namespace uhh2;
using namespace std;
using namespace vlqToHiggsPair;

JetPtSelection::JetPtSelection(float minpt, float maxpt, const boost::optional<JetId> & jetid) : minpt_(minpt), maxpt_(maxpt), jetid_(jetid) {} 

bool JetPtSelection::passes(const Event & event)
{
    const auto & jets = event.jets;

    assert(jets);
    bool pass = false;
    if (jets->size() > 0)
    {
        pass = (*jets)[0].pt() > minpt_ && (maxpt_ < 0 || (*jets)[0].pt() < maxpt_);
        if (pass && jetid_)
        {
            pass = (*jetid_)((*jets)[0], event);
        }
    }

    return pass;

}

MuonPtSelection::MuonPtSelection(float minpt, float maxpt, const boost::optional<MuonId> & muonid) :
    minpt_(minpt), maxpt_(maxpt), muonid_(muonid) {} 

bool MuonPtSelection::passes(const Event & event)
{
    const auto & muons = event.muons;

    assert(muons);
    bool pass = false;
    if (muons->size() > 0)
    {
        pass = (*muons)[0].pt() > minpt_ && (maxpt_ < 0 || (*muons)[0].pt() < maxpt_);
        if (pass && muonid_)
            pass = (*muonid_)((*muons)[0], event);
    }

    return pass;

}

PrimaryLeptonPtSelection::PrimaryLeptonPtSelection(Event::Handle<FlavorParticle> const & hndl, float minpt, float maxpt) : h_primlept_(hndl), minpt_(minpt), maxpt_(maxpt) {} 

bool PrimaryLeptonPtSelection::passes(const Event & event)
{
    if (event.is_valid(h_primlept_))
    {
        float primlep_pt = event.get(h_primlept_).pt();
        return primlep_pt > minpt_ && (maxpt_ < 0 || primlep_pt < maxpt_);
    }

    return false;

}

HTSelection::HTSelection(Event::Handle<double> const & hndl, float minht, float maxht) : h_ht_(hndl), minht_(minht), maxht_(maxht) {} 

bool HTSelection::passes(const Event & event)
{
    if (event.is_valid(h_ht_))
    {
        double ht = event.get(h_ht_);
        return ht > minht_ && (maxht_ < 0 || ht < maxht_);
    }

    return false;

}

STSelection::STSelection(Event::Handle<double> const & hndl1, Event::Handle<FlavorParticle> const & hndl2, float minst, float maxst) :
    h_ht_(hndl1), h_primlept_(hndl2), minst_(minst), maxst_(maxst) {} 

bool STSelection::passes(const Event & event)
{
    float met = event.met->pt();
    float ht = -1.f, primlep_pt = -1.f;
    if (event.is_valid(h_ht_))
    {
        ht = event.get(h_ht_);
    }
    if (event.is_valid(h_primlept_))
    {
        primlep_pt = event.get(h_primlept_).pt();
    }

    if (primlep_pt > 0.f && ht > 0.f)
    {
        float st = primlep_pt + met + ht;
        return st > minst_ && (maxst_ < 0 || st < maxst_    );
    }

    return false;

}

NGenParticleSelection::NGenParticleSelection(Event::Handle<int> const & hndl, int n_min, int n_max) : 
    hndl_(hndl), n_min_(n_min), n_max_(n_max) {}

bool NGenParticleSelection::passes(const Event & event)
{
    int n_particles = event.get(hndl_);
    return n_particles >= n_min_ && (n_max_ < 0 || n_particles <= n_max_);
}

GenParticleIdSelection::GenParticleIdSelection(const GenParticleId & id, int n_min, int n_max): 
    id_(id), n_min_(n_min), n_max_(n_max) {}

bool GenParticleIdSelection::passes(const Event & event)
{
    int n_passes = 0;
    for (const auto & genp : *event.genparticles )
    {
        if (id_(genp, event))
            n_passes++;
    }
    return n_passes >= n_min_ && (n_max_ < 0 || n_passes <= n_max_);
}

BoolSelection::BoolSelection(Event::Handle<bool> const & hndl) : hndl_(hndl) {}

bool BoolSelection::passes(const Event & event)
{
    bool pass = event.get(hndl_);
    return pass;
}

VetoSelection::VetoSelection(std::shared_ptr<Selection> sel) : sel_(sel) {}

bool VetoSelection::passes(const Event & event)
{
    bool pass = sel_->passes(event);
    return !pass;
}

bool OrSelection::passes(const Event & event)
{
    for(size_t i=0; i<selections.size(); ++i){
        if(selections[i]->passes(event)){
            return true;
        }
    }
    return false;
}

// TopTagSelection::TopTagSelection(Event::Handle<int> const & hndl, int minntags, int maxntags) :
//     h_ntopjets_(hndl), minntags_(minntags), maxntags_(maxntags) {} 

// bool TopTagSelection::passes(const Event & event)
// {
//     if (event.is_valid(h_ntopjets_))
//     {
//         int n_tags = event.get(h_ntopjets_);
//         return n_tags >= minntags_ && (maxntags_ < 0. || n_tags <= maxntags_) 
//     }

//     return false;

// }

// HiggsTagSelection::HiggsTagSelection(Event::Handle<double> const & hndl, float minht, float maxht) : h_ht_(hndl), minht_(minht), maxht_(maxht) {} 

// bool HiggsTagSelection::passes(const Event & event)
// {
//     if (event.is_valid(h_ht_))
//     {
//         double ht = event.get(h_ht_);
//         return ht > minht_ && (maxht_ < 0 || ht < maxht_);
//     }

//     return false;

// }
