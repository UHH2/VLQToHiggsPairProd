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

dict_uncerts = {
'TTbar' : 1.10,
'WJets' : 1.10,
'QCD' : 1.8,
'DYJets' : 1.8,
'SingleTop' : 1.8,
}

def get_model(hist_dir, final_states):
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
    model.add_lognormal_uncertainty('ttbar_rate', math.log(dict_uncerts['TTbar']), 'TTbar')
    model.add_lognormal_uncertainty('qcd_rate', math.log(dict_uncerts['QCD']), 'QCD')
    model.add_lognormal_uncertainty('wjets_rate', math.log(dict_uncerts['WJets']), 'WJets')
    model.add_lognormal_uncertainty('zjets_rate', math.log(dict_uncerts['DYJets']), 'DYJets')
    model.add_lognormal_uncertainty('singlet_rate', math.log(dict_uncerts['SingleTop']), 'SingleTop')
    for smpl in background_samples:
        model.add_lognormal_uncertainty('luminosity', math.log(1.027), smpl)
    return model

def get_model_with_norm(hist_dir, final_states):
    dict_uncerts_ = dict(dict_uncerts)
    dict_uncerts_.update({'TTbar' : 1.5, 'WJets' : 1.5,})
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
    model.add_lognormal_uncertainty('ttbar_rate', math.log(dict_uncerts_['TTbar']), 'TTbar')
    model.add_lognormal_uncertainty('wjets_rate', math.log(dict_uncerts_['WJets']), 'WJets')
    model.add_lognormal_uncertainty('qcd_rate', math.log(dict_uncerts_['QCD']), 'QCD')
    model.add_lognormal_uncertainty('zjets_rate', math.log(dict_uncerts_['DYJets']), 'DYJets')
    model.add_lognormal_uncertainty('singlet_rate', math.log(dict_uncerts_['SingleTop']), 'SingleTop')
    bkg_model_width = {'width': float('inf')}
    dist_dict = {'mean': 0.0,
                'range': [float('-inf'), float('inf')],
                'typ': 'gauss',
                'width': float('inf')}
    model.distribution.distributions.update({
        'ttbar_rate' : dist_dict,
        'wjets_rate' : dist_dict})
    for smpl in background_samples:
        model.add_lognormal_uncertainty('luminosity', math.log(1.027), smpl)
    return model


def get_model_no_norm(hist_dir, final_states):
    dict_uncerts_ = dict(dict_uncerts)
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
    # model.add_lognormal_uncertainty('ttbar_rate', math.log(dict_uncerts_['TTbar']), 'TTbar')
    # model.add_lognormal_uncertainty('wjets_rate', math.log(dict_uncerts_['WJets']), 'WJets')
    model.add_lognormal_uncertainty('qcd_rate', math.log(dict_uncerts_['QCD']), 'QCD')
    model.add_lognormal_uncertainty('zjets_rate', math.log(dict_uncerts_['DYJets']), 'DYJets')
    model.add_lognormal_uncertainty('singlet_rate', math.log(dict_uncerts_['SingleTop']), 'SingleTop')
    for smpl in background_samples:
        model.add_lognormal_uncertainty('luminosity', math.log(1.027), smpl)
    return model