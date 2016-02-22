#pragma once

#include <algorithm>

#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/core/include/Event.h"

class TPrimeMassProducer: public AnalysisModule {
public:

    explicit TPrimeMassProducer(Context & ctx,
                                std::string const & h_htags,
                                std::string const & h_tops,
                                std::string const & h_primlep,
                                std::string const & h_out
                                ) :
        h_htags_(ctx.get_handle<std::vector<TopJet>>(h_htags)),
        h_tops_(ctx.get_handle<std::vector<TopJet>>(h_tops)),
        h_primlep_(ctx.get_handle<FlavorParticle>(h_primlep)),
        h_mHLep_(ctx.declare_event_output<float>(h_out+"_mass_HLep")),
        h_mHtop_(ctx.declare_event_output<float>(h_out+"_mass_Htop")),
        h_mMax_(ctx.declare_event_output<float>(h_out+"_mass_Max")),
        h_mMin_(ctx.declare_event_output<float>(h_out+"_mass_Min")) {}

    bool process(Event & event) override {
        if (!event.is_valid(h_htags_) || !event.is_valid(h_tops_) || !event.is_valid(h_primlep_)) {
            std::cout << "Error in TPrimeMassProducer: input handle not valid!\n";
            assert(false);
        }
        vector<TopJet> const & htags = event.get(h_htags_);
        vector<TopJet> const & htops = event.get(h_tops_);
        FlavorParticle const & primlep = event.get(h_primlep_);
        float hlep_mass = -1.;
        float htop_mass = -1.;
        float max_mass = -1.;
        float min_mass = -1.;
        if (htags.size()) {
        	TopJet const & ld_htag = htags[0];
        	LorentzVector htag_lep = ld_htag.v4() + primlep.v4();
        	hlep_mass = htag_lep.M();
        	if (htops.size()) {
        		TopJet const & ld_top = htops[0];
        		LorentzVector htag_lep = ld_htag.v4() + ld_top.v4();
        		htop_mass = htag_lep.M();
        	}
        	if (htop_mass > 0.) {
        		min_mass = std::min(hlep_mass, htop_mass);
        		max_mass = std::max(hlep_mass, htop_mass);
        	}
        	else {
        		min_mass = hlep_mass;
        		max_mass = hlep_mass;
        	}
        }
        event.set(h_mHLep_, hlep_mass);
        event.set(h_mHtop_, htop_mass);
        event.set(h_mMax_, max_mass);
        event.set(h_mMin_, min_mass);
        return true;

    }

private:
    uhh2::Event::Handle<std::vector<TopJet>> h_htags_;
    uhh2::Event::Handle<std::vector<TopJet>> h_tops_;
    uhh2::Event::Handle<FlavorParticle> h_primlep_;
    uhh2::Event::Handle<float> h_mHLep_;
    uhh2::Event::Handle<float> h_mHtop_;
    uhh2::Event::Handle<float> h_mMax_;
    uhh2::Event::Handle<float> h_mMin_;
};