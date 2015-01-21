#!/usr/bin/env python

#######

#  automatized plots generator for b-tagging performances
#  Adrien Caudron, 2013, UCL

#######

#import all what is needed
import copy
from NIhistoStyle import *
#parser options
from optparse import OptionParser
usage="""%prog [options]"""
description="""A simple script to generate validation plots"""
epilog="""Example:
plotFactory.py -f BTagRelVal_TTbar_Startup_600.root -F BTagRelVal_TTbar_Startup_600gspre3.root -r 600 -R 600gspre3 -s TTbar_Startup -S TTbar_Startup 
"""
parser = OptionParser(usage=usage,add_help_option=True,description=description,epilog=epilog)
parser.add_option("-f", "--valInputFile", dest="valPath", default=fileNameVal,
                  help="Read input file for sample to validated", metavar="VALFILE")
parser.add_option("-F", "--refInputFile", dest="refPath", default=fileNameRef,
                  help="Read input file for reference sample", metavar="RAFFILE")
parser.add_option("-r", "--valReleaseName", dest="ValRel", default=ValRel,
                  help="Name to refer to the release/conditions to validate, ex: 600, GTV18 ...", metavar="VALREL")
parser.add_option("-R", "--refReleaseName", dest="RefRel", default=RefRel,
                  help="Name to refer to the reference release/conditions, ex: 600pre11, GTV16 ...", metavar="REFREL")
parser.add_option("-s", "--valSampleName", dest="ValSample", default=ValSample,
                  help="Name to refer to the sample name to validate, ex: TTbar_FullSim, 2012C ...", metavar="VALSAMPLE")
parser.add_option("-S", "--refSampleName", dest="RefSample", default=RefSample,
                  help="Name to refer to the reference sample name, ex: TTbar_FullSim, 2012C ...", metavar="REFSAMPLE")
parser.add_option("-b", "--batch", dest="batch", default=batch,
                  action="store_true", help="if False, the script will run in batch mode")
parser.add_option("-l", "--drawLegend", dest="drawLegend", default=drawLegend,
                  action="store_true", help="if True the legend will be drawn on top of the plots")
parser.add_option("-p", "--printBanner", dest="printBanner", default=printBanner,
                  action="store_true", help="if True, a banner will be print on top of the plots")
parser.add_option("-B", "--Banner", dest="Banner", default=Banner,
                  help="String to write as banner on top of the plots, option -B should be used")
parser.add_option("-n", "--noRatio", dest="doRatio", default=doRatio,
                  action="store_false", help="if True, ratios plots will be created")
(options, args) = parser.parse_args()
#print "file for validation", options.valPath, "file for reference", options.refPath
#print "Validation release:", options.ValRel, "Reference release:", options.RefRel
#print "Validation sample:", options.ValSample, "Reference sample:", options.RefSample
#print "Options : batch mode ?", options.batch, "draw legend ?", options.drawLegend, "print banner ?", options.printBanner, "banner is ", options.Banner, "make ratio plots ?", options.doRatio
#define the input root files                                                                                                                                                                              
if options.valPath :
	fileVal = TFile(options.valPath,"READ")
#batch mode ?
if options.batch : ROOT.gROOT.SetBatch()
# style
_style = Style.Style()
_style.SetStyle()
#title
if options.ValSample==options.RefSample : title=options.ValRel+"vs"+options.RefRel+" "+options.ValSample+" "
elif options.ValRel==options.RefRel : title=options.ValRel+" "+options.ValSample+"_vs_"+options.RefSample+" "
elif not options.RefSample and not options.RefRel : title=options.ValRel+" "+options.ValSample+" "
else : title=options.ValRel+"vs"+options.RefRel+" "+options.ValSample+"_vs_"+options.RefSample+" "
#declaration

for rhocut in rhoRange :
    for version in range (0, maxRange) :
        for version2 in range (version, maxRange) :
            for compTag in tagCombos : #  ["compStand","compAll", "compRho", "comp2", "comp1"]
                for tagger in taggers :
                    mapColor = mapColorStandard
                    listTag = [tagger+"-StandardRho25"]
                    tagselection = "rho"+rhocut+"v"
                    if compTag == "compStand" and rhocut == "25" and version == 0 and version2 == version :
                        listTag = []
                        for comp in rhoRange:
                            listTag.append(tagger+"-StandardRho"+comp)
                        tagselection = "compAllRho"
                    elif compTag == "compAll" and version2 > version+1:
                        for x in range (version, version2+1) :
                            listTag.append(tagger+"-NICleanedRho"+rhocut+"v"+str(x))
                            tagselection = tagselection+"_"+str(x)
                    elif compTag == "compRho" and rhocut == "25" and version2 == version :
                        tagselection = "comp"
                        mapColor = mapColorRhoComp
                        for x in rhoRange :
                            if x != "25" : 
                                tagName = tagger+"-StandardRho"+x
                                listTag.append(tagName)
                            tagName = tagger+"-NICleanedRho"+x+"v"+str(version)
                            listTag.append(tagName)
                            tagselection = tagselection+"Rho"+x
                        tagselection = tagselection+"v"+str(version)
                    elif compTag == "comp2" and not version2 == version :
                        listTag.append(tagger+"-NICleanedRho"+rhocut+"v"+str(version))
                        listTag.append(tagger+"-NICleanedRho"+rhocut+"v"+str(version2))
                        tagselection = tagselection+str(version)+"_"+str(version2)
                    elif compTag == "comp1" and version2 == version :
                        listTag.append(tagger+"-NICleanedRho"+rhocut+"v"+str(version))
                        tagselection = tagselection+str(version)
                    else : continue
                    #print "\nTAGSELECTION:", tagselection, listTag, '\n'
                    DirName = DirPath+tagselection
                    c = {}
                    saveHistos = {}
                    Histos = {}
                    ratios = {}
                    #loop over eta an pt bins
                    for b in EtaPtBin :
                        #count = -1
                        #loop over the histos
                        perfAll = {}
                        for h in listHistos :
                            h.doNormalization = True
                            #print h
                            #print h.name
                            #count += 1
                            compAll = {}
                            compAll_keys = []
                            perfAll_keys = []
                            for f in listFlavors :
                                perfAll[f] = {}
                            #loop over the list of taggers
                            if h.listTagger is not None : listTag=h.listTagger
                            for tag in listTag :
                                keyHisto = tag+"_"+h.name+"_"+b
                                #print tag
                                if h.doPerformance :
                                    keyHisto = tag+"_performance_vs_"+h.tagFlavor
                                #loop over the flavours
                                histos = {}
                                passH = False
                                for f in listFlavors :
                                    path = pathInFile+tag+"_"+b+"/"+h.name+"_"+tag+"_"+b+f
                                    #if count > 4 and "CSVIVFv2-StandardRho9999" in tag :
                                        #path = pathInFile+tag+"-Tag_"+b+"/"+h.name+"_"+tag+"-Tag_"+b+f
                                    if "_B_" in path : 
                                        path=path.replace("_B_","_"+f+"_")
                                        path=path.replace(b+f,b)
                                    #print path
                                    #get histos
                                    histos[f] = fileVal.Get(path)
                                    if not histos[f] :
                                        print "ERROR :", path, "not found in the roofiles, please check the spelling or check if this histogram is present in the rootdile"
                                        passH = True
                                if passH : continue
                                #stop if FlavEffVsBEff_?_discr plot for all the taggers
                                if h.name=="FlavEffVsBEff_B_discr" :
                                    for f in listFlavors :
                                        perfAll[f][tag]=histos[f]
                                    perfAll_keys.append(tag)
                                    continue
                                elif compTag=="comp2" or compTag =="compRho" or compTag == "comp1" or compTag == "compStand":
                                    for f in listFlavors :
                                        compAll[tag+f]=histos[f]
                                        perfAll[f][tag]=histos[f]
                                        compAll_keys.append(tag+f)
                                    perfAll_keys.append(tag)
                                    continue
                                #create final histos   
                                if h.doPerformance :
                                    saveHistos[keyHisto]=graphProducer(plot=h,histos=histos,color=mapColorFlavour)
                                else :    
                                    saveHistos[keyHisto]=histoProducer(plot=h,histos=histos,keys=listFlavors,color=mapColorFlavour)
                                if saveHistos[keyHisto] is None : continue
                                #if len(saveHistos[keyHisto])!=len(refHistos[keyHisto]) : print "ERROR"
                                #compute ratios 
                                if options.doRatio :
                                    if h.doPerformance:
                                        ratiosList = createRatioFromGraph(saveHistos[keyHisto],refHistos[keyHisto])
                                    else :
                                        ratiosList = createRatio(saveHistos[keyHisto],refHistos[keyHisto])
                                    ratios[keyHisto] = ratiosList
                                else :
                                    ratiosList = None
                                #set name file
                                histname=h.name+"_"+tag
                                if options.ValSample == options.RefSample : saveName=options.ValRel+"vs"+options.RefRel+"_"+options.ValSample+"_all"
                                elif options.ValRel==options.RefRel : saveName=options.ValRel+"_"+options.ValSample+"_vs_"+options.RefSample+"_all"
                                elif not options.RefSample and not options.RefRel : saveName=options.ValRel+"_"+options.ValSample+"_all"
                                else : saveName=options.ValRel+"vs"+options.RefRel+"_"+options.ValSample+"_vs_"+options.RefSample+"_all"
                                #save canvas
                                c[keyHisto] = savePlots(title=title+tag,dirname=DirName+"/"+b,saveName=histname+"_"+saveName,listFromats=listFromats,plot=h,Histos=saveHistos[keyHisto],options=options,ratios=ratiosList,keyHisto=keyHisto,listLegend=listFlavors,legendName=h.legend)
                            #for FlavEffVsBEff_B_discr
                            if h.name=="FlavEffVsBEff_B_discr" :
                                for f in ["DUSG"] :
                                    print "FlavEffVsBEff_B_discr keys: ", perfAll_keys
                                    keyHisto=f+"perf"
                                    #setup the histos
                                    #print perfAll_keys
                                    Histos[keyHisto]=histoProducer(plot=h,histos=perfAll[f],keys=perfAll_keys,color=mapColor)
                                    #set name file    
                                    saveName=options.ValRel+"_"+options.ValSample+"_performance_Bvs"+f+"_"+b+"_"+tagger+"_"+tagselection
                                    #set title
                                    titleFlav = options.ValRel+"_"+options.ValSample+"_performance_Bvs"+f+"_"+tagselection
                                    #save canvas
                                    c[keyHisto] = savePlots(title=titleFlav,dirname=DirName+"/"+b,saveName=h.name+"_"+saveName,listFromats=listFromats,plot=h,Histos=Histos[keyHisto],keyHisto=keyHisto,listLegend=listTag,options=options,legendName=h.legend.replace("FLAV",f))
                            elif compTag == "comp2" or compTag == "compRho"  or compTag == "comp1" or compTag == "compStand":
                                #print "comp Variables:", compAll_keys
                                keyHisto=h.name+"_"+b+"_"+compTag
                                #setup the histos
                                Histos[keyHisto]=histoProducer(plot=h,histos=compAll,keys=compAll_keys,color=mapColor,drawOption="HIST")
                                #set name file    
                                saveName=options.ValRel+"_"+options.ValSample+"_"+tagger+"_"+tagselection
                                #set title
                                titleFlav = options.ValRel+"_"+options.ValSample+"_"+tagselection
                                #save canvas
                                c[keyHisto] = savePlots(title=titleFlav,dirname=DirName+"/"+b,saveName=h.name+"_"+saveName,listFromats=listFromats,plot=h,Histos=Histos[keyHisto],keyHisto=keyHisto,listLegend=compAll_keys,options=options,legendName=h.legend,drawOption="HIST")
                                for f in ["B","DUSG"] :
                                    #print "ListLegend: ", listTag
                                    keyHisto=h.name+"_"+b+"_"+f+"comp"
                                    #setup the histos
                                    #print perfAll_keys
                                    Histos[keyHisto]=histoProducer(plot=h,histos=perfAll[f],keys=perfAll_keys,color=mapColor)
                                    #set name file    
                                    saveName=options.ValRel+"_"+options.ValSample+"_"+f+"_"+tagger+"_"+tagselection
                                    #set title
                                    titleFlav = options.ValRel+"_"+options.ValSample+"_"+f+"_"+tagselection
                                    #save canvas
                                    c[keyHisto] = savePlots(title=titleFlav,dirname=DirName+"/"+b,saveName=h.name+"_"+saveName,listFromats=listFromats,plot=h,Histos=Histos[keyHisto],keyHisto=keyHisto,listLegend=listTag,options=options,legendName=h.legend, drawOption="HIST")