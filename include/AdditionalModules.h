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

class HiggsTag {
public:
    explicit HiggsTag(float minmass = 60.f, float maxmass = std::numeric_limits<float>::infinity(), JetId const & id = CSVBTag(CSVBTag::WP_MEDIUM)) :
        minmass_(minmass), maxmass_(maxmass), btagid_(id) {}

    bool operator()(TopJet const & topjet, uhh2::Event const & event) const
    {
        auto subjets = topjet.subjets();
        if(subjets.size() < 2) return false;
        clean_collection(subjets, event, btagid_);
        if (subjets.size() < 2) return false;
        sort_by_pt(subjets);

        LorentzVector firsttwosubjets = subjets[0].v4() + subjets[1].v4();
        if(!firsttwosubjets.isTimelike()) {
            return false;
        }
        auto mjet = firsttwosubjets.M();
        if(mjet < minmass_) return false;
        if(mjet > maxmass_) return false;
        return true;
    }

private:
    float minmass_, maxmass_;
    JetId btagid_;

};


