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
import CPDtools
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

def S6purge():
  p90C=float(TopCmds.GETPAR("P 1"))
  ampC=float(TopCmds.GETPAR("PLdB 1"))
  MAS =float(TopCmds.GETPAR("CNST 31"))
  
  MaxB1 = 1000000./4./p90C
  p90sC=float(TopCmds.GETPAR("P 6"))
  
  SPname=(TopCmds.GETPAR2("SPNAM 6"))
  if p90sC == 0: p90sC = 1500000./MAS
  SP=SPname

  #Check for existence and default
  if SP == "gauss" or SP == "None" :
    #TopCmds.MSG("Please set spnam6")
    TopCmds.XCMD("spnam6")
    SP=(TopCmds.GETPAR2("SPNAM 6"))
    
  offs = float(TopCmds.GETPAR("SPOFFS 6"))
  ppm=CFrq.offs2ppm(offs)

  if ppm > 140.0 : ppm=55.0
  if ppm < -10.0 : ppm=55.0

  index = TopCmds.INPUT_DIALOG("CA 90 purge", "S6 soft 90", \
  ["Duration","Offset","Pulse Name (3pi/2 Sinc)"],\
  [str('%3.2f' %p90sC),str('%3.2f' %ppm),SP],\
  ["us","ppm",""],\
  ["1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)
  
  p90sC=float(index[0])
  ppm=float(index[1])
  SP=index[2]
  offs=CFrq.ppm2offs(ppm)
  
  AvgAmp=IntShape.Integrate(SP)/100.
  adjust=20*math.log10(p90C/p90sC/AvgAmp)
  Power=ampC-adjust
  
  PowerW=pwr.dBtoW(Power)
  
  confirm = TopCmds.SELECT("Adjusting the S6 purge pulse:",\
  "This will set\n \
  13C amp (pl26) to :" + str('%3.2f' %PowerW)+ " W\n \
  Pulse offset to   :" + str('%8.0f' %offs) + " Hz\n \
  Equivalent to     :" + str('%3.1f' %ppm ) + " ppm\n \
  p6 to             :" + str('%6.1f' %p90sC)+ " us\n "\
  ,["Update", "Keep Previous"])
  
  if confirm != 1:
    TopCmds.PUTPAR("PLdB 26",str('%3.2f' %Power))
    TopCmds.PUTPAR("SPNAM 6",SP)
    TopCmds.PUTPAR("SPOFFS 6",str('%8.2f' %offs))
    TopCmds.PUTPAR("P 6",str('%3.2f' %p90sC))


def S7purge():
  p90C=float(TopCmds.GETPAR("P 1"))
  ampC=float(TopCmds.GETPAR("PLdB 1"))
  MAS =float(TopCmds.GETPAR("CNST 31"))
  
  MaxB1 = 1000000./4./p90C
  p90sC=float(TopCmds.GETPAR("P 7"))
  
  SPname=(TopCmds.GETPAR2("SPNAM 7"))
  if p90sC == 0: p90sC = 1500000./MAS
  SP=SPname

  #Check for existence and default
  if SP == "gauss" or SP == "None" :
    #TopCmds.MSG("Please set spnam7")
    TopCmds.XCMD("spnam7")
    SP=(TopCmds.GETPAR("SPNAM 7"))
      
  offs = float(TopCmds.GETPAR2("SPOFFS 7"))
  ppm=CFrq.offs2ppm(offs)

  if ppm < 140.0 : ppm=175.0
  if ppm > 220.0 : ppm=175.0

  index = TopCmds.INPUT_DIALOG("CO 90 purge", "S7 soft 90", \
  ["Duration","Offset","Pulse Name (3pi/2 Sinc)"],\
  [str('%3.2f' %p90sC),str('%3.2f' %ppm),SP],\
  ["us","ppm",""],\
  ["1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)
  
  p90sC=float(index[0])
  ppm=float(index[1])
  SP=index[2]
  offs=CFrq.ppm2offs(ppm)
  
  AvgAmp=IntShape.Integrate(SP)/100.
  adjust=20*math.log10(p90C/p90sC/AvgAmp)
  Power=ampC-adjust
  PowerW=pwr.dBtoW(Power)
  confirm = TopCmds.SELECT("Adjusting the S7 purge pulse:",\
  "This will set\n \
  13C amp (pl27) to :" + str('%3.2f' %PowerW)+ " W\n \
  Pulse offset to   :" + str('%8.0f' %offs) + " Hz\n \
  Equivalent to     :" + str('%3.1f' %ppm ) + " ppm\n \
  p7 to             :" + str('%6.1f' %p90sC)+ " us\n "\
  ,["Update", "Keep Previous"])
  
  if confirm != 1:  
    TopCmds.PUTPAR("PLdB 27",str('%3.2f' %Power))
    TopCmds.PUTPAR("SPNAM 7",SP)
    TopCmds.PUTPAR("SPOFFS 7",str('%8.2f' %offs))
    TopCmds.PUTPAR("P 7",str('%3.2f' %p90sC))

def S8refocus():
  p90C=float(TopCmds.GETPAR("P 1"))
  ampC=float(TopCmds.GETPAR("PLdB 1"))
  MAS =float(TopCmds.GETPAR("CNST 31"))
  
  MaxB1 = 1000000./4./p90C
  p180sC=float(TopCmds.GETPAR("P 8"))
  
  SPname=(TopCmds.GETPAR2("SPNAM 8"))
  if p180sC == 0: p180sC = 1500000./MAS
  SP=SPname

  #Check for existence and default
  if SP == "gauss" or SP == "None" :
    #TopCmds.MSG("Please set spnam8")
    TopCmds.XCMD("spnam8")
    SP=(TopCmds.GETPAR2("SPNAM 8"))
    
  offs = float(TopCmds.GETPAR("SPOFFS 8"))
  ppm=CFrq.offs2ppm(offs)
  
  if ppm > 140.0 : ppm=55.0
  if ppm < -10.0 : ppm=55.0

  index = TopCmds.INPUT_DIALOG("CA 180 refocus", "S8 soft 180", \
  ["Duration","Offset","Pulse Name (RSnob)"],\
  [str('%3.2f' %p180sC),str('%3.2f' %ppm),SP],\
  ["us","ppm",""],\
  ["1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)
  
  p180sC=float(index[0])
  ppm=float(index[1])
  SP=index[2]
  offs=CFrq.ppm2offs(ppm)
  
  AvgAmp=IntShape.Integrate(SP)/100.
  adjust=20*math.log10(2*p90C/p180sC/AvgAmp)
  Power=ampC-adjust
  PowerW=pwr.dBtoW(Power)
  confirm = TopCmds.SELECT("Adjusting the S8 refocus pulse:",\
  "This will set\n \
  13C amp (pl28) to :" + str('%3.2f' %PowerW)+ " W\n \
  Pulse offset to   :" + str('%8.0f' %offs) + " Hz\n \
  Equivalent to     :" + str('%3.1f' %ppm ) + " ppm\n \
  p8 to             :" + str('%6.1f' %p180sC)+ " us\n "\
  ,["Update", "Keep Previous"])

  if confirm != 1:  
    TopCmds.PUTPAR("PLdB 28",str('%3.2f' %Power))
    TopCmds.PUTPAR("SPNAM 8",SP)
    TopCmds.PUTPAR("SPOFFS 8",str('%8.2f' %offs))
    TopCmds.PUTPAR("P 8",str('%3.2f' %p180sC))

def S9refocus():
  p90C=float(TopCmds.GETPAR("P 1"))
  ampC=float(TopCmds.GETPAR("PLdB 1"))
  MAS =float(TopCmds.GETPAR("CNST 31"))
  
  MaxB1 = 1000000./4./p90C
  p180sC=float(TopCmds.GETPAR("P 9"))
  
  SPname=(TopCmds.GETPAR2("SPNAM 9"))
  if p180sC == 0: p180sC = 1500000./MAS
  SP=SPname

  #Check for existence and default
  if SP == "gauss" or SP == "None" :
    #TopCmds.MSG("Please set spnam9")
    TopCmds.XCMD("spnam9")
    SP=(TopCmds.GETPAR2("SPNAM 9"))
    
  offs = float(TopCmds.GETPAR("SPOFFS 9"))
  ppm=CFrq.offs2ppm(offs)
  if ppm < 140.0 : ppm=175.0
  if ppm > 220.0 : ppm=175.0

  index = TopCmds.INPUT_DIALOG("CO 180 refocus", "S9 soft 180", \
  ["Duration","Offset","Pulse Name (RSnob)"],\
  [str('%3.2f' %p180sC),str('%3.2f' %ppm),SP],\
  ["us","ppm",""],\
  ["1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)
  
  p180sC=float(index[0])
  ppm=float(index[1])
  SP=index[2]
  offs=CFrq.ppm2offs(ppm)
  
  AvgAmp=IntShape.Integrate(SP)/100.
  adjust=20*math.log10(2*p90C/p180sC/AvgAmp)
  Power=ampC-adjust
  PowerW=pwr.dBtoW(Power)
  confirm = TopCmds.SELECT("Adjusting the S9 refocus pulse:",\
  "This will set\n \
  13C amp (pl29) to :" + str('%3.2f' %PowerW)+ " W\n \
  Pulse offset to   :" + str('%8.0f' %offs) + " Hz\n \
  Equivalent to     :" + str('%3.1f' %ppm ) + " ppm\n \
  p9 to             :" + str('%6.1f' %p180sC)+ " us\n "\
  ,["Update", "Keep Previous"])
  
  if confirm != 1:  
    TopCmds.PUTPAR("PLdB 29",str('%3.2f' %Power))
    TopCmds.PUTPAR("SPNAM 9",SP)
    TopCmds.PUTPAR("SPOFFS 9",str('%8.2f' %offs))
    TopCmds.PUTPAR("P 9",str('%3.2f' %p180sC))


def CalS6purge():
  p90C=float(TopCmds.GETPAR("P 1"))
  ampC=float(TopCmds.GETPAR("PLdB 1"))
  
  MaxB1 = 1000000./4./p90C
  p90sC=float(TopCmds.GETPAR("P 6"))
  
  SPname=(TopCmds.GETPAR("SPNAM6"))
  if p90sC == 0: p90sC = 1500000./MAS
  SP=SPname
  if SP == "gauss" : SP = "3pi2SINC.wtf"
  offs = float(TopCmds.GETPAR("SPOFFS 6"))

  index = TopCmds.INPUT_DIALOG("OFF-resonance 90 purge", "S6 soft 90", \
  ["Duration","Offset","Pulse Name (3pi/2 Sinc)"],\
  [str(p90sC),str(offs),SP],\
  ["us","Hz",""],\
  ["1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)
  p90sC=float(index[0])
  offs=float(index[1])
  SP=index[2]
  
  #TopCmds.MSG(str(p90sC)+' p90sC')
  AvgAmp=IntShape.Integrate(SP)/100.
  adjust=20*math.log10(p90C/p90sC/AvgAmp)
  TopCmds.MSG(str(adjust)+'adjust')
  
  Power=ampC-adjust
  
  #TopCmds.MSG(str(Power))
  
  TopCmds.PUTPAR("PLdB 26",str('%3.2f' %Power))
  TopCmds.PUTPAR("SPNAM6",SP)
  TopCmds.PUTPAR("SPOFFS 6",str('%8.2f' %offs))
  TopCmds.PUTPAR("P 6",str('%3.2f' %p90sC))


def CalS7purge():
  p90C=float(TopCmds.GETPAR("P 1"))
  ampC=float(TopCmds.GETPAR("PLdB 1"))
  
  MaxB1 = 1000000./4./p90C
  p90sC=float(TopCmds.GETPAR("P 7"))
  
  SPname=(TopCmds.GETPAR("SPNAM7"))
  if p90sC == 0: p90sC = 1500000./MAS
  SP=SPname
  if SP == "gauss" : SP = "3pi2SINC.wtf"
  offs = float(TopCmds.GETPAR("SPOFFS 7"))

  index = TopCmds.INPUT_DIALOG("ON-resonance 90 purge", "S7 soft 90", \
  ["Duration","Offset","Pulse Name (3pi/2 Sinc)"],\
  [str(p90sC),str(offs),SP],\
  ["us","Hz",""],\
  ["1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)
  
  p90sC=float(index[0])
  offs=float(index[1])
  SP=index[2]
  
  AvgAmp=IntShape.Integrate(SP)/100.
  
  adjust=20*math.log10(p90C/p90sC/AvgAmp)
  Power=ampC-adjust
  
  TopCmds.PUTPAR("PLdB 27",str('%3.2f' %Power))
  TopCmds.PUTPAR("SPNAM7",SP)
  TopCmds.PUTPAR("SPOFFS 7",str('%8.2f' %offs))
  TopCmds.PUTPAR("P 7",str('%3.2f' %p90sC))     


def CalS8refocus():
  p90C=float(TopCmds.GETPAR("P 1"))
  ampC=float(TopCmds.GETPAR("PLdB 1"))
  
  MaxB1 = 1000000./4./p90C
  p180sC=float(TopCmds.GETPAR("P 8"))
  
  SPname=(TopCmds.GETPAR("SPNAM8"))
  if p180sC == 0: p180sC = 1500000./MAS
  SP=SPname
  if SP == "gauss" : SP = "RSnob"
  offs = float(TopCmds.GETPAR("SPOFFS 8"))

  index = TopCmds.INPUT_DIALOG("ON-resonance 180 Refocussing", "S8 soft 180", \
  ["Duration","Offset","Pulse Name (rSNOB)"],\
  [str(p180sC),str(offs),SP],\
  ["us","Hz",""],\
  ["1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)
  p180sC=float(index[0])
  offs=float(index[1])
  SP=index[2]
  
  #TopCmds.MSG(str(p90sC)+' p90sC')
  AvgAmp=IntShape.Integrate(SP)/100.
  adjust=20*math.log10(2*p90C/p180sC/AvgAmp)
  #TopCmds.MSG(str(adjust)+'adjust')
  
  Power=ampC-adjust
  
  #opCmds.MSG(str(Power))
  
  TopCmds.PUTPAR("PLdB 28",str('%3.2f' %Power))
  TopCmds.PUTPAR("SPNAM8",SP)
  TopCmds.PUTPAR("SPOFFS 8",str('%8.2f' %offs))
  TopCmds.PUTPAR("P 8",str('%3.2f' %p180sC))  
  
  
def CalS9refocus():
  p90C=float(TopCmds.GETPAR("P 1"))
  ampC=float(TopCmds.GETPAR("PLdB 1"))
  
  MaxB1 = 1000000./4./p90C
  p180sC=float(TopCmds.GETPAR("P 9"))
  
  SPname=(TopCmds.GETPAR("SPNAM9"))
  if p180sC == 0: p90sC = 1500000./MAS
  SP=SPname
  if SP == "gauss" : SP = "RSnob"
  offs = float(TopCmds.GETPAR("SPOFFS 9"))

  index = TopCmds.INPUT_DIALOG("OFF-resonance 180 Refocussing", "S9 soft 180", \
  ["Duration","Offset","Pulse Name (RSnob)"],\
  [str(p180sC),str(offs),SP],\
  ["us","Hz",""],\
  ["1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)
  p180sC=float(index[0])
  offs=float(index[1])
  SP=index[2]
  
  #TopCmds.MSG(str(p90sC)+' p90sC')
  AvgAmp=IntShape.Integrate(SP)/100.
  adjust=20*math.log10(2*p90C/p180sC/AvgAmp)
  #TopCmds.MSG(str(adjust)+'adjust')
  
  Power=ampC-adjust
  
  #TopCmds.MSG(str(Power))
  
  TopCmds.PUTPAR("PLdB 29",str('%3.2f' %Power))
  TopCmds.PUTPAR("SPNAM9",SP)
  TopCmds.PUTPAR("SPOFFS 9",str('%8.2f' %offs))
  TopCmds.PUTPAR("P 9",str('%3.2f' %p180sC))

