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

HTSelection::HTSelection(Context & ctx, float minht, float maxht) : h_ht_(ctx.get_handle<float>("HT")), minht_(minht), maxht_(maxht) {} 

bool HTSelection::passes(const Event & event)
{
    if (event.get_state(h_ht_)==GenericEvent::state::valid)
    {
        float ht = event.get(h_ht_);
        return ht > minht_ && (maxht_ < 0 || ht < maxht_);
    }

    return false;

}
