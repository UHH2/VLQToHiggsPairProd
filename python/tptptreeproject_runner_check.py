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
import tptpsframe_runner as sframe
from varial.extensions import git


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
import tex_content

# hadd = Hadd(
#     input_pat, 
#     common_plot.basenames, 
#     add_aliases_to_analysis=False,
#     samplename_func=vlq_common.get_samplename
# )


varial.settings.pretty_names.update({
    # 'LimitEl45Only' : 'ElectronOnly',
    'LimitMu45Only' : 'MuonOnly',
    'LimitNoDRCut' : 'NoDRCut',
    'LimitWithDRCut' : 'WithDRCut',
    'LimitNoIso' : 'NoIso',
    'LimitWithIso' : 'WithIso',
    'LimitNoWJets' : 'NoWJets',
    'LimitWithWJets' : 'WithWJets',
    'LimitNoClean' : 'No Ak8 Cleaning',
    'LimitWithClean' : 'With Ak8 Cleaning',
    'LimitCombinedChannels' : 'CombinedChannels',
})

varial.settings.colors.update({
    'LimitEl45Only' : 1,
    'LimitMu45Only' : 1,
    'LimitCombinedChannels' : 4,
    'LimitNoDRCut' : 3,
    'LimitWithDRCut' : 4,
    'LimitNoIso' : 1,
    'LimitWithIso' : 4,
    'LimitNoWJets' : 3,
    'LimitWithWJets' : 4,
    'LimitNoClean' : 3,
    'LimitWithClean' : 4,
})


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


varial.settings.asymptotic = True
varial.settings.merge_decay_channels = False

#!/usr/bin/env python

baseline_selection = [
    'gendecay_accept        == 1',
]

# final regions

sr2b_channel = baseline_selection + [
    'n_higgs_tags_2b_med    >= 1',
    # 'n_additional_btags_medium  >= 1',
]

sr1b_channel = baseline_selection + [
    'n_higgs_tags_2b_med    == 0',
    'n_higgs_tags_1b_med    >= 1',
    # 'n_additional_btags_medium  >= 1',
]

sb_channel = baseline_selection + [
    'n_higgs_tags_1b_med        == 0',
    # 'n_additional_btags_medium  >= 1',
]

# cleaned selections

sr2b_channel_clean = baseline_selection + [
    'n_ak8_cleaned_dr          >= 2',
    'n_higgs_tags_2b_med_cleaned_dr    >= 1',
    # 'n_additional_btags_medium  >= 1',
]

sr1b_channel_clean = baseline_selection + [
    'n_ak8_cleaned_dr          >= 2',
    'n_higgs_tags_2b_med_cleaned_dr    == 0',
    'n_higgs_tags_1b_med_cleaned_dr    >= 1',
    # 'n_additional_btags_medium  >= 1',
]

sb_channel_clean = baseline_selection + [
    'n_ak8_cleaned_dr          >= 2',
    'n_higgs_tags_1b_med_cleaned_dr    == 0',
    # 'n_additional_btags_medium  >= 1',
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

# final regions for analysis

final_regions = (
    ('BaseLineSelectionEl45', el_channel),
    ('BaseLineSelectionMu45', mu_channel),
    ('SignalRegion2b_El45', sr2b_channel + el_channel),
    ('SignalRegion1b_El45', sr1b_channel + el_channel),
    ('SidebandRegion_El45', sb_channel + el_channel),
    ('SignalRegion2b_Mu45', sr2b_channel + mu_channel),
    ('SignalRegion1b_Mu45', sr1b_channel + mu_channel),
    ('SidebandRegion_Mu45', sb_channel + mu_channel),
    ('SignalRegion2bClean_El45', sr2b_channel_clean + el_channel),
    ('SignalRegion1bClean_El45', sr1b_channel_clean + el_channel),
    ('SidebandRegionClean_El45', sb_channel_clean + el_channel),
    ('SignalRegion2bClean_Mu45', sr2b_channel_clean + mu_channel),
    ('SignalRegion1bClean_Mu45', sr1b_channel_clean + mu_channel),
    ('SidebandRegionClean_Mu45', sb_channel_clean + mu_channel),
)

def mk_limit_list_check_ak8clean():
    limit_list = []
    for ind, brs_ in enumerate(sensitivity.br_list):
        # if ind > 2: break
        tc = []
        tc.append(varial.tools.ToolChain(
            'NoClean',
            sensitivity.mk_limit_tc(brs_, sensitivity.select_files([
                "SignalRegion2b_Mu45",
                "SignalRegion1b_Mu45",
                "SidebandRegion_Mu45",
                "SignalRegion2b_El45",
                "SignalRegion1b_El45",
                "SidebandRegion_El45",
                ],
                'ST'),
            name='NoClean', sys_pat=''))
        )
        tc.append(varial.tools.ToolChain(
            'WithClean',
            sensitivity.mk_limit_tc(brs_, sensitivity.select_files([
                "SignalRegion2bClean_Mu45",
                "SignalRegion1bClean_Mu45",
                "SidebandRegionClean_Mu45",
                "SignalRegion2bClean_El45",
                "SignalRegion1bClean_El45",
                "SidebandRegionClean_El45",
                ],
                'ST'),
            name='WithClean', sys_pat=''))
        )
        limit_list.append(
            varial.tools.ToolChainParallel('Limit'+str(ind),tc))
    return limit_list

def run_treeproject_and_plot(base_path, output_dir):
    tc = varial.tools.ToolChain(
        output_dir,
        [
            # varial.extensions.make.Make([
            #     uhh_base + 'core',
            #     uhh_base + 'common',
            #     uhh_base + 'VLQSemiLepPreSel',
            #     uhh_base + 'VLQToHiggsAndLepton',
            # ]),
            # varial.tools.UserInteraction('Really run sframe? (Kill me otherwise.)'),
            # sframe_tools.sframe_tools,
            git.GitAdder(),
            varial.tools.ToolChain(
                'Inputs', [
                    treeproject_tptp.mk_tp(base_path, final_regions),
                    # treeproject_tptp.mk_sys_tps(base_path),
                    # hadd,
                ]
            ),
            varial.tools.ToolChain(
                'Histograms',
                [
                    plot.mk_toolchain('HistogramsOnlyPdf', [output_dir+'/Inputs/TreeProjector/*.root'], None, plot.samples_to_plot_final),
                    # sensitivity.mk_tc('LimitsSyst', mk_limit_list_syst(output_dir+'/Inputs/SysTreeProjectors/*/*.root')), # , output_dir+'/Inputs/SysTreeProjectors/*/*.root'
                    sensitivity.mk_tc('LimitsCheck', mk_limit_list_check_ak8clean), # , output_dir+'/Inputs/SysTreeProjectors/*/*.root'
                ]
                # [
                #     plot.mk_toolchain('Selections', '%s/Inputs/TreeProjector/*.root' % dir_name),
                #     # plot.mk_toolchain('SFramePlots', '%s/Inputs/Hadd/*.root' % dir_name, cutflow=True),
                #     # sideband_overlays.tc,
                #     # sensitivity.tc,
                # ]
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