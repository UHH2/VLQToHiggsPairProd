
####### 

#  automatized plots generator for b-tagging performances
#  Adrien Caudron, 2013, UCL

#######

class plotInfo :
    def __init__ (self, name, title, #mandatory
                  legend="", Xlabel="", Ylabel="", logY=False, grid=False,
                  binning=None, Rebin=None,
                  doNormalization=False,
                  listTagger=None,
                  doPerformance=False, tagFlavor="B", mistagFlavor=["C","DUSG"], legPos=[]):
        self.name = name #name of the histos without postfix as PT/ETA bin or flavor
        self.title = title #title of the histograms : better if specific for the histogram
        self.legend = legend #legend name, if contain 'KEY', it will be replace by the list of keys you provide (as flavor, tagger ...)
        self.Xlabel = Xlabel #label of the X axis
        self.Ylabel = Ylabel #label of the Y axis
        self.logY = logY #if True : Y axis will be in log scale
        self.grid = grid #if True : a grid will be drawn
        self.binning = binning #if you want to change the binning put a list with [nBins,xmin,xmax]
        self.Rebin = Rebin #if you want to rebin the histos
        self.doNormalization = doNormalization #if you want to normalize to 1 all the histos 
        self.legPos = legPos
        self.doPerformance = doPerformance #if you want to draw the performance as TGraph
        if self.doPerformance : 
            #replace TAG by the tag flavor choosen (B, C, UDSG ...)
            self.title = name.replace("TAG",tagFlavor)
            self.Xlabel = Xlabel.replace("TAG",tagFlavor)
            self.Ylabel = Ylabel.replace("TAG",tagFlavor)
            self.legend = legend.replace("TAG",tagFlavor)
            self.tagFlavor = tagFlavor
            self.mistagFlavor = mistagFlavor
        if listTagger is None :
            self.listTagger=None #you will take the list of tagger defined centrally
        else :
            self.listTagger=listTagger #you take the list passed as argument
#define here the histograms you interested by
#by jets
jetPt = plotInfo(name="jetPt", title="Pt of all jets", legend="KEY-jets", Xlabel="Pt (GeV/c)", Ylabel="abitrary units",
                 logY=True, grid=False,
                 binning=[300,10.,310.], Rebin=20, doNormalization=False
                 )
jetEta = plotInfo(name="jetEta", title="Eta of all jets", legend="KEY-jets", Xlabel="#eta", Ylabel="abitrary units",
                  logY=True, grid=False,
                  binning=[11,90], Rebin=4, doNormalization=False
                  )
discr = plotInfo(name="discr", title="Discriminant of all jets", legend="KEY-jets", Xlabel="Discriminant", Ylabel="abitrary units",
                 logY=True, grid=False,
                 binning=None, Rebin=None, doNormalization=False
                 )
effVsDiscrCut_discr = plotInfo(name="effVsDiscrCut_discr", title="Efficiency versus discriminant cut for all jets", legend="KEY-jets", Xlabel="Discriminant", Ylabel="efficiency", logY=True, grid=False, legPos=[0.2,0.2,0.3,0.3] )
#MC only
FlavEffVsBEff_discr = plotInfo(name="FlavEffVsBEff_B_discr", title="b-tag efficiency versus non b-tag efficiency", 
                               legend="KEY FLAV-jets versus b-jets", Xlabel="b-tag efficiency", Ylabel="non b-tag efficiency",
                               logY=True, grid=False, legPos=[0.2,0.8,0.3,0.9]
                               )
#MC only
#performance = plotInfo(name="effVsDiscrCut_discr", title="TAG-tag efficiency versus non TAG-tag efficiency", 
                       #legend="KEY-jets versus TAG-jets", Xlabel="TAG-tag efficiency", Ylabel="non TAG-tag efficiency",
                       #logY=True, grid=True, 
                       #doPerformance=True, tagFlavor="B", mistagFlavor=["C","DUSG", "PU", "NI"]
                       #)
##MC only, to do C vs B and C vs light
#performanceC = plotInfo(name="effVsDiscrCut_discr", title="TAG-tag efficiency versus non TAG-tag efficiency", 
                       #legend="KEY-jets versus TAG-jets", Xlabel="TAG-tag efficiency", Ylabel="non TAG-tag efficiency",
                       #logY=True, grid=True, 
                       #doPerformance=True, tagFlavor="C", mistagFlavor=["B","DUSG"]
                       #)
##by tracks
#IP = plotInfo(name="ip_3D", title="Impact parameter", legend="KEY-jets", Xlabel="IP [cm]", Ylabel="abitrary units",
              #logY=True, grid=False,
              #binning=None,Rebin=None, doNormalization=False,
              ##listTagger=["IPTag"]
              #)
#IPe = plotInfo(name="ipe_3D", title="Impact parameter error", legend="KEY-jets", Xlabel="IPE [cm]", Ylabel="abitrary units",
               #logY=True, grid=False, 
               #binning=None, Rebin=None, doNormalization=False,
               ##listTagger=["IPTag"]
               #)
#IPs = plotInfo(name="ips_3D", title="Impact parameter significance", legend="KEY-jets", Xlabel="IPS", Ylabel="abitrary units", 
               #logY=True, grid=False, 
               #binning=None, Rebin=None, doNormalization=False,
               ##listTagger=["IPTag"]
               #)
#NTracks = plotInfo(name="selTrksNbr_3D", title="number of selected tracks", legend="KEY-jets", Xlabel="number of selected tracks", Ylabel="abitrary units",
                   #logY=True, grid=False,
                   #binning=None, Rebin=None, doNormalization=False,
                   ##listTagger=["IPTag"]
                   #)
#distToJetAxis = plotInfo(name="jetDist_3D", title="track distance to the jet axis", legend="KEY-jets", Xlabel="distance to the jet axis [cm]", Ylabel="abitrary units",
                         #logY=True, grid=False,
                         #binning=None, Rebin=None, doNormalization=False, 
                         ##listTagger=["IPTag"]
                         #)
#decayLength = plotInfo(name="decLen_3D", title="track decay length", legend="KEY-jets", Xlabel="decay length [cm]", Ylabel="abitrary units",
                       #logY=True, grid=False,
                       #binning=None, Rebin=None, doNormalization=False, #listTagger=["IPTag"]
                       #)
#NHits = plotInfo(name="tkNHits_3D", title="Number of Hits / selected tracks", legend="KEY-jets", Xlabel="Number of Hits", Ylabel="abitrary units",
                 #logY=True, grid=False,
                 #binning=None, Rebin=None, doNormalization=False,
                 ##listTagger=["IPTag"]
                 #)
#NPixelHits = plotInfo(name="tkNPixelHits_3D", title="Number of Pixel Hits / selected tracks", legend="KEY-jets", Xlabel="Number of Pixel Hits", Ylabel="abitrary units",
                      #logY=True, grid=False, 
                      #binning=None, Rebin=None, doNormalization=False,
                      ##listTagger=["IPTag"]
                      #)
#NormChi2 = plotInfo(name="tkNChiSqr_3D", title="Normalized Chi2", legend="KEY-jets", Xlabel="Normilized Chi2", Ylabel="abitrary units",
                    #logY=True, grid=False,
                    #binning=None, Rebin=None, doNormalization=False,
                    ##listTagger=["IPTag"]
                    #)
#trackPt = plotInfo(name="tkPt_3D", title="track Pt", legend="KEY-jets", Xlabel="track Pt", Ylabel="abitrary units",
                   #logY=True, grid=False,
                   #binning=None, Rebin=None, doNormalization=False,
                   ##listTagger=["IPTag"]
                   #)
                   
                   
                   
# want to plot the following:
# * noCAT: FlavEffVsBEff_discr, discr, effVsDiscrCut_discr, jetEta, (jetFlavour), (jetMomentum), (jetPhi), jetPt, (jetMultiplicity), jetNSecondaryVertices, flightDistance2dSig, flightDistance2dVal, flightDistance3dSig, flightDistance3dVal
# * CAT0-3, ind 0-3: trackDecayLenVal, trackDeltaR, trackEtaRel, trackjetDist, trackMomentum, trackPPar, trackPParRatio, trackPtRatio, trackPtRel, trackSip2dSig, trackSip2dVal, trackSip3dSig, trackSip3dVal
# * CAT0-3, no ind:  (trackSip2dSigAboveCharm), (trackSip2dValAboveCharm), (trackSip3dSigAboveCharm), (trackSip3dValAboveCharm), trackSumJetDeltaR, trackSumJetEtRatio, vertexCategory
# * CAT0-2, no ind: vertexEnergyRatio, vertexJetDeltaR, vertexMass, vertexNTracks





#by SV and for CSV information
flightDist3Dval = plotInfo(name="flightDistance3dVal", title="3D flight distance value", legend="KEY-jets", Xlabel="3D flight distance value [cm]", Ylabel="abitrary units",
                           logY=True, grid=False,
                           binning=None, Rebin=None, doNormalization=False
                           #listTagger=["CSVTag"]
                           )
flightDist3Dsig = plotInfo(name="flightDistance3dSig", title="3D flight distance significance", legend="KEY-jets", Xlabel="3D flight distance significance", Ylabel="abitrary units",
                           logY=True, grid=False,
                           binning=None, Rebin=None, doNormalization=False
                           #listTagger=["CSVTag"]
                           )
flightDist2Dval = plotInfo(name="flightDistance2dVal", title="2D flight distance value", legend="KEY-jets", Xlabel="2D flight distance value [cm]", Ylabel="abitrary units",
                           logY=True, grid=False,
                           binning=None, Rebin=None, doNormalization=False
                           #listTagger=["CSVTag"]
                           )
flightDist2Dsig = plotInfo(name="flightDistance2dSig", title="2D flight distance significance", legend="KEY-jets", Xlabel="2D flight distance significance", Ylabel="abitrary units",
                           logY=True, grid=False,
                           binning=None, Rebin=None, doNormalization=False
                           #listTagger=["CSVTag"]
                           )
jetNSecondaryVertices = plotInfo(name="jetNSecondaryVertices", title="Number of SV / jet", legend="KEY-jets", Xlabel="Number of SV / jet", Ylabel="abitrary units",
                           logY=True, grid=False,
                           binning=None, Rebin=None, doNormalization=False
                           #listTagger=["CSVTag"]
                           )
vertexCategory = plotInfo(name="vertexCategory", title="Reco, Pseudo, No vertex", legend="KEY-jets", Xlabel="Reco, Pseudo, No vertex", Ylabel="abitrary units",
                          logY=True, grid=False,
                          binning=None, Rebin=None, doNormalization=False
                          #listTagger=["CSVTag"]
                          )
#Reco and pseudo vertex information
vertexMass = []
vertexNTracks = []
vertexJetDeltaR = []
vertexEnergyRatio = []

for cat in [""] : # , "_CAT1", "_CAT2"
	vertexMass.append(plotInfo(name="vertexMass"+cat, title="vertex mass"+cat.replace("_"," "), legend="KEY-jets", Xlabel="vertex mass GeV/c^2", Ylabel="abitrary units",
                      logY=True, grid=False,
                      binning=None, Rebin=None, doNormalization=False
                      #listTagger=["CSVTag"]
                      ))
	vertexNTracks.append(plotInfo(name="vertexNTracks"+cat, title="number of tracks at SV"+cat.replace("_"," "), legend="KEY-jets", Xlabel="number of tracks at SV", Ylabel="abitrary units",
                      logY=True, grid=False,
                      binning=None, Rebin=None, doNormalization=False
                      #listTagger=["CSVTag"]
                      ))
	vertexJetDeltaR.append(plotInfo(name="vertexJetDeltaR"+cat, title="Delta R between the SV and the jet axis"+cat.replace("_"," "), legend="KEY-jets", Xlabel="Delta R between the SV and the jet axis", Ylabel="abitrary units",
                      logY=True, grid=False,
                      binning=None, Rebin=None, doNormalization=False
                      #listTagger=["CSVTag"]
                      ))
	vertexEnergyRatio.append(plotInfo(name="vertexEnergyRatio"+cat, title="Energy Ratio between SV and the jet"+cat.replace("_"," "), legend="KEY-jets", Xlabel="Energy Ratio between SV and the jet", Ylabel="abitrary units",
                      logY=True, grid=False,
                      binning=None, Rebin=None, doNormalization=False
                      #listTagger=["CSVTag"]
                      ))
#Reco, pseudo and no vertex information

trackSumJetEtRatio = []
trackSumJetDeltaR = []

for cat in [""] : # , "_CAT1", "_CAT2", "_CAT3"
	trackSumJetEtRatio.append(plotInfo(name="trackSumJetEtRatio"+cat, title="track sum Et / jet energy"+cat.replace("_", " "), legend="KEY-jets", Xlabel="track sum Et / jet energy", Ylabel="abitrary units",
                              logY=True, grid=False,
                              binning=None, Rebin=None, doNormalization=False
                              #listTagger=["CSVTag"]
                              ))
	trackSumJetDeltaR.append(plotInfo(name="trackSumJetDeltaR"+cat, title="Delta R between track 4-vector sum and jet axis"+cat.replace("_"," "), legend="KEY-jets", Xlabel="Delta R between track 4-vector sum and jet axis", Ylabel="abitrary units", logY=True, grid=False, binning=None, Rebin=None, doNormalization=False
                             #listTagger=["CSVTag"]
                             ))

                             
                             
# * CAT0-3, ind 0-3: trackDecayLenVal, trackDeltaR, trackEtaRel, trackjetDist, trackMomentum, trackPPar, trackJetDist, trackPParRatio, trackPtRatio, trackPtRel, trackSip2dSig, trackSip2dVal, trackSip3dSig, trackSip3dVal
trackSip3dVal = []
trackSip3dSig = []
trackSip2dVal = []
trackSip2dSig = []
trackDeltaR = []
trackEtaRel = []
trackDecayLenVal = []
trackJetDist = []
trackPtRel = []
trackMomentum = []
trackPtRatio = []
trackPPar = []
trackPParRatio = []

for cat in [""] : # , "_CAT1", "_CAT2", "_CAT3"
	for i in [" ", "1"] : # , "1", "2", "3"
		trackSip3dVal.append(plotInfo(name="trackSip3dVal"+i.replace(" ","")+cat, title="track "+i+" IP 3D"+cat.replace("_", " "), legend="KEY-jets", Xlabel="track IP 3D [cm]", Ylabel="abitrary units",
                         logY=True, grid=False,
                         binning=None, Rebin=None, doNormalization=False, legPos=[0.2,0.8,0.3,0.9]
                         #listTagger=["CSVTag"]
                         ))
		trackSip3dSig.append(plotInfo(name="trackSip3dSig"+i.replace(" ","")+cat, title="track "+i+" IPS 3D"+cat.replace("_", " "), legend="KEY-jets", Xlabel="track IPS 3D", Ylabel="abitrary units",
                         logY=True, grid=False,
                         binning=None, Rebin=None, doNormalization=False, legPos=[0.2,0.8,0.3,0.9]
                         #listTagger=["CSVTag"]
                         ))
		trackSip2dVal.append(plotInfo(name="trackSip2dVal"+i.replace(" ","")+cat, title="track "+i+"IP 2D"+cat.replace("_", " "), legend="KEY-jets", Xlabel="track IP 2D [cm]", Ylabel="abitrary units",
                         logY=True, grid=False,
                         binning=None, Rebin=None, doNormalization=False, legPos=[0.2,0.8,0.3,0.9]
                         #listTagger=["CSVTag"]
                         ))
		trackSip2dSig.append(plotInfo(name="trackSip2dSig"+i.replace(" ","")+cat, title="track "+i+"IPS 2D"+cat.replace("_", " "), legend="KEY-jets", Xlabel="track IPS 2D", Ylabel="abitrary units",
                         logY=True, grid=False,
                         binning=None, Rebin=None, doNormalization=False, legPos=[0.2,0.8,0.3,0.9]
                         #listTagger=["CSVTag"]
                         ))
		trackDeltaR.append(plotInfo(name="trackDeltaR"+i.replace(" ","")+cat, title="Delta R between the track "+i+"and the jet axis"+cat.replace("_", " "), legend="KEY-jets", Xlabel="DeltaR(track,jet axis)", Ylabel="abitrary units",
                       logY=True, grid=False,
                       binning=None, Rebin=None, doNormalization=False
                       #listTagger=["CSVTag"]
                       ))
		trackEtaRel.append(plotInfo(name="trackEtaRel"+i.replace(" ","")+cat, title="track "+i+"eta relative to the jet axis"+cat.replace("_", " "), legend="KEY-jets", Xlabel="track eta relative to the jet axis", Ylabel="abitrary units",
                       logY=True, grid=False,
                       binning=None, Rebin=None, doNormalization=False
                       #listTagger=["CSVTag"]
                       ))
		trackDecayLenVal.append(plotInfo(name="trackDecayLenVal"+i.replace(" ","")+cat, title="track "+i+"decay length"+cat.replace("_", " "), legend="KEY-jets", Xlabel="track decay length", Ylabel="abitrary units",
                            logY=True, grid=False,
                            binning=None, Rebin=None, doNormalization=False
                            #listTagger=["CSVTag"]
                            ))
		trackJetDist.append(plotInfo(name="trackJetDist"+i.replace(" ","")+cat, title="track "+i+"distance to jet axis"+cat.replace("_", " "), legend="KEY-jets", Xlabel="track distance to jet axis", Ylabel="abitrary units",
                        logY=True, grid=False,
                        binning=None, Rebin=None, doNormalization=False
                        #listTagger=["CSVTag"]
                        ))
		trackPtRel.append(plotInfo(name="trackPtRel"+i.replace(" ","")+cat, title="track "+i+"Pt relative to jet axis"+cat.replace("_", " "), legend="KEY-jets", Xlabel="track Pt relative to jet axis", Ylabel="abitrary units",
                      logY=True, grid=False,
                      binning=None, Rebin=None, doNormalization=False
                      #listTagger=["CSVTag"]
                      ))
		trackPtRatio.append(plotInfo(name="trackPtRatio"+i.replace(" ","")+cat, title="track "+i+"Pt relative to jet axis, normalized to its energy"+cat.replace("_", " "), legend="KEY-jets", Xlabel="track Pt relative to jet axis, normalized to its energy", Ylabel="abitrary units",
                        logY=True, grid=False,
                        binning=None, Rebin=None, doNormalization=False
                        #listTagger=["CSVTag"]
                        ))
		trackMomentum.append(plotInfo(name="trackMomentum"+i.replace(" ","")+cat, title="track "+i+"momentum", legend="KEY-jets"+cat.replace("_", " "), Xlabel="track momentum [GeV/c]", Ylabel="abitrary units",
                         logY=True, grid=False,
                         binning=None, Rebin=None, doNormalization=False
                         #listTagger=["CSVTag"]
                         ))
		trackPPar.append(plotInfo(name="trackPPar"+i.replace(" ","")+cat, title="track "+i+"parallel momentum along the jet axis"+cat.replace("_", " "), legend="KEY-jets", Xlabel="track parallel momentum along the jet axis", Ylabel="abitrary units",
                     logY=True, grid=False,
                     binning=None, Rebin=None, doNormalization=False
                     #listTagger=["CSVTag"]
                     ))
		trackPParRatio.append(plotInfo(name="trackPParRatio"+i.replace(" ","")+cat, title="track "+i+"parallel momentum along the jet axis, normalized to its energy"+cat.replace("_", " "), legend="KEY-jets", Xlabel="track parallel momentum along the jet axis, normalized to its energy", Ylabel="abitrary units",
                          logY=True, grid=False,
                          binning=None, Rebin=None, doNormalization=False
                          #listTagger=["CSVTag"]
                          ))


#trackSip3dSigAboveCharm = plotInfo(name="trackSip3dSigAboveCharm", title="first track IPS 3D lifting SV mass above charm", legend="KEY-jets", Xlabel="first track IPS 3D lifting SV mass above charm", Ylabel="abitrary units",
                                   #logY=True, grid=False,
                                   #binning=None, Rebin=None, doNormalization=False
                                   ##listTagger=["CSVTag"]
                                   #)