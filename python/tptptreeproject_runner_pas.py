#!/usr/bin/env python

import UHH2.VLQSemiLepPreSel.vlq_settings as vlq_settings
import UHH2.VLQSemiLepPreSel.common as vlq_common
from varial.extensions.hadd import Hadd
import varial.extensions.make
import varial.tools
import varial.generators as gen
import os
import glob
import sys
import pprint
import ast
# import varial.analysis as analysis
from ROOT import TLatex
import cPickle

import common_plot
import plot as plot
from varial.extensions import git, limits


varial.settings.max_num_processes = 24
varial.settings.max_open_root_files = 1500

# if len(sys.argv) < 2:
#     print 'Provide output dir!'
#     exit(-1)

# dir_name = sys.argv[1]
uhh_base = os.getenv('CMSSW_BASE') + '/src/UHH2/'
analysis_base = os.getcwd()
# base_path = '/nfs/dust/cms/user/nowatsd/sFrameNew/'\
#     'RunII-25ns-v2/CMSSW_7_4_15_patch1/src/UHH2/VLQToHiggsPairProd/'\
#     'Samples-25ns-v2/TpTpFinalSelectionTreeOutput-v0wBTagSF/Files_and_Plots/'\
#     'Files_and_Plots_nominal/SFrame/nominal/workdir/uhh2.AnalysisModuleRunner.*.root'

# varial.settings.pretty_names.update({
#      'no sel._tex':                 r'no sel.',
#      'trigger_accept_tex':          r'trigger',
#      '2D cut_tex':                  r'2D-iso',
#      'primary_lepton_pt_tex':       r'lep. \pt',
#      'leading_jet_pt_tex':          r'ld. jet \pt',
#      'ST_tex':                      r'ST',
#      'event_chi2_tex':              r'$\chi^2$',
#      'dr_higg_top_tex':             r'$\Delta R(H, t)$',
#      'tlep_pt_tex':                 r't \pt',
#      'h_mass_tex':                  r'$M(H)$',
#      '1000 X output/input_tex':     r'$\epsilon$ * 1000'
# })


# these imports might need the settings above
# import sframe_tools
import treeproject_tptp
import sensitivity
import model_vlqpair
import common_sensitivity
import tex_content
import analysis
from get_eff_count import CountTable, EffTable # EffNumTable, 

varial.settings.plot_obs = True
varial.settings.asymptotic = False
varial.settings.merge_decay_channels = True

varial.settings.style = 'PAS'

all_regions = [
    'SignalRegion2b_Mu45',
    'SignalRegion1b_Mu45',
    'SidebandRegion_Mu45',
    'SignalRegion2b_El45',
    'SignalRegion1b_El45',
    'SidebandRegion_El45',
]
cr_only_regions = [
    # 'SidebandRegion_El45',
    # 'SidebandRegion_Mu45',
    'SidebandTTJetsRegion_El45',
    'SidebandTTJetsRegion_Mu45',
    'SidebandWPlusJetsRegion_El45',
    'SidebandWPlusJetsRegion_Mu45',
]

br_list_all = []

# only br_th = 100% for now
w_max = 1
# w_max = 0
for w_br in [i/10. for i in xrange(0, int(w_max*10)+2, 2)]:
    z_max = 1.0-w_br
    # z_max = 0
    for z_br in [ii/10. for ii in xrange(0, int(z_max*10)+2, 2)]:
        h_br = 1-w_br-z_br
        # print w_br, h_br, z_br
        br_list_all.append({
            'w' : w_br,
            'h' : h_br,
            'z' : z_br,
        })

br_list_th_only = [{
            'w' : 0.,
            'h' : 1.,
            'z' : 0.,
        }]

br_list_thbw = [{
            'w' : 0.5,
            'h' : 0.5,
            'z' : 0.,
        }]

def mk_limit_plot_tc(lim_path,
        x_axis_lim="m_{T} [GeV]",
        y_axis_lim="upper limit on #sigma_{TT} #times BR(T #rightarrow tH) [pb]"):
    def tmp():
        # if ind > 5: break
        tc = []
        tc.append(varial.tools.ToolChain('LimitsWithGraphs',[
            limits.LimitGraphs(
                limit_path=lim_path,
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
                hook_loaded_histos=sensitivity.limit_curve_loader_hook(br_list_th_only),
                plot_grouper=lambda ws: varial.gen.group(
                        ws, key_func=lambda w: w.save_name),
                # save_name_func=varial.plotter.save_by_name_with_hash
                save_name_func=lambda w: w.save_name,
                plot_setup=lambda w: sensitivity.plot_setup_graphs(w,
                    th_x=common_sensitivity.theory_masses,
                    th_y=common_sensitivity.theory_cs),
                keep_content_as_result=True,
                canvas_decorators=[varial.rendering.Legend(x_pos=.75, y_pos=0.7, label_width=0.2, label_height=0.05),
                        varial.rendering.TextBox(textbox=TLatex(0.16, 0.89, "#scale[0.7]{#bf{CMS}} #scale[0.6]{#it{Preliminary}}")),
                        varial.rendering.TextBox(textbox=TLatex(0.67, 0.89, "#scale[0.5]{2.7 fb^{-1} (13 TeV)}")),
                    # varial.rendering.TitleBox(text='#scale[1.2]{#bf{#it{Work in Progress}}}')
                    ],
                # save_lin_log_scale=True
                ),
            ]))
        # tc.append(varial.tools.ToolChain('LimitsWithGraphsNoObs',[
        #     limits.LimitGraphs(
        #         limit_path='../../ThetaLimits/*/ThetaLimit',
        #         plot_obs=False,
        #         plot_1sigmabands=True,
        #         plot_2sigmabands=True,
        #         axis_labels=(x_axis_lim, y_axis_lim),
        #         ),
        #     varial.plotter.Plotter(
        #         name='LimitCurvesCompared',
        #         input_result_path='../LimitGraphs',
        #         # filter_keyfunc=lambda w: 'Uncleaned' in w.legend,
        #         # plot_setup=plot_setup,
        #         hook_loaded_histos=sensitivity.limit_curve_loader_hook(brs_),
        #         plot_grouper=lambda ws: varial.gen.group(
        #                 ws, key_func=lambda w: w.save_name),
        #         # save_name_func=varial.plotter.save_by_name_with_hash
        #         save_name_func=lambda w: w.save_name,
        #         plot_setup=lambda w: sensitivity.plot_setup_graphs(w,
        #             th_x=common_sensitivity.theory_masses,
        #             th_y=common_sensitivity.theory_cs),
        #         keep_content_as_result=True,
        #         canvas_decorators=[varial.rendering.Legend(x_pos=.75, y_pos=0.7, label_width=0.2, label_height=0.05),
        #                 varial.rendering.TextBox(textbox=TLatex(0.16, 0.89, "#scale[0.7]{#bf{CMS}} #scale[0.6]{#it{Simulation}}")),
        #                 varial.rendering.TextBox(textbox=TLatex(0.67, 0.89, "#scale[0.5]{2.7 fb^{-1} (13 TeV)}")),
        #             # varial.rendering.TitleBox(text='#scale[1.2]{#bf{#it{Work in Progress}}}')
        #             ],
        #         # save_lin_log_scale=True
        #         ),
        #     ]))
        return tc
    return tmp


all_uncerts = [
    'jec',
    'jer',
    'btag_bc',
    'btag_udsg',
    'sfmu_id',
    'sfmu_trg',
    'sfel_id',
    'sfel_trg',
    'pu',
    'PDF',
    'ScaleVar',
    'rate',
    'PSScale',
    'higgs_smear',
    # 'top_pt_weight',
    'ht_reweight',
    # 'sflep_id',
    # 'sflep_trg'
]

analysis.shape_uncertainties.update(dict((a, 1.) for a in all_uncerts))


# varial.settings.lookup_aliases = False

def make_tp_plot_chain(name, base_path, output_dir, uncertainties=None, br_list=br_list_th_only):


    sys_path = output_dir+'/%s/TreeProject/SysTreeProjectors' % name
    
    def get_sys_dir():
        return set(sys.split('__')[0] for d in glob.glob(sys_path) for sys in os.listdir(d) if all(g not in sys for g in ['Norm', 'SysTreeProjectors']))

    def unselect_theory_uncert(wrp):
        sample = os.path.basename(wrp.file_path)
        sample = os.path.splitext(sample)[0]
        sample = sample.split('-')[-1]
        if any(s == sample for s in [treeproject_tptp.ttbar_smpl, 'WJets']):
            if any(g in wrp.file_path for g in ['ScaleVar', 'PDF']):
                return False
        if 'PSScale' in wrp.file_path:
            return False
        return True

    def mk_tc_sens():

        def select_sig_htrew(list_region, tp_path):
            def sel_sig(signal):
                def tmp(wrp):
                    if (wrp.file_path.endswith('.root')
                            # and name in wrp.file_path
                            and ('Run2015CD' not in wrp.file_path or varial.settings.plot_obs)
                            and wrp.in_file_path.endswith('ST')
                            and (any(a in wrp.file_path for a in sensitivity.back_plus_data)
                                or any(signal+f in wrp.file_path for f in sensitivity.final_states_to_use))
                            and all(a not in wrp.file_path for a in sensitivity.datasets_not_to_use)
                            and (any(wrp.in_file_path.split('/')[0] == a for a in list_region))
                            and ((tp_path in wrp.file_path and 'TpTp' in wrp.file_path) or 'TpTp' not in wrp.file_path)):
                        return True
                return tmp
            return sel_sig


        def unselect_theory_uncert_single_sig(list_region):
            def sel_sig(signal):
                def tmp(wrp):
                    if (wrp.file_path.endswith('.root')
                            # and name in wrp.file_path
                            and ('Run2015CD' not in wrp.file_path or varial.settings.plot_obs)
                            and wrp.in_file_path.endswith('ST')
                            and (any(a in wrp.file_path for a in sensitivity.back_plus_data)
                                or any(signal+f in wrp.file_path for f in sensitivity.final_states_to_use))
                            and all(a not in wrp.file_path for a in sensitivity.datasets_not_to_use)
                            and (any(wrp.in_file_path.split('/')[0] == a for a in list_region))
                            and unselect_theory_uncert(wrp)):
                        return True
                return tmp
            return sel_sig

        uncerts = uncertainties or get_sys_dir()
        rate_uncerts_part = dict((s, r) for s, r in analysis.rate_uncertainties.iteritems() if s not in ['TTbar', 'WJets'])
        # sys_uncerts = list(i for i in all_uncerts if all(g not in i for g in ['ScaleVar', 'PSScale', 'PDF']))

        lim_list = []
        lim_list += [
            # post-fit distributions and event yields - or use plots above? check Zprime analysis
            varial.tools.ToolChain(
                'BackgroundOnlyFitNoTheoryAllRegions',
                sensitivity.mk_tc_postfit_plot(os.path.join(output_dir, name)+'/Limit/BackgroundOnlyFitNoTheoryAllRegions/ThetaLimit/'),
                    signal='', sys_pat=list(sys_path+'/%s*/*.root'% i for i in all_uncerts), sys_uncerts=all_uncerts,
                    rate_uncertainties=sensitivity.get_constr_uncerts(os.path.join(os.path.join(analysis_base, output_dir), name)+\
                        '/Limit/BackgroundOnlyFitNoTheoryCR/PostFitPlots/HistogramsPostfit/StackedAll/BaseLineSelection/_varial_infodata.pkl',
                        analysis.rate_uncertainties),
                    pattern=[os.path.join(output_dir, name)+'/TreeProject/TreeProjector/*.root'],
                    filter_plots=unselect_theory_uncert, include_rate=False
                ),
        ]
        lim_list += [            
            # final limits with all BRs
            sensitivity.mk_tc('TTLimitsNoTheoryAllRegionsFinal', mk_limit_plot_tc(
                os.path.join(output_dir, name)+'/Limit/TTLimitsNoTheoryAllRegionsFinal/Ind_Limits/Limit0/ThetaLimits/*/ThetaLimit/'),
                limit_rel_path=os.path.join(output_dir, name)+'/Limit/TTLimitsNoTheoryAllRegionsFinal/Ind_Limits/Limit*/LimitsWithGraphs/LimitCurvesCompared/'
                ),
            # sensitivity.mk_tc('BBLimitsNoTheoryAllRegionsFinal', mk_limit_plot_tc(
            #         output_dir,
            #         name,
            #         list(sys_path+'/%s*/*.root'% i for i in all_uncerts)+list(sys_path+'BB/%s*/*.root'% i for i in all_uncerts),
            #         all_regions,
            #         pattern=[os.path.join(output_dir, name)+'/TreeProject/TreeProjector/*.root', os.path.join(output_dir, name)+'/TreeProject/TreeProjectorBB/*.root'],
            #         br_list=br_list_all,
            #         model_func=model_vlqpair.get_model_constr_uncerts(os.path.join(os.path.join(analysis_base, output_dir), name)+\
            #             '/Limit/BackgroundOnlyFitNoTheoryCR/PostFitPlots/HistogramsPostfit/StackedAll/BaseLineSelection/_varial_infodata.pkl',
            #             analysis.rate_uncertainties),
            #         signals=treeproject_tptp.bpbp_signals,
            #         filter_func=unselect_theory_uncert_single_sig(all_regions),
            #         x_axis_lim="m_{B} [GeV]",
            #         y_axis_lim="#sigma(pp #rightarrow BB)[pb]"
            #         ),
            #     leg_x='BR(B #rightarrow bH)', leg_y='BR(B #rightarrow bZ)'),

            # plot.mk_toolchain('HistogramsCompUncertsShape', plot.less_samples_to_plot_only_th,
            #             pattern=[os.path.join(output_dir, name)+'/TreeProject/TreeProjector/*.root',
            #                 os.path.join(output_dir, name)+'/TreeProject/TreeProjectorHTSignal/*.root',
            #                 sys_path+'/ht_reweight*/*.root', sys_path+'HTSignal/ht_reweight*/*.root'],
            #             filter_keyfunc=select_sig_htrew(all_regions, 'HTSignal/')('TpTp_M-1200'),   
            #             plotter_factory=plot.plotter_factory_uncerts()),
            # plot.mk_toolchain('HistogramsCompUncertsUncOnly', plot.less_samples_to_plot_only_th,
            #             pattern=[os.path.join(output_dir, name)+'/TreeProject/TreeProjector/*.root',
            #                 os.path.join(output_dir, name)+'/TreeProject/TreeProjectorHTSignalUncOnly/*.root',
            #                 sys_path+'/ht_reweight*/*.root', sys_path+'HTSignalUncOnly/ht_reweight*/*.root',
            #                 ],
            #             filter_keyfunc=select_sig_htrew(all_regions, 'HTSignalUncOnly/')('TpTp_M-1200'),   
            #             plotter_factory=plot.plotter_factory_uncerts(),
            #             lookup_aliases=False),
        ]
        return lim_list

    # def mk_tc_plot(style='AN'):
    def mk_tc_plot():
        # def tmp():
        uncerts = uncertainties or get_sys_dir()
        # varial.settings.style = style
        return [

                    ######## HISTOGRAMS WITH LEPTON CHANNELS SEPARATE ########

                    # plot.mk_toolchain('Histograms', plot.less_samples_to_plot_only_th, 
                    #             pattern=[output_dir+'/%s/TreeProject/TreeProjector/*.root'%name]
                    #             + list(sys_path+'/%s*/*.root'% i for i in uncerts)
                    #             ),
                    # plot.mk_toolchain('HistogramsNoTheory', plot.less_samples_to_plot_only_th, 
                    #             pattern=[output_dir+'/%s/TreeProject/TreeProjector/*.root'%name]
                    #             + list(sys_path+'/%s*/*.root'% i for i in uncerts),
                    #             filter_keyfunc=unselect_theory_uncert,
                    #             plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=True)
                    #             ),                                             
                    # plot.mk_toolchain('HistogramsCompUncerts', plot.less_samples_to_plot_only_th,
                    #             pattern=[output_dir+'/%s/TreeProject/TreeProjector/*.root'%name]
                    #             + list(sys_path+'/%s*/*.root'% i for i in uncerts),
                    #             filter_keyfunc=lambda w: any(f in w.file_path for f in [treeproject_tptp.ttbar_smpl, 'WJets', 'TpTp_M-0800', 'TpTp_M-1600']) and any(w.in_file_path.endswith(g) for g in ['ST', 'HT']),   
                    #             plotter_factory=plot.plotter_factory_uncerts()),                                             
                    # plot.mk_toolchain('HistogramsNormToInt', plot.less_samples_to_plot_only_th, 
                    #             pattern=[output_dir+'/%s/TreeProject/TreeProjector/*.root'%name]
                    #             + list(sys_path+'/%s*/*.root'% i for i in uncerts),
                    #             filter_keyfunc=lambda w: 'TpTp' not in w.file_path,
                    #             plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, hook_loaded_histos=plot.loader_hook_norm_to_int,
                    #                 plot_setup=plot.stack_setup_norm_all_to_intgr)),
                    # plot.mk_toolchain('HistogramsNoData', plot.less_samples_to_plot_only_th, 
                    #             pattern=[output_dir+'/%s/TreeProject/TreeProjector/*.root'%name]
                    #             + list(sys_path+'/%s*/*.root'% i for i in uncerts),
                    #             filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in plot.less_samples_to_plot_only_th if 'Run2015CD' not in f)),
                    # plot.mk_toolchain('HistogramsCompFinalStates', plot.less_samples_to_plot_only_th,
                    #             pattern=[output_dir+'/%s/TreeProject/TreeProjector/*.root'%name]
                    #             + list(sys_path+'/%s*/*.root'% i for i in uncerts),
                    #             filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in plot.less_samples_to_plot_only_th if not any(g in w.file_path.split('/')[-1] for g in ['TpTp_M-0800', 'TpTp_M-1600'])),
                    #             plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, hook_loaded_histos=plot.loader_hook_compare_finalstates),
                    #             ),
                    # # # plot.mk_toolchain_pull('HistogramsPull', [output_dir+'/%s/TreeProject/TreeProjector/*.root'%name]
                    # # #             + list(sys_path+'/%s*/*.root'% i for i in uncerts)
                    # # #             ,plot.less_samples_to_plot_only_th),               
                    # # # plot.mk_toolchain('HistogramsNoUncerts', plot.less_samples_to_plot_only_th, 
                    # # #             pattern=[output_dir+'/%s/TreeProject/TreeProjector/*.root'%name],
                    # # #             filter_keyfunc=lambda w: 'TpTp' not in w.file_path
                    # # #             # + list(sys_path+'/%s*/*.root'% i for i in uncerts)
                    # # #             ),

                    ####### MERGE LEPTON CHANNELS ########


                    # varial.tools.ToolChain('MergeChannelsHists', [
                    #     varial.tools.ToolChainParallel('HistoLoader',
                    #     list(varial.tools.HistoLoader(
                    #         pattern=[output_dir+'/%s/TreeProject/TreeProjector/*%s*.root'%(name, g)]+list(sys_path+'/%s*/*%s*.root'% (i, g) for i in uncerts),
                    #         filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in plot.less_samples_to_plot_only_th) and\
                    #             'Region_Comb' not in w.in_file_path and\
                    #             any(w.in_file_path.endswith(f) for f in ['ST', 'HT', 'n_ak4', 'topjets[0].m_pt', 'topjets[1].m_pt',
                    #                 'n_ak8', 'met', 'pt_ld_ak4_jet', 'pt_subld_ak4_jet', 'jets[2].m_pt','jets[3].m_pt', 'jets[].m_pt', 'n_additional_btags_medium', 'n_prim_vertices',
                    #                 'n_higgs_tags_1b_med_sm10', 'n_higgs_tags_2b_med_sm10', 'primary_electron_pt', 'primary_muon_pt', 'PrimaryLepton.Particle.m_eta', 'wtags_mass_softdrop',
                    #                 'nobtag_boost_mass_nsjbtags', 'nomass_boost_1b_mass_softdrop', 'nomass_boost_2b_mass_softdrop', 'noboost_mass_1b[0].m_pt', 'noboost_mass_2b[0].m_pt']),
                    #         hook_loaded_histos=plot.loader_hook_merge_regions,
                    #         name='HistoLoader_'+g,
                    #         lookup_aliases=False,
                    #         raise_on_empty_result=False
                    #         ) for g in plot.less_samples_to_plot_only_th)),
                    #     plot.mk_toolchain('Histograms',
                    #         plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, hook_loaded_histos=plot.loader_hook_merge_lep_channels),
                    #         pattern=None, input_result_path='../HistoLoader/HistoLoader*'),
                    #     plot.mk_toolchain('HistogramsCompUncerts',
                    #         filter_keyfunc=lambda w: any(f in w.file_path for f in [treeproject_tptp.ttbar_smpl, 'WJets', 'TpTp_M-0800', 'TpTp_M-1600']) and any(w.in_file_path.endswith(g) for g in ['ST', 'HT']),   
                    #         plotter_factory=plot.plotter_factory_uncerts(analysis.rate_uncertainties, uncerts, hook_loaded_histos=lambda w: plot.loader_hook_uncerts(plot.loader_hook_merge_lep_channels(w))),
                    #         pattern=None, input_result_path='../HistoLoader/HistoLoader*'),
                    #     plot.mk_toolchain('HistogramsHiggsComp', pattern=None, input_result_path='../HistoLoader/HistoLoader*',
                    #         filter_keyfunc=lambda w: all(g not in w.sample for g in ['TpTp_M-0800', 'TpTp_M-1600']),
                    #         plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, 
                    #             hook_loaded_histos=plot.loader_hook_compare_finalstates,
                    #             # hook_canvas_post_build=lambda w: plot.canvas_setup_post(common_plot.mod_shift_leg(w))
                    #             )
                    #         ),
                    #     plot.mk_toolchain('HistogramsNoDataHiggsComp', pattern=None, input_result_path='../HistoLoader/HistoLoader*',
                    #         filter_keyfunc=lambda w: 'Run2015CD' not in w.file_path.split('/')[-1] and all(g not in w.sample for g in ['TpTp_M-0800', 'TpTp_M-1600']),
                    #         plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, 
                    #             hook_loaded_histos=plot.loader_hook_compare_finalstates,
                    #             # hook_canvas_post_build=lambda w: plot.canvas_setup_post(common_plot.mod_shift_leg(w))
                    #             )
                    #         ),
                    #     # # plot.mk_toolchain('HistogramsNormToInt',
                    #     # #     filter_keyfunc=lambda w: 'TpTp' not in w.file_path,
                    #     # #     pattern=None, input_result_path='../HistoLoader*',
                    #     # #     plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, hook_loaded_histos=plot.loader_hook_norm_to_int,
                    #     # #         plot_setup=plot.stack_setup_norm_all_to_intgr)),
                    #     # # plot.mk_toolchain('HistogramsNoUncerts', filter_keyfunc=lambda w: not w.is_signal and not w.sys_info,
                    #     # #     plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, 
                    #     # #         hook_loaded_histos=plot.loader_hook_merge_lep_channels,
                    #     # #         hook_canvas_post_build=lambda w: common_plot.mod_no_2D_leg(plot.canvas_setup_post(w))
                    #     # #         ),
                    #     # #     pattern=None, input_result_path='../HistoLoader/HistoLoader*'),
                    #     # # plot.mk_toolchain('HistogramsNoUncertsPull', filter_keyfunc=lambda w: not w.is_signal and not w.sys_info,
                    #     # #     plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, 
                    #     # #         hook_loaded_histos=plot.loader_hook_merge_lep_channels,
                    #     # #         hook_canvas_post_build=lambda w: common_plot.mod_no_2D_leg(plot.canvas_setup_post(w)),
                    #     # #         canvas_decorators=[
                    #     # #             varial.rendering.BottomPlotRatioPullErr,
                    #     # #             varial.rendering.Legend,
                    #     # #             ]
                    #     # #         ),
                    #     # #     pattern=None, input_result_path='../HistoLoader/HistoLoader*'),
                    #     # # plot.mk_toolchain('HistogramsNoData', filter_keyfunc=lambda w: not w.is_data,
                    #     # #     plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, hook_loaded_histos=plot.loader_hook_merge_lep_channels),
                    #     # #     pattern=None, input_result_path='../HistoLoader/HistoLoader*'),
                        
                    #     ]),
                    
                    # varial.tools.ToolChain('MergeChannelsHistsNoTheory', [
                    #     varial.tools.ToolChainParallel('HistoLoader',
                    #     list(varial.tools.HistoLoader(
                    #         pattern=[output_dir+'/%s/TreeProject/TreeProjector/*%s*.root'%(name, g)]+list(sys_path+'/%s*/*%s*.root'% (i, g) for i in uncerts),
                    #         filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in plot.less_samples_to_plot_only_th) and\
                    #             'Region_Comb' not in w.in_file_path and\
                    #             any(w.in_file_path.endswith(f) for f in ['ST', 'HT', 'n_ak4', 'topjets[0].m_pt', 'topjets[1].m_pt',
                    #                 'n_ak8', 'met', 'pt_ld_ak4_jet', 'pt_subld_ak4_jet', 'jets[2].m_pt','jets[3].m_pt', 'jets[].m_pt', 'n_additional_btags_medium', 'n_prim_vertices',
                    #                 'n_higgs_tags_1b_med_sm10', 'n_higgs_tags_2b_med_sm10', 'primary_electron_pt', 'primary_muon_pt', 'PrimaryLepton.Particle.m_eta', 'wtags_mass_softdrop',
                    #                 'nobtag_boost_mass_nsjbtags', 'nomass_boost_1b_mass_softdrop', 'nomass_boost_2b_mass_softdrop', 'noboost_mass_1b[0].m_pt', 'noboost_mass_2b[0].m_pt']) and\
                    #             unselect_theory_uncert(w),
                    #         hook_loaded_histos=plot.loader_hook_merge_regions,
                    #         name='HistoLoader_'+g,
                    #         lookup_aliases=False,
                    #         raise_on_empty_result=False
                    #         ) for g in plot.less_samples_to_plot_only_th)),
                    #     plot.mk_toolchain('Histograms',
                    #         plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=True, hook_loaded_histos=plot.loader_hook_merge_lep_channels),
                    #         pattern=None, input_result_path='../HistoLoader/HistoLoader*'),
                    #     plot.mk_toolchain('HistogramsCompUncerts',
                    #         filter_keyfunc=lambda w: any(f in w.file_path for f in [treeproject_tptp.ttbar_smpl, 'WJets', 'TpTp_M-0800', 'TpTp_M-1600']) and any(w.in_file_path.endswith(g) for g in ['ST', 'HT']),   
                    #         plotter_factory=plot.plotter_factory_uncerts(analysis.rate_uncertainties, uncerts, include_rate=True, hook_loaded_histos=lambda w: plot.loader_hook_uncerts(plot.loader_hook_merge_lep_channels(w))),
                    #         pattern=None, input_result_path='../HistoLoader/HistoLoader*'),
                    #     plot.mk_toolchain('HistogramsHiggsComp', pattern=None, input_result_path='../HistoLoader/HistoLoader*',
                    #         filter_keyfunc=lambda w: all(g not in w.sample for g in ['TpTp_M-0800', 'TpTp_M-1600']),
                    #         plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=True, 
                    #             hook_loaded_histos=plot.loader_hook_compare_finalstates,
                    #             # hook_canvas_post_build=lambda w: plot.canvas_setup_post(common_plot.mod_shift_leg(w))
                    #             )
                    #         ),
                    #     plot.mk_toolchain('HistogramsNoDataHiggsComp', pattern=None, input_result_path='../HistoLoader/HistoLoader*',
                    #         filter_keyfunc=lambda w: 'Run2015CD' not in w.file_path.split('/')[-1] and all(g not in w.sample for g in ['TpTp_M-0800', 'TpTp_M-1600']),
                    #         plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=True, 
                    #             hook_loaded_histos=plot.loader_hook_compare_finalstates,
                    #             # hook_canvas_post_build=lambda w: plot.canvas_setup_post(common_plot.mod_shift_leg(w))
                    #             )
                    #         ),
                    #     plot.mk_toolchain('HistogramsNormToInt',
                    #         filter_keyfunc=lambda w: 'TpTp' not in w.file_path,
                    #         pattern=None, input_result_path='../HistoLoader/HistoLoader*',
                    #         plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, hook_loaded_histos=plot.loader_hook_norm_to_int,
                    #             plot_setup=plot.stack_setup_norm_all_to_intgr)),
                    #     ]),



                    ####### MERGE LEPTON CHANNELS, COMBINE FINAL STATES ########
                    
                    # # varial.tools.ToolChain('MergeChannelsHistsCombFinalStates', [
                    # #     varial.tools.HistoLoader(
                    # #         pattern=[output_dir+'/%s/TreeProject/TreeProjector/*.root'%name]+list(sys_path+'/%s*/*.root'% i for i in uncerts),
                    # #         filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in plot.less_samples) and\
                    # #             'Region_Comb' not in w.in_file_path and\
                    # #             any(w.in_file_path.endswith(f) for f in ['nobtag_boost_mass_nsjbtags', 'nomass_boost_1b_mass_softdrop', 'nomass_boost_2b_mass_softdrop', 'noboost_mass_1b[0].m_pt', 'noboost_mass_2b[0].m_pt']),
                    # #         hook_loaded_histos=plot.loader_hook_merge_regions,
                    # #     ),
                    # #     plot.mk_toolchain('Histograms', pattern=None, input_result_path='../HistoLoader',
                    # #         filter_keyfunc=lambda w: all(g not in w.sample for g in ['TpTp_M-0800', 'TpTp_M-1600']),
                    # #         plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, 
                    # #             hook_loaded_histos=plot.loader_hook_compare_finalstates,
                    # #             # hook_canvas_post_build=lambda w: plot.canvas_setup_post(common_plot.mod_shift_leg(w))
                    # #             )
                    # #         ),
                    # #     plot.mk_toolchain('HistogramsNoData', pattern=None, input_result_path='../HistoLoader',
                    # #         filter_keyfunc=lambda w: 'Run2015CD' not in w.file_path.split('/')[-1] and all(g not in w.sample for g in ['TpTp_M-0800', 'TpTp_M-1600']),
                    # #         plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, 
                    # #             hook_loaded_histos=plot.loader_hook_compare_finalstates,
                    # #             # hook_canvas_post_build=lambda w: plot.canvas_setup_post(common_plot.mod_shift_leg(w))
                    # #             )
                    # #         )
                    # #     ]),

                    # ####### TABLES ########

                    # # varial.tools.ToolChain('MergeChannelsTables', [
                    # #     varial.tools.ToolChainParallel('HistoLoader',
                    # #         list(varial.tools.HistoLoader(
                    # #             pattern=[output_dir+'/%s/TreeProject/TreeProjector/*%s*.root'%(name, g)]+list(sys_path+'/%s*/*%s*.root'% (i, g) for i in uncerts),
                    # #             filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in plot.more_samples) and\
                    # #                 'Region_Comb' not in w.in_file_path and\
                    # #                 any(w.in_file_path.endswith(f) for f in ['ST']),
                    # #             hook_loaded_histos=plot.loader_hook_merge_regions,
                    # #             name='HistoLoader_'+g,
                    # #             lookup_aliases=False,
                    # #             raise_on_empty_result=False
                    # #             ) for g in plot.more_samples)),
                    # #     plot.mk_toolchain('Histograms',
                    # #         plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, hook_loaded_histos=plot.loader_hook_merge_lep_channels),
                    # #         pattern=None, input_result_path='../HistoLoader/HistoLoader*'),
                    # #     CountTable([
                    # #             common_plot.table_block_signal,
                    # #             common_plot.table_block_background,
                    # #             [(r'\textbf{Total Background}', lambda w: 'Integral___bkg_sum' in w)],
                    # #             [(r'\textbf{data}', lambda w: 'Integral___Run2015CD' in w)],
                    # #         ],
                    # #         common_plot.get_table_category_block(),
                    # #         name='CountTable'
                    # #         ),
                    # #     EffTable([
                    # #             common_plot.table_block_signal,
                    # #         ],
                    # #         common_plot.get_table_category_block(),
                    # #         common_plot.norm_factors,
                    # #         squash_errs=True,
                    # #         name='EffTable'
                    # #         ),
                    # #     EffTable([
                    # #             common_plot.table_block_signal_fs_700,
                    # #             common_plot.table_block_signal_fs_1700,
                    # #         ],
                    # #         common_plot.get_table_category_block(),
                    # #         common_plot.norm_factors,
                    # #         squash_errs=True,
                    # #         name='EffTableCompFS'
                    # #         ),
                    # #     ]),

                    varial.tools.ToolChain('MergeChannelsTablesNoTheory', [
                        varial.tools.ToolChainParallel('HistoLoader',
                            list(varial.tools.HistoLoader(
                                pattern=[output_dir+'/%s/TreeProject/TreeProjector/*%s*.root'%(name, g)]+list(sys_path+'/%s*/*%s*.root'% (i, g) for i in uncerts),
                                filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in plot.more_samples) and\
                                    'Region_Comb' not in w.in_file_path and\
                                    any(w.in_file_path.endswith(f) for f in ['ST']) and\
                                    unselect_theory_uncert(w),
                                hook_loaded_histos=plot.loader_hook_merge_regions,
                                name='HistoLoader_'+g,
                                lookup_aliases=False,
                                raise_on_empty_result=False
                                ) for g in plot.more_samples)),
                        plot.mk_toolchain('Histograms',
                            plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=True, hook_loaded_histos=plot.loader_hook_merge_lep_channels),
                            pattern=None, input_result_path='../HistoLoader/HistoLoader*'),
                        plot.mk_toolchain('HistogramsCompUncerts',
                            filter_keyfunc=lambda w: any(f in w.file_path for f in [treeproject_tptp.ttbar_smpl, 'WJets', 'TpTp_M-0800', 'TpTp_M-1600']) and any(w.in_file_path.endswith(g) for g in ['ST', 'HT']),   
                            plotter_factory=plot.plotter_factory_uncerts(analysis.rate_uncertainties, uncerts, include_rate=True, hook_loaded_histos=lambda w: plot.loader_hook_uncerts(plot.loader_hook_merge_lep_channels(w))),
                            pattern=None, input_result_path='../HistoLoader/HistoLoader*'),
                        # CountTable([
                        #         common_plot.table_block_signal,
                        #         common_plot.table_block_background,
                        #         [(r'\textbf{Total Background}', lambda w: 'Integral___bkg_sum' in w)],
                        #         [(r'\textbf{data}', lambda w: 'Integral___Run2015CD' in w)],
                        #     ],
                        #     common_plot.get_table_category_block(),
                        #     name='CountTable'
                        #     ),
                        # EffTable([
                        #         common_plot.table_block_signal,
                        #     ],
                        #     common_plot.get_table_category_block(),
                        #     common_plot.norm_factors,
                        #     squash_errs=True,
                        #     name='EffTable'
                        #     ),
                        # EffTable([
                        #         common_plot.table_block_signal_fs_700,
                        #         common_plot.table_block_signal_fs_1700,
                        #     ],
                        #     common_plot.get_table_category_block(),
                        #     common_plot.norm_factors,
                        #     squash_errs=True,
                        #     name='EffTableCompFS'
                        #     ),
                        # ]),
                        CountTable([
                                common_plot.table_block_signal,
                                common_plot.table_block_background,
                                [(r'\textbf{Total Background}', lambda w: 'Integral___bkg_sum' in w)],
                                [(r'\textbf{data}', lambda w: 'Integral___Run2015CD' in w)],
                            ],
                            common_plot.get_table_category_block(),
                            name='CountTable'
                            ),
                        EffTable([
                                common_plot.table_block_signal_fs_700,
                                common_plot.table_block_signal_fs_1700,
                            ],
                            common_plot.get_table_category_block(),
                            common_plot.norm_factors,
                            squash_errs=True,
                            name='EffTableCompFS'
                            ),
                        ]),

                    # # varial.tools.ToolChain('TablesSplitLepton', [
                    # #     varial.tools.ToolChainParallel('HistoLoader',
                    # #         list(varial.tools.HistoLoader(
                    # #             pattern=[output_dir+'/%s/TreeProject/TreeProjector/*%s*.root'%(name, g)]+list(sys_path+'/%s*/*%s*.root'% (i, g) for i in uncerts),
                    # #             filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in plot.more_samples) and\
                    # #                 'Region_Comb' not in w.in_file_path and\
                    # #                 any(w.in_file_path.endswith(f) for f in ['ST']),
                    # #             # hook_loaded_histos=plot.loader_hook_merge_regions,
                    # #             name='HistoLoader_'+g,
                    # #             lookup_aliases=False,
                    # #             raise_on_empty_result=False
                    # #             ) for g in plot.more_samples)),
                    # #     plot.mk_toolchain('Histograms', plot.more_samples, 
                    # #             pattern=None, input_result_path='../HistoLoader/HistoLoader*'
                    # #             ),  
                    # #     CountTable([
                    # #             common_plot.table_block_signal,
                    # #             common_plot.table_block_background,
                    # #             [(r'\textbf{Total Background}', lambda w: 'Integral___bkg_sum' in w)],
                    # #             [(r'\textbf{data}', lambda w: 'Integral___Run2015CD' in w)],
                    # #         ],
                    # #         common_plot.get_table_category_block_split('Mu45'),
                    # #         name='CountTableMu45'
                    # #         ),
                    # #     CountTable([
                    # #             common_plot.table_block_signal,
                    # #             common_plot.table_block_background,
                    # #             [(r'\textbf{Total Background}', lambda w: 'Integral___bkg_sum' in w)],
                    # #             [(r'\textbf{data}', lambda w: 'Integral___Run2015CD' in w)],
                    # #         ],
                    # #         common_plot.get_table_category_block_split('El45'),
                    # #         name='CountTableEl45'
                    # #         ),
                    # #     EffTable([
                    # #             common_plot.table_block_signal,
                    # #         ],
                    # #         common_plot.get_table_category_block_split('Mu45'),
                    # #         common_plot.norm_factors,
                    # #         squash_errs=True,
                    # #         name='EffTableMu45'
                    # #         ),
                    # #     EffTable([
                    # #             common_plot.table_block_signal,
                    # #         ],
                    # #         common_plot.get_table_category_block_split('El45'),
                    # #         common_plot.norm_factors,
                    # #         squash_errs=True,
                    # #         name='EffTableEl45'
                    # #         ),

                    # #     ]),

                    # varial.tools.ToolChain('TablesSplitLeptonNoTheory', [
                    #     varial.tools.ToolChainParallel('HistoLoader',
                    #         list(varial.tools.HistoLoader(
                    #             pattern=[output_dir+'/%s/TreeProject/TreeProjector/*%s*.root'%(name, g)]+list(sys_path+'/%s*/*%s*.root'% (i, g) for i in uncerts),
                    #             filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in plot.more_samples) and\
                    #                 'Region_Comb' not in w.in_file_path and\
                    #                 any(w.in_file_path.endswith(f) for f in ['ST']) and\
                    #                 unselect_theory_uncert(w),
                    #             # hook_loaded_histos=plot.loader_hook_merge_regions,
                    #             name='HistoLoader_'+g,
                    #             lookup_aliases=False,
                    #             raise_on_empty_result=False
                    #             ) for g in plot.more_samples)),
                    #     plot.mk_toolchain('Histograms', plot.more_samples, 
                    #             pattern=None, input_result_path='../HistoLoader/HistoLoader*',
                    #             plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=True)
                    #             ),  
                    #     CountTable([
                    #             common_plot.table_block_signal,
                    #             common_plot.table_block_background,
                    #             [(r'\textbf{Total Background}', lambda w: 'Integral___bkg_sum' in w)],
                    #             [(r'\textbf{data}', lambda w: 'Integral___Run2015CD' in w)],
                    #         ],
                    #         common_plot.get_table_category_block_split('Mu45'),
                    #         name='CountTableMu45'
                    #         ),
                    #     CountTable([
                    #             common_plot.table_block_signal,
                    #             common_plot.table_block_background,
                    #             [(r'\textbf{Total Background}', lambda w: 'Integral___bkg_sum' in w)],
                    #             [(r'\textbf{data}', lambda w: 'Integral___Run2015CD' in w)],
                    #         ],
                    #         common_plot.get_table_category_block_split('El45'),
                    #         name='CountTableEl45'
                    #         ),
                    #     EffTable([
                    #             common_plot.table_block_signal,
                    #         ],
                    #         common_plot.get_table_category_block_split('Mu45'),
                    #         common_plot.norm_factors,
                    #         squash_errs=True,
                    #         name='EffTableMu45'
                    #         ),
                    #     EffTable([
                    #             common_plot.table_block_signal,
                    #         ],
                    #         common_plot.get_table_category_block_split('El45'),
                    #         common_plot.norm_factors,
                    #         squash_errs=True,
                    #         name='EffTableEl45'
                    #         ),

                    #     ]),

                    varial.tools.WebCreator(),
                    

                    ]
            # return tmp

    ######### DEPRECATED #########

    # for uc_name, uncert_list in plot_uncerts.iteritems():
    #     if all(i in sys_list for i in uncert_list):
    #         tc_plot_sens += [
    #             plot.mk_toolchain('HistogramsComp_'+uc_name, plot.less_samples_to_plot_only_th, 
    #                 pattern=[output_dir+'/%s/TreeProject/TreeProjector/*.root'%name]
    #                 + list(sys_path+'/%s*/*.root'% i for i in uncert_list if i in uncerts)
    #                 )
    #             # plot.mk_toolchain_norm('HistogramsCompNormToInt_'+uc_name, [output_dir+'/%s/TreeProject/TreeProjector/*.root'%name]
    #             #     + list(sys_path+'/%s*/*.root'% i for i in uncert_list if i in uncerts)
    #             #     ,plot.less_samples_to_plot_only_th),
    #             ]


    ###############################
    ############ FOR AN ###########
    ###############################
    path_sens = os.path.join(output_dir, name+'/Limit')
    # path_sens_old = os.path.join(output_dir, name+'/PlotAndSens')
    path_an = os.path.join(output_dir, name+'/PlotAN')
    path_pas = os.path.join(output_dir, name+'/PlotPAS')
    def mk_tc_an():
        tc_tex = [
            tex_content.mk_autoContentSignalControlRegion(path_an+'/HistogramsNoTheory', 'El45', 'Mu45', 'WithDataFinalRegions_'+name),
            tex_content.mk_autoContentSignalControlRegionCombined(path_an+'/MergeChannelsHistsNoTheory/Histograms/StackedAll', 'WithDataFinalRegionsCombinedMore_'+name),
            # tex_content.mk_autoContentSignalControlRegionCombined(path_an+'/MergeChannelsHistsNoTheory/HistogramsNoData/StackedAll', 'NoDataFinalRegionsCombinedMore_'+name),
            tex_content.mk_autoContentSignalControlRegionCombined(path_an+'/MergeChannelsHistsNoTheory/HistogramsNormToInt/StackedAll', 'NormedSystPlotsCombinedMore_'+name),
            tex_content.mk_autoContentSignalControlRegionCombined(path_sens+'/BackgroundOnlyFitNoTheoryAllRegions/PostFitPlots/HistogramsPostfit/StackedAll', 'PostfitDistributionsCombined_'+name),
            # tex_content.mk_compSystematicPlots(path_an+'/HistogramsCompUncerts', treeproject_tptp.ttbar_smpl, 'El45', 'Mu45', 'CompUncertPlotsTTbar_'+name),
            tex_content.mk_compSystematicPlots(path_an+'/MergeChannelsHists/HistogramsCompUncerts', 'TTbar', '', 'CompUncertPlotsTTbar_'+name),
            tex_content.mk_compSystematicPlots(path_an+'/MergeChannelsHists/HistogramsCompUncerts', 'WJets', '', 'CompUncertPlotsWJets_'+name),
            tex_content.mk_compSystematicPlots(path_an+'/MergeChannelsHists/HistogramsCompUncerts', 'TpTp_M-0800_thth', '', 'CompUncertPlotsTpTpM0800_'+name),
            tex_content.mk_compSystematicPlots(path_an+'/MergeChannelsHists/HistogramsCompUncerts', 'TpTp_M-1600_thth', '', 'CompUncertPlotsTpTpM1600_'+name),
            tex_content.mk_compSystematicPlots(path_sens+'/HistogramsCompUncertsShape', 'TpTp_M-1200_thth', '_Mu45', 'CompUncertPlotsSigRewShapeTpTpM1200_'+name),
            tex_content.mk_compSystematicPlots(path_sens+'/HistogramsCompUncertsUncOnly', 'TpTp_M-1200_thth', '_Mu45', 'CompUncertPlotsSigRewUncOnlyTpTpM1200_'+name),
            # tex_content.mk_autoContentCompareSplitWithMergedLep(path_an+'/Histograms/StackedAll', path_an+'/MergeChannelsHistsNoTheory/Histograms/StackedAll', 'Sideband', 'El45', 'Mu45', 'WithDataSidebandRegions_'+name),
            tex_content.mk_autoContentLimits(path_sens, 'TTLimitsNoTheory%sFinal', 'TTLimitPlots_'+name),
            tex_content.mk_autoContentLimits(path_sens, 'BBLimitsNoTheory%sFinal', 'BBLimitPlots_'+name),

            tex_content.mk_autoContentLimitsVarSize(path_sens+'/BackgroundOnlyFitNoTheoryCR', 0.47, 'PostfitNoTheory_'+name),
            tex_content.mk_autoContentLimitsVarSize(path_sens+'/BackgroundOnlyFitWithTheoryCR', 0.47, 'PostfitWithTheory_'+name),
            tex_content.mk_autoContentLimitsVarSize(path_sens+'/BackgroundOnlyFitTheoryAndRateCR', 0.47, 'PostfitTheoryAndRate_'+name),
            tex_content.mk_autoContentLimitsVarSize(path_sens+'/TTLimitsNoTheoryAllRegions', 0.47, 'ExpLimitsNoTheory_'+name),
            tex_content.mk_autoContentLimitsVarSize(path_sens+'/TTLimitsWithTheoryAllRegions', 0.47, 'ExpLimitsWithTheory_'+name),
            tex_content.mk_autoContentLimitsVarSize(path_sens+'/TTLimitsTheoryAndRateAllRegions', 0.47, 'ExpLimitsTheoryAndRate_'+name),
            tex_content.mk_autoContentLimitsVarSize(path_sens+'/TTLimitsOnlyHTAllRegionsWithNormNOSigRew', 0.47, 'ExpLimitsNOSigRew_'+name),
            tex_content.mk_autoContentLimitsVarSize(path_sens+'/TTLimitsOnlyHTAllRegionsWithNormSigRew', 0.47, 'ExpLimitsSigRew_'+name),
            tex_content.mk_autoContentLimitsVarSize(path_sens+'/TTLimitsOnlyHTAllRegionsWithNormSigRewUncOnly', 0.47, 'ExpLimitsSigRewUncOnly_'+name),
            tex_content.mk_autoContentSysTabs(path_sens+'/TTLimitsNoTheoryAllRegionsFinal', 'El45', 'Mu45', 'SysTabs_'+name, mass_points=['M-0800', 'M-1200', 'M-1600']),
            ######## TABLES ########
            tex_content.mk_autoEffCount(path_an+'/MergeChannelsTablesNoTheory/EffTable/count_table_content.tex', name='EffTable_'+name),
            tex_content.mk_autoEffCount(path_an+'/MergeChannelsTablesNoTheory/EffTableCompFS/count_table_content.tex', name='EffTableCompFS_'+name),
            tex_content.mk_autoEffCount(path_an+'/MergeChannelsTablesNoTheory/CountTable/count_table_content.tex', name='CountTable_'+name),
            tex_content.mk_autoEffCount(path_an+'/TablesSplitLeptonNoTheory/EffTableEl45/count_table_content.tex', name='EffTableEl45_'+name),
            tex_content.mk_autoEffCount(path_an+'/TablesSplitLeptonNoTheory/EffTableMu45/count_table_content.tex', name='EffTableMu45_'+name),
            tex_content.mk_autoEffCount(path_an+'/TablesSplitLeptonNoTheory/CountTableEl45/count_table_content.tex', name='CountTableEl45_'+name),
            tex_content.mk_autoEffCount(path_an+'/TablesSplitLeptonNoTheory/CountTableMu45/count_table_content.tex', name='CountTableMu45_'+name),
            tex_content.mk_autoEffCount(path_sens+'/BackgroundOnlyFitNoTheoryAllRegions/PostFitPlots/CountTablePostFit/count_table_content.tex', name='CountTablePostFit_'+name),
            ######### DEPRECATED #########
            # # tex_content.mk_autoContentSystematicCRPlots(path_an+'/Histograms', 'El45', 'Mu45', 'SystematicCRPlots_'+name),
            # # tex_content.mk_autoContentHiggsVarCombinedMore(path_an+'/MergeChannelsHistsCombFinalStates/Histograms/StackedAll', 'WithDataFinalRegionsCombinedCompFinalStates_'+name, size='0.45'),
            # # tex_content.mk_autoContentHiggsVarCombinedMore(path_an+'/MergeChannelsHistsCombFinalStates/HistogramsNoData/StackedAll', 'NoDataFinalRegionsCombinedCompFinalStates_'+name, size='0.45'),
            # # tex_content.mk_autoContentSystematicCRPlots(path_an+'/HistogramsNormToInt', 'El45', 'Mu45', 'SystematicCRPlotsNormed_'+name),
            # # tex_content.mk_autoContentSignalControlRegionCombined(path_an+'/MergeChannels/HistogramsMergeLeptonChannels', 'WithDataFinalRegionsCombined_'+name),
            # # tex_content.mk_autoContentSignalControlRegion(path_an+'/HistogramsNoData', 'El45', 'Mu45', 'NoDataFinalRegions_'+name),
            # # tex_content.mk_autoContentLimitsVarSize(path_sens, 'El45', 'Mu45', 'LimitPlotsLarge_'+name),
            # # tex_content.mk_autoContentLimits(path_sens_old, 'El45', 'Mu45', 'LimitPlotsOld_'+name),
            # # tex_content.mk_autoContentLimitsVarSize(path_sens_old, 'El45', 'Mu45', 'LimitPlotsLargeOld_'+name),
        ]
        
        ######## LIMIT PLOTS AND SYSTEMATIC TABLES ########

        # # if name == 'TopPtAndHTReweighting':
        # #     tc_tex += [tex_content.mk_autoContentLimits(path_an, 'El45', 'Mu45', 'LimitPlots_'+name, mass_points=['TpTp_M-0700', 'TpTp_M-1000', 'TpTp_M-1300', 'TpTp_M-1700'])]
        # #     tc_tex += [tex_content.mk_autoContentLimitsVarSize(path_an, 'El45', 'Mu45', 'LimitPlotsLarge_'+name, mass_points=['TpTp_M-0700', 'TpTp_M-1000', 'TpTp_M-1300', 'TpTp_M-1700'])]


        if name == 'NoReweighting':
            # if all(os.path.exists(sys_path+'/'+s+suf) for s in ['ScaleVar', 'Exp'] for suf in ['__plus', '__minus']):
            tc_tex += [
                # tex_content.mk_autoContentCompSystPlots(
                #     list(path_an+'/HistogramsComp_'+uc_name for uc_name in ['ScaleVar', 'Exp']), # ['ScaleVar', 'PDF', 'TTbarScale', 'Exp']
                #     'El45', 'Mu45', 'CompSystPlots_'+name),
                tex_content.mk_autoContentSignalControlRegionCombined(path_an+'/MergeChannelsHists/HistogramsNoUncerts/StackedAll', 'WithDataFinalRegionsCombinedMoreNoUncerts_'+name),
                ]
        # # for uc_name, uncert_list in plot_uncerts.iteritems():
        # #     if any(i in uncerts for i in uncert_list):
        # #         tc_tex += [
        # #             tex_content.mk_autoContentSystematicCRPlots(
        # #                 path_an+'/HistogramsComp_'+uc_name, 'El45', 'Mu45', 'SystematicCRPlots_'+uc_name+'_'+name),
        # #             # tex_content.mk_autoContentSystematicCRPlots(
        # #             #     path_an+'/HistogramsCompNormToInt_'+uc_name, 'El45', 'Mu45', 'SystematicCRPlotsNormed_'+uc_name+'_'+name)
        # #             ]
        # #     tc_tex += [tex_content.mk_autoContentLimits(path_an, 'El45', 'Mu45', 'LimitPlots_'+name, prefix='LimitsAllUncertsAllRegions', mass_points=['TpTp_M-0700', 'TpTp_M-1000', 'TpTp_M-1300', 'TpTp_M-1700'])]
        # #     tc_tex += [tex_content.mk_autoContentLimitsVarSize(path_an, 'El45', 'Mu45', 'LimitPlotsLarge_'+name, mass_points=['TpTp_M-0700', 'TpTp_M-1000', 'TpTp_M-1300', 'TpTp_M-1700'])]

        # # tc_tex += [tex_content.mk_autoContentCompSystPlots(
        # #             list(path_an+'/HistogramsCompNormToInt_'+uc_name for uc_name in ['ScaleVar', 'PDF', 'TTbarScale', 'Exp']),
        # #              'El45', 'Mu45', 'CompSystPlotsNormed_'+name)]

        tc_tex = [
            varial.tools.ToolChain('Tex', tc_tex),
            varial.tools.CopyTool('dnowatsc@lxplus.cern.ch:AN-Dir/notes/AN-15-327/trunk/', src='../Tex/*', ignore=('*.svn', '*.html'), use_rsync=True),
            ]
        return tc_tex

    ######### DEPRECATED #########


    ###############################
    ############ FOR PAS ##########
    ###############################

    def mk_tc_pas():
        tc_tex_pas = [
            tex_content.mk_autoContentSignalControlRegionCombined(path_pas+'/MergeChannelsHists/Histograms/StackedAll', 'WithDataFinalRegionsCombinedMore_'+name, size='0.45'),
            tex_content.mk_autoContentSignalControlRegionCombined(path_pas+'/MergeChannelsHists/HistogramsNoData/StackedAll', 'NoDataFinalRegionsCombinedMore_'+name),
            tex_content.mk_autoEffCount(path_pas+'/MergeChannelsTables/EffTable/count_table_content.tex', name='EffTable_'+name),
            tex_content.mk_autoEffCount(path_pas+'/MergeChannelsTables/EffTableCompFS/count_table_content.tex', name='EffTableCompFS_'+name),
            tex_content.mk_autoEffCount(path_pas+'/MergeChannelsTables/CountTable/count_table_content.tex', name='CountTable_'+name),
            # tex_content.mk_autoContentCompareSplitWithMergedLep(path_pas+'/Histograms/StackedAll', path_pas+'/MergeChannelsHists/Histograms/StackedAll', 'Sideband', 'El45', 'Mu45', 'WithDataSidebandRegions_'+name),
            
            ######### DEPRECATED #########
            # # tex_content.mk_autoContentHiggsVarCombinedMore(path_pas+'/MergeChannelsHistsCombFinalStates/Histograms/StackedAll', 'WithDataFinalRegionsCombinedCompFinalStates_'+name, size='0.45'),
            # # tex_content.mk_autoContentHiggsVarCombinedMore(path_pas+'/MergeChannelsHistsCombFinalStates/HistogramsNoData/StackedAll', 'NoDataFinalRegionsCombinedCompFinalStates_'+name, size='0.45'),
            # # tex_content.mk_autoContentLimits(path_sens_old, 'El45', 'Mu45', 'LimitPlotsOld_'+name),
            # # tex_content.mk_autoContentLimitsVarSize(path_sens_old, 'El45', 'Mu45', 'LimitPlotsLargeOld_'+name),
            # # tex_content.mk_autoContentSignalControlRegionCombined(path_pas+'/MergeChannelsHists/HistogramsNoUncerts/StackedAll', 'WithDataFinalRegionsCombinedMore_'+name),
            # # tex_content.mk_autoContentSignalControlRegionCombined(path_pas+'/MergeChannelsHists/HistogramsNoData/StackedAll', 'NoDataFinalRegionsCombinedMore_'+name),
            # # tex_content.mk_autoEffCount(path_pas+'/MergeChannels/EffTable/count_table_content.tex', name='EffTable_'+name),
            # # tex_content.mk_autoEffCount(path_pas+'/MergeChannels/EffTableCompFS/count_table_content.tex', name='EffTableCompFS_'+name),
            # # tex_content.mk_autoEffCount(path_pas+'/MergeChannels/CountTable/count_table_content.tex', name='CountTable_'+name),
            
        ]
        # # if name == 'TopPtAndHTReweighting':
        # #     tc_tex_pas += [tex_content.mk_autoContentLimits(path_pas, 'El45', 'Mu45', 'LimitPlots_'+name, mass_points=['TpTp_M-0700', 'TpTp_M-1000', 'TpTp_M-1300', 'TpTp_M-1700'])]
        # #     tc_tex_pas += [tex_content.mk_autoContentLimitsVarSize(path_pas, 'El45', 'Mu45', 'LimitPlotsLarge_'+name, mass_points=['TpTp_M-0700', 'TpTp_M-1000', 'TpTp_M-1300', 'TpTp_M-1700'])]
        # # else:
        # #     tc_tex_pas += [tex_content.mk_autoContentLimits(path_pas, 'El45', 'Mu45', 'LimitPlots_'+name, prefix='LimitsAllUncertsAllRegions', mass_points=['TpTp_M-0700', 'TpTp_M-1000', 'TpTp_M-1300', 'TpTp_M-1700'])]
        # #     tc_tex_pas += [tex_content.mk_autoContentLimitsVarSize(path_pas, 'El45', 'Mu45', 'LimitPlotsLarge_'+name, mass_points=['TpTp_M-0700', 'TpTp_M-1000', 'TpTp_M-1300', 'TpTp_M-1700'])]
        tc_tex_pas = [
            varial.tools.ToolChain('TexPas', tc_tex_pas),
            varial.tools.CopyTool('dnowatsc@lxplus.cern.ch:PAS-Dir/notes/B2G-16-011/trunk/', src='../TexPas/*', ignore=('*.svn', '*.html'), use_rsync=True),
            ]
        return tc_tex_pas



    
    
    return varial.tools.ToolChain(name, [
            # varial.tools.ToolChainParallel('TreeProject', lazy_eval_tools_func=mk_tc_tp, n_workers=1),
            # varial.tools.ToolChainParallel('PlotAN', lazy_eval_tools_func=mk_tc_plot, n_workers=1),
            varial.tools.ToolChainParallel('LimitPAS', lazy_eval_tools_func=mk_tc_sens, n_workers=1),
            # varial.tools.ToolChainParallel('PlotPAS', lazy_eval_tools_func=mk_tc_plot, n_workers=1),
            # varial.tools.ToolChainParallel('TexAN', lazy_eval_tools_func=mk_tc_an, n_workers=1),
            # varial.tools.ToolChainParallel('TexPAS', lazy_eval_tools_func=mk_tc_pas, n_workers=1),

        ])

def run_treeproject_and_plot(output_dir):
    base_path = os.path.join(os.getcwd(), 'Files_and_Plots')
    tc = varial.tools.ToolChain(
        output_dir,
        [
            git.GitAdder(),
            varial.tools.ToolChainParallel('RunAnalysis', [

                make_tp_plot_chain('HTReweighting', base_path, output_dir+'/RunAnalysis',
                    # br_list=br_list_all,
                    uncertainties=all_uncerts
                ),
                # make_tp_plot_chain('NoReweighting', base_path, output_dir+'/RunAnalysis', 
                #     add_uncert_func=add_all_without_weight_uncertainties,
                #     # uncertainties=all_uncerts
                # ),
                # make_tp_plot_chain('TopPtReweighting', base_path, output_dir+'/RunAnalysis',
                #     add_uncert_func=add_all_with_weight_uncertainties({'top_pt_reweight' : {treeproject_tptp.ttbar_smpl : top_pt_reweight}}),
                #     mod_sample_weights={treeproject_tptp.ttbar_smpl : treeproject_tptp.base_weight+'*'+top_pt_reweight},
                #     # uncertainties=all_uncerts+['top_pt_reweight']
                #     ),
                # make_tp_plot_chain('TopPtAndHTReweighting', base_path, output_dir+'/RunAnalysis',
                #     add_uncert_func=add_all_with_weight_uncertainties({
                #         'ht_reweight' : {
                #             treeproject_tptp.ttbar_smpl : ht_reweight_ttbar_w_top_pt_reweight,
                #             'WJets' : ht_reweight_wjets_w_top_pt_reweight
                #             },
                #         'top_pt_reweight' : {treeproject_tptp.ttbar_smpl : top_pt_reweight}
                #         }),
                #     mod_sample_weights={
                #         treeproject_tptp.ttbar_smpl : treeproject_tptp.base_weight+'*'+top_pt_reweight+'*'+ht_reweight_ttbar_w_top_pt_reweight,
                #         'WJets' : treeproject_tptp.base_weight+'*'+ht_reweight_wjets_w_top_pt_reweight,
                #     },
                #     # uncertainties=all_uncerts+['ht_reweight', 'top_pt_reweight']
                #     ),

                ], n_workers=1),
                varial.tools.WebCreator(),
            # varial.tools.ToolChain('ReweightingComparision', [
            #     tex_content.mk_autoCompareReweightingMethods(output_dir+'/RunAnalysis', ['NoReweighting', 'HTReweighting', 'TopPtReweighting', 'TopPtAndHTReweighting'], name='CompareReweightingDistributions'),
            #     tex_content.mk_autoComparePostfitPlots(output_dir+'/RunAnalysis', ['NoReweighting', 'HTReweighting', 'TopPtReweighting', 'TopPtAndHTReweighting'], name='CompareReweightingPostfits'),
            #     ]),
            # varial.tools.CopyTool('dnowatsc@lxplus.cern.ch:AN-Dir/notes/AN-15-327/trunk/', src='../ReweightingComparision/*', ignore=('*.svn', '*.html'), use_rsync=True),
            git.GitTagger(commit_prefix='In {0}'.format(output_dir)),
            # mk_tex_tc_post(output_dir+'/Histograms/')(), 

            # varial.tools.PrintToolTree(),
            # tex_content.tc,
            # varial.tools.CopyTool('~/www/auth/VLQ2HT', use_rsync=True),
        ]
    )
    return tc


varial.settings.try_reuse_results = True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Provide output_dir!'
        exit(-1)
    varial.tools.Runner(run_treeproject_and_plot(sys.argv[1]), True)

# varial.settings.rootfile_postfixes += ['.pdf']
# varial.tools.Runner(tc, True)
# import varial.main
# varial.main.main(toolchain=tc)