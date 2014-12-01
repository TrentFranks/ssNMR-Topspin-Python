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
import Setup
from GetLib import pul

ret=u"\u000D"
spc=u"\u0020"

def CH(units):
  Title="CH CP Input"; SuTit="Carbon-Proton Cross Polarization"
  Label=["Proton B1 Field","H Ramp","Carbon B1 Field","C Ramp","Contact Time"]
  In  =Title,SuTit,Label
  
  Title="Adjusting the CH CP parameters:"; Label="1H","13C"
  Out =Title,Label

  copyCP('aHch','sHch','aCch','sCch','pCH','aHhc','sHhc','aChc','sChc','pHC',In,Out,units)

def NH(units):
  Title="NH CP Input"; SuTit="Nitrogen-Proton Cross Polarization"
  Label=["Proton B1 Field","H Ramp","Nitrogen B1 Field","N Ramp","Contact Time"]
  In  =Title,SuTit,Label
  
  Title="Adjusting the CH CP parameters:"; Label="1H","15N"
  Out =Title,Label

  copyCP('aHnh','sHnh','aNnh','sNnh','pNH','aHhn','sHhn','aNhn','sNhn','pHN',In,Out,units)

def HC(units):
  Title="CH CP Input"; SuTit="Carbon-Proton Cross Polarization"
  Label=["Proton B1 Field","H Ramp","Carbon B1 Field","C Ramp","Contact Time"]
  In  =Title,SuTit,Label
  
  Title="Adjusting the CH CP parameters:"; Label="1H","13C"
  Out =Title,Label

  copyCP('aHhhc','sHhhc','aChhc','sChhc','phhC','aHhc','sHhc','aChc','sChc','pHC',In,Out,units)

def copyCP(aH,sH,aL,sL,pCP,aH0,sH0,aL0,sL0,pCP0,Input,Output,units):
  """
  aH/L(0)  : dict key for High/Low G CP amp (0 for default)
  pCP(0)   : dict key for CP contact (0 default)
  shH/L(0) : dict key of CP shape files
  units    : Watts (W) or decibel (dB)
  In       : Title, Subtitle, and Label for Input Dialog
  Out      : Title and Label for Selection/Confirmation Window
  """  

  #Use Dictionary Definitions to find hard pulse powers
  if aH.find('H') >= 0:AmpH=pul.GetPar('aH',"dB"); P90H=pul.GetPar('pH90',""); Hnuc="1H"
  if aH.find('C') >= 0:AmpH=pul.GetPar('aC',"dB"); P90H=pul.GetPar('pC90',""); Hnuc="13C"
  if aH.find('N') >= 0:AmpH=pul.GetPar('aN',"dB"); P90H=pul.GetPar('pN90',""); Hnuc="15N"

  if aL.find('H') >= 0:AmpL=pul.GetPar('aH',"dB"); P90L=pul.GetPar('pH90',""); Lnuc="1H"
  if aL.find('C') >= 0:AmpL=pul.GetPar('aC',"dB"); P90L=pul.GetPar('pC90',""); Lnuc="13C"
  if aL.find('N') >= 0:AmpL=pul.GetPar('aN',"dB"); P90L=pul.GetPar('pN90',""); Lnuc="15N"
  
  MaxB1H=1000000./4./P90H
  MaxB1L=1000000./4./P90L

  SPH =pul.GetPar(sH,"")
  SPL =pul.GetPar(sL,"")

  Hamp0=pul.GetPar(aH0,"dB")
  Lamp0=pul.GetPar(aL0,"dB")
  
  if pul.GetPar(pCP,"") <=   1.00  :
    pul.SetPar(pCP,pul.GetPar(pCP0,""),"")

  CNCT = pul.GetPar(pCP,"")/1000.

  if SPH == "gauss" or SPH == "None" or SPH == ""  or SPH == "0" :
    pul.SetPar(sH,pul.GetPar(sH0,""),"")
    TopCmds.XCMD(pul.xcmd_name(pul.pulDict[sH]))
    SPH = pul.GetPar(sH,"")

  if SPL == "gauss" or SPL == "None" or SPL == "" or SPL == "0":
    pul.SetPar(sL,pul.GetPar(sL0,""),"")
    TopCmds.XCMD(pul.xcmd_name(pul.pulDict[sL]))
    SPX=pul.GetPar(sL0,"")

  if SPH == "Unused":
    Hav  = 1.
    Hav0 = 1.
  else:
    Hav  = IntShape.Integrate(pul.GetPar(sH,""))/100.
    Hav0 = IntShape.Integrate(pul.GetPar(sH0,""))/100.
  
  if SPL == "Unused":
    Lav  = 1.
    Lav0 = 1.
  else:
    Lav  = IntShape.Integrate(pul.GetPar(sL,""))/100.
    Lav0 = IntShape.Integrate(pul.GetPar(sL0,""))/100.

  #This is the new integration times the change in new/old
  Hint = ((Hav)**2)/Hav0
  Lint = ((Lav)**2)/Lav0
  
  B1H = MaxB1H*Hint*math.pow(10,(AmpH-Hamp0)/20.)
  B1L = MaxB1L*Lint*math.pow(10,(AmpL-Lamp0)/20.)
  
  index=TopCmds.INPUT_DIALOG(Input[0],Input[1],Input[2],\
  [str('%.3f' %(B1H/1000.)),SPH,str('%.3f' %(B1L/1000.)),SPL,str(CNCT)],\
  ["kHz","","kHz","","ms"],\
  ["1","1","1","1","1",],\
  ["Accept","Close"], [spc,ret], 10)
  
  if index == None:TopCmds.EXIT()
  SPH=index[1]
  SPX=index[3]
  CNCT=1000*float(index[4])

  adjust=20*(math.log10(1000.*float(index[0])/MaxB1H))
  Hamp1 = AmpH-adjust
  if SPH == "Unused":
    AvgAmp=1.
  else:
    AvgAmp=IntShape.Integrate(index[1])/100.
  adjust=20*(math.log10(1./AvgAmp))
  Hamp = Hamp1-adjust

  adjust=20*(math.log10(1000.*float(index[2])/MaxB1L))
  Lamp = AmpL-adjust
  if SPL == "Unused":
    AvgAmp=1.
  else:
    AvgAmp=IntShape.Integrate(index[3])/100.
  adjust=20*(math.log10(1./AvgAmp))
  Lamp = Lamp-adjust

  if units == "W":
    Hamp=Setup.dBtoW(Hamp)
    Lamp=Setup.dBtoW(Lamp)

  value = TopCmds.SELECT(Output[0],\
  "This will set\n"+\
  Hnuc+" power to:  " + str('%3.2f' %Hamp)+" "+units+"\n"+ \
  Lnuc+" power to:  " +str('%3.2f' %Lamp) + units,\
  ["Update", "Keep Previous"],[spc,ret])
    
  if value != 1:
    pul.SetPar(aH,Hamp,units)
    pul.SetPar(aL,Lamp,units)
    pul.SetPar(pCP,CNCT,"")
    if SPH != "Unused":
      pul.SetPar(sH,index[1],"")
    if SPX != "Unused":
      pul.SetPar(sL,index[3],"")
