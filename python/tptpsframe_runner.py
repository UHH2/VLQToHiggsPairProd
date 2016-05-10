#!/usr/bin/env python

##################################### definition of UserConfig item changes ###


start_all_parallel = False


############################################################### script code ###
import varial
import sys
import os
import copy

from varial.extensions import git

varial.settings.max_num_processes = 12

categories_final = [
        # 'CombinedElMu',
        'El45_Baseline',
        'El45_H2B',
        'El45_H1B',
        'El45_Sideband',
        'Mu45_Baseline',
        'Mu45_H2B',
        'Mu45_H1B',
        'Mu45_Sideband',
        'MuElComb_Baseline',
        'MuElComb_H2B',
        'MuElComb_H1B',
        'MuElComb_Sideband',
        ]

categories_pre = [ #"NoSelection",
        'IsoMuo20',
        'IsoEle27',
        'Mu45',
        'El45',
        ]

sys_uncerts_final = {
    # 'name' : {'item name': 'item value', ...},
    # 'jec_up'        : {'jecsmear_direction':'up'},
    # 'jec_down'      : {'jecsmear_direction':'down'},
    # 'jer_up'        : {'jersmear_direction':'up'},
    # 'jer_down'      : {'jersmear_direction':'down'},
    'nominal'       : {'jecsmear_direction':'nominal'}
    # 'jer_jec_up'    : {'jersmear_direction':'up','jecsmear_direction':'up'},
    # 'jer_jec_down'  : {'jersmear_direction':'down','jecsmear_direction':'down'},
}
no_sys_uncerts = {
    'nominal'       : {'jecsmear_direction':'nominal'}
}
  

final_states_to_split_into = [
    'thth',
    'thtz',
    'thbw',
    'noH_tztz',
    'noH_tzbw',
    'noH_bwbw',
]


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
    if varial.settings.sys_uncerts:
        uncert = varial.settings.sys_uncerts[uncert_name]
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

def setup_for_finalsel(outputdir = '', allowed_datasets = None, count = '-1', analysis_module='', uncert_name='', categories=None):
    def tmp_func(element_tree):
        set_analysis_module(element_tree, analysis_module)
        set_output_dir(element_tree, outputdir)
        clean_input_data(element_tree, allowed_datasets)
        make_higgs_split_item(element_tree, final_states_to_split_into)
        do_set_eventnumber(element_tree, count)
        set_uncert(element_tree, uncert_name)
        do_set_cat(element_tree, " ".join(categories))
    return tmp_func

def setup_for_presel(outputdir = '', allowed_datasets = None, count = '-1', analysis_module='', uncert_name='', categories=None):
    def tmp_func(element_tree):
        set_analysis_module(element_tree, analysis_module)
        set_output_dir(element_tree, outputdir)
        clean_input_data(element_tree, allowed_datasets)
        # make_higgs_split_item(element_tree, final_states_to_split_into)
        do_set_eventnumber(element_tree, count)
        # set_uncert(element_tree, uncert_name)
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
   <ConfigParse NEventsBreak="50000" FileSplit="0" AutoResubmit="0" />
   <ConfigSGE RAM ="2" DISK ="2" Mail="dominik.nowatschin@cern.de" Notification="as" Workdir="workdir"/>
-->
"""
        if os.path.exists(self.cwd + 'workdir'):
            opt = ' -rl --exitOnQuestion'
        else:
            opt = ' -sl --exitOnQuestion'

        self.exe = 'sframe_batch.py' + opt



sframe_cfg_final = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/UHH2/VLQToHiggsPairProd/config/TpTpFinalSelectionV2.xml'
sframe_cfg_pre = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/UHH2/VLQToHiggsPairProd/config/TpTpPreselectionV2.xml'

import common_plot
import plot as plot
from optparse import OptionParser
import tex_content
from varial.extensions.hadd import Hadd

varial.settings.sys_uncerts = {}

def mk_sframe_tools_and_plot(argv):
    parser = OptionParser()

    parser.add_option('--output', type='string', action='store',
                      dest='outputdir',
                      help='Output directory')

    parser.add_option('--sel', type='string', action='store',
                      dest='selection',
                      help='Selection type (pre or final)')

    (options, args) = parser.parse_args(argv)
    argv = []

    count = '-1'

    if options.selection == 'pre':
        sframe_cfg = sframe_cfg_pre
        setup_for_ind_run = setup_for_presel
        categories = categories_pre
        analysis_module = 'TpTpPreselectionV2'
        varial.settings.sys_uncerts = no_sys_uncerts
        basenames = plot.basenames_pre
        tex_base = '/Files_and_Plots/Files_and_Plots_nominal/Plots/'
        samples_to_plot = plot.samples_to_plot_pre
        varial.settings.fix_presel_sample = True
        # varial.settings.merge_decay_channels = True
    elif options.selection == 'final':
        sframe_cfg = sframe_cfg_final
        setup_for_ind_run = setup_for_finalsel
        categories = categories_final
        analysis_module = 'TpTpFinalSelectionTreeOutput'
        varial.settings.sys_uncerts = sys_uncerts_final
        basenames = plot.basenames_final
        tex_base = '/Files_and_Plots/Files_and_Plots_nominal/Plots/'
        samples_to_plot = plot.samples_to_plot_only_th
        # varial.settings.merge_decay_channels = False
    else:
        print "Provide correct 'selection' option ('pre' or 'final')!"
        exit(-1)

    def sf_batch_tc():
        hadd = Hadd(
            src_glob_path='../../SFrame/workdir/uhh2.AnalysisModuleRunner.*.root',
            basenames=basenames,
            add_aliases_to_analysis=False,
            samplename_func=plot.get_samplename,
            # overwrite=False
            )
        plots = varial.tools.ToolChainParallel(
            'Plots',
            lazy_eval_tools_func=plot.mk_plots_and_cf(categories=categories, datasets=samples_to_plot, filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in samples_to_plot) and ('Baseline' in w.in_file_path))
        )
        plots_comp_fs = varial.tools.ToolChainParallel(
            'PlotsCompFinalStates',
            lazy_eval_tools_func=plot.mk_plots_and_cf(categories=None, datasets=plot.samples_to_plot_final,
                filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in plot.samples_to_plot_final\
                    if not any(g in w.file_path.split('/')[-1] for g in ['TpTp_M-0700', 'TpTp_M-1300', 'TpTp_M-1700']))\
                    and ('Baseline' in w.in_file_path),
                compare_uncerts=False, hook_loaded_histos=plot.loader_hook_compare_finalstates
            )
        )
        tc_list = []
        for uncert in varial.settings.sys_uncerts:
            sf_batch = MySFrameBatch(
                cfg_filename=sframe_cfg,
                # xml_tree_callback=set_uncert_func(uncert),
                xml_tree_callback=setup_for_ind_run(outputdir='./', count='-1', analysis_module=analysis_module,
                    uncert_name=uncert, categories=categories),
                name='SFrame',
                # name='SFrame_' + uncert,
                halt_on_exception=False,
                )
            if uncert == 'nominal':
                tc_list.append(varial.tools.ToolChain('Files_and_Plots_'+uncert,[
                    # sf_batch,
                    varial.tools.ToolChain(
                        'Plots',
                        [
                            # hadd,
                            plots,
                            plots_comp_fs,
                            # varial.tools.WebCreator(no_tool_check=True)
                        ]
                    )
                    ]))
            else:
                tc_list.append(varial.tools.ToolChain('Files_and_Plots_'+uncert,[
                    sf_batch
                    ]))

        return tc_list

    def mk_tex_tc_pre(base):
        return varial.tools.ToolChain('TexCopyPre', [
            varial.tools.ToolChain(
                'Tex', 
                [
                    # mk_autoContentSignalControlRegion(p_postbase),
                    # tex_content.mk_autoContentControlPlots(base, 'El45', 'Mu45'),
                    # tex_content.mk_autoContentFinalSelectionHiggsVar(base),
                    tex_content.mk_autoContentPreSelectionNm1(base+'Plots/', 'El45', 'Mu45'),
                    # tex_content.mk_autoContentJetPtReweight(base),
                    # mk_autoContentLimits(p_postbase)
                ]
            ),
            varial.tools.CopyTool('dnowatsc@lxplus.cern.ch:AN-Dir/notes/AN-15-327/trunk/', src='../Tex/*', ignore=('.svn'), use_rsync=True)
        ])

    def mk_tex_tc_final(base):
        return varial.tools.ToolChain('TexCopyFinal', [
            varial.tools.ToolChain(
                'Tex', 
                [
                    # mk_autoContentSignalControlRegion(p_postbase),
                    tex_content.mk_autoContentControlPlots(base+'Plots', 'El45_Baseline', 'Mu45_Baseline'),
                    tex_content.mk_autoContentFinalSelectionHiggsVar(base+'Plots', 'El45_Baseline', 'Mu45_Baseline'),
                    tex_content.mk_autoContentFinalSelectionHiggsVar(base+'PlotsCompFinalStates', 'El45_Baseline', 'Mu45_Baseline', name='HiggsVarCompFinalState'),
                    # tex_content.mk_autoContentPreSelectionNm1(base, 'El45_Baseline', 'Mu45_Baseline'),
                    # tex_content.mk_autoContentJetPtReweight(base),
                    # mk_autoContentLimits(p_postbase)
                ]
            ),
            varial.tools.CopyTool('dnowatsc@lxplus.cern.ch:AN-Dir/notes/AN-15-327/trunk/', src='../Tex/*', ignore=('.svn'), use_rsync=True)
        ])            


    if options.selection == 'pre':
        return varial.tools.ToolChain(
            options.outputdir,
            [
                git.GitAdder(),
                ToolChain('Files_and_Plots',
                    sf_batch_tc()
                ),
                mk_tex_tc_pre(options.outputdir+tex_base),
                varial.tools.WebCreator(no_tool_check=False),
                git.GitTagger(commit_prefix='In {0}'.format(options.outputdir)),
            ]
        )
    else:
        return varial.tools.ToolChain(
            options.outputdir,
            [
                git.GitAdder(),
                ToolChain('Files_and_Plots',
                    sf_batch_tc()
                ),
                mk_tex_tc_final(options.outputdir+tex_base),
                varial.tools.WebCreator(no_tool_check=False),
                git.GitTagger(commit_prefix='In {0}'.format(options.outputdir)),
            ]
        )

if __name__ == '__main__':
    # if len(sys.argv) != 3:
    #     print 'Provide output dir and whether you want to run preselecton (pre) or final selection (final)!'
    #     exit(-1)
    varial.tools.Runner(mk_sframe_tools_and_plot(sys.argv), True)