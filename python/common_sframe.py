from varial.extensions.sframe import SFrame
import varial.tools

# sframe_cfg_test = '/nfs/dust/cms/user/nowatsd/sFrameNew/CMSSW_7_4_7/src/UHH2/VLQToHiggsPairProd/config/TestNewFormat.xml'

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


def set_category_datasets_and_eventnumber(catname, count ="1000", allowed_datasets=None):
    def tmp_func(element_tree):
        clean_input_data(element_tree, allowed_datasets)
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

# sframe_and_plot_version = 'EventLoopAndPlots_v0'