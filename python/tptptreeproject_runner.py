#!/usr/bin/env python

import UHH2.VLQSemiLepPreSel.vlq_settings as vlq_settings
import UHH2.VLQSemiLepPreSel.common as vlq_common
from varial.extensions.hadd import Hadd
import varial.extensions.make
import varial.tools
import os
import sys

import common_plot
import tptpfinalselection_plot as plot

# varial.settings.max_num_processes = 1

if len(sys.argv) < 2:
    print 'Provide output dir!'
    exit(-1)

dir_name = sys.argv[1]
uhh_base = os.getenv('CMSSW_BASE') + '/src/UHH2/'
input_pat = '/nfs/dust/cms/user/nowatsd/sFrameNew/'\
    'RunII-25ns-v2/CMSSW_7_4_15_patch1/src/UHH2/VLQToHiggsPairProd/'\
    'Samples-25ns-v2/TpTpFinalSelectionTreeOutput-v0wBTagSF/Files_and_Plots/'\
    'Files_and_Plots_nominal/SFrame/nominal/workdir/uhh2.AnalysisModuleRunner.*.root'

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


hadd = Hadd(
    input_pat, 
    common_plot.basenames, 
    add_aliases_to_analysis=False,
    samplename_func=vlq_common.get_samplename
)


tc = varial.tools.ToolChain(
    dir_name,
    [
        # varial.extensions.make.Make([
        #     uhh_base + 'core',
        #     uhh_base + 'common',
        #     uhh_base + 'VLQSemiLepPreSel',
        #     uhh_base + 'VLQToHiggsAndLepton',
        # ]),
        # varial.tools.UserInteraction('Really run sframe? (Kill me otherwise.)'),
        # sframe_tools.sframe_tools,
        
        varial.tools.ToolChain(
            'Inputs', [
                tptp_treeproject.mk_tp(input_pat),
                tptp_treeproject.mk_sys_tps(),
                # hadd,
            ]
        ),
        varial.tools.ToolChainParallel(
            'Histograms',
            [
                plot.mk_toolchain('Histograms', dir_name+'/Inputs/TreeProjector/*.root'),
                sensitivity.mk_limit_chain('Ind_Limits', dir_name+'/Inputs/SysTreeProjectors/*/*.root'), # 
            ]
            # [
            #     plot.mk_toolchain('Selections', '%s/Inputs/TreeProjector/*.root' % dir_name),
            #     # plot.mk_toolchain('SFramePlots', '%s/Inputs/Hadd/*.root' % dir_name, cutflow=True),
            #     # sideband_overlays.tc,
            #     # sensitivity.tc,
            # ]
        ),

        # varial.tools.PrintToolTree(),
        varial.tools.WebCreator(),
        # tex_content.tc,
        # varial.tools.CopyTool('~/www/auth/VLQ2HT', use_rsync=True),
    ]
)


varial.settings.try_reuse_results = True
# varial.settings.rootfile_postfixes += ['.pdf']
# varial.tools.Runner(tc, True)
import varial.main
varial.main.main(toolchain=tc)