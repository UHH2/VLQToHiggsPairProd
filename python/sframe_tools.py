
from varial.extensions.sframeproxy import SFrame
import varial.tools
import plot


sframe_cfg = '/nfs/dust/cms/user/nowatsd/sFrameNew/CMSSW_7_4_0_pre6'\
                '/src/UHH2/VLQToHiggsPairProd/config/TpTpTightSelection.xml'


def set_category_and_eventnumber(catname, count ="-1"):
    def do_set_cat(element_tree):
        user_config = element_tree.getroot().find('Cycle').find('UserConfig')
        for item in user_config:
            if item.get('Name') == 'category':
                item.set('Value', catname)
                break
        input_data = element_tree.getroot().find('Cycle').findall('InputData')
        for attr in input_data:
            attr.set('NEventsMax', count)
    return do_set_cat


def mk_sframe_and_plot_tools(catname):
    """Makes a toolchain for one category with sframe and plots."""
    sframe = SFrame(
        cfg_filename=sframe_cfg,
        xml_tree_callback=set_category_and_eventnumber(catname, count="1000"), # 
    )
    plots = varial.tools.ToolChainParallel(
        'Plots',
        lazy_eval_tools_func=lambda: plot.mk_tools()
    )
    tc = varial.tools.ToolChain(
        catname,
        [
            sframe,
            plots
        ]
    )
    return tc


sframe_tools = varial.tools.ToolChain(
    'EventLoopAndPlots',
    [
        mk_sframe_and_plot_tools('PrunedCat1htag0btag'),
        mk_sframe_and_plot_tools('PrunedCat1htag1btag'),
        # mk_sframe_and_plot_tools('PrunedCat1htag2plusbtag'),
        # mk_sframe_and_plot_tools('PrunedCat0htag2plusbtag'),
        # mk_sframe_and_plot_tools('PrunedCat2htag')
    ]
)