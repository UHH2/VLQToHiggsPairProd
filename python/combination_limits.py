#!/usr/bin/env python

# import UHH2.VLQSemiLepPreSel.vlq_settings as vlq_settings
# import UHH2.VLQSemiLepPreSel.common as vlq_common
import varial.tools
import os
import glob
import sys

import common_plot
import plot as plot
from varial.extensions import git, limits


varial.settings.max_num_processes = 24
varial.settings.max_open_root_files = 1500

import sensitivity
import model_vlqpair
import theta_combined_template
import common_sensitivity
from get_eff_count import CountTable, EffTable # EffNumTable,

base_path = '/nfs/dust/cms/user/nowatsd/sFrameNew/RunII_76X_v1/CMSSW_7_6_3/src/UHH2/VLQToHiggsPairProd/NewSamples-76X-v1/Julie_files/templates_minMlb_'
file_suffix = '_2p318fb_rebinnedDV.root'
br_list = (
    'bW0p5_tZ0p25_tH0p25',
    # 'bW0p0_tZ0p0_tH1p0',
    # 'bW0p0_tZ0p2_tH0p8',
    # 'bW0p0_tZ0p4_tH0p6',
    # 'bW0p0_tZ0p5_tH0p5',
    # 'bW0p0_tZ0p6_tH0p4',
    # 'bW0p0_tZ0p8_tH0p2',
    # 'bW0p0_tZ1p0_tH0p0',
    # 'bW0p2_tZ0p0_tH0p8',
    # 'bW0p2_tZ0p2_tH0p6',
    # 'bW0p2_tZ0p4_tH0p4',
    # 'bW0p2_tZ0p6_tH0p2',
    # 'bW0p2_tZ0p8_tH0p0',
    # 'bW0p4_tZ0p0_tH0p6',
    # 'bW0p4_tZ0p2_tH0p4',
    # 'bW0p4_tZ0p4_tH0p2',
    # 'bW0p4_tZ0p6_tH0p0',
    # 'bW0p6_tZ0p0_tH0p4',
    # 'bW0p6_tZ0p2_tH0p2',
    # 'bW0p6_tZ0p4_tH0p0',
    # 'bW0p8_tZ0p0_tH0p2',
    # 'bW0p8_tZ0p2_tH0p0',
    # 'bW1p0_tZ0p0_tH0p0',
    )
signals = [
    'TTM700',
    'TTM800',
    'TTM900',
    'TTM1000',
    'TTM1100',
    'TTM1200',
    'TTM1300',
    'TTM1400',
    'TTM1500',
    'TTM1600',
    'TTM1700',
    'TTM1800',
]
dict_uncerts = {
    'TTbar' : 1.10,
    'WJets' : 1.10,
    'QCD' : 2.0,
    'DYJets' : 1.2,
    'SingleTop' : 1.2,
}

x_axis_lim="m_{T} [GeV]"
y_axis_lim="Upper limit on #sigma(pp #rightarrow TT)[pb]"


def mk_limit_tc(brs, input_path, model_func, signal=''):
    # def tmp():
    limits = common_sensitivity.TpTpThetaLimitsFromFile(
        name='ThetaLimit',
        input_path=input_path,
        # name= 'ThetaLimitsSplit'+str(ind),
        asymptotic=True,
        brs=brs,
        # model_func=lambda w: model_func(w, signal)
        model_func=model_func
        # do_postfit=False,
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
                    varial.rendering.TextBox(textbox=TLatex(0.67, 0.89, "#scale[0.5]{2.6 fb^{-1} (13 TeV)}")),
                    ],
        raise_on_no_histograms=False
        )
    return [limits, postfit, corr_mat, corr_plotter] # post_loader, plotter_postfit, 
        # return tmp


def mk_limit_list(output_name):
    def tmp():
        limit_list = []
        for br_str, brs_ in br_list:
            # if ind > 5: break
            tc = []
            tc.append(varial.tools.ToolChainParallel(
                'ThetaLimits', list(varial.tools.ToolChain(
                    sig, mk_limit_tc(
                        brs_,
                        base_path+sig+br_str+file_suffix,
                        sig,
                        theta_combined_template.get0H_model
                    ))
                for sig in signals)
            ))
            tc.append(varial.tools.ToolChain('LimitsWithGraphs',[
                limits.LimitGraphs(
                    limit_path='../../ThetaLimits/*/ThetaLimit',
                    plot_obs=True,
                    plot_1sigmabands=True,
                    plot_2sigmabands=True,
                    axis_labels=(x_axis_lim, y_axis_lim),
                    ),
                varial.plotter.Plotter(
                    name='LimitCurvesCompared',
                    input_result_path='../LimitGraphs',
                    # filter_keyfunc=lambda w: 'Uncleaned' in w.legend,
                    # plot_setup=plot_setup,
                    hook_loaded_histos=sensitivity.limit_curve_loader_hook(brs_),
                    plot_grouper=lambda ws: varial.gen.group(
                            ws, key_func=lambda w: w.save_name),
                    # save_name_func=varial.plotter.save_by_name_with_hash
                    save_name_func=lambda w: w.save_name,
                    plot_setup=lambda w: sensitivity.plot_setup_graphs(w,
                        th_x=common_sensitivity.theory_masses,
                        th_y=common_sensitivity.theory_cs),
                    keep_content_as_result=True,
                    # hook_canvas_post_build=lambda w: sensitivity.canvas_setup_post(w, max_y=100.),
                    canvas_decorators=[varial.rendering.Legend(x_pos=.7, y_pos=0.7, label_width=0.25, label_height=0.06, text_size=0.036),
                            # varial.rendering.TextBox(textbox=TLatex(0.19, 0.79, "#scale[0.7]{#bf{CMS}}")),
                            # varial.rendering.TextBox(textbox=TLatex(0.19, 0.73, "#scale[0.6]{#it{Preliminary}}")),
                            varial.rendering.TextBox(textbox=TLatex(0.52, 0.89, "#scale[0.5]{2.6 (e), 2.7 (#mu) fb^{-1} (13 TeV)}")),
                        # varial.rendering.TitleBox(text='#scale[1.2]{#bf{#it{Work in Progress}}}')
                        ],
                    # save_lin_log_scale=True
                    ),
                ]))
            tc.append(varial.tools.ToolChain('LimitsWithGraphsNoObs',[
                limits.LimitGraphs(
                    limit_path='../../ThetaLimits/*/ThetaLimit',
                    plot_obs=False,
                    plot_1sigmabands=True,
                    plot_2sigmabands=True,
                    axis_labels=(x_axis_lim, y_axis_lim),
                    ),
                varial.plotter.Plotter(
                    name='LimitCurvesCompared',
                    input_result_path='../LimitGraphs',
                    # filter_keyfunc=lambda w: 'Uncleaned' in w.legend,
                    # plot_setup=plot_setup,
                    hook_loaded_histos=sensitivity.limit_curve_loader_hook(brs_),
                    plot_grouper=lambda ws: varial.gen.group(
                            ws, key_func=lambda w: w.save_name),
                    # save_name_func=varial.plotter.save_by_name_with_hash
                    save_name_func=lambda w: w.save_name,
                    plot_setup=lambda w: sensitivity.plot_setup_graphs(w,
                        th_x=common_sensitivity.theory_masses,
                        th_y=common_sensitivity.theory_cs),
                    keep_content_as_result=True,
                    # hook_canvas_post_build=lambda w: sensitivity.canvas_setup_post(w, max_y=100.),
                    canvas_decorators=[varial.rendering.Legend(x_pos=.7, y_pos=0.7, label_width=0.25, label_height=0.06, text_size=0.036),
                            # varial.rendering.TextBox(textbox=TLatex(0.19, 0.79, "#scale[0.7]{#bf{CMS}}")),
                            # varial.rendering.TextBox(textbox=TLatex(0.19, 0.73, "#scale[0.6]{#it{Simulation}}")),
                            varial.rendering.TextBox(textbox=TLatex(0.52, 0.89, "#scale[0.5]{2.6 (e), 2.7 (#mu) fb^{-1} (13 TeV)}")),
                        # varial.rendering.TitleBox(text='#scale[1.2]{#bf{#it{Work in Progress}}}')
                        ],
                    # save_lin_log_scale=True
                    ),
                ]))
            limit_list.append(
                varial.tools.ToolChain('Limit'+str(ind), tc))
        return limit_list
    return tmp


if __name__ == '__main__':
    output_name = sys.argv[1]
    all_tools = mk_limit_list(output_name)
    varial.tools.Runner(all_tools, default_reuse=False)
    # varial.tools.CopyTool('~/www/vlq_analysis/tight_selection2/',
    #     src=final_dir, use_rsync=True).run()