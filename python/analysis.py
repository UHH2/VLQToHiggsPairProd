#!/usr/bin/env python


# import UHH2.VLQSemiLepPreSel.vlq_settings as vlq_settings
# import UHH2.VLQSemiLepPreSel.common as common
import tptpfinalselection
import tptplooseselection
# import sensitivity
# import tex_content

import varial.tools
import varial.extensions.git as git
import varial.extensions.make as make
import os

import tptp_settings

# varial.settings.use_parallel_chains = False

# mod_name = 'TpTpLooseSelection'
mod_name = 'TpTpControlRegion'
# mod_name = 'TpTpFinalSelectionRunII'
uhh_base = os.getenv('CMSSW_BASE') + '/src/UHH2/'

version = 'FilesAndPlots_v15_morePlots'
count = -1

signal_regions_final = [
    'SignalRegion_0HiggsTags2addBtags',
    'SignalRegion_1HiggsTag0addBtags',
    'SignalRegion_1HiggsTag1addBtags',
    'SignalRegion_1HiggsTag2addBtags'
]

signal_regions_control = [
    'SignalRegionHLoose',
    'SignalRegionHLooseBoost',
    'SignalRegionHMed',
] # , '1HiggsLooseTagSignalRegion'

control_regions = [
    'ControlRegionBVeto',    
    'ControlRegionBVetoBoost',
    # '1BoostAntiHTBVetoHighMass',
    'ControlRegionMassInvert1BTag',
    'ControlRegionMassInvert0BTag',
    'ControlRegionMassInvert1BTagBoost',
    'ControlRegionMassInvert0BTagBoost',
    # '0HiggsMedTagSideBandRegion'
]

tc = varial.tools.ToolChain(
    mod_name,
    [
        # make.Make([
        #    uhh_base + 'core',
        #    uhh_base + 'common',
        #    uhh_base + 'VLQSemiLepPreSel',
        #    uhh_base + 'VLQToHiggsPairProd',
        # ]),
        # # varial.tools.UserInteraction('Really run sframe? (Kill me otherwise.)'),
        tptpfinalselection.mk_sframe_and_plot_tools(
            analysis_module=mod_name,
            version=version,
            count=count,
            signal_regions=signal_regions_control,
            control_regions=control_regions
        ),
        # tptplooseselection.mk_sframe_and_plot_tools(
        #     # analysis_module=mod_name,
        #     version=version,
        #     count=count,
        #     # signal_regions=signal_regions_final
        # ),
        git.GitAdder(),
        git.GitTagger(),
        # varial.tools.CopyTool('~/www/test'),
    ]
)


# varial.settings.max_num_processes = 1
varial.settings.try_reuse_results = True
varial.tools.Runner(tc, default_reuse=True)
# import varial.main
# varial.main.main(toolchain=tc, try_reuse_results=True)