#!/usr/bin/env python

import os
import time
import glob

import common_vlq
import common_sensitivity
import varial.tools
import varial.generators as gen
import varial.analysis as analysis
import varial.wrappers as wrappers

from varial.sample import Sample
from varial.extensions.limits import *

import theta_auto
import model_vlqpair

# varial.settings.use_parallel_chains = False

theta_auto.config.theta_dir = "/nfs/dust/cms/user/nowatsd/theta"

src_dir_rel = '../../../../../EventLoopAndPlots'

# def file_stack_all():
#     src_dir = analysis.cwd+src_dir_rel
#     file_list = []
#     for cat_dir in os.listdir(src_dir):
#         if os.path.isdir(cat_dir):
#             for fil in os.listdir(src_dir+'/'+cat_dir+'/SFrame'):
#                 if (fil.endswith('.root') and 'M1000_' not in fil):
#                     file_list.append(src_dir+cat_dir+'/SFrame/'+fil)
#     return file_list

# def file_stack_split():
#     src_dir = analysis.cwd+src_dir_rel
#     file_list = []
#     for cat_dir in os.listdir(src_dir):
#         print cat_dir
#         print analysis.cwd
#         if os.path.isdir(src_dir+'/'+cat_dir):
#             print "Is Dir"
#             for fil in os.listdir(src_dir+'/'+cat_dir+'/SFrame'):
#                 if (fil.endswith('.root') and not (fil.endswith('_M1000.root') or 'onelep' in fil)):
#                     file_list.append(src_dir+'/'+cat_dir+'/SFrame/'+fil)
#     # print file_list
#     return file_list

def get_category(wrp):
    # print wrp.file_path.split('/')
    return wrp.file_path.split('/')[-3]

# def file_stack_split():
#     src_dir = analysis.cwd+src_dir_rel
#     return [os.path.join(src_dir, f) for f in os.listdir(src_dir) if
#     (f.endswith('.root') and not (f.endswith('_M1000.root') or 'onelep' in f)
#         # and 'HT' not in f
#     )]

br_list = []

for th_br in [i/10. for i in range(0, 12, 2)]:
    for tz_br in [ii/10. for ii in range(0, int(12-th_br*10), 2)]:
        bw_br = 1-th_br-tz_br
        # print bw_br, th_br, tz_br
        br_list.append({
            'bw' : bw_br,
            'th' : th_br,
            'tz' : tz_br
        })

def select_files(wrp):
    file_path = wrp.file_path
    in_file_path = wrp.in_file_path
    # print "before selecting: "+wrp.file_path
    # print file_path
    if file_path.endswith('.root') and not (file_path.endswith('_M1000.root')\
        or 'onelep' in file_path or 'PrunedCat2htag' in file_path)\
        and in_file_path == 'PostSelection/ST':
        return True

def loader_hook_func(brs):
    def temp(w):
        # print varial.analysis.fs_aliases
        return common_sensitivity.loader_hook_scale(w, brs)
    return temp

# maybe pack this up into a list of individual tool chains so that HistoLoader is the first
# tool and ThetaLimitsBranchingRatios runs afterwards (input_path would then be s.th. like
# input_path='..')

def mk_limit_list():
    limit_list = []
    for ind, brs_ in enumerate(br_list):
        if ind > 2: break
        limit_list.append(
            varial.tools.ToolChain('Limit'+str(ind),[
                varial.tools.HistoLoader(
                    # name='HistoLoaderSplit'+str(ind),
                    # pattern=file_stack_split(),
                    filter_keyfunc=select_files,
                    hook_loaded_histos=loader_hook_func(brs_)
                ),
                varial.tools.Plotter(
                    input_result_path='../HistoLoader',
                    plot_grouper=lambda ws: varial.gen.group(
                        ws, key_func=lambda w: w.category),
                    plot_setup=lambda w: varial.gen.mc_stack_n_data_sum(w, None, True),
                    save_name_func=lambda w: w.category
                ),
                ThetaLimitsBranchingRatios(
                    input_path= '../HistoLoader',
                    cat_key=lambda w: w.category,
                    # name= 'ThetaLimitsSplit'+str(ind),
                    # asymptotic= False,
                    brs=brs_,
                    model_func= lambda w: model_vlqpair.get_model(w, ['TpTp_M1000'])
                )
            ]))
    return limit_list


# tool_list.append(TriangleLimitPlots())

dir_limit = 'Limits2'

def mk_limit_chain():
    return varial.tools.ToolChainParallel(
        'Ind_Limits', lazy_eval_tools_func=lambda: mk_limit_list()
        )

def add_draw_option(wrps, draw_option=''):
    for wrp in wrps:
        if type(wrp) == wrappers.HistoWrapper:
            wrp.draw_option = draw_option
        yield wrp

def plot_setup(wrps):
    wrps = (add_draw_option(ws, 'colz text') for ws in wrps)
    wrps = (gen.apply_markercolor(ws, colors=[1]) for ws in wrps)
    # print wrps.wrps[0].type
    return wrps

def mk_tc():
    return varial.tools.ToolChain(dir_limit, 
        [
        mk_limit_chain(),
        TriangleLimitPlots(
            limit_rel_path='Ind_Limits/Limit*/ThetaLimitsBranchingRatios'
            ),
        # # varial.tools.HistoLoader(
        # #     # name='HistoLoaderSplit'+str(ind),
        # #     pattern=dir_limit+'/TriangleLimitPlots/*.root',
        # #     # filter_keyfunc=lambda w: w.in_file_path == 'EventHistsPost/EventHists/ST',
        # #     # hook_loaded_histos=loader_hook
        # #     ),
        varial.plotter.Plotter(
            input_result_path='../TriangleLimitPlots',
            plot_setup=plot_setup
            ),
        # varial.tools.WebCreator()
        # varial.tools.CopyTool()
        ])

# tc = varial.tools.ToolChain("", [tc])

if __name__ == '__main__':
    time.sleep(1)
    # print analysis.cwd
    # print mk_tc()
    varial.tools.Runner(mk_tc())
    # os.chdir(dir_limit)
    # # varial.tools.WebCreator().run()
    # os.chdir('..') 

