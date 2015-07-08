#pragma once

#include <vector>
#include "UHH2/VLQSemiLepPreSel/include/SelectionItem.h"


typedef SelectionItemData<int>      SelDatI;
typedef SelectionItemData<float>    SelDatF;
typedef SelectionItemData<double>   SelDatD;


static const vector<shared_ptr<SelectionItem>> SEL_ITEMS_VLQPair_loose {
    shared_ptr<SelectionItem>(new SelDatI("trigger_accept",    "ele+Jets OR mu+Jets",      2,  -.5, 1.5        ,1      )),
    shared_ptr<SelectionItem>(new SelDatI("n_leptons",         "N_{lepton}",               11, -.5, 10.5       ,1      )),
    shared_ptr<SelectionItem>(new SelDatD("ST",                "ST",                       100,  0, 5000       ,700    )),
    shared_ptr<SelectionItem>(new SelDatF("leading_jet_pt",    "leading jet p_{T}",        50,   0, 1500       ,200    )),

    shared_ptr<SelectionItem>(new SelDatF("subleading_jet_pt", "sub-leading jet p_{T}",    50,   0, 1500               )),
    shared_ptr<SelectionItem>(new SelDatI("n_btags",           "N_{b-tag}",                11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatI("n_jets",            "N_{jet}",                  21, -.5, 20.5               )),
    shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_ca15", "N_{H jet}",                11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_ca8",  "N_{H jet}",                11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatI("n_toptags",         "N_{H jet}",                11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt", "primary lepton p_{T}",     50, 100, 1500               )),
    shared_ptr<SelectionItem>(new SelDatF("min_deltaR_lep_nu", "min deltaR(lepton, nu)",   20, 0., 5.                  )),
    shared_ptr<SelectionItem>(new SelDatF("deltaR_leading_bjets", "deltaR(b1, b2)",        20, 0., 5.                  )),
    shared_ptr<SelectionItem>(new SelDatF("min_deltaR_lep_bjets", "min deltaR(lepton, leading bs)",   20, 0., 5.       )),
    // shared_ptr<SelectionItem>(new SelDatI("n_fwd_jets",        "N_{fwd jet}",              11, -.5, 10.5               )),
    // shared_ptr<SelectionItem>(new SelDatI("n_leading_btags",   "N_{b-tag leading}",        11, -.5, 10.5               )),
    // shared_ptr<SelectionItem>(new SelDatF("dr_higg_top",       "#DeltaR(H, t)",            50, 0, 5                    )),
    // shared_ptr<SelectionItem>(new SelDatF("tlep_pt",           "lept. top p_{T}",          50, 0, 1000                 )),
    // shared_ptr<SelectionItem>(new SelDatF("tlep_eta",          "lept. top #eta",           50, -5., 5.                 )),
    // shared_ptr<SelectionItem>(new SelDatF("tlep_mass",         "lept. top mass",           50, 0, 1000                 )),
    // shared_ptr<SelectionItem>(new SelDatF("h_pt",              "Higgs p_{T}",              50, 0, 1000                 )),
    // shared_ptr<SelectionItem>(new SelDatF("h_eta",             "Higgs #eta",               50, -5., 5.                 )),
    // shared_ptr<SelectionItem>(new SelDatF("h_mass",            "Higgs mass",               50, 0, 1000                 )),
    // shared_ptr<SelectionItem>(new SelDatF("vlq_pt",            "T p_{T}",                 50, 0, 1000                 )),
    // shared_ptr<SelectionItem>(new SelDatF("vlq_eta",           "T #eta",                  50, -5., 5.                 )),
    // shared_ptr<SelectionItem>(new SelDatF("vlq_mass",          "T mass",                  50, 0, 2000                 )),
};

static const vector<shared_ptr<SelectionItem>> SEL_ITEMS_VLQPair_tight_base {
    shared_ptr<SelectionItem>(new SelDatI("n_jets",                 "N_{jet}",                                21, -.5, 20.5         ,4    )),
    shared_ptr<SelectionItem>(new SelDatF("leading_jet_pt",         "leading jet p_{T}",                      15,   0, 1500         ,250. )),
    shared_ptr<SelectionItem>(new SelDatF("subleading_jet_pt",      "sub-leading jet p_{T}",                  15,   0, 1500         ,100. )),
    shared_ptr<SelectionItem>(new SelDatI("n_toptags",              "N_{Top Tags}",                           11, -.5, 10.5         ,1    )),
    shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_ca15",      "N_{H Tags (CA15)}",                      11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_ca15_notop", "N_{H Tags (CA15), no top}",             11, -.5, 10.5               )),
    // shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_ca8_notop", "N_{H Tags (CA8), no top}", 11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_ca8",       "N_{H Tags (CA8)}",                       11, -.5, 10.5               )),

    shared_ptr<SelectionItem>(new SelDatF("leading_topjet_pt",      "leading topjet p_{T}",                   15,   0, 1500               )),
    shared_ptr<SelectionItem>(new SelDatF("leading_ca8jet_pt",      "leading CA8 jet p_{T}",                  15,   0, 1500               )),
    shared_ptr<SelectionItem>(new SelDatF("leading_ca15jet_pt",     "leading CA15 jet p_{T}",                 15,   0, 1500               )),

    shared_ptr<SelectionItem>(new SelDatF("mass_ld_higgs_tag_ca15", "Mass ld Higgs tag (CA15)",               25,   0, 500                )),
    shared_ptr<SelectionItem>(new SelDatF("mass_ld_higgs_tag_ca8",  "Mass ld Higgs tag (CA8)",                25,   0, 500                )),
    shared_ptr<SelectionItem>(new SelDatF("mass_ld_higgs_tag_ca15_notop", "Mass ld Higgs tag (CA15), no top", 25,   0, 500                )),
    shared_ptr<SelectionItem>(new SelDatF("mass_ld_higgs_tag_ca8_notop",  "Mass ld Higgs tag (CA8), no top",  25,   0, 500                )),
    shared_ptr<SelectionItem>(new SelDatF("mass_ld_toptag",         "Mass ld Top tag",                        25,   0, 500                )),
    shared_ptr<SelectionItem>(new SelDatI("n_leptons",              "N_{lepton}",                             11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatD("ST",                     "ST",                                     40,   0, 5000               )),
    // shared_ptr<SelectionItem>(new SelDatI("n_genleptons",           "number gen leptons",                     11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatI("n_btags",                "N_{b-tag}",                              11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt",      "primary lepton p_{T}",                   15,   0, 1500               )),
    // shared_ptr<SelectionItem>(new SelDatF("min_deltaR_lep_nu",      "min deltaR(lepton, nu)",                 20,   0, 5.                 )),
    // shared_ptr<SelectionItem>(new SelDatF("deltaR_leading_bjets",   "deltaR(b1, b2)",                         20,   0, 5.                 )),
    // shared_ptr<SelectionItem>(new SelDatF("min_deltaR_lep_bjets",   "min deltaR(lepton, leading bs)",         20,   0, 5.                 )),
    shared_ptr<SelectionItem>(new SelDatF("smallest_pt_toptags",    "smallest pt of toptags",                 15,   0, 1500               )),
    // shared_ptr<SelectionItem>(new SelDatI("n_additional_btags",     "N_{additional b-tags}",    11, -.5, 10.5               )),
    // shared_ptr<SelectionItem>(new SelDatI("n_fwd_jets",        "N_{fwd jet}",              11, -.5, 10.5               )),
    // shared_ptr<SelectionItem>(new SelDatI("n_leading_btags",   "N_{b-tag leading}",        11, -.5, 10.5               )),
    // shared_ptr<SelectionItem>(new SelDatF("dr_higg_top",       "#DeltaR(H, t)",            50, 0, 5                    )),
    // shared_ptr<SelectionItem>(new SelDatF("tlep_pt",           "lept. top p_{T}",          50, 0, 1000                 )),
    // shared_ptr<SelectionItem>(new SelDatF("tlep_eta",          "lept. top #eta",           50, -5., 5.                 )),
    // shared_ptr<SelectionItem>(new SelDatF("tlep_mass",         "lept. top mass",           50, 0, 1000                 )),
    // shared_ptr<SelectionItem>(new SelDatF("h_pt",              "Higgs p_{T}",              50, 0, 1000                 )),
    // shared_ptr<SelectionItem>(new SelDatF("h_eta",             "Higgs #eta",               50, -5., 5.                 )),
    // shared_ptr<SelectionItem>(new SelDatF("h_mass",            "Higgs mass",               50, 0, 1000                 )),
    // shared_ptr<SelectionItem>(new SelDatF("vlq_pt",            "T p_{T}",                 50, 0, 1000                 )),
    // shared_ptr<SelectionItem>(new SelDatF("vlq_eta",           "T #eta",                  50, -5., 5.                 )),
    // shared_ptr<SelectionItem>(new SelDatF("vlq_mass",          "T mass",                  50, 0, 2000                 )),
};