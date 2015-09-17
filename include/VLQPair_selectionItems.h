#pragma once

#include <vector>
#include "UHH2/VLQSemiLepPreSel/include/SelectionItem.h"


typedef SelectionItemData<int>      SelDatI;
typedef SelectionItemData<float>    SelDatF;
typedef SelectionItemData<double>   SelDatD;


static const vector<shared_ptr<SelectionItem>> SEL_ITEMS_VLQPair_loose_base {
    shared_ptr<SelectionItem>(new SelDatI("trigger_accept",         "trigger accept",                          2, -.5, 1.5          ,1      )),
    shared_ptr<SelectionItem>(new SelDatD("ST",                     "ST",                                     30,  0, 3000          ,700    )),
    shared_ptr<SelectionItem>(new SelDatI("n_btags",                "N_{b-tag}",                              11, -.5, 10.5         ,1      )),
    shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt",      "primary lepton p_{T}",                   90,   0, 900          ,25.    )),
    shared_ptr<SelectionItem>(new SelDatF("leading_jet_pt",         "leading jet p_{T}",                      50,   0, 1500                 )),
    
    shared_ptr<SelectionItem>(new SelDatI("n_leptons",              "N_{lepton}",                             11, -.5, 10.5                 )),
    shared_ptr<SelectionItem>(new SelDatI("n_jets",                 "N_{jet}",                                21, -.5, 20.5                 )),
    shared_ptr<SelectionItem>(new SelDatF("subleading_jet_pt",      "sub-leading jet p_{T}",                  15,   0, 1500                 )),
    // shared_ptr<SelectionItem>(new SelDatF("smallest_pt_toptags",    "smallest pt of toptags",                 15,   0, 1500                 )),
    // shared_ptr<SelectionItem>(new SelDatF("min_deltaR_top_higgsak8","min deltaR(top, higgs)",                 20,   0, 5.                   )),
    // shared_ptr<SelectionItem>(new SelDatF("min_deltaR_top_higgsak8notop","min deltaR(top, higgs(separated))", 20,   0, 5.                   )),
    // shared_ptr<SelectionItem>(new SelDatF("min_deltaR_top_higgsak8_twotop","min deltaR(top, higgs, two tops)",                 20,   0, 5.  )),
    // shared_ptr<SelectionItem>(new SelDatF("min_deltaR_top_higgsak8notop_twotop","min deltaR(top, higgs(separated), two tops)", 20,   0, 5.  )),

};

static const vector<shared_ptr<SelectionItem>> SEL_ITEMS_VLQPair_tight_base {
    shared_ptr<SelectionItem>(new SelDatI("n_jets",                 "N_{jet}",                                21, -.5, 20.5         ,4      )),
    shared_ptr<SelectionItem>(new SelDatF("leading_jet_pt",         "leading jet p_{T}",                      15,   0, 1500         ,250.   )),
    shared_ptr<SelectionItem>(new SelDatF("subleading_jet_pt",      "sub-leading jet p_{T}",                  15,   0, 1500         ,100.   )),
    shared_ptr<SelectionItem>(new SelDatI("n_toptags",              "N_{Top Tags}",                           11, -.5, 10.5         ,1      )),

    shared_ptr<SelectionItem>(new SelDatI("n_leptons",              "N_{lepton}",                             11, -.5, 10.5                 )),
    shared_ptr<SelectionItem>(new SelDatD("ST",                     "ST",                                     30,  0, 3000                  )),
    shared_ptr<SelectionItem>(new SelDatI("n_btags",                "N_{b-tag}",                              11, -.5, 10.5                 )),
    shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt",      "primary lepton p_{T}",                   90,   0,  900                 )),
    shared_ptr<SelectionItem>(new SelDatF("smallest_pt_toptags",    "smallest pt of toptags",                 15,   0, 1500                 )),\
    shared_ptr<SelectionItem>(new SelDatF("leading_topjet_pt",      "leading topjet p_{T}",                   15,   0, 1500                 )),
    shared_ptr<SelectionItem>(new SelDatF("leading_ak8jet_pt",      "leading AK8 jet p_{T}",                  15,   0, 1500                 )),
    shared_ptr<SelectionItem>(new SelDatF("leading_ca15jet_pt",     "leading CA15 jet p_{T}",                 15,   0, 1500                 )),
    
    shared_ptr<SelectionItem>(new SelDatF("mass_ld_toptag",         "Mass ld Top tag",                        60,   0, 300                  )),
    shared_ptr<SelectionItem>(new SelDatF("mass_sj_ld_toptag",         "Mass (of Subjets) ld Top tag",                        60,   0, 300  )),
    shared_ptr<SelectionItem>(new SelDatF("mass_ld_higgs_tag_ak8",  "Mass ld Higgs tag (AK8)",                60,   0, 300                  )),
    shared_ptr<SelectionItem>(new SelDatF("mass_ld_higgs_tag_ak8_notop",  "Mass ld Higgs tag (AK8), no top",  60,   0, 300                  )),
    shared_ptr<SelectionItem>(new SelDatF("mass_sj_ld_higgs_tag_ak8",  "Mass (of Subjets) ld Higgs tag (AK8)",                60,   0, 300  )),
    shared_ptr<SelectionItem>(new SelDatF("mass_sj_ld_higgs_tag_ak8_notop",  "Mass (of Subjets) ld Higgs tag (AK8), no top",  60,   0, 300  )),
    shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_ca15",      "N_{H Tags (CA15)}",                      11, -.5, 10.5                 )),
    shared_ptr<SelectionItem>(new SelDatF("mass_ld_higgs_tag_ca15", "Mass ld Higgs tag (CA15)",               60,   0, 300                  )),
    shared_ptr<SelectionItem>(new SelDatF("mass_sj_ld_higgs_tag_ca15", "Mass (of Subjets) ld Higgs tag (CA15)",               60,   0, 300  )),
    shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_ca15_notop", "N_{H Tags (CA15), no top}",             11, -.5, 10.5                 )),
    shared_ptr<SelectionItem>(new SelDatF("mass_ld_higgs_tag_ca15_notop", "Mass ld Higgs tag (CA15), no top", 60,   0, 300                  )),
    shared_ptr<SelectionItem>(new SelDatF("mass_sj_ld_higgs_tag_ca15_notop", "Mass (of Subjets) ld Higgs tag (CA15), no top", 60,   0, 300  )),
    shared_ptr<SelectionItem>(new SelDatF("min_deltaR_top_higgsak8","min deltaR(top, higgs)",                 20,   0, 5.                   )),
    shared_ptr<SelectionItem>(new SelDatF("min_deltaR_top_higgsak8notop","min deltaR(top, higgs(separated))", 20,   0, 5.                   )),
    shared_ptr<SelectionItem>(new SelDatF("min_deltaR_top_higgsak8_twotop","min deltaR(top, higgs, two tops)",                 20,   0, 5.  )),
    shared_ptr<SelectionItem>(new SelDatF("min_deltaR_top_higgsak8notop_twotop","min deltaR(top, higgs(separated), two tops)", 20,   0, 5.  )),
};

static const vector<shared_ptr<SelectionItem>> SEL_ITEMS_VLQPair_testQCD_base {
    shared_ptr<SelectionItem>(new SelDatI("n_jets",                 "N_{jet}",                                21, -.5, 20.5                 )),
    shared_ptr<SelectionItem>(new SelDatF("leading_jet_pt",         "leading jet p_{T}",                      15,   0, 1500                 )),
    shared_ptr<SelectionItem>(new SelDatF("subleading_jet_pt",      "sub-leading jet p_{T}",                  15,   0, 1500                 )),
    // shared_ptr<SelectionItem>(new SelDatI("n_toptags",              "N_{Top Tags}",                           11, -.5, 10.5                 )),
    shared_ptr<SelectionItem>(new SelDatI("n_leptons",              "N_{lepton}",                             11, -.5, 10.5                 )),
    // shared_ptr<SelectionItem>(new SelDatD("ST",                     "ST",                                     30,  0, 3000                  )),
    shared_ptr<SelectionItem>(new SelDatF("smallest_pt_toptags",    "smallest pt of toptags",                 15,   0, 1500                 )),
    shared_ptr<SelectionItem>(new SelDatF("min_deltaR_top_higgsak8","min deltaR(top, higgs)",                 20,   0, 5.                   )),
    shared_ptr<SelectionItem>(new SelDatF("min_deltaR_top_higgsak8notop","min deltaR(top, higgs(separated))", 20,   0, 5.                   )),
    shared_ptr<SelectionItem>(new SelDatF("min_deltaR_top_higgsak8_twotop","min deltaR(top, higgs, two tops)",                 20,   0, 5.  )),
    shared_ptr<SelectionItem>(new SelDatF("min_deltaR_top_higgsak8notop_twotop","min deltaR(top, higgs(separated), two tops)", 20,   0, 5.  )),
};


static const vector<shared_ptr<SelectionItem>> SEL_ITEMS_VLQPair_controlregion_base {
    // shared_ptr<SelectionItem>(new SelDatI("n_toptags",              "N_{Top Tags}",                           11, -.5, 10.5         ,1      )),
    shared_ptr<SelectionItem>(new SelDatI("trigger_accept",         "trigger accept",                          2, -.5, 1.5,             1   )),
    shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt",      "primary lepton p_{T}",                   90,   0,  900            ,50. )),

    shared_ptr<SelectionItem>(new SelDatD("ST",                     "ST",                                     30,  0, 3000             ,600.)),
    shared_ptr<SelectionItem>(new SelDatI("n_jets",                 "N_{jet}",                                21, -.5, 20.5                 )),
    shared_ptr<SelectionItem>(new SelDatF("met",                    "MET",                                    50,   0, 1000                 )),
    shared_ptr<SelectionItem>(new SelDatF("leading_jet_pt",         "leading jet p_{T}",                      15,   0, 1500                 )),
    shared_ptr<SelectionItem>(new SelDatF("leading_ele_pt",         "leading electron p_{T}",                 90,   0, 900                  )),
    shared_ptr<SelectionItem>(new SelDatF("leading_mu_pt",          "leading muon p_{T}",                     90,   0, 900                  )),
    shared_ptr<SelectionItem>(new SelDatF("subleading_jet_pt",      "sub-leading jet p_{T}",                  15,   0, 1500                 )),
    shared_ptr<SelectionItem>(new SelDatI("n_leptons",              "N_{lepton}",                             11, -.5, 10.5                 )),
    shared_ptr<SelectionItem>(new SelDatI("n_btags",                "N_{b-tag}",                              11, -.5, 10.5                 )),
    shared_ptr<SelectionItem>(new SelDatI("n_additional_btags", "N_{additional b-tags}",                      11, -.5, 10.5                 )),
    shared_ptr<SelectionItem>(new SelDatF("smallest_pt_toptags",    "smallest pt of toptags",                 15,   0, 1500                 )),

    shared_ptr<SelectionItem>(new SelDatF("min_deltaR_top_higgsak8","min deltaR(top, higgs)",                 20,   0, 5.                   )),
    shared_ptr<SelectionItem>(new SelDatF("min_deltaR_top_higgsak8notop","min deltaR(top, higgs(separated))", 20,   0, 5.                   )),
    shared_ptr<SelectionItem>(new SelDatF("min_deltaR_top_higgsak8_twotop","min deltaR(top, higgs, two tops)",                 20,   0, 5.  )),
    shared_ptr<SelectionItem>(new SelDatF("min_deltaR_top_higgsak8notop_twotop","min deltaR(top, higgs(separated), two tops)", 20,   0, 5.  )),
};