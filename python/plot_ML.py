import plot as plot

import varial.tools


tc = [
varial.tools.ToolChain('MergeChannelsHistsNoTheory', [
    varial.tools.ToolChainParallel('HistoLoader',
    list(varial.tools.HistoLoader(
        pattern=map(lambda w: w.format('*'+g+'*'), input_pattern),
        filter_keyfunc=lambda w: any(f in w.file_path.split('/')[-1] for f in plot.less_samples) and\
            'Region_Comb' not in w.in_file_path and\
            any(w.in_file_path.endswith(f) for f in ['ST', 'HT', 'n_ak4', 'topjets[0].m_pt', 'topjets[1].m_pt',
                'n_ak8', 'met', 'pt_ld_ak4_jet', 'pt_subld_ak4_jet', 'jets[2].m_pt','jets[3].m_pt', 'jets[].m_pt', 'n_additional_btags_medium', 'n_prim_vertices',
                'n_higgs_tags_1b_med_sm10', 'n_higgs_tags_2b_med_sm10', 'primary_electron_pt', 'primary_muon_pt', 'PrimaryLepton.Particle.m_eta', 'wtags_mass_softdrop',
                'nobtag_boost_mass_nsjbtags', 'nomass_boost_1b_mass_softdrop', 'nomass_boost_2b_mass_softdrop', 'noboost_mass_1b[0].m_pt', 'noboost_mass_2b[0].m_pt']) and\
            unselect_theory_uncert(w),
        hook_loaded_histos=plot.loader_hook_merge_regions,
        name='HistoLoader_'+g,
        lookup_aliases=False,
        raise_on_empty_result=False
        ) for g in plot.less_samples)),
    plot.mk_toolchain('Histograms', plot.less_samples_to_plot_only_th,
        plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=True, hook_loaded_histos=plot.loader_hook_merge_lep_channels),
        pattern=None, input_result_path='../HistoLoader/HistoLoader*'),
    # plot.mk_toolchain('HistogramsCompUncerts', plot.less_samples_to_plot_only_th,
    #     filter_keyfunc=lambda w: any(f in w.file_path for f in [treeproject_tptp.ttbar_smpl, 'QCD', 'WJets', 'TpTp_M-0800', 'TpTp_M-1600']) and any(w.in_file_path.endswith(g) for g in ['ST', 'HT']),   
    #     plotter_factory=plot.plotter_factory_uncerts(
    #         hook_loaded_histos=lambda w: plot.loader_hook_uncerts(plot.loader_hook_merge_lep_channels(w), 
    #             analysis.rate_uncertainties, uncerts, include_rate=True)),
    #     pattern=None, input_result_path='../HistoLoader/HistoLoader*'),
    # plot.mk_toolchain('HistogramsNormToInt',
    #     filter_keyfunc=lambda w: 'TpTp' not in w.file_path,
    #     pattern=None, input_result_path='../HistoLoader/HistoLoader*',
    #     plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, def_uncerts, hook_loaded_histos=plot.loader_hook_norm_to_int,
    #         plot_setup=plot.stack_setup_norm_all_to_intgr)),
    plot.mk_toolchain('HistogramsHiggsComp', pattern=None, input_result_path='../HistoLoader/HistoLoader*',
        filter_keyfunc=lambda w: all(g not in w.sample for g in ['TpTp_M-0800', 'TpTp_M-1600']),
        plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=True, 
            hook_loaded_histos=plot.loader_hook_compare_finalstates,
            ),
        # pattern=None, input_result_path='../HistoLoader/HistoLoader*'
        ),
    # plot.mk_toolchain('HistogramsNoDataHiggsComp', pattern=None, input_result_path='../HistoLoader/HistoLoader*',
    #     filter_keyfunc=lambda w: 'Run2015CD' not in w.file_path.split('/')[-1] and all(g not in w.sample for g in ['TpTp_M-0800', 'TpTp_M-1600']),
    #     plotter_factory=plot.plotter_factory_stack(analysis.rate_uncertainties, uncerts, include_rate=True, 
    #         hook_loaded_histos=plot.loader_hook_compare_finalstates,
    #         )
    #     ),
    ])

]