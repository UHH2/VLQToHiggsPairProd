#pragma once

#include <vector>
#include "UHH2/VLQSemiLepPreSel/include/SelectionItem.h"


typedef SelectionItemData<int>      SelDatI;
typedef SelectionItemData<float>    SelDatF;
typedef SelectionItemData<double>   SelDatD;


static const vector<shared_ptr<SelectionItem>> SEL_ITEMS_VLQPair {
    shared_ptr<SelectionItem>(new SelDatI("trigger_accept",    "ele+Jets OR mu+Jets",      2, -.5, 1.5         ,1      )),
    shared_ptr<SelectionItem>(new SelDatI("n_leptons",         "N_{lepton}",               11, -.5, 10.5       ,1      )),
    shared_ptr<SelectionItem>(new SelDatD("ST",                "ST",                       100, 0, 5000        ,700    )),
    shared_ptr<SelectionItem>(new SelDatF("leading_jet_pt",    "leading jet p_{T}",        50, 100, 1500       ,200    )),
    // shared_ptr<SelectionItem>(new SelDatF("subleading_jet_pt", "sub-leading jet p_{T}",    50, 100, 1500       ,65     )),

    shared_ptr<SelectionItem>(new SelDatI("n_btags",           "N_{b-tag}",                11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatI("n_jets",            "N_{jet}",                  21, -.5, 20.5               )),
    shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_ca15", "N_{H jet}",                11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatI("n_higgs_tags_ca8",  "N_{H jet}",                11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatI("n_toptags",         "N_{H jet}",                11, -.5, 10.5               )),
    shared_ptr<SelectionItem>(new SelDatF("primary_lepton_pt", "primary lepton p_{T}",     50, 100, 1500               )),
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