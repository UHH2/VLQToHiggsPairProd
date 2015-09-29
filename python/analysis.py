#!/usr/bin/env python


# import UHH2.VLQSemiLepPreSel.vlq_settings as vlq_settings
# import UHH2.VLQSemiLepPreSel.common as common
import tptpfinalselection
import tptplooseselection
import tptptightselection
import tptppreselection
# import sensitivity
# import tex_content

import varial.tools
import varial.extensions.git as git
import varial.extensions.make as make
import os
import sys

import tptp_settings

# varial.settings.use_parallel_chains = False

# mod_name = 'TpTpLooseSelection'
# mod_name = 'TpTpControlRegion'
# mod_name = 'TpTpTightSelectionRunII'
uhh_base = os.getenv('CMSSW_BASE') + '/src/UHH2/'

version = 'FilesAndPlots_v0'
count = -1

tptp_datasets_final = [
    # 'Run2015B_Ele',
    'Run2015B_Mu',
    # 'Run2015B_Had',
    # 'TpTp_M-700',
    'TpTp_M-800',
    'TpTp_M-900',
    'TpTp_M-1000',
    'TpTp_M-1100',
    # 'TpTp_M-1200',
    'TpTp_M-1300',
    # 'TpTp_M-1400',
    # 'TpTp_M-1500',
    'TpTp_M-1600',
    # 'TpTp_M-1700',
    # 'TpTp_M-1800',
    # 'QCD_Pt15to30',
    # 'QCD_Pt30to50',
    # 'QCD_Pt50to80',
    # 'QCD_Pt80to120',
    # 'QCD_Pt120to170',
    # 'QCD_Pt170to300',
    'QCD_Pt300to470',
    'QCD_Pt470to600',
    'QCD_Pt600to800',
    'QCD_Pt800to1000',
    'QCD_Pt1000to1400',
    'QCD_Pt1400to1800',
    'QCD_Pt1800to2400',
    # 'QCD_Pt2400to3200',
    'QCD_Pt3200toInf',
    # 'TTbar',
    'TTbar_Mtt0to700',
    'TTbar_Mtt700to1000',
    'TTbar_Mtt1000toInf',
    'WJets',
    # 'ZJetsM10to50',
    'ZJetsM50toInf',
    'SingleT_tChannel',
    'SingleT_WAntitop',
    'SingleT_WTop',
]

tptp_datasets_tight = [
    'Run2015B_Ele',
    'Run2015B_Mu',
    'Run2015B_Had',
    # 'TpTp_M-700',
    'TpTp_M-800',
    'TpTp_M-900',
    'TpTp_M-1000',
    'TpTp_M-1100',
    # 'TpTp_M-1200',
    'TpTp_M-1300',
    # 'TpTp_M-1400',
    # 'TpTp_M-1500',
    'TpTp_M-1600',
    # 'TpTp_M-1700',
    # 'TpTp_M-1800',
    # 'QCD_Pt15to30',
    # 'QCD_Pt30to50',
    # 'QCD_Pt50to80',
    'QCD_Pt80to120',
    'QCD_Pt120to170',
    'QCD_Pt170to300',
    'QCD_Pt300to470',
    'QCD_Pt470to600',
    'QCD_Pt600to800',
    'QCD_Pt800to1000',
    'QCD_Pt1000to1400',
    'QCD_Pt1400to1800',
    'QCD_Pt1800to2400',
    'QCD_Pt2400to3200',
    'QCD_Pt3200toInf',
    # 'TTbar',
    'TTbar_Mtt0to700',
    'TTbar_Mtt700to1000',
    'TTbar_Mtt1000toInf',
    'WJets',
    'ZJetsM10to50',
    'ZJetsM50toInf',
    'SingleT_tChannel',
    'SingleT_WAntitop',
    'SingleT_WTop',
]

signal_regions_final = [
    'SignalRegion_0HiggsTags2addBtags',
    'SignalRegion_1HiggsTag0addBtags',
    'SignalRegion_1HiggsTag1addBtags',
    'SignalRegion_1HiggsTag2addBtags'
]

signal_regions_control = [
    'SignalRegionHLooseBoost',
    'SignalRegionHMedBoost',
    # 'SignalRegionHMed',
] # , '1HiggsLooseTagSignalRegion'

control_regions = [
    'ControlRegionBVetoBoostLoose',    
    'ControlRegionMassInvert1BTagBoostLoose',
    # '1BoostAntiHTBVetoHighMass',
    'ControlRegionMassInvert0BTagBoostLoose',
    'ControlRegionBVetoBoostMed',
    'ControlRegionMassInvert1BTagBoostMed',
    'ControlRegionMassInvert0BTagBoostMed',
    # '0HiggsMedTagSideBandRegion'
]

tc_list = [
    make.Make([
       uhh_base + 'core',
       uhh_base + 'common',
       uhh_base + 'VLQSemiLepPreSel',
       uhh_base + 'VLQToHiggsPairProd',
    ]),
    # # varial.tools.UserInteraction('Really run sframe? (Kill me otherwise.)'),
    git.GitAdder(),    
]

if len(sys.argv) < 2:
    print "ERROR not enough arguments for analysis.py!"

    

if str(sys.argv[1]) == 'loose':
    mod_name='TpTpLooseSelection'
    tc_list.append(
        tptplooseselection.mk_sframe_and_plot_tools(
            version='FilesAndPlots_v3_exclTTbar_splitSignal',
            count=count,
            allowed_datasets=tptp_datasets
        ),
    )
elif str(sys.argv[1]) == 'pre':
    mod_name='TpTpPreSelection'
    tc_list.append(
        tptppreselection.mk_sframe_and_plot_tools(
            version='FilesAndPlots_v0',
            allowed_datasets=tptp_datasets_tight
        ),
    )
elif str(sys.argv[1]) == 'tight':
    mod_name='TpTpTightSelectionRunII'
    tc_list.append(
        tptptightselection.mk_sframe_and_plot_tools(
            version='FilesAndPlots_v2_withPtPlots',
            count=count,
            allowed_datasets=tptp_datasets_tight
        ),
    )
elif str(sys.argv[1]) == 'final':
    mod_name='TpTpFinalSelectionRunII'
    tc_list.append(
        tptpfinalselection.mk_sframe_and_plot_tools(
            analysis_module='TpTpFinalSelectionRunII',
            version='FilesAndPlots_v3_higgsUpperM150',
            count=count,
            allowed_datasets=tptp_datasets_final,
            signal_regions=signal_regions_final,
        ),
    )
elif str(sys.argv[1]) == 'control':
    mod_name='TpTpControlRegion'
    tc_list.append(
        tptpfinalselection.mk_sframe_and_plot_tools(
            analysis_module='TpTpControlRegion',
            version='FilesAndPlots_v17_morePlots',
            count=count,
            allowed_datasets=tptp_datasets_final,
            signal_regions=signal_regions_control,
            control_regions=control_regions
        ),
    )

tc_list.append(
    # git.GitAdder(),
    git.GitTagger(),
    )

tc = varial.tools.ToolChain(
    mod_name,
    tc_list
)


# varial.settings.max_num_processes = 1
varial.settings.try_reuse_results = True
varial.tools.Runner(tc, default_reuse=True)
# import varial.main
# varial.main.main(toolchain=tc, try_reuse_results=True)