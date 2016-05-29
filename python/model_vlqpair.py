import math
import theta_auto
import os
import pprint

import varial.monitor

background_samples = [
    'TTbar',
    'QCD',
    'WJets',
    'DYJets',
    'SingleTop',
]

def_dict_uncerts = {
'TTbar' : 1.10,
'QCD' : 1.50,
'WJets' : 1.10,
'DYJets' : 1.50,
'SingleTop' : 1.50,
}

def get_model(hist_dir, final_states, dict_uncerts=None):
    dict_uncerts_ = dict(def_dict_uncerts)
    if dict_uncerts:
        dict_uncerts_.update(dict_uncerts)
    model = theta_auto.build_model_from_rootfile(
        hist_dir,
        include_mc_uncertainties = True)#mc uncertainties=true
    model.fill_histogram_zerobins()
    if final_states:
        if isinstance(final_states, str):
            final_states = [final_states]
        model.set_signal_processes(final_states)
    else:
        model.set_signal_process_groups({'':[]})
    # for process, factor in branching_ratios:
    #     model.scale_predictions(factor, process, observable)
    # model.add_lognormal_uncertainty('ttbar_rate', math.log(1.15), 'TTbar')
    # model.add_lognormal_uncertainty('ttbar_rate', math.log(dict_uncerts_['TTbar']), 'TTbar')
    model.add_lognormal_uncertainty('qcd_rate', math.log(dict_uncerts_['QCD']), 'QCD')
    # model.add_lognormal_uncertainty('wjets_rate', math.log(1.15), 'WJets')
    # model.add_lognormal_uncertainty('wjets_rate', math.log(dict_uncerts_['WJets']), 'WJets')
    # model.add_lognormal_uncertainty('zjets_rate', math.log(dict_uncerts_['DYJets']), 'DYJets')
    model.add_lognormal_uncertainty('singlet_rate', math.log(dict_uncerts_['SingleTop']), 'SingleTop')
    for smpl in background_samples:
        model.add_lognormal_uncertainty('luminosity', math.log(1.027), smpl)
    return model
