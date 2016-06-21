#!/usr/bin/env python

import UHH2.VLQSemiLepPreSel.vlq_settings as vlq_settings
import UHH2.VLQSemiLepPreSel.common as vlq_common
from varial.extensions.hadd import Hadd
import varial.extensions.make
import varial.tools
import varial.generators as gen
import os
import glob
import sys
import pprint
import varial.analysis as analysis
from ROOT import TLatex
import cPickle

import common_plot
import plot as plot
from varial.extensions import git, limits


varial.settings.max_num_processes = 24
varial.settings.max_open_root_files = 5000

# if len(sys.argv) < 2:
#     print 'Provide output dir!'
#     exit(-1)

# dir_name = sys.argv[1]
uhh_base = os.getenv('CMSSW_BASE') + '/src/UHH2/'
# base_path = '/nfs/dust/cms/user/nowatsd/sFrameNew/'\
#     'RunII-25ns-v2/CMSSW_7_4_15_patch1/src/UHH2/VLQToHiggsPairProd/'\
#     'Samples-25ns-v2/TpTpFinalSelectionTreeOutput-v0wBTagSF/Files_and_Plots/'\
#     'Files_and_Plots_nominal/SFrame/nominal/workdir/uhh2.AnalysisModuleRunner.*.root'

# varial.settings.pretty_names.update({
#      'no sel._tex':                 r'no sel.',
#      'trigger_accept_tex':          r'trigger',
#      '2D cut_tex':                  r'2D-iso',
#      'primary_lepton_pt_tex':       r'lep. \pt',
#      'leading_jet_pt_tex':          r'ld. jet \pt',
#      'ST_tex':                      r'ST',
#      'event_chi2_tex':              r'$\chi^2$',
#      'dr_higg_top_tex':             r'$\Delta R(H, t)$',
#      'tlep_pt_tex':                 r't \pt',
#      'h_mass_tex':                  r'$M(H)$',
#      '1000 X output/input_tex':     r'$\epsilon$ * 1000'
# })


# these imports might need the settings above
# import sframe_tools
import treeproject_tptp
import sensitivity
import model_vlqpair
import common_sensitivity
import tex_content
from get_eff_count import CountTable, EffTable # EffNumTable, 

varial.settings.plot_obs = True
varial.settings.asymptotic = False
varial.settings.merge_decay_channels = True

all_regions = [
    'SignalRegion2b_Mu45',
    'SignalRegion1b_Mu45',
    'SidebandRegion_Mu45',
    'SignalRegion2b_El45',
    'SignalRegion1b_El45',
    'SidebandRegion_El45',
]
cr_only_regions = [
    # 'SidebandRegion_El45',
    # 'SidebandRegion_Mu45',
    'SidebandTTJetsRegion_El45',
    'SidebandTTJetsRegion_Mu45',
    'SidebandWPlusJetsRegion_El45',
    'SidebandWPlusJetsRegion_Mu45',
]

br_list_all = []

# only br_th = 100% for now
bw_max = 1
# bw_max = 0
for bw_br in [i/10. for i in xrange(0, int(bw_max*10)+2, 2)]:
    tz_max = 1.0-bw_br
    # tz_max = 0
    for tz_br in [ii/10. for ii in xrange(0, int(tz_max*10)+2, 2)]:
        th_br = 1-bw_br-tz_br
        # print bw_br, th_br, tz_br
        br_list_all.append({
            'bw' : bw_br,
            'th' : th_br,
            'tz' : tz_br
        })

br_list_th_only = [{
            'bw' : 0.,
            'th' : 1.,
            'tz' : 0.
        }]

def mk_limit_list_syst(base_path, name, sys_pat=None, list_region=all_regions, br_list=br_list_th_only, model_func=model_vlqpair.get_model):

    def tmp():
        limit_list = []
        for ind, brs_ in enumerate(br_list):
            # if ind > 5: break
            tc = []
            tc.append(varial.tools.ToolChainParallel(
                'ThetaLimits', list(varial.tools.ToolChain(
                    sig, sensitivity.mk_limit_tc_single(
                        brs_,
                        sig,
                        filter_keyfunc=sensitivity.select_single_sig(sig, list_region),
                        selection='ThetaLimits',
                        sys_pat=sys_pat,
                        pattern=[os.path.join(base_path, name)+'/TreeProject/TreeProjector/*.root'],
                        model_func=model_func
                        # select_no_sig(),
                    ))
                for sig in sensitivity.signals_to_use)
            ))
            tc.append(varial.tools.ToolChain('LimitsWithGraphs',[
                limits.LimitGraphs(
                    limit_path='../../ThetaLimits/*/ThetaLimit',
                    plot_obs=varial.settings.plot_obs,
                    plot_1sigmabands=True,
                    plot_2sigmabands=True,
                    axis_labels=("m_{T} [GeV]", "#sigma x BR [pb]"),
                    ),
                varial.plotter.Plotter(
                    name='LimitCurvesCompared',
                    input_result_path='../LimitGraphs',
                    # filter_keyfunc=lambda w: 'Uncleaned' in w.legend,
                    # plot_setup=plot_setup,
                    hook_loaded_histos=sensitivity.limit_curve_loader_hook(brs_),
                    plot_grouper=lambda ws: varial.gen.group(
                            ws, key_func=lambda w: w.save_name),
                    # save_name_func=varial.plotter.save_by_name_with_hash
                    save_name_func=lambda w: w.save_name,
                    plot_setup=lambda w: sensitivity.plot_setup_graphs(w,
                        th_x=common_sensitivity.theory_masses,
                        th_y=common_sensitivity.theory_cs),
                    keep_content_as_result=True,
                    canvas_decorators=[varial.rendering.Legend(x_pos=.75, y_pos=0.7, label_width=0.2, label_height=0.05),
                            varial.rendering.TextBox(textbox=TLatex(0.16, 0.89, "#scale[0.7]{#bf{CMS}} #scale[0.6]{#it{Preliminary}}")),
                            varial.rendering.TextBox(textbox=TLatex(0.67, 0.89, "#scale[0.5]{2.7 fb^{-1} (13 TeV)}")),
                        # varial.rendering.TitleBox(text='#scale[1.2]{#bf{#it{Work in Progress}}}')
                        ],
                    # save_lin_log_scale=True
                    ),
                ]))
            tc.append(varial.tools.ToolChain('LimitsWithGraphsNoObs',[
                limits.LimitGraphs(
                    limit_path='../../ThetaLimits/*/ThetaLimit',
                    plot_obs=False,
                    plot_1sigmabands=True,
                    plot_2sigmabands=True,
                    axis_labels=("m_{T'} [GeV]", "#sigma x BR [pb]"),
                    ),
                varial.plotter.Plotter(
                    name='LimitCurvesCompared',
                    input_result_path='../LimitGraphs',
                    # filter_keyfunc=lambda w: 'Uncleaned' in w.legend,
                    # plot_setup=plot_setup,
                    hook_loaded_histos=sensitivity.limit_curve_loader_hook(brs_),
                    plot_grouper=lambda ws: varial.gen.group(
                            ws, key_func=lambda w: w.save_name),
                    # save_name_func=varial.plotter.save_by_name_with_hash
                    save_name_func=lambda w: w.save_name,
                    plot_setup=lambda w: sensitivity.plot_setup_graphs(w,
                        th_x=common_sensitivity.theory_masses,
                        th_y=common_sensitivity.theory_cs),
                    keep_content_as_result=True,
                    canvas_decorators=[varial.rendering.Legend(x_pos=.75, y_pos=0.7, label_width=0.2, label_height=0.05),
                            varial.rendering.TextBox(textbox=TLatex(0.16, 0.89, "#scale[0.7]{#bf{CMS}} #scale[0.6]{#it{Simulation}}")),
                            varial.rendering.TextBox(textbox=TLatex(0.67, 0.89, "#scale[0.5]{2.7 fb^{-1} (13 TeV)}")),
                        # varial.rendering.TitleBox(text='#scale[1.2]{#bf{#it{Work in Progress}}}')
                        ],
                    # save_lin_log_scale=True
                    ),
                ]))
            limit_list.append(
                varial.tools.ToolChain('Limit'+str(ind), tc))
        return limit_list
    return tmp

# def mk_tex_tc_post(base):
#     def tmp():
#         return varial.tools.ToolChain('TexCopy', [
#             varial.tools.ToolChain(
#                 'Tex', 
#                 [
#                     tex_content.mk_autoContentSignalControlRegion(base),
#                     tex_content.mk_autoContentLimits(base)
#                 ]
#             ),
#             varial.tools.CopyTool('dnowatsc@lxplus.cern.ch:AN-Dir/notes/AN-15-327/trunk/', src='../Tex/*', ignore=(), use_rsync=True)
#         ])
#     return tmp


#!/usr/bin/env python

baseline_selection = [
    'gendecay_accept          == 1',
    'n_ak8                    >= 2',
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
    'n_additional_btags_medium  >= 1',
]

sr1b_channel = baseline_selection_btag + [
    'n_higgs_tags_2b_med_sm10    == 0',
    'n_higgs_tags_1b_med_sm10    >= 1',
    'n_additional_btags_medium  >= 1',
]

sb_channel = baseline_selection_btag + [
    'n_higgs_tags_1b_med_sm10        == 0',
    'met                        >= 100',
    'n_additional_btags_medium  >= 1',
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

final_regions_syst = (
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
    # ('SidebandTTJetsRegion_El45', sb_ttbar_channel + el_channel),
    # ('SidebandTTJetsRegion_Mu45', sb_ttbar_channel + mu_channel),
    # ('SidebandWPlusJetsRegion_El45', sb_wjets_channel + el_channel),
    # ('SidebandWPlusJetsRegion_Mu45', sb_wjets_channel + mu_channel),
)

final_regions_test = (
    ('BaseLineSelection_El45', baseline_selection+el_channel),
    ('BaseLineSelection_Mu45', baseline_selection+mu_channel),
    # ('SidebandTTJetsRegion_Comb', comb_lep_chan     + sb_ttbar_channel),
    # ('SidebandWPlusJetsRegion_Comb', comb_lep_chan  + sb_wjets_channel),
    # ('SignalRegion2b_El45', sr2b_channel + el_channel),
    # ('SignalRegion1b_El45', sr1b_channel + el_channel),
    # ('SidebandRegion_El45', sb_channel + el_channel),
    # ('SignalRegion2b_Mu45', sr2b_channel + mu_channel),
    # ('SignalRegion1b_Mu45', sr1b_channel + mu_channel),
    # ('SidebandRegion_Mu45', sb_channel + mu_channel),
    # ('SidebandTTJetsRegion_El45', sb_ttbar_channel + el_channel),
    # ('SidebandTTJetsRegion_Mu45', sb_ttbar_channel + mu_channel),
    # ('SidebandWPlusJetsRegion_El45', sb_wjets_channel + el_channel),
    # ('SidebandWPlusJetsRegion_Mu45', sb_wjets_channel + mu_channel),
)


all_uncerts = [
    'jec',
    'jer',
    'btag_bc',
    'btag_udsg',
    'sfmu_id',
    'sfmu_trg',
    'sfel_id',
    'sfel_trg',
    'pu',
    'PDF',
    'ScaleVar',
    # 'rate',
    'PSScale'
    # 'top_pt_weight',
    # 'ht_reweight'
]

plot_uncerts = {
    'Exp' : ['jec', 'jer', 'btag_bc', 'btag_udsg', 'pu', 'sfmu_id', 'sfmu_trg', 'sfel_id', 'sfel_trg'], # , 'sfmu_id', 'sfmu_trg', 'sfel_id', 'sfel_trg'
    'ScaleVar' : ['ScaleVar'],
    'PDF' : ['PDF'],
    'TTbarScale' : ['ttbar_scale'],
    'Theo' : ['ScaleVar', 'PDF', 'PSScale'],
    'TopPt' : ['top_pt_reweight'],
    'HT' : ['ht_reweight'],
}

# theory_uncerts = [
#     'PDF',
#     'ScaleVar',
#     'top_pt_weight',
#     'ht_reweight'
# ]


lumi_times_pure_BR = 2630.*0.111
lumi_times_mixed_BR = 2630.*0.222
lumi = 2630.
lumi_ele = 2540.

def get_dict(hist_path, var):
    def tmp(base_path):
        path = hist_path
        if not os.path.exists(path):
            path = os.path.join(base_path, path)
        with open(os.path.join(path, '_varial_infodata.pkl')) as f:
            res = cPickle.load(f)
        return res[var]
    return tmp

table_block_signal = [
    (r'T#bar{T} (0.7 TeV) $\rightarrow$ tHtH', lambda w: 'Integral___TpTp_M-0700_thth' in w, True),
    (r'T#bar{T} (0.9 TeV) $\rightarrow$ tHtH', lambda w: 'Integral___TpTp_M-0900_thth' in w, True),
    (r'T#bar{T} (1.1 TeV) $\rightarrow$ tHtH', lambda w: 'Integral___TpTp_M-1100_thth' in w, True),
    (r'T#bar{T} (1.3 TeV) $\rightarrow$ tHtH', lambda w: 'Integral___TpTp_M-1300_thth' in w, True),
    (r'T#bar{T} (1.5 TeV) $\rightarrow$ tHtH', lambda w: 'Integral___TpTp_M-1500_thth' in w, True),
    (r'T#bar{T} (1.7 TeV) $\rightarrow$ tHtH', lambda w: 'Integral___TpTp_M-1700_thth' in w, True),
]

table_block_signal_fs_700 = [
    (r'T#bar{T} (0.7 TeV) $\rightarrow$ tHtH', lambda w: 'Integral___TpTp_M-0700_thth' in w, True),
    (r'T#bar{T} (0.7 TeV) $\rightarrow$ tHtZ', lambda w: 'Integral___TpTp_M-0700_thtz' in w, True),
    (r'T#bar{T} (0.7 TeV) $\rightarrow$ tHbW', lambda w: 'Integral___TpTp_M-0700_thbw' in w, True),
    (r'T#bar{T} (0.7 TeV) $\rightarrow$ tZtZ', lambda w: 'Integral___TpTp_M-0700_noH_tztz' in w, True),
    (r'T#bar{T} (0.7 TeV) $\rightarrow$ tZbW', lambda w: 'Integral___TpTp_M-0700_noH_tzbw' in w, True),
    (r'T#bar{T} (0.7 TeV) $\rightarrow$ bWbW', lambda w: 'Integral___TpTp_M-0700_noH_bwbw' in w, True),
]

table_block_signal_fs_1700 = [
    (r'T#bar{T} (1.7 TeV) $\rightarrow$ tHtH', lambda w: 'Integral___TpTp_M-1700_thth' in w, True),
    (r'T#bar{T} (1.7 TeV) $\rightarrow$ tHtZ', lambda w: 'Integral___TpTp_M-1700_thtz' in w, True),
    (r'T#bar{T} (1.7 TeV) $\rightarrow$ tHbW', lambda w: 'Integral___TpTp_M-1700_thbw' in w, True),
    (r'T#bar{T} (1.7 TeV) $\rightarrow$ tZtZ', lambda w: 'Integral___TpTp_M-1700_noH_tztz' in w, True),
    (r'T#bar{T} (1.7 TeV) $\rightarrow$ tZbW', lambda w: 'Integral___TpTp_M-1700_noH_tzbw' in w, True),
    (r'T#bar{T} (1.7 TeV) $\rightarrow$ bWbW', lambda w: 'Integral___TpTp_M-1700_noH_bwbw' in w, True),
]

table_block_background = [
    (r'$\mathrm{t\bar{t}}$', lambda w: 'Integral___t#bar{t}' in w),
    ('W + Jets', lambda w: 'Integral___W + jets' in w),
    ('Z + Jets', lambda w: 'Integral___DY + jets' in w),
    ('QCD', lambda w: 'Integral___QCD' in w),
    ('Single t', lambda w: 'Integral___Single t' in w),
]

norm_factors = [
    ('T#bar{T} (0.7 TeV)', (1./common_plot.normfactors['TpTp_M-0700'])*lumi),
    ('T#bar{T} (0.9 TeV)', (1./common_plot.normfactors['TpTp_M-0900'])*lumi),
    ('T#bar{T} (1.1 TeV)', (1./common_plot.normfactors['TpTp_M-1100'])*lumi),
    ('T#bar{T} (1.3 TeV)', (1./common_plot.normfactors['TpTp_M-1300'])*lumi),
    ('T#bar{T} (1.5 TeV)', (1./common_plot.normfactors['TpTp_M-1500'])*lumi),
    ('T#bar{T} (1.7 TeV)', (1./common_plot.normfactors['TpTp_M-1700'])*lumi),
]

def get_table_category_block():
    return [
        ('0H category', get_dict('../HistogramsMerged/StackedAll/SidebandRegion', 'ST')),
        ('H1B category', get_dict('../HistogramsMerged/StackedAll/SignalRegion1b', 'ST')),
        ('H2B category', get_dict('../HistogramsMerged/StackedAll/SignalRegion2b', 'ST')),
    ] if varial.settings.style == 'PAS' else [
        ('Preselection', get_dict('../HistogramsMerged/StackedAll/BaseLineSelection', 'ST')),
        ('0H category', get_dict('../HistogramsMerged/StackedAll/SidebandRegion', 'ST')),
        ('H1B category', get_dict('../HistogramsMerged/StackedAll/SignalRegion1b' , 'ST')),
        ('H2B category', get_dict('../HistogramsMerged/StackedAll/SignalRegion2b', 'ST')),
    ]

def get_table_category_block_split(chan):
    return [
        ('Preselection', get_dict('../Histograms/StackedAll/BaseLineSelection_%s' % chan, 'ST')),
        ('0H category', get_dict('../Histograms/StackedAll/SidebandRegion_%s' % chan, 'ST')),
        ('H1B category', get_dict('../Histograms/StackedAll/SignalRegion1b_%s' % chan , 'ST')),
        ('H2B category', get_dict('../Histograms/StackedAll/SignalRegion2b_%s' % chan, 'ST')),
    ]

# table_category_block_comp_fs = [
#     ('0H category', get_dict('../HistogramsMerged/StackedAll/SidebandRegion', 'ST')),
#     ('H1B category', get_dict('../HistogramsMerged/StackedAll/SignalRegion1b', 'ST')),
#     ('H2B category', get_dict('../HistogramsMerged/StackedAll/SignalRegion2b', 'ST')),
# ] if varial.settings.style == 'PAS' else [
#     ('Preselection', get_dict('../HistogramsMerged/StackedAll/BaseLineSelection', 'ST')),
#     ('0H category', get_dict('../HistogramsMerged/StackedAll/SidebandRegion', 'ST')),
#     ('H1B category', get_dict('../HistogramsMerged/StackedAll/SignalRegion1b' , 'ST')),
#     ('H2B category', get_dict('../HistogramsMerged/StackedAll/SignalRegion2b', 'ST')),
# ]

# NO TOP PT REWEIGHTING
# values from FinalSelection-v21/Run5_withHiggsTagVar/ReweightCalc/
# values from combination of lepton channels in SidebandTTJetsRegion
p0_ttbar_from0_no_top_pt_reweight = 1.241155
p1_ttbar_from0_no_top_pt_reweight = -0.000363264
# values from combination of lepton channels in SidebandWPlusJetsRegion
p0_wjets_from0_no_top_pt_reweight = 1.127182
p1_wjets_from0_no_top_pt_reweight = -0.000243715

# WITH TOP PT REWEIGHTING
# values from combination of lepton channels in SidebandTTJetsRegion
p0_ttbar_from0_w_top_pt_reweight = 1.424121
p1_ttbar_from0_w_top_pt_reweight = -0.000352462
# values from combination of lepton channels in SidebandWPlusJetsRegion
p0_wjets_from0_w_top_pt_reweight = 1.201648
p1_wjets_from0_w_top_pt_reweight = -0.000250984

# ht_reweight_ttbar_no_top_pt_reweight = '({0}+{1}*HT)'.format(p0_ttbar_from0_no_top_pt_reweight, p1_ttbar_from0_no_top_pt_reweight)
# ht_reweight_wjets_no_top_pt_reweight = '({0}+{1}*HT)'.format(p0_wjets_from0_no_top_pt_reweight, p1_wjets_from0_no_top_pt_reweight)
# ht_reweight_ttbar_w_top_pt_reweight = '({0}+{1}*HT)'.format(p0_ttbar_from0_w_top_pt_reweight, p1_ttbar_from0_w_top_pt_reweight)
# ht_reweight_wjets_w_top_pt_reweight = '({0}+{1}*HT)'.format(p0_wjets_from0_w_top_pt_reweight, p1_wjets_from0_w_top_pt_reweight)
ht_reweight_ttbar_no_top_pt_reweight = 'weight_htrew_tt'
ht_reweight_wjets_no_top_pt_reweight = 'weight_htrew_wjets'
ht_reweight_ttbar_w_top_pt_reweight = 'weight_htrew_tt_toppt'
ht_reweight_wjets_w_top_pt_reweight = 'weight_htrew_wjets_toppt'

# gen_ht_reweight = '({0}+{1}*gen_ht)'.format(p0_from0_no_top_pt_reweight_0, p1_from0_no_top_pt_reweight_0)
# parton_ht_reweight = '({0}+{1}*parton_ht)'.format(p0_from0_no_top_pt_reweight_0, p1_from0_no_top_pt_reweight_0)
top_pt_reweight = '(weight_ttbar/0.9910819)'

path_ttbar_scale_files = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/UHH2/VLQToHiggsPairProd/NewSamples-76X-v1/FinalSelection_onlyTTbarScaleVar/Files_and_Plots/'

def add_all_with_weight_uncertainties(dict_weight_uncerts):
    def add_uncerts(base_path, regions, weights, samples, params):
        pdf_params = params if params == treeproject_tptp.st_only_params else treeproject_tptp.st_plus_jets_params
        def tmp():
            sys_tps = []
            sys_tps += treeproject_tptp.add_higgs_smear_uncerts(base_path, regions, weights, samples, params)
            sys_tps += treeproject_tptp.add_generic_uncerts(base_path, regions, weights, samples, params)
            sys_tps += treeproject_tptp.add_scale_var_uncerts(base_path, regions, weights, samples, params)
            for weight_name, weight_dict in dict_weight_uncerts.iteritems():
                sys_tps += treeproject_tptp.add_weight_uncerts(base_path, regions, weights, weight_name, weight_dict, samples, params)
            if treeproject_tptp.ttbar_smpl in samples:
                sys_tps += treeproject_tptp.add_ttbar_scale_uncerts(base_path, base_path, regions, weights, samples, params)
            sys_tps += treeproject_tptp.add_jec_uncerts(base_path, regions, weights, samples, params)
            sys_tps += treeproject_tptp.add_pdf_uncerts(base_path, regions, weights, samples, pdf_params)
            return sys_tps
        return tmp
    return add_uncerts

# def add_only_weight_uncertainties(dict_weight_uncerts):
#     def add_uncerts(base_path, regions, weights, samples, params):
#         def tmp():
#             sys_tps = []
#             for weight_name, weight_dict in dict_weight_uncerts.iteritems():
#                 sys_tps += treeproject_tptp.add_weight_uncerts(base_path, regions, weights, weight_name, weight_dict, samples, params)
#             return sys_tps
#         return tmp
#     return add_uncerts

def add_all_without_weight_uncertainties(base_path, regions, weights, samples, params):
    pdf_params = params if params == treeproject_tptp.st_only_params else treeproject_tptp.st_plus_jets_params
    def tmp():
        sys_tps = []
        sys_tps += treeproject_tptp.add_higgs_smear_uncerts(base_path, regions, weights, samples, params)
        sys_tps += treeproject_tptp.add_jec_uncerts(base_path, regions, weights, samples, params)
        sys_tps += treeproject_tptp.add_generic_uncerts(base_path, regions, weights, samples, params)
        sys_tps += treeproject_tptp.add_scale_var_uncerts(base_path, regions, weights, samples, params)
        if treeproject_tptp.ttbar_smpl in samples:
            sys_tps += treeproject_tptp.add_ttbar_scale_uncerts(base_path, base_path, regions, weights, samples, params)
        sys_tps += treeproject_tptp.add_pdf_uncerts(base_path, regions, weights, samples, pdf_params)
        return sys_tps
    return tmp

def no_uncertainties(x, y):
    def tmp():
        return []
    return tmp


# varial.settings.lookup_aliases = False

def make_tp_plot_chain(name, base_path, output_dir, add_uncert_func,
    mod_sample_weights=None, uncertainties=None, br_list=br_list_th_only):

    if mod_sample_weights:
        weights = dict(treeproject_tptp.sample_weights_def)
        weights.update(mod_sample_weights)
    else:
        weights = treeproject_tptp.sample_weights_def


    tc_tp = [
            treeproject_tptp.mk_tp(base_path, final_regions_all, weights, samples=treeproject_tptp.samples_w_data),
            treeproject_tptp.mk_sys_tps(add_uncert_func(base_path, final_regions_all, weights,
                samples=treeproject_tptp.samples_no_data, params=treeproject_tptp.sys_params),
                name='SysTreeProjectors'),
            # treeproject_tptp.mk_sys_tps(add_uncert_func(base_path, final_regions_syst, weights,
            #     samples=treeproject_tptp.background_samples, params=treeproject_tptp.sys_params),
            #     name='SysTreeProjectorsBkg'),
            # treeproject_tptp.mk_sys_tps(add_uncert_func(base_path, final_regions_all, weights,
            #     samples=treeproject_tptp.signal_samples_important, params=treeproject_tptp.st_only_params),
            #     name='SysTreeProjectorsSigImportant'),
            # treeproject_tptp.mk_sys_tps(add_uncert_func(base_path, final_regions_all, weights,
            # # treeproject_tptp.mk_sys_tps(add_uncert_func(base_path, final_regions_syst, weights,
            #     samples=treeproject_tptp.signal_samples_rest, params=treeproject_tptp.st_only_params),
            #     name='SysTreeProjectorsSigRest'),
            # # # treeproject_tptp.mk_sys_tps(add_uncert_func(base_path, final_regions_all, weights,
            # # #     samples=treeproject_tptp.signal_samples, params=treeproject_tptp.st_only_params),
            # # #     name='SysTreeProjectorsSig'),
            # # treeproject_tptp.mk_sys_tps(add_uncert_func(base_path, final_regions_all, weights,
            # #     samples=treeproject_tptp.samples_no_data, params=treeproject_tptp.sys_params),
            # #     name='SysTreeProjectors'),
    ]

    sys_path = output_dir+'/%s/TreeProject/SysTreeProjectors*' % name
    
    def get_sys_dir():
        return set(sys.split('__')[0] for d in glob.glob(sys_path) for sys in os.listdir(d) if 'Norm' not in sys)

    def mk_tc_sens():
        uncerts = uncertainties or get_sys_dir()
        lim_list = [
            sensitivity.mk_tc('LimitsAllUncertsAllRegionsNoNorm', mk_limit_list_syst(
                output_dir,
                name,
                list(sys_path+'/%s*/*.root'% i for i in uncerts if all(g not in i for g in ['Norm'])),
                all_regions,
                br_list=br_list,
                model_func=model_vlqpair.get_model_no_norm,
                )),

            sensitivity.mk_tc('LimitsAllUncertsAllRegionsWithNorm', mk_limit_list_syst(
                output_dir,
                name,
                list(sys_path+'/%s*/*.root'% i for i in uncerts if all(g not in i for g in ['Norm', 'ScaleVar'])),
                all_regions,
                br_list=br_list,
                model_func=model_vlqpair.get_model_with_norm,
                )),
        ]
        lim_list += [
            varial.tools.ToolChain(
                'BackgroundOnlyFitBoth', 
                sensitivity.mk_limit_tc_single(
                    br_list_th_only[0],
                    filter_keyfunc=sensitivity.select_no_sig(cr_only_regions),
                    selection='ThetaLimits',
                    sys_pat=list(sys_path+'/%s*/*.root'% i for i in uncerts if all(g not in i for g in ['Norm'])),
                    pattern=[os.path.join(output_dir, name)+'/TreeProject/TreeProjector/*.root'],
                    model_func=model_vlqpair.get_model_with_norm,
                    hook_loaded_histos=sensitivity.loader_hook(br_list_th_only[0], 15)
                )),
            varial.tools.ToolChain(
                'BackgroundOnlyFitNoScaleVar', 
                sensitivity.mk_limit_tc_single(
                    br_list_th_only[0],
                    filter_keyfunc=sensitivity.select_no_sig(cr_only_regions),
                    selection='ThetaLimits',
                    sys_pat=list(sys_path+'/%s*/*.root'% i for i in uncerts if all(g not in i for g in ['Norm', 'ScaleVar'])),
                    pattern=[os.path.join(output_dir, name)+'/TreeProject/TreeProjector/*.root'],
                    model_func=model_vlqpair.get_model_with_norm,
                    hook_loaded_histos=sensitivity.loader_hook(br_list_th_only[0], 15)
                )),
            varial.tools.ToolChain(
                'BackgroundOnlyFitWithScaleVar', 
                sensitivity.mk_limit_tc_single(
                    br_list_th_only[0],
                    filter_keyfunc=sensitivity.select_no_sig(cr_only_regions),
                    selection='ThetaLimits',
                    sys_pat=list(sys_path+'/%s*/*.root'% i for i in uncerts if all(g not in i for g in ['Norm'])),
                    pattern=[os.path.join(output_dir, name)+'/TreeProject/TreeProjector/*.root'],
                    model_func=model_vlqpair.get_model_no_norm,
                    hook_loaded_histos=sensitivity.loader_hook(br_list_th_only[0], 15)
                )),
            ]
        if name == 'HTReweighting':
            lim_list += [
                # sensitivity.mk_tc('LimitsAllUncertsOnlyEl', mk_limit_list_syst(
                #     output_dir,
                #     name,
                #     list(sys_path+'/%s*/*.root'% i for i in uncerts if all(g not in i for g in ['Norm'])),
                #     ['SignalRegion2b_El45', 'SignalRegion1b_El45', 'SidebandRegion_El45'],
                #     br_list=br_list_th_only,
                #     ), mk_triangle=False),
                # sensitivity.mk_tc('LimitsAllUncertsOnlyMu', mk_limit_list_syst(
                #     output_dir,
                #     name,
                #     list(sys_path+'/%s*/*.root'% i for i in uncerts if all(g not in i for g in ['Norm'])),
                #     ['SignalRegion2b_Mu45', 'SignalRegion1b_Mu45', 'SidebandRegion_Mu45'],
                #     br_list=br_list_th_only,
                #     ), mk_triangle=False),
                ]
        return lim_list

    # def mk_tc_plot(style='AN'):
    varial.settings.style = 'PAS'
    def mk_tc_plot():
        # def tmp():
        uncerts = uncertainties or get_sys_dir()
        # varial.settings.style = style
        return [

                    ######## HISTOGRAMS WITH LEPTON CHANNELS SEPARATE ########

                    plot.mk_toolchain('Histograms', plot.less_samples_to_plot_only_th, 
                                pattern=[output_dir+'/%s/TreeProject/TreeProjector/*.root'%name]
                                + list(sys_path+'/%s*/*.root'% i for i in uncerts)
                                ),                                             
                    plot.mk_toolchain('HistogramsCompUncerts', plot.less_samples_to_plot_only_th,
                                pattern=[output_dir+'/%s/TreeProject/TreeProjector/*.root'%name]
                                + list(sys_path+'/%s*/*.root'% i for i in uncerts),
                                filter_keyfunc=lambda w: any(f in w.file_path for f in [treeproject_tptp.ttbar_smpl, 'WJets', 'TpTp_M-0800']) and any(w.in_file_path.endswith(g) for g in ['ST', 'HT']),   
                                plotter_factory=plot.plotter_factory_uncerts()),                                             
                    # plot.mk_toolchain('HistogramsNormToInt', plot.less_samples_to_plot_only_th, 
                    #             pattern=[output_dir+'/%s/TreeProject/TreeProjector/*.root'%name]
                    #             + list(sys_path+'/%s*/*.root'% i for i in uncerts),
                    #             filter_keyfunc=lambda w: 'TpTp' not in w.file_path,
                    #             plotter_factory=plot.plotter_factory_stack(hook_loaded_histos=plot.loader_hook_norm_to_int,
                    #                 plot_setup=plot.stack_setup_norm_all_to_intgr)),
                    # plot.mk_toolchain('HistogramsNoData', plot.less_samples_to_plot_only_th, 
                    #             pattern=[output_dir+'/%s/TreeProject/TreeProjector/*.root'%name]
                    #             + list(sys_path+'/%s*/*.root'% i for i in uncerts),
                    #             filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in plot.less_samples_to_plot_only_th if 'Run2015CD' not in f)),
                    # plot.mk_toolchain('HistogramsCompFinalStates', plot.less_samples_to_plot_only_th,
                    #             pattern=[output_dir+'/%s/TreeProject/TreeProjector/*.root'%name]
                    #             + list(sys_path+'/%s*/*.root'% i for i in uncerts),
                    #             filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in plot.less_samples_to_plot_only_th if not any(g in w.file_path.split('/')[-1] for g in ['TpTp_M-0800', 'TpTp_M-1600'])),
                    #             plotter_factory=plot.plotter_factory_stack(hook_loaded_histos=plot.loader_hook_compare_finalstates),
                    #             ),
                    # # # plot.mk_toolchain_pull('HistogramsPull', [output_dir+'/%s/TreeProject/TreeProjector/*.root'%name]
                    # # #             + list(sys_path+'/%s*/*.root'% i for i in uncerts)
                    # # #             ,plot.less_samples_to_plot_only_th),               
                    # # # plot.mk_toolchain('HistogramsNoUncerts', plot.less_samples_to_plot_only_th, 
                    # # #             pattern=[output_dir+'/%s/TreeProject/TreeProjector/*.root'%name],
                    # # #             filter_keyfunc=lambda w: 'TpTp' not in w.file_path
                    # # #             # + list(sys_path+'/%s*/*.root'% i for i in uncerts)
                    # # #             ),

                    ####### MERGE LEPTON CHANNELS ########

                    # varial.tools.ToolChain('MergeChannelsMoreHists', [
                    #     varial.tools.HistoLoader(
                    #         pattern=[output_dir+'/%s/TreeProject/TreeProjector/*.root'%name]+list(sys_path+'/%s*/*.root'% i for i in uncerts),
                    #         filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in plot.less_samples_to_plot_only_th) and\
                    #             'Region_Comb' not in w.in_file_path and\
                    #             any(w.in_file_path.endswith(f) for f in ['ST', 'HT', 'n_ak4', 'pt_ld_ak8_jet', 'pt_subld_ak8_jet',
                    #                 'n_ak8', 'met', 'pt_ld_ak4_jet', 'pt_subld_ak4_jet', 'pt_third_ak4_jet','pt_fourth_ak4_jet', 'n_ak8_higgs_cand', 'n_additional_btags_medium',
                    #                 'n_higgs_tags_1b_med', 'n_higgs_tags_2b_med', 'primary_electron_pt', 'primary_muon_pt', 'primary_lepton_pt',
                    #                 'nobtag_boost_mass_nsjbtags', 'nomass_boost_1b_mass', 'nomass_boost_2b_mass', 'noboost_mass_1b_pt', 'noboost_mass_2b_pt']),
                    #         hook_loaded_histos=plot.loader_hook_merge_regions,
                    #     ),
                    #     plot.mk_toolchain('HistogramsMerged',
                    #         plotter_factory=plot.plotter_factory_stack(hook_loaded_histos=plot.loader_hook_merge_lep_channels),
                    #         pattern=None, input_result_path='../HistoLoader'),
                    #     # plot.mk_toolchain('HistogramsMergedNoUncerts', filter_keyfunc=lambda w: not w.is_signal and not w.sys_info,
                    #     #     plotter_factory=plot.plotter_factory_stack(
                    #     #         hook_loaded_histos=plot.loader_hook_merge_lep_channels,
                    #     #         hook_canvas_post_build=lambda w: common_plot.mod_no_2D_leg(plot.canvas_setup_post(w))
                    #     #         ),
                    #     #     pattern=None, input_result_path='../HistoLoader'),
                    #     plot.mk_toolchain('HistogramsMergedNoData', filter_keyfunc=lambda w: not w.is_data,
                    #         plotter_factory=plot.plotter_factory_stack(hook_loaded_histos=plot.loader_hook_merge_lep_channels),
                    #         pattern=None, input_result_path='../HistoLoader'),                                             
                    #     plot.mk_toolchain('HistogramsNormToInt',
                    #                 filter_keyfunc=lambda w: 'TpTp' not in w.file_path,
                    #                 pattern=None, input_result_path='../HistoLoader',
                    #                 plotter_factory=plot.plotter_factory_stack(hook_loaded_histos=plot.loader_hook_norm_to_int,
                    #                     plot_setup=plot.stack_setup_norm_all_to_intgr)),
                    #     ]),
                    



                    # ####### MERGE LEPTON CHANNELS, COMBINE FINAL STATES ########
                    
                    # varial.tools.ToolChain('MergeChannelsMoreHistsCombFinalStates', [
                    #     varial.tools.HistoLoader(
                    #         pattern=[output_dir+'/%s/TreeProject/TreeProjector/*.root'%name]+list(sys_path+'/%s*/*.root'% i for i in uncerts),
                    #         filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in plot.less_samples) and\
                    #             'Region_Comb' not in w.in_file_path and\
                    #             any(w.in_file_path.endswith(f) for f in ['nobtag_boost_mass_nsjbtags', 'nomass_boost_1b_mass', 'nomass_boost_2b_mass', 'noboost_mass_1b_pt', 'noboost_mass_2b_pt']),
                    #         hook_loaded_histos=plot.loader_hook_merge_regions,
                    #     ),
                    #     plot.mk_toolchain('HistogramsMerged', pattern=None, input_result_path='../HistoLoader',
                    #         filter_keyfunc=lambda w: all(g not in w.sample for g in ['TpTp_M-0800', 'TpTp_M-1600']),
                    #         plotter_factory=plot.plotter_factory_stack(
                    #             hook_loaded_histos=plot.loader_hook_compare_finalstates,
                    #             # hook_canvas_post_build=lambda w: plot.canvas_setup_post(common_plot.mod_shift_leg(w))
                    #             )
                    #         ),
                    #     plot.mk_toolchain('HistogramsNoData', pattern=None, input_result_path='../HistoLoader',
                    #         filter_keyfunc=lambda w: 'Run2015CD' not in w.file_path.split('/')[-1] and all(g not in w.sample for g in ['TpTp_M-0800', 'TpTp_M-1600']),
                    #         plotter_factory=plot.plotter_factory_stack(
                    #             hook_loaded_histos=plot.loader_hook_compare_finalstates,
                    #             # hook_canvas_post_build=lambda w: plot.canvas_setup_post(common_plot.mod_shift_leg(w))
                    #             )
                    #         )
                    #     ]),

                    ####### TABLES ########

                    # varial.tools.ToolChain('MergeChannelsTables', [
                    #     varial.tools.HistoLoader(
                    #         pattern=[output_dir+'/%s/TreeProject/TreeProjector/*.root'%name]+list(sys_path+'/%s*/*.root'% i for i in uncerts),
                    #         filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in plot.more_samples) and\
                    #             'Region_Comb' not in w.in_file_path and\
                    #             any(w.in_file_path.endswith(f) for f in ['ST']),
                    #         hook_loaded_histos=plot.loader_hook_merge_regions,
                    #     ),
                    #     plot.mk_toolchain('HistogramsMerged',
                    #         plotter_factory=plot.plotter_factory_stack(hook_loaded_histos=plot.loader_hook_merge_lep_channels),
                    #         pattern=None, input_result_path='../HistoLoader'),
                    #     CountTable([
                    #             table_block_signal,
                    #             table_block_background,
                    #             [(r'\textbf{Total Background}', lambda w: 'Integral___bkg_sum' in w)],
                    #             [(r'\textbf{data}', lambda w: 'Integral___Run2015CD' in w)],
                    #         ],
                    #         get_table_category_block(),
                    #         name='CountTable'
                    #         ),
                    #     EffTable([
                    #             table_block_signal,
                    #         ],
                    #         get_table_category_block(),
                    #         norm_factors,
                    #         squash_errs=True,
                    #         name='EffTable'
                    #         ),
                    #     EffTable([
                    #             table_block_signal_fs_700,
                    #             table_block_signal_fs_1700,
                    #         ],
                    #         get_table_category_block(),
                    #         norm_factors,
                    #         squash_errs=True,
                    #         name='EffTableCompFS'
                    #         ),
                    #     ]),

                    # varial.tools.ToolChain('TablesSplitLepton', [
                    #     plot.mk_toolchain('Histograms', plot.more_samples, 
                    #             pattern=[output_dir+'/%s/TreeProject/TreeProjector/*.root'%name]
                    #             + list(sys_path+'/%s*/*.root'% i for i in uncerts)
                    #             ),  
                    #     CountTable([
                    #             table_block_signal,
                    #             table_block_background,
                    #             [(r'\textbf{Total Background}', lambda w: 'Integral___bkg_sum' in w)],
                    #             [(r'\textbf{data}', lambda w: 'Integral___Run2015CD' in w)],
                    #         ],
                    #         get_table_category_block_split('Mu45'),
                    #         name='CountTableMu45'
                    #         ),
                    #     CountTable([
                    #             table_block_signal,
                    #             table_block_background,
                    #             [(r'\textbf{Total Background}', lambda w: 'Integral___bkg_sum' in w)],
                    #             [(r'\textbf{data}', lambda w: 'Integral___Run2015CD' in w)],
                    #         ],
                    #         get_table_category_block_split('El45'),
                    #         name='CountTableEl45'
                    #         ),
                    #     EffTable([
                    #             table_block_signal,
                    #         ],
                    #         get_table_category_block_split('Mu45'),
                    #         norm_factors,
                    #         squash_errs=True,
                    #         name='EffTableMu45'
                    #         ),
                    #     EffTable([
                    #             table_block_signal,
                    #         ],
                    #         get_table_category_block_split('El45'),
                    #         norm_factors,
                    #         squash_errs=True,
                    #         name='EffTableEl45'
                    #         ),

                    #     ]),

                    varial.tools.WebCreator(),
                    

                    ]
            # return tmp

    ######### DEPRECATED #########

    # for uc_name, uncert_list in plot_uncerts.iteritems():
    #     if all(i in sys_list for i in uncert_list):
    #         tc_plot_sens += [
    #             plot.mk_toolchain('HistogramsComp_'+uc_name, plot.less_samples_to_plot_only_th, 
    #                 pattern=[output_dir+'/%s/TreeProject/TreeProjector/*.root'%name]
    #                 + list(sys_path+'/%s*/*.root'% i for i in uncert_list if i in uncerts)
    #                 )
    #             # plot.mk_toolchain_norm('HistogramsCompNormToInt_'+uc_name, [output_dir+'/%s/TreeProject/TreeProjector/*.root'%name]
    #             #     + list(sys_path+'/%s*/*.root'% i for i in uncert_list if i in uncerts)
    #             #     ,plot.less_samples_to_plot_only_th),
    #             ]


    ###############################
    ############ FOR AN ###########
    ###############################
    path_sens = os.path.join(output_dir, name+'/Limit')
    path_sens_old = os.path.join(output_dir, name+'/PlotAndSens')
    path_an = os.path.join(output_dir, name+'/PlotAN')
    path_pas = os.path.join(output_dir, name+'/PlotPAS')
    def mk_tc_an():
        tc_tex = [
            tex_content.mk_autoContentSignalControlRegion(path_an+'/HistogramsNoData', 'El45', 'Mu45', 'NoDataFinalRegions_'+name),
            tex_content.mk_autoContentSignalControlRegion(path_an+'/Histograms', 'El45', 'Mu45', 'WithDataFinalRegions_'+name),
            tex_content.mk_autoContentSystematicCRPlots(path_an+'/Histograms', 'El45', 'Mu45', 'SystematicCRPlots_'+name),
            tex_content.mk_autoContentSystematicCRPlots(path_an+'/HistogramsNormToInt', 'El45', 'Mu45', 'SystematicCRPlotsNormed_'+name),
            tex_content.mk_compSystematicPlots(path_an+'/HistogramsCompUncerts', treeproject_tptp.ttbar_smpl, 'El45', 'Mu45', 'CompUncertPlotsTTbar_'+name),
            tex_content.mk_autoContentSignalControlRegionCombinedMore(path_an+'/MergeChannelsMoreHists/HistogramsMerged/StackedAll', 'WithDataFinalRegionsCombinedMore_'+name),
            tex_content.mk_autoContentHiggsVarCombinedMore(path_an+'/MergeChannelsMoreHistsCombFinalStates/HistogramsMerged/StackedAll', 'WithDataFinalRegionsCombinedCompFinalStates_'+name, size='0.45'),
            tex_content.mk_autoContentHiggsVarCombinedMore(path_an+'/MergeChannelsMoreHistsCombFinalStates/HistogramsNoData/StackedAll', 'NoDataFinalRegionsCombinedCompFinalStates_'+name, size='0.45'),
            tex_content.mk_autoContentSignalControlRegionCombinedMore(path_an+'/MergeChannelsMoreHists/HistogramsMergedNoData/StackedAll', 'NoDataFinalRegionsCombinedMore_'+name),
            tex_content.mk_autoContentSignalControlRegionCombinedMore(path_an+'/MergeChannelsMoreHists/HistogramsNormToInt/StackedAll', 'NormedSystPlotsCombinedMore_'+name),
            tex_content.mk_autoContentLimits(path_sens, 'El45', 'Mu45', 'LimitPlots_'+name),
            tex_content.mk_autoContentLimitsLarge(path_sens, 'El45', 'Mu45', 'LimitPlotsLarge_'+name),
            tex_content.mk_autoContentLimits(path_sens_old, 'El45', 'Mu45', 'LimitPlotsOld_'+name),
            tex_content.mk_autoContentLimitsLarge(path_sens_old, 'El45', 'Mu45', 'LimitPlotsLargeOld_'+name),
            tex_content.mk_autoContentSysTabs(path_sens, 'El45', 'Mu45', 'SysTabs_'+name, mass_points=['M-0800', 'M-1200', 'M-1600']),
            ######## TABLES ########
            tex_content.mk_autoEffCount(path_an+'/MergeChannelsTables/EffTable/count_table_content.tex', name='EffTable_'+name),
            tex_content.mk_autoEffCount(path_an+'/MergeChannelsTables/EffTableCompFS/count_table_content.tex', name='EffTableCompFS_'+name),
            tex_content.mk_autoEffCount(path_an+'/MergeChannelsTables/CountTable/count_table_content.tex', name='CountTable_'+name),
            tex_content.mk_autoEffCount(path_an+'/TablesSplitLepton/EffTableEl45/count_table_content.tex', name='EffTableEl45_'+name),
            tex_content.mk_autoEffCount(path_an+'/TablesSplitLepton/EffTableMu45/count_table_content.tex', name='EffTableMu45_'+name),
            tex_content.mk_autoEffCount(path_an+'/TablesSplitLepton/CountTableEl45/count_table_content.tex', name='CountTableEl45_'+name),
            tex_content.mk_autoEffCount(path_an+'/TablesSplitLepton/CountTableMu45/count_table_content.tex', name='CountTableMu45_'+name),

            ######### DEPRECATED #########
            # tex_content.mk_autoContentSignalControlRegionCombined(path_an+'/MergeChannels/HistogramsMergeLeptonChannels', 'WithDataFinalRegionsCombined_'+name),
        ]
        
        ######## LIMIT PLOTS AND SYSTEMATIC TABLES ########

        # if name == 'TopPtAndHTReweighting':
        #     tc_tex += [tex_content.mk_autoContentLimits(path_an, 'El45', 'Mu45', 'LimitPlots_'+name, mass_points=['TpTp_M-0700', 'TpTp_M-1000', 'TpTp_M-1300', 'TpTp_M-1700'])]
        #     tc_tex += [tex_content.mk_autoContentLimitsLarge(path_an, 'El45', 'Mu45', 'LimitPlotsLarge_'+name, mass_points=['TpTp_M-0700', 'TpTp_M-1000', 'TpTp_M-1300', 'TpTp_M-1700'])]


        if name == 'NoReweighting':
            # if all(os.path.exists(sys_path+'/'+s+suf) for s in ['ScaleVar', 'Exp'] for suf in ['__plus', '__minus']):
            tc_tex += [
                # tex_content.mk_autoContentCompSystPlots(
                #     list(path_an+'/HistogramsComp_'+uc_name for uc_name in ['ScaleVar', 'Exp']), # ['ScaleVar', 'PDF', 'TTbarScale', 'Exp']
                #     'El45', 'Mu45', 'CompSystPlots_'+name),
                tex_content.mk_autoContentSignalControlRegionCombinedMore(path_an+'/MergeChannelsMoreHists/HistogramsMergedNoUncerts/StackedAll', 'WithDataFinalRegionsCombinedMoreNoUncerts_'+name),
                ]
        # for uc_name, uncert_list in plot_uncerts.iteritems():
        #     if any(i in uncerts for i in uncert_list):
        #         tc_tex += [
        #             tex_content.mk_autoContentSystematicCRPlots(
        #                 path_an+'/HistogramsComp_'+uc_name, 'El45', 'Mu45', 'SystematicCRPlots_'+uc_name+'_'+name),
        #             # tex_content.mk_autoContentSystematicCRPlots(
        #             #     path_an+'/HistogramsCompNormToInt_'+uc_name, 'El45', 'Mu45', 'SystematicCRPlotsNormed_'+uc_name+'_'+name)
        #             ]
        #     tc_tex += [tex_content.mk_autoContentLimits(path_an, 'El45', 'Mu45', 'LimitPlots_'+name, prefix='LimitsAllUncertsAllRegions', mass_points=['TpTp_M-0700', 'TpTp_M-1000', 'TpTp_M-1300', 'TpTp_M-1700'])]
        #     tc_tex += [tex_content.mk_autoContentLimitsLarge(path_an, 'El45', 'Mu45', 'LimitPlotsLarge_'+name, mass_points=['TpTp_M-0700', 'TpTp_M-1000', 'TpTp_M-1300', 'TpTp_M-1700'])]

        # tc_tex += [tex_content.mk_autoContentCompSystPlots(
        #             list(path_an+'/HistogramsCompNormToInt_'+uc_name for uc_name in ['ScaleVar', 'PDF', 'TTbarScale', 'Exp']),
        #              'El45', 'Mu45', 'CompSystPlotsNormed_'+name)]
        tc_tex = [
            varial.tools.ToolChain('Tex', tc_tex),
            varial.tools.CopyTool('dnowatsc@lxplus.cern.ch:AN-Dir/notes/AN-15-327/trunk/', src='../Tex/*', ignore=('*.svn', '*.html'), use_rsync=True),
            ]
        return tc_tex

    ######### DEPRECATED #########


    ###############################
    ############ FOR PAS ##########
    ###############################

    def mk_tc_pas():
        tc_tex_pas = [
            tex_content.mk_autoContentSignalControlRegionCombinedMore(path_pas+'/MergeChannelsMoreHists/HistogramsMerged/StackedAll', 'WithDataFinalRegionsCombinedMore_'+name, size='0.45'),
            tex_content.mk_autoContentHiggsVarCombinedMore(path_pas+'/MergeChannelsMoreHistsCombFinalStates/HistogramsMerged/StackedAll', 'WithDataFinalRegionsCombinedCompFinalStates_'+name, size='0.45'),
            tex_content.mk_autoContentHiggsVarCombinedMore(path_pas+'/MergeChannelsMoreHistsCombFinalStates/HistogramsNoData/StackedAll', 'NoDataFinalRegionsCombinedCompFinalStates_'+name, size='0.45'),
            tex_content.mk_autoContentSignalControlRegionCombinedMore(path_pas+'/MergeChannelsMoreHists/HistogramsMergedNoData/StackedAll', 'NoDataFinalRegionsCombinedMore_'+name),
            tex_content.mk_autoContentLimits(path_sens_old, 'El45', 'Mu45', 'LimitPlotsOld_'+name),
            tex_content.mk_autoContentLimitsLarge(path_sens_old, 'El45', 'Mu45', 'LimitPlotsLargeOld_'+name),
            tex_content.mk_autoEffCount(path_pas+'/MergeChannelsTables/EffTable/count_table_content.tex', name='EffTable_'+name),
            tex_content.mk_autoEffCount(path_pas+'/MergeChannelsTables/EffTableCompFS/count_table_content.tex', name='EffTableCompFS_'+name),
            tex_content.mk_autoEffCount(path_pas+'/MergeChannelsTables/CountTable/count_table_content.tex', name='CountTable_'+name),
            # tex_content.mk_autoContentSignalControlRegionCombinedMore(path_pas+'/MergeChannelsMoreHists/HistogramsMergedNoUncerts/StackedAll', 'WithDataFinalRegionsCombinedMore_'+name),
            # tex_content.mk_autoContentSignalControlRegionCombinedMore(path_pas+'/MergeChannelsMoreHists/HistogramsMergedNoData/StackedAll', 'NoDataFinalRegionsCombinedMore_'+name),
            tex_content.mk_autoContentControlRegion(path_pas+'/Histograms/StackedAll', path_pas+'/MergeChannelsMoreHists/HistogramsMerged/StackedAll', 'El45', 'Mu45', 'WithDataSidebandRegions_'+name),
            # # tex_content.mk_autoEffCount(path_pas+'/MergeChannels/EffTable/count_table_content.tex', name='EffTable_'+name),
            # # tex_content.mk_autoEffCount(path_pas+'/MergeChannels/EffTableCompFS/count_table_content.tex', name='EffTableCompFS_'+name),
            # # tex_content.mk_autoEffCount(path_pas+'/MergeChannels/CountTable/count_table_content.tex', name='CountTable_'+name),
        ]
        # if name == 'TopPtAndHTReweighting':
        #     tc_tex_pas += [tex_content.mk_autoContentLimits(path_pas, 'El45', 'Mu45', 'LimitPlots_'+name, mass_points=['TpTp_M-0700', 'TpTp_M-1000', 'TpTp_M-1300', 'TpTp_M-1700'])]
        #     tc_tex_pas += [tex_content.mk_autoContentLimitsLarge(path_pas, 'El45', 'Mu45', 'LimitPlotsLarge_'+name, mass_points=['TpTp_M-0700', 'TpTp_M-1000', 'TpTp_M-1300', 'TpTp_M-1700'])]
        # else:
        #     tc_tex_pas += [tex_content.mk_autoContentLimits(path_pas, 'El45', 'Mu45', 'LimitPlots_'+name, prefix='LimitsAllUncertsAllRegions', mass_points=['TpTp_M-0700', 'TpTp_M-1000', 'TpTp_M-1300', 'TpTp_M-1700'])]
        #     tc_tex_pas += [tex_content.mk_autoContentLimitsLarge(path_pas, 'El45', 'Mu45', 'LimitPlotsLarge_'+name, mass_points=['TpTp_M-0700', 'TpTp_M-1000', 'TpTp_M-1300', 'TpTp_M-1700'])]
        tc_tex_pas = [
            varial.tools.ToolChain('TexPas', tc_tex_pas),
            varial.tools.CopyTool('dnowatsc@lxplus.cern.ch:PAS-Dir/notes/B2G-16-011/trunk/', src='../TexPas/*', ignore=('*.svn', '*.html'), use_rsync=True),
            ]
        return tc_tex_pas



    
    
    return varial.tools.ToolChain(name, [
            # varial.tools.ToolChainParallel('TreeProject', tc_tp, n_workers=1),
            varial.tools.ToolChainParallel('Limit', lazy_eval_tools_func=mk_tc_sens, n_workers=1),
            # varial.tools.ToolChainParallel('PlotAN', lazy_eval_tools_func=mk_tc_plot, n_workers=1),
            # varial.tools.ToolChainParallel('PlotPAS', lazy_eval_tools_func=mk_tc_plot, n_workers=1),
            # varial.tools.ToolChainParallel('TexAN', lazy_eval_tools_func=mk_tc_an, n_workers=1),
            # varial.tools.ToolChainParallel('TexPAS', lazy_eval_tools_func=mk_tc_pas, n_workers=1),

        ])

def run_treeproject_and_plot(output_dir):
    base_path = os.path.join(os.getcwd(), 'Files_and_Plots')
    tc = varial.tools.ToolChain(
        output_dir,
        [
            git.GitAdder(),
            varial.tools.ToolChainParallel('RunAnalysis', [

                make_tp_plot_chain('HTReweighting', base_path, output_dir+'/RunAnalysis',
                    add_uncert_func=add_all_with_weight_uncertainties({
                        'ht_reweight' : {
                            treeproject_tptp.ttbar_smpl : ht_reweight_ttbar_no_top_pt_reweight,
                            'WJets' : ht_reweight_wjets_no_top_pt_reweight
                            }
                        }),
                    mod_sample_weights={
                        treeproject_tptp.ttbar_smpl : treeproject_tptp.base_weight+'*'+ht_reweight_ttbar_no_top_pt_reweight,
                        'WJets' : treeproject_tptp.base_weight+'*'+ht_reweight_wjets_no_top_pt_reweight,
                    },
                    # br_list=br_list_all,
                    # uncertainties=all_uncerts+['ht_reweight']
                    ),
                # make_tp_plot_chain('NoReweighting', base_path, output_dir+'/RunAnalysis', 
                #     add_uncert_func=add_all_without_weight_uncertainties,
                #     # uncertainties=all_uncerts
                #     ),
                # make_tp_plot_chain('TopPtReweighting', base_path, output_dir+'/RunAnalysis',
                #     add_uncert_func=add_all_with_weight_uncertainties({'top_pt_reweight' : {treeproject_tptp.ttbar_smpl : top_pt_reweight}}),
                #     mod_sample_weights={treeproject_tptp.ttbar_smpl : treeproject_tptp.base_weight+'*'+top_pt_reweight},
                #     # uncertainties=all_uncerts+['top_pt_reweight']
                #     ),
                # make_tp_plot_chain('TopPtAndHTReweighting', base_path, output_dir+'/RunAnalysis',
                #     add_uncert_func=add_all_with_weight_uncertainties({
                #         'ht_reweight' : {
                #             treeproject_tptp.ttbar_smpl : ht_reweight_ttbar_w_top_pt_reweight,
                #             'WJets' : ht_reweight_wjets_w_top_pt_reweight
                #             },
                #         'top_pt_reweight' : {treeproject_tptp.ttbar_smpl : top_pt_reweight}
                #         }),
                #     mod_sample_weights={
                #         treeproject_tptp.ttbar_smpl : treeproject_tptp.base_weight+'*'+top_pt_reweight+'*'+ht_reweight_ttbar_w_top_pt_reweight,
                #         'WJets' : treeproject_tptp.base_weight+'*'+ht_reweight_wjets_w_top_pt_reweight,
                #     },
                #     # uncertainties=all_uncerts+['ht_reweight', 'top_pt_reweight']
                #     ),

                ], n_workers=1),
            # varial.tools.ToolChain('ReweightingComparision', [
            #     tex_content.mk_autoCompareReweightingMethods(output_dir+'/RunAnalysis', ['NoReweighting', 'HTReweighting', 'TopPtReweighting', 'TopPtAndHTReweighting'], name='CompareReweightingDistributions'),
            #     tex_content.mk_autoComparePostfitPlots(output_dir+'/RunAnalysis', ['NoReweighting', 'HTReweighting', 'TopPtReweighting', 'TopPtAndHTReweighting'], name='CompareReweightingPostfits'),
            #     ]),
            # varial.tools.CopyTool('dnowatsc@lxplus.cern.ch:AN-Dir/notes/AN-15-327/trunk/', src='../ReweightingComparision/*', ignore=('*.svn', '*.html'), use_rsync=True),
            git.GitTagger(commit_prefix='In {0}'.format(output_dir)),
            # mk_tex_tc_post(output_dir+'/Histograms/')(), 

            # varial.tools.PrintToolTree(),
            # tex_content.tc,
            # varial.tools.CopyTool('~/www/auth/VLQ2HT', use_rsync=True),
        ]
    )
    return tc


varial.settings.try_reuse_results = True

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Provide output_dir!'
        exit(-1)
    varial.tools.Runner(run_treeproject_and_plot(sys.argv[1]), True)

# varial.settings.rootfile_postfixes += ['.pdf']
# varial.tools.Runner(tc, True)
# import varial.main
# varial.main.main(toolchain=tc)