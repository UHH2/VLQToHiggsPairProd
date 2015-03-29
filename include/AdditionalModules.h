// Additional modules

#include <iostream>

#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Event.h"

#include "UHH2/common/include/JetIds.h"
#include "UHH2/common/include/TopJetIds.h"
#include "UHH2/common/include/Utils.h"
#include "UHH2/common/include/ObjectIdUtils.h"
#include "UHH2/common/include/GenTools.h"

using namespace std;
using namespace uhh2;



class JetPtSorter : public AnalysisModule
{
public:
    explicit JetPtSorter() {}
    virtual bool process(uhh2::Event & event) override {
        std::vector<Jet> & ev_jets = *event.jets;
        sort_by_pt(ev_jets);

        return true;
    }
private:

};


class JetTagCalculator : public AnalysisModule
{
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

class TopTagCalculator : public AnalysisModule
{
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

class GenParticleMotherId
{
public:
    GenParticleMotherId(int mother_id = 0, int veto_mother_id = 0) :
        mother_id_(mother_id), veto_mother_id_(veto_mother_id)
        {}

    bool operator()(const GenParticle & genp, const Event & event) const
    {
        if (mother_id_ > 0 || veto_mother_id_ > 0)
        {
            bool right_mother = mother_id_ > 0 ? false : true;
            GenParticle const * gen_mother = findMother(genp, event.genparticles);
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
                return false;
        }

        return true;
    }

private:
    int mother_id_, veto_mother_id_;
};


