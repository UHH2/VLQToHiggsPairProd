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

class JetPtSorter : public AnalysisModule {
public:
    explicit JetPtSorter() {}
    virtual bool process(uhh2::Event & event) override {
        std::vector<Jet> & ev_jets = *event.jets;
        std::map<double, Jet> sorted_jets;
        std::vector<Jet> result;
        for (const Jet & jet : ev_jets) {
            sorted_jets[jet.pt()] = jet;
        }
        for (std::map<double, Jet>::reverse_iterator it = sorted_jets.rbegin();
            it != sorted_jets.rend();
            ++it) {
            result.push_back(it->second);
        }
        std::swap(result, ev_jets);

        return true;
    }
private:

};


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
