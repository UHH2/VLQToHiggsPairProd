import copy

import varial.tools
from varial.extensions.sframe import SFrame

# sframe_cfg_test = '/nfs/dust/cms/user/nowatsd/sFrameNew/CMSSW_7_4_7/src/UHH2/VLQToHiggsPairProd/config/TestNewFormat.xml'

final_states_to_split_into = [
    'thth',
    'thtz',
    'thbw',
    'noH_tztz',
    'noH_tzbw',
    'noH_bwbw',
]

signal_files_to_split = [
    'TpTp_M-700',
    'TpTp_M-800',
    'TpTp_M-900',
    'TpTp_M-1000',
    'TpTp_M-1100',
    'TpTp_M-1200',
    'TpTp_M-1300',
    'TpTp_M-1400',
    'TpTp_M-1500',
    'TpTp_M-1600',
    'TpTp_M-1700',
    'TpTp_M-1800',
]

def do_set_cat(element_tree, catname):
    user_config = element_tree.getroot().find('Cycle').find('UserConfig')
    for item in user_config:
        if item.get('Name') == 'category':
            item.set('Value', catname)
            break

def do_set_eventnumber(element_tree, count=-1):
    input_data = element_tree.getroot().find('Cycle').findall('InputData')
    for attr in input_data:
        attr.set('NEventsMax', str(count))

def clean_input_data(element_tree, allowed_datasets):
    tree_cycle = element_tree.getroot().find('Cycle')
    for item in tree_cycle.findall('InputData'):
        if item.get('Version') not in allowed_datasets:
            tree_cycle.remove(item)

def make_higgs_split_item(element_tree, final_states=None):
    tree_cycle = element_tree.getroot().find('Cycle')
    for ind, item in enumerate(tree_cycle.findall('InputData')):
        if 'TpTp' in item.get('Version'):
            for ver in final_states:
                split_smpl = copy.deepcopy(item)
                split_smpl.set('Version', split_smpl.get('Version')+'_'+ver)
                tree_cycle.insert(ind, split_smpl)
            tree_cycle.remove(item)

def split_item_and_set_filename(element_tree, datasets=None, final_states=None):
    tree_cycle = element_tree.getroot().find('Cycle')
    for ind, item in enumerate(tree_cycle.findall('InputData')):
        item_ver = item.get('Version')
        if item_ver in datasets:
            for ver in final_states:
                split_smpl = copy.deepcopy(item)
                in_item = split_smpl.find('In')
                filename = in_item.get('FileName')
                filename = filename.replace(item_ver, item_ver+'_'+ver)
                split_smpl.set('Version', item_ver+'_'+ver)
                in_item.set('FileName', filename)
                tree_cycle.insert(ind, split_smpl)
            tree_cycle.remove(item)

def set_analysis_module(element_tree, analysis_module=''):
    if analysis_module:
        user_config = element_tree.getroot().find('Cycle').find('UserConfig')
        for item in user_config:
            if item.get('Name') == 'AnalysisModule':
                item.set('Value', analysis_module)
                break

def set_output_dir(element_tree, outputdir=''):
    if outputdir:
        sframe_cycle = element_tree.getroot().find('Cycle')
        sframe_cycle.set('OutputDirectory', outputdir)





def set_category_datasets_and_eventnumber(catname, count ="1000", allowed_datasets=None, analysis_module=''):
    def tmp_func(element_tree):
        set_analysis_module(element_tree, analysis_module)
        clean_input_data(element_tree, allowed_datasets)
        do_set_cat(element_tree, catname)
        do_set_eventnumber(element_tree, count)
    return tmp_func

def set_category_datasets_eventnumber_and_split(catname, count ="1000", allowed_datasets=None, analysis_module=''):
    def tmp_func(element_tree):
        set_analysis_module(element_tree, analysis_module)
        clean_input_data(element_tree, allowed_datasets)
        split_item_and_set_filename(element_tree, signal_files_to_split, final_states_to_split_into)
        do_set_cat(element_tree, catname)
        do_set_eventnumber(element_tree, count)
    return tmp_func

def set_datasets_eventnumber_and_split(count ="1000", allowed_datasets=None, analysis_module=''):
    def tmp_func(element_tree):
        set_analysis_module(element_tree, analysis_module)
        clean_input_data(element_tree, allowed_datasets)
        split_item_and_set_filename(element_tree, signal_files_to_split, final_states_to_split_into)
        do_set_eventnumber(element_tree, count)
    return tmp_func

def set_eventnumber(count="-1", analysis_module=''):
    def tmp_func(element_tree):
        set_analysis_module(element_tree, analysis_module)
        do_set_eventnumber(element_tree, count)
    return tmp_func

def set_eventnumber_and_datasets(count='-1', allowed_datasets=None, analysis_module=''):
    def tmp_func(element_tree):
        set_analysis_module(element_tree, analysis_module)
        clean_input_data(element_tree, allowed_datasets)
        do_set_eventnumber(element_tree, count)
    return tmp_func

def set_datasets_eventnumber_and_split_loose(outputdir='', count='-1', allowed_datasets=None, analysis_module=''):
    def tmp_func(element_tree):
        set_output_dir(element_tree, outputdir)
        set_analysis_module(element_tree, analysis_module)
        clean_input_data(element_tree, allowed_datasets)
        make_higgs_split_item(element_tree, final_states_to_split_into)
        do_set_eventnumber(element_tree, count)
    return tmp_func

# sframe_and_plot_version = 'EventLoopAndPlots_v0'




def setup_for_ind_run(analysis_module = '', allowed_datasets = None, count = '-1'):
    def tmp_func(element_tree):
        set_analysis_module(element_tree, analysis_module)
        clean_input_data(element_tree, allowed_datasets)
        do_set_eventnumber(element_tree, count)
    return tmp_func

sframe_cfg = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII-25ns-v2/CMSSW_7_4_15_patch1/src/UHH2/VLQToHiggsPairProd/config/TpTpAnalysisModule.xml'

if __name__ == '__main__':
    time.sleep(1)
    src_dir = sys.argv[1]
    final_dir = sys.argv[2]
    sframe = SFrame(
        cfg_filename=sframe_cfg,
        xml_tree_callback=setup_for_ind_run(
            count=count, allowed_datasets=allowed_datasets,
        ), # 
    )
    varial.tools.Runner(all_tools, default_reuse=True)
    # varial.tools.CopyTool('~/www/vlq_analysis/tight_selection2/',
    #     src=final_dir, use_rsync=True).run()