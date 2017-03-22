#!/usr/bin/env python

from multiprocessing import Pool
import itertools
import glob
import os
import sys
import pprint


out_name = 'test_dm'
smpls = glob.glob('/pnfs/desy.de/cms/tier2/store/user/mmeyer/sframe-ntuples/RunII-ntuple-v3/signals/MC_TTbarDMJets_pseudoscalar_Mchi-10_Mphi-10_*.root')
pdf_offset = 110



def get_name(smpl):
    name = get_basename(smpl)
    name = name.replace('MC_', '')
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

def get_basename_ht_rew(smpl):
    filename = os.path.basename(smpl)
    filename = filename.split('.')[-2]
    tokens = filename.split('_')[:-1]
    basename = '_'.join(tokens)
    return basename


def tmp(smpl_grp):
    name = get_basename_ht_rew(smpl_grp[0])
    print 'working on sample:', name
    import ROOT

    sum_events = 0.
    sum_weight_pdf = [0.]*100
    sum_weight_scale = [0.]*9

    files = (ROOT.TFile(s) for s in smpl_grp)
    trees = (f.Get('AnalysisTree') for f in files)
    events = (e for t in trees for e in t)

    for e in events:
        if not sum_events % 10000:
            print 'at event:', sum_events, name
        sum_events += 1
        if sum_events == 100:
            break
        scale_uncert = e.genInfo.originalXWGTUP()
        for i in xrange(100):
            sum_weight_pdf[i] += e.genInfo.systweights()[pdf_offset + i]/scale_uncert

        for i in xrange(9):
            sum_weight_scale[i] += e.genInfo.systweights()[i]/scale_uncert

    sum_weight_pdf = list(w / sum_events for w in sum_weight_pdf)
    sum_weight_scale = list(w / sum_events for w in sum_weight_scale)
    return name, sum_weight_pdf, sum_weight_scale

smpls = sorted(smpls)
smpl_grps = list(list(g) for _, g in itertools.groupby(smpls, get_basename))

pool = Pool(24)
weight_list = list(pool.imap_unordered(tmp, smpl_grps))
weight_dict_pdf = dict((n, p) for n, p, _ in weight_list)
weight_dict_scale = dict((n, s) for n, _, s in weight_list)
with open('weight_dict_pdf_'+out_name, 'a') as f:
    f.write(repr(weight_dict_pdf))
with open('weight_dict_scale_'+out_name, 'a') as f:
    f.write(repr(weight_dict_scale))
