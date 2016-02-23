#!/usr/bin/env python

import UHH2.VLQSemiLepPreSel.vlq_settings as vlq_settings
import UHH2.VLQSemiLepPreSel.common as vlq_common
from varial.extensions.hadd import Hadd
import varial.extensions.make
import varial.tools
import os
import sys
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

# hadd = Hadd(
#     input_pat, 
#     common_plot.basenames, 
#     add_aliases_to_analysis=False,
#     samplename_func=vlq_common.get_samplename
# )

# def mk_limit_list_syst(sys_pat=''):
#     def temp():
#         limit_list = []
#         for ind, brs_ in enumerate(sensitivity.br_list):
#             # if ind > 2: break
#             tc = []
#             # tc.append(varial.tools.ToolChain(
#             #     'El45Only',
#             #     sensitivity.mk_limit_tc(brs_, sensitivity.select_files([
#             #         "SignalRegion2b_El45",
#             #         "SignalRegion1b_El45",
#             #         "SidebandRegion_El45"],
#             #         'ST'),
#             #     name='El45Only', sys_pat=sys_pat))
#             # )
#             # tc.append(varial.tools.ToolChain(
#             #     'Mu45Only',
#             #     sensitivity.mk_limit_tc(brs_, sensitivity.select_files([
#             #         "SignalRegion2b_Mu45",
#             #         "SignalRegion1b_Mu45",
#             #         "SidebandRegion_Mu45"],
#             #         'ST'),
#             #     name='Mu45Only', sys_pat=sys_pat))
#             # )
#             tc.append(varial.tools.ToolChain(
#                 'CombinedChannels',
#                 sensitivity.mk_limit_tc(brs_, sensitivity.select_files([
#                     "SignalRegion2b_El45",
#                     "SignalRegion1b_El45",
#                     "SidebandRegion_El45",
#                     "SignalRegion2b_Mu45",
#                     "SignalRegion1b_Mu45",
#                     "SidebandRegion_Mu45",
#                     ],
#                     'ST'),
#                 sys_pat=sys_pat))
#             )
#             limit_list.append(
#                 varial.tools.ToolChainParallel('Limit'+str(ind),tc))
#         return limit_list
#     return temp

varial.settings.asymptotic = False

def mk_limit_list_syst(sys_pat=None):
    def tmp():
        limit_list = []
        for ind, brs_ in enumerate(sensitivity.br_list):
            # if ind > 2: break
            tc = []
            tc.append(varial.tools.ToolChainParallel(
                'ThetaLimits', list(varial.tools.ToolChain(
                    sig,
                    sensitivity.mk_limit_tc_single(brs_, sensitivity.select_single_sig([
                        # 'SignalRegion2b_Mu45',
                        # 'SignalRegion1b_Mu45',
                        'SidebandRegion_Mu45',
                        # 'SignalRegion2b_El45',
                        # 'SignalRegion1b_El45',
                        'SidebandRegion_El45',
                        ],
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
                    canvas_decorators=[varial.rendering.Legend(x_pos=.85, y_pos=0.5, label_width=0.2, label_height=0.07),
                        varial.rendering.TitleBox(text='#scale[1.2]{#bf{#it{Work in Progress}}}')
                        ],
                    save_lin_log_scale=True
                    ),
                ]))
            limit_list.append(
                varial.tools.ToolChain('Limit'+str(ind),tc))
        return limit_list
    return tmp

def mk_tex_tc_post(base):
    def tmp():
        return varial.tools.ToolChain('TexCopy', [
            varial.tools.ToolChain(
                'Tex', 
                [
                    tex_content.mk_autoContentSignalControlRegion(base),
                    tex_content.mk_autoContentLimits(base)
                ]
            ),
            varial.tools.CopyTool('dnowatsc@lxplus.cern.ch:AN-Dir/notes/AN-15-327/trunk/', src='../Tex/*', ignore=(), use_rsync=True)
        ])
    return tmp


varial.settings.asymptotic = False
varial.settings.merge_decay_channels = False


#!/usr/bin/env python

baseline_selection = [
    # 'gendecay_accept        == 1',
    'n_ak8                    >= 2'
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
)


def run_treeproject_and_plot(base_path, output_dir):
    tc = varial.tools.ToolChain(
        output_dir,
        [
            git.GitAdder(),
            varial.tools.ToolChain(
                'Inputs', [
                    treeproject_tptp.mk_tp(base_path, final_regions),
                    treeproject_tptp.mk_sys_tps(base_path, final_regions),
                ]
            ),
            varial.tools.ToolChain(
                'Histograms',
                [
                    plot.mk_toolchain('HistogramsAll', [output_dir+'/Inputs/TreeProjector/*.root', output_dir+'/Inputs/SysTreeProjectors/*/*.root'], None, plot.samples_to_plot_final),
                    # plot.mk_toolchain('HistogramsOnlyPdfAndScale', [output_dir+'/Inputs/TreeProjector/*.root',
                    #     output_dir+'/Inputs/SysTreeProjectors/PDF*/*.root',
                    #     output_dir+'/Inputs/SysTreeProjectors/Scale*/*.root'],
                    #     None, plot.samples_to_plot_final),
                    # plot.mk_toolchain('HistogramsOnlyPdf', [output_dir+'/Inputs/TreeProjector/*.root',
                    #     output_dir+'/Inputs/SysTreeProjectors/PDF*/*.root',
                    #     ],
                    #     None, plot.samples_to_plot_final),
                    # plot.mk_toolchain('HistogramsOnlyScale', [output_dir+'/Inputs/TreeProjector/*.root',
                    #     output_dir+'/Inputs/SysTreeProjectors/Scale*/*.root',
                    #     ],
                    #     None, plot.samples_to_plot_final),
                    # plot.mk_toolchain('HistogramsNoPdfAndScale', [output_dir+'/Inputs/TreeProjector/*.root',
                    #     output_dir+'/Inputs/SysTreeProjectors/btag_bc*/*.root',
                    #     output_dir+'/Inputs/SysTreeProjectors/btag_udsg*/*.root',
                    #     output_dir+'/Inputs/SysTreeProjectors/jec*/*.root',
                    #     output_dir+'/Inputs/SysTreeProjectors/jer*/*.root',
                    #     output_dir+'/Inputs/SysTreeProjectors/pu*/*.root',
                    #     output_dir+'/Inputs/SysTreeProjectors/sfmu_id*/*.root',
                    #     output_dir+'/Inputs/SysTreeProjectors/sfmu_trg*/*.root',
                    #     ],
                    #     None, plot.samples_to_plot_final),
                    # sensitivity.mk_tc('LimitsSystScalePdf', mk_limit_list_syst([
                    #     output_dir+'/Inputs/SysTreeProjectors/Scale*/*.root',
                    #     output_dir+'/Inputs/SysTreeProjectors/PDF*/*.root'
                    #     ])),
                    # sensitivity.mk_tc('LimitsSystAllSigCorr', mk_limit_list_syst([
                    #     output_dir+'/Inputs/SysTreeProjectors/*/*.root',
                    #     ])),
                    # sensitivity.mk_tc('LimitsSystNoUncert', mk_limit_list_syst()),
                    # sensitivity.mk_tc('LimitsCheck', limit_tcs.mk_limit_list_check_ak8clean), # , output_dir+'/Inputs/SysTreeProjectors/*/*.root'
                ]
            ),
            # mk_tex_tc_post(output_dir+'/Histograms/')(), 
            varial.tools.WebCreator(),
            git.GitTagger(commit_prefix='In {0}'.format(output_dir)),

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