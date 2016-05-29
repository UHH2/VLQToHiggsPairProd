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
import varial.operations
import varial.util as util
from ROOT import TLatex
from varial.sample import Sample
from varial.extensions.limits import *
from UHH2.VLQSemiLepPreSel.common import TpTpThetaLimits, TriangleMassLimitPlots

import common_sensitivity
import common_plot
import model_vlqpair
# import limit_plots

# varial.settings.use_parallel_chains = False

theta_auto.config.theta_dir = "/nfs/dust/cms/user/nowatsd/theta"

# src_dir_rel = '../../../../../EventLoopAndPlots'

varial.settings.__setattr__('asymptotic', True)

br_list = []

# only br_th = 100% for now
# bw_max = 1
bw_max = 1
for bw_br in [i/10. for i in xrange(0, int(bw_max*10)+2, 2)]:
    tz_max = 1.0-bw_br
    # tz_max = 0.8
    for tz_br in [ii/10. for ii in xrange(0, int(tz_max*10)+2, 2)]:
        th_br = 1-bw_br-tz_br
        # print bw_br, th_br, tz_br
        br_list.append({
            'bw' : bw_br,
            'th' : th_br,
            'tz' : tz_br
        })

backgrounds_to_use = [
    # 'Run2015CD',
    'QCD',
    'TTbar',
    'WJets',
    'DYJets',
    'SingleTop',
]

signals_to_use = [
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
]

final_states_to_use = [
    '_thth',
    '_thtz',
    '_thbw',
    '_noH_tztz',
    '_noH_tzbw',
    '_noH_bwbw',
]

datasets_to_use = backgrounds_to_use + signals_to_use + ['Run2015CD']

back_plus_data = backgrounds_to_use + ['Run2015CD']

datasets_not_to_use = [
    'ak4_jetpt__minus/TpTp',
    'ak4_jetpt__plus/TpTp',
]

# def select_files(categories=None, var=''):
#     def tmp(wrp):
#         file_path = wrp.file_path
#         in_file_path = wrp.in_file_path
#         # print "before selecting: "+wrp.file_path
#         # print file_path
#         if (file_path.endswith('.root')
#                 # and 'DATA' not in file_path\
#                 # and in_file_path.endswith('PostSelection/ST')
#                 and ('Run2015CD' not in wrp.file_path or varial.settings.plot_obs)
#                 and in_file_path.endswith(var)
#                 and any(a in wrp.file_path for a in datasets_to_use)
#                 and all(a not in wrp.file_path for a in datasets_not_to_use)
#                 and (any(wrp.in_file_path.split('/')[0] == a for a in categories) if categories else True)) :
#             # print wrp
#             return True
#     return tmp

def rebin_st(wrps):
    st_bounds = st_bounds = [0., 800., 900., 1000., 1200., 1500., 2000., 2500., 3000., 4500., 6500.]
    for w in wrps:
        if w.in_file_path.endswith('ST'):
            # w = varial.operations.rebin_nbins_max(w, 15)
            w = varial.operations.rebin(w, st_bounds, False)
        yield w

def loader_hook(brs):
    def temp(wrps):
        wrps = common_sensitivity.loader_hook_scale_excl(wrps, brs)
        wrps = rebin_st(wrps)
        wrps = common_plot.norm_smpl(wrps,
            smpl_fct=common_plot.normfactors,
            # norm_all=(3000./552.67)
            )
        return wrps
    return temp

def loader_hook_sys(brs):
    def temp(wrps):
        hook = loader_hook(brs)
        wrps = hook(wrps)
        # wrps = varial.gen.gen_add_wrp_info(
        #     wrps,
        #     sys_type=lambda w: w.file_path.split('/')[-2],
        # )
        return wrps
    return temp



def limit_curve_loader_hook(brs):
    def tmp(wrps):
        # wrps = list(wrps)
        # print wrps
        # wrps = gen.gen_add_wrp_info(wrps, save_name=lambda w: 'tH%.0ftZ%.0fbW%.0f'\
        #    % (brs['th']*100, brs['tz']*100, brs['bw']*100))
        wrps = gen.gen_add_wrp_info(wrps, brs=lambda w: brs)
        wrps = gen.sort(wrps, key_list=['save_name'])
        return wrps
    return tmp


def scale_bkg_postfit(wrps, theta_res_path):
    theta_res = varial.ana.lookup_result(theta_res_path)
    try:
        r, _ = theta_res.postfit_vals['TpTp_M-0700']['bkg_rate'][0]
    except KeyError:
        r = 0

    for w in wrps:
        if w.sample == 'Bkg':
            w.sample = 'BkgPostFit'
            w.legend = 'Bkg. post-fit'
            w.histo.Scale(1+r)
        yield w

# maybe pack this up into a list of individual tool chains so that HistoLoader is the first
# tool and ThetaLimitsBranchingRatios runs afterwards (input_path would then be s.th. like
# input_path='..')

# def mk_limit_tc(brs, filter_keyfunc, sys_pat=''):

#     loader = varial.tools.HistoLoader(
#         name='HistoLoader',
#         # pattern=file_stack_split(),
#         # pattern=,
#         filter_keyfunc=filter_keyfunc,
#         hook_loaded_histos=loader_hook(brs)
#     )
#     plotter = varial.tools.Plotter(
#         name='Plotter',
#         input_result_path='../HistoLoader',
#         plot_grouper=lambda ws: varial.gen.group(
#             ws, key_func=lambda w: w.category),
#         plot_setup=lambda w: varial.gen.mc_stack_n_data_sum(w, None, True),
#         save_name_func=lambda w: w.category
#     )
#     limits = TpTpThetaLimits(
#         name='ThetaLimit',
#         # input_path= '../HistoLoader',
#         cat_key=lambda w: w.category,
#         sys_key=lambda w: w.sys_info,
#         # name= 'ThetaLimitsSplit'+str(ind),
#         asymptotic=varial.settings.asymptotic,
#         brs=brs,
#         model_func= lambda w: model_vlqpair.get_model(w, signals_to_use),
#         # do_postfit=False,
#     )
#     postfit = ThetaPostFitPlot(
#         name='PostFit',
#         input_path='../ThetaLimit')
#     # plotter_postfit = varial.tools.Plotter(
#     #     filter_keyfunc=lambda w: '700' in w.sample 
#     #                              or '900' in w.sample 
#     #                              or not w.is_signal,
#     #     plot_grouper=lambda ws: varial.gen.group(
#     #         ws, key_func=lambda w: w.category),
#     #     plot_setup=lambda w: varial.gen.mc_stack_n_data_sum(w, None, True),
#     #     save_name_func=lambda w: w.category,
#     #     hook_canvas_post_build=varial.gen.add_sample_integrals,
#     #     hook_loaded_histos=lambda w: scale_bkg_postfit(
#     #         w, '../Limit'+name),
#     #     name='PostFit',
#     # )
#     plot_limits = varial.tools.ToolChain('LimitsWithGraphs',[
#             LimitGraphs(
#                 limit_path='../../ThetaLimit',
#                 plot_obs=varial.settings.plot_obs,
#                 plot_1sigmabands=True,
#                 plot_2sigmabands=True,
#                 ),
#             varial.plotter.Plotter(
#                 name='LimitCurvesCompared',
#                 input_result_path='../LimitGraphs',
#                 # filter_keyfunc=lambda w: 'Uncleaned' in w.legend,
#                 # plot_setup=plot_setup,
#                 hook_loaded_histos=limit_curve_loader_hook,
#                 plot_grouper=lambda ws: varial.gen.group(
#                         ws, key_func=lambda w: w.save_name),
#                 # save_name_func=varial.plotter.save_by_name_with_hash
#                 save_name_func=lambda w: w.save_name,
#                 plot_setup=lambda w: plot_setup_graphs(w,
#                     th_x=common_sensitivity.theory_masses,
#                     th_y=common_sensitivity.theory_cs),
#                 canvas_decorators=[
#                     # varial.rendering.Legend(x_pos=0.85, y_pos=0.5, label_width=0.2, label_height=0.07),
#                     # varial.rendering.TitleBox(text='#scale[1.2]{#bf{#it{Work in Progress}}}')
#                     ],
#                 save_lin_log_scale=True
#                 ),
#             ])
#     if sys_pat:
#         sys_loader = varial.tools.HistoLoader(
#             name='HistoLoaderSys',
#             filter_keyfunc=lambda w: filter_keyfunc(w) and 'ak4_pt' not in w.file_path,
#             pattern=sys_pat,
#             hook_loaded_histos=loader_hook_sys(brs)
#         )
#         return [loader, sys_loader, plotter, limits, plot_limits, postfit] # , plotter_postfit
#     else:
#         return [loader, plotter, limits, plot_limits]

def select_no_sig(list_region):
    def tmp(wrp):
        # print "before selecting: "+wrp.file_path
        # print file_path
        # print name
        if (wrp.file_path.endswith('.root')
                # and name in wrp.file_path
                and ('Run2015CD' not in wrp.file_path or varial.settings.plot_obs)
                and wrp.in_file_path.endswith('ST')
                and (any(a in wrp.file_path for a in back_plus_data)
                    # or any(signal+f in wrp.file_path for f in final_states_to_use)
                    )
                and all(a not in wrp.file_path for a in datasets_not_to_use)
                and (any(wrp.in_file_path.split('/')[0] == a for a in list_region))) :
            # print wrp
            return True
    return tmp

def select_single_sig(signal, list_region):
    def tmp(wrp):
        # print "before selecting: "+wrp.file_path
        # print file_path
        # print name
        if (wrp.file_path.endswith('.root')
                # and name in wrp.file_path
                and ('Run2015CD' not in wrp.file_path or varial.settings.plot_obs)
                and wrp.in_file_path.endswith('ST')
                and (any(a in wrp.file_path for a in back_plus_data)
                    or any(signal+f in wrp.file_path for f in final_states_to_use))
                and all(a not in wrp.file_path for a in datasets_not_to_use)
                and (any(wrp.in_file_path.split('/')[0] == a for a in list_region))) :
            # print wrp
            return True
    return tmp

def mk_limit_tc_single(brs, filter_keyfunc, signal='', sys_pat=None, selection='', pattern=None, dict_uncerts=None):
    loader = varial.tools.HistoLoader(
        name='HistoLoader',
        pattern=pattern,
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
        name='ThetaLimit',
        # input_path= '../HistoLoader',
        cat_key=lambda w: w.category,
        sys_key=lambda w: w.sys_info,
        # name= 'ThetaLimitsSplit'+str(ind),
        asymptotic=varial.settings.asymptotic,
        brs=brs,
        model_func= lambda w: model_vlqpair.get_model(w, signal, dict_uncerts),
        selection=selection
        # do_postfit=False,
    )
    if sys_pat:
        sys_loader = varial.tools.HistoLoader(
            name='HistoLoaderSys',
            filter_keyfunc=filter_keyfunc,
            pattern=sys_pat,
            hook_loaded_histos=loader_hook(brs)
        )
        postfit = ThetaPostFitPlot(
            name='PostFit',
            input_path='../ThetaLimit'
        )
        corr_mat = CorrelationMatrix(
            input_path='../ThetaLimit',
            proc_name=signal
            )
        corr_plotter = varial.plotter.Plotter(
            name='CorrelationPlot',
            input_result_path='../CorrelationMatrix',
            plot_setup=lambda w: add_draw_option(w, 'col text'),
            # save_name_func=lambda w: w.save_name,
            canvas_decorators=[
                        varial.rendering.TextBox(textbox=TLatex(0.16, 0.89, "#scale[0.7]{#bf{CMS}} #scale[0.6]{#it{Preliminary}}")),
                        varial.rendering.TextBox(textbox=TLatex(0.67, 0.89, "#scale[0.5]{2.7 fb^{-1} (13 TeV)}")),]
            )
        # plotter_postfit = varial.tools.Plotter(
        #     # filter_keyfunc=lambda w: '700' in w.sample 
        #     #                          or '900' in w.sample 
        #     #                          or not w.is_signal,
        #     plot_grouper=lambda ws: varial.gen.group(
        #         ws, key_func=lambda w: w.category),
        #     plot_setup=lambda w: varial.gen.mc_stack_n_data_sum(w, None, True),
        #     save_name_func=lambda w: w.category,
        #     hook_canvas_post_build=varial.gen.add_sample_integrals,
        #     hook_loaded_histos=lambda w: scale_bkg_postfit(
        #         w, '../Limit'+name),
        #     # name='PostFitPlot',
        # )
        return [loader, plotter, sys_loader, limits, postfit] #, corr_mat, corr_plotter # , plotter_postfit
    else:
        return [loader, plotter, limits]


# tool_list.append(TriangleLimitPlots())

def mk_limit_chain(name='Ind_Limits', mk_limit_list=None):
    return varial.tools.ToolChainParallel(
        name, lazy_eval_tools_func=mk_limit_list, n_workers=1
        )

def add_draw_option(wrps, draw_option=''):
    for wrp in wrps:
        if type(wrp) == wrappers.HistoWrapper:
            wrp.draw_option = draw_option
        yield wrp

def plot_setup_triangle(opt):
    def tmp(grps):
        grps = (add_draw_option(ws, opt) for ws in grps)
        grps = (gen.apply_markercolor(ws, colors=[1]) for ws in grps)
        # print grps.grps[0].type
        return grps
    return tmp



def calc_intersection(graph1, graph2):
    for x in xrange(700, 1800, 10):
        y11 = graph1.Eval(x)
        y21 = graph2.Eval(x)
        y12 = graph1.Eval(x+10)
        y22 = graph2.Eval(x+10)
        if (y11 > y21 and y12 < y22) or (y11 < y21 and y12 > y22) or y11 == y21:
            return x

def plot_calc_intersect(grps):
    for g in grps:
        exp_graph = None
        obs_graph = None
        th_graph = None
        for w in g:
            if hasattr(w, 'is_exp'):
                exp_graph = w.graph
            if hasattr(w, 'is_obs'):
                obs_graph = w.graph
            if hasattr(w, 'is_th'):
                th_graph = w.graph
        if exp_graph and th_graph:
            expintersect = calc_intersection(exp_graph, th_graph)
            setattr(g[0], 'exp_mass_excl', expintersect)
        if obs_graph and th_graph:
            obsintersect = calc_intersection(obs_graph, th_graph)
            setattr(g[0], 'obs_mass_excl', obsintersect)
        yield g

def plot_setup_graphs(grps, th_x=None, th_y=None):
    # grps = varial.plotter.default_plot_colorizer(grps)
    grps = add_th_curve(grps, th_x, th_y, min_thy=1e-2)
    grps = plot_calc_intersect(grps)
    # print list(grps)
    return grps

class DrawLess700(util.Decorator):
    """
    Draw Textbox.

    Instanciate with textbox argument:
    ``tb = TextBox(textbox=ROOT.TLatex(0.5, 0.5, 'My Box'))``.
    """

    def configure(self):
        self.decoratee.configure()
        rnd = self.renderers[0]
        rnd = rnd.histo
        self.list_coords = []
        for x_bin in xrange(rnd.GetNbinsX()+1):
            for y_bin in xrange(rnd.GetNbinsY()+1):
                cont = rnd.GetBinContent(x_bin, y_bin)
                if cont > 0. and cont < 1.:
                    x = rnd.GetXaxis().GetBinCenter(x_bin)
                    y = rnd.GetYaxis().GetBinCenter(y_bin)
                    self.list_coords.append((x, y))

    def do_final_cosmetics(self):
        self.decoratee.do_final_cosmetics()
        boxes = TLatex()
        boxes.SetTextSize(0.024)
        boxes.SetTextAlign(22)
        for x, y in self.list_coords:
            boxes.DrawLatex(x, y, '< 700')
        # self.dec_par['textbox'].SetNDC()
        # self.dec_par['textbox'].Draw()

def mk_tc(dir_limit='Limits', mk_limit_list=None):
# setattr(lim_wrapper, 'save_name', 'tH%.0ftZ%.0fbW%.0f'\
        #    % (wrp.brs['th']*100, wrp.brs['tz']*100, wrp.brs['bw']*100))
    return varial.tools.ToolChain(dir_limit, [
        mk_limit_chain(mk_limit_list=mk_limit_list),
        varial.tools.ToolChain('LimitTriangle',[
                TriangleMassLimitPlots(
                    limit_rel_path='../Ind_Limits/Limit*/LimitsWithGraphs/LimitCurvesCompared'
                    ),
                varial.plotter.Plotter(
                    name='PlotterBoxExp',
                    input_result_path='../TriangleMassLimitPlots',
                    filter_keyfunc=lambda w: 'exp' in w.save_name,
                    plot_setup=plot_setup_triangle('col text'),
                    save_name_func=lambda w: w.save_name,
                    canvas_decorators=[DrawLess700,
                                varial.rendering.TextBox(textbox=TLatex(0.16, 0.89, "#scale[0.7]{#bf{CMS}} #scale[0.6]{#it{Simulation}}")),
                                varial.rendering.TextBox(textbox=TLatex(0.67, 0.89, "#scale[0.5]{2.7 fb^{-1} (13 TeV)}")),]
                    ),
                varial.plotter.Plotter(
                    name='PlotterBoxObs',
                    input_result_path='../TriangleMassLimitPlots',
                    filter_keyfunc=lambda w: 'obs' in w.save_name,
                    plot_setup=plot_setup_triangle('col text'),
                    save_name_func=lambda w: w.save_name,
                    canvas_decorators=[DrawLess700,
                                varial.rendering.TextBox(textbox=TLatex(0.16, 0.89, "#scale[0.7]{#bf{CMS}} #scale[0.6]{#it{Preliminary}}")),
                                varial.rendering.TextBox(textbox=TLatex(0.67, 0.89, "#scale[0.5]{2.7 fb^{-1} (13 TeV)}")),]
                    ),
                varial.plotter.Plotter(
                    name='PlotterCont',
                    input_result_path='../TriangleMassLimitPlots',
                    plot_setup=plot_setup_triangle('contz'),
                    save_name_func=lambda w: w.save_name,
                    canvas_decorators=()
                    ),
                ]),
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

