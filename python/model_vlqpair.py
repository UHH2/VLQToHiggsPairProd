import math
import theta_auto
import os

import varial.monitor

background_samples = [
    'TTbar',
    'QCD',
    'WJets',
    'DYJets',
    'SingleTop',
]

def get_model(hist_dir, final_states):
    model = theta_auto.build_model_from_rootfile(
        hist_dir,
        include_mc_uncertainties = True)#mc uncertainties=true
    model.fill_histogram_zerobins()
    model.set_signal_processes(final_states)
    # for process, factor in branching_ratios:
    #     model.scale_predictions(factor, process, observable)
    model.add_lognormal_uncertainty('ttbar_rate', math.log(1.25), 'TTbar')
    model.add_lognormal_uncertainty('qcd_rate', math.log(1.50), 'QCD')
    model.add_lognormal_uncertainty('wjets_rate', math.log(1.25), 'WJets')
    model.add_lognormal_uncertainty('zjets_rate', math.log(1.50), 'DYJets')
    model.add_lognormal_uncertainty('singlet_rate', math.log(1.50), 'SingleTop')
    for smpl in background_samples:
        model.add_lognormal_uncertainty('luminosity', math.log(1.046), smpl)
    try:
        for smpl in background_samples:
            model.add_lognormal_uncertainty('el_trg+id', math.log(1.05), smpl, 'SignalRegion2b_El45')
            model.add_lognormal_uncertainty('el_trg+id', math.log(1.05), smpl, 'SignalRegion1b_El45')
            model.add_lognormal_uncertainty('el_trg+id', math.log(1.05), smpl, 'SidebandRegion_El45')
    except RuntimeError:
        varial.monitor.message(
            'sensitivity.get_model_data_bkg', 
            'WARNING Cannot apply lognormal uncert for ele-trg (in mu-chan?).'
        )
    try:
        for smpl in background_samples:
            model.add_lognormal_uncertainty('mu_trg+id', math.log(1.01), smpl, 'SignalRegion2b_Mu45')
            model.add_lognormal_uncertainty('mu_trg+id', math.log(1.01), smpl, 'SignalRegion1b_Mu45')
            model.add_lognormal_uncertainty('mu_trg+id', math.log(1.01), smpl, 'SidebandRegion_Mu45')
    except RuntimeError:
        varial.monitor.message(
            'sensitivity.get_model_data_bkg', 
            'WARNING Cannot apply lognormal uncert for mu-trg (in ele-chan?).'
        )
    
    # model.add_lognormal_uncertainty('tptp700_rate', math.log(1.15), 'TpTp_M-700')
    # model.add_lognormal_uncertainty('tptp800_rate', math.log(1.15), 'TpTp_M-800')
    # model.add_lognormal_uncertainty('tptp900_rate', math.log(1.15), 'TpTp_M-900')
    # model.add_lognormal_uncertainty('tptp1000_rate', math.log(1.15), 'TpTp_M-1000')
    # # model.add_lognormal_uncertainty('tptp1100_rate', math.log(1.15), 'TpTp_M-1100')
    # model.add_lognormal_uncertainty('tptp1200_rate', math.log(1.15), 'TpTp_M-1200')
    # model.add_lognormal_uncertainty('tptp1400_rate', math.log(1.15), 'TpTp_M-1400')
    # model.add_lognormal_uncertainty('tptp1600_rate', math.log(1.15), 'TpTp_M-1600')
    # for p in model.processes:
    #     if p == 'QCD': continue
    #     model.add_lognormal_uncertainty('lumi', 0.026, p)
    return model
