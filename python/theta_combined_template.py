import os,sys
from operator import itemgetter,attrgetter
import theta_auto
import math

outDir = os.environ['CMSSW_BASE']+'/src/theta/utils/optimization/limits/lep40_MET80_leadJet450_subLeadJet75_leadbJet0_ST0_HT0'

input0H = '/uscms_data/d3/ssagir/ljmet/CMSSW_7_3_0/src/LJMet/macros/optimization_condor/templates_2015_8_3_4_23_24/lep40_MET80_leadJet450_subLeadJet75_leadbJet0_ST0_HT0/templates_HT_T53T53M900left_5fb_lep40_MET80_leadJet450_subLeadJet75_leadbJet0_ST0_HT0.root'

input1H = ''

rFileName = input0H.split('/')[-1][:-5]
                                                                                                                                          
def get_full_model(input_file=input0H, signal='TpTp_M-*', histogram_filter=lambda w: True):
    model = theta_auto.build_model_from_rootfile(input_file, histogram_filter=histogram_filter, include_mc_uncertainties=True)#,histogram_filter = (lambda s: s.count('jec')==0 and s.count('jer')==0)
    
    model.fill_histogram_zerobins()
    if signal:
        model.set_signal_processes(signal)
    else:
        model.set_signal_process_groups({'':[]})
    
    procs = model.processes
    obsvs = model.observables.keys()

    for obs in obsvs:
        if 'SignalRegion' in obs or 'SidebandRegion' in obs:
            try: model.add_lognormal_uncertainty('TTbar_rate',  math.log(1.087), 'TTbar', obs) # from ttbar CR
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('WJets_rate',  math.log(1.06), 'WJets', obs) # from ttbar CR
            except RuntimeError: pass
            # try: model.add_lognormal_uncertainty('DYJets_rate',  math.log(1.2), 'DYJets', obs) # from ttbar CR
            # except RuntimeError: pass
            try: model.add_lognormal_uncertainty('QCD_rate',  math.log(2.00), 'QCD', obs) # from ttbar CR
            except RuntimeError: pass
            # try: model.add_lognormal_uncertainty('SingleTop_rate',  math.log(1.16), 'SingleTop', obs) # from ttbar CR
            # except RuntimeError: pass
            # try: model.add_lognormal_uncertainty('Diboson_rate',  math.log(1.15), 'Diboson', obs) # from ttbar CR
            # except RuntimeError: pass

    for obs in obsvs:
        if 'isE' in obs:
            try: model.add_lognormal_uncertainty('sfel_trg', math.log(1.05), '*', obs)
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('sfel_id', math.log(1.01), '*', obs)
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('sfel_iso', math.log(1.01), '*', obs)
            except RuntimeError: pass
        elif 'isM' in obs:
            try: model.add_lognormal_uncertainty('sfmu_trg', math.log(1.05), '*', obs)
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('sfmu_id', math.log(1.01), '*', obs)
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('sfmu_iso', math.log(1.01), '*', obs)
            except RuntimeError: pass
        elif 'El45' in obs:
            try: model.add_lognormal_uncertainty('sfel_trg', math.log(1.02), '*', obs)
            except RuntimeError: pass

    try: model.add_lognormal_uncertainty('luminosity', math.log(1.027), '*', '*')
    except RuntimeError: pass

    try: model.add_lognormal_uncertainty('SingleTop_rate',  math.log(1.16), 'SingleTop', '*') # from ttbar CR
    except RuntimeError: pass
    try: model.add_lognormal_uncertainty('Diboson_rate',  math.log(1.15), 'Diboson', '*') # from ttbar CR
    except RuntimeError: pass

    for proc in procs:
        if proc != 'TTbar': continue # and proc != 'SingleTop': continue
        for obs in obsvs:
            if 'nW0_nB0' in obs:
                try: model.add_lognormal_uncertainty('TTbar_rate',  math.log(1.111), proc, obs) # from ttbar CR
                except RuntimeError: pass
            if 'nW0_nB1' in obs:
                try: model.add_lognormal_uncertainty('TTbar_rate',  math.log(1.051), proc, obs) # from ttbar CR
                except RuntimeError: pass
            if 'nW0_nB2' in obs:
                try: model.add_lognormal_uncertainty('TTbar_rate',  math.log(1.055), proc, obs) # from ttbar CR
                except RuntimeError: pass
            if 'nW0_nB3p' in obs:
                try: model.add_lognormal_uncertainty('TTbar_rate', math.log(1.055), proc, obs) # from ttbar CR
                except RuntimeError: pass
            if 'nW1p_nB0' in obs:
                try: model.add_lognormal_uncertainty('TTbar_rate', math.log(1.111), proc, obs) # from ttbar CR
                except RuntimeError: pass
            if 'nW1p_nB1' in obs:
                try: model.add_lognormal_uncertainty('TTbar_rate', math.log(1.051), proc, obs) # from ttbar CR
                except RuntimeError: pass
            if 'nW1p_nB2' in obs:
                try: model.add_lognormal_uncertainty('TTbar_rate', math.log(1.055), proc, obs) # from ttbar CR
                except RuntimeError: pass
            if 'nW1p_nB3p' in obs:
                try: model.add_lognormal_uncertainty('TTbar_rate',math.log(1.055), proc, obs) # from ttbar CR
                except RuntimeError: pass

    for proc in procs:
        if proc != 'WJets': continue #proc != 'DYJets' and 
        for obs in obsvs:
            if 'nW0_nB0' in obs:
                try: model.add_lognormal_uncertainty('WJets_rate',  math.log(1.182), proc, obs) # from Wjets CR
                except RuntimeError: pass
            if 'nW0_nB1' in obs:
                try: model.add_lognormal_uncertainty('WJets_rate',  math.log(1.182), proc, obs) # from Wjets CR
                except RuntimeError: pass
            if 'nW0_nB2' in obs:
                try: model.add_lognormal_uncertainty('WJets_rate',  math.log(1.182), proc, obs) # from Wjets CR
                except RuntimeError: pass
            if 'nW0_nB3p' in obs:
                try: model.add_lognormal_uncertainty('WJets_rate', math.log(1.182), proc, obs) # from Wjets CR
                except RuntimeError: pass
            if 'nW1p_nB0' in obs:
                try: model.add_lognormal_uncertainty('WJets_rate', math.log(1.046), proc, obs) # from Wjets CR
                except RuntimeError: pass
            if 'nW1p_nB1' in obs:
                try: model.add_lognormal_uncertainty('WJets_rate', math.log(1.046), proc, obs) # from Wjets CR
                except RuntimeError: pass
            if 'nW1p_nB2' in obs:
                try: model.add_lognormal_uncertainty('WJets_rate', math.log(1.046), proc, obs) # from Wjets CR
                except RuntimeError: pass
            if 'nW1p_nB3p' in obs:
                try: model.add_lognormal_uncertainty('WJets_rate',math.log(1.046), proc, obs) # from Wjets CR
                except RuntimeError: pass


    return model

def get_model_ex_anticorr_chan(input_file=input0H, signal='TpTp_M-*', histogram_filter=lambda w: True):
    model = get_full_model(input_file, signal, histogram_filter)
    
    obsvs = model.observables.keys()

    for obs in obsvs:
        if 'SignalRegion' in obs or 'SidebandRegion' in obs:
            try: model.add_lognormal_uncertainty('htag_eff',  math.log(1.03), '*', obs) # from ttbar CR
            except RuntimeError: pass
        if 'minMlb' in obs:
            try: model.add_lognormal_uncertainty('htag_eff', math.log(0.97), '*', obs)
            except RuntimeError: pass

    return model

def get_model_ex_corr_chan(input_file=input0H, signal='TpTp_M-*', histogram_filter=lambda w: True):
    model = get_full_model(input_file, signal, histogram_filter)
    
    obsvs = model.observables.keys()
    
    for obs in obsvs:
        # if 'SignalRegion' in obs or 'SidebandRegion' in obs:
        try: model.add_lognormal_uncertainty('htag_eff',  math.log(1.03), '*', obs) # from ttbar CR
        except RuntimeError: pass
        # if 'minMlb' in obs:
        #     try: model.add_lognormal_uncertainty('htag_eff', math.log(1.03), '*', obs)
        #     except RuntimeError: pass

    return model

def get_model_ex_corr_btag(input_file=input0H, signal='TpTp_M-*', histogram_filter=lambda w: True):
    model = get_full_model(input_file, signal, histogram_filter)
    
    obsvs = model.observables.keys()

    for obs in obsvs:
        # if 'SignalRegion' in obs or 'SidebandRegion' in obs:
        try: model.add_lognormal_uncertainty('btag_bc',  math.log(1.03), '*', obs) # from ttbar CR
        except RuntimeError: pass
        # if 'minMlb' in obs:
        #     try: model.add_lognormal_uncertainty('btag_bc', math.log(0.97), '*', obs)
        #     except RuntimeError: pass

    return model

def get_model_ex_anticorr_btag(input_file=input0H, signal='TpTp_M-*', histogram_filter=lambda w: True):
    model = get_full_model(input_file, signal, histogram_filter)
    
    obsvs = model.observables.keys()

    for obs in obsvs:
        if 'SignalRegion' in obs or 'SidebandRegion' in obs:
            try: model.add_lognormal_uncertainty('btag_bc',  math.log(1.03), '*', obs) # from ttbar CR
            except RuntimeError: pass
        if 'minMlb' in obs:
            try: model.add_lognormal_uncertainty('btag_bc', math.log(0.97), '*', obs)
            except RuntimeError: pass

    return model

def get_bkg_only_model(input_file=input0H, signal='TpTp_M-*', histogram_filter=lambda w: True):
    model = theta_auto.build_model_from_rootfile(input_file, histogram_filter=histogram_filter, include_mc_uncertainties=True)#,histogram_filter = (lambda s: s.count('jec')==0 and s.count('jer')==0)
    
    model.fill_histogram_zerobins()
    if signal:
        model.set_signal_processes(signal)
    else:
        model.set_signal_process_groups({'':[]})
    
    procs = model.processes
    obsvs = model.observables.keys()

    for obs in obsvs:
        if 'SignalRegion' in obs or 'SidebandRegion' in obs:
            try: model.add_lognormal_uncertainty('TTbar_rate',  math.log(1.087), 'TTbar', obs) # from ttbar CR
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('WJets_rate',  math.log(1.06), 'WJets', obs) # from ttbar CR
            except RuntimeError: pass
            # try: model.add_lognormal_uncertainty('DYJets_rate',  math.log(1.2), 'DYJets', obs) # from ttbar CR
            # except RuntimeError: pass
            try: model.add_lognormal_uncertainty('QCD_rate',  math.log(2.00), 'QCD', obs) # from ttbar CR
            except RuntimeError: pass
            # try: model.add_lognormal_uncertainty('SingleTop_rate',  math.log(1.16), 'SingleTop', obs) # from ttbar CR
            # except RuntimeError: pass
            # try: model.add_lognormal_uncertainty('Diboson_rate',  math.log(1.15), 'Diboson', obs) # from ttbar CR
            # except RuntimeError: pass

    for obs in obsvs:
        if 'isE' in obs:
            try: model.add_lognormal_uncertainty('sfel_trg', math.log(1.05), '*', obs)
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('sfel_id', math.log(1.01), '*', obs)
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('sfel_iso', math.log(1.01), '*', obs)
            except RuntimeError: pass
        elif 'isM' in obs:
            try: model.add_lognormal_uncertainty('sfmu_trg', math.log(1.05), '*', obs)
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('sfmu_id', math.log(1.01), '*', obs)
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('sfmu_iso', math.log(1.01), '*', obs)
            except RuntimeError: pass
        elif 'El45' in obs:
            try: model.add_lognormal_uncertainty('sfel_trg', math.log(1.02), '*', obs)
            except RuntimeError: pass

    try: model.add_lognormal_uncertainty('luminosity', math.log(1.027), '*', '*')
    except RuntimeError: pass

    try: model.add_lognormal_uncertainty('SingleTop_rate',  math.log(1.16), 'SingleTop', '*') # from ttbar CR
    except RuntimeError: pass
    try: model.add_lognormal_uncertainty('Diboson_rate',  math.log(1.15), 'Diboson', '*') # from ttbar CR
    except RuntimeError: pass

    for proc in procs:
        if proc != 'TTbar': continue # and proc != 'SingleTop': continue
        for obs in obsvs:
            if 'nW0_nB0' in obs:
                try: model.add_lognormal_uncertainty('TTbar_rate',  math.log(1.111), proc, obs) # from ttbar CR
                except RuntimeError: pass
            if 'nW0_nB1' in obs:
                try: model.add_lognormal_uncertainty('TTbar_rate',  math.log(1.051), proc, obs) # from ttbar CR
                except RuntimeError: pass
            if 'nW0_nB2' in obs:
                try: model.add_lognormal_uncertainty('TTbar_rate',  math.log(1.055), proc, obs) # from ttbar CR
                except RuntimeError: pass
            if 'nW0_nB3p' in obs:
                try: model.add_lognormal_uncertainty('TTbar_rate', math.log(1.055), proc, obs) # from ttbar CR
                except RuntimeError: pass
            if 'nW1p_nB0' in obs:
                try: model.add_lognormal_uncertainty('TTbar_rate', math.log(1.111), proc, obs) # from ttbar CR
                except RuntimeError: pass
            if 'nW1p_nB1' in obs:
                try: model.add_lognormal_uncertainty('TTbar_rate', math.log(1.051), proc, obs) # from ttbar CR
                except RuntimeError: pass
            if 'nW1p_nB2' in obs:
                try: model.add_lognormal_uncertainty('TTbar_rate', math.log(1.055), proc, obs) # from ttbar CR
                except RuntimeError: pass
            if 'nW1p_nB3p' in obs:
                try: model.add_lognormal_uncertainty('TTbar_rate',math.log(1.055), proc, obs) # from ttbar CR
                except RuntimeError: pass

    for proc in procs:
        if proc != 'WJets': continue #proc != 'DYJets' and 
        for obs in obsvs:
            if 'nW0_nB0' in obs:
                try: model.add_lognormal_uncertainty('WJets_rate',  math.log(1.182), proc, obs) # from Wjets CR
                except RuntimeError: pass
            if 'nW0_nB1' in obs:
                try: model.add_lognormal_uncertainty('WJets_rate',  math.log(1.182), proc, obs) # from Wjets CR
                except RuntimeError: pass
            if 'nW0_nB2' in obs:
                try: model.add_lognormal_uncertainty('WJets_rate',  math.log(1.182), proc, obs) # from Wjets CR
                except RuntimeError: pass
            if 'nW0_nB3p' in obs:
                try: model.add_lognormal_uncertainty('WJets_rate', math.log(1.182), proc, obs) # from Wjets CR
                except RuntimeError: pass
            if 'nW1p_nB0' in obs:
                try: model.add_lognormal_uncertainty('WJets_rate', math.log(1.046), proc, obs) # from Wjets CR
                except RuntimeError: pass
            if 'nW1p_nB1' in obs:
                try: model.add_lognormal_uncertainty('WJets_rate', math.log(1.046), proc, obs) # from Wjets CR
                except RuntimeError: pass
            if 'nW1p_nB2' in obs:
                try: model.add_lognormal_uncertainty('WJets_rate', math.log(1.046), proc, obs) # from Wjets CR
                except RuntimeError: pass
            if 'nW1p_nB3p' in obs:
                try: model.add_lognormal_uncertainty('WJets_rate',math.log(1.046), proc, obs) # from Wjets CR
                except RuntimeError: pass


    return model


def get_bkg_only_model_flat(input_file=input0H, signal='TpTp_M-*', histogram_filter=lambda w: True):
    model = theta_auto.build_model_from_rootfile(input_file, histogram_filter=histogram_filter, include_mc_uncertainties=True)#,histogram_filter = (lambda s: s.count('jec')==0 and s.count('jer')==0)
    
    model.fill_histogram_zerobins()
    if signal:
        model.set_signal_processes(signal)
    else:
        model.set_signal_process_groups({'':[]})
    
    procs = model.processes
    obsvs = model.observables.keys()
    
    for obs in obsvs:
        if 'isE' in obs:
            try: model.add_lognormal_uncertainty('sfel_trg', math.log(1.05), '*', obs)
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('sfel_id', math.log(1.01), '*', obs)
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('sfel_iso', math.log(1.01), '*', obs)
            except RuntimeError: pass
        elif 'isM' in obs:
            try: model.add_lognormal_uncertainty('sfmu_trg', math.log(1.05), '*', obs)
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('sfmu_id', math.log(1.01), '*', obs)
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('sfmu_iso', math.log(1.01), '*', obs)
            except RuntimeError: pass
        elif 'El45' in obs:
            try: model.add_lognormal_uncertainty('sfel_trg', math.log(1.02), '*', obs)
            except RuntimeError: pass
    try: model.add_lognormal_uncertainty('luminosity', math.log(1.027), '*', '*')
    except RuntimeError: pass

    for obs in obsvs:
        # if 'SignalRegion' in obs:
        try: model.add_lognormal_uncertainty('TTbar_rate',  math.log(1.80), 'TTbar', obs) # from ttbar CR
        except RuntimeError: pass
        try: model.add_lognormal_uncertainty('WJets_rate',  math.log(1.80), 'WJets', obs) # from ttbar CR
        except RuntimeError: pass
        try: model.add_lognormal_uncertainty('QCD_rate',  math.log(2.00), 'QCD', obs) # from ttbar CR
        except RuntimeError: pass
        try: model.add_lognormal_uncertainty('SingleTop_rate',  math.log(1.16), 'SingleTop', obs) # from ttbar CR
        except RuntimeError: pass
        try: model.add_lognormal_uncertainty('Diboson_rate',  math.log(1.15), 'Diboson', obs) # from ttbar CR
        except RuntimeError: pass


    dist_dict = {'mean': 0.0,
                'range': [float('-inf'), float('inf')],
                'typ': 'gauss',
                'width': float('inf')}
    # model.distribution.distributions.update({
    #     'TTbar_rate' : dist_dict,
    #     'WJets_rate' : dist_dict})


    return model


##################################################################################################################

if __name__ == '__main__':
    Model0H = get0H_model()

    #Model1H = get1H_model()
    #Model0H.combine(Model1H)

    model_summary(Model0H)

    #Bayesian Limits
    plot_exp, plot_obs = bayesian_limits(Model0H,'all', n_toy = 5000, n_data = 500)
    #plot_exp, plot_obs = bayesian_limits(model,'expected')
    plot_exp.write_txt('limits_'+rFileName+'_expected.txt')
    plot_obs.write_txt('limits_'+rFileName+'_observed.txt')

    report.write_html('htmlout_'+rFileName)
