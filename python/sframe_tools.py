
from varial.extensions.sframe import SFrame
import varial.tools
import plot_loose
import plot_tight

sframe_cfg_test = '/nfs/dust/cms/user/nowatsd/sFrameNew/CMSSW_7_4_7/src/UHH2/VLQToHiggsPairProd/config/TestNewFormat.xml'
sframe_cfg_loose = '/nfs/dust/cms/user/nowatsd/sFrameNew/CMSSW_7_4_7/src/UHH2/VLQToHiggsPairProd/config/TpTpLooseSelection.xml'
sframe_cfg_tight = '/nfs/dust/cms/user/nowatsd/sFrameNew/CMSSW_7_4_7/src/UHH2/VLQToHiggsPairProd/config/TpTpTightSelection.xml'

tptp_loose_datasets = [
    'Run2015B_Ele',
    'Run2015B_Mu',
    # 'TpTp_M-700',
    'TpTp_M-800',
    # 'TpTp_M-900',
    # 'TpTp_M-1000',
    # 'TpTp_M-1100',
    # 'TpTp_M-1200',
    'TpTp_M-1300',
    # 'TpTp_M-1400',
    # 'TpTp_M-1500',
    # 'TpTp_M-1600',
    # 'TpTp_M-1700',
    'TpTp_M-1800',
    'QCD_Pt15to30',
    'QCD_Pt30to50',
    'QCD_Pt50to80',
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

def do_set_cat(element_tree, catname):
    user_config = element_tree.getroot().find('Cycle').find('UserConfig')
    for item in user_config:
        if item.get('Name') == 'category':
            item.set('Value', catname)
            break

def do_set_eventnumber(element_tree, count):
    input_data = element_tree.getroot().find('Cycle').findall('InputData')
    for attr in input_data:
        attr.set('NEventsMax', count)

def clean_input_data(element_tree, allowed_datasets):
    tree_cycle = element_tree.getroot().find('Cycle')
    for item in tree_cycle.findall('InputData'):
        if item.get('Version') not in allowed_datasets:
            tree_cycle.remove(item)




def set_category_and_eventnumber(catname, count ="1000"):
    def tmp_func(element_tree):
        do_set_cat(element_tree, catname)
        do_set_eventnumber(element_tree, count)
    return tmp_func

def set_eventnumber(count="-1"):
    def tmp_func(element_tree):
        do_set_eventnumber(element_tree, count)
    return tmp_func

def set_eventnumber_and_datasets(count='-1', allowed_datasets=None):
    def tmp_func(element_tree):
        clean_input_data(element_tree, allowed_datasets)
        do_set_eventnumber(element_tree, count)
    return tmp_func




def mk_sframe_and_plot_tools_tight(catname):
    """Makes a toolchain for one category with sframe and plots."""
    sframe = SFrame(
        cfg_filename=sframe_cfg_tight,
        xml_tree_callback=set_category_and_eventnumber(catname, count="1000"), # 
    )
    plots = varial.tools.ToolChainParallel(
        'Plots',
        lazy_eval_tools_func=lambda: plot_tight.mk_tools()
    )
    tc = varial.tools.ToolChain(
        catname,
        [
            sframe,
            plots
        ]
    )
    return tc

def mk_sframe_and_plot_tools_loose():
    """Makes a toolchain for one category with sframe and plots."""
    sframe = SFrame(
        cfg_filename=sframe_cfg_loose,
        xml_tree_callback=set_eventnumber_and_datasets(count="100", allowed_datasets=tptp_loose_datasets), # 
    )
    plots = varial.tools.ToolChainParallel(
        'Plots4',
        lazy_eval_tools_func=lambda: plot_loose.mk_tools()
    )
    tc = varial.tools.ToolChain(
        "EventLooptAndPlots",
        [
            # sframe,
            plots
        ]
    )
    return tc

sframe_tools_tight = varial.tools.ToolChain(
    'EventLoopAndPlots',
    [
        mk_sframe_and_plot_tools_tight('PrunedCat1htag0btag'),
        mk_sframe_and_plot_tools_tight('PrunedCat1htag1btag'),
        # mk_sframe_and_plot_tools('PrunedCat1htag2plusbtag'),
        # mk_sframe_and_plot_tools('PrunedCat0htag2plusbtag'),
        # mk_sframe_and_plot_tools('PrunedCat2htag')
    ]
)

sframe_tools_loose = mk_sframe_and_plot_tools_loose()