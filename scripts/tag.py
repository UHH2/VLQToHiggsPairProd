#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch()
ROOT.gROOT.ProcessLine('gErrorIgnoreLevel = kError;')

import os
import time
import varial.tools as tools


tagger = tools.GitTagger('/nfs/dust/cms/user/nowatsd/sFrameNew/CMSSW_7_4_0_pre6/src/UHH2/VLQToHiggsPairProd/GITTAGGER_LOG.txt')

tagger.run()

