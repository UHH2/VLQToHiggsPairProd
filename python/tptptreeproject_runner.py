#!/usr/bin/env python

import UHH2.VLQSemiLepPreSel.vlq_settings as vlq_settings
import UHH2.VLQSemiLepPreSel.common as vlq_common
from varial.extensions.hadd import Hadd
import varial.extensions.make
import varial.tools
import os
import sys

import common_plot
import plot as plot
import tptpsframe_runner as sframe
from varial.extensions import git


varial.settings.max_num_processes = 24

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
import tptp_treeproject
import sensitivity
# import tex_content


# hadd = Hadd(
#     input_pat, 
#     common_plot.basenames, 
#     add_aliases_to_analysis=False,
#     samplename_func=vlq_common.get_samplename
# )


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
                    tptp_treeproject.mk_tp(base_path),
                    # tptp_treeproject.mk_sys_tps(base_path),
                    # hadd,
                ]
            ),
            varial.tools.ToolChainParallel(
                'Histograms',
                [
                    plot.mk_toolchain('Histograms', output_dir+'/Inputs/TreeProjector/*.root', None),
                    sensitivity.mk_tc('Limits'), # , output_dir+'/Inputs/SysTreeProjectors/*/*.root'
                ]
                # [
                #     plot.mk_toolchain('Selections', '%s/Inputs/TreeProjector/*.root' % dir_name),
                #     # plot.mk_toolchain('SFramePlots', '%s/Inputs/Hadd/*.root' % dir_name, cutflow=True),
                #     # sideband_overlays.tc,
                #     # sensitivity.tc,
                # ]
            ),
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