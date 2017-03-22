#pragma once

#include "UHH2/core/include/Hists.h"
#include "UHH2/core/include/Event.h"
#include "UHH2/core/include/GenParticle.h"
#include "UHH2/common/include/JetIds.h"
#include "UHH2/core/include/LorentzVector.h"
#include "UHH2/common/include/Utils.h"
// #include "UHH2/VLQToHiggsPairProd/include/TpTpAnalysisModule.h"
// #include "UHH2/common/include/PrintingModules.h"

using namespace uhh2;
using namespace std;

template<typename T>
class NParticleMultiHistProducer : public Hists {
public:

    explicit NParticleMultiHistProducer(Context & ctx,
                        const string & dirname,
                        const string & h_in,
                        const vector<string> & variables = {"n", "pt", "eta", "phi"},
                        unsigned part_ind = 1,
                        const string & h_primlep = "PrimaryLepton") :
        Hists(ctx, dirname),
        h_name_(h_in),
        h_in_(ctx.get_handle<vector<T>>(h_in)),
        part_ind_(part_ind),
        h_primlep_(ctx.get_handle<FlavorParticle>(h_primlep))
        {
            // === TEST: test if it's possible to make hist names without handle names
            for (string const & var : variables) {
                if (var == "n") hists_[var] = book<TH1F>("n", "n", 10, -.5, 9.5);
                if (var == "n_subjets") hists_[var] = book<TH1F>("n_subjets", "n_subjets", 10, -.5, 9.5);
                if (var == "pt") hists_[var] = book<TH1F>("pt", "pt", 60, 0., 1500.);
                if (var == "eta") hists_[var] = book<TH1F>("eta", "eta", 50, -3., 3.);
                if (var == "phi") hists_[var] = book<TH1F>("phi", "phi", 50, -3.14, 3.14);
                if (var == "mass") hists_[var] = book<TH1F>("mass", "mass", 60, 0., 300.);
                if (var == "mass_sj") hists_[var] = book<TH1F>("mass_sj", "mass sj", 60, 0., 300.);
                if (var == "tau21") hists_[var] = book<TH1F>("tau21", "tau21", 50, 0., 1.);
                if (var == "tau32") hists_[var] = book<TH1F>("tau32", "tau32", 50, 0., 1.);
                if (var == "csv_first_sj") hists_[var] = book<TH1F>("csv_first_sj", "csv_first_sj", 50, 0., 1.);
                if (var == "csv_second_sj") hists_[var] = book<TH1F>("csv_second_sj", "csv_second_sj", 50, 0., 1.);
                if (var == "csv_max_sj") hists_[var] = book<TH1F>("csv_max_sj", "csv_max_sj", 50, 0., 1.);
                if (var == "dRlepton") hists_[var] = book<TH1F>("dRlepton", "dR(ak8 jet, lepton)", 50, 0., 5.);
                if (var == "dRak4") hists_[var] = book<TH1F>("dRak4", "dR(Ak8 jet, closest Ak4 jet)", 50, 0., 5.);
                if (var == "dRak8") hists_[var] = book<TH1F>("dRak8", "dR(Ak8 jet, closest Ak8 jet)", 50, 0., 5.);
                if (split(var, "-")[0] == "n_sjbtags") hists_[var] = book<TH1F>("n_sjbtags_"+split(var, "-")[1], "N sjbtags "+split(var, "-")[1], 5, -.5, 4.5);
            }  
        }

    virtual void fill(Event const & event) override {
        bool is_topjet = std::is_same<T, TopJet>::value;
        double w = event.weight;
        // double w = 1.;
        if (!event.is_valid(h_in_)) {
            cout << "WARNING: handle " << h_name_ <<" in NParticleMultiHistProducer not valid!\n";
            return;
        }
        vector<T> const & coll = event.get(h_in_);
        for (map<string, TH1F*>::const_iterator it = hists_.begin(); it != hists_.end(); ++it) {
            if (it->first == "n") it->second->Fill(coll.size(), w);
            if (coll.size() >= part_ind_) {
                T const & particle = coll[part_ind_-1];
                if (it->first == "pt") it->second->Fill(particle.pt(), w);
                if (it->first == "eta") it->second->Fill(particle.eta(), w);
                if (it->first == "phi") it->second->Fill(particle.phi(), w);
                if (it->first == "mass") it->second->Fill(particle.v4().M(), w);
                if (it->first == "n_subjets") {
                        // assert(false);
                    assert(is_topjet);
                    it->second->Fill(particle.subjets().size(), w);
                };
                if (it->first == "mass_sj") {
                        // assert(false);
                    assert(is_topjet);
                    it->second->Fill(particle.softdropmass(), w);
                    // if (particle.subjets().size()){
                    //     LorentzVector sum_subjets;
                    //     for (Jet const & subjet : particle.subjets())
                    //         sum_subjets += subjet.v4();
                    //     it->second->Fill(sum_subjets.M(), w);
                    // } else {
                    //     it->second->Fill(-1., w);
                    // }
                };
                if (it->first == "tau21") {
                    assert(is_topjet);
                    it->second->Fill(particle.tau2()/particle.tau1(), w);
                }
                if (it->first == "tau32") {
                    assert(is_topjet);
                    it->second->Fill(particle.tau3()/particle.tau2(), w);
                }
                if (it->first == "csv_first_sj") {
                    assert(is_topjet);
                    if (particle.subjets().size() >= 1){
                        it->second->Fill(particle.subjets()[0].btag_combinedSecondaryVertex(), w);
                    } else {
                        it->second->Fill(-1., w);
                    }
                }
                if (it->first == "csv_second_sj") {
                    assert(is_topjet);
                    if (particle.subjets().size() >= 2){
                        it->second->Fill(particle.subjets()[1].btag_combinedSecondaryVertex(), w);
                    } else {
                        it->second->Fill(-1., w);
                    }
                }
                if (it->first == "csv_max_sj") {
                    assert(is_topjet);
                    double csv_max = -1.;
                    for (Jet const & subjet : particle.subjets()){
                        if (subjet.btag_combinedSecondaryVertex() > csv_max)
                            csv_max = subjet.btag_combinedSecondaryVertex();
                    }
                    it->second->Fill(csv_max, w);
                }
                if (it->first == "dRlepton") {
                    if (event.is_valid(h_primlep_)) {
                        float dRlep = deltaR(particle, event.get(h_primlep_));
                        it->second->Fill(dRlep, w);
                    }
                    else {it->second->Fill(-1., w);}
                }
                if (it->first == "dRak4") {
                    auto const * closest_ak4 = closestParticle(particle, *event.jets);
                    if (closest_ak4) {
                        float dRak4 = deltaR(particle, *closest_ak4);
                        it->second->Fill(dRak4, w);
                    }
                    else {it->second->Fill(-1., w);}
                }
                if (it->first == "dRak8") {
                    auto const * closest_ak8 = closestParticle(particle, *event.topjets);
                    if (closest_ak8) {
                        float dRak8 = deltaR(particle, *closest_ak8);
                        it->second->Fill(dRak8, w);
                    }
                    else {it->second->Fill(-1., w);}
                }
                if (split(it->first, "-")[0] == "n_sjbtags") {
                    CSVBTag::wp wp_;
                    if (split(it->first, "-")[1] == "loose")
                        wp_ = CSVBTag::WP_LOOSE;
                    else if (split(it->first, "-")[1] == "tight")
                        wp_ = CSVBTag::WP_TIGHT;
                    else
                        wp_ = CSVBTag::WP_MEDIUM;
                    CSVBTag btag_(wp_);
                    int n_sj = 0;
                    for (auto const & sj : particle.subjets()) {
                        if (btag_(sj, event))
                            n_sj++;
                    }
                    it->second->Fill(n_sj, w);
                }
            }
        }

        for (auto sub_hist : sub_hists_)
            sub_hist->fill(event);
    }


    void set_subhists(Hists * sub_hist) {
        sub_hists_.emplace_back(sub_hist);
    }


private:
    string h_name_;
    Event::Handle<vector<T>> h_in_;
    unsigned part_ind_;
    Event::Handle<FlavorParticle> h_primlep_;
    map<string, TH1F*> hists_;
    vector<shared_ptr<Hists>> sub_hists_;
};


template<typename T>
class NParticleMultiHistProducerHelper {
public:
    explicit NParticleMultiHistProducerHelper(
                        const string & rel_dirname,
                        const string & h_name,
                        const vector<string> & variables = {"n", "pt", "eta", "phi", "mass_sj", "csv_first_sj", "csv_second_sj", "n_subjets"},
                        unsigned part_ind = 1) :
        rel_dirname_(rel_dirname),
        h_name_(h_name),
        variables_(variables),
        part_ind_(part_ind) {}

    // ~NParticleMultiHistProducerHelper() {
    //     cout << "destroying dir " << rel_dirname_ << " for handle " << h_name_ << endl;
    // }

    void add_level(const string & rel_dirname,
                   const string & h_name,
                   const vector<string> & variables = {"n", "pt", "eta", "phi", "mass_sj", "csv_first_sj", "csv_second_sj", "n_subjets"},
                   unsigned part_ind = 1) {
        sub_levels_.emplace_back(rel_dirname, h_name, variables, part_ind);
        indizes_[rel_dirname] = sub_levels_.size()-1;
        // return &sub_levels_.end()-1;
    }

    NParticleMultiHistProducer<T>* book_histograms(Context & ctx, const string & dirname) const {
        NParticleMultiHistProducer<T> * new_hist = new NParticleMultiHistProducer<T>(ctx, dirname+"/"+rel_dirname_,
            h_name_, variables_, part_ind_);
        for (auto const & sub_level : sub_levels_)
            new_hist->set_subhists(sub_level.book_histograms(ctx, dirname+"/"+rel_dirname_));
        return new_hist;
    }

    NParticleMultiHistProducerHelper<T> & operator[](const string & rel_dirname) {
        unsigned ind = indizes_[rel_dirname];
        return sub_levels_[ind];
    }

    NParticleMultiHistProducerHelper<T> & at(const string & rel_dirname) {
        unsigned ind = indizes_[rel_dirname];
        return sub_levels_[ind];
    }

    NParticleMultiHistProducerHelper<T> & back() {
        unsigned ind = sub_levels_.size()-1;
        return sub_levels_[ind];
    }

    // vector<NParticleMultiHistProducerHelper<T>> const & get_sublevels() const {
    //     return sub_levels_;
    // }

    void print_name() {
        cout << "rel_dirname_: " << rel_dirname_ << " h_name_: " << h_name_ << " address: " << this << endl;
    }

    // virtual bool process(Event & event) override {
    //     if (event.is_valid(h_part_coll_)) {
    //         bool is_topjet = std::is_same<T, TopJet>::value;
    //         vector<T> const & coll = event.get(h_part_coll_);
    //         for (map<string, Event::Handle<int>>::const_iterator it = h_int_.begin(); it != h_int_.end(); ++it) {
    //             if (it->first == "n") event.set(it->second, coll.size() );
    //             if (coll.size() >= part_ind_) {
    //                 T const & particle = coll[part_ind_-1];
    //                 if (it->first == "n_subjets") {
    //                         // assert(false);
    //                     assert(is_topjet);
    //                     event.set(it->second, particle.subjets().size() );
    //                 }
    //             }
    //         }
    //         for (map<string, Event::Handle<float>>::const_iterator it = h_float_.begin(); it != h_float_.end(); ++it) {
    //             if (coll.size() >= part_ind_) {
    //                 T const & particle = coll[part_ind_-1];
    //                 if (it->first == "pt") event.set(it->second, particle.pt() );
    //                 if (it->first == "eta") event.set(it->second, particle.eta() );
    //                 if (it->first == "phi") event.set(it->second, particle.phi() );
    //                 if (it->first == "mass") event.set(it->second, particle.v4().M() );
    //                 if (it->first == "mass_sj") {
    //                     assert(is_topjet);
    //                     if (particle.subjets().size()){
    //                         LorentzVector sum_subjets;
    //                         for (Jet const & subjet : particle.subjets())
    //                             sum_subjets += subjet.v4();
    //                         event.set(it->second, sum_subjets.M() );
    //                     } else {
    //                         event.set(it->second, -1. );
    //                     }
    //                 }
    //                 if (it->first == "tau21") {
    //                     assert(is_topjet);
    //                     event.set(it->second, particle.tau2()/particle.tau1() );
    //                 }
    //                 if (it->first == "tau32") {
    //                     assert(is_topjet);
    //                     event.set(it->second, particle.tau3()/particle.tau2() );
    //                 }
    //                 if (it->first == "csv_first_sj") {
    //                     assert(is_topjet);
    //                     if (particle.subjets().size() >= 1){
    //                         event.set(it->second, particle.subjets()[0].btag_combinedSecondaryVertex() );
    //                     } else {
    //                         event.set(it->second, -1. );
    //                     }
    //                 }
    //                 if (it->first == "csv_second_sj") {
    //                     assert(is_topjet);
    //                     if (particle.subjets().size() >= 2){
    //                         event.set(it->second, particle.subjets()[1].btag_combinedSecondaryVertex() );
    //                     } else {
    //                         event.set(it->second, -1. );
    //                     }
    //                 }
    //                 if (it->first == "csv_max_sj") {
    //                     assert(is_topjet);
    //                     double csv_max = -1.;
    //                     for (Jet const & subjet : particle.subjets()){
    //                         if (subjet.btag_combinedSecondaryVertex() > csv_max)
    //                             csv_max = subjet.btag_combinedSecondaryVertex();
    //                     }
    //                     event.set(it->second, csv_max );
    //                 }
    //                 // if (it->first == "dRlepton") {
    //                 //     if (event.is_valid(h_primlep_)) {
    //                 //         float dRlep = deltaR(particle, event.get(h_primlep_));
    //                 //         event.set(it->second, dRlep );
    //                 //     }
    //                 //     else {event.set(it->second, -1. );}
    //                 // }
    //                 if (it->first == "dRak4") {
    //                     auto const * closest_ak4 = closestParticle(particle, *event.jets);
    //                     if (closest_ak4) {
    //                         float dRak4 = deltaR(particle, *closest_ak4);
    //                         event.set(it->second, dRak4 );
    //                     }
    //                     else {event.set(it->second, -1. );}
    //                 }
    //                 if (it->first == "dRak8") {
    //                     auto const * closest_ak8 = closestParticle(particle, *event.topjets);
    //                     if (closest_ak8) {
    //                         float dRak8 = deltaR(particle, *closest_ak8);
    //                         event.set(it->second, dRak8 );
    //                     }
    //                     else {event.set(it->second, -1. );}
    //                 }
    //                 if (split(it->first, "-")[0] == "n_sjbtags") {
    //                     CSVBTag::wp wp_;
    //                     if (split(it->first, "-")[1] == "loose")
    //                         wp_ = CSVBTag::WP_LOOSE;
    //                     else if (split(it->first, "-")[1] == "tight")
    //                         wp_ = CSVBTag::WP_TIGHT;
    //                     else
    //                         wp_ = CSVBTag::WP_MEDIUM;
    //                     CSVBTag btag_(wp_);
    //                     int n_sj = 0;
    //                     for (auto const & sj : particle.subjets()) {
    //                         if (btag_(sj, event))
    //                             n_sj++;
    //                     }
    //                     event.set(it->second, n_sj );
    //                 }
    //             }
    //         }
    //     }
    //     for (auto & sub_level : sub_levels_)
    //         sub_level.process(event);

    //     return true;
    // }

private:
    string rel_dirname_;
    string h_name_;
    vector<string> variables_;
    std::map<string, unsigned> indizes_;
    vector<NParticleMultiHistProducerHelper<T>> sub_levels_;
    unsigned part_ind_;
    // Event::Handle<vector<T>> h_part_coll_;
    // map<string, Event::Handle<int>> h_int_;
    // map<string, Event::Handle<float>> h_float_;
    // vector<Event::Handle<double>> h_double_;
};

class OwnHistCollector : public uhh2::Hists {
public:
    OwnHistCollector(Context & ctx, const string & dirname, bool gen_plots = false, JetId const & btag_id = CSVBTag(CSVBTag::WP_LOOSE),
        set<string> const & hists = {"ev", "mu", "jet", "lumi", "cmstopjet", "heptopjet", "ak8softdroptopjet"}) :
    Hists(ctx, dirname),
    el_hists(hists.find("el") != hists.end() ? new ExtendedElectronHists(ctx, dirname+"/ElectronHists", gen_plots) : NULL),
    mu_hists(hists.find("mu") != hists.end() ? new ExtendedMuonHists(ctx, dirname+"/MuonHists", gen_plots) : NULL),
    tau_hists(hists.find("tau") != hists.end() ? new TauHists(ctx, dirname+"/TauHists") : NULL),
    ev_hists(hists.find("ev") != hists.end() ? new ExtendedEventHists(ctx, dirname+"/EventHists", "n_btags_loose", "n_btags_medium", "n_btags_tight") : NULL),
    jet_hists(hists.find("jet") != hists.end() ? new ExtendedJetHists(ctx, dirname+"/JetHists", 4) : NULL),
    jet_clean_hists(hists.find("jet_clean") != hists.end() ? new ExtendedJetHists(ctx, dirname+"/JetHistsCleaned", 4, "jets_pt_cleaned") : NULL),
    cmstopjet_hists(hists.find("cmstopjet") != hists.end() ? new ExtendedTopJetHists(ctx, dirname+"/SlimmedAk8Jets", btag_id, 3) : NULL),
    cmstopjet_cleaned_hists(hists.find("cmstopjet_cleaned") != hists.end() ? new ExtendedTopJetHists(ctx, dirname+"/SlimmedAk8JetsUnCleaned", btag_id, 3, "topjets_uncleaned") : NULL),
    heptopjet_hists(hists.find("heptopjet") != hists.end() ? new ExtendedTopJetHists(ctx, dirname+"/HEPTopJetHists", btag_id, 3, "patJetsHepTopTagCHSPacked_daughters") : NULL),
    ak8softdroptopjet_hists(hists.find("ak8softdroptopjet") != hists.end() ? new ExtendedTopJetHists(ctx, dirname+"/PatJetsSoftDropHists", btag_id, 3, "patJetsAk8CHSJetsSoftDropPacked_daughters") : NULL),
    lumi_hist((ctx.get("dataset_type", "") != "MC") && hists.find("lumi") != hists.end()? new LuminosityHists(ctx, dirname+"/LuminosityHists") : NULL),
    gen_hists(gen_plots && hists.find("gen") != hists.end() ? new CustomizableGenHists(ctx, dirname+"/GenHists", "parton_ht") : NULL)
    {
        // if (gen_hists)
        // {
        //     gen_hists->add_genhistcoll(8000001, 1, true, true, true, true);
        //     gen_hists->add_genhistcoll(8000001, 2, true, true, true, true);
        //     gen_hists->add_genhistcoll(6, 1, true, true, true, true);
        //     gen_hists->add_genhistcoll(6, 2, true, true, true, true);
        //     gen_hists->add_genhistcoll(25, 1, true, true, true, true);
        //     gen_hists->add_genhistcoll(25, 2, true, true, true, true);
        //     gen_hists->add_genhistcoll(0, 0);
        //     // gen_hists->add_genhistcoll(0, 1);
        //     // gen_hists->add_genhistcoll(0, 2);
        //     gen_hists->add_genhistcoll(11, 1, false, true, false, false, GenParticleId(GenParticleMotherId(6)), "_from_top");
        //     gen_hists->add_genhistcoll(11, 2, false, true, false, false, GenParticleId(GenParticleMotherId(6)), "_from_top");
        //     gen_hists->add_genhistcoll(13, 1, false, true, false, false, GenParticleId(GenParticleMotherId(6)), "_from_top");
        //     gen_hists->add_genhistcoll(13, 2, false, true, false, false, GenParticleId(GenParticleMotherId(6)), "_from_top");
        //     gen_hists->add_genhistcoll(11, 1, false, true, false, false, GenParticleId(AndId<GenParticle>(GenParticleMotherId(24,6),GenParticleMotherId(24,25))), "_from_tpW");
        //     gen_hists->add_genhistcoll(11, 2, false, true, false, false, GenParticleId(AndId<GenParticle>(GenParticleMotherId(24,6),GenParticleMotherId(24,25))), "_from_tpW");
        //     gen_hists->add_genhistcoll(13, 1, false, true, false, false, GenParticleId(AndId<GenParticle>(GenParticleMotherId(24,6),GenParticleMotherId(24,25))), "_from_tpW");
        //     gen_hists->add_genhistcoll(13, 2, false, true, false, false, GenParticleId(AndId<GenParticle>(GenParticleMotherId(24,6),GenParticleMotherId(24,25))), "_from_tpW");

        // }
    } 

    virtual void fill(const Event & event) {
        if (lumi_hist) lumi_hist->fill(event);
        if (el_hists) el_hists->fill(event);
        if (mu_hists) mu_hists->fill(event);
        if (tau_hists) tau_hists->fill(event);
        if (ev_hists) ev_hists->fill(event);
        if (jet_hists) jet_hists->fill(event);
        if (jet_clean_hists) jet_clean_hists->fill(event);
        if (cmstopjet_hists) cmstopjet_hists->fill(event);
        if (cmstopjet_cleaned_hists) cmstopjet_cleaned_hists->fill(event);
        if (heptopjet_hists) heptopjet_hists->fill(event);
        if (ak8softdroptopjet_hists) ak8softdroptopjet_hists->fill(event);
        // ca15filteredtopjet_hists->fill(event);
        if (gen_hists) gen_hists->fill(event);
    }

    ~OwnHistCollector(){
        delete lumi_hist;
        delete el_hists;
        delete mu_hists;
        delete tau_hists;
        delete ev_hists;
        delete jet_hists;
        delete jet_clean_hists;
        delete cmstopjet_hists;
        delete cmstopjet_cleaned_hists;
        delete heptopjet_hists;
        delete ak8softdroptopjet_hists;
        // delete ca15filteredtopjet_hists;
        delete gen_hists;
    }

private:
    ExtendedElectronHists * el_hists;
    ExtendedMuonHists * mu_hists;
    TauHists * tau_hists;
    ExtendedEventHists * ev_hists;
    ExtendedJetHists * jet_hists, *jet_clean_hists;
    ExtendedTopJetHists * cmstopjet_hists, *cmstopjet_cleaned_hists;
    ExtendedTopJetHists * heptopjet_hists;
    ExtendedTopJetHists * ak8softdroptopjet_hists;
    LuminosityHists * lumi_hist;
    // ExtendedTopJetHists * ca15filteredtopjet_hists;
    CustomizableGenHists * gen_hists;
};


class HiggsGenHist: public Hists {
public:
    explicit HiggsGenHist(Context & ctx,
                        const string & dirname,
                        const string & handlename,
                        const string & version):
        Hists(ctx, dirname),
        hndl(ctx.get_handle<std::vector<TopJet>>(handlename)),
        versionname(version),
        hist1(book<TH1F>("dR_gen_higgs_"+handlename+"_"+versionname+"_1", "dR(GenHiggs, 1st TopJet)", 60, 0., 6.)),
        hist2(book<TH1F>("dR_gen_higgs_"+handlename+"_"+versionname+"_2", "dR(GenHiggs, 2nd TopJet)", 60, 0., 6.)),
        hist3(book<TH1F>("dR_gen_higgs_"+handlename+"_"+versionname+"_3", "dR(GenHiggs, 3rd TopJet)", 60, 0., 6.)) {}

    virtual void fill(const Event & event) override {
        // if (TpTpAnalysisModule::version.find(versionname) == string::npos)
        //     return;
        assert(event.genparticles);
        if (event.is_valid(hndl)) {
            std::vector<TopJet> const & tj_coll = event.get(hndl);
            GenParticle const *higgs1 = 0;
            GenParticle const *higgs2 = 0;
            TopJet const *tj1 = 0;
            TopJet const *tj2 = 0;
            TopJet const *tj3 = 0;
            if (tj_coll.size())
                tj1 = &tj_coll[0];
            if (tj_coll.size() > 1)
                tj2 = &tj_coll[1];
            if (tj_coll.size() > 2)
                tj3 = &tj_coll[2];
            for (GenParticle const & gp : *event.genparticles) {
                if (abs(gp.pdgId()) == 25) {
                    GenParticle const * daughter1 = gp.daughter(event.genparticles);
                    if (daughter1 && abs(daughter1->pdgId()) == 5) {
                        if (!higgs1)
                            higgs1 = &gp;
                        else
                            higgs2 = &gp;
                    }
                }
            }
            if (higgs1 && !higgs2) {
                if (tj1) hist1->Fill(deltaR(*higgs1, *tj1), event.weight);
                if (tj2) hist2->Fill(deltaR(*higgs1, *tj2), event.weight);
                if (tj3) hist3->Fill(deltaR(*higgs1, *tj3), event.weight);
            }
            else if (higgs1 && higgs2) {
                std::vector<GenParticle> higgses = {*higgs1, *higgs2};
                // higgses.push_back(*higgs1);
                // higgses.push_back(*higgs2);
                if (tj1) hist1->Fill(deltaR(*closestParticle<GenParticle>(*tj1, higgses), *tj1), event.weight);
                if (tj2) hist2->Fill(deltaR(*closestParticle<GenParticle>(*tj2, higgses), *tj2), event.weight);
                if (tj3) hist3->Fill(deltaR(*closestParticle<GenParticle>(*tj3, higgses), *tj3), event.weight);
            }
        }
    }

private:
    Event::Handle<std::vector<TopJet>> hndl;
    string versionname;
    TH1F *hist1, *hist2, *hist3;
};


class JetCleaningControlPlots: public Hists {
public:
    explicit JetCleaningControlPlots(Context & ctx,
                        const string & dirname,
                        const string & ak4_weight
                        // const string & ak8_weight
                        ):
        Hists(ctx, dirname),
        ak4_w_hndl_(ctx.get_handle<float>(ak4_weight)),
        // ak8_w_hndl_(ctx.get_handle<float>(ak8_weight)),
        pt_ld_ak4_jet_hndl_(ctx.get_handle<float>("pt_ld_ak4_jet")),
        // pt_ld_ak8_jet_hndl_(ctx.get_handle<float>("pt_ld_ak8_jet")),
        st_hndl_(ctx.get_handle<double>("ST")),
        n_ak4_hndl_(ctx.get_handle<int>("n_ak4")),
        // n_ak8_hndl_(ctx.get_handle<int>("n_ak8")),
        st_cleaned(book<TH1F>("ST_cleaned", "ST cleaned", 45, 0, 4500)),
        met_cleaned(book<TH1F>("MET_cleaned","missing E_{T} cleaned", 200,0,1000)),
        pt_ak4_cleaned(book<TH1F>("pt_ak4_cleaned", "Pt(ld Ak4 Jet) cleaned", 60, 0., 1500.)),
        n_ak4_cleaned(book<TH1F>("n_ak4_cleaned", "N(Ak4 Jet) cleaned", 15, -.5, 14.5))
        // pt_ak8_cleaned(book<TH1F>("pt_ak8_cleaned", "Pt(ld Ak8 Jet) cleaned", 60, 0., 1500.)),
        // n_ak8_cleaned(book<TH1F>("n_ak8_cleaned", "N(Ak8 Jet) cleaned", 8, -.5, 7.5))
        {}

    virtual void fill(const Event & event) override {
        // if (TpTpAnalysisModule::version.find(versionname) == string::npos)
        //     return;
        auto pt_ld_ak4_jet = event.get(pt_ld_ak4_jet_hndl_);
        // auto pt_ld_ak8_jet = event.get(pt_ld_ak8_jet_hndl_);
        auto st = event.get(st_hndl_);
        auto n_ak4 = event.get(n_ak4_hndl_);
        // auto n_ak8 = event.get(n_ak8_hndl_);
        auto ak4_ptreweight = event.get(ak4_w_hndl_);
        // auto ak8_ptreweight = event.get(ak8_w_hndl_);


        pt_ak4_cleaned->Fill(pt_ld_ak4_jet, event.weight*ak4_ptreweight);
        // pt_ak8_cleaned->Fill(pt_ld_ak8_jet, event.weight*ak8_ptreweight);
        st_cleaned->Fill(st, event.weight*ak4_ptreweight);
        met_cleaned->Fill(event.met->pt(), event.weight*ak4_ptreweight);
        n_ak4_cleaned->Fill(n_ak4, event.weight*ak4_ptreweight);
        // n_ak8_cleaned->Fill(n_ak8, event.weight/ak8_ptreweight);
    }

private:
    Event::Handle<float> ak4_w_hndl_, pt_ld_ak4_jet_hndl_;
    Event::Handle<double> st_hndl_;
    Event::Handle<int> n_ak4_hndl_;
    TH1F *st_cleaned, *met_cleaned, *pt_ak4_cleaned, *n_ak4_cleaned;
};


template<typename T>
class RecoGenVarComp: public Hists {
public:
    explicit RecoGenVarComp(Context & ctx,
                         const string & dirname,
                         const string & reco_var_name,
                         const string & gen_var_name,
                         const string & var_name):
        Hists(ctx, dirname),
        h_reco_var(ctx.get_handle<T>(reco_var_name)),
        h_gen_var(ctx.get_handle<T>(gen_var_name)),
        hist(book<TH2F>("RecoGen_"+var_name,
                        ";reco "+var_name+";gen "+var_name,
                        45, 0., 4500., 45, 0., 4500.)) {}

    virtual void fill(const Event & e) override {
        if (!e.is_valid(h_reco_var) || !e.is_valid(h_gen_var)) {
            return;
        }
        hist->Fill(e.get(h_reco_var), e.get(h_gen_var), e.weight);
    }

private:
    Event::Handle<T> h_reco_var;
    Event::Handle<T> h_gen_var;
    TH2F * hist;
};


class VarSTComparison: public Hists {
public:
    explicit VarSTComparison(Context & ctx,
                         const string & dirname,
                         const string & var_name,
                         const string & st_name = "ST"):
        Hists(ctx, dirname),
        h_var(ctx.get_handle<float>(var_name)),
        h_st(ctx.get_handle<double>(st_name)),
        hist_2d(book<TH2F>("Comp_"+st_name+"_"+var_name,
                        ";"+st_name+";"+var_name,
                        65, 0., 6500., 50, 0., 5.))
        // hist_1d(book<TH1F>("Sing_"+var_name,
        //                 "Sing_"+var_name, 50, 0., 5.))
        {}

    virtual void fill(const Event & e) override {
        assert(e.is_valid(h_var) && e.is_valid(h_st));
        hist_2d->Fill(e.get(h_st), e.get(h_var), e.weight);
        // hist_1d->Fill(e.get(h_var), e.weight);
    }

private:
    Event::Handle<float> h_var;
    Event::Handle<double> h_st;
    TH2F * hist_2d;
    // TH1F * hist_1d;
};

// SelectedSelHists
class TriggerEffHists: public Hists {
public:
    explicit TriggerEffHists(Context & ctx,
                         const string & dir,
                         const SelItemsHelper & sel_helper,
                         const vector<string> & dists,
                         const vector<string> & veto_selections):
        Hists(ctx, dir),
        h_sel_res(ctx.get_handle<vector<bool>>(sel_helper.s_vec_bool())),
        v_all_items(sel_helper.get_item_names()),
        dists_(dists),
        v_veto_selections(veto_selections)
    {
        for (const string & item : v_all_items) {
            for (const string & dist : dists) {
                if (dist == item) {
                    v_hists_eff[dist+"_sub"] = move(unique_ptr<Hists>(sel_helper.get_sel_item(dist)->make_hists(ctx, dir, "_sub")));
                    v_hists_eff[dist+"_tot"] = move(unique_ptr<Hists>(sel_helper.get_sel_item(dist)->make_hists(ctx, dir, "_tot")));
                }
            }
        }
    }

    void insert_sel(unsigned pos, const string & sel) {
        // v_hists.insert(v_hists.begin() + pos, move(unique_ptr<Hists>(hists)));
        v_all_items.insert(v_all_items.begin() + pos, sel);
    }

    // void insert_additional_hist(Hists * hists) {
    //     v_hists.push_back(move(unique_ptr<Hists>(hists)));
    // }

    virtual void fill(const Event & event) override {
        // SelectedSelHists::fill(event);
        const auto & v_accept = event.get(h_sel_res);
        assert(v_accept.size() == v_all_items.size());
        for (unsigned i = 0; i < dists_.size(); ++i) {
            bool accept_all = true;
            bool accept_sel = true;
            string dist = dists_[i];
            vector<string>::const_iterator it = v_all_items.begin();
            for (;it != v_all_items.end(); ++it) {
                if (*it == dist)
                    break;
            }
            if (it == v_all_items.end())
                continue;
            for (unsigned j=0; j<v_accept.size(); ++j) {
                bool ignore_sel = v_veto_selections.size() ? false : true;
                if (dist == v_all_items[j])
                    ignore_sel = true;
                for (const string & sel : v_veto_selections) {
                    if (sel == v_all_items[j]) {
                        ignore_sel = true;  
                        if (!v_accept[j])
                            accept_sel = false;
                        break;
                    }
                }
                if (!ignore_sel) {
                    if (!v_accept[j]) {
                        accept_all = false;
                        break;
                    }
                }
            }
            if (accept_all) {
                v_hists_eff[dist+"_tot"]->fill(event);
                if (accept_sel)
                    v_hists_eff[dist+"_sub"]->fill(event);
            }
        }
    }

private:
    Event::Handle<vector<bool>> h_sel_res;
    vector<string> v_all_items;
    // const vector<string> v_selections;
    const vector<string> dists_;
    const vector<string> v_veto_selections;
    map<string, unique_ptr<Hists>> v_hists_eff;
};


// SelectedSelHists
template<typename T>
class TagEffHists: public Hists {
public:

    typedef std::function<bool (const T &, const uhh2::Event &)> TYPE_ID;

    explicit TagEffHists(Context & ctx,
                         const string & dir,
                         const string & h_name,
                         const string & h_in,
                         TYPE_ID const & id_den = TrueId<T>::is_true,
                         TYPE_ID const & id_num = TrueId<T>::is_true
                         ):
        Hists(ctx, dir),
        h_in_(ctx.get_handle<std::vector<T>>(h_in)),
        h_num_pt_(book<TH1F>(h_name+"_pt_sub", h_name+"_pt_sub", 120, 0., 2400.)),
        h_den_pt_(book<TH1F>(h_name+"_pt_tot", h_name+"_pt_tot", 120, 0., 2400.)),
        h_num_eta_(book<TH1F>(h_name+"_eta_sub", h_name+"_eta_sub", 50, -3., 3.)),
        h_den_eta_(book<TH1F>(h_name+"_eta_tot", h_name+"_eta_tot", 50, -3., 3.)),
        h_num_incl_(book<TH1F>(h_name+"_incl_sub", h_name+"_incl_sub", 1, 0.5, 1.5)),
        h_den_incl_(book<TH1F>(h_name+"_incl_tot", h_name+"_incl_tot", 1, 0.5, 1.5)),
        id_den_(id_den),
        id_num_(id_num)
    {}

    // void insert_additional_hist(Hists * hists) {
    //     v_hists.push_back(move(unique_ptr<Hists>(hists)));
    // }

    virtual void fill(const Event & event) override {
        // SelectedSelHists::fill(event);
        // double w = event.weight;

        if (!event.is_valid(h_in_))
            throw;
        const std::vector<T> coll_in = event.get(h_in_);

        for (const T & p : coll_in) {
            if (id_den_(p, event)) {
                // std::cout << "    topjet pt/eta/phi/mass/csv1/csv2: " << p.pt() << "/" << p.eta() << "/" << p.phi() << "/" << p.softdropmass();
                // if (p.subjets().size())
                //     std::cout << "/" << p.subjets()[0].btag_combinedSecondaryVertex();
                // if (p.subjets().size() > 1)
                //     std::cout << "/" << p.subjets()[1].btag_combinedSecondaryVertex();
                // std::cout << std::endl;
                // std::cout << "   DENOMINATOR:" << std::endl;
                h_den_pt_->Fill(p.pt());
                h_den_eta_->Fill(p.eta());
                h_den_incl_->Fill(1.);
            }
            if (id_den_(p, event) && id_num_(p, event)) {
                // std::cout << "    topjet TAGGED pt/eta/phi/mass/csv1/csv2: " << p.pt() << "/" << p.eta() << "/" << p.phi() << "/" << p.softdropmass();
                // if (p.subjets().size())
                //     std::cout << "/" << p.subjets()[0].btag_combinedSecondaryVertex();
                // if (p.subjets().size() > 1)
                //     std::cout << "/" << p.subjets()[1].btag_combinedSecondaryVertex();
                // std::cout << std::endl;
                // std::cout << "   NUMERATOR:" << std::endl;
                h_num_pt_->Fill(p.pt());
                h_num_eta_->Fill(p.eta());
                h_num_incl_->Fill(1.);
            }
        }
    }

private:
    Event::Handle<vector<T>> h_in_;
    TH1F *h_num_pt_, *h_den_pt_, *h_num_eta_, *h_den_eta_, *h_num_incl_, *h_den_incl_;
    TYPE_ID id_den_, id_num_;
};


class AK8TagEffHists: public Hists {
public:

    typedef std::function<bool (const TopJet &, const uhh2::Event &)> TYPE_ID;

    explicit AK8TagEffHists(Context & ctx,
                         const string & dir,
                         const string & h_name,
                         const string & h_in,
                         TYPE_ID const & id_den = TrueId<TopJet>::is_true,
                         TYPE_ID const & id_num = TrueId<TopJet>::is_true
                         ):
        Hists(ctx, dir),
        h_in_(ctx.get_handle<std::vector<TopJet>>(h_in)),
        h_num_pt_(book<TH1F>(h_name+"_pt_sub", h_name+"_pt_sub", 120, 0., 2400.)),
        h_den_pt_(book<TH1F>(h_name+"_pt_tot", h_name+"_pt_tot", 120, 0., 2400.)),
        h_num_eta_(book<TH1F>(h_name+"_eta_sub", h_name+"_eta_sub", 50, -3., 3.)),
        h_den_eta_(book<TH1F>(h_name+"_eta_tot", h_name+"_eta_tot", 50, -3., 3.)),
        h_num_mass_(book<TH1F>(h_name+"_mass_sub", h_name+"_mass_sub", 100, 0., 300.)),
        h_den_mass_(book<TH1F>(h_name+"_mass_tot", h_name+"_mass_tot", 100, 0., 300.)),
        h_num_nsjbtags_(book<TH1F>(h_name+"_nsjbtags_sub", h_name+"_nsjbtags_sub", 6, -0.5, 5.5)),
        h_den_nsjbtags_(book<TH1F>(h_name+"_nsjbtags_tot", h_name+"_nsjbtags_tot", 6, -0.5, 5.5)),
        h_num_incl_(book<TH1F>(h_name+"_incl_sub", h_name+"_incl_sub", 1, 0.5, 1.5)),
        h_den_incl_(book<TH1F>(h_name+"_incl_tot", h_name+"_incl_tot", 1, 0.5, 1.5)),
        id_den_(id_den),
        id_num_(id_num)
    {}

    // void insert_additional_hist(Hists * hists) {
    //     v_hists.push_back(move(unique_ptr<Hists>(hists)));
    // }

    virtual void fill(const Event & event) override {
        // SelectedSelHists::fill(event);
        // double w = event.weight;

        if (!event.is_valid(h_in_))
            throw;
        const std::vector<TopJet> coll_in = event.get(h_in_);

        // std::cout << "  NEW HISTOGRAM" << std::endl;
        for (const TopJet & p : coll_in) {
            if (id_den_(p, event)) {
                // std::cout << "    topjet pt/eta/phi/mass/csv1/csv2: " << p.pt() << "/" << p.eta() << "/" << p.phi() << "/" << p.softdropmass();
                // if (p.subjets().size())
                //     std::cout << "/" << p.subjets()[0].btag_combinedSecondaryVertex();
                // if (p.subjets().size() > 1)
                //     std::cout << "/" << p.subjets()[1].btag_combinedSecondaryVertex();
                // std::cout << std::endl;
                // std::cout << "   DENOMINATOR:" << std::endl;
                CSVBTag btag_(CSVBTag::WP_MEDIUM);
                int n_sj = 0;
                for (auto const & sj : p.subjets()) {
                    if (btag_(sj, event))
                        n_sj++;
                }
                h_den_pt_->Fill(p.pt());
                h_den_eta_->Fill(p.eta());
                h_den_mass_->Fill(p.softdropmass());
                h_den_nsjbtags_->Fill(n_sj);
                h_den_incl_->Fill(1.);
            }
            if (id_den_(p, event) && id_num_(p, event)) {
                // std::cout << "    topjet TAGGED pt/eta/phi/mass/csv1/csv2: " << p.pt() << "/" << p.eta() << "/" << p.phi() << "/" << p.softdropmass();
                // if (p.subjets().size())
                //     std::cout << "/" << p.subjets()[0].btag_combinedSecondaryVertex();
                // if (p.subjets().size() > 1)
                //     std::cout << "/" << p.subjets()[1].btag_combinedSecondaryVertex();
                // std::cout << std::endl;
                // std::cout << "   NUMERATOR:" << std::endl;
                CSVBTag btag_(CSVBTag::WP_MEDIUM);
                int n_sj = 0;
                for (auto const & sj : p.subjets()) {
                    if (btag_(sj, event))
                        n_sj++;
                }
                h_num_pt_->Fill(p.pt());
                h_num_eta_->Fill(p.eta());
                h_num_mass_->Fill(p.softdropmass());
                h_num_nsjbtags_->Fill(n_sj);
                h_num_incl_->Fill(1.);
            }
        }
    }

private:
    Event::Handle<vector<TopJet>> h_in_;
    TH1F *h_num_pt_, *h_den_pt_, *h_num_eta_, *h_den_eta_, *h_num_mass_, *h_den_mass_, *h_num_nsjbtags_, *h_den_nsjbtags_, *h_num_incl_, *h_den_incl_;
    TYPE_ID id_den_, id_num_;
};


// SelectedSelHists
template<typename T>
class SelEffHists: public Hists {
public:

    // typedef std::function<bool (const T &, const uhh2::Event &)> TYPE_ID;

    SelEffHists(Context & ctx,
                         const string & dir,
                         const string & h_in,
                         const string & h_name,
                         Selection * sel_den,
                         Selection * sel_num,
                         int n_bins, float min_x, float max_x,
                         T inc_cut_min = -999999., T inc_cut_max = 999999.
                         ):
        Hists(ctx, dir),
        h_in_name_(h_in),
        h_in_(ctx.get_handle<T>(h_in)),
        h_num_(book<TH1F>(h_name+"_sub", h_name+"_sub", n_bins, min_x, max_x)),
        h_den_(book<TH1F>(h_name+"_tot", h_name+"_tot", n_bins, min_x, max_x)),
        h_incl_num_(book<TH1F>(h_name+"_incl_sub", h_name+"_incl_sub", 1, .5, 1.5)),
        h_incl_den_(book<TH1F>(h_name+"_incl_tot", h_name+"_incl_tot", 1, .5, 1.5)),
        sel_den_(sel_den),
        sel_num_(sel_num),
        inc_cut_min_(inc_cut_min),
        inc_cut_max_(inc_cut_max)
    {}

    // void insert_additional_hist(Hists * hists) {
    //     v_hists.push_back(move(unique_ptr<Hists>(hists)));
    // }

    vector<shared_ptr<Hists>> & get_add_hists_den() {
        return add_hists_den_;
    }
    vector<shared_ptr<Hists>> & get_add_hists_num() {
        return add_hists_num_;
    }

    virtual void fill(const Event & event) override {
        // SelectedSelHists::fill(event);
        // double w = event.weight;

        if (!event.is_valid(h_in_))
            throw runtime_error("Handle " + h_in_name_ + " not valid!");
        T var = event.get(h_in_);

        if (sel_den_->passes(event)) {
            // std::cout << "    topjet pt/eta/phi/mass/csv1/csv2: " << p.pt() << "/" << p.eta() << "/" << p.phi() << "/" << p.softdropmass();
            // if (p.subjets().size())
            //     std::cout << "/" << p.subjets()[0].btag_combinedSecondaryVertex();
            // if (p.subjets().size() > 1)
            //     std::cout << "/" << p.subjets()[1].btag_combinedSecondaryVertex();
            // std::cout << std::endl;
            // std::cout << "   DENOMINATOR:" << std::endl;
            h_den_->Fill(var);
            if (var > inc_cut_min_ && var < inc_cut_max_)
                h_incl_den_->Fill(1.);
            for (auto & hist : add_hists_den_) {
                hist->fill(event);
            }
        }
        if (sel_den_->passes(event) && sel_num_->passes(event)) {
            // std::cout << "    topjet TAGGED pt/eta/phi/mass/csv1/csv2: " << p.pt() << "/" << p.eta() << "/" << p.phi() << "/" << p.softdropmass();
            // if (p.subjets().size())
            //     std::cout << "/" << p.subjets()[0].btag_combinedSecondaryVertex();
            // if (p.subjets().size() > 1)
            //     std::cout << "/" << p.subjets()[1].btag_combinedSecondaryVertex();
            // std::cout << std::endl;
            // std::cout << "   NUMERATOR:" << std::endl;
            h_num_->Fill(var);
            if (var > inc_cut_min_ && var < inc_cut_max_)
                h_incl_num_->Fill(1.);
            for (auto & hist : add_hists_num_) {
                hist->fill(event);
            }
        }
    }

private:
    std::string h_in_name_;
    Event::Handle<T> h_in_;
    TH1F *h_num_, *h_den_, *h_incl_num_, *h_incl_den_;
    Selection *sel_den_, *sel_num_;
    vector<shared_ptr<Hists>> add_hists_den_, add_hists_num_;
    T inc_cut_min_, inc_cut_max_;
};