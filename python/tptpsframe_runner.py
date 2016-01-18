#!/usr/bin/env python

##################################### definition of UserConfig item changes ###

sys_uncerts = {
    # 'name' : {'item name': 'item value', ...},
    # 'jec_up'        : {'jecsmear_direction':'up'},
    # 'jec_down'      : {'jecsmear_direction':'down'},
    # 'jer_up'        : {'jersmear_direction':'up'},
    # 'jer_down'      : {'jersmear_direction':'down'},
    'nominal'       : {'jecsmear_direction':'nominal'}
    # 'jer_jec_up'    : {'jersmear_direction':'up','jecsmear_direction':'up'},
    # 'jer_jec_down'  : {'jersmear_direction':'down','jecsmear_direction':'down'},
}
start_all_parallel = True


############################################################### script code ###
import varial
import sys
import os
import copy

from varial.extensions import git

# varial.settings.max_num_processes = 1

categories = ["NoSelection",
        # "HiggsTag0Med-Control", #"HiggsTag0Med-Control-2Ak8", "HiggsTag0Med-Control-3Ak8", "HiggsTag0Med-Control-4Ak8", 
        # "HiggsTag1bMed-Signal", #"HiggsTag1bMed-Signal-1addB", "HiggsTag1bMed-Signal-2addB", "HiggsTag1bMed-Signal-3addB",
        # "HiggsTag2bMed-Signal", 
        ]

datasets_to_plot = [
    'Run2015D',
    'TpTp_M-800_thth',
    'TpTp_M-800_thtz',
    'TpTp_M-800_thbw',
    'TpTp_M-1600_thth',
    'TpTp_M-1600_thtz',
    'TpTp_M-1600_thbw',
    'QCD',
    'TTbar',
    'WJets',
    'DYJets',
    'SingleT',
]
  

final_states_to_split_into = [
    'thth',
    'thtz',
    'thbw',
    'noH_tztz',
    'noH_tzbw',
    'noH_bwbw',
]

# signal_files_to_split = [
#     'TpTp_M-700',
#     'TpTp_M-800',
#     'TpTp_M-900',
#     'TpTp_M-1000',
#     'TpTp_M-1100',
#     'TpTp_M-1200',
#     'TpTp_M-1300',
#     'TpTp_M-1400',
#     'TpTp_M-1500',
#     'TpTp_M-1600',
#     'TpTp_M-1700',
#     'TpTp_M-1800',
# ]


# xml config editing functions

def do_set_cat(element_tree, catname):
    user_config = element_tree.getroot().find('Cycle').find('UserConfig')
    for item in user_config:
        if item.get('Name') == 'category':
            item.set('Value', catname)
            break

def make_higgs_split_item(element_tree, final_states=None):
    tree_cycle = element_tree.getroot().find('Cycle')
    for ind, item in enumerate(tree_cycle.findall('InputData')):
        if 'TpTp' in item.get('Version'):
            for ver in final_states:
                split_smpl = copy.deepcopy(item)
                split_smpl.set('Version', split_smpl.get('Version')+'_'+ver)
                tree_cycle.insert(ind, split_smpl)
            tree_cycle.remove(item)

def do_set_eventnumber(element_tree, count=-1):
    input_data = element_tree.getroot().find('Cycle').findall('InputData')
    for attr in input_data:
        attr.set('NEventsMax', str(count))

def clean_input_data(element_tree, allowed_datasets):
    if allowed_datasets:
        tree_cycle = element_tree.getroot().find('Cycle')
        for item in tree_cycle.findall('InputData'):
            if item.get('Version') not in allowed_datasets:
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

def set_uncert(element_tree, uncert_name=''):
    uncert = sys_uncerts[uncert_name]
    cycle = element_tree.getroot().find('Cycle')
    user_config = cycle.find('UserConfig')
    for name, value in uncert.iteritems():
        uc_item = list(i for i in user_config if i.get('Name') == name)
        assert uc_item, 'could not find item with name: %s' % name
        uc_item[0].set('Value', value)

# xml treecallback functions

# def set_uncert_func(uncert_name):
#     uncert = sys_uncerts[uncert_name]
#     def do_set_uncert(element_tree):
#         cycle = element_tree.getroot().find('Cycle')
#         user_config = cycle.find('UserConfig')
#         output_dir = cycle.get('OutputDirectory')
#         cycle.set('OutputDirectory', os.path.join(output_dir, uncert_name))

#         for name, value in uncert.iteritems():
#             uc_item = list(i for i in user_config if i.get('Name') == name)
#             assert uc_item, 'could not find item with name: %s' % name
#             uc_item[0].set('Value', value)

#     return do_set_uncert

def setup_for_ind_run(outputdir = '', allowed_datasets = None, count = '-1', analysis_module='', uncert_name=''):
    def tmp_func(element_tree):
        set_analysis_module(element_tree, analysis_module)
        set_output_dir(element_tree, outputdir)
        clean_input_data(element_tree, allowed_datasets)
        make_higgs_split_item(element_tree, final_states_to_split_into)
        do_set_eventnumber(element_tree, count)
        set_uncert(element_tree, uncert_name)
        do_set_cat(element_tree, " ".join(categories))
    return tmp_func


from varial.extensions.sframe import SFrame
from varial import tools
if start_all_parallel:
    ToolChain = tools.ToolChainParallel
else:
    ToolChain = tools.ToolChain



class MySFrameBatch(SFrame):

    def configure(self):
        self.xml_doctype = self.xml_doctype + """
<!--
   <ConfigParse NEventsBreak="100000" FileSplit="0" AutoResubmit="2" />
   <ConfigSGE RAM ="2" DISK ="2" Mail="dominik.nowatschin@cern.de" Notification="as" Workdir="workdir"/>
-->
"""
        if os.path.exists(self.cwd + 'workdir'):
            opt = ' -rl --exitOnQuestion'
        else:
            opt = ' -sl --exitOnQuestion'

        self.exe = 'sframe_batch.py' + opt



sframe_cfg = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII-25ns-v2/CMSSW_7_4_15_patch1/src/UHH2/VLQToHiggsPairProd/config/TpTpFinalSelectionV2.xml'

import tptpfinalselection_plot as final_plotting

def mk_sframe_tools_and_plot(name='All_Files'):
    tc = ToolChain('Files_and_Plots',
        list(
            varial.tools.ToolChain('Files_and_Plots_'+uncert,
                [
                MySFrameBatch(
                    cfg_filename=sframe_cfg,
                    # xml_tree_callback=set_uncert_func(uncert),
                    xml_tree_callback=setup_for_ind_run(outputdir='./', count='-1', analysis_module='TpTpFinalSelectionTreeOutput',
                        uncert_name=uncert),
                    name='SFrame',
                    # name='SFrame_' + uncert,
                    halt_on_exception=False,
                    ),
                final_plotting.hadd_and_plot(version='Plots',
                    src='SFrame/workdir/uhh2.AnalysisModuleRunner.*.root',
                    categories=categories)
                ]
                )
            for uncert in sys_uncerts
            )
        )

    return varial.tools.ToolChain(
        name,
        [
            git.GitAdder(),
            tc,
            varial.tools.WebCreator(no_tool_check=False),
            git.GitTagger()
            ]
    )


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Pls. give me da name of da outputdir! ... dude!'
        exit(-1)
    varial.tools.Runner(mk_sframe_tools_and_plot(sys.argv[1]))