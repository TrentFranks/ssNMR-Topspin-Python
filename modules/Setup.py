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
import GetNUCs as NUC
from GetLib import pul

Nucs=NUC.list()

deg=u"\u00b0"
ret=u"\u000D"
spc=u"\u0020"
unb=u"\u005f"
crt=u"\u005e"

def dBtoW(dB):
  
  watts=math.pow(10,-dB/10.)
  return watts

def WtodB(watts):
  
  if watts>0.0:
    dB=-10.*math.log10(watts)
  else:
    dB=1000.
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

  p90H, p90C, p90N, ampH, ampC, ampN, MAS = ReadHPFromData(units)

  index = TopCmds.INPUT_DIALOG("Mr Setup Input", "Pulse Widths and Power", \
  ["1H 90 pw","1H ampl","13C 90 pw","13C ampl","15N 90 pw","15N ampl","MAS"],\
  [str('%.2f' %p90H),str('%.2f' %ampH),str('%.2f' %p90C),str('%.2f' %ampC),\
  str('%.2f' %p90N),str('%.2f' %ampN),str('%.2f' %MAS)],\
  ["us",units,"us",units,"us",units," Hz"],\
  ["1","1","1","1","1","1","1"],\
  ["Accept","Close"], [spc,ret], 10)
  
  if index == None:TopCmds.EXIT()
    
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
  # Read the Prosol data (Defaults remain if no Prosol) 
  # Still under development :(
  
  p90H=2.5
  p90C=3.0
  p90N=5.0
  if units == "W":
    ampH=100.
    ampC=200.
    ampN=400.
  else:
    ampH=0.
    ampC=0.
    ampN=0.
  MAS = 10000

  #Read the Prosol data if it exists
  #XCMD('rprosol')

  #p90H, p90C, p90N, ampH, ampC, ampN, MAS = ReadHPFromData(units)
  
  index = TopCmds.INPUT_DIALOG("Mr Setup Input", "Pulse Widths and Power", \
  ["1H 90 pw","1H ampl","13C 90 pw","13C ampl","15N 90 pw","15N ampl","MAS"],\
  [str(p90H),str(ampH),str(p90C),str(ampC),str(p90N),str(ampN),str(MAS)],\
  ["us",units,"us",units,"us",units," Hz"],\
  ["1","1","1","1","1","1","1"],\
  ["Accept","Close"], [spc,ret], 10)
  
  if index == None:TopCmds.EXIT()
  
  p90H=float(index[0])
  ampH=float(index[1])
  p90C=float(index[2])
  ampC=float(index[3])
  p90N=float(index[4])
  ampN=float(index[5])
  MAS =float(index[6])
  TauR= 1000000./MAS
  
  PutPars(p90H,ampH,p90C,ampC,p90N,ampN,MAS,units)

def ReadHPFromData(units):

  p90H=pul.GetPar('pH90',"")
  p90C=pul.GetPar('pC90',"")
  p90N=pul.GetPar('pN90',"")
  ampH=pul.GetPar('aH',units)
  ampC=pul.GetPar('aC',units)
  ampN=pul.GetPar('aN',units)
  MAS =pul.GetPar('MAS',"")
  
  return p90H, p90C, p90N, ampH, ampC, ampN, MAS

def HC(units):

  Title="HC CP Input"; SuTit="Proton Carbon Cross Polarization"
  Label=["Proton B1 Field","H Ramp","Carbon B1 Field","C Ramp",\
         "Contact Time ("+str(pul.pulDict['pHC'])+")"]
  In  =Title,SuTit,Label
  
  Title="Adjusting the HC CP parameters:"; Label="1H","13C"
  Out =Title,Label

  CalCP('pH90','pC90','aHhc','aChc','empty','pHC','sHhc','sChc',"HX","Max",units,"",In,Out)
  
def HN(units):

  Title="HN CP Input"; SuTit="Proton Nitrogen Cross Polarization"
  Label=["Proton B1 Field","H Ramp","Nitrogen B1 Field","N Ramp",\
         "Contact Time ("+str(pul.pulDict['pHN'])+")"]
  In  =Title,SuTit,Label
  Title="Adjusting the HN CP parameters:"; Label="1H","15N"
  Out =Title,Label

  CalCP('pH90','pN90','aHhn','aNhn','empty','pHN','sHhn','sNhn',"HX","Max",units,"",In,Out)
  
def NCA(units):

  Title="NCA CP Input"; SuTit="N-Ca SPECIFIC CP (3/2*C; 5/2*N)"
  Label=  ["CA B1 field","Carbon Ramp","N B1 field","Nitrogen Ramp",\
           "Contact Time ("+str(pul.pulDict['pNCA'])+")","H B1 decoupler"]
  In  =Title,SuTit,Label
  Title="Adjusting the N-Ca CP parameters:"; Label="13C","15N","1H"
  Out =Title,Label

  CalCP('pC90','pN90','aCnca','aNnca','aHnca','pNCA','sCnca','sNnca',"XY","Low",\
  units,"",In,Out)

def NCO(units):

  Title="NCO CP Input"; SuTit="N-Co SPECIFIC CP (7/2*C; 5/2*N)"
  Label=  ["CO B1 field","Carbon Ramp","N B1 field","Nitrogen Ramp",\
           "Contact Time ("+str(pul.pulDict['pNCO'])+")","H B1 decoupler"]
  In  =Title,SuTit,Label
  Title="Adjusting the N-Co CP parameters:"
  Label="13C","15N","1H"
  Out =Title,Label

  CalCP('pC90','pN90','aCnco','aNnco','aHnco','pNCO','sCnco','sNnco',"XY","High",\
  units,"",In,Out)

def CH(units):

  Title="C to H CP Input"; SuTit="Carbon to Proton Cross Polarization"
  Label=["Proton B1 Field","H Ramp","Carbon B1 Field","C Ramp",\
         "Contact Time ("+str(pul.pulDict['pCH'])+")"]
  In  =Title,SuTit,Label
  
  Title="Adjusting the CH CP parameters:"; Label="1H","13C"
  Out =Title,Label

  CalCP('pH90','pC90','aHch2','aCch2','empty','pCH2','sHch2','sCch2',"HX","Max",units,"",In,Out)
  
def NH(units):

  Title="N to H CP Input"; SuTit="Nitrogen to Proton Cross Polarization"
  Label=["Proton B1 Field","H Ramp","Nitrogen B1 Field","N Ramp",\
         "Contact Time ("+str(pul.pulDict['pNH'])+")"]
  In  =Title,SuTit,Label
  Title="Adjusting the HN CP parameters:"; Label="1H","15N"
  Out =Title,Label

  CalCP('pH90','pN90','aHnh2','aNnh2','empty','pNH2','sHnh2','sNnh2',"HX","Max",units,"",In,Out)

def NCAdec(units):
  Title="NCA Decoupling Input"
  SuTit="N-Ca SPECIFIC CP Decoupling"
  Label=  ["H B1 decoupler"]
  In  =Title,SuTit,Label
  Title="Adjusting the N-Ca Decoupling parameters:"
  Label="1H"
  Out =Title,Label

  CPdec('aHnca',units,In,Out)

def NCOdec(units):
  Title="NCO Decoupling Input"; SuTit="N-CO SPECIFIC CP Decoupling"
  Label=  ["H B1 decoupler"]
  In  =Title,SuTit,Label
  Title="Adjusting the N-Co Decoupling parameters:"
  Label="1H"
  Out =Title,Label

  CPdec('aHnco',units,In,Out)
 
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

  dfltWv = "tppm15"
  dfltB0 = 75.0
  dfltPH =170.0
  aOption=['aHdec','aHdec2','aHdec3']
  aFaults=['aNdec']

  pulse=CalDec('pH90','aH','prgHDec',"1H",units,dfltWv,dfltB0,dfltPH,aOption,aFaults)

  if pulse[0]=='pcpd':
    for i in range(len(Nucs)):
      if Nucs[i]=='1H':pcpd="PCPD "+str(i+1)      
    if pcpd != None: pul.SetPar(pcpd,pulse[1],"")
  if pulse[0]=='p31':
      pul.SetPar("P31",pulse[1],"")
      pul.SetPar("P30",pulse[1],"")
  if pulse[0]=='p62':
      pul.SetPar("P61",pulse[1],"")
      pul.SetPar("P62",pulse[1],"")
  
def NDec(units):

  dfltWv = "waltz64"
  dfltB0 = 15.0
  dfltPH = 90.0
  aOption=['aNdec']
  aFaults=['aHdec','aHdec2','aHdec3','aCdec']

  pulse=CalDec('pN90','aN','prgNDec',"15N",units,dfltWv,dfltB0,dfltPH,aOption,aFaults)

  if pulse[0]=='pcpd':
    for i in range(len(Nucs)):
      if Nucs[i]=='15N':pcpd="PCPD "+str(i+1)      
    if pcpd != None: pul.SetPar(pcpd,pulse[1],"")
  if pulse[0]=='p31':
      pul.SetPar("P31",pulse[1],"")
      pul.SetPar("P30",pulse[1],"")
  if pulse[0]=='p62':
      pul.SetPar("P61",pulse[1],"")
      pul.SetPar("P62",pulse[1],"")

def DecError(PL,Nuc):
  TopCmds.MSG("You are using "+PL+" for "+Nuc+" decouling.\n  It is usually reserved for another Nucleus \n Please verify")

def CDec(units):

  dfltWv = "mlev16"
  dfltB0 = 15.0
  dfltPH = 90.0
  aOption=['aCdec']
  aFaults=['aHdec','aHdec2','aHdec3','aNdec']

  pulse=CalDec('pC90','aC','prgCDec',"13C",units,dfltWv,dfltB0,dfltPH,aOption,aFaults)
  
  if pulse[0]=='pcpd':
    for i in range(len(Nucs)):
      if Nucs[i]=='13C':pcpd="PCPD "+str(i+1)      
    if pcpd != None: pul.SetPar(pcpd,pulse[1],"")
  if pulse[0]=='p31':
      pul.SetPar("P31",pulse[1],"")
      pul.SetPar("P30",pulse[1],"")
  if pulse[0]=='p62':
      pul.SetPar("P61",pulse[1],"")
      pul.SetPar("P62",pulse[1],"")

def DDec(units):

  dfltWv = "garp"
  dfltB0 = 15.0
  dfltPH = 90.0
  aOption=['aDdec']
  aFaults=['aHdec','aHdec2','aHdec3','aNdec','aCdec']

  pulse=CalDec('pD90','aD','prgDDec',"2H",units,dfltWv,dfltB0,dfltPH,aOption,aFaults)

  if pulse[0]=='pcpd':
    for i in range(len(Nucs)):
      if Nucs[i]=='2H':pcpd="PCPD "+str(i+1)      
    if pcpd != None: pul.SetPar(pcpd,pulse[1],"")
  if pulse[0]=='p31':
      pul.SetPar("P31",pulse[1],"")
      pul.SetPar("P30",pulse[1],"")
  if pulse[0]=='p62':
      pul.SetPar("P61",pulse[1],"")
      pul.SetPar("P62",pulse[1],"")

def DARR(units):

  CalcSym("C",1,1,1,1,'pH90','aHdarr',"None","dDarr",0.010,"1H","None",units)

def C72(units):

  CalcSym("C",7,2,1,2,'pC90','aCc7',"None","lC7",14,"13C","aHdec2",units)

def SPC5_2(units):

  CalcSym("C",5,2,1,2,'pC90','aCc5',"None","lC5",10,"13C","aHdec2",units)

def SPC5_3(units):

  CalcSym("C",5,3,1,2,'pC90','aCc5',"None","lC5",10,"13C","aHdec2",units)
  
def CPdec(amp,units,In,Out):
  """
  amp   : dict key for CP decoupling amp     
  units : Watts (W) or decibel (dB)
  In    : Title, Subtitle, and Label for Input Dialog
  Out   : Title and Label for Selection/Confirmation Window
  """  

  P90  =pul.GetPar('pH90',"")

  Amp90=pul.GetPar('aH',"dB")
  AmpD0=pul.GetPar(amp,"dB")

  MaxB1D = 1000000./4./P90

  B1_0 = MaxB1D*(math.pow(10,(Amp90-AmpD0)/20.))
  
  if B1_0 >  100.  : Dcond='% .1f' % B1_0
  if B1_0 >  MaxB1D: Dcond='85000.0'
  if B1_0 <= 100.  : Dcond='85000.0'
  Val=[str('%3.3f' %(float(Dcond)/1000.))]

  index=TopCmds.INPUT_DIALOG(In[0],In[1],In[2],\
    Val,["kHz"],["1"],\
    ["Accept","Close"], [spc,ret], 10)
  
  if index == None:
    TopCmds.EXIT()

  #Safety 
  Damp = DecSafely(1000.*float(index[0]),amp,MaxB1D,150000.,Amp90,units)
              
  if units == "W":
    Damp=dBtoW(Damp)
    
  value = TopCmds.SELECT(Out[0],"This will set\n "+\
    Out[1]+" power to:  " + str('%3.2f' %Damp)+" "+ units,\
    ["Update", "Keep Previous"],[spc,ret])
  
  if value != 1:
    pul.SetPar(amp,Damp,units)

  return

def CalCP(p90H,p90L,ampH,ampL,ampD,Cnct,shH,shL,HXorXY,iGuess,units,offsCP,In,Out):
  """
  p90H/L: Dictionary Key for High/Low Gamma Nucleus 90 degree pulse
  ampH/L: dict key for High/Low G CP amp     
  ampD  : dict key for Decoupler (assumed to be 1H) or "empty"
  Cnct  : dict key for CP contact
  shH/L : dict key of CP shape files
  HXorXY: Determines whether decoupling is used
  iGuess: "Max", "High", "Low", "LG"
          Max  : determine highest allowed condition
          High : High G = 3/2 Wr Low G = 5/2 Wr
          Low  : High G = 7/2 Wr Low G = 5/2 Wr
          LG   : Use Max, but adjust for Lee-Goldburg
  units : Watts (W) or decibel (dB)
  offsCP: offset for CP in Hz (LG or off-resonance CP)
  In    : Title, Subtitle, and Label for Input Dialog
  Out   : Title and Label for Selection/Confirmation Window
  """  
  P90H=pul.GetPar(p90H,"")
  P90L=pul.GetPar(p90L,"")
  P90D=pul.GetPar('pH90',"")

  #Use Dictionary Definitions to find hard pulse powers
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
  if iGuess == "LG":
    #Adjust MaxB1H for Lee-Goldburg
    MaxB1H=MaxB1H*math.sqrt(3.0/2.)
  if iGuess == "Max" or iGuess == "LG":
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
      HCond=LCond + MAS

    while HCond > MaxB1H :
      LCond=LCond - MAS
      HCond=LCond + MAS

    if LCond < MAS :
      LCond= 0.25*MAS
      HCond= 0.75*MAS

  if iGuess == "LG":
    #Change MaxB1H back for proper conversion 
    MaxB1H = 1000000./4./P90H
  
  if HXorXY=="HX":
    index=TopCmds.INPUT_DIALOG(In[0],In[1],In[2],\
      [str('%.3f' %(HCond/1000.)),str(SPH),str('%.3f' %(LCond/1000.)),str(SPL),\
      str('%.3f' %(CNCT/1000.))],\
      ["kHz","","kHz","","ms"],\
      ["1","1","1","1","1"],\
      ["Accept","Close"], [spc,ret], 10)
      
  if HXorXY=="XY":
     index=TopCmds.INPUT_DIALOG(In[0],In[1],In[2],\
      [str('%.3f' %(HCond/1000.)),str(SPH),str('%.3f' %(LCond/1000.)),str(SPL),\
      str('%.3f' %(CNCT/1000.)),str('%.3f' %(float(Dcond)/1000.))],\
      ["kHz","","kHz","","ms","kHz"],\
      ["1","1","1","1","1","1"],\
      ["Accept","Close"], [spc,ret], 10)
  
  if index == None:
    TopCmds.EXIT()

  if iGuess == "LG":
    w1H=float(index[0])*math.sqrt(2./3.)
    LGoffs=1000*float(index[0])/math.sqrt(3.)
  else:
    w1H=float(index[0])

  #TopCmds.MSG("w1H "+str('%.2f' %(w1H*1000.))+" MaxB1H: "+str('%.2f' %(MaxB1H)))
  adjust=20*(math.log10(w1H*1000./MaxB1H))
  Hamp1 = AmpH-adjust

  if SPH == "Unused":
    AvgAmp=1.
  else:
    AvgAmp=IntShape.Integrate(index[1])/100.
  adjust=20*(math.log10(1./AvgAmp))
  Hamp = Hamp1-adjust

  adjust=20*(math.log10(float(index[2])*1000./MaxB1L))
  Lamp1 = AmpL-adjust
  if SPL == "Unused":
    AvgAmp=1.
  else:
    AvgAmp=IntShape.Integrate(index[3])/100.
  adjust=20*(math.log10(1./AvgAmp))
  Lamp = Lamp1-adjust

  CNCT = float(index[4])*1000.

  if HXorXY=="XY":
    #Decouple Safely 
    Damp = DecSafely(1000.*float(index[5]),ampD,MaxB1D,150000.,AmpD,units)
                  
  if units == "W":
    Hamp=dBtoW(Hamp)
    Lamp=dBtoW(Lamp)
    if HXorXY=="XY":Damp=dBtoW(Damp)
    
  if HXorXY=="HX":
    if iGuess == "LG":
      value = TopCmds.SELECT(Out[0],\
      "This will set\n "+\
      Out[1][0]+" power ("+ pul.pulDict[ampH] +") to:  " + str('%3.2f' %Hamp)+" "+ units+"\n"+\
      Out[1][1]+" power ("+ pul.pulDict[ampL] +") to:  " + str('%3.2f' %Lamp)+" "+ units+"\n"+\
      "1H LG offset ("+ pul.pulDict[offsCP] +") to:  "+   str('%3.2f' %LGoffs)+ " Hz",\
      ["Update", "Keep Previous"],[spc,ret])
    else:
      value = TopCmds.SELECT(Out[0],\
      "This will set\n "+\
      Out[1][0]+" power ("+ pul.pulDict[ampH] +") to:  " + str('%3.2f' %Hamp)+" "+ units+"\n"+\
      Out[1][1]+" power ("+ pul.pulDict[ampL] +") to:  " + str('%3.2f' %Lamp)+" "+ units,\
      ["Update", "Keep Previous"],[spc,ret])

  if HXorXY=="XY":
    value = TopCmds.SELECT(Out[0],\
    "This will set\n "+\
    Out[1][0]+" power ("+ pul.pulDict[ampH] +") to:  " + str('%3.2f' %Hamp)+" "+ units+"\n"+\
    Out[1][1]+" power ("+ pul.pulDict[ampL] +") to:  " + str('%3.2f' %Lamp)+" "+ units+"\n"+\
    Out[1][2]+" power ("+ pul.pulDict[ampD] +") to:  " + str('%3.2f' %Damp)+" "+ units,\
    ["Update", "Keep Previous"],[spc,ret])
  
  if value != 1:
    pul.SetPar(ampH,Hamp,units)
    pul.SetPar(ampL,Lamp,units)
    pul.SetPar(Cnct,CNCT,"")
    
    if iGuess == "LG":
      pul.SetPar(offsCP,LGoffs,"")
    if HXorXY=="XY":
      pul.SetPar(ampD,Damp,units)
    if SPH != "Unused":
      pul.SetPar(shH,index[1],"")
    if SPL != "Unused":
      pul.SetPar(shL,index[3],"")

  return
  
def DecSafely(B1,amp,B1max,B1upper,aMax,units):
  """
  B1   = input decoupling field
  amp  = Decoupling Dict key
  B1max= Soft limit
  B1upper=Hard limit
  aMax = Soft limit ampl
  input must be in dB
  """
  adjust=20*(math.log10(float(B1)/B1max))
  
  if float(B1) > B1upper:
    if units =="W": MaxAmp=dBtoW(aMax)
    if units =="dB": MaxAmp=aMax
    TopCmds.MSG("<html><p style='text-align: center;'><font size=28><font color=\'DF013A\'>"+\
    "WARNING !!!</p></font><br>"+\
    "\n\nThe decoupling field ("+\
    pul.pulDict[amp]+") exceeds "+str('%.3f' %(float(B1upper)/1000.))+" kHz maximum\n\n"+\
    pul.pulDict[amp]+" will be set to "+str(MaxAmp)+units+"  ("+str('%.3f' %(float(B1max)/1000.))+" kHz)</font>")
    Damp=aMax
    
  elif float(B1) > B1max:
    TopCmds.MSG("<html><p style='text-align: center;'><font size=28><font color=\'DF013A\'>"+\
    "WARNING !!!</p></font><br>"+\
    "\n\nThe desired decoupling field ("+\
    pul.pulDict[amp]+") is "+ str('%.3f' %(float(B1)/1000.))+" kHz\n\n The hard pulse maximum field is "+\
    str('%.3f' %(float(B1max)/1000.))+"\n"+" kHz</html>")
    Damp= aMax-adjust
  else :
    Damp= aMax-adjust
    
  return Damp
  
def CalDec(p90,amp,cpd,nuc,units,dfltWave,dfltB0,dfltPH,aOption,aFaults):
  """
  p90     : Dict key for Hard Pulse of Decoupled Nucleus
  amp     : Dict key for Hard Pulse Amplitude
  cpd     : Dict key for CPD file
  nuc     : Decoupled Nucleus
  units   : Watts (W) or Decibels (dB)
  dfltWave: Default CPD
  dfltB0  : Default field
  dfltPH  : Default tip angle used in CPD
  aOption : List of accepted amplitude dict keys
  aFaults : List of amplitude dict keys that will cause a PLEASE CONFIRM Message
  """
  Stuff = []
  
  P90=pul.GetPar(p90,"")
  Amp=pul.GetPar(amp,units)
  CPD=pul.GetPar(cpd,"")
  
  MaxB1 = 1000000./4./P90

  if CPD == "mlev" or CPD == "None" or CPD == None or CPD == "" :
    pul.SetPar(cpd,dfltWave,"")
    TopCmds.XCMD(pul.xcmd_name(pul.pulDict[cpd]))
    CPD=pul.GetPar(cpd,"")

  Stuff=CPDtools.CPDparse(CPD,nuc)
  Amp0=CPDtools.Find_old_pl(Stuff[0],units)

  if units == "W":
    Amp=WtodB(Amp)
    Amp0=WtodB(Amp0)
    
  decpw0=CPDtools.Find_old_pw(Stuff[1],nuc)

  B1_0=MaxB1*(math.pow(10,(Amp-Amp0)/20.))/1000.
  if B1_0 > 1.         : B1out='% .3f' % B1_0
  if B1_0 > MaxB1/1000.: B1out='% .3f' % dfltB0
  if B1_0 <= 1.        : B1out='% .3f' % dfltB0
  
  index = TopCmds.INPUT_DIALOG("Mr Setup Input", "Decoupling Window", \
  ["Desired "+nuc+" Decoupling Amplitude","File"],\
  [B1out,CPD],["kHz",""],["1","1"],\
  ["Accept","Close"], [spc,ret], 10)
  
  if index == None:
    TopCmds.EXIT()

  pul.SetPar(cpd,index[1],"")
  pl=pul.pp_2_xcmd(Stuff[0],"")

  matched=0
  
  for a in aOption:
    if pl==pul.pulDict[a]:
      matched=1
      Hamp = DecSafely(float(index[0])*1000,a,MaxB1,2*1000.*dfltB0,Amp,units)
  
  if matched==0:
    Hamp = DecSafely(float(index[0])*1000,aOption[0],MaxB1,2*1000.*dfltB0,Amp,units)

  decpw= (MaxB1/1000./float(index[0]))*(dfltPH/180.)*2*P90
  
  if units =="W":
    Hamp=dBtoW(Hamp)

  value = TopCmds.SELECT("Adjusting the "+nuc+" decoupling parameters:",\
  "This will set\n "+nuc+" power ("+ Stuff[0] +") to:  "+ str('%.2f' %Hamp)+" "+ units+"\n \
  Pulse width ("+ Stuff[1] +") to:  " +str('%3.2f' %decpw)+" us",["Update", "Keep Previous"])
  
  if value != 1:
    if Stuff[0]=="":
      pul.SetPar(aOption[0],Hamp,units)
      
    for i in aFaults:
      if pl==pul.pulDict[i]:
        DecError(f,nuc)

    for a in aOption:
      if pl==pul.pulDict[a]:
        pul.SetPar(a,Hamp,units)

  return Stuff[1], decpw

def CalcSym(CorR,N,n,v,mult,p90,amp,Wave,time,dfltT,nuc,dec,units):
  """
  CorR    : Symmetry Element
  N       : Step Number
  n       : Space Winding Number
  v       : Spin Winding Number (not used here, yet)
  mult    : Mulitplier for Composite Pulses
  p90     : Dict key for Hard Pulse of Nucleus
  amp     : Dict key for recoupling Amplitude
  Wave    : Shaped pulse (None or Unused)
  nuc     : Recoupled Nucleus
  dec     : Dict key for Decoupler Nucleus
  dfltT   : Default Time or Loop
  """
  value = 0
  if pul.pulDict[time].find("D")>=0:
    lblT="Delay","s"
  elif pul.pulDict[time].find("L")>=0:
    lblT="Loop","cycles"
  elif pul.pulDict[time].find("P")>=0:
    lblT="Pulse","us"

  #Use Dictionary Definitions to find hard pulse powers
  if p90.find('H') >= 0:Amp=pul.GetPar('aH',"dB")
  if p90.find('C') >= 0:Amp=pul.GetPar('aC',"dB")
  if p90.find('N') >= 0:Amp=pul.GetPar('aN',"dB")

  #Assume 1H decoupling if neccessary
  P90   = pul.GetPar(p90,"")
  P90D  = pul.GetPar('pH90',"")
  MAS   = pul.GetPar('MAS',"")

  Tau_r = 1./float(MAS)
  MaxB1 = 1000000./4./P90
  MaxB1D= 1000000./4./P90D
  #Calculate the RF field
  if CorR == "C":
    Cond=mult*1.*N*MAS/n
  if CorR == "R":
    Cond=mult*2.*N*MAS/n
  
  #Set Decoupler if Appropriate
  if dec!="None":
    AmpD =pul.GetPar('aH',"dB")
    AmpD0=pul.GetPar(dec,"dB")

    B1_0 = MaxB1D*(math.pow(10,(AmpD-AmpD0)/20.))

    if B1_0 >  100.  : Dcond=B1_0
    if B1_0 >  MaxB1D: Dcond=85000.0
    if B1_0 <= 100.  : Dcond=85000.0
    
  if Cond > MaxB1 :
    TopCmds.MSG("The match condition for " + CorR+str(N)+unb+str(n)+crt+str(v)+" is "+\
    str('%.3f' %(Cond/1000.))+" kHz \n\nIt is greater than the Max B1 ("+ str('%.3f' %(MaxB1/1000.))+" kHz)\n\n"+\
    pul.pulDict[amp]+" will NOT be set  ")
    
    TopCmds.EXIT()
  else :
     if dec == "None":
       Title = "Adjusting "+nuc+" Power for Symmetry-Based Recoupling"
       Subtit= CorR+str(N)+unb+str(n)+crt+str(v)+"Symmetry Match"
       Label = [nuc+" Amplitude",lblT[0]+" "+pul.pulDict[time]]
       Values= [str('%.3f' %(Cond/1000.)),str(dfltT)]
       Units = ["kHz",lblT[1]]
       Types = ["1","1"]
       Buttons=["Accept","Cancel"]
       ShortCuts=[spc,ret]
       columns=10
       
     else :
       Title = "Adjusting "+nuc+" Power for Symmetry-Based Recoupling"
       Subtit= CorR+str(N)+unb+str(n)+crt+str(v)+" Symmetry Match"
       Label = [nuc+" Amplitude",lblT[0]+" "+pul.pulDict[time],\
                "1H decoupling field"]

       temp1=Cond/1000.
       temp2=Dcond/1000.
       Values= [str('%.3f' %temp1),str(dfltT),str('%.3f' %temp2)]
       Units = ["kHz",lblT[1],"kHz"]
       Types = ["1","1","1"]
       Buttons=["Accept","Cancel"]
       ShortCuts=[spc,ret]
       columns=10
     
     index=TopCmds.INPUT_DIALOG(Title,Subtit,Label,Values,Units,Types,Buttons,ShortCuts,columns)
     
     if index == None:
       TopCmds.EXIT()
     if index != None:
       Cond=float(index[0])*1000.
       Time=str(index[1])
       if dec != "None":
         #Safety 
         Damp = DecSafely(1000.*float(index[2]),dec,MaxB1D,150000.,AmpD,units)
         
  #Calculate the power
  adjust=20*(math.log10(Cond/MaxB1))
  Condition=Amp-adjust
  
  #Calculate the Integration if shaped pulses are used
  if Wave != "None" and Wave != "Unused" :

    if pul.GetPar(Wave,"") == "gauss" or pul.GetPar(Wave,"") == "None" or \
    pul.GetPar(Wave,"") == "" or pul.GetPar(Wave,"") == "0" :
      pul.SetPar(Wave,"square.100","")
      TopCmds.XCMD(pul.xcmd_name(pul.pulDict[Wave]))
      SP=pul.GetPar(Wave,"")

    AvgAmp=IntShape.Integrate(SP)/100.

    adjust=20*(math.log10(1./AvgAmp))
    Condition=Condition-adjust

  if units == "W":
    Condition=dBtoW(Condition)
    if dec != "None":Damp=dBtoW(Damp)
  
  if dec == "None":
     Confirm=nuc+" Power for "+CorR+str(N)+"_"+str(n)+"^"+str(v)+"Symmetry Match" 
     Power  ="Set\n "+ pul.pulDict[amp]+" to:  "+str('%3.2f' %Condition)+" "+ units+"\n"+\
                         pul.pulDict[time]+" "+lblT[1]+" to: "+index[1]
  else:
     Confirm="Adjusting "+nuc+" and 1H Power for "+CorR+str(N)+"_"+str(n)+"^"+str(v)+"Symmetry Match" 
     Power  ="Set\n "+ pul.pulDict[amp]+" to:  "+str('%3.2f' %Condition)+" "+ units+"\n"+\
                       pul.pulDict[dec]+" (Dec) power to:  "+str('%3.2f' %Damp)+" "+ units+"\n"+\
                       pul.pulDict[time]+" "+lblT[1]+" to: "+index[1]
  
  if Confirm == "None":
    value=1
  else:
    value = TopCmds.SELECT(Confirm,Power,["Update", "Keep Previous"],[spc,ret])
  
  if value != 1:
    pul.SetPar(amp,Condition,units)
    pul.SetPar(time,index[1],"")
    if dec != "None":pul.SetPar(dec,Damp,units)
    
