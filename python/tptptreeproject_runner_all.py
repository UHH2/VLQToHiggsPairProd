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
import common_sensitivity
import tex_content

varial.settings.plot_obs = True
varial.settings.asymptotic = False
varial.settings.merge_decay_channels = False

all_regions = [
    'SignalRegion2b_Mu45',
    'SignalRegion1b_Mu45',
    'SidebandRegion_Mu45',
    'SignalRegion2b_El45',
    'SignalRegion1b_El45',
    'SidebandRegion_El45',
]

def mk_limit_list_syst(sys_pat=None, list_region=all_regions):
    def tmp():
        limit_list = []
        for ind, brs_ in enumerate(sensitivity.br_list):
            # if ind > 2: break
            tc = []
            tc.append(varial.tools.ToolChainParallel(
                'ThetaLimits', list(varial.tools.ToolChain(
                    sig,
                    sensitivity.mk_limit_tc_single(brs_, sensitivity.select_single_sig(list_region,
                        'ST', sig),
                    sig, selection='ThetaLimits', sys_pat=sys_pat))
                for sig in sensitivity.signals_to_use)
            ))
            tc.append(varial.tools.ToolChain('LimitsWithGraphs',[
                limits.LimitGraphs(
                    limit_path='../../ThetaLimits/*/ThetaLimit',
                    plot_obs=varial.settings.plot_obs,
                    plot_1sigmabands=True,
                    plot_2sigmabands=True,
                    axis_labels=("m_{T'} [GeV]", "#sigma x BR [pb]"),
                    ),
                varial.plotter.Plotter(
                    name='LimitCurvesCompared',
                    input_result_path='../LimitGraphs',
                    # filter_keyfunc=lambda w: 'Uncleaned' in w.legend,
                    # plot_setup=plot_setup,
                    hook_loaded_histos=sensitivity.limit_curve_loader_hook,
                    plot_grouper=lambda ws: varial.gen.group(
                            ws, key_func=lambda w: w.save_name),
                    # save_name_func=varial.plotter.save_by_name_with_hash
                    save_name_func=lambda w: w.save_name,
                    plot_setup=lambda w: sensitivity.plot_setup_graphs(w,
                        th_x=common_sensitivity.theory_masses,
                        th_y=common_sensitivity.theory_cs),
                    canvas_decorators=[varial.rendering.Legend(x_pos=.85, y_pos=0.6, label_width=0.2, label_height=0.07),
                        # varial.rendering.TitleBox(text='#scale[1.2]{#bf{#it{Work in Progress}}}')
                        ],
                    # save_lin_log_scale=True
                    ),
                ]))
            limit_list.append(
                varial.tools.ToolChain('Limit'+str(ind),tc))
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
    'ST                       > 800'
]

# final regions

sr2b_channel = baseline_selection + [
    'n_higgs_tags_2b_med    >= 1',
    'n_additional_btags_medium  >= 1',
]

sr1b_channel = baseline_selection + [
    'n_higgs_tags_2b_med    == 0',
    'n_higgs_tags_1b_med    >= 1',
    'n_additional_btags_medium  >= 1',
]

sb_channel = baseline_selection + [
    'n_higgs_tags_1b_med        == 0',
    'n_additional_btags_medium  >= 1',
    'met                        >= 100'
]

sb_ttbar_channel = baseline_selection + [
    'n_higgs_tags_1b_med        == 0',
    'n_additional_btags_medium  >= 2',
    'met                        >= 100'
]

sb_wjets_channel = baseline_selection + [
    'n_higgs_tags_1b_med        == 0',
    'n_additional_btags_medium  == 0',
    'met                        >= 100'
]


# lepton selections

el_channel = [
    'trigger_accept_el45   >= 1',
    'trigger_accept_mu45   == 0',
    'pt_ld_ak4_jet         > 250.',
    'pt_subld_ak4_jet      > 65.',
    'primary_lepton_pt     > 50.'
]

mu_channel = [
    'trigger_accept_mu45   >= 1',
    'primary_lepton_pt     > 47.'
]

final_regions = (
    ('BaseLineSelectionEl45', el_channel),
    ('BaseLineSelectionMu45', mu_channel),
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


all_uncerts = [
    'jec',
    'jer',
    'btag_bc',
    'btag_udsg',
    'sfmu_id',
    'sfmu_trg',
    'pu',
    # 'PDF',
    'ScaleVar',
    'rate'
    # 'top_pt_weight',
    # 'ht_reweight'
]

plot_uncerts = {
    'Exp' : ['jec', 'jer', 'btag_bc', 'btag_udsg', 'sfmu_id', 'sfmu_trg', 'pu', 'rate'],
    'ScaleVar' : ['ScaleVar'],
    # 'PDF' : ['PDF'],
    'TopPt' : ['top_pt_reweight'],
    'HT' : ['ht_reweight'],
}

# theory_uncerts = [
#     'PDF',
#     'ScaleVar',
#     'top_pt_weight',
#     'ht_reweight'
# ]

# values below from FinalSelection-v14/RunWJetsSideband/fit_results_ht_sideband_w_toppt_reweight.txt
# p0_from1000 = 1.252481
# p1_from1000 = -0.000216602

# p0_from0 = 1.353281
# p1_from0 = -0.000251745

# values below from FinalSelection-v14/RunCompTopPtWeight/fit_results_ht_sideband_no_toppt_reweight.txt

# values from mean of SidebandRegion
# p0_from0_no_top_pt_reweight_0 = 1.165688
# p1_from0_no_top_pt_reweight_0 = -0.000236061

# NO TOP PT REWEIGHTING
# values from mean of SidebandTTJetsRegion
p0_ttbar_from0_no_top_pt_reweight = 1.1565025
p1_ttbar_from0_no_top_pt_reweight = -0.000297251
# values from mean of SidebandWPlusJetsRegion
p0_wjets_from0_no_top_pt_reweight = 1.1012315
p1_wjets_from0_no_top_pt_reweight = -0.000217951

# WITH TOP PT REWEIGHTING
# values from mean of SidebandTTJetsRegion
p0_ttbar_from0_w_top_pt_reweight = 1.376561
p1_ttbar_from0_w_top_pt_reweight = -0.000331145
# values from mean of SidebandWPlusJetsRegion
p0_wjets_from0_w_top_pt_reweight = 1.14162275
p1_wjets_from0_w_top_pt_reweight = -0.000225091

ht_reweight_ttbar_no_top_pt_reweight = '({0}+{1}*HT)'.format(p0_ttbar_from0_no_top_pt_reweight, p1_ttbar_from0_no_top_pt_reweight)
ht_reweight_wjets_no_top_pt_reweight = '({0}+{1}*HT)'.format(p0_wjets_from0_no_top_pt_reweight, p1_wjets_from0_no_top_pt_reweight)
ht_reweight_ttbar_w_top_pt_reweight = '({0}+{1}*HT)'.format(p0_ttbar_from0_w_top_pt_reweight, p1_ttbar_from0_w_top_pt_reweight)
ht_reweight_wjets_w_top_pt_reweight = '({0}+{1}*HT)'.format(p0_wjets_from0_w_top_pt_reweight, p1_wjets_from0_w_top_pt_reweight)
# gen_ht_reweight = '({0}+{1}*gen_ht)'.format(p0_from0_no_top_pt_reweight_0, p1_from0_no_top_pt_reweight_0)
# parton_ht_reweight = '({0}+{1}*parton_ht)'.format(p0_from0_no_top_pt_reweight_0, p1_from0_no_top_pt_reweight_0)
top_pt_reweight = '(weight_ttbar/0.9910819)'


def add_all_with_weight_uncertainties(dict_weight_uncerts):
    def add_uncerts(base_path, weights):
        def tmp():
            sys_tps = []
            sys_tps += treeproject_tptp.add_jec_uncerts(base_path, final_regions, weights)
            sys_tps += treeproject_tptp.add_generic_uncerts(base_path, final_regions, weights)
            # sys_tps += treeproject_tptp.add_pdf_uncerts(base_path, final_regions, weights)
            sys_tps += treeproject_tptp.add_scale_var_uncerts(base_path, final_regions, weights)
            for weight_name, weight_dict in dict_weight_uncerts.iteritems():
                sys_tps += treeproject_tptp.add_weight_uncerts(base_path, final_regions, weights, weight_name, weight_dict)
            return sys_tps
        return tmp
    return add_uncerts

def add_only_weight_uncertainties(dict_weight_uncerts):
    def add_uncerts(base_path, weights):
        def tmp():
            sys_tps = []
            for weight_name, weight_dict in dict_weight_uncerts.iteritems():
                sys_tps += treeproject_tptp.add_weight_uncerts(base_path, final_regions, weights, weight_name, weight_dict)
            return sys_tps
        return tmp
    return add_uncerts

def add_all_without_weight_uncertainties(base_path, weights):
    def tmp():
        sys_tps = []
        sys_tps += treeproject_tptp.add_jec_uncerts(base_path, final_regions, weights)
        sys_tps += treeproject_tptp.add_generic_uncerts(base_path, final_regions, weights)
        # sys_tps += treeproject_tptp.add_pdf_uncerts(base_path, final_regions, weights)
        sys_tps += treeproject_tptp.add_scale_var_uncerts(base_path, final_regions, weights)
        return sys_tps
    return tmp

def no_uncertainties(x, y):
    def tmp():
        return []
    return tmp

def mk_tex_tc_post(base, name):
    # return varial.tools.ToolChain('TexCopy', [
    return varial.tools.ToolChain(
            'Tex', 
            [
                # mk_autoContentSignalControlRegion(p_postbase),
                # tex_content.mk_autoContentFinalSelectionHiggsVar(base, 'El45', 'Mu45'),
                # tex_content.mk_autoContentPreSelectionNm1(base, 'El45_Baseline', 'Mu45_Baseline'),
                # tex_content.mk_autoContentJetPtReweight(base),
                # mk_autoContentLimits(p_postbase)
            ]
        )
        # varial.tools.CopyTool('dnowatsc@lxplus.cern.ch:AN-Dir/notes/AN-15-327/trunk/', src='../Tex/*', ignore=(), use_rsync=True)
    # ])


def make_tp_plot_chain(name, base_path, output_dir, add_uncert_func,
    mod_sample_weights=None, uncertainties=None):
    if mod_sample_weights:
        weights = dict(treeproject_tptp.sample_weights_def)
        weights.update(mod_sample_weights)
    else:
        weights = treeproject_tptp.sample_weights_def
    uncerts = uncertainties or []
    tc = [
            treeproject_tptp.mk_tp(base_path, final_regions, weights),
            treeproject_tptp.mk_sys_tps(add_uncert_func(base_path, weights)),
            # sensitivity.mk_tc('LimitsAllUncertsAllRegions', mk_limit_list_syst(
            #     list(output_dir+'/%s/SysTreeProjectors/%s*/*.root'%(name, i) for i in uncerts),
            #     all_regions
            # )),                                             
            # plot.mk_toolchain('Histograms', [output_dir+'/%s/TreeProjector/*.root'%name]
            #             + list(output_dir+'/%s/SysTreeProjectors/%s*/*.root'%(name, i) for i in uncerts)
            #             ,plot.samples_to_plot_final, compare_uncerts=True),
            # plot.mk_toolchain('HistogramsNoData', [output_dir+'/%s/TreeProjector/*.root'%name]
            #             # + list(output_dir+'/%s/SysTreeProjectors/%s*/*.root'%(name, i) for i in uncerts)
            #             ,plot.samples_to_plot_final,
            #             filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in plot.samples_to_plot_final if 'Run2015CD' not in f)),
            # # plot.mk_toolchain_pull('HistogramsPull', [output_dir+'/%s/TreeProjector/*.root'%name]
            # #             + list(output_dir+'/%s/SysTreeProjectors/%s*/*.root'%(name, i) for i in uncerts)
            # #             ,plot.samples_to_plot_final),               
            # plot.mk_toolchain('HistogramsNoUncerts', [output_dir+'/%s/TreeProjector/*.root'%name]
            #             # + list(output_dir+'/%s/SysTreeProjectors/%s*/*.root'%(name, i) for i in uncerts)
            #             ,plot.samples_to_plot_final),
        ]
    # for uc_name, uncert_list in plot_uncerts.iteritems():
    #     if any(i in uncerts for i in uncert_list):
    #         tc += [plot.mk_toolchain('Histograms'+uc_name, [output_dir+'/%s/TreeProjector/*.root'%name]
    #             + list(output_dir+'/%s/SysTreeProjectors/%s*/*.root'%(name, i) for i in uncert_list if i in uncerts)
    #             ,plot.samples_to_plot_final)]
    tc += [
        # sensitivity.mk_tc('LimitsAllUncertsAllRegions', mk_limit_list_syst(
        #     list(output_dir+'/%s/SysTreeProjectors/%s*/*.root'%(name, i) for i in uncerts),
        #     all_regions
        # )),
        # sensitivity.mk_tc('LimitsAllUncertsOnlyEl', mk_limit_list_syst(
        #     list(output_dir+'/%s/SysTreeProjectors/%s*/*.root'%(name, i) for i in uncerts),
        #     ['SignalRegion2b_El45', 'SignalRegion1b_El45', 'SidebandRegion_El45']
        # )),
        # sensitivity.mk_tc('LimitsAllUncertsOnlyMu', mk_limit_list_syst(
        #     list(output_dir+'/%s/SysTreeProjectors/%s*/*.root'%(name, i) for i in uncerts),
        #     ['SignalRegion2b_Mu45', 'SignalRegion1b_Mu45', 'SidebandRegion_Mu45']
        # )),
        # sensitivity.mk_tc('LimitsAllUncertsOnlySignal', mk_limit_list_syst(
        #     list(output_dir+'/%s/SysTreeProjectors/%s*/*.root'%(name, i) for i in uncerts),
        #     ['SignalRegion2b_Mu45', 'SignalRegion1b_Mu45', 'SignalRegion2b_El45', 'SignalRegion1b_El45']
        # )),
        # sensitivity.mk_tc('LimitsAllUncertsNoH1B', mk_limit_list_syst(
        #     list(output_dir+'/%s/SysTreeProjectors/%s*/*.root'%(name, i) for i in uncerts),
        #     ['SignalRegion2b_Mu45', 'SidebandRegion_Mu45', 'SignalRegion2b_El45', 'SidebandRegion_El45']
        # )),
        # sensitivity.mk_tc('LimitsAllUncertsOnlyH2B', mk_limit_list_syst(
        #     list(output_dir+'/%s/SysTreeProjectors/%s*/*.root'%(name, i) for i in uncerts),
        #     ['SignalRegion2b_Mu45', 'SignalRegion2b_El45']
        # )),
        varial.tools.HistoLoader(
            pattern='../TreeProjector/*.root',
            name='MergedSidebandsLoader',
            # pattern=common_plot.file_select(datasets_to_plot),
            # input_result_path='../../../../HistoLoader',
            filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in plot.samples_to_plot_final) and\
            any(i in w.in_file_path for i in ['SidebandTTJets', 'SidebandWPlusJets']) and\
            w.in_file_path.endswith('HT'),
                           # and (('SingleEle' not in w.file_path and 'Mu' in category) or\
                           # ('SingleMuon' not in w.file_path and 'El' in category)),
            # hook_loaded_histos=lambda w: cutflow_tables.rebin_cutflow(loader_hook(w))
            hook_loaded_histos=plot.loader_hook_merge_sidebands,
        ),
        varial.plotter.Plotter(
            name='HistogramsMergeSidbands',
            stack=True,
            input_result_path='../MergedSidebandsLoader',
            # filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in plot.samples_to_plot_final) and\
            #                 any(i in w.in_file_path for i in ['SidebandTTJets', 'SidebandWPlusJets']) and\
            #                 w.in_file_path.endswith('HT'),
            # plot_setup=plot_setup,
            stack_grouper=lambda ws: gen.group(ws, key_func=lambda w: w.region),
            save_name_func=lambda w: w._renderers[0].region+'_'+w.name
            # save_name_func=lambda w: w._renderers[0].in_file_path.split('/')[0].split('_')[0]+'_'+w._renderers[0]'_'+w.name
            # save_name_func=lambda w: w.save_name,
            # plot_setup=lambda w: sensitivity.plot_setup_graphs(w,
            #     th_x=common_sensitivity.theory_masses,
            #     th_y=common_sensitivity.theory_cs),
            # canvas_decorators=[varial.rendering.Legend(x_pos=.85, y_pos=0.6, label_width=0.2, label_height=0.07),
            #     # varial.rendering.TitleBox(text='#scale[1.2]{#bf{#it{Work in Progress}}}')
            #     ],
            )
        # plot.mk_toolchain('HistogramsMergeSidbands', [output_dir+'/%s/TreeProjector/*.root'%name]
        #             ,plot.samples_to_plot_final,
        #             filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in plot.samples_to_plot_final) and\
        #                     any(i in w.in_file_path for i in ['SidebandTTJets', 'SidebandWPlusJets']) and\
        #                     w.in_file_path.endswith('HT'),
        #             hook_loaded_histos=plot.loader_hook_merge_sidebands), 
        ]
    tc_tex = [
        tex_content.mk_autoContentSignalControlRegion(os.path.join(output_dir, name)+'/HistogramsNoData', 'El45', 'Mu45', 'NoDataFinalRegions_'+name),
        tex_content.mk_autoContentSignalControlRegion(os.path.join(output_dir, name)+'/Histograms', 'El45', 'Mu45', 'WithDataFinalRegions_'+name),
        tex_content.mk_autoContentSystematicCRPlots(os.path.join(output_dir, name)+'/Histograms', 'El45', 'Mu45', 'SystematicCRPlots_'+name),
        # tex_content.mk_autoContentLimits(os.path.join(output_dir, name), 'El45', 'Mu45', 'LimitPlots_'+name, prefix='LimitsAllUncertsAllRegions'),
    ]
    if name == 'NoReweighting' or name == 'TopPtAndHTReweighting':
        tc_tex += [tex_content.mk_autoContentLimits(os.path.join(output_dir, name), 'El45', 'Mu45', 'LimitPlots_'+name)]
    else:
        tc_tex += [tex_content.mk_autoContentLimits(os.path.join(output_dir, name), 'El45', 'Mu45', 'LimitPlots_'+name, prefix='LimitsAllUncertsAllRegions')]

    for uc_name, uncert_list in plot_uncerts.iteritems():
        if any(i in uncerts for i in uncert_list):
            tc_tex += [tex_content.mk_autoContentSystematicCRPlots(
                os.path.join(output_dir, name)+'/Histograms'+uc_name, 'El45', 'Mu45', 'SystematicCRPlots_'+uc_name+'_'+name)]
    tc += [varial.tools.ToolChain('Tex', tc_tex),
        # varial.tools.CopyTool('dnowatsc@lxplus.cern.ch:AN-Dir/notes/AN-15-327/trunk/', src='../Tex/*', ignore=(), use_rsync=True)
        ]
    return varial.tools.ToolChain(name, tc)

def run_treeproject_and_plot(base_path, output_dir):
    tc = varial.tools.ToolChain(
        output_dir,
        [
            git.GitAdder(),
            make_tp_plot_chain('NoReweighting', base_path, output_dir, 
                add_uncert_func=add_all_without_weight_uncertainties, uncertainties=all_uncerts),
            # make_tp_plot_chain('TopPtReweighting', base_path, output_dir,
            #     add_uncert_func=add_all_with_weight_uncertainties({'top_pt_reweight' : {'TTbar' : top_pt_reweight}}),
            #     mod_sample_weights={'TTbar' : treeproject_tptp.base_weight+'*'+top_pt_reweight},
            #     uncertainties=all_uncerts+['top_pt_reweight']
            #     ),
            # make_tp_plot_chain('HTReweighting', base_path, output_dir,
            #     add_uncert_func=add_all_with_weight_uncertainties({
            #         'ht_reweight' : {
            #             'TTbar' : ht_reweight_ttbar_no_top_pt_reweight,
            #             'WJets' : ht_reweight_wjets_no_top_pt_reweight
            #             }
            #         }),
            #     mod_sample_weights={
            #         'TTbar' : treeproject_tptp.base_weight+'*'+ht_reweight_ttbar_no_top_pt_reweight,
            #         'WJets' : treeproject_tptp.base_weight+'*'+ht_reweight_wjets_no_top_pt_reweight,
            #     },
            #     uncertainties=all_uncerts+['ht_reweight']
            #     ),
            # make_tp_plot_chain('TopPtAndHTReweighting', base_path, output_dir,
            #     add_uncert_func=add_all_with_weight_uncertainties({
            #         'ht_reweight' : {
            #             'TTbar' : ht_reweight_ttbar_w_top_pt_reweight,
            #             'WJets' : ht_reweight_wjets_w_top_pt_reweight
            #             },
            #         'top_pt_reweight' : {'TTbar' : top_pt_reweight}
            #         }),
            #     mod_sample_weights={
            #         'TTbar' : treeproject_tptp.base_weight+'*'+top_pt_reweight+'*'+ht_reweight_ttbar_w_top_pt_reweight,
            #         'WJets' : treeproject_tptp.base_weight+'*'+ht_reweight_wjets_w_top_pt_reweight,
            #     },
            #     uncertainties=all_uncerts+['ht_reweight', 'top_pt_reweight']
            #     ),
            varial.tools.WebCreator(),
            git.GitTagger(commit_prefix='In {0}'.format(output_dir)),
            # mk_tex_tc_post(output_dir+'/Histograms/')(), 
            # varial.tools.CopyTool('dnowatsc@lxplus.cern.ch:AN-Dir/notes/AN-15-327/trunk/', src='../Tex/*', ignore=(), use_rsync=True)

            # varial.tools.PrintToolTree(),
            # tex_content.tc,
            # varial.tools.CopyTool('~/www/auth/VLQ2HT', use_rsync=True),
        ]
    )
    return tc


varial.settings.try_reuse_results = True

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Provide input_dir and output_dir!'
        exit(-1)
    varial.tools.Runner(run_treeproject_and_plot(sys.argv[1], sys.argv[2]), True)

# varial.settings.rootfile_postfixes += ['.pdf']
# varial.tools.Runner(tc, True)
# import varial.main
# varial.main.main(toolchain=tc)