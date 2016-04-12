#include "UHH2/VLQToHiggsPairProd/include/TpTpReconstruction.h"
#include "UHH2/core/include/LorentzVector.h"
#include "UHH2/common/include/ReconstructionHypothesisDiscriminators.h"
#include "UHH2/common/include/Utils.h"
#include "UHH2/core/include/Utils.h"
#include <cassert>

using namespace uhh2;
using namespace std;

TpTpReconstruction::TpTpReconstruction(Context & ctx,
                                    string const & ttbar_hyp,
                                    const string & h_out,
                                    const string & discriminator_name):
            ttbar_hyps_(ctx.get_handle<std::vector<ReconstructionHypothesis>>(ttbar_hyp)),
            h_recohyps_(ctx.get_handle<vector<TpTpReconstructionHypothesis>>(h_out)),
            discriminator_name_(discriminator_name) {}

TpTpReconstruction::~TpTpReconstruction() {}

bool TpTpReconstruction::check_overlap(Jet const & ref_jet, vector<Jet> const & jet_coll) {
    for (auto const & jet : jet_coll) {
        if (deltaR(ref_jet, jet) < 0.1)
            return false;

    }
    return true;
}


bool TpTpReconstruction::process(uhh2::Event & event) {
    assert(event.jets);
    //find primary charged lepton
    vector<TpTpReconstructionHypothesis> recoHyps;

    std::vector<ReconstructionHypothesis> const & ttbar_hyps = event.get(ttbar_hyps_);
    
    ReconstructionHypothesis const * ttbar_hyp_ = get_best_hypothesis(ttbar_hyps, discriminator_name_);

    vector<Jet> sep_jets;
    for (auto const & jet : *event.jets) {
        if (check_overlap(jet, ttbar_hyp_->tophad_jets()) && check_overlap(jet, ttbar_hyp_->tophad_jets()))
            sep_jets.push_back(jet);
    }
    unsigned int n_jets = sep_jets.size();
    if(n_jets>10) n_jets=10; //avoid crashes in events with many jets
    // idea: loop over 3^Njet possibilities and write the current loop
    // index j in the 3-base system. The Njets digits represent whether
    // to assign each jet to the hadronic side (0), leptonic side (1),
    // or none of them (2).
    const unsigned int max_j = pow(3, n_jets);

    LorentzVector tophad_v4 = ttbar_hyp_->tophad_v4();
    LorentzVector toplep_v4 = ttbar_hyp_->toplep_v4();

    for (unsigned int j=0; j < max_j; j++) {
        LorentzVector tp_lep = toplep_v4;
        LorentzVector tp_had = tophad_v4;
        int hadjets=0;
        int lepjets=0;
        int num = j;
        TpTpReconstructionHypothesis hyp;
        for (unsigned int k=0; k<n_jets; k++) {
            Jet const & ref_jet = sep_jets.at(k);
            if(num%3==0) {
                tp_had = tp_had + ref_jet.v4();
                hyp.add_tphad_jet(ref_jet);
                hadjets++;
            }

            if(num%3==1) {
                tp_lep = tp_lep + ref_jet.v4();
                hyp.add_tplep_jet(ref_jet);
                lepjets++;
            }
                //in case num%3==2 do not take this jet at all
                //shift the trigits of num to the right:
            num /= 3;
        }

	    //search jet with highest pt assigned to leptonic top

            //fill only hypotheses with at least one jet assigned to each top quark
        if(hadjets>0 && lepjets>0) {
            hyp.set_tphad_v4(tp_had);
            hyp.set_tplep_v4(tp_lep);
            recoHyps.emplace_back(move(hyp));
        }
    } // 3^n_jets jet combinations
    event.set(h_recohyps_, move(recoHyps));
    return true;
}


