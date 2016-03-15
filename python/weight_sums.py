#!/usr/bin/env python

from multiprocessing import Pool
import itertools
import glob
import os
import sys

# smpls = glob.glob('/pnfs/desy.de/cms/tier2/store/user/htholen/TpB_20151125/TprimeBToTH_M-*_TuneCUETP8M1_13TeV-madgraph-pythia8/crab_TprimeBToTH_M-*H_25ns/*/*/Ntuple_*.root')
# out_name = 'weight_dict_TpB'

if len(sys.argv) != 2:
    print "State whether you want to run over pdfs or scale variations!"
    exit(-1)

do_pdfs=True

if sys.argv[1] == 'pdf':
    out_name = 'weight_dict_pdf'
    do_pdfs = True
elif sys.argv[1] == 'scale':
    out_name = 'weight_dict_scale'
    do_pdfs = False
else:
    print "Provide either 'pdf' or 'scale'!"
    exit(-1)


smpls = glob.glob('/nfs/dust/cms/user/nowatsd/grid_control_new/gc-output/RunII-25ns-v2/tptp_signals/MC_TpTp_M-*_Ntuple.root')

# def get_name_pnfs(name):
#     name = name.replace('crab_', '').replace('_25ns', '')  # TprimeBToTH_M-700_LH
#     name = name.replace('ToTH', '_TH')  # TprimeB_TH_M-700_LH
#     name = name.replace('rime', '')  # TpB_TH_M-700_LH
#     name = name.replace('M-', 'M')  # TpB_TH_M700_LH
#     name = name.replace('M7', 'M07')  # TpB_TH_M0700_LH
#     name = name.replace('M8', 'M08')  # TpB_TH_M0700_LH
#     name = name.replace('M9', 'M09')  # TpB_TH_M0700_LH
#     name_lst = name.split('_')
#     name_lst = [name_lst[0], name_lst[1], name_lst[3], name_lst[2]]
#     name =  '_'.join(name_lst)  # TpB_TH_LH_M0700
#     name = 'Signal_' + name  # Signal_TpB_TH_LH_M0700
#     return name


# def get_name_nfs(name):
#     name = name.replace('MC_', 'Signal_') # MC_TpT_TH_LH_M1600
#     return name

fix_messup_name = {
    'TpTp_M-1600' : 'TpTp_M-0700',
    'TpTp_M-1700' : 'TpTp_M-0800',
    'TpTp_M-1800' : 'TpTp_M-0900',
    'TpTp_M-700' : 'TpTp_M-1000',
    'TpTp_M-800' : 'TpTp_M-1100',
    'TpTp_M-900' : 'TpTp_M-1200',
    'TpTp_M-1000' : 'TpTp_M-1300',
    'TpTp_M-1100' : 'TpTp_M-1400',
    'TpTp_M-1200' : 'TpTp_M-1500',
    'TpTp_M-1300' : 'TpTp_M-1600',
    'TpTp_M-1400' : 'TpTp_M-1700',
    'TpTp_M-1500' : 'TpTp_M-1800',
}

def get_name(smpl):
    name = get_basename(smpl)
    name = name.replace('MC_', '')
    name = fix_messup_name[name]
    return name


def get_basename(filename):
    filename = os.path.splitext(filename)[0]
    filename = os.path.basename(filename)
    tokens = filename.split('_')
    if tokens[-1] == 'Ntuple':              # grid control
        tokens = tokens[:-2]
    else:                                   # sframe batch
        tokens = tokens[:-1]
    basename = '_'.join(tokens)
    return basename


# def handle_sample(do_pdfs):
def tmp(smpl_grp):
    if do_pdfs:
        print 'Do pdfs!'
    else:
        print 'Do scales!'
    name = get_name(smpl_grp[0])
    print 'working on sample:', name
    import ROOT

    sum_events = 0.
    sum_weight = [0.]*100

    files = (ROOT.TFile(s) for s in smpl_grp)
    trees = (f.Get('AnalysisTree') for f in files)
    events = (e for t in trees for e in t)

    for e in events:
        if not sum_events % 10000:
            print 'at event:', sum_events, name
        sum_events += 1
        scale_uncert = e.genInfo.originalXWGTUP()
        if do_pdfs:
            for i in xrange(100):
                sum_weight[i] += e.genInfo.systweights()[110 + i]/scale_uncert

        else:
            for i in xrange(9):
                sum_weight[i] += e.genInfo.systweights()[i]/scale_uncert

    sum_weight = list(w / sum_events for w in sum_weight)
    print '='*15, 'TOTAL EVENTS:', sum_events, name
    return name, sum_weight
    # return tmp

smpls = sorted(smpls)
smpl_grps = list(list(g) for _, g in itertools.groupby(smpls, get_basename))

pool = Pool(24)
weight_dict = dict(pool.imap_unordered(tmp, smpl_grps))
print weight_dict
with open(out_name, 'w') as f:
    f.write(repr(weight_dict))