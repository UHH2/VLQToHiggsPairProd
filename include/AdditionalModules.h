// Additional modules

#include <iostream>

#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Event.h"

#include "UHH2/common/include/JetIds.h"
#include "UHH2/common/include/TopJetIds.h"

using namespace std;
using namespace uhh2;

namespace vlqToHiggsPair {
    static const size_t number_selections = 7;

    static const char* selection_names[] = {
        "OneElectronCut",
        "OneMuonCut",
        "ElectronCut",
        "MuonCut",
        "BTagCut",
        "JetPtCut",
        "HTCut"
    };
    inline void fill_hists(
        Event const & event,
        std::map<const char *, bool> const & pass_selection,
        std::map<const char *, std::unique_ptr<Hists> > & nm1_hists,
        std::unique_ptr<Hists> & allsel_hists
    )
    {
        bool pass_all_selections = true;

        // std::cout << "Fill Histograms:" << std::endl;

        for (std::map<const char *, bool>::const_iterator iSel = pass_selection.begin();
            iSel != pass_selection.end(); ++iSel)
        {
            const char * sel_name = iSel->first;
            bool pass_sel = iSel->second;

            // std::cout << "  " << sel_name << " " << pass_sel << std::endl;

            if (!pass_sel)
                pass_all_selections = false;

            bool pass_nm1 = true;

            // std::cout << std::endl << "  Fill nm1 histograms:" << std::endl;

            for (size_t iName = 0; iName < number_selections; ++iName)
            {
                try
                {
                    // std::cout << "    " << sel_name << " " << selection_names[iName] << " "
                    // << pass_selection.at(selection_names[iName]) << std::endl;
                    if (string(sel_name) != selection_names[iName]
                        && !pass_selection.at(selection_names[iName]))
                        pass_nm1 = false;
                }
                catch (const std::out_of_range & e)
                {
                    continue;
                }
            }

            // std::cout << "    Bool pass_nm1: " << pass_nm1 << std::endl << std::endl;

            if (pass_nm1)
                try
                {
                    nm1_hists.at(sel_name)->fill(event);
                }
                catch (const std::out_of_range & e)
                {
                    continue;
                }

        }

    // std::cout << "Bool pass_all_selections: " << pass_all_selections << std::endl << std::endl;

        if (pass_all_selections)
            allsel_hists->fill(event);
    }

}



// class NGenParticleCalculator : public AnalysisModule {
// public:
//     explicit NGenParticleCalculator(Context & ctx, std::string hndl_name, int genp_id, boost::optional<int> mother_id = boost::none) :
//         hndl_(ctx.get_handle<int>(hndl_name)), genp_id_(genp_id), mother_id_(mother_id) {}

//     virtual bool process(Event & event) {
//         int n_particles = 0;
//         for (GenParticle const & genp : *event.genparticles)
//         {
//             if (abs(genp.pdgId()) == genp_id_)
//             {
//                 if (mother_id_)
//                 {
//                     bool right_mother = false;
//                     GenParticle const * gen_mother = vlqToHiggsPair::findMother(genp, event.genparticles);
//                     while (gen_mother)
//                     {
//                         if (abs(gen_mother->pdgId()) == *mother_id_)
//                         {
//                             right_mother = true;
//                             break;
//                         }
//                         gen_mother = vlqToHiggsPair::findMother(*gen_mother, event.genparticles);
//                     }
//                     if (!right_mother)
//                         continue;
//                 }
//                 n_particles++;
//             }
//         }

//         event.set(hndl_, n_particles);
//         return true;
//     }

// private:
//     Event::Handle<int> hndl_;
//     int genp_id_;
//     boost::optional<int> mother_id_;
// };


class BTagCalculator : public AnalysisModule {
public:
    explicit BTagCalculator(Context & ctx, std::string hndl_name, CSVBTag const & id = CSVBTag(CSVBTag::WP_MEDIUM)) :
        tagger_(id), hndl_(ctx.get_handle<int>(hndl_name)) {}

    virtual bool process(Event & event) {
        int n_btags = 0;
        for (const Jet & jet : *event.jets)
        {
            if (tagger_(jet, event))
                n_btags++;
        }
        event.set(hndl_, n_btags);
        return true;
    }

private:
    CSVBTag tagger_;
    Event::Handle<int> hndl_;
};

class CMSTopTagCalculator : public AnalysisModule {
public:
    explicit CMSTopTagCalculator(Context & ctx, std::string hndl_name, CMSTopTag const & id = CMSTopTag()) :
        tagger_(id), hndl_(ctx.get_handle<int>(hndl_name)) {}

    virtual bool process(Event & event) {
        int n_toptags = 0;
        if (event.topjets)
        {
            for (const TopJet & jet : *event.topjets)
            {
                if (tagger_(jet, event))
                    n_toptags++;
            }
        }
        event.set(hndl_, n_toptags);
        return true;
    }

private:
    CMSTopTag tagger_;
    Event::Handle<int> hndl_;
};


// template<typename Id> class tagger_helper;

// template<>
// class tagger_helper<CMSTopTag>
// {
// public:
//     explicit tagger_helper(const CMSTopTag & tagger) : tagger_(tagger) {}
//     explicit tagger_helper(const CSVBTag & tagger) : tagger_(0., 0., 0.) {}

//     bool operator()(const TopJet & topjet, const uhh2::Event & event) const {return tagger_(topjet, event);}
//     bool operator()(const Jet & jet, const uhh2::Event & event) const {return false;}

// private:
//     CMSTopTag tagger_;

// };

// template<>
// class tagger_helper<CSVBTag>
// {
// public:
//     explicit tagger_helper(const CSVBTag & tagger) : tagger_(tagger) {}
//     explicit tagger_helper(const CMSTopTag & tagger) : tagger_(CSVBTag::WP_LOOSE) {}

//     bool operator()(const Jet & jet, const uhh2::Event & event) const {return tagger_(jet, event);}
//     bool operator()(const TopJet & topjet, const uhh2::Event & event) const {return false;}

// private:
//     CSVBTag tagger_;

// };


// template<typename T>
// class NJetIdCalculator : public AnalysisModule {
// public:
//     // typedef std::function<bool (const T&, const uhh2::Event &)> id_type;

//     // typedef typename T::input_type input_type;

//     NJetIdCalculator(Context & ctx, const T & tagger, std::string handle_name) :
//         tagger_(tagger), hndl(ctx.get_handle<int>(handle_name)) {}

//     virtual bool process(Event & event) {
//         int n_tags = 0;
//         if (event.jets)
//         {
//             for (const Jet & jet : *event.jets)
//             {
//                 if (tagger_(jet, event))
//                     n_tags++;
//             }
//         }
//         if (event.topjets)
//         {
//             for (const TopJet & jet : *event.topjets)
//             {
//                 if (tagger_(jet, event))
//                     n_tags++;
//             }
//         }
//         event.set(hndl, n_tags);
//         return true;
//     }

// private:
//     tagger_helper<T> tagger_;
//     Event::Handle<int> hndl;

// };