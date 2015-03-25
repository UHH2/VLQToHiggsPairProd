#!/bin/bash

mkdir -p unmerged_files
hadd -f uhh2.AnalysisModuleRunner.MC.QCD.root uhh2.AnalysisModuleRunner.MC.QCD_HT250to500.root uhh2.AnalysisModuleRunner.MC.QCD_HT500to1000.root uhh2.AnalysisModuleRunner.MC.QCD_HT1000toInf.root
hadd -f uhh2.AnalysisModuleRunner.MC.WJets.root uhh2.AnalysisModuleRunner.MC.WJets_HT100to200.root uhh2.AnalysisModuleRunner.MC.WJets_HT200to400.root uhh2.AnalysisModuleRunner.MC.WJets_HT400to600.root uhh2.AnalysisModuleRunner.MC.WJets_HT600toInf.root
hadd -f uhh2.AnalysisModuleRunner.MC.ZJets.root uhh2.AnalysisModuleRunner.MC.ZJets_HT100to200.root uhh2.AnalysisModuleRunner.MC.ZJets_HT200to400.root uhh2.AnalysisModuleRunner.MC.ZJets_HT400to600.root uhh2.AnalysisModuleRunner.MC.ZJets_HT600toInf.root
mv uhh2.AnalysisModuleRunner.MC.WJets_HT* unmerged_files/
mv uhh2.AnalysisModuleRunner.MC.ZJets_HT* unmerged_files/
mv uhh2.AnalysisModuleRunner.MC.QCD_HT* unmerged_files/


