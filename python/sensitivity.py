#!/usr/bin/env python

import os
import time
import glob
import cPickle
import pprint

import theta_auto

import varial.tools
import varial.generators as gen
import varial.analysis
import varial.wrappers as wrappers
import varial.plotter
import varial.rendering
import varial.settings
import varial.operations
import varial.util as util
import varial.monitor
from ROOT import TLatex, gStyle, TColor
import ROOT
from varial.sample import Sample
from varial.extensions.limits import *
from UHH2.VLQSemiLepPreSel.common import TpTpThetaLimits, TriangleMassLimitPlots, label_axes

import common_sensitivity
import common_plot
import model_vlqpair
import analysis
import plot
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
        br_list.append({
            'bw' : bw_br,
            'th' : th_br,
            'tz' : tz_br
        })

backgrounds_to_use = [
    # 'Run2015CD',
    'QCD',
    'TTbar_split',
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
    # 'ak4_jetpt__minus/TpTp',
    # 'ak4_jetpt__plus/TpTp',
]

# def select_files(categories=None, var=''):
#     def tmp(wrp):
#         file_path = wrp.file_path
#         in_file_path = wrp.in_file_path
#         if (file_path.endswith('.root')
#                 # and 'DATA' not in file_path\
#                 # and in_file_path.endswith('PostSelection/ST')
#                 and ('Run2015CD' not in wrp.file_path or varial.settings.plot_obs)
#                 and in_file_path.endswith(var)
#                 and any(a in wrp.file_path for a in datasets_to_use)
#                 and all(a not in wrp.file_path for a in datasets_not_to_use)
#                 and (any(wrp.in_file_path.split('/')[0] == a for a in categories) if categories else True)) :
#             return True
#     return tmp

st_bounds = [0., 800., 900., 1000., 1200., 1500., 2000., 2500., 3000., 4500., 6500.]

def rebin_st(wrps, bounds):
    for w in wrps:
        if w.in_file_path.endswith('ST'):
            # w = varial.operations.rebin_nbins_max(w, 15)
            if isinstance(bounds, list):
                w = varial.operations.rebin(w, bounds, False)
            elif isinstance(bounds, int):
                w = varial.operations.rebin_nbins_max(w, bounds)
        yield w

def loader_hook(brs, bounds=st_bounds):
    def temp(wrps):
        wrps = common_sensitivity.loader_hook_scale_excl(wrps, brs)
        wrps = rebin_st(wrps, bounds)
        wrps = common_plot.norm_smpl(wrps,
            smpl_fct=common_plot.normfactors,
            # norm_all=(3000./552.67)
            )
        return wrps
    return temp

# def loader_hook_postfit(wrps):
#     wrps = common_plot.add_wrp_info(wrps)
#     wrps = varial.generators.gen_add_wrp_info(
#         wrps, category=lambda w: w.name.split('__')[0],
#         is_data=lambda w: w.name.split('__')[1] == 'DATA',
#         sample=lambda w: w.name.split('__')[1],
#         legend=lambda w: w.name.split('__')[1],
#         )
#     wrps = common_plot.mod_legend(wrps)
#     wrps = label_axes(wrps)
#     wrps = common_plot.mod_title(wrps)
#     wrps = sorted(wrps, key=lambda w: w.category)
#     return wrps

# def loader_hook_triangle(wrps):
#     for w in wrps:
#         if isinstance(w, wrappers.HistoWrapper):
#             w.histo.GetZaxis().SetRangeUser(-100, 100)
#         yield wrps



def limit_curve_loader_hook(brs):
    def tmp(wrps):
        # wrps = list(wrps)
        # wrps = gen.gen_add_wrp_info(wrps, save_name=lambda w: 'tH%.0ftZ%.0fbW%.0f'\
        #    % (brs['th']*100, brs['tz']*100, brs['bw']*100))
        wrps = gen.gen_add_wrp_info(wrps, brs=lambda w: brs)
        wrps = gen.sort(wrps, key_list=['save_name'])
        return wrps
    return tmp

def select_no_sig(list_region):
    def tmp(wrp):
        if (wrp.file_path.endswith('.root')
                # and name in wrp.file_path
                and ('Run2015CD' not in wrp.file_path or varial.settings.plot_obs)
                and wrp.in_file_path.endswith('ST')
                and (any(a in wrp.file_path for a in back_plus_data)
                    # or any(signal+f in wrp.file_path for f in final_states_to_use)
                    )
                and all(a not in wrp.file_path for a in datasets_not_to_use)
                and (any(wrp.in_file_path.split('/')[0] == a for a in list_region))) :
            return True
    return tmp

def select_single_sig(signal, list_region):
    def tmp(wrp):
        if (wrp.file_path.endswith('.root')
                # and name in wrp.file_path
                and ('Run2015CD' not in wrp.file_path or varial.settings.plot_obs)
                and wrp.in_file_path.endswith('ST')
                and (any(a in wrp.file_path for a in back_plus_data)
                    or any(signal+f in wrp.file_path for f in final_states_to_use))
                and all(a not in wrp.file_path for a in datasets_not_to_use)
                and (any(wrp.in_file_path.split('/')[0] == a for a in list_region))) :
            return True
    return tmp



def scale_bkg_postfit(wrps, theta_res_path, signal):
    theta_res = varial.analysis.lookup_result(theta_res_path)
    if not theta_res:
        theta_res = varial.analysis.lookup_result(os.path.join(varial.analysis.cwd, theta_res_path))
    bkg_scl_dict = {}
    try:
        postfit_vals = cPickle.loads(theta_res.postfit_vals)
        postfit_vals = postfit_vals[signal]
        for smpl in analysis.rate_uncertainties:
            s = analysis.rate_uncertainties[smpl][0]
            prior = analysis.rate_uncertainties[smpl][1]
            constr = postfit_vals.get(s, None)
            if constr:
                r, _ = constr[0]
                r = prior**r
            else:
                varial.monitor.message('sensitivity.scale_bkg_postfit', 'WARNING syst uncertainty %s not found. Possible uncertainties: %s' % (s, str(postfit_vals)))
                r = 1.
            bkg_scl_dict[smpl] = r
    except KeyError as e:
        varial.monitor.message('sensitivity.scale_bkg_postfit', 'WARNING loading theta result did not work')
        raise e

    for w in wrps:
        if bkg_scl_dict.get(w.sample, None) and not w.is_signal:
            w.legend = w.legend + ' post-fit'
            w.histo.Scale(1+r)
        yield w



def loader_hook_postfit(wrps, theta_res_path, signal):
    wrps = plot.loader_hook_merge_lep_channels(wrps)
    wrps = scale_bkg_postfit(wrps, theta_res_path, signal)
    return wrps


def stack_setup_postfit(grps, theta_res_path, signal):
    theta_res = varial.analysis.lookup_result(theta_res_path)
    if not theta_res:
        theta_res = varial.analysis.lookup_result(os.path.join(varial.analysis.cwd, theta_res_path))
    unc_dict = {}
    try:
        postfit_vals = cPickle.loads(theta_res.postfit_vals)
        postfit_vals = postfit_vals[signal]
        for s in analysis.shape_uncertainties:
            constr = postfit_vals.get(s, None)
            if constr:
                _, c = constr[0]
            else:
                varial.monitor.message('sensitivity.stack_setup_postfit', 'WARNING syst uncertainty %s not found. Possible uncertainties: %s' % (s, str(postfit_vals)))
                c = 1.
            unc_dict[s] = c
    except KeyError as e:
        varial.monitor.message('sensitivity.stack_setup_postfit', 'WARNING loading theta result did not work')
        raise e

    grps = gen.mc_stack_n_data_sum(grps, calc_sys_integral=True, scl_dict=unc_dict)
    return grps

def plotter_factory_postfit(theta_res_path, signal, **args):
    def tmp(**kws):
        # common_plot.plotter_factory_stack(common_plot.normfactors, **kws)
        # kws['filter_keyfunc'] = lambda w: (f in w.sample for f in datasets_to_plot)
        kws['hook_loaded_histos'] = lambda w: loader_hook_postfit(w, theta_res_path, signal)
        kws['plot_grouper'] = plot.plot_grouper_by_in_file_path_mod
        kws['plot_setup'] = lambda w: stack_setup_postfit(w, theta_res_path, signal)
        kws['stack_setup'] = lambda w: stack_setup_postfit(w, theta_res_path, signal)
        # kws['canvas_decorators'] += [rnd.TitleBox(text='CMS Simulation 20fb^{-1} @ 13TeV')]
        # kws['y_axis_scale'] = 'lin'
        kws['hook_canvas_post_build'] = plot.canvas_setup_post
        # kws['hook_canvas_pre_build'] = common_plot.mod_pre_canv
        kws['canvas_decorators'] = common_plot.get_style()
        kws.update(**args)
        return varial.tools.Plotter(**kws)
    return tmp


def mk_limit_tc_single(brs, signal='', sys_pat=None, selection='', pattern=None, model_func=model_vlqpair.get_model(), **kws):
    # def tmp():
    load_dict = {
        'hook_loaded_histos' : loader_hook(brs)
    }
    load_dict.update(**kws)
    loader = varial.tools.HistoLoader(
        name='HistoLoader',
        pattern=pattern,
        **load_dict
    )
    plotter = varial.tools.Plotter(
        name='Plotter',
        input_result_path='../HistoLoader',
        plot_grouper=lambda ws: varial.gen.group(
            ws, key_func=lambda w: w.category),
        plot_setup=lambda w: varial.gen.mc_stack_n_data_sum(w, None, True),
        save_name_func=lambda w: w.category,
        hook_canvas_post_build=varial.gen.add_sample_integrals,
    )
    limits = TpTpThetaLimits(
        name='ThetaLimit',
        # input_path= '../HistoLoader',
        cat_key=lambda w: w.category,
        sys_key=lambda w: w.sys_info,
        # name= 'ThetaLimitsSplit'+str(ind),
        asymptotic=varial.settings.asymptotic,
        brs=brs,
        model_func=lambda w: model_func(w, signal),
        selection=selection
        # do_postfit=False,
    )
    if sys_pat:
        sys_loader = varial.tools.HistoLoader(
            name='HistoLoaderSys',
            pattern=sys_pat,
            **load_dict
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
            plot_setup=plot_setup_corr_matrix('colz text'),
            # hook_loaded_histos=loader_hook_triangle,
            # save_name_func=lambda w: w.save_name,
            canvas_decorators=[
                        # varial.rendering.TextBox(textbox=TLatex(0.16, 0.89, "#scale[0.7]{#bf{CMS}} #scale[0.6]{#it{Preliminary}}")),
                        varial.rendering.TextBox(textbox=TLatex(0.67, 0.89, "#scale[0.5]{2.7 fb^{-1} (13 TeV)}")),
                        ]
            )
        return [loader, plotter, sys_loader, limits, postfit, corr_mat, corr_plotter] # post_loader, plotter_postfit, 
    else:
        return [loader, plotter, limits]
        # return tmp


def mk_tc_postfit(brs, signal='', sys_pat=None, selection='', pattern=None, model_func=model_vlqpair.get_model(), **kws):
    # def tmp():
    return mk_limit_tc_single(brs, signal, sys_pat, selection, pattern, model_func, **kws) +\
        [varial.tools.ToolChain('PostFitPlots', [
            varial.tools.ToolChainParallel('HistoLoaderPost',
                list(varial.tools.HistoLoader(
                    pattern=[i for pat in pattern for i in glob.glob(pat) if g in i]+[i for pat in sys_pat for i in glob.glob(pat) if g in i],
                    filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in plot.less_samples_to_plot_only_th) and\
                        'Region_Comb' not in w.in_file_path and\
                        any(w.in_file_path.endswith(f) for f in ['ST', 'HT', 'n_ak4', 'topjets[0]', 'topjets[1]',
                            'n_ak8', 'met', 'pt_ld_ak4_jet', 'pt_subld_ak4_jet', 'jets[2].m_pt','jets[3].m_pt', 'jets[].m_pt', 'n_additional_btags_medium', 'n_prim_vertices',
                            'n_higgs_tags_1b_med', 'n_higgs_tags_2b_med', 'primary_electron_pt', 'primary_muon_pt', 'PrimaryLepton.Particle.m_eta', 'wtags_mass_softdrop',
                            'nobtag_boost_mass_nsjbtags', 'nomass_boost_1b_mass_softdrop', 'nomass_boost_2b_mass_softdrop', 'noboost_mass_1b[0].m_pt', 'noboost_mass_2b[0].m_pt']),
                    hook_loaded_histos=plot.loader_hook_merge_regions,
                    name='HistoLoader_'+g,
                    lookup_aliases=False,
                    raise_on_empty_result=False
                    ) for g in plot.less_samples_to_plot_only_th)),
            plot.mk_toolchain('HistogramsPostfit',
                plotter_factory=plotter_factory_postfit('../../../../ThetaLimit', signal),
                pattern=None,
                input_result_path='../HistoLoaderPost/HistoLoader*',
                # auto_legend=False,
                # name='HistogramsPostfit',
                # lookup_aliases=varial.settings.lookup_aliases
                )
            ])]
    # return tmp

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

def plot_setup_corr_matrix(opt):
    gStyle.SetPalette(1) # kBird
    gStyle.SetPaintTextFormat('.2f')
    def tmp(grps):
        grps = (add_draw_option(ws, opt) for ws in grps)
        return grps
    return tmp

def plot_setup_triangle(opt):
    def tmp(grps):
        grps = (add_draw_option(ws, opt) for ws in grps)
        grps = (gen.apply_markercolor(ws, colors=[1]) for ws in grps)
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

def mk_tc(dir_limit='Limits', mk_limit_list=None, mk_triangle=True):
# setattr(lim_wrapper, 'save_name', 'tH%.0ftZ%.0fbW%.0f'\
        #    % (wrp.brs['th']*100, wrp.brs['tz']*100, wrp.brs['bw']*100))
    tc = [mk_limit_chain(mk_limit_list=mk_limit_list)]
    if mk_triangle:
        tc.append(varial.tools.ToolChain('LimitTriangle',[
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
            ]))
    return varial.tools.ToolChain(dir_limit, tc)

# tc = varial.tools.ToolChain("", [tc])

if __name__ == '__main__':
    time.sleep(1)
    varial.tools.Runner(mk_tc())
    # os.chdir(dir_limit)
    # # varial.tools.WebCreator().run()
    # os.chdir('..') 

