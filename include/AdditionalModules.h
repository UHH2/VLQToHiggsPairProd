// Additional modules

#include <iostream>

#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Event.h"

#include "UHH2/common/include/JetIds.h"
#include "UHH2/common/include/TopJetIds.h"
#include "UHH2/common/include/Utils.h"
#include "UHH2/common/include/ObjectIdUtils.h"

using namespace std;
using namespace uhh2;



class JetPtSorter : public AnalysisModule {
public:
    explicit JetPtSorter() {}
    virtual bool process(uhh2::Event & event) override {
        std::vector<Jet> & ev_jets = *event.jets;
        sort_by_pt(ev_jets);

        return true;
    }
private:

};


class JetTagCalculator : public AnalysisModule {
public:
    explicit JetTagCalculator(Context & ctx, std::string hndl_name, JetId const & id = JetId(CSVBTag(CSVBTag::WP_MEDIUM))) :
        tagger_(id), hndl_(ctx.get_handle<int>(hndl_name)) {}

    virtual bool process(Event & event) {
        int n_btags = 0;
        for (const Jet & jet : *event.jets) {
            if (tagger_(jet, event))
                n_btags++;
        }
        event.set(hndl_, n_btags);
        return true;
    }

private:
    JetId tagger_;
    Event::Handle<int> hndl_;
};

class TopTagCalculator : public AnalysisModule {
public:
    explicit TopTagCalculator(Event::Handle<int> hndl, TopJetId const & id = TopJetId(CMSTopTag()), boost::optional<Event::Handle<std::vector<TopJet> > > const & topjets = boost::none) :
        tagger_(id), hndl_(hndl), h_topjets_(topjets) {}

    virtual bool process(Event & event) {
        int n_toptags = 0;
        std::vector<TopJet> const * topjets = (h_topjets_ && event.is_valid(*h_topjets_)) ? &event.get(*h_topjets_) : event.topjets;
        if (topjets)
        {
            for (const TopJet & jet : *topjets)
            {
                if (tagger_(jet, event))
                    n_toptags++;
            }
        }
        event.set(hndl_, n_toptags);
        return true;
    }

private:
    TopJetId tagger_;
    Event::Handle<int> hndl_;
    boost::optional<Event::Handle<std::vector<TopJet> > > h_topjets_;

};


