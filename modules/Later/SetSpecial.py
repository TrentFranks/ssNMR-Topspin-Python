"""
Modules to Set default parameters:
W.T. Franks FMP Berlin
"""
import de.bruker.nmr.mfw.root as root
import de.bruker.nmr.prsc.toplib as top
#import os
import sys
from sys import argv
import TopCmds
import math

import IntShape
import PWR as pwr
import FREQ as fq
import GetNUCs as NUC

WAIT_TILL_DONE = 1;

#these are Carbon pulses, so we need to know which channel is the Carbon Channel
Nucs=NUC.list()
if Nucs[0]=='13C':
  CFrq=fq.O1()
elif Nucs[1]=='13C':
  CFrq=fq.O2()
elif Nucs[2]=='13C':
  CFrq=fq.O3()
elif Nucs[3]=='13C':
  CFrq=fq.O4()

def CalNCA():
  p90C=float(TopCmds.GETPAR("P 1"))
  ampC=float(TopCmds.GETPAR("PLdB 1"))
  p90N=float(TopCmds.GETPAR("P 21"))
  ampN=float(TopCmds.GETPAR("PLdB 21"))
  MAS =float(TopCmds.GETPAR("CNST 31"))
  SP=TopCmds.GETPAR("SPNAM 3")
  CNCT=float(TopCmds.GETPAR("P 16"))

  if CNCT <= 1.: CNCT = 3500.
  if SP == "gauss" or SP == "None" :
    #TopCmds.MSG("Please set spnam3")
    TopCmds.XCMD("spnam3")
    SP=(TopCmds.GETPAR2("SPNAM 3"))

  MaxB1N = 1000000./4./p90N
  MaxB1C = 1000000./4./p90C
  Coffs=Cfrq.ppm2offs(55.0)
  #find the channel with the lowest B1

  NCond=(5./2.)*MAS
  CCond=(3./2.)*MAS

  while NCond > MaxB1N :
    NCond=NCond - MAS
    CCond=NCond + MAS

  while CCond > MaxB1C :
    NCond=NCond - MAS
    CCond=NCond + MAS

  if NCond < MAS :
    NCond= 0.25*MAS
    CCond= 0.75*MAS
 
  index = TopCmds.INPUT_DIALOG("NCA off-resonance CP Input",\
   "N-CA SPECIFIC-CP w1C=3/2*wr; w1N=5/2*wr", \
  ["Carbon B1 field","Carbon offset (55ppm)","Nitrogen B1 field","Contact Time(P16)","Ramp Name"],\
  [str(CCond),str(Coffs),str(NCond),str(CNCT),SP],\
  ["Hz","Hz","Hz","us",""],\
  ["1","1","1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)
  
  NCond=(float(index[2]))*MAS
  CCond=math.sqrt( (float(index[0]))**2 - (float(index[1]))**2))
  
  adjust=20*(math.log10(CCond/MaxB1C))
  Camp = ampC-adjust
  adjust=20*(math.log10(NCond/MaxB1N))
  Namp = ampN-adjust
  #Insert ramp calibration here
  AvgAmp=IntShape.Integrate(SP)/100.
  adjust=20*(math.log10(1./AvgAmp))
  Camp = Camp-adjust
  CNCT = float(index[3])
  
  CampW=pwr.dBtoW(Camp)
  NampW=pwr.dBtoW(Namp)
  
  value = TopCmds.SELECT("Adjusting the NC CP parameters:",\
  "This will set\n 13C power to:  " + str('%3.2f' %CampW)+ " W\n \
  15N power to:  " +str('%3.2f' %NampW) + " W",["Update", "Keep Previous"]) 
  if value != 1:
    TopCmds.PUTPAR("PLdB 17",str('%3.2f' %Namp))
    TopCmds.PUTPAR("PLdB 16",str('%3.2f' %Camp))
    TopCmds.PUTPAR("P 16",str('%3.2f' %CNCT))
    TopCmds.PUTPAR("SPNAM 3",SP)
      
      
def CalNCO():
  p90C=float(TopCmds.GETPAR("P 1"))
  ampC=float(TopCmds.GETPAR("PLdB 1"))
  p90N=float(TopCmds.GETPAR("P 21"))
  ampN=float(TopCmds.GETPAR("PLdB 21"))
  MAS =float(TopCmds.GETPAR("CNST 31"))
  SP=TopCmds.GETPAR("SPNAM 3")
  CNCT=float(TopCmds.GETPAR("P 16"))

  if CNCT <= 1.: CNCT = 3500.
  if SP == "gauss" or SP == "None" :
    #TopCmds.MSG("Please set spnam3")
    TopCmds.XCMD("spnam3")
    SP=(TopCmds.GETPAR2("SPNAM 3"))

  MaxB1N = 1000000./4./p90N
  MaxB1C = 1000000./4./p90C
  Coffs=Cfrq.ppm2offs(170.0)

  NCond=(5./2.)*MAS
  CCond=(7./2.)*MAS

  while NCond > MaxB1N :
    NCond=NCond - MAS
    CCond=NCond + MAS

  while CCond > MaxB1C :
    NCond=NCond - MAS
    CCond=NCond + MAS

  if NCond < MAS :
    NCond= 0.25*MAS
    CCond= 0.75*MAS
 
  index = TopCmds.INPUT_DIALOG("NCO off-resonance CP Input",\
   "N-CO SPECIFIC-CP w1C=7/2*wr; w1N=5/2*wr", \
  ["Carbon B1 field","Carbon offset (170ppm)","Nitrogen B1 field","Contact Time(P16)","Ramp Name"],\
  [str(CCond),str(Coffs),str(NCond),str(CNCT),SP],\
  ["Hz","Hz","Hz","us",""],\
  ["1","1","1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)
  
  NCond=(float(index[2]))*MAS
  CCond=math.sqrt( (float(index[0]))**2 - (float(index[1]))**2))
  
  adjust=20*(math.log10(CCond/MaxB1C))
  Camp = ampC-adjust
  adjust=20*(math.log10(NCond/MaxB1N))
  Namp = ampN-adjust
  #Insert ramp calibration here
  AvgAmp=IntShape.Integrate(SP)/100.
  adjust=20*(math.log10(1./AvgAmp))
  Camp = Camp-adjust
  CNCT = float(index[3])
  
  CampW=pwr.dBtoW(Camp)
  NampW=pwr.dBtoW(Namp)
  
  value = TopCmds.SELECT("Adjusting the NC CP parameters:",\
  "This will set\n 13C power to:  " + str('%3.2f' %CampW)+ " W\n \
  15N power to:  " +str('%3.2f' %NampW) + " W",["Update", "Keep Previous"]) 
  if value != 1:
    TopCmds.PUTPAR("PLdB 17",str('%3.2f' %Namp))
    TopCmds.PUTPAR("PLdB 16",str('%3.2f' %Camp))
    TopCmds.PUTPAR("P 16",str('%3.2f' %CNCT))
    TopCmds.PUTPAR("SPNAM 3",SP)
      
      
