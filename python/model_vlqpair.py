import math
import os
import pprint
import cPickle

import varial.monitor
import varial.analysis

background_samples = [
    'TTbar',
    'QCD',
    'WJets',
    'DYJets',
    'SingleTop',
]

dict_uncerts_default = {
    'TTbar' : 1.20,
    'WJets' : 1.20,
    'DYJets' : 1.20,
    'SingleTop' : 1.20,
    'Diboson' : 1.20,
    'QCD' : 2.0,
}


def get_model_no_norm(dict_uncerts=None):
    def tmp(hist_dir, final_states=None, scale=None):
        import theta_auto

        model = theta_auto.build_model_from_rootfile(
            hist_dir,
            include_mc_uncertainties = True)#mc uncertainties=true
        model.fill_histogram_zerobins()

        if scale:
            model.scale_predictions(scale)

        if final_states:
            if isinstance(final_states, str):
                final_states = [final_states]
            model.set_signal_processes(final_states)
        else:
            model.set_signal_process_groups({'':[]})
        if dict_uncerts:
            for s, u in dict_uncerts.iteritems():
                model.add_lognormal_uncertainty(s+'_rate', math.log(u), s)

        obsvs = model.observables.keys()
        for obs in obsvs:
            if 'El45' in obs:
                model.add_lognormal_uncertainty('sfel_trg', math.log(1.02), '*', obs)
        # model.add_lognormal_uncertainty('ttbar_rate', math.log(dict_uncerts['TTbar']), 'TTbar')
        # model.add_lognormal_uncertainty('wjets_rate', math.log(dict_uncerts['WJets']), 'WJets')
        # model.add_lognormal_uncertainty('qcd_rate', math.log(dict_uncerts['QCD']), 'QCD')
        # model.add_lognormal_uncertainty('zjets_rate', math.log(dict_uncerts['DYJets']), 'DYJets')
        # model.add_lognormal_uncertainty('singlet_rate', math.log(dict_uncerts['SingleTop']), 'SingleTop')
        for smpl in background_samples:
            model.add_lognormal_uncertainty('luminosity', math.log(1.027), smpl)
        return model
    return tmp


def get_model_with_norm(dict_uncerts=None):
    def tmp(hist_dir, final_states=None):
        import theta_auto

        # dict_uncerts = dict(dict_uncerts)
        # dict_uncerts.update({'TTbar' : 1.5, 'WJets' : 1.5,})
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
        if dict_uncerts:
            for s, u in dict_uncerts.iteritems():
                model.add_lognormal_uncertainty(s+'_rate', math.log(u), s)

        obsvs = model.observables.keys()
        for obs in obsvs:
            if 'El45' in obs:
                model.add_lognormal_uncertainty('sfel_trg', math.log(1.02), '*', obs)
        # model.add_lognormal_uncertainty('ttbar_rate', math.log(dict_uncerts['TTbar']), 'TTbar')
        # model.add_lognormal_uncertainty('wjets_rate', math.log(dict_uncerts['WJets']), 'WJets')
        # model.add_lognormal_uncertainty('qcd_rate', math.log(dict_uncerts['QCD']), 'QCD')
        # model.add_lognormal_uncertainty('zjets_rate', math.log(dict_uncerts['DYJets']), 'DYJets')
        # model.add_lognormal_uncertainty('singlet_rate', math.log(dict_uncerts['SingleTop']), 'SingleTop')
        # bkg_model_width = {'width': float('inf')}
        dist_dict = {'mean': 0.0,
                    'range': [float('-inf'), float('inf')],
                    'typ': 'gauss',
                    'width': float('inf')}
        model.distribution.distributions.update({
            'TTbar_rate' : dist_dict,
            'WJets_rate' : dist_dict})
        for smpl in background_samples:
            model.add_lognormal_uncertainty('luminosity', math.log(1.027), smpl)
        return model
    return tmp


def get_model_constr_uncerts(dict_path, prior_uncerts):
    def tmp(hist_dir, final_states=None):
        import theta_auto

        path = dict_path if os.path.exists(dict_path) else os.path.join(varial.analysis.cwd, dict_path)
        with open(path) as f:
            post_dict = cPickle.load(f)
        dict_uncerts = {}
        for s in prior_uncerts:
            uncert = post_dict['ST'].get(s+'_rate_post', None)
            if uncert:
                uncert = uncert/100.+1
            else:
                varial.monitor.message('model_vlq.get_model_constr_uncerts', 'WARNING no constraint found for sample %s' % s)
                uncert = prior_uncerts[s]
            dict_uncerts[s] = uncert

        # dict_uncerts = dict(dict_uncerts)
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
        if dict_uncerts:
            for s, u in dict_uncerts.iteritems():
                model.add_lognormal_uncertainty(s+'_rate', math.log(u), s)
                
        obsvs = model.observables.keys()
        for obs in obsvs:
            if 'El45' in obs:
                model.add_lognormal_uncertainty('sfel_trg', math.log(1.02), '*', obs)
        # model.add_lognormal_uncertainty('ttbar_rate', math.log(dict_uncerts['TTbar']), 'TTbar')
        # model.add_lognormal_uncertainty('wjets_rate', math.log(dict_uncerts['WJets']), 'WJets')
        # model.add_lognormal_uncertainty('qcd_rate', math.log(dict_uncerts['QCD']), 'QCD')
        # model.add_lognormal_uncertainty('zjets_rate', math.log(dict_uncerts['DYJets']), 'DYJets')
        # model.add_lognormal_uncertainty('singlet_rate', math.log(dict_uncerts['SingleTop']), 'SingleTop')
        for smpl in background_samples:
            model.add_lognormal_uncertainty('luminosity', math.log(1.027), smpl)
        return model
    return tmp
