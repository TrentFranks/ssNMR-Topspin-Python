"""
Modules to Set default parameters:
W.T. Franks FMP Berlin
"""

import de.bruker.nmr.mfw.root as root

import math
import os
import sys
import TopCmds
import IntShape
import CPDtools

p90H=2.5
ampH=4.0
p90C=3.0
ampC=0.0
p90N=5.0
ampN=-2.0
MAS =10000.0

def dBtoW(dB):
  
  watts=math.pow(10,-dB/10.)
  #TopCmds.MSG("watts " + str(watts))
  
  return watts

def WtodB(watts):
  
  dB=-10.*math.log10(watts)
  #TopCmds.MSG("dB " + str(dB))
  
  return dB


def PutPars(p90H,ampH,p90C,ampC,p90N,ampN,MAS):
  TopCmds.PUTPAR("P 3",str(p90H))
  TopCmds.PUTPAR("PLW 2",str(ampH))
  TopCmds.PUTPAR("P 1",str(p90C))
  TopCmds.PUTPAR("PLW 1",str(ampC))
  TopCmds.PUTPAR("P 21",str(p90N))
  TopCmds.PUTPAR("PLW 3",str(ampN))
  TopCmds.PUTPAR("CNST 31",str(MAS))
  TopCmds.PUTPAR("MASR",str(MAS))
  TopCmds.PUTPAR("P 4",str(2*p90H))
  TopCmds.PUTPAR("P 2",str(2*p90C))
  TopCmds.PUTPAR("P 22",str(2*p90N))	

def LoadFromData():
  p90H=float(TopCmds.GETPAR("P 3"))
  ampH=float(TopCmds.GETPAR("PLW 2"))
  p90C=float(TopCmds.GETPAR("P 1"))
  ampC=float(TopCmds.GETPAR("PLW 1"))
  p90N=float(TopCmds.GETPAR("P 21"))
  ampN=float(TopCmds.GETPAR("PLW 3"))
  MAS =float(TopCmds.GETPAR("CNST 31"))
  
  index = TopCmds.INPUT_DIALOG("Mr Setup Input", "Pulse Widths and Power", \
  ["1H 90 pw","1H ampl","13C 90 pw","13C ampl","15N 90 pw","15N ampl","MAS"],\
  [str('%.2f' %p90H),str('%.2f' %ampH),str('%.2f' %p90C),str('%.2f' %ampC),str('%.2f' %p90N),str('%.2f' %ampN),str('%.2f' %MAS)],\
  ["us","W","us","W","us","W"," Hz"],\
  ["1","1","1","1","1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)
  p90H=float(index[0])
  ampH=float(index[1])
  p90C=float(index[2])
  ampC=float(index[3])
  p90N=float(index[4])
  ampN=float(index[5])
  MAS =float(index[6])
  TauR= 1000000./MAS
  PutPars(p90H,ampH,p90C,ampC,p90N,ampN,MAS)

def LoadDefault():
  #
  # Should have an external file to read from, but for now, this will do.
  #
  #ReadPars(p90H,ampH,p90C,ampC,p90N,ampN,MAS)
  index = TopCmds.INPUT_DIALOG("Mr Setup Input", "Pulse Widths and Power", \
  ["1H 90 pw","1H ampl","13C 90 pw","13C ampl","15N 90 pw","15N ampl","MAS"],\
  ["2.5","100","3.0","200.0","5.0","500.0","10000"],\
  ["us","W","us","W","us","W"," Hz"],\
  ["1","1","1","1","1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)
  p90H=float(index[0])
  ampH=float(index[1])
  p90C=float(index[2])
  ampC=float(index[3])
  p90N=float(index[4])
  ampN=float(index[5])
  MAS =float(index[6])
  TauR= 1000000./MAS
  PutPars(p90H,ampH,p90C,ampC,p90N,ampN,MAS)

def CalHC():
  p90H=float(TopCmds.GETPAR("P 3"))
  ampH=float(TopCmds.GETPAR("PLdB 2"))
  p90C=float(TopCmds.GETPAR("P 1"))
  ampC=float(TopCmds.GETPAR("PLdB 1"))
  MAS =float(TopCmds.GETPAR("CNST 31"))
  CNCT=float(TopCmds.GETPAR("P 15"))
  SPH=TopCmds.GETPAR2("SPNAM 40")
  SPX=TopCmds.GETPAR2("SPNAM 41")

  if CNCT <= 1.: CNCT = 1000.

  if SPH == "gauss" or SPH == "None" or SPH == "":
    #TopCmds.MSG("Please set spnam40")
    TopCmds.PUTPAR("SPNAM 40","ramp.100")
    TopCmds.XCMD("spnam40")
    SPH=(TopCmds.GETPAR2("SPNAM 40"))
    SPH.join()

  if SPX == "gauss" or SPX == "None" or SPX == "":
    #TopCmds.MSG("Please set spnam10")
    TopCmds.PUTPAR("SPNAM 41","square.100")
    TopCmds.XCMD("spnam41")
    SPX=(TopCmds.GETPAR2("SPNAM 41"))
    SPX.join()

  MaxB1H = 1000000./4./p90H
  MaxB1C = 1000000./4./p90C

  #find the channel with the lowest B1
  if MaxB1C < MaxB1H :
    Ratio=int(math.floor(MaxB1C/MAS))
    #TopCmds.MSG(str(Ratio))
    CCond=(Ratio-0.5)*MAS
    HCond=(Ratio+0.5)*MAS

    if HCond > MaxB1H:
      Ratio=Ratio-1
      CCond=(Ratio-0.5)*MAS
      HCond=(Ratio+0.5)*MAS

    # If spinning very fast or using weak B1s
    if Ratio <= 1:
      CCond= .25*MAS
      HCond= .75*MAS

  if MaxB1C >= MaxB1H :
    Ratio=int(math.floor(MaxB1H/MAS))
    HCond=(Ratio-0.5)*MAS
    CCond=(Ratio+0.5)*MAS

    if CCond > MaxB1C:
      Ratio=Ratio-1
      HCond=(Ratio-0.5)*MAS
      CCond=(Ratio+0.5)*MAS

    # If spinning very fast or using weak B1s
    if Ratio <= 1:
      CCond= .75*MAS
      HCond= .25*MAS

  adjust=20*(math.log10(CCond/MaxB1C))
  Camp = ampC-adjust
  adjust=20*(math.log10(HCond/MaxB1H))
  Hamp = ampH-adjust

  index = TopCmds.INPUT_DIALOG("HC CP Input", "Proton Carbon Cross Polarization", \
  ["Proton B1 Field","H Ramp","Carbon B1 Field","C Ramp","Contact Time(P15)"],\
  [str(HCond),SPH,str(CCond),SPX,str(CNCT)],\
  ["kHz","","kHz","","us"],\
  ["1","1","1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)

  adjust=20*(math.log10(float(index[0])/MaxB1H))
  Hamp1 = ampH-adjust
  AvgAmp=IntShape.Integrate(index[1])/100.
  adjust=20*(math.log10(1./AvgAmp))
  Hamp = Hamp1-adjust

  adjust=20*(math.log10(float(index[2])/MaxB1C))
  Camp1 = ampC-adjust
  #Ramp integration adjustment
  AvgAmp=IntShape.Integrate(index[3])/100.
  adjust=20*(math.log10(1./AvgAmp))
  Camp = Camp1-adjust

  CNCT = float(index[4])

  Hwatts=dBtoW(Hamp)
  Cwatts=dBtoW(Camp)
  value = TopCmds.SELECT("Adjusting the HC CP parameters:",\
  "This will set\n 1H power to:  " + str('%3.2f' %Hwatts)+ " W\n \
  13C power to:  " +str('%3.2f' %Cwatts) + " W",["Update", "Keep Previous"])

  if value != 1:
    TopCmds.PUTPAR("SPdB 40",str('%3.2f' %Hamp))
    TopCmds.PUTPAR("SPdB 41",str('%3.2f' %Camp))
    TopCmds.PUTPAR("PLdB 40",str('%3.2f' %Hamp))
    TopCmds.PUTPAR("PLdB 41",str('%3.2f' %Camp))
    TopCmds.PUTPAR("P 15" ,str('%3.2f' %CNCT))
    TopCmds.PUTPAR("SPNAM 40",index[1])
    TopCmds.PUTPAR("SPNAM 41",index[3])

def CalHN():
  p90H=float(TopCmds.GETPAR("P 3"))
  ampH=float(TopCmds.GETPAR("PLdB 2"))
  p90N=float(TopCmds.GETPAR("P 21"))
  ampN=float(TopCmds.GETPAR("PLdB 3"))
  MAS =float(TopCmds.GETPAR("CNST 31"))
  CNCT=float(TopCmds.GETPAR("P 25"))
  SPH=TopCmds.GETPAR2("SPNAM 42")
  SPX=TopCmds.GETPAR2("SPNAM 43")

  if CNCT <= 1.: CNCT = 1000.

  if SPH == "gauss" or SPH == "None" or SPH == "":
    #TopCmds.MSG("Please set spnam1")
    TopCmds.PUTPAR("SPNAM 42","ramp.100")
    TopCmds.XCMD("spnam42")
    SPH=(TopCmds.GETPAR2("SPNAM 42"))
    SPH.join()
    #TopCmds.MSG("Please set spnam0")

  if SPX == "gauss" or SPX == "None" or SPX == "":
    #TopCmds.MSG("Please set spnam11")
    TopCmds.PUTPAR("SPNAM 43","square.100")
    TopCmds.XCMD("spnam43")
    SPX=(TopCmds.GETPAR2("SPNAM 43"))
    SPX.join()

  MaxB1H = 1000000./4./p90H
  MaxB1N = 1000000./4./p90N

  #find the channel with the lowest B1
  if MaxB1N < MaxB1H :
    Ratio=int(math.floor(MaxB1N/MAS))
    NCond=(Ratio-0.5)*MAS
    HCond=(Ratio+0.5)*MAS

    if HCond > MaxB1H:
      Ratio=Ratio-1
      NCond=(Ratio-0.5)*MAS
      HCond=(Ratio+0.5)*MAS

    # If spinning very fast or using weak B1s
    if Ratio <= 1:
      NCond= .25*MAS
      HCond= .75*MAS

  if MaxB1N >= MaxB1H :
    Ratio=int(math.floor(MaxB1H/MAS))
    HCond=(Ratio-0.5)*MAS
    NCond=(Ratio+0.5)*MAS
    
    if NCond > MaxB1N:
      Ratio=Ratio-1 
      HCond=(Ratio-0.5)*MAS
      NCond=(Ratio+0.5)*MAS

    # If spinning very fast or using weak B1s
    if Ratio <= 1:
      NCond= .25*MAS
      HCond= .75*MAS

  adjust=20*(math.log10(NCond/MaxB1N))
  Namp = ampN-adjust
  adjust=20*(math.log10(HCond/MaxB1H))
  Hamp = ampH-adjust
  
  index = TopCmds.INPUT_DIALOG("HN CP Input", "Proton Nitrogen Cross Polarization", \
  ["Proton B1 Field","H Ramp","Nitrogen B1 Field","N Ramp","Contact Time(P25)"],\
  [str(HCond),SPH,str(NCond),SPX,str(CNCT)],\
  ["kHz","","kHz","","us"],\
  ["1","1","1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)
  
  adjust=20*(math.log10(float(index[0])/MaxB1H))
  Hamp1 = ampH-adjust
  AvgAmp=IntShape.Integrate(index[1])/100.
  adjust=20*(math.log10(1./AvgAmp))
  Hamp = Hamp1-adjust
  
  adjust=20*(math.log10(float(index[2])/MaxB1N))
  Namp = ampN-adjust
  #Ramp integration adjustment
  AvgAmp=IntShape.Integrate(index[3])/100.
  adjust=20*(math.log10(1./AvgAmp))
  Namp = Namp-adjust
  
  CNCT = float(index[4])

  #TopCmds.MSG("Adjusting the HC CP parameters:\n Your Proton Amplitude is set to " + str('%3.2f' %Hamp)+ "dB\n Your Nitrogen Ammplitude is set to " +str('%3.2f' %Namp))
    
  Hwatts=dBtoW(Hamp)
  Nwatts=dBtoW(Namp)

  value = TopCmds.SELECT("Adjusting the HN CP parameters:",\
  "This will set\n 1H power to:  " + str('%3.2f' %Hwatts)+ " W\n \
  15N power to:  " +str('%3.2f' %Nwatts) + " W",["Update", "Keep Previous"])
  
  if value != 1:
    TopCmds.PUTPAR("SPdB 42",str('%3.2f' %Hamp))
    TopCmds.PUTPAR("SPdB 43",str('%3.2f' %Namp))
    TopCmds.PUTPAR("PLdB 42",str('%3.2f' %Hamp))
    TopCmds.PUTPAR("PLdB 43",str('%3.2f' %Namp))
    TopCmds.PUTPAR("P 25" ,str('%.2f' %CNCT))
    TopCmds.PUTPAR("SPNAM 42",index[1])
    TopCmds.PUTPAR("SPNAM 43",index[3])
 
def CalNCA():
  p90C=float(TopCmds.GETPAR("P 1"))
  ampC=float(TopCmds.GETPAR("PLdB 1"))
  p90N=float(TopCmds.GETPAR("P 21"))
  ampN=float(TopCmds.GETPAR("PLdB 3"))
  MAS =float(TopCmds.GETPAR("CNST 31"))
  SP=TopCmds.GETPAR2("SPNAM 50")
  CNCT=float(TopCmds.GETPAR("P 16"))

  if CNCT <= 1.: CNCT = 3500.
  if SP == "gauss" or SP == "None" or SP == "" :
    #TopCmds.MSG("Please set spnam50")
    TopCmds.XCMD("spnam50")
    SP=(TopCmds.GETPAR2("SPNAM 50"))
    SP.join()

  MaxB1N = 1000000./4./p90N
  MaxB1C = 1000000./4./p90C
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
 
  index = TopCmds.INPUT_DIALOG("NCA CP Input", "N-CA SPECIFIC-CP 3/2*C; 5/2*N", \
  ["Carbon B1 field","Nitrogen B1 field","Contact Time(P16)","Ramp Name"],\
  [str(CCond),str(NCond),str(CNCT),SP],\
  ["kHz","kHz","us",""],\
  ["1","1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)  
  
  adjust=20*(math.log10(float(index[0])/MaxB1C))
  Camp = ampC-adjust
  adjust=20*(math.log10(float(index[1])/MaxB1N))
  Namp = ampN-adjust
  #Insert ramp calibration here
  AvgAmp=IntShape.Integrate(SP)/100.
  adjust=20*(math.log10(1./AvgAmp))
  Camp = Camp-adjust
  CNCT = float(index[2])
  
  Nwatts=dBtoW(Namp)
  Cwatts=dBtoW(Camp)

  value = TopCmds.SELECT("Adjusting the NC CP parameters:",\
  "This will set\n 13C power to:  " + str('%3.2f' %Cwatts)+ " W\n \
  15N power to:  " +str('%3.2f' %Nwatts) + " W",["Update", "Keep Previous"])
  
  if value != 1:
    TopCmds.PUTPAR("PLdB 5",str('%3.2f' %Namp))
    TopCmds.PUTPAR("PLdB 50",str('%3.2f' %Camp))
    TopCmds.PUTPAR("SPdB 50",str('%3.2f' %Camp))
    TopCmds.PUTPAR("P 16",str('%3.2f' %CNCT))
    TopCmds.PUTPAR("SPNAM 50",SP)

def CalNCO():
  p90C=float(TopCmds.GETPAR("P 1"))
  ampC=float(TopCmds.GETPAR("PLdB 1"))
  p90N=float(TopCmds.GETPAR("P 21"))
  ampN=float(TopCmds.GETPAR("PLdB 3"))
  MAS =float(TopCmds.GETPAR("CNST 31"))
  SP=TopCmds.GETPAR2("SPNAM 51")
  CNCT=float(TopCmds.GETPAR("P 17"))

  if CNCT <= 1.: CNCT = 3500.
  if SP == "gauss" or SP == "None" or SP == "":
    #TopCmds.MSG("Please set spnam2")
    TopCmds.XCMD("spnam51")
    SP=(TopCmds.GETPAR2("SPNAM 51"))
    SP.join()

  MaxB1N = 1000000./4./p90N
  MaxB1C = 1000000./4./p90C
  #find the channel with the lowest B1
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
 
  index = TopCmds.INPUT_DIALOG("NCO CP Input", "N-CO  SPECIFIC 7/2*C; 5/2*N", \
  ["Carbon B1 field","Nitrogen B1 field","Contact Time(P17)","Ramp Name"],\
  [str(CCond),str(NCond),str(CNCT),SP],\
  ["kHz","kHz","us",""],\
  ["1","1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)  
  
  adjust=20*(math.log10(float(index[0])/MaxB1C))
  Camp = ampC-adjust
  adjust=20*(math.log10(float(index[1])/MaxB1N))
  Namp = ampN-adjust
  #Insert ramp calibration here
  AvgAmp=IntShape.Integrate(SP)/100.
  adjust=20*(math.log10(1./AvgAmp))
  Camp = Camp-adjust
  CNCT = float(index[2])

  Nwatts=dBtoW(Namp)
  Cwatts=dBtoW(Camp)

  value = TopCmds.SELECT("Adjusting the NC CP parameters:",\
  "This will set\n 13C power to:  " + str('%3.2f' %Cwatts)+ " W\n \
  15N power to:  " +str('%3.2f' %Nwatts) + " W",["Update", "Keep Previous"])
    
  if value != 1:
    TopCmds.PUTPAR("PLdB 6",str('%3.2f' %Namp))
    TopCmds.PUTPAR("PLdB 51",str('%3.2f' %Camp))
    TopCmds.PUTPAR("SPdB 51",str('%3.2f' %Camp))
    TopCmds.PUTPAR("P 17",str('%3.2f' %CNCT))
    TopCmds.PUTPAR("SPNAM 51",SP)

def Find_PWdec(Text):
   while i < len(Text):
    about=''
    if Text[i].find("pcpd") >= 0: type="PCPD"
    elif Text[i].find("p31") >= 0: type="P 31"
    elif Text[i].find("p63") >= 0: type="P 63"
    elif Text[i].find("p62") >= 0: type="P 62"
    else :
      TopCmds.MSG("File for Decoupling not found; Exiting")
      TopCmds.EXIT()

def HDec():

  Stuff = []
  p90H=float(TopCmds.GETPAR("P 3"))
  ampH=float(TopCmds.GETPAR("PLdB 2"))
  MaxB1H = 1000000./4./p90H

  CPD=TopCmds.GETPAR2("CPDPRG 2")
  if CPD == "mlev" or CPD == "None" :
    TopCmds.XCMD("cpdprg2")
    CPD=(TopCmds.GETPAR2("CPDPRG 2"))

  #TopCmds.MSG(str(CPD))
  Stuff=CPDtools.CPDparse(CPD,"1H")
  TopCmds.MSG(str(Stuff))
  amp0=CPDtools.Find_old_pl(Stuff[0])
  decpw0=CPDtools.Find_old_pw(Stuff[1],"1H")

  B1_0=MaxB1H*(math.pow(10,(ampH-amp0)/20.))/1000.
  if B1_0 > 1.: B1out='% .1f' % B1_0
  if B1_0 <= 1.: B1out='75.0'

  index = TopCmds.INPUT_DIALOG("Mr Setup Input", "Decoupling Window", \
  ["Desired 1H Decoupling Amplitude","File"],\
  [B1out,CPD],["kHz",""],["1","1",],\
  ["Accept","Close"], ['a','c'], 10)

  TopCmds.PUTPAR("CPDPRG 2",index[1])

  #print(index[0], MaxB1H)
  adjust=20*(math.log10(1000.*float(index[0])/MaxB1H))
  Hamp = ampH-adjust
  decpwH= (MaxB1H/1000./float(index[0]))*(170./180.)*2*p90H

  wattsH=dBtoW(Hamp)

  value = TopCmds.SELECT("Adjusting the H decoupling parameters:",\
  "This will set\n 1H power ("+ Stuff[0] +") to:  "+ str('%.2f' %wattsH)+ " W\n \
  Pulse width ("+ Stuff[1] +") to:  " +str('%3.2f' %decpwH) + " us",["Update", "Keep Previous"])

  if value != 1:

    if Stuff[0]=='pl12':
      TopCmds.PUTPAR("PLdB 12",str('%3.2f' %Hamp))
    elif Stuff[0]=='pl13':
      TopCmds.PUTPAR("PLdB 13",str('%3.2f' %Hamp))
    elif Stuff[0]=='pl14':
      TopCmds.PUTPAR("PLdB 14",str('%3.2f' %Hamp))

    if Stuff[1]=='pcpd':
      TopCmds.PUTPAR("PCPD 2",str('%3.2f' %decpwH))
    elif Stuff[1]=='p31':
      TopCmds.PUTPAR("P 31",str('%3.2f' %decpwH))
      TopCmds.PUTPAR("P 30",str('%3.2f' %decpwH))
    elif Stuff[1]=='p62':
      TopCmds.PUTPAR("P 61",str('%3.2f' %decpwH))
      TopCmds.PUTPAR("P 62",str('%3.2f' %decpwH))

def NDec():

  Stuff = []
  p90=float(TopCmds.GETPAR("P 21"))
  amp=float(TopCmds.GETPAR("PLdB 21"))
  MaxB1 = 1000000./4./p90

  CPD=TopCmds.GETPAR2("CPDPRG 3")
  if CPD == "mlev" or CPD == "None" :
    TopCmds.XCMD("cpdprg3")
    CPD=(TopCmds.GETPAR2("CPDPRG 3"))

  Stuff=CPDtools.CPDparse(CPD,"15N")
  amp0=CPDtools.Find_old_pl(Stuff[0])
  decpw0=CPDtools.Find_old_pw(Stuff[1],"15N")

  B1_0=MaxB1*(math.pow(10,(amp-amp0)/20.))/1000.
  if B1_0 > 1.: B1out='% .1f' % B1_0
  if B1_0 <= 1.: B1out='15.0'
  
  index = TopCmds.INPUT_DIALOG("Mr Setup Input", "Decoupling Window", \
  ["Desired 15N Decoupling Amplitude","File"],\
  [B1out,CPD],["kHz",""],["1","1",],\
  ["Accept","Close"], ['a','c'], 10)
  
  TopCmds.PUTPAR("CPDPRG 3",index[1])
  adjust=20*(math.log10(1000.*float(index[0])/MaxB1))
  ampli = amp-adjust
  decpw = (MaxB1/1000./float(index[0]))*2*p90

  Nwatts=dBtoW(Namp)
  
  value = TopCmds.SELECT("Adjusting the N decoupling parameters:",\
  "This will set\n 15N power ("+ Stuff[0] +") to:  "+ str('%3.2f' %Nwatts)+ " W\n \
  Pulse width ("+ Stuff[1] +"= 180deg) to:  " +str('%3.2f' %decpw) + " us",["Update", "Keep Previous"])

  if value != 1:

    if Stuff[0]=='':
      TopCmds.PUTPAR("PLdB 3",str('%3.2f' %ampli))
    elif Stuff[0]=='pl3':
      TopCmds.PUTPAR("PLdB 3",str('%3.2f' %ampli))
    elif Stuff[0]=='pl12':
      TopCmds.MSG("You are using pl12 for 15N decouling.  It is usually reserved for 1H \n Please verify")
      #TopCmds.PUTPAR("PLdB 12",str('%3.2f' %ampli))
    elif Stuff[0]=='pl13':
      TopCmds.MSG("You are using pl13 for 15N decouling.  It is usually reserved for 1H \n Please verify")
      #TopCmds.PUTPAR("PLdB 13",str('%3.2f' %ampli))
    elif Stuff[0]=='pl14':
      TopCmds.MSG("You are using pl14 for 15N decouling.  It is usually reserved for 1H \n Please verify")
      #TopCmds.PUTPAR("PLdB 14",str('%3.2f' %ampli))
    
    if Stuff[1]=='pcpd':
      TopCmds.PUTPAR("PCPD 3",str('%3.2f' %decpw))
    elif Stuff[1]=='p31':
      TopCmds.PUTPAR("P 31",str('%3.2f' %decpw))
      TopCmds.PUTPAR("P 30",str('%3.2f' %decpw))
    elif Stuff[1]=='p62':
      TopCmds.PUTPAR("P 61",str('%3.2f' %decpw))
      TopCmds.PUTPAR("P 62",str('%3.2f' %decpw))

def CDec():

  Stuff = []
  p90=float(TopCmds.GETPAR("P 1"))
  amp=float(TopCmds.GETPAR("PLdB 1"))
  MaxB1 = 1000000./4./p90

  CPD=TopCmds.GETPAR2("CPDPRG 1")
  if CPD == "mlev" or CPD == "None" :
    TopCmds.XCMD("cpdprg1")
    CPD=(TopCmds.GETPAR2("CPDPRG 1"))

  Stuff=CPDtools.CPDparse(CPD,"13C")
  TopCmds.MSG(str(Stuff))
  amp0=CPDtools.Find_old_pl(Stuff[0])
  decpw0=CPDtools.Find_old_pw(Stuff[1],"13C")

  B1_0=MaxB1*(math.pow(10,(amp-amp0)/20.))/1000.
  if B1_0 > 1.: B1out='% .1f' % B1_0
  if B1_0 <= 1.: B1out='5.0'
  
  index = TopCmds.INPUT_DIALOG("Mr Setup Input", "Decoupling Window", \
  ["Desired 13C Decoupling Amplitude","File"],\
  [B1out,CPD],["kHz",""],["1","1",],\
  ["Accept","Close"], ['a','c'], 10)
  
  TopCmds.PUTPAR("CPDPRG 1",index[1])
  adjust=20*(math.log10(1000.*float(index[0])/MaxB1))
  ampli = amp-adjust
  decpw = (MaxB1/1000./float(index[0]))*2*p90

  watts=dBtoW(ampli)
  
  value = TopCmds.SELECT("Adjusting the 13C decoupling parameters:",\
  "This will set\n 13C power ("+ Stuff[0] +") to:  "+ str('%3.2f' %watts)+ " W\n \
  Pulse width ("+ Stuff[1] +"= 180deg) to:  " +str('%3.2f' %decpw) + " us",["Update", "Keep Previous"])

  if value != 1:

    if Stuff[0]=='':
      TopCmds.PUTPAR("PLdB 4",str('%3.2f' %ampli))
    elif Stuff[0]=='pl4':
      TopCmds.PUTPAR("PLdB 4",str('%3.2f' %ampli))
    elif Stuff[0]=='pl12':
      TopCmds.MSG("You are using pl12 for 13C decouling.  It is usually reserved for 1H \n Please verify")
      #TopCmds.PUTPAR("PLdB 12",str('%3.2f' %ampli))
    elif Stuff[0]=='pl13':
      TopCmds.MSG("You are using pl13 for 13C decouling.  It is usually reserved for 1H \n Please verify")
      #TopCmds.PUTPAR("PLdB 13",str('%3.2f' %ampli))
    elif Stuff[0]=='pl14':
      TopCmds.MSG("You are using pl14 for 13C decouling.  It is usually reserved for 1H \n Please verify")
      #TopCmds.PUTPAR("PLdB 14",str('%3.2f' %ampli))
    
    if Stuff[1]=='pcpd':
      TopCmds.PUTPAR("PCPD 1",str('%3.2f' %decpw))
    elif Stuff[1]=='p31':
      TopCmds.PUTPAR("P 31",str('%3.2f' %decpw))
      TopCmds.PUTPAR("P 30",str('%3.2f' %decpw))
    elif Stuff[1]=='p62':
      TopCmds.PUTPAR("P 61",str('%3.2f' %decpw))
      TopCmds.PUTPAR("P 62",str('%3.2f' %decpw))
    elif Stuff[1]=='p60':
      TopCmds.PUTPAR("P 59",str('%3.2f' %decpw))
      TopCmds.PUTPAR("P 60",str('%3.2f' %decpw))
  
def DDec():

  Stuff = []
  p90=float(TopCmds.GETPAR("P 32"))
  amp=float(TopCmds.GETPAR("PLdB 31"))
  MaxB1 = 1000000./4./p90

  CPD=TopCmds.GETPAR2("CPDPRG 5")
  if CPD == "mlev" or CPD == "None" :
    TopCmds.XCMD("cpdprg5")
    CPD=(TopCmds.GETPAR2("CPDPRG 5"))

  Stuff=CPDtools.CPDparse(CPD,"2D")
  TopCmds.MSG(str(Stuff))
  amp0=CPDtools.Find_old_pl(Stuff[0])
  decpw0=CPDtools.Find_old_pw(Stuff[1],"2D")

  B1_0=MaxB1*(math.pow(10,(amp-amp0)/20.))/1000.
  if B1_0 > 1.: B1out='% .1f' % B1_0
  if B1_0 <= 1.: B1out='5.0'
  
  index = TopCmds.INPUT_DIALOG("Mr Setup Input", "Decoupling Window", \
  ["Desired 2H Decoupling Amplitude","File"],\
  [B1out,CPD],["kHz",""],["1","1",],\
  ["Accept","Close"], ['a','c'], 10)
  
  TopCmds.PUTPAR("CPDPRG 5",index[1])
  adjust=20*(math.log10(1000.*float(index[0])/MaxB1))
  ampli = amp-adjust
  decpw = (MaxB1/1000./float(index[0]))*2*p90

  watts=dBtoW(ampli)
  
  value = TopCmds.SELECT("Adjusting the D decoupling parameters:",\
  "This will set\n 2H power ("+ Stuff[0] +") to:  "+ str('%3.2f' %watts)+ " W\n \
  Pulse width ("+ Stuff[1] +"= 180deg) to:  " +str('%3.2f' %decpw) + " us",["Update", "Keep Previous"])

  if value != 1:

    if Stuff[0]=='':
      TopCmds.PUTPAR("PLdB 25",str('%3.2f' %ampli))
    elif Stuff[0]=='pl3':
      TopCmds.PUTPAR("PLdB 25",str('%3.2f' %ampli))
    elif Stuff[0]=='pl12':
      TopCmds.MSG("You are using pl12 for 2H decouling.  It is usually reserved for 1H \n Please verify")
      #TopCmds.PUTPAR("PLdB 12",str('%3.2f' %ampli))
    elif Stuff[0]=='pl13':
      TopCmds.MSG("You are using pl13 for 2H decouling.  It is usually reserved for 1H \n Please verify")
      #TopCmds.PUTPAR("PLdB 13",str('%3.2f' %ampli))
    elif Stuff[0]=='pl14':
      TopCmds.MSG("You are using pl14 for 2H decouling.  It is usually reserved for 1H \n Please verify")
      #TopCmds.PUTPAR("PLdB 14",str('%3.2f' %ampli))
    
    if Stuff[1]=='pcpd':
      TopCmds.PUTPAR("PCPD 5",str('%3.2f' %decpw))
    elif Stuff[1]=='p31':
      TopCmds.PUTPAR("P 31",str('%3.2f' %decpw))
      TopCmds.PUTPAR("P 30",str('%3.2f' %decpw))
    elif Stuff[1]=='p62':
      TopCmds.PUTPAR("P 61",str('%3.2f' %decpw))
      TopCmds.PUTPAR("P 62",str('%3.2f' %decpw))
  
def CalC72():
   p90C=float(TopCmds.GETPAR("P 1"))
   ampC=float(TopCmds.GETPAR("PLdB 1"))
   MaxB1 = 1000000./4./p90C
   C7B1  = 7.0*MAS
   adjust=20*(math.log10(C7B1/MaxB1))
   Condition=ampC-adjust
   TopCmds.PUTPAR("PLdB 17",str('%3.2f' %Condition))
   TopCmds.PUTPAR("L 7",str(14))

def CalSPC5_2():
   p90C=float(TopCmds.GETPAR("P 1"))
   ampC=float(TopCmds.GETPAR("PLdB 1"))
   MaxB1 = 1000000./4./p90C
   C5B1  = 5.0*MAS
   adjust=20*(math.log10(C5B1/MaxB1))
   condition=ampC-adjust
   TopCmds.PUTPAR("PLdB 15",str('%3.2f' %condition))
   TopCmds.PUTPAR("L 5",str(10))

def CalSPC5_3():
  p90C=float(TopCmds.GETPAR("P 1"))
  ampC=float(TopCmds.GETPAR("PLdB 1"))
  MaxB1 = 1000000./4./p90C
  C5B1  = 10.0*MAS/3.0
  adjust=20*(math.log10(C5B1/MaxB1))
  condition=ampC-adjust
  TopCmds.PUTPAR("PLdB 15",str('%3.2f' %condition))
  TopCmds.PUTPAR("L 5",str(10))

  


