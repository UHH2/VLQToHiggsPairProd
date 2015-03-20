#pragma once

#include "UHH2/core/include/Selection.h"
#include "UHH2/core/include/Event.h"

#include "UHH2/common/include/ObjectIdUtils.h"

using namespace uhh2;

namespace vlqToHiggsPair {

class JetPtSelection : public Selection {
public:
    explicit JetPtSelection(float minpt, float maxpt = -1., const boost::optional<JetId> & jetid = boost::none);
    virtual bool passes(const Event &);

private:
    float minpt_, maxpt_;
    boost::optional<JetId> jetid_;
};

class MuonPtSelection : public Selection {
public:
    explicit MuonPtSelection(float minpt, float maxpt = -1.);
    virtual bool passes(const Event &);

private:
    float minpt_, maxpt_;
};

class PrimaryLeptonPtSelection : public Selection {
public:
    explicit PrimaryLeptonPtSelection(Event::Handle<FlavorParticle> const & hndl, float minpt, float maxpt = -1.);
    virtual bool passes(const Event &);

private:
    Event::Handle<FlavorParticle> h_primlept_;
    float minpt_, maxpt_;
};

class HTSelection : public Selection {
public:
    explicit HTSelection(Event::Handle<double> const & hndl, float minht, float maxht = -1.);
    virtual bool passes(const Event &);

private:
    Event::Handle<double> h_ht_;
    float minht_, maxht_;
};

class STSelection : public Selection {
public:
    explicit STSelection(Event::Handle<double> const & hndl1, Event::Handle<FlavorParticle> const & hndl2, float minst, float maxst = -1.);
    virtual bool passes(const Event &);

private:
    Event::Handle<double> h_ht_;
    Event::Handle<FlavorParticle> h_primlept_;
    float minst_, maxst_;
};

class NGenParticleSelection : public Selection {
public:
    explicit NGenParticleSelection(Event::Handle<int> const & hndl, int n_min, int n_max = -1);
    virtual bool passes(const Event &);

private:
    Event::Handle<int> hndl_;
    int n_min_, n_max_;
};

class BoolSelection : public Selection {
public:
    explicit BoolSelection(Event::Handle<bool> const & hndl);
    virtual bool passes(const Event &);
private:
    Event::Handle<bool> hndl_;
};

}
