from common_sframe import *
from varial.extensions.sframe import SFrame
import varial.tools
import loose_plot

sframe_cfg = '/nfs/dust/cms/user/nowatsd/sFrameNew/CMSSW_7_4_7/src/UHH2/VLQToHiggsPairProd/config/TpTpLooseSelection.xml'

tptp_loose_datasets = [
    'Run2015B_Ele',
    'Run2015B_Mu',
    'Run2015B_Had',
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
    'TTbar',
    'WJets',
    'ZJetsM10to50',
    'ZJetsM50toInf',
    'SingleT_tChannel',
    'SingleT_WAntitop',
    'SingleT_WTop',
]

def mk_sframe_and_plot_tools():
    """Makes a toolchain for one category with sframe and plots."""
    sframe = SFrame(
        cfg_filename=sframe_cfg,
        xml_tree_callback=set_eventnumber_and_datasets(count="-1", allowed_datasets=tptp_loose_datasets), # 
    )
    plots = varial.tools.ToolChainParallel(
        'Plots',
        lazy_eval_tools_func=lambda: loose_plot.mk_tools()
    )
    tc = varial.tools.ToolChain(
        "EventLooptAndPlots_v1",
        [
            sframe,
            plots
        ]
    )
    return tc

sframe_tools = mk_sframe_and_plot_tools()