from varial.extensions.sframe import SFrame
import varial.tools
import copy

# sframe_cfg_test = '/nfs/dust/cms/user/nowatsd/sFrameNew/CMSSW_7_4_7/src/UHH2/VLQToHiggsPairProd/config/TestNewFormat.xml'

def_final_states = [
    'thth',
    'thtz',
    'thbw',
    'noH_tztz',
    'noH_tzbw',
    'noH_bwbw',
]

def_signal_samples = [
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

def do_set_eventnumber(element_tree, count):
    input_data = element_tree.getroot().find('Cycle').findall('InputData')
    for attr in input_data:
        attr.set('NEventsMax', count)

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




def set_category_datasets_and_eventnumber(catname, count ="1000", allowed_datasets=None):
    def tmp_func(element_tree):
        clean_input_data(element_tree, allowed_datasets)
        do_set_cat(element_tree, catname)
        do_set_eventnumber(element_tree, count)
    return tmp_func

def set_category_datasets_eventnumber_and_split(catname, count ="1000", allowed_datasets=None):
    def tmp_func(element_tree):
        clean_input_data(element_tree, allowed_datasets)
        split_item_and_set_filename(element_tree, def_signal_samples, def_final_states)
        do_set_cat(element_tree, catname)
        do_set_eventnumber(element_tree, count)
    return tmp_func

def set_datasets_eventnumber_and_split(count ="1000", allowed_datasets=None):
    def tmp_func(element_tree):
        clean_input_data(element_tree, allowed_datasets)
        split_item_and_set_filename(element_tree, def_signal_samples, def_final_states)
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

def set_eventnumber_datasets_and_split(count='-1', allowed_datasets=None):
    def tmp_func(element_tree):
        clean_input_data(element_tree, allowed_datasets)
        make_higgs_split_item(element_tree, def_final_states)
        do_set_eventnumber(element_tree, count)
    return tmp_func

# sframe_and_plot_version = 'EventLoopAndPlots_v0'