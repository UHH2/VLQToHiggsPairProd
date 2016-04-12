#pragma once

#include "UHH2/core/include/AnalysisModule.h"
#include "UHH2/common/include/ReconstructionHypothesis.h"
// #include "TMinuit.h"
#include "UHH2/core/include/Event.h"
// #include "UHH2/common/include/ObjectIdUtils.h"
// #include "UHH2/common/include/TopJetIds.h"
// #include "UHH2/common/include/PrimaryLepton.h"


class TpTpReconstructionHypothesis {
public:
  explicit TpTpReconstructionHypothesis(){}

  LorentzVector toplep_v4() const{return m_toplep_v4;}
  LorentzVector tophad_v4() const{return m_tophad_v4;} 
  LorentzVector tplep_v4() const{return m_tplep_v4;} 
  LorentzVector tphad_v4() const{return m_tphad_v4;}
  const std::vector<Jet>& tplep_jets() const{return m_tplep_jets;}
  const std::vector<Jet>& tphad_jets() const{return m_tphad_jets;}

  /// get the discriminator value for this hypothesis; thows a runtime_error if it does not exist.
  float discriminator(const std::string & l) const {
      auto it = m_discriminators.find(l);
      if(it == m_discriminators.end()){
          throw std::runtime_error("ReconstructionHypothesis::discriminator: discriminator with label '" + l + "' not set");
      }
      return it->second;
  }
  
  /// test if a discriminator value with a certian label has already been added
  bool has_discriminator(const std::string & label) const {
      return m_discriminators.find(label) != m_discriminators.end();
  }
  
  void set_tplep_v4(LorentzVector v4){m_tplep_v4=v4;}
  void set_tphad_v4(LorentzVector v4){m_tphad_v4=v4;} 
  void add_tplep_jet(const Jet& j){m_tplep_jets.push_back(j);}
  void add_tphad_jet(const Jet& j){m_tphad_jets.push_back(j);}
  void set_discriminator(const std::string & label, float discr){
      m_discriminators[label] = discr;
  }
  


private:
  LorentzVector m_toplep_v4;
  LorentzVector m_tophad_v4;
  LorentzVector m_tplep_v4;
  LorentzVector m_tphad_v4;

  std::vector<Jet> m_tplep_jets;
  std::vector<Jet> m_tphad_jets;
  

  std::map<std::string, float> m_discriminators;
};



class TpTpReconstruction: public uhh2::AnalysisModule {
public:

    explicit TpTpReconstruction(uhh2::Context & ctx,
          std::string const & ttbar_hyp,
          const std::string & h_out="TpTpReconstruction",
          const std::string & discriminator_name = "Chi2");

    virtual bool process(uhh2::Event & event) override;

    bool check_overlap(Jet const &, std::vector<Jet> const &);

    virtual ~TpTpReconstruction();

private:
    uhh2::Event::Handle<std::vector<ReconstructionHypothesis>> ttbar_hyps_;
    uhh2::Event::Handle<std::vector<TpTpReconstructionHypothesis>> h_recohyps_;
    std::string discriminator_name_;
};

