#!/usr/bin/env python

import os
import time
import glob

import theta_auto

import varial.tools
import varial.generators as gen
import varial.analysis as analysis
import varial.wrappers as wrappers
import varial.plotter
import varial.rendering
import varial.settings
from varial.sample import Sample
from varial.extensions.limits import *
from UHH2.VLQSemiLepPreSel.common import TpTpThetaLimits, TriangleLimitPlots

import common_sensitivity
import common_plot
import model_vlqpair
import limit_plots

# varial.settings.use_parallel_chains = False

theta_auto.config.theta_dir = "/nfs/dust/cms/user/nowatsd/theta"

# src_dir_rel = '../../../../../EventLoopAndPlots'

br_list = []

# only br_th = 100% for now
# bw_max = 1
bw_max = 0
for bw_br in [i/10. for i in range(0, int(bw_max*10)+2, 2)]:
    # tz_max = 1.0-bw_br
    tz_max = 0
    for tz_br in [ii/10. for ii in range(0, int(tz_max*10)+2, 2)]:
        th_br = 1-bw_br-tz_br
        # print bw_br, th_br, tz_br
        br_list.append({
            'bw' : bw_br,
            'th' : th_br,
            'tz' : tz_br
        })

datasets_to_use = [
    'Run2015D',
    'TpTp_M-0700',
    'TpTp_M-0800',
    'TpTp_M-0900',
    'TpTp_M-1000',
    'TpTp_M-1100',
    'TpTp_M-1200',
    'TpTp_M-1300',
    'TpTp_M-1400',
    'TpTp_M-1500',
    'TpTp_M-1600',
    'TpTp_M-1700',
    'TpTp_M-1800',
    'QCD',
    'TTbar',
    'WJets',
    'DYJets',
    'SingleTop',
]

def select_files(categories=None, var=''):
    def tmp(wrp):
        file_path = wrp.file_path
        in_file_path = wrp.in_file_path
        # print "before selecting: "+wrp.file_path
        # print file_path
        if (file_path.endswith('.root')
                # and 'DATA' not in file_path\
                # and in_file_path.endswith('PostSelection/ST')
                and in_file_path.endswith(var)
                and any(a in wrp.file_path for a in datasets_to_use)
                and (wrp.in_file_path.split('/')[0] in categories if categories else True)) :
            # print wrp
            return True
    return tmp

def loader_hook(brs):
    def temp(wrps):
        wrps = common_sensitivity.loader_hook_scale_excl(wrps, brs)
        wrps = common_plot.norm_smpl(wrps,
            smpl_fct={
                'TpTp_M-0700' : 1./0.455,
                'TpTp_M-0800' : 1./0.196,
                'TpTp_M-0900' : 1./0.0903,
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
            # norm_all=(3000./552.67)
            )
        return wrps
    return temp

def loader_hook_sys(brs):
    def temp(wrps):
        hook = loader_hook(brs)
        wrps = hook(wrps)
        wrps = varial.gen.gen_add_wrp_info(
            wrps,
            sys_type=lambda w: w.file_path.split('/')[-2],
        )
        return wrps
    return temp

# maybe pack this up into a list of individual tool chains so that HistoLoader is the first
# tool and ThetaLimitsBranchingRatios runs afterwards (input_path would then be s.th. like
# input_path='..')

def mk_limit_tc(brs, filter_keyfunc, name='', sys_pat=''):
    loader = varial.tools.HistoLoader(
        name='HistoLoader',
        # pattern=file_stack_split(),
        # pattern=,
        filter_keyfunc=filter_keyfunc,
        hook_loaded_histos=loader_hook(brs)
    )
    plotter = varial.tools.Plotter(
        name='Plotter',
        input_result_path='../HistoLoader',
        plot_grouper=lambda ws: varial.gen.group(
            ws, key_func=lambda w: w.category),
        plot_setup=lambda w: varial.gen.mc_stack_n_data_sum(w, None, True),
        save_name_func=lambda w: w.category
    )
    limits = TpTpThetaLimits(
        name='Limit'+name,
        # input_path= '../HistoLoader',
        cat_key=lambda w: w.category,
        sys_key=lambda w: w.sys_type,
        # name= 'ThetaLimitsSplit'+str(ind),
        # asymptotic= False,
        brs=brs,
        model_func= lambda w: model_vlqpair.get_model(w, [
            'TpTp_M-0700',
            'TpTp_M-0800',
            'TpTp_M-0900',
            'TpTp_M-1000',
            'TpTp_M-1100',
            'TpTp_M-1200',
            'TpTp_M-1300',
            'TpTp_M-1400',
            'TpTp_M-1500',
            'TpTp_M-1600',
            'TpTp_M-1700',
            'TpTp_M-1800'])
    )
    if sys_pat:
        sys_loader = varial.tools.HistoLoader(
            name='HistoLoaderSys',
            filter_keyfunc=lambda w: filter_keyfunc(w) and 'ak4_pt' not in w.file_path,
            pattern=sys_pat,
            hook_loaded_histos=loader_hook_sys(brs)
        )
        return [loader, sys_loader, plotter, limits]
    else:
        return [loader, plotter, limits]


# tool_list.append(TriangleLimitPlots())

def mk_limit_chain(name='Ind_Limits', mk_limit_list=None):
    return varial.tools.ToolChain(
        name, lazy_eval_tools_func=mk_limit_list
        )

def add_draw_option(wrps, draw_option=''):
    for wrp in wrps:
        if type(wrp) == wrappers.HistoWrapper:
            wrp.draw_option = draw_option
        yield wrp

def plot_setup_triangle(grps):
    grps = (add_draw_option(ws, 'colz text') for ws in grps)
    grps = (gen.apply_markercolor(ws, colors=[1]) for ws in grps)
    # print grps.grps[0].type
    return grps

def plot_setup_graphs(grps, th_x=None, th_y=None):
    # grps = varial.plotter.default_plot_colorizer(grps)
    grps = limit_plots.add_th_curve(grps, th_x, th_y)
    # print list(grps)
    return grps

def mk_tc(dir_limit='Limits', mk_limit_list=None):
    return varial.tools.ToolChain(dir_limit, 
        [
        mk_limit_chain(mk_limit_list=mk_limit_list),
        # varial.tools.ToolChain('LimitTriangle',[
        #     TriangleLimitPlots(
        #         limit_rel_path='../Ind_Limits/Limit*/TpTpThetaLimits'
        #         ),
        #     varial.plotter.Plotter(
        #         input_result_path='../TriangleLimitPlots',
        #         plot_setup=plot_setup_triangle,
        #         save_name_func=lambda w: 'M-'+str(w.mass)
        #         ),
        #     ]),
        varial.tools.ToolChain('LimitsWithGraphs',[
            limit_plots.LimitGraphs(
                limit_rel_path='../Ind_Limits/Limit*/*/Limit*'
                ),
            varial.plotter.Plotter(
                name='LimitCurvesCompared',
                input_result_path='../LimitGraphs',
                # filter_keyfunc=lambda w: 'Uncleaned' in w.legend,
                # plot_setup=plot_setup,
                hook_loaded_histos=lambda w: gen.sort(w, key_list=["save_name"]),
                plot_grouper=lambda ws: varial.gen.group(
                        ws, key_func=lambda w: w.save_name),
                # save_name_func=varial.plotter.save_by_name_with_hash
                save_name_func=lambda w: w.save_name,
                plot_setup=lambda w: plot_setup_graphs(w,
                    th_x=common_sensitivity.theory_masses,
                    th_y=common_sensitivity.theory_cs),
                canvas_decorators=[varial.rendering.Legend(x_pos=0.5, y_pos=0.5, label_width=0.2, label_height=0.07)],
                save_lin_log_scale=True
                ),
            # varial.plotter.Plotter(
            #     name='Cleaned',
            #     input_result_path='../LimitGraphs',
            #     filter_keyfunc=lambda w: 'Cleaned' in w.legend,
            #     # plot_setup=plot_setup,
            #     hook_loaded_histos=lambda w: gen.sort(w, key_list=["save_name"]),
            #     plot_grouper=lambda ws: varial.gen.group(
            #             ws, key_func=lambda w: w.save_name),
            #     # save_name_func=varial.plotter.save_by_name_with_hash
            #     save_name_func=lambda w: w.save_name,
            #     plot_setup=lambda w: plot_setup_graphs(w,
            #         th_x=common_sensitivity.theory_masses,
            #         th_y=common_sensitivity.theory_cs),
            #     canvas_decorators=[varial.rendering.Legend(x_pos=0.5, y_pos=0.5, label_width=0.2, label_height=0.07)],
            #     save_lin_log_scale=True
            #     ),
            ]),
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

