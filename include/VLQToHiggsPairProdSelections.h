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

class HTSelection : public Selection {
public:
    explicit HTSelection(Context & ctx, float minht, float maxht = -1.);
    virtual bool passes(const Event &);

private:
    Event::Handle<float> h_ht_;
    float minht_, maxht_;
};

}
