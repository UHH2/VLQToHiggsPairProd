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

tptp_datasets_loose = [
    # 'Run2015D_Ele',
    # 'Run2015D_Mu',
    # 'Run2015D_Had',
    # 'TpTp_M-700',
    # 'TpTp_M-800',
    # 'TpTp_M-900',
    # 'TpTp_M-1000',
    # 'TpTp_M-1100',
    # 'TpTp_M-1200',
    # 'TpTp_M-1300',
    # 'TpTp_M-1400',
    # 'TpTp_M-1500',
    # 'TpTp_M-1600',
    # 'TpTp_M-1700',
    # 'TpTp_M-1800',
    # 'QCD_Pt80to120_MuEnr',
    # 'QCD_Pt120to170_MuEnr',
    # 'QCD_Pt170to300_MuEnr',
    # 'QCD_Pt300to470_MuEnr',
    # 'QCD_Pt470to600_MuEnr',
    # 'QCD_Pt600to800_MuEnr',
    # 'QCD_Pt800to1000_MuEnr',
    # 'QCD_Pt1000toInf_MuEnr',
    # 'TTbar',
    # 'TTbar_Mtt0to700',
    # 'TTbar_Mtt700to1000',
    # 'TTbar_Mtt1000toInf',
    # 'WJets',
    # 'DYJetsToLL_HT100to200',
    # 'DYJetsToLL_HT200to400',
    # 'DYJetsToLL_HT400to600',
    # 'DYJetsToLL_HT600toInf',
    # 'WJets_LNu_HT100To200',
    # 'WJets_LNu_HT200To400',
    'WJets_LNu_HT400To600',
    'WJets_LNu_HT600To800',
    'WJets_LNu_HT800To1200',
    'WJets_LNu_HT1200To2500',
    'WJets_LNu_HT2500ToInf',
    'SingleT_tChannel',
    'SingleT_WAntitop',
    'SingleT_WTop',
    'SingleT_sChannel',
]

tptp_datasets_tight = [
    # 'Run2015D_Ele',
    'Run2015D_Mu',
    # 'Run2015D_Had',
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
    'QCD_Pt80to120_MuEnr',
    'QCD_Pt120to170_MuEnr',
    'QCD_Pt170to300_MuEnr',
    'QCD_Pt300to470_MuEnr',
    'QCD_Pt470to600_MuEnr',
    'QCD_Pt600to800_MuEnr',
    'QCD_Pt800to1000_MuEnr',
    'QCD_Pt1000toInf_MuEnr',
    'TTbar',
    # 'TTbar_Mtt0to700',
    # 'TTbar_Mtt700to1000',
    # 'TTbar_Mtt1000toInf',
    # 'WJets',
    'DYJetsToLL_HT100to200',
    'DYJetsToLL_HT200to400',
    'DYJetsToLL_HT400to600',
    'DYJetsToLL_HT600toInf',
    'WJets_LNu_HT100To200',
    'WJets_LNu_HT200To400',
    'WJets_LNu_HT400To600',
    'WJets_LNu_HT600To800',
    'WJets_LNu_HT800To1200',
    'WJets_LNu_HT1200To2500',
    'WJets_LNu_HT2500ToInf',
    'SingleT_tChannel',
    'SingleT_WAntitop',
    'SingleT_WTop',
    'SingleT_sChannel',
]

tptp_datasets_final = [
    # 'Run2015D_Ele',
    'Run2015D_Mu',
    # 'Run2015D_Had',
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
    'QCD_Pt80to120_MuEnr',
    'QCD_Pt120to170_MuEnr',
    'QCD_Pt170to300_MuEnr',
    'QCD_Pt300to470_MuEnr',
    'QCD_Pt470to600_MuEnr',
    'QCD_Pt600to800_MuEnr',
    'QCD_Pt800to1000_MuEnr',
    'QCD_Pt1000toInf_MuEnr',
    'TTbar',
    # 'TTbar_Mtt0to700',
    # 'TTbar_Mtt700to1000',
    # 'TTbar_Mtt1000toInf',
    # 'WJets',
    'DYJetsToLL_HT100to200',
    'DYJetsToLL_HT200to400',
    'DYJetsToLL_HT400to600',
    'DYJetsToLL_HT600toInf',
    'WJets_LNu_HT100To200',
    'WJets_LNu_HT200To400',
    'WJets_LNu_HT400To600',
    'WJets_LNu_HT600To800',
    'WJets_LNu_HT800To1200',
    'WJets_LNu_HT1200To2500',
    'WJets_LNu_HT2500ToInf',
    'SingleT_tChannel',
    'SingleT_WAntitop',
    'SingleT_WTop',
    'SingleT_sChannel',
]

signal_regions_final = [
    # 'SignalRegion_0HiggsTags2addBtags',
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

    

if str(sys.argv[1]) == 'pre':
    mod_name='TpTpPreSelection'
    tc_list.append(
        tptppreselection.mk_sframe_and_plot_tools(
            version='FilesAndPlots_v0',
            allowed_datasets=tptp_datasets_tight
        ),
    )
elif str(sys.argv[1]) == 'loose':
    mod_name='TpTpLooseSelection'
    tc_list.append(
        tptplooseselection.mk_sframe_and_plot_tools(
            version='FilesAndPlots_v5_muonId',
            count=count,
            allowed_datasets=tptp_datasets_loose
        ),
    )
elif str(sys.argv[1]) == 'tight':
    mod_name='TpTpTightSelectionRunII'
    tc_list.append(
        tptptightselection.mk_sframe_and_plot_tools(
            version='FilesAndPlots_v6',
            count=count,
            allowed_datasets=tptp_datasets_tight
        ),
    )
elif str(sys.argv[1]) == 'final':
    mod_name='TpTpFinalSelectionRunII'
    tc_list.append(
        tptpfinalselection.mk_sframe_and_plot_tools(
            analysis_module='TpTpFinalSelectionRunII',
            version='FilesAndPlots_v6',
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
            version='FilesAndPlots_v20',
            count=count,
            allowed_datasets=tptp_datasets_final,
            signal_regions=signal_regions_control,
            control_regions=control_regions
        ),
    )
else:
    print "Wrong argment!"
    raise(RuntimeError)

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