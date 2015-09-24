from common_sframe import *
from varial.extensions.sframe import SFrame
import varial.tools
import tight_plot
import compare_crs
import sensitivity


tptp_tight_datasets = [
    'Run2015B_Ele',
    'Run2015B_Mu',
    'Run2015B_Had',
    # 'TpTp_M-700',
    'TpTp_M-800',
    # 'TpTp_M-900',
    # 'TpTp_M-1000',
    # 'TpTp_M-1100',
    # 'TpTp_M-1200',
    # 'TpTp_M-1300',
    # 'TpTp_M-1400',
    # 'TpTp_M-1500',
    'TpTp_M-1600',
    # 'TpTp_M-1700',
    # 'TpTp_M-1800',
    # 'QCD_Pt15to30',
    # 'QCD_Pt30to50',
    # 'QCD_Pt50to80',
    # 'QCD_Pt80to120',
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

# def mk_sframe_and_plot_tools(catname):
#     """Makes a toolchain for one category with sframe and plots."""
#     sframe = SFrame(
#         cfg_filename=sframe_cfg,
#         xml_tree_callback=set_category_datasets_and_eventnumber(catname, count="-1", allowed_datasets=tptp_tight_datasets), # 
#     )
#     plots = varial.tools.ToolChainParallel(
#         'Plots',
#         lazy_eval_tools_func=lambda: tight_plot.mk_tools()
#     )
#     tc = varial.tools.ToolChain(
#         catname,
#         [
#             sframe,
#             plots
#         ]
#     )
#     return tc

# sframe_tools = varial.tools.ToolChain(
#     'EventLoopAndPlots_v0',
#     [
#         mk_sframe_and_plot_tools('SoftDropCat1htag0btag'),
#         mk_sframe_and_plot_tools('SoftDropCat1htag1btag'),
#         # mk_sframe_and_plot_tools('SoftDropCat1htag2plusbtag'),
#         mk_sframe_and_plot_tools('SoftDropCat0htag2plusbtag'),
#         # mk_sframe_and_plot_tools('SoftDropCat2htag')
#     ]
# )

sframe_cfg = '/nfs/dust/cms/user/nowatsd/sFrameNew/CMSSW_7_4_7/src/UHH2/VLQToHiggsPairProd/config/TpTpTightSelection.xml'

signal_regions_final = [
    'SignalRegion_0HiggsTags2addBtags',
    'SignalRegion_1HiggsTag0addBtags',
    'SignalRegion_1HiggsTag1addBtags',
    'SignalRegion_1HiggsTag2addBtags'
]


def mk_sframe_and_plot_tools_final_new():
    """Makes a toolchain for one category with sframe and plots."""
    sframe = SFrame(
        cfg_filename=sframe_cfg,
        xml_tree_callback=set_category_datasets_eventnumber_and_split(
            catname=' '.join(signal_regions_final),
            count="-1", allowed_datasets=tptp_tight_datasets
        ), # 
    )
    plots = varial.tools.ToolChainParallel(
        'Plots',
        lazy_eval_tools_func=tight_plot.mk_tools_cats(signal_regions_final)
    )
    tc = varial.tools.ToolChain(
        'FilesAndPlots_v0',
        [
            sframe,
            # plots,
            # varial.tools.ToolChain(
            #     'CompareControlRegion',
            #     lazy_eval_tools_func=compare_crs.mk_tc(srs=signal_regions_final, crs=control_regions)
            #     ),
            sensitivity.mk_tc(),
            varial.tools.WebCreator(no_tool_check=True)
        ]
    )
    return tc

sframe_tools_final = mk_sframe_and_plot_tools_final_new()

# for control regions:

sframe_cfg_control_region = '/nfs/dust/cms/user/nowatsd/sFrameNew/CMSSW_7_4_7/src/UHH2/VLQToHiggsPairProd/config/TpTpControlRegion.xml'

signal_regions = [
    '1HiggsLooseTagSignalRegion',
    '1BoostHiggsLooseTagSignalRegion',
    '1HiggsMedTagSignalRegion',
] # , '1HiggsLooseTagSignalRegion'

control_regions = [
    '1AntiHTBVeto',    
    '1BoostAntiHTBVeto',
    '1BoostAntiHTBVetoHighMass',
    '1AntiHTMassInvert1BTag',
    '1AntiHTMassInvert0BTag',
    '1BoostAntiHTMassInvert1BTag',
    '1BoostAntiHTMassInvert0BTag',
    # '0HiggsMedTagSideBandRegion'
]


def mk_sframe_and_plot_tools_control_region_new():
    """Makes a toolchain for one category with sframe and plots."""
    sframe = SFrame(
        cfg_filename=sframe_cfg_control_region,
        xml_tree_callback=set_category_datasets_eventnumber_and_split(
            catname=' '.join(signal_regions+control_regions),
            count="-1", allowed_datasets=tptp_tight_datasets
        ), # 
    )
    plots = varial.tools.ToolChainParallel(
        'Plots',
        lazy_eval_tools_func=tight_plot.mk_tools_cats(signal_regions+control_regions)
    )
    tc = varial.tools.ToolChain(
        'FilesAndPlots_v14_moreCrs',
        [
            sframe,
            plots,
            varial.tools.ToolChain(
                'CompareControlRegion',
                lazy_eval_tools_func=compare_crs.mk_tc(srs=signal_regions, crs=control_regions)
                ),
            varial.tools.WebCreator(no_tool_check=True)
        ]
    )
    return tc

sframe_tools_control_region = mk_sframe_and_plot_tools_control_region_new()


# to test QCD:

# sframe_cfg_qcd_test = '/nfs/dust/cms/user/nowatsd/sFrameNew/CMSSW_7_4_7/src/UHH2/VLQToHiggsPairProd/config/TpTpTestQCD.xml'

# def mk_sframe_and_plot_tools_qcd_test(catname):
#     """Makes a toolchain for one category with sframe and plots."""
#     sframe = SFrame(
#         cfg_filename=sframe_cfg_qcd_test,
#         xml_tree_callback=set_category_datasets_and_eventnumber(catname, count="-1", allowed_datasets=tptp_tight_datasets), # 
#     )
#     plots = varial.tools.ToolChainParallel(
#         'Plots',
#         lazy_eval_tools_func=lambda: tight_plot.mk_tools()
#     )
#     tc = varial.tools.ToolChain(
#         catname,
#         [
#             sframe,
#             plots
#         ]
#     )
#     return tc

# sframe_tools_qcd_test = varial.tools.ToolChain(
#     'EventLoopAndPlots_v4_after_corrected_preselection',
#     [
#         mk_sframe_and_plot_tools_qcd_test('RejectQCD'),
#         mk_sframe_and_plot_tools_qcd_test('EnrichQCD'),
#         # mk_sframe_and_plot_tools_qcd_test('NoSelectionNoPrimLepPtReq'),
#         # mk_sframe_and_plot_tools_qcd_test('NoSelectionWithPrimLepPtReq')
#         mk_sframe_and_plot_tools_qcd_test('RejectQCDOnlyMuons'),
#     ]
# )