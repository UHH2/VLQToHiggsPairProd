import math
import theta_auto
import os

def get_model(hist_dir, final_states):
    model = theta_auto.build_model_from_rootfile(
        hist_dir,
        include_mc_uncertainties = True)#mc uncertainties=true
    model.fill_histogram_zerobins()
    model.set_signal_processes(final_states)
    # for process, factor in branching_ratios:
    #     model.scale_predictions(factor, process, observable)
    model.add_lognormal_uncertainty('ttbar_rate', math.log(1.15), 'TTbar')
    model.add_lognormal_uncertainty('qcd_rate', math.log(1.30), 'QCD')
    model.add_lognormal_uncertainty('wjets_rate', math.log(1.25), 'WJets')
    model.add_lognormal_uncertainty('zjets_rate', math.log(1.50), 'DYJets')
    model.add_lognormal_uncertainty('singlet_rate', math.log(1.20), 'SingleTop')
    model.add_lognormal_uncertainty('tptp700_rate', math.log(1.15), 'TpTp_M-700')
    model.add_lognormal_uncertainty('tptp800_rate', math.log(1.15), 'TpTp_M-800')
    model.add_lognormal_uncertainty('tptp900_rate', math.log(1.15), 'TpTp_M-900')
    model.add_lognormal_uncertainty('tptp1000_rate', math.log(1.15), 'TpTp_M-1000')
    # model.add_lognormal_uncertainty('tptp1100_rate', math.log(1.15), 'TpTp_M-1100')
    model.add_lognormal_uncertainty('tptp1200_rate', math.log(1.15), 'TpTp_M-1200')
    model.add_lognormal_uncertainty('tptp1400_rate', math.log(1.15), 'TpTp_M-1400')
    model.add_lognormal_uncertainty('tptp1600_rate', math.log(1.15), 'TpTp_M-1600')
    # for p in model.processes:
    #     if p == 'QCD': continue
    #     model.add_lognormal_uncertainty('lumi', 0.026, p)
    return model
