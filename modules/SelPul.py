"""
Modules to Set default parameters:
W.T. Franks FMP Berlin
"""
import de.bruker.nmr.mfw.root as root
import de.bruker.nmr.prsc.toplib as top
import os
import sys
from sys import argv
import TopCmds
import math

import IntShape
import Setup
import CPDtools
import FREQ as fq
import GetNUCs as NUC
from GetLib import pul
import FREQ as fq

ret=u"\u000D"
spc=u"\u0020"

WAIT_TILL_DONE = 1;

#Sort which channel is which
Nucs=NUC.list()
MaxDim=TopCmds.GETPROCDIM()
i=0
for item in Nucs:
  if i < MaxDim:
    if item =='13C':Cfrq=fq.fq(item,i+1)
    if item =='1H': Hfrq=fq.fq(item,i+1)
    if item =='15N':Nfrq=fq.fq(item,i+1)
    if item =='2H': Dfrq=fq.fq(item,i+1)
  i=i+1

def CAexc(units):
  MAS =pul.GetPar('MAS',"")
  
  Title="CA 90 excite/purge"
  Sutit=pul.pulDict['sCAe']+" soft 90"
  Label=["Duration","Offset","Pulse Name (3pi/2 Sinc)"]
  Dims =["us","ppm",""]
  Input=Title, Sutit,Label,Dims
  
  Confirm="Adjusting the "+pul.pulDict['sCAe']+" purge pulse:"
  
  Names  ='pCAe','aCAe','sCAe','oCAe'
  limits =140.,-10.  #(in ppm)
  default= 1.5*1000000./MAS,"ESnob",55.
  
  CalSP("13C",units,Names,default,limits,Input,Confirm,90.)

def COexc(units):
  MAS =pul.GetPar('MAS',"")
  
  Title="CO 90 excite/purge"
  Sutit=pul.pulDict['sCOe']+" soft 90"
  Label=["Duration","Offset","Pulse Name (3pi/2 Sinc)"]
  Dims =["us","ppm",""]
  Input=Title, Sutit,Label,Dims
  
  Confirm="Adjusting the "+pul.pulDict['sCOe']+" purge pulse:"
   
  Names  ='pCOe','aCOe','sCOe','oCOe'
  limits =220.,140.1  #(in ppm)
  default= 1.5*1000000./MAS,"ESnob",175.
  
  CalSP("13C",units,Names,default,limits,Input,Confirm,90.)

def CAref(units):
  MAS =pul.GetPar('MAS',"")
  
  Title="CA 180 refocussing"
  Sutit=pul.pulDict['sCAr']+" soft 180"
  Label=["Duration","Offset","Pulse Name (rSnob)"]
  Dims =["us","ppm",""]
  Input=Title, Sutit,Label,Dims
  
  Confirm="Adjusting the "+pul.pulDict['sCAr']+" purge pulse:"
  
  Names  ='pCAr','aCAr','sCAr','oCAr'
  limits =140.,-10.  #(in ppm)
  default= 1.5*1000000./MAS,"RSnob",55.
  
  #TopCmds.MSG("Calling Softpulse calculation")
  CalSP("13C",units,Names,default,limits,Input,Confirm,180.)

def COref(units):
  MAS =pul.GetPar('MAS',"")
  
  Title="CO 180 refocussing"
  Sutit=pul.pulDict['sCOr']+" soft 180"
  Label=["Duration","Offset","Pulse Name (rSnob)"]
  Dims =["us","ppm",""]
  Input=Title, Sutit,Label,Dims
  
  Confirm="Adjusting the "+pul.pulDict['sCOe']+" purge pulse:"
   
  Names  ='pCOr','aCOr','sCOr','oCOr'
  limits =220.,140.1  #(in ppm)
  default= 1.5*1000000./MAS,"RSnob",175.
  
  CalSP("13C",units,Names,default,limits,Input,Confirm,180.)

def S6purge(units):
  CAexc(units)
def S7purge(units):
  COexc(units)
def S8refocus(units):
  CAref(units)
def S9refocus(units):
  COref(units)

def CalSP(nuc,units,para,dflt,limits,dia,conf,tip):
  """
  nuc     : Nucleus, 13C or 1H
  units   : Watts (W) or Decibels (dB)
  para    : Dict keys for soft pulse wave (time,amp,shape,offs)
  dflt    : Defaults (time,shape,offs(in ppm))
  limits  : ppm frequency limits (upper, lower)
  """
	
  if nuc=="13C":p90=pul.GetPar('pC90',""); amp=pul.GetPar('aC',units)
  if nuc=="1H": p90=pul.GetPar('pH90',""); amp=pul.GetPar('aH',units)
  MAS =pul.GetPar('MAS',"")
  
  if units == "W":
    amp=Setup.WtodB(amp)  

  MaxB1 = 1000000./4./p90
  pSft  = pul.GetPar(para[0],"")
  if pSft == 0: pSft = dflt[0]
  SP=pul.GetPar(para[2],"")
  offs0 = pul.GetPar(para[3],"")
  
  #Check for existence and default
  if SP == "gauss" or SP == "None" or SP == "0"  or SP == "" :
    pul.SetPar(para[2],dflt[1],"")
    TopCmds.XCMD(pul.xcmd_name(pul.pulDict[para[2]]))
    SP=pul.GetPar(para[2],"")
  
  if pul.pulDict['uoffs']=='ppm':
    ppm=offs0
    offs=Cfrq.ppm2offs(offs0)
  else:
    #offs0 is in Hz
    ppm=Cfrq.offs2ppm(offs0)
    offs=offs0
  
  if ppm > limits[0] : ppm=dflt[2]
  if ppm < limits[1] : ppm=dflt[2]

  index = TopCmds.INPUT_DIALOG(dia[0],dia[1],dia[2],\
  [str('%3.2f' %pSft),str('%3.2f' %ppm),SP],\
  dia[3],["1","1","1"],\
  ["Accept","Close"], [spc,ret], 10)

  if index == None:TopCmds.EXIT()

  pSft=float(index[0])
  ppm=float(index[1])
  SP=index[2]
  offs=Cfrq.ppm2offs(ppm)

  AvgAmp=IntShape.Integrate(SP)/100.
  adjust=20*math.log10((tip/90.)*p90/pSft/AvgAmp)
  Power =amp-adjust

  if units == "W":
    Power=Setup.dBtoW(Power)  

  confirm = TopCmds.SELECT(conf,\
  "This will set\n "+\
  nuc+" amp "+pul.pulDict[para[1]]+" to : " + str('%3.2f' %Power)+ " "+units+"\n \
  Pulse offset to   : " + str('%8.0f' %offs) + " Hz\n \
  Equivalent to     : " + str('%3.1f' %ppm ) + " ppm\n "+\
  pul.pulDict[para[0]]+" to     :" + str('%6.1f' %pSft)+ " us\n "\
  ,["Update", "Keep Previous"])
  
  if confirm != 1:
    pul.SetPar(para[0],pSft,"")
    pul.SetPar(para[1],Power,units)
    pul.SetPar(para[2],SP,"")

    if pul.pulDict['uoffs']=='ppm':
      pul.SetPar(para[3],ppm,"")
    elif pul.pulDict['uoffs']=='Hz':
      pul.SetPar(para[3],offs,"")
    else :
      pul.SetPar(para[3],ppm,"")
      
