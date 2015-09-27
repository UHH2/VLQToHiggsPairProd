#!/usr/bin/env python

import os
import time
import glob

import theta_auto

import varial.tools
import varial.generators as gen
import varial.analysis as analysis
import varial.wrappers as wrappers
from varial.sample import Sample
from varial.extensions.limits import *
from UHH2.VLQSemiLepPreSel.common import TpTpThetaLimits, TriangleLimitPlots

import common_sensitivity
import common_plot
import model_vlqpair

# varial.settings.use_parallel_chains = False

theta_auto.config.theta_dir = "/nfs/dust/cms/user/nowatsd/theta"

src_dir_rel = '../../../../../EventLoopAndPlots'

br_list = []

# only br_th = 100% for now

for th_br in [i/10. for i in range(6, 12, 2)]:
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
    if file_path.endswith('.root')\
        and 'DATA' not in file_path\
        and in_file_path.endswith('PostSelection/ST'):
        return True

def loader_hook_func(brs):
    def temp(wrps):
        wrps = common_sensitivity.loader_hook_scale(wrps, brs)
        wrps = common_plot.norm_smpl(wrps,
            smpl_fct={
                'TpTp_M-700' : 1./0.455,
                'TpTp_M-800' : 1./0.196,
                'TpTp_M-900' : 1./0.0903,
                'TpTp_M-1000' : 1./0.0440,
                'TpTp_M-1100' : 1./0.0224,
                'TpTp_M-1200' : 1./0.0118,
                'TpTp_M-1300' : 1./0.00639,
                'TpTp_M-1400' : 1./0.00354,
                'TpTp_M-1500' : 1./0.00200,
                'TpTp_M-1600' : 1./0.001,
                'TpTp_M-1700' : 1./0.0005,
                'TpTp_M-1800' : 1./0.00025,
            },
            norm_all=(5000./42.477))
        return wrps
    return temp

# maybe pack this up into a list of individual tool chains so that HistoLoader is the first
# tool and ThetaLimitsBranchingRatios runs afterwards (input_path would then be s.th. like
# input_path='..')

def mk_limit_list():
    limit_list = []
    for ind, brs_ in enumerate(br_list):
        # if ind > 2: break
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
                TpTpThetaLimits(
                    input_path= '../HistoLoader',
                    cat_key=lambda w: w.category,
                    # name= 'ThetaLimitsSplit'+str(ind),
                    # asymptotic= False,
                    brs=brs_,
                    model_func= lambda w: model_vlqpair.get_model(w, [
                        'TpTp_M-800',
                        'TpTp_M-900',
                        'TpTp_M-1000',
                        'TpTp_M-1100',
                        'TpTp_M-1300',
                        'TpTp_M-1600'])
                )
            ]))
    return limit_list


# tool_list.append(TriangleLimitPlots())

dir_limit = 'Limits5fb'

def mk_limit_chain():
    return varial.tools.ToolChainParallel(
        'Ind_Limits', lazy_eval_tools_func=mk_limit_list
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
            limit_rel_path='Ind_Limits/Limit*/TpTpThetaLimits'
            ),
        # # varial.tools.HistoLoader(
        # #     # name='HistoLoaderSplit'+str(ind),
        # #     pattern=dir_limit+'/TriangleLimitPlots/*.root',
        # #     # filter_keyfunc=lambda w: w.in_file_path == 'EventHistsPost/EventHists/ST',
        # #     # hook_loaded_histos=loader_hook
        # #     ),
        varial.plotter.Plotter(
            input_result_path='../TriangleLimitPlots',
            plot_setup=plot_setup,
            save_name_func=lambda w: 'M-'+str(w.mass)
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

