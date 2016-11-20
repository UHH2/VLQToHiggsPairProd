#!/usr/bin/env python

import sys
import os
import time
import math

import varial.settings
import varial.rendering as rnd
import UHH2.VLQSemiLepPreSel.common as vlq_common

# import common_vlq
import tptp_settings
# import final_plotting
import common_plot_new as common_plot
import plot_new as plot
# import tptp_sframe 
# import compare_crs
import analysis
import treeproject_tptp
import plot_noreweighting as pn

from ROOT import TLatex, TH2

varial.settings.max_num_processes = 23

# hists_to_plot = [
#     'SingleTop',
#     'QCD',
#     'DYJets',
#     'WJets',
#     'Run2015CD',
#     # 'Diboson'
#     'TTbar_split'
# ]

# samples_to_plot = hists_to_plot + list(g + '_thth' for g in plot.less_signals)

base_path = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/UHH2/'\
    'VLQToHiggsPairProd/NewSamples-76X-v1/FinalSelection-v25'

# common_plot.pas_normfactors = {}

# common_plot.norm_reg_dict = {}


uncerts = analysis.all_uncerts + ['sfel_trg', 'jsf'] # or get_sys_dir()


baseline_selection = [
    'gendecay_accept          == 1',
    'n_ak8                    >= 2',
    'n_ak4                    >= 3',
    'ST                       > 800',
]

baseline_selection_btag = baseline_selection + [
    'n_additional_btags_medium  >= 1',
]

comb_lep_chan = [
    'trigger_accept_el45 + trigger_accept_mu45          >= 1'
]

# final regions

sr2b_channel = baseline_selection_btag + [
    'n_higgs_tags_2b_med_sm10    >= 1',
    # 'n_additional_btags_medium  >= 1',
]

sr1b_channel = baseline_selection_btag + [
    'n_higgs_tags_2b_med_sm10    == 0',
    'n_higgs_tags_1b_med_sm10    >= 1',
    # 'n_additional_btags_medium  >= 1',
]

sb_channel = baseline_selection_btag + [
    'n_higgs_tags_1b_med_sm10        == 0',
    'met                        >= 100',
    # 'n_additional_btags_medium  >= 1',
]

sb_ttbar_channel = baseline_selection + [
    'n_higgs_tags_1b_med_sm10        == 0',
    'n_additional_btags_medium  >= 2',
    'met                        >= 100',
]

sb_wjets_channel = baseline_selection + [
    'n_higgs_tags_1b_med_sm10        == 0',
    'n_additional_btags_medium  == 0',
    'met                        >= 100',
]


# lepton selections

el_channel = [
    'trigger_accept_el45   >= 1',
    'trigger_accept_mu45   == 0',
    'pt_ld_ak4_jet         > 250.',
    'pt_subld_ak4_jet      > 70.',
    'primary_lepton_pt     > 50.'
]

mu_channel = [
    'trigger_accept_mu45   >= 1',
    'primary_lepton_pt     > 47.'
]

ht_reweight_ttbar_no_top_pt_reweight = 'weight_htrew_tt*0.914621131' # last factor to correct discrepancy due to data but that you had previously
ht_reweight_wjets_no_top_pt_reweight = 'weight_htrew_wjets'
# ht_reweight_ttbar_w_top_pt_reweight = 'weight_htrew_tt_toppt'
# ht_reweight_wjets_w_top_pt_reweight = 'weight_htrew_wjets_toppt'
# top_pt_reweight = '(weight_ttbar/0.9910819)'
jetpt_reweight_ttbar_no_top_pt_reweight = 'weight_jetpt'
jetpt_reweight_wjets_no_top_pt_reweight = 'weight_jetpt'


final_regions_all = (
    ('BaseLineSelection_El45', baseline_selection+el_channel),
    ('BaseLineSelection_Mu45', baseline_selection+mu_channel),
    # ('SidebandTTJetsRegion_Comb', comb_lep_chan     + sb_ttbar_channel),
    # ('SidebandWPlusJetsRegion_Comb', comb_lep_chan  + sb_wjets_channel),
    ('SignalRegion2b_El45', sr2b_channel + el_channel),
    ('SignalRegion1b_El45', sr1b_channel + el_channel),
    ('SidebandRegion_El45', sb_channel + el_channel),
    ('SignalRegion2b_Mu45', sr2b_channel + mu_channel),
    ('SignalRegion1b_Mu45', sr1b_channel + mu_channel),
    ('SidebandRegion_Mu45', sb_channel + mu_channel),
    ('SidebandTTJetsRegion_El45', sb_ttbar_channel + el_channel),
    ('SidebandTTJetsRegion_Mu45', sb_ttbar_channel + mu_channel),
    ('SidebandWPlusJetsRegion_El45', sb_wjets_channel + el_channel),
    ('SidebandWPlusJetsRegion_Mu45', sb_wjets_channel + mu_channel),
)

# def add_all_with_weight_uncertainties(dict_weight_uncerts):
#     def add_uncerts(base_path, regions, weights, samples, params):
#         pdf_params = params if params == treeproject_tptp.st_only_params else treeproject_tptp.st_plus_jets_params
#         def tmp():
#             sys_tps = []
#             sys_tps += treeproject_tptp.add_higgs_smear_uncerts(base_path, regions, weights, samples, params)
#             sys_tps += treeproject_tptp.add_generic_uncerts(base_path, regions, weights, samples, params)
#             sys_tps += treeproject_tptp.add_scale_var_uncerts(base_path, regions, weights, samples, params)
#             for weight_name, weight_dict in dict_weight_uncerts.iteritems():
#                 sys_tps += treeproject_tptp.add_weight_uncerts(base_path, regions, weights, weight_name, weight_dict, samples, params)
#             if treeproject_tptp.ttbar_smpl in samples:
#                 sys_tps += treeproject_tptp.add_ttbar_scale_uncerts(base_path, base_path, regions, weights, samples, params)
#             sys_tps += treeproject_tptp.add_jec_uncerts(base_path, regions, weights, samples, params)
#             sys_tps += treeproject_tptp.add_pdf_uncerts(base_path, regions, weights, samples, pdf_params)
#             return sys_tps
#         return tmp
#     return add_uncerts

# def add_only_weight_uncertainties(dict_weight_uncerts):
#     def add_uncerts(base_path, regions, weights, samples, params):
#         def tmp():
#             sys_tps = []
#             for weight_name, weight_dict in dict_weight_uncerts.iteritems():
#                 sys_tps += treeproject_tptp.add_weight_uncerts(base_path, regions, weights, weight_name, weight_dict, samples, params)
#             return sys_tps
#         return tmp
#     return add_uncerts

def_weights = dict(treeproject_tptp.sample_weights_def)

def add_all_with_weight_uncertainties(dict_weight_uncerts):
    def add_uncerts(base_path, regions, weights, samples, params):
        pdf_params = params if params == treeproject_tptp.st_only_params else treeproject_tptp.st_plus_jets_params
        def tmp(**kws):
            treeproject = kws.pop('treeproject', TreeProjector)
            sys_tps = []
            sys_tps += treeproject_tptp.add_higgs_smear_uncerts(base_path, regions, weights, samples, params, treeproject=treeproject, **kws)
            sys_tps += treeproject_tptp.add_generic_uncerts(base_path, regions, weights, samples, params, treeproject=treeproject, **kws)
            sys_tps += treeproject_tptp.add_scale_var_uncerts(base_path, regions, weights, samples, params, treeproject=treeproject, **kws)
            for weight_name, weight_dict in dict_weight_uncerts.iteritems():
                sys_tps += treeproject_tptp.add_weight_uncerts(base_path, regions, weights, weight_name, weight_dict, samples, params, treeproject=treeproject, **kws)
            # if treeproject_tptp.ttbar_smpl in samples:
            #     sys_tps += treeproject_tptp.add_ttbar_scale_uncerts(base_path, base_path, regions, weights, samples, params, treeproject=treeproject, **kws)
            sys_tps += treeproject_tptp.add_jec_uncerts(base_path, regions, weights, samples, params, treeproject=treeproject, **kws)
            sys_tps += treeproject_tptp.add_pdf_uncerts(base_path, regions, weights, samples, pdf_params, treeproject=treeproject, **kws)
            return sys_tps
        return tmp
    return add_uncerts

def add_only_weight_uncertainties(dict_weight_uncerts):
    def add_uncerts(base_path, regions, weights, samples, params):
        def tmp(**kws):
            treeproject = kws.pop('treeproject', TreeProjector)
            sys_tps = []
            for weight_name, weight_dict in dict_weight_uncerts.iteritems():
                sys_tps += treeproject_tptp.add_weight_uncerts(base_path, regions, weights, weight_name, weight_dict, samples, params, treeproject=treeproject, **kws)
            return sys_tps
        return tmp
    return add_uncerts

def no_uncertainties(x, y):
    def tmp():
        return []
    return tmp


def run_treeproject_with_reweighting(final_dir, treeprojector, add_uncert_func=None, weight_dict=None):
    weights = dict(def_weights)
    if weight_dict:
        weights.update(weight_dict)
    # source_dir = os.path.join(base_path, final_dir)
    # uncerts = analysis.all_uncerts + ['sfel_trg'] # or get_sys_dir()
    nom_pattern = ['../TreeProject/TreeProjector*/{0}.root']
    sys_pattern = list('../TreeProject/SysTreeProjectors*/%s*/{0}.root'% i for i in uncerts)
    input_pattern = nom_pattern+sys_pattern

    signals_tt = treeproject_tptp.tptp_signal_samples
    signals_bb = treeproject_tptp.bpbp_signal_samples
    final_states_tt = treeproject_tptp.tptp_final_states
    final_states_bb = treeproject_tptp.bpbp_final_states

    plot_hists = ['ST', 'HT', 'n_ak4', 'nomass_boost_1b_mass_softdrop', 'nomass_boost_2b_mass_softdrop', 'noboost_mass_1b[0].m_pt', 'noboost_mass_2b[0].m_pt',
        'nobtag_boost_mass_nsjbtags', 'jets[].m_pt', 'pt_ld_ak4_jet', 'pt_subld_ak4_jet', 'jets[2].m_pt','jets[3].m_pt',
        'met', 'primary_lepton_pt']


    tp_chain = [
        treeproject_tptp.mk_tp(base_path+'/Files_and_Plots2', final_regions_all, weights, samples=treeproject_tptp.bkg_w_data, treeproject=treeprojector, 
            name='TreeProjectorBkg'),
        treeproject_tptp.mk_tp(base_path+'/Files_and_Plots2', final_regions_all, weights, samples=signals_tt, treeproject=treeprojector, 
            name='TreeProjectorTT'),
        treeproject_tptp.mk_tp(base_path+'/Files_and_Plots2', final_regions_all, weights, samples=signals_bb, treeproject=treeprojector, 
            name='TreeProjectorBB'),
    ]
    if add_uncert_func:
        tp_chain += [treeproject_tptp.mk_sys_tps(add_uncert_func(base_path+'/Files_and_Plots2', final_regions_all, weights,
            samples=treeproject_tptp.bkg_no_data, params=treeproject_tptp.sys_params),
            name='SysTreeProjectorsBkg', treeproject=treeprojector),
        ]
        tp_chain += list(treeproject_tptp.mk_sys_tps(add_uncert_func(base_path+'/Files_and_Plots2', final_regions_all, weights,
            samples=list(s + g for s in treeproject_tptp.tptp_signals), params=treeproject_tptp.st_only_params),
            name='SysTreeProjectorsTT'+g, treeproject=treeprojector) for g in final_states_tt)
        tp_chain += list(treeproject_tptp.mk_sys_tps(add_uncert_func(base_path+'/Files_and_Plots2', final_regions_all, weights,
            samples=list(s + g for s in treeproject_tptp.bpbp_signals), params=treeproject_tptp.st_only_params),
            name='SysTreeProjectorsBB'+g, treeproject=treeprojector) for g in final_states_bb)

    return varial.tools.ToolChain(final_dir, [
        # varial.tools.ToolChain('TreeProject',[
        varial.tools.ToolChainParallel('TreeProject', tp_chain, n_workers=2),
        #     treeproject_tptp.mk_sys_tps(add_uncert_func(base_path+'/Files_and_Plots2', final_regions_all, weights,
        #         samples=treeproject_tptp.tptp_signal_samples, params=treeproject_tptp.st_only_params),
        #         name='SysTreeProjectorsTT'),
            # ]),
            # ], n_workers=1),
        plot.mk_toolchain('Histograms', plot.less_samples_to_plot_only_th, 
            pattern=map(lambda w: w.format('*'), input_pattern),
            web_create=True,
            lookup_aliases=False
            # quiet_mode=True
            ),
        pn.mk_histoloader_merge(list('../'+ i for i in input_pattern), plot_hists),
        pn.mk_histograms_merge(uncerts, name='HistogramsMerged')
        ])

# sframe_tools = mk_sframe_and_plot_tools()

from varial_ext.treeprojector import TreeProjector 
import multiprocessing as mp

if __name__ == '__main__':
    time.sleep(1)
    # src_dir = sys.argv[1]
    final_dir = sys.argv[1]
    treeproject = TreeProjector
    if len(sys.argv) > 2:
        use_batch = sys.argv[2]
        if use_batch == "True":
            from varial_ext.treeprojector_spark import SparkTreeProjector 
            treeproject = SparkTreeProjector
            # job_proc = mp.Process(target=treeproject_tptp._start_job_submitter)
            # job_proc.start()

    all_tools = varial.tools.ToolChainParallel(final_dir,
        [
            run_treeproject_with_reweighting('HTReweighting', treeproject,
                add_uncert_func=add_all_with_weight_uncertainties({
                        'jsf' : {
                            treeproject_tptp.ttbar_smpl : ht_reweight_ttbar_no_top_pt_reweight,
                            'WJets' : ht_reweight_wjets_no_top_pt_reweight
                            }
                        }),
                weight_dict={
                    treeproject_tptp.ttbar_smpl : treeproject_tptp.base_weight+'*'+ht_reweight_ttbar_no_top_pt_reweight,
                    'WJets' : treeproject_tptp.base_weight+'*'+ht_reweight_wjets_no_top_pt_reweight,
                }),
            varial.tools.WebCreator(no_tool_check=True)
            # combination_limits.mk_limit_list('Limits')
        ], n_workers=1)
    varial.tools.Runner(all_tools, default_reuse=True)
    # varial.tools.CopyTool('~/www/vlq_analysis/tight_selection2/',
    #     src=final_dir, use_rsync=True).run()