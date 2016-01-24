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
                    if (particle.subjets().size()){
                        LorentzVector sum_subjets;
                        for (Jet const & subjet : particle.subjets())
                            sum_subjets += subjet.v4();
                        it->second->Fill(sum_subjets.M(), w);
                    } else {
                        it->second->Fill(-1., w);
                    }
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
        part_ind_(part_ind) {
        }

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

private:
    string rel_dirname_;
    string h_name_;
    vector<string> variables_;
    std::map<string, unsigned> indizes_;
    vector<NParticleMultiHistProducerHelper<T>> sub_levels_;
    unsigned part_ind_;
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
                        const string & ak4_weight,
                        const string & ak8_weight):
        Hists(ctx, dirname),
        ak4_w_hndl_(ctx.get_handle<float>(ak4_weight)),
        ak8_w_hndl_(ctx.get_handle<float>(ak8_weight)),
        pt_ld_ak4_jet_hndl_(ctx.get_handle<float>("pt_ld_ak4_jet")),
        pt_ld_ak8_jet_hndl_(ctx.get_handle<float>("pt_ld_ak8_jet")),
        st_hndl_(ctx.get_handle<double>("ST")),
        n_ak4_hndl_(ctx.get_handle<int>("n_ak4")),
        n_ak8_hndl_(ctx.get_handle<int>("n_ak8")),
        st_cleaned(book<TH1F>("ST_cleaned", "ST cleaned", 45, 0, 4500)),
        met_cleaned(book<TH1F>("MET_cleaned","missing E_{T} cleaned", 200,0,1000)),
        pt_ak4_cleaned(book<TH1F>("pt_ak4_cleaned", "Pt(ld Ak4 Jet) cleaned", 60, 0., 1500.)),
        n_ak4_cleaned(book<TH1F>("n_ak4_cleaned", "N(Ak4 Jet) cleaned", 15, -.5, 14.5)),
        pt_ak8_cleaned(book<TH1F>("pt_ak8_cleaned", "Pt(ld Ak8 Jet) cleaned", 60, 0., 1500.)),
        n_ak8_cleaned(book<TH1F>("n_ak8_cleaned", "N(Ak8 Jet) cleaned", 8, -.5, 7.5)) {}

    virtual void fill(const Event & event) override {
        // if (TpTpAnalysisModule::version.find(versionname) == string::npos)
        //     return;
        auto pt_ld_ak4_jet = event.get(pt_ld_ak4_jet_hndl_);
        auto pt_ld_ak8_jet = event.get(pt_ld_ak8_jet_hndl_);
        auto st = event.get(st_hndl_);
        auto n_ak4 = event.get(n_ak4_hndl_);
        auto n_ak8 = event.get(n_ak8_hndl_);
        auto ak4_ptreweight = event.get(ak4_w_hndl_);
        auto ak8_ptreweight = event.get(ak8_w_hndl_);


        pt_ak4_cleaned->Fill(pt_ld_ak4_jet, event.weight*ak4_ptreweight);
        pt_ak8_cleaned->Fill(pt_ld_ak8_jet, event.weight*ak8_ptreweight);
        st_cleaned->Fill(st, event.weight*ak4_ptreweight);
        met_cleaned->Fill(event.met->pt(), event.weight*ak4_ptreweight);
        n_ak4_cleaned->Fill(n_ak4, event.weight*ak4_ptreweight);
        n_ak8_cleaned->Fill(n_ak8, event.weight*ak8_ptreweight);
    }

private:
    Event::Handle<float> ak4_w_hndl_, ak8_w_hndl_, pt_ld_ak4_jet_hndl_, pt_ld_ak8_jet_hndl_;
    Event::Handle<double> st_hndl_;
    Event::Handle<int> n_ak4_hndl_, n_ak8_hndl_;
    TH1F *st_cleaned, *met_cleaned, *pt_ak4_cleaned, *n_ak4_cleaned, *pt_ak8_cleaned, *n_ak8_cleaned;
};