"""
Modules to Set default parameters:
W.T. Franks FMP Berlin
"""

import de.bruker.nmr.mfw.root as root
import sys
sys.path.append(root.UtilPath.getTopspinHome()+ '/exp/stan/nmr/py/BioPY/modules/')

import math
import TopCmds
import IntShape
import CPDtools
from GetLib import pul

def dBtoW(dB):
  
  watts=math.pow(10,-dB/10.)
  #TopCmds.MSG("watts " + str(watts))
  
  return watts

def WtodB(watts):
  
  if watts>0.0:
    dB=-10.*math.log10(watts)
  else:
    dB=1000.
  #TopCmds.MSG("dB " + str(dB))
  
  return dB


def PutPars(p90H,ampH,p90C,ampC,p90N,ampN,MAS,units):

  pul.SetPar('pH90',p90H,"")
  pul.SetPar('pC90',p90C,"")
  pul.SetPar('pN90',p90N,"")
  pul.SetPar('pH180',2*p90H,"")
  pul.SetPar('pC180',2*p90C,"")
  pul.SetPar('pN180',2*p90N,"")
  pul.SetPar('aH',ampH,units)
  pul.SetPar('aC',ampC,units)
  pul.SetPar('aN',ampN,units)
  pul.SetPar('MAS',MAS,"")
  
def LoadFromData(units):

  p90H=pul.GetPar('pH90',"")
  p90C=pul.GetPar('pC90',"")
  p90N=pul.GetPar('pN90',"")
  ampH=pul.GetPar('aH',units)
  ampC=pul.GetPar('aC',units)
  ampN=pul.GetPar('aN',units)
  MAS =pul.GetPar('MAS',"")

  index = TopCmds.INPUT_DIALOG("Mr Setup Input", "Pulse Widths and Power", \
  ["1H 90 pw","1H ampl","13C 90 pw","13C ampl","15N 90 pw","15N ampl","MAS"],\
  [str('%.2f' %p90H),str('%.2f' %ampH),str('%.2f' %p90C),str('%.2f' %ampC),str('%.2f' %p90N),str('%.2f' %ampN),str('%.2f' %MAS)],\
  ["us",units,"us",units,"us",units," Hz"],\
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
  PutPars(p90H,ampH,p90C,ampC,p90N,ampN,MAS,units)

def LoadDefault(units):
  #
  # Should have an external file to read from, but for now, this will do.
  #
  #ReadPars(p90H,ampH,p90C,ampC,p90N,ampN,MAS)
  
  #XCMD('rpar')
  index = TopCmds.INPUT_DIALOG("Mr Setup Input", "Pulse Widths and Power", \
  ["1H 90 pw","1H ampl","13C 90 pw","13C ampl","15N 90 pw","15N ampl","MAS"],\
  ["2.5","100","3.0","200.0","5.0","500.0","10000"],\
  ["us",units,"us",units,"us",units," Hz"],\
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
  PutPars(p90H,ampH,p90C,ampC,p90N,ampN,MAS,units)

def HC_neu(units):

  Title="HC CP Input"
  SuTit="Proton Carbon Cross Polarization"
  Label=["Proton B1 Field","H Ramp","Carbon B1 Field","C Ramp","Contact Time(P15)"]

  In  =Title,SuTit,Label
  
  Title="Adjusting the HC CP parameters:"
  Label="1H","13C"
  
  Out =Title,Label

  CalCP('pH90','pC90','aHhc','aChc','empty','pHC','sHhc','sChc',"HX","Max",units,In,Out)
  
def HN_neu(units):

  Title="HN CP Input"
  SuTit="Proton Nitrogen Cross Polarization"
  Label=["Proton B1 Field","H Ramp","Nitrogen B1 Field","N Ramp","Contact Time(P25)"]

  In  =Title,SuTit,Label
  
  Title="Adjusting the HN CP parameters:"
  Label="1H","15N"
  
  Out =Title,Label

  CalCP('pH90','pN90','aHhn','aNhn','empty','pHN','sHhn','sNhn',"HX","Max",units,In,Out)
  
def NCA_neu(units):

  Title="NCA CP Input"
  SuTit="N-Ca SPECIFIC CP (3/2*C; 5/2*N)"
  Label=  ["CA B1 field","Carbon Ramp","N B1 field","Nitrogen Ramp","Contact Time","H B1 decoupler"]

  In  =Title,SuTit,Label
  
  Title="Adjusting the N-Ca CP parameters:"
  Label="13C","15N","1H"
  
  Out =Title,Label

  CalCP('pC90','pN90','aCnca','aNnca','aHnca','pNCA','sCnca','sNnca',"XY","Low",units,In,Out)

def NCO_neu(units):

  Title="NCO CP Input"
  SuTit="N-Co SPECIFIC CP (7/2*C; 5/2*N)"
  Label=  ["CA B1 field","Carbon Ramp","N B1 field","Nitrogen Ramp","Contact Time","H B1 decoupler"]

  In  =Title,SuTit,Label
  
  Title="Adjusting the N-Ca CP parameters:"
  Label="13C","15N","1H"
  
  Out =Title,Label

  CalCP('pC90','pN90','aCnco','aNnco','aHnco','pNCO','sCnco','sNnco',"XY","High",units,In,Out)
  
def HC(units):
  p90H=pul.GetPar('pH90',"")
  p90C=pul.GetPar('pC90',"")
  ampH=pul.GetPar('aH',units)
  ampC=pul.GetPar('aC',units)
  MAS =pul.GetPar('MAS',"")
  CNCT=pul.GetPar('pHC',"")
  SPH =pul.GetPar('sHhc',"")
  SPX =pul.GetPar('sChc',"")

  if units == "W":
    ampH=WtodB(ampH)
    ampC=WtodB(ampC)

  if CNCT <= 1.: CNCT = 1000.

  if SPH == "gauss" or SPH == "None" or SPH == "" or SPH == "0":
    pul.SetPar('sHhc',"ramp.100","")
    TopCmds.XCMD(pul.xcmd_name(pul.pulDict['sHhc']))
    SPH=pul.GetPar('sHhc',"")
      
  if SPX == "gauss" or SPX == "None" or SPX == "" or SPX == "0":
    pul.SetPar('sChc',"square.100","")
    TopCmds.XCMD(pul.xcmd_name(pul.pulDict['sChc']))
    SPX=pul.GetPar('sChc',"")

  MaxB1H = 1000000./4./p90H
  MaxB1C = 1000000./4./p90C

  #find the channel with the lowest B1
  if MaxB1C < MaxB1H :
    Ratio=int(math.floor(MaxB1C/MAS))
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
  [str(HCond),str(SPH),str(CCond),str(SPX),str(CNCT)],\
  ["Hz","","Hz","","us"],\
  ["1","1","1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)

  adjust=20*(math.log10(float(index[0])/MaxB1H))
  Hamp1 = ampH-adjust
  if SPH == "Unused":
    AvgAmp=1.
  else:
    AvgAmp=IntShape.Integrate(index[1])/100.
  adjust=20*(math.log10(1./AvgAmp))
  Hamp = Hamp1-adjust

  adjust=20*(math.log10(float(index[2])/MaxB1C))
  Camp1 = ampC-adjust
  if SPX == "Unused":
    AvgAmp=1.
  else:
    AvgAmp=IntShape.Integrate(index[3])/100.
  adjust=20*(math.log10(1./AvgAmp))
  Camp = Camp1-adjust

  CNCT = float(index[4])
  
  if units == "W":
    Hamp=dBtoW(Hamp)
    Camp=dBtoW(Camp)

  value = TopCmds.SELECT("Adjusting the HC CP parameters:",\
  "This will set\n 1H power to:  " + str('%3.2f' %Hamp)+" "+ units+"\n \
  13C power to:  " +str('%3.2f' %Camp) + " "+units,["Update", "Keep Previous"])
  
  if value != 1:
    pul.SetPar('aHhc',Hamp,units)
    pul.SetPar('aChc',Camp,units)
    pul.SetPar('pHC',CNCT,"")
    if SPH != "Unused":
      pul.SetPar('sHhc',index[1],"")
    if SPX != "Unused":
      pul.SetPar('sChc',index[3],"")
    
def HN(units):
  p90H=pul.GetPar('pH90',"")
  p90N=pul.GetPar('pN90',"")
  ampH=pul.GetPar('aH',units)
  ampN=pul.GetPar('aN',units)
  MAS =pul.GetPar('MAS',"")
  CNCT=pul.GetPar('pHN',"")
  SPH =pul.GetPar('sHhn',"")
  SPX =pul.GetPar('sNhn',"")

  if units == "W":
    ampH=WtodB(ampH)
    ampN=WtodB(ampN)
 
  if CNCT <= 1.: CNCT = 1000.

  if SPH == "gauss" or SPH == "None" or SPH == "" or SPH == "0":
    pul.SetPar('sHhn',"ramp.100","")
    TopCmds.XCMD(pul.xcmd_name(pul.pulDict['sHhn']))
    SPH=pul.GetPar('sHhn',"")

  if SPX == "gauss" or SPX == "None" or SPX == "" or SPX == "0":
    pul.SetPar('sNhn',"square.100","")
    TopCmds.XCMD(pul.xcmd_name(pul.pulDict['sNhn']))
    SPX = pul.GetPar('sNhn',"")

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
  ["Hz","","Hz","","us"],\
  ["1","1","1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)
  
  adjust=20*(math.log10(float(index[0])/MaxB1H))
  Hamp1 = ampH-adjust
  if SPH == "Unused":
    AvgAmp=1.
  else:
    AvgAmp=IntShape.Integrate(index[1])/100.
  adjust=20*(math.log10(1./AvgAmp))
  Hamp = Hamp1-adjust
  
  adjust=20*(math.log10(float(index[2])/MaxB1N))
  Namp = ampN-adjust
  if SPX == "Unused":
    AvgAmp=1.
  else:
    AvgAmp=IntShape.Integrate(index[3])/100.
  adjust=20*(math.log10(1./AvgAmp))
  Namp = Namp-adjust
  
  CNCT = float(index[4])

  #TopCmds.MSG("Adjusting the HC CP parameters:\n Your Proton Amplitude is set to " + str('%3.2f' %Hamp)+ "dB\n Your Nitrogen Ammplitude is set to " +str('%3.2f' %Namp))

  if units == "W":
    Hamp=dBtoW(Hamp)
    Namp=dBtoW(Namp)

  value = TopCmds.SELECT("Adjusting the HN CP parameters:",\
  "This will set\n 1H power to:  " + str('%3.2f' %Hamp)+" "+ units+"\n \
  15N power to:  " +str('%3.2f' %Namp) + units,["Update", "Keep Previous"])
    
  if value != 1:
    pul.SetPar('aHhn',Hamp,units)
    pul.SetPar('aNhn',Namp,units)
    pul.SetPar('pHN',CNCT,"")
    if SPH != "Unused":
      pul.SetPar('sHhn',index[1],"")
    if SPX != "Unused":
      pul.SetPar('sNhn',index[3],"")
 
def NCA(units):
  p90H=pul.GetPar('pH90',"")
  p90C=pul.GetPar('pC90',"")
  p90N=pul.GetPar('pN90',"")
  ampH=pul.GetPar('aH',units)
  ampC=pul.GetPar('aC',units)
  ampN=pul.GetPar('aN',units)
  MAS =pul.GetPar('MAS',"")
  CNCT=pul.GetPar('pNCA',"")
  SPX =pul.GetPar('sCnca',"")
  SPY =pul.GetPar('sNnca',"")

  MaxB1H= 1000000./4./p90H

  if units == "W":
    ampN=WtodB(ampN)
    ampC=WtodB(ampC)
    ampH=WtodB(ampH)
    
  if CNCT <= 1.: CNCT = 3500.
  if SPX == "gauss" or SPX == "None" or SPX == "" or SPX == "0" :
    pul.SetPar('sCnca',"ramp.100","")
    TopCmds.XCMD(pul.xcmd_name(pul.pulDict['sCnca']))
    SPX=pul.GetPar('sCnca',"")
  if SPY == "gauss" or SPY == "None" or SPY == "" or SPY == "0" :
    pul.SetPar('sNnca',"ramp.100","")
    TopCmds.XCMD(pul.xcmd_name(pul.pulDict['sNnca']))
    SPY=pul.GetPar('sNnca',"")

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
  ["CA B1 field","N B1 field","H B1 decoupler","Contact Time","Carbon Ramp","Nitrogen Ramp"],\
  [str(CCond),str(NCond),"85000.0",str(CNCT),SPX,SPY],\
  ["Hz","Hz","Hz","us","",""],\
  ["1","1","1","1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)  
  
  adjust=20*(math.log10(float(index[0])/MaxB1C))
  Camp = ampC-adjust
  adjust=20*(math.log10(float(index[1])/MaxB1N))
  Namp = ampN-adjust
  adjust=20*(math.log10(float(index[2])/MaxB1H))
  Hamp = ampH-adjust
  
  CNCT = float(index[3])
  
  #Insert ramp calibration here
  if SPX == "Unused":
    AvgAmp=1.
  else:
    AvgAmp=IntShape.Integrate(index[4])/100.
  adjust=20*(math.log10(1./AvgAmp))
  Camp = Camp-adjust

  if SPY == "Unused":
    AvgAmp=1.
  else:
    AvgAmp=IntShape.Integrate(index[5])/100.
  adjust=20*(math.log10(1./AvgAmp))
  Namp = Namp-adjust  
  
  if units == "W":
    Namp=dBtoW(Namp)
    Camp=dBtoW(Camp)
    Hamp=dBtoW(Hamp)

  value = TopCmds.SELECT("Adjusting the NCA CP parameters:",\
  "This will set\n \
  13C power to:  " + str('%3.2f' %Camp) + " " + units +"\n \
  15N power to:  " + str('%3.2f' %Namp) + " " + units +"\n \
  1H power to:   " + str('%3.2f' %Hamp) + " " + units,["Update", "Keep Previous"])
  
  if value != 1:
    pul.SetPar('aNnca',Namp,units)
    pul.SetPar('aCnca',Camp,units)
    pul.SetPar('aHnca',Hamp,units)
    pul.SetPar('pNCA',CNCT,"")
    if SPX != "Unused":
      pul.SetPar('sCnca',index[4],"")
    if SPY != "Unused":
      pul.SetPar('sNnca',index[5],"")

def NCO(units):
  p90H=pul.GetPar('pH90',"")
  p90C=pul.GetPar('pC90',"")
  p90N=pul.GetPar('pN90',"")
  ampH=pul.GetPar('aH',units)
  ampC=pul.GetPar('aC',units)
  ampN=pul.GetPar('aN',units)
  MAS =pul.GetPar('MAS',"")
  CNCT=pul.GetPar('pNCO',"")
  SPX =pul.GetPar('sCnco',"")
  SPY =pul.GetPar('sNnco',"")

  #TopCmds.MSG(str(CNCT))
  MaxB1H= 1000000./4./p90H

  if units == "W":
    ampN=WtodB(ampN)
    ampC=WtodB(ampC)
    ampH=WtodB(ampH)

  if CNCT <= 1.: CNCT = 3500.
  if SPX == "gauss" or SPX == "None" or SPX == "" or SPX == "0":
    pul.SetPar('sCnco',"ramp.100","")
    TopCmds.XCMD(pul.xcmd_name(pul.pulDict['sCnco']))
    SPX=pul.GetPar('sCnco',"")
  if SPY == "gauss" or SPY == "None" or SPY == "" or SPY == "0" :
    pul.SetPar('sNnco',"ramp.100","")
    TopCmds.XCMD(pul.xcmd_name(pul.pulDict['sNnco']))
    SPY=pul.GetPar('sNnco',"")

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
  ["CO B1 field","N B1 field","H B1 decoupler","Contact Time","Carbon Ramp","Nitrogen Ramp"],\
  [str(CCond),str(NCond),"85000.0",str(CNCT),SPX,SPY],\
  ["Hz","Hz","Hz","us","",""],\
  ["1","1","1","1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)  
  
  adjust=20*(math.log10(float(index[0])/MaxB1C))
  Camp = ampC-adjust
  adjust=20*(math.log10(float(index[1])/MaxB1N))
  Namp = ampN-adjust
  adjust=20*(math.log10(float(index[2])/MaxB1H))
  Hamp = ampH-adjust

  CNCT = float(index[3])

  #Insert ramp calibration here
  if SPX == "Unused":
    AvgAmp=1.
  else:
    AvgAmp=IntShape.Integrate(index[4])/100.
  adjust=20*(math.log10(1./AvgAmp))
  Camp = Camp-adjust

  if SPY == "Unused":
    AvgAmp=1.
  else:
    AvgAmp=IntShape.Integrate(index[5])/100.
  adjust=20*(math.log10(1./AvgAmp))
  Namp = Namp-adjust

  
  if units == "W":
    Namp=dBtoW(Namp)
    Camp=dBtoW(Camp)
    Hamp=dBtoW(Hamp)

  value = TopCmds.SELECT("Adjusting the NCO CP parameters:",\
  "This will set\n \
  13C power to:  " + str('%3.2f' %Camp) + " " + units +"\n \
  15N power to:  " + str('%3.2f' %Namp) + " " + units +"\n \
  1H power to:   " + str('%3.2f' %Hamp) + " " + units,["Update", "Keep Previous"])
    
  if value != 1:
    pul.SetPar('aNnco',Namp,units)
    pul.SetPar('aCnco',Camp,units)
    pul.SetPar('aHnco',Hamp,units)
    pul.SetPar('pNCO',CNCT,"")
    if SPX != "Unused":
      pul.SetPar('sCnco',index[4],"")
    if SPY != "Unused":
      pul.SetPar('sNnco',index[5],"")

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

def HDec(units):

  Stuff = []
  p90=pul.GetPar('pH90',"")
  amp=pul.GetPar('aH',units)
  CPD=pul.GetPar('prgHDec',"")
  MaxB1 = 1000000./4./p90

  if CPD == "mlev" or CPD == "None" :
    pul.SetPar('prgHDec',"tppm15","")
    TopCmds.XCMD(pul.xcmd_name(pul.pulDict['prgHDec']))
    CPD=pul.GetPar('prgHDec',"")

  TopCmds.MSG(str(CPD)+" CPD")
  
  Stuff=CPDtools.CPDparse(CPD,"1H")
  TopCmds.MSG(str(Stuff)+" Stuff")
  amp0=CPDtools.Find_old_pl(Stuff[0],units)
  TopCmds.MSG(str(amp0)+" amp0")

  if units == "W":
    amp=WtodB(amp)
    amp0=WtodB(amp0)
    
  decpw0=CPDtools.Find_old_pw(Stuff[1],"1H")

  B1_0=MaxB1*(math.pow(10,(amp-amp0)/20.))/1000.
  if B1_0 > 1.: B1out='% .1f' % B1_0
  if B1_0 > MaxB1/1000.: B1out='75.0'
  if B1_0 <= 1.: B1out='75.0'
  
  index = TopCmds.INPUT_DIALOG("Mr Setup Input", "Decoupling Window", \
  ["Desired 1H Decoupling Amplitude","File"],\
  [B1out,CPD],["kHz",""],["1","1",],\
  ["Accept","Close"], ['a','c'], 10)
  
  pul.SetPar('prgHDec',index[1],"")
  
  adjust=20*(math.log10(1000.*float(index[0])/MaxB1))
  Hamp = amp-adjust
  decpwH= (MaxB1/1000./float(index[0]))*(170./180.)*2*p90
  
  if units =="W":
    Hamp=dBtoW(Hamp)

  value = TopCmds.SELECT("Adjusting the H decoupling parameters:",\
  "This will set\n 1H power ("+ Stuff[0] +") to:  "+ str('%.2f' %Hamp)+" "+ units+"\n \
  Pulse width ("+ Stuff[1] +") to:  " +str('%3.2f' %decpwH)+" us",["Update", "Keep Previous"])
  
  if value != 1:
    pl=""
    if Stuff[0]!="":  pl=pul.pp_2_xcmd(Stuff[0],"")

    if pl==pul.pulDict['aHdec']:
      pul.SetPar('aHdec',Hamp,units)
    elif pl==pul.pulDict['aHdec2']:
      pul.SetPar('aHdec2',Hamp,units)
    elif pl==pul.pulDict['aHdec3']:
      pul.SetPar('aHdec3',Hamp,units)

    if Stuff[1]=='pcpd':
      pul.SetPar("PCPD 2",decpwH,"")
    elif Stuff[1]=='p31':
      pul.SetPar("P31",decpwH,"")
      pul.SetPar("P30",decpwH,"")
    elif Stuff[1]=='p62':
      pul.SetPar("P61",decpwH,"")
      pul.SetPar("P62",decpwH,"")
  
def NDec(units):

  Stuff = []
  p90=pul.GetPar('pN90',"")
  amp=pul.GetPar('aN',units)
  CPD=pul.GetPar('prgNDec',"")
  MaxB1 = 1000000./4./p90

  if units == "W":
    amp=WtodB(amp)

  if CPD == "mlev" or CPD == "None" :
    TopCmds.XCMD(pul.xcmd_name(pul.pulDict['prgNDec']))
    CPD = pul.GetPar('prgNDec',"")

  Stuff=CPDtools.CPDparse(CPD,"15N")
  amp0=CPDtools.Find_old_pl(Stuff[0],units)
  decpw0=CPDtools.Find_old_pw(Stuff[1],"15N")

  B1_0=MaxB1*(math.pow(10,(amp-amp0)/20.))/1000.
  if B1_0 > 1.: B1out='% .1f' % B1_0
  if B1_0 <= 1.: B1out='15.0'
  
  index = TopCmds.INPUT_DIALOG("Mr Setup Input", "Decoupling Window", \
  ["Desired 15N Decoupling Amplitude","File"],\
  [B1out,CPD],["kHz",""],["1","1",],\
  ["Accept","Close"], ['a','c'], 10)
  
  pul.SetPar('aNdec',index[1],"")
  adjust=20*(math.log10(1000.*float(index[0])/MaxB1))
  Namp = amp-adjust
  decpw = (MaxB1/1000./float(index[0]))*2*p90

  if units =="W":
    Namp=dBtoW(Namp)
  
  value = TopCmds.SELECT("Adjusting the N decoupling parameters:",\
  "This will set\n 15N power ("+ Stuff[0] +") to:  "+ str('%3.2f' %Namp)+" "+ units+"\n \
  Pulse width ("+ Stuff[1] +"= 180deg) to:  " +str('%3.2f' %decpw) + " us",["Update", "Keep Previous"])

  if value != 1:

    pl=""
    if Stuff[0]!="":  pl=pul.pp_2_xcmd(Stuff[0],"")

    if Stuff[0]=="":
      pul.SetPar('aNdec',Namp,units)
    elif pl==pul.pulDict['aNdec']:
      pul.SetPar('aNdec',Namp,units)
    elif pl==pul.pulDict['aHdec']:
      DecError('aHdec',"15N")
    elif pl==pul.pulDict['aHdec2']:
      DecError('aHdec2',"15N")
    elif pl==pul.pulDict['aHdec3']:
      DecError('aHdec3',"15N")

    if Stuff[1]=='pcpd':
      pul.SetPar("PCPD 3",decpw,"")
    elif Stuff[1]=='p31':
      pul.SetPar("P31",decpw,"")
      pul.SetPar("P30",decpw,"")
    elif Stuff[1]=='p62':
      pul.SetPar("P61",decpw,"")
      pul.SetPar("P62",decpw,"")

def DecError(PL,Nuc):
  TopCmds.MSG("You are using "+PL+" for "+Nuc+" decouling.\n  It is usually reserved for 1H \n Please verify")

def CDec(units):

  Stuff = []
  p90=pul.GetPar('pC90',"")
  amp=pul.GetPar('aC',units)
  CPD=pul.GetPar('prgCDec',"")
  MaxB1 = 1000000./4./p90

  if units == "W":
    amp=WtodB(amp)

  if CPD == "mlev" or CPD == "None" :
    TopCmds.XCMD(pul.xcmd_name(pul.pulDict['prgCDec']))
    CPD=pul.GetPar('prgCDec',"")

  Stuff=CPDtools.CPDparse(CPD,"13C")
  amp0=CPDtools.Find_old_pl(Stuff[0])
  decpw0=CPDtools.Find_old_pw(Stuff[1],"13C")

  B1_0=MaxB1*(math.pow(10,(amp-amp0)/20.))/1000.
  if B1_0 > 1.: B1out='% .1f' % B1_0
  if B1_0 <= 1.: B1out='5.0'
  
  index = TopCmds.INPUT_DIALOG("Mr Setup Input", "Decoupling Window", \
  ["Desired 13C Decoupling Amplitude","File"],\
  [B1out,CPD],["kHz",""],["1","1",],\
  ["Accept","Close"], ['a','c'], 10)
  
  pul.SetPar('aCdec',index[1],"")
  adjust=20*(math.log10(1000.*float(index[0])/MaxB1))
  ampli = amp-adjust
  decpw = (MaxB1/1000./float(index[0]))*2*p90

  if units == "W":
    ampli=dBtoW(ampli)
  
  value = TopCmds.SELECT("Adjusting the 13C decoupling parameters:",\
  "This will set\n 13C power ("+ Stuff[0] +") to:  "+ str('%3.2f' %ampli)+" "+ units+"\n \
  Pulse width ("+ Stuff[1] +"= 180deg) to:  " +str('%3.2f' %decpw) + " us",["Update", "Keep Previous"])

  if value != 1:
    pl=""
    if Stuff[0]!="":  pl=pul.pp_2_xcmd(Stuff[0],"")

    if pl=="":
      pul.SetPar('aCdec',ampli,units)
    elif pl==pul.pulDict['aCdec']:
      pul.SetPar('aCdec',ampli,units)
    elif pl==pul.pulDict['aHdec']:
      DecError('aHdec',"13C")
    elif pl==pul.pulDict['aHdec2']:
      DecError('aHdec2',"13C")
    elif pl==pul.pulDict['aHdec3']:
      DecError('aHdec3',"13C")

    if Stuff[1]=='pcpd':
      pul.SetPar("PCPD 3",decpw,"")
    elif Stuff[1]=='p31':
      pul.SetPar("P31",decpw,"")
      pul.SetPar("P30",decpw,"")
    elif Stuff[1]=='p62':
      pul.SetPar("P61",decpw,"")
      pul.SetPar("P62",decpw,"")

def DDec(units):

  Stuff = []
  p90=pul.GetPar('pD90',"")
  amp=pul.GetPar('aD',units)
  CPD=pul.GetPar('prgDDec',"")
  MaxB1 = 1000000./4./p90

  if units == "W":
    amp=WtodB(amp)

  if CPD == "mlev" or CPD == "None" :
    TopCmds.XCMD(pul.xcmd_name(pul.pulDict['prgDDec']))
    CPD=pul.GetPar('prgDDec',"")

  Stuff=CPDtools.CPDparse(CPD,"2H")
  amp0=CPDtools.Find_old_pl(Stuff[0])
  decpw0=CPDtools.Find_old_pw(Stuff[1],"2H")

  B1_0=MaxB1*(math.pow(10,(amp-amp0)/20.))/1000.
  if B1_0 > 1.: B1out='% .1f' % B1_0
  if B1_0 <= 1.: B1out='15.0'
  
  index = TopCmds.INPUT_DIALOG("Mr Setup Input", "Decoupling Window", \
  ["Desired 2H Decoupling Amplitude","File"],\
  [B1out,CPD],["kHz",""],["1","1",],\
  ["Accept","Close"], ['a','c'], 10)
  
  pul.SetPar('aDdec',index[1],"")
  adjust=20*(math.log10(1000.*float(index[0])/MaxB1))
  ampli = amp-adjust
  decpw = (MaxB1/1000./float(index[0]))*2*p90

  if units == "W":
    ampli=dBtoW(ampli)
  
  value = TopCmds.SELECT("Adjusting the 2H decoupling parameters:",\
  "This will set\n 2H power ("+ Stuff[0] +") to:  "+ str('%3.2f' %ampli)+" "+ units+"\n \
  Pulse width ("+ Stuff[1] +"= 180deg) to:  " +str('%3.2f' %decpw) + " us",["Update", "Keep Previous"])

  if value != 1:
    pl=""
    if Stuff[0]!="":  pl=pul.pp_2_xcmd(Stuff[0],"")

    if pl=="":
      pul.SetPar('aDdec',ampli,units)
    elif pl==pul.pulDict['aDdec']:
      pul.SetPar('aDdec',ampli,units)
    elif pl==pul.pulDict['aHdec']:
      DecError('aHdec',"13C")
    elif pl==pul.pulDict['aHdec2']:
      DecError('aHdec2',"13C")
    elif pl==pul.pulDict['aHdec3']:
      DecError('aHdec3',"13C")

    if Stuff[1]=='pcpd':
      pul.SetPar("PCPD 3",decpw,"")
    elif Stuff[1]=='p31':
      pul.SetPar("P31",decpw,"")
      pul.SetPar("P30",decpw,"")
    elif Stuff[1]=='p62':
      pul.SetPar("P61",decpw,"")
      pul.SetPar("P62",decpw,"")

def C72(units):
  p90=pul.GetPar('pC90',"")
  amp=pul.GetPar('aC',units)
  MAS =pul.GetPar('MAS',"")
   
  if units == "W":
    amp=WtodB(amp)

  MaxB1 = 1000000./4./p90
  C7B1  = 7.0*MAS
  adjust=20*(math.log10(C7B1/MaxB1))
  Condition=amp-adjust

  if units == "W":
    Condition=dBtoW(Condition)
  
  pul.SetPar('aCc7',Condition,units)
  pul.SetPar('lC7',"14","")

def SPC5_2(units):
  p90=pul.GetPar('pC90',"")
  amp=pul.GetPar('aC',units)
  MAS =pul.GetPar('MAS',"")
   
  if units == "W":
    amp=WtodB(amp)

  MaxB1 = 1000000./4./p90
  C5B1  = 5.0*MAS
  adjust=20*(math.log10(C5B1/MaxB1))
  Condition=amp-adjust

  if units == "W":
    Condition=dBtoW(Condition)

  pul.SetPar('aCc5',Condition,units)
  pul.SetPar('lC5',"10","")

def SPC5_3(units):
  p90=pul.GetPar('pC90',"")
  amp=pul.GetPar('aC',units)
  MAS =pul.GetPar('MAS',"")
   
  if units == "W":
    amp=WtodB(amp)

  MaxB1 = 1000000./4./p90

  C5B1  = 10.0*MAS/3.0
  adjust=20*(math.log10(C5B1/MaxB1))
  Condition=amp-adjust
  
  if units == "W":
    Condition=dBtoW(Condition)

  pul.SetPar('aCc5',Condition,units)
  pul.SetPar('lC5',"10","")
  
def CalCP(p90H,p90L,ampH,ampL,ampD,Cnct,shH,shL,HXorXY,iGuess,units,In,Out):
    
  P90H=pul.GetPar(p90H,"")
  P90L=pul.GetPar(p90L,"")
  P90D=pul.GetPar('pH90',"")

  #Use Definitions to find hard pulse powers
  if p90H.find('H') >= 0:AmpH=pul.GetPar('aH',units)
  if p90H.find('C') >= 0:AmpH=pul.GetPar('aC',units)
  if p90H.find('N') >= 0:AmpH=pul.GetPar('aN',units)

  if p90L.find('H') >= 0:AmpL=pul.GetPar('aH',units)
  if p90L.find('C') >= 0:AmpL=pul.GetPar('aC',units)
  if p90L.find('N') >= 0:AmpL=pul.GetPar('aN',units)

  SPH =pul.GetPar(shH,"")
  SPL =pul.GetPar(shL,"")
  
  MAS =pul.GetPar('MAS',"")
  CNCT=pul.GetPar(Cnct,"")

  if CNCT <= 1.    : CNCT =  1000.
  if CNCT >= 10000.: CNCT = 10000.

  MaxB1H = 1000000./4./P90H
  MaxB1L = 1000000./4./P90L
  MaxB1D = 1000000./4./P90D

  #Set Decoupler if Appropriate
  if HXorXY=="XY":
    AmpD =pul.GetPar('aH',"dB")
    AmpD0=pul.GetPar(ampD,"dB")

    B1_0 = MaxB1D*(math.pow(10,(AmpD-AmpD0)/20.))
    if B1_0 >  100.  : Dcond='% .1f' % B1_0
    if B1_0 >  MaxB1D: Dcond='85000.0'
    if B1_0 <= 100.  : Dcond='85000.0'
  
  if units == "W":
    AmpH=WtodB(AmpH)
    AmpL=WtodB(AmpL)

  if pul.GetPar(shH,"") == "gauss" or pul.GetPar(shH,"") == "None" or \
  pul.GetPar(shH,"") == "" or pul.GetPar(shH,"") == "0" :
    pul.SetPar(shH,"ramp.100","")
    TopCmds.XCMD(pul.xcmd_name(pul.pulDict[shH]))
    SPH=pul.GetPar(shH,"")
      
  if pul.GetPar(shL,"") == "gauss" or pul.GetPar(shL,"") == "None" or \
  pul.GetPar(shL,"") == "" or pul.GetPar(shL,"") == "0" :
    pul.SetPar(shL,"square.100","")
    TopCmds.XCMD(pul.xcmd_name(pul.pulDict[shL]))
    SPH=pul.GetPar(shL,"")

  if iGuess == "Max":
    #find the channel with the lowest B1
    if MaxB1L < MaxB1H :
      Ratio=int(math.floor(MaxB1L/MAS))
      HCond=(Ratio+0.5)*MAS
      LCond=(Ratio-0.5)*MAS

    if MaxB1L >= MaxB1H :
      Ratio=int(math.floor(MaxB1H/MAS))
      HCond=(Ratio-0.5)*MAS
      LCond=(Ratio+0.5)*MAS

    while HCond > MaxB1H or LCond > MaxB1L:
      Ratio=Ratio-1
      if MaxB1L < MaxB1H :
        HCond=(Ratio+0.5)*MAS
        LCond=(Ratio-0.5)*MAS
      if MaxB1L >= MaxB1H :
        HCond=(Ratio-0.5)*MAS
        LCond=(Ratio+0.5)*MAS

    # If spinning very fast or using weak B1s
    if Ratio == 2:
      LCond= 0.75*MAS
      HCond= 1.75*MAS
    if Ratio <= 1 or HCond > MaxB1H or LCond > MaxB1L:
      LCond= .25*MAS
      HCond= .75*MAS

  else:
    LCond=(5./2.)*MAS
    if iGuess == "Low":
      HCond=(3./2.)*MAS
    else:
      #iGuess == "High":
      HCond=(7./2.)*MAS

    while LCond > MaxB1L :
      LCond=LCond - MAS
      CCond=LCond + MAS

    while HCond > MaxB1H :
      LCond=LCond - MAS
      CCond=LCond + MAS

    if LCond < MAS :
      LCond= 0.25*MAS
      HCond= 0.75*MAS

  adjust=20*(math.log10(LCond/MaxB1L))
  Lamp = AmpL-adjust
  adjust=20*(math.log10(HCond/MaxB1H))
  Hamp = AmpH-adjust

  if HXorXY=="HX":
    index=TopCmds.INPUT_DIALOG(In[0],In[1],In[2],\
      [str(HCond),str(SPH),str(LCond),str(SPL),str(CNCT)],\
      ["Hz","","Hz","","us"],\
      ["1","1","1","1","1"],\
      ["Accept","Close"], ['a','c'], 10)
      
  if HXorXY=="XY":
    index=TopCmds.INPUT_DIALOG(In[0],In[1],In[2],\
      [str(HCond),str(SPH),str(LCond),str(SPL),str(CNCT),str(Dcond)],\
      ["Hz","","Hz","","us","Hz"],\
      ["1","1","1","1","1","1"],\
      ["Accept","Close"], ['a','c'], 10)
  
  adjust=20*(math.log10(float(index[0])/MaxB1H))
  Hamp1 = AmpH-adjust
  if SPH == "Unused":
    AvgAmp=1.
  else:
    AvgAmp=IntShape.Integrate(index[1])/100.
  adjust=20*(math.log10(1./AvgAmp))
  Hamp = Hamp1-adjust

  adjust=20*(math.log10(float(index[2])/MaxB1L))
  Lamp1 = AmpL-adjust
  if SPL == "Unused":
    AvgAmp=1.
  else:
    AvgAmp=IntShape.Integrate(index[3])/100.
  adjust=20*(math.log10(1./AvgAmp))
  Lamp = Lamp1-adjust

  CNCT = float(index[4])

  if HXorXY=="XY":
    adjust=20*(math.log10(float(index[5])/MaxB1D))
    Damp= AmpD-adjust

  if units == "W":
    Hamp=dBtoW(Hamp)
    Lamp=dBtoW(Lamp)
    if HXorXY=="XY":Damp=dBtoW(Damp)
    
  if HXorXY=="HX":
    value = TopCmds.SELECT(Out[0],\
    "This will set\n "+\
    Out[1][0]+" power to:  " + str('%3.2f' %Hamp)+" "+ units+"\n"+\
    Out[1][1]+" power to:  " + str('%3.2f' %Lamp)+" "+ units,\
    ["Update", "Keep Previous"])

  if HXorXY=="XY":
    value = TopCmds.SELECT(Out[0],\
    "This will set\n "+\
    Out[1][0]+" power to:  " + str('%3.2f' %Hamp)+" "+ units+"\n"+\
    Out[1][1]+" power to:  " + str('%3.2f' %Lamp)+" "+ units+"\n"+\
    Out[1][2]+" power to:  " + str('%3.2f' %Damp)+" "+ units,\
    ["Update", "Keep Previous"])
  
  if value != 1:
    pul.SetPar(ampH,Hamp,units)
    pul.SetPar(ampL,Lamp,units)
    
    if HXorXY=="XY":
      pul.SetPar(ampD,Damp,units)
    pul.SetPar(Cnct,CNCT,"")
    if SPH != "Unused":
      pul.SetPar(shH,index[1],"")
    if SPL != "Unused":
      pul.SetPar(shL,index[3],"")

  return

