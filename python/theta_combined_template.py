import os,sys
from operator import itemgetter,attrgetter
import theta_auto

outDir = os.environ['CMSSW_BASE']+'/src/theta/utils/optimization/limits/lep40_MET80_leadJet450_subLeadJet75_leadbJet0_ST0_HT0'

input0H = '/uscms_data/d3/ssagir/ljmet/CMSSW_7_3_0/src/LJMet/macros/optimization_condor/templates_2015_8_3_4_23_24/lep40_MET80_leadJet450_subLeadJet75_leadbJet0_ST0_HT0/templates_HT_T53T53M900left_5fb_lep40_MET80_leadJet450_subLeadJet75_leadbJet0_ST0_HT0.root'

input1H = ''

rFileName = input0H.split('/')[-1][:-5]
                                                                                                                                          
def get0H_model(input_file=input0H):
    model = theta_auto.build_model_from_rootfile(input_file,include_mc_uncertainties=True)#,histogram_filter = (lambda s: s.count('jec')==0 and s.count('jer')==0)
    
    model.fill_histogram_zerobins()
    model.set_signal_processes('TpTp_M-*')
    
    procs = model.processes
    obsvs = model.observables.keys()
    
    for obs in obsvs:
        if 'isE' in obs:
            try: model.add_lognormal_uncertainty('elTrigSys', math.log(1.05), '*', obs)
            except: pass
            try: model.add_lognormal_uncertainty('elIdSys', math.log(1.01), '*', obs)
            except: pass
            try: model.add_lognormal_uncertainty('elIsoSys', math.log(1.01), '*', obs)
            except: pass
        elif 'isM' in obs:
            try: model.add_lognormal_uncertainty('muTrigSys', math.log(1.05), '*', obs)
            except: pass
            try: model.add_lognormal_uncertainty('muIdSys', math.log(1.01), '*', obs)
            except: pass
            try: model.add_lognormal_uncertainty('muIsoSys', math.log(1.01), '*', obs)
            except: pass
    try: model.add_lognormal_uncertainty('lumiSys', math.log(1.027), '*', '*')
    except: pass
#     try: model.add_lognormal_uncertainty('MC', math.log(1.50), 'qcd', '*')
#     except: pass
#     try: model.add_lognormal_uncertainty('MC', math.log(1.055), 'top', '*')
#     except: pass
#     try: model.add_lognormal_uncertainty('MC', math.log(1.05), 'ewk', '*')
#     except: pass

    #modeling uncertainties -- TOP
    #top_0p_1 : 0.0329102713402
    #top_0p_0 : 0.112672510016
    #top_0p_2p : 0.0269434949196

    for obs in obsvs:
        if 'nW0_nB0' in obs:
            try: model.add_lognormal_uncertainty('top0W0BSys',  math.log(1.113), 'top', obs) # from ttbar CR
            except: pass
        if 'nW0_nB1' in obs:
            try: model.add_lognormal_uncertainty('top0W1BSys',  math.log(1.033), 'top', obs) # from ttbar CR
            except: pass
        if 'nW0_nB2' in obs:
            try: model.add_lognormal_uncertainty('top0W2BSys',  math.log(1.027), 'top', obs) # from ttbar CR
            except: pass
        if 'nW0_nB3p' in obs:
            try: model.add_lognormal_uncertainty('top0W3pBSys', math.log(1.027), 'top', obs) # from ttbar CR
            except: pass
        if 'nW1p_nB0' in obs:
            try: model.add_lognormal_uncertainty('top1pW0BSys', math.log(1.113), 'top', obs) # from ttbar CR
            except: pass
        if 'nW1p_nB1' in obs:
            try: model.add_lognormal_uncertainty('top1pW1BSys', math.log(1.033), 'top', obs) # from ttbar CR
            except: pass
        if 'nW1p_nB2' in obs:
            try: model.add_lognormal_uncertainty('top1pW2BSys', math.log(1.027), 'top', obs) # from ttbar CR
            except: pass
        if 'nW1p_nB3p' in obs:
            try: model.add_lognormal_uncertainty('top1pW3pBSys',math.log(1.027), 'top', obs) # from ttbar CR
            except: pass

	#modeling uncertainties -- EWK
    #ewk_1p_0p : 0.0187917020575
    #ewk_0_0p : 0.191617716032
    for obs in obsvs:
        if 'nW0_nB0' in obs:
            try: model.add_lognormal_uncertainty('ewk0W0BSys',  math.log(1.192), 'ewk', obs) # from Wjets CR
            except: pass
        if 'nW0_nB1' in obs:
            try: model.add_lognormal_uncertainty('ewk0W1BSys',  math.log(1.192), 'ewk', obs) # from Wjets CR
            except: pass
        if 'nW0_nB2' in obs:
            try: model.add_lognormal_uncertainty('ewk0W2BSys',  math.log(1.192), 'ewk', obs) # from Wjets CR
            except: pass
        if 'nW0_nB3p' in obs:
            try: model.add_lognormal_uncertainty('ewk0W3pBSys', math.log(1.192), 'ewk', obs) # from Wjets CR
            except: pass
        if 'nW1p_nB0' in obs:
            try: model.add_lognormal_uncertainty('ewk1pW0BSys', math.log(1.019), 'ewk', obs) # from Wjets CR
            except: pass
        if 'nW1p_nB1' in obs:
            try: model.add_lognormal_uncertainty('ewk1pW1BSys', math.log(1.019), 'ewk', obs) # from Wjets CR
            except: pass
        if 'nW1p_nB2' in obs:
            try: model.add_lognormal_uncertainty('ewk1pW2BSys', math.log(1.019), 'ewk', obs) # from Wjets CR
            except: pass
        if 'nW1p_nB3p' in obs:
            try: model.add_lognormal_uncertainty('ewk1pW3pBSys',math.log(1.019), 'ewk', obs) # from Wjets CR
            except: pass

    #modeling uncertainties -- TOP -- CORRELATED
#     for obs in obsvs:
# 		if 'nW0_nB0' in obs:
# 			try: model.add_lognormal_uncertainty('topCRSys', math.log(1.15), 'top', obs) # from ttbar CR
# 			except: pass
# 		if 'nW0_nB1' in obs:
# 			try: model.add_lognormal_uncertainty('topCRSys', math.log(1.12), 'top', obs) # from ttbar CR
# 			except: pass
# 		if 'nW0_nB2' in obs:
# 			try: model.add_lognormal_uncertainty('topCRSys', math.log(1.02), 'top', obs) # from ttbar CR
# 			except: pass
# 		if 'nW0_nB3p' in obs:
# 			try: model.add_lognormal_uncertainty('topCRSys', math.log(1.02), 'top', obs) # from ttbar CR
# 			except: pass
# 		if 'nW1p_nB0' in obs:
# 			try: model.add_lognormal_uncertainty('topCRSys', math.log(1.15), 'top', obs) # from ttbar CR
# 			except: pass
# 		if 'nW1p_nB1' in obs:
# 			try: model.add_lognormal_uncertainty('topCRSys', math.log(1.12), 'top', obs) # from ttbar CR
# 			except: pass
# 		if 'nW1p_nB2' in obs:
# 			try: model.add_lognormal_uncertainty('topCRSys', math.log(1.02), 'top', obs) # from ttbar CR
# 			except: pass
# 		if 'nW1p_nB3p' in obs:
# 			try: model.add_lognormal_uncertainty('topCRSys', math.log(1.02), 'top', obs) # from ttbar CR
# 			except: pass

	#modeling uncertainties -- EWK -- CORRELATED
#     for obs in obsvs:
# 		if 'nW0_nB0' in obs:
# 			try: model.add_lognormal_uncertainty('ewkCRSys', math.log(1.22), 'ewk', obs) # from Wjets CR
# 			except: pass
# 		if 'nW0_nB1' in obs:
# 			try: model.add_lognormal_uncertainty('ewkCRSys', math.log(1.22), 'ewk', obs) # from Wjets CR
# 			except: pass
# 		if 'nW0_nB2' in obs:
# 			try: model.add_lognormal_uncertainty('ewkCRSys', math.log(1.22), 'ewk', obs) # from Wjets CR
# 			except: pass
# 		if 'nW0_nB3p' in obs:
# 			try: model.add_lognormal_uncertainty('ewkCRSys', math.log(1.22), 'ewk', obs) # from Wjets CR
# 			except: pass
# 		if 'nW1p_nB0' in obs:
# 			try: model.add_lognormal_uncertainty('ewkCRSys', math.log(1.02), 'ewk', obs) # from Wjets CR
# 			except: pass
# 		if 'nW1p_nB1' in obs:
# 			try: model.add_lognormal_uncertainty('ewkCRSys', math.log(1.02), 'ewk', obs) # from Wjets CR
# 			except: pass
# 		if 'nW1p_nB2' in obs:
# 			try: model.add_lognormal_uncertainty('ewkCRSys', math.log(1.02), 'ewk', obs) # from Wjets CR
# 			except: pass
# 		if 'nW1p_nB3p' in obs:
# 			try: model.add_lognormal_uncertainty('ewkCRSys', math.log(1.02), 'ewk', obs) # from Wjets CR
# 			except: pass
   
    #flat uncertainties for optimization
#     try: model.add_lognormal_uncertainty('topSys', math.log(1.25), 'top', '*')
#     except: pass
#     try: model.add_lognormal_uncertainty('ewkSys', math.log(1.50), 'ewk', '*')
#     except: pass
#     try: model.add_lognormal_uncertainty('qcdSys', math.log(2.00), 'qcd', '*')
#     except: pass
#     try: model.add_lognormal_uncertainty('sigSys', math.log(1.15), 'sig', '*')
#     except: pass

    return model

def get1H_model():
    model = theta_auto.build_model_from_rootfile(input1H,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('Sideband')==0))
    
    model.fill_histogram_zerobins()
    model.set_signal_processes('TpTp_M*')
    
    procs = model.processes
    obsvs = model.observables.keys()
    
    try: model.add_lognormal_uncertainty('NormWJet1H', math.log(1.06), 'Wjets', '*')
    except: pass
    try: model.add_lognormal_uncertainty('NormTTbar1H', math.log(1.087), 'TTbar', '*')
    except: pass
    try: model.add_lognormal_uncertainty('NormZJet1H', math.log(1.20), 'DYJets', '*')
    except: pass
    try: model.add_lognormal_uncertainty('NormST1H', math.log(1.20), 'ST', '*')
    except: pass
    try: model.add_lognormal_uncertainty('NormVV1H', math.log(1.20), 'VV', '*')
    except: pass
    try: model.add_lognormal_uncertainty('NormQCD1H', math.log(2.00), 'QCD', '*')
    except: pass
    try: model.add_lognormal_uncertainty('lumiSys', math.log(1.027), '*', '*')
    except: pass

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
