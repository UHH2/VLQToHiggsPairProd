#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch()
ROOT.gROOT.ProcessLine('gErrorIgnoreLevel = kError;')

import os
import time
import varial.tools as tools


tagger = tools.GitTagger('./GITTAGGER_LOG.txt')

tagger.run()

