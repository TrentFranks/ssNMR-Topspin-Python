"""
Module to adjust existing optimizations upon MAS change:
W.T. Franks FMP Berlin
"""

import de.bruker.nmr.mfw.root as root
import math
import sys
sys.path.append(root.UtilPath.getTopspinHome()+ '/exp/stan/nmr/py/BioPY/modules/')

import TopCmds
import IntShape
import Setup
import GetNUCs as NUC
from GetLib import pul

Nucs=NUC.list()

ret=u"\u000D"
spc=u"\u0020"

def FindMatch(params,pulses,Dia):

  p90H,ampHdB,p90X,ampXdB,avgH0,avgX0=pulses

  MAS0 =float(params[0])
  MAS  =float(params[1])
  ampHCP0dB=float(params[2])
  ampXCP0dB=float(params[3])
  CNCT =float(params[4])
  SPH  =params[5]
  SPX  =params[6]

  avgH=1.
  avgX=1.

  if SPH != "None" and SPH != None and SPH != 'Unused' :
    avgH=IntShape.Integrate(SPH)/100.
    
  if SPX != "None" and SPX != None and SPX != 'Unused' :
    avgX=IntShape.Integrate(SPX)/100.
  
  MaxB1H = 1000000./4./p90H
  MaxB1X = 1000000./4./p90X
    
  HCPpw0=(p90H/avgH0)*(math.pow(10,((ampHCP0dB-ampHdB)/20.)))
  XCPpw0=(p90X/avgX0)*(math.pow(10,((ampXCP0dB-ampXdB)/20.)))
  
  HB1_0=1000000./HCPpw0/4.
  XB1_0=1000000./XCPpw0/4.
  
  HR0=HB1_0/MAS0
  XR0=XB1_0/MAS0
    
  ###   Choices for adjusting the match  ###

  value = TopCmds.SELECT(Dia[0],Dia[1],Dia[2])

  if value == 0:
    XB1=XB1_0
    if HB1_0 > XB1_0 :
      HB1=XB1_0+MAS
    if HB1_0 <= XB1_0 :
      HB1=XB1_0-MAS

    HR=HB1/MAS
    XR=XB1/MAS
    
  elif value == 1:
    HB1=HB1_0
    if HB1_0 > XB1_0 :
      XB1=HB1_0-MAS
    if HB1_0 <= XB1_0 :
      XB1=HB1_0+MAS

    HR=HB1/MAS
    XR=XB1/MAS
    
  elif value == 2:
    HB1=HR0*MAS
    XB1=XR0*MAS
    
    HR=HR0
    XR=XR0
    
    # If we are slowing down, keep CP levels similar to previous
    if MAS0 < MAS:
      if XB1 <= HB1:
        while XB1 <= XB1_0 :
          XR=XR+1
          XB1=XR*MAS
          HR=HR+1
      if XB1 >> HB1:
        while HB1 <= HB1_0 :
          HR=HR+1
          HB1=HR*MAS
          XR=XR+1
      XR=XR-1  #the above should always go one step too far
      HR=HR-1
      XB1=XR*MAS
      HB1=HR*MAS
  else:
    TopCmds.EXIT()
  
  #  Don't allow feilds higher than max
  while XB1 > MaxB1X :
    HR=HR-1
    XR=XR-1
    HB1=HR*MAS
    XB1=XR*MAS
  while HB1 > MaxB1H :
    HR=HR-1
    XR=XR-1
    HB1=HR*MAS
    XB1=XR*MAS

  adjust=20*(math.log10(HB1/HB1_0))
  ampHCPdB = ampHCP0dB-adjust
  adjust=20*(math.log10(avgH/avgH0))  #in case there is a Ramp change 
  ampHCPdB = ampHCP0dB-adjust
  
  adjust=20*(math.log10(XB1/XB1_0))
  ampXCPdB = ampXCP0dB-adjust
  adjust=20*(math.log10(avgX/avgX0))  #in case there is a Ramp change 
  ampXCPdB = ampXCP0dB-adjust
  
  return ampHCPdB, ampXCPdB
  

def HC(MAS0,MAS,units):
  
  p90H=pul.GetPar('pH90',"")
  ampH=pul.GetPar('aH',units)
  SPH=pul.GetPar('sHhc',"")
  ampHCP=pul.GetPar('aHhc',units)
  avgH=1.0

  p90X=pul.GetPar('pC90',"")
  ampX=pul.GetPar('aC',units)
  SPX=pul.GetPar('sChc',"")
  ampXCP=pul.GetPar('aChc',units)
  avgX=1.0
  
  CNCT=pul.GetPar('pHC',"")

  params = TopCmds.INPUT_DIALOG("HC CP MAS adjustment", "Proton Carbon Cross Polarization", \
  ["Old MAS rate","New MAS rate","Old 1H power ("+pul.pulDict['aHhc']+")",\
  "Old 13C power ("+pul.pulDict['aChc']+")","Contact Time ("+pul.pulDict['pHC']+")",\
  "H-Ramp ("+pul.pulDict['sHhc']+")","C-Ramp ("+pul.pulDict['sChc']+")"],\
  [str(MAS0),str(MAS),str(ampXCP),str(ampHCP),str(CNCT),SPH,SPX],\
  ["Hz","Hz",units,units,"us","",""],\
  ["1","1","1","1","1","1","1"],\
  ["Accept","Close"], [spc,ret], 10)

  if params == None:TopCmds.EXIT()

  if units == "W":
    params[2]=str(Setup.WtodB(float(params[2])))
    params[3]=str(Setup.WtodB(float(params[3])))
    ampH=Setup.WtodB(ampH)
    ampX=Setup.WtodB(ampX)

  if SPH != "None" and SPH != None and SPH != "Unused":
    avgH=IntShape.Integrate(SPH)/100.
  if SPX != "None" and SPX != None and SPX != "Unused":
    avgX=IntShape.Integrate(SPX)/100.
  
  pulses=p90H,ampH,p90X,ampX,avgH,avgX
  
  SelectorText="Adjust the HC CP parameters:","Calculate New Match for:",\
  ["Proton","Carbon","Maximum for Both"]
  
  ampHCP, ampXCP = FindMatch(params,pulses,SelectorText)

  if units == "W":
    ampXCP=Setup.dBtoW(ampXCP)
    ampHCP=Setup.dBtoW(ampHCP)
  
  value = TopCmds.SELECT("Adjusting the HC CP parameters:",\
  "This will set\n 1H power to:  " + str('%3.2f' %ampHCP)+ " "+units+"\n \
  13C power to:  " +str('%3.2f' %ampXCP) + " "+units,["Update", "Keep Previous"])
    
  if value != 1:
    pul.SetPar('aHhc',ampHCP,units)
    pul.SetPar('aChc',ampXCP,units)
    pul.SetPar('pHC',CNCT,"")      
    pul.SetPar('sHhc',SPH,"")      
    pul.SetPar('sChc',SPX,"")      

def HN(MAS0,MAS,units):

  p90H=pul.GetPar('pH90',"")
  ampH=pul.GetPar('aH',units)
  SPH=pul.GetPar('sHhn',"")
  ampHCP=pul.GetPar('aHhn',units)
  avgH=1.0

  p90X=pul.GetPar('pN90',"")
  ampX=pul.GetPar('aN',units)
  SPX=pul.GetPar('sNhn',"")
  ampXCP=pul.GetPar('aNhn',units)
  avgX=1.0
  
  CNCT=pul.GetPar('pHN',"")
  
  params = TopCmds.INPUT_DIALOG("HN CP MAS adjustment", "Proton Nitrogen Cross Polarization", \
  ["Old MAS rate","New MAS rate","Old 1H power ("+pul.pulDict['aHhc']+")",\
  "Old 15N power ("+pul.pulDict['aNhn']+")","Contact Time ("+pul.pulDict['pHN']+")",\
  "H-Ramp ("+pul.pulDict['sHhc']+")","N-Ramp ("+pul.pulDict['sChc']+")"],\
  [str(MAS0),str(MAS),str(ampXCP),str(ampHCP),str(CNCT),SPH,SPX],\
  ["Hz","Hz",units,units,"us","",""],\
  ["1","1","1","1","1","1","1"],\
  ["Accept","Close"], [spc,ret], 10)

  if params == None: TopCmds.EXIT()

  if units == "W":
    params[2]=str(Setup.WtodB(float(params[2])))
    params[3]=str(Setup.WtodB(float(params[3])))
    ampH=Setup.WtodB(ampH)
    ampX=Setup.WtodB(ampX)

  if SPH != "None" and SPH != None and SPH != "Unused":
    avgH=IntShape.Integrate(SPH)/100.
  if SPX != "None" and SPX != None and SPX != "Unused":
    avgX=IntShape.Integrate(SPX)/100.
  
  pulses=p90H,ampH,p90X,ampX,avgH,avgX
  
  SelectorText="Adjust the HN CP parameters:","Calculate New Match for:",\
  ["Proton","Nitrogen","Maximum for Both"]
  
  ampHCP, ampXCP = FindMatch(params,pulses,SelectorText)

  if units == "W":
    ampXCP=Setup.dBtoW(ampXCP)
    ampHCP=Setup.dBtoW(ampHCP)
  
  value = TopCmds.SELECT("Adjusting the HN CP parameters:",\
  "This will set\n 1H power to:  " + str('%3.2f' %ampHCP)+ " "+units+"\n \
  15N power to:  " +str('%3.2f' %ampXCP) + " "+units,["Update", "Keep Previous"])
    
  if value != 1:
    pul.SetPar('aHhn',ampHCP,units)
    pul.SetPar('aNhn',ampXCP,units)
    pul.SetPar('pHN',CNCT,"")
    pul.SetPar('sHhn',SPH,"")
    pul.SetPar('sNhn',SPX,"")

def NCA(MAS0,MAS,units):

  p90X=pul.GetPar('pC90',"")
  ampX=pul.GetPar('aC',units)
  ampXCP=pul.GetPar('aCnca',units)
  SPX=pul.GetPar('sCnca',"")
  avgX=1.  

  p90Y=pul.GetPar('pN90',"")
  ampY=pul.GetPar('aN',units)
  ampYCP=pul.GetPar('aNnca',units)
  SPY=pul.GetPar('sNnca',"")
  avgY=1.  
  
  CNCT=pul.GetPar('pNCA',"")

  # Get the integration before possibly changing the shape.
  if SPX != "None" and SPX != None and SPX != "Unused":
    avgX=IntShape.Integrate(SPX)/100.
  if SPY == "None" or SPY == None and SPY != "Unused":
    avgY=IntShape.Integrate(SPY)/100.

  #Interact with user about MAS and power levels, likely not needed
  params = TopCmds.INPUT_DIALOG("NCA CP MAS adjustment", "NCA", \
  ["Old MAS rate","New MAS rate","Old CA power ("+pul.pulDict['aCnca']+")",\
  "Old 15N power ("+pul.pulDict['aNnca']+")","Contact Time ("+pul.pulDict['pNCA']+")",\
  "CA-Ramp ("+pul.pulDict['sCnca']+")","N-Ramp ("+pul.pulDict['sNnca']+")"],\
  [str(MAS0),str(MAS),str(ampXCP),str(ampYCP),str(CNCT),SPX,SPY],\
  ["Hz","Hz",units,units,"us","",""],\
  ["1","1","1","1","1","1","1"],\
  ["Accept","Close"], [spc,ret], 10)
 
  if params == None: TopCmds.EXIT()

  # Everything is written with dB, so we might have to convert
  if units == "W":
    params[2]=str(Setup.WtodB(float(params[2])))
    params[3]=str(Setup.WtodB(float(params[3])))
    ampX=Setup.WtodB(ampX)
    ampY=Setup.WtodB(ampY)
  
  pulses=p90X,ampX,p90Y,ampY,avgX,avgY
  
  SelectorText="Adjust the NCA CP parameters:","Calculate New Power Level for:",\
  ["Carbon","Nitrogen","Both"]
  
  ampXCP, ampYCP = FindMatch(params,pulses,SelectorText)

  if units == "W":
    ampXCP=Setup.dBtoW(ampXCP)
    ampYCP=Setup.dBtoW(ampYCP)
  
  value = TopCmds.SELECT("Adjusting the NCA CP parameters:",\
  "This will set\n 13C power to:  " + str('%3.2f' %ampXCP)+ " "+units+"\n \
  15N power to:  " +str('%3.2f' %ampYCP) + " "+units,["Update", "Keep Previous"])
    
  if value != 1:
    pul.SetPar('aCnca',ampXCP,units)
    pul.SetPar('aNnca',ampYCP,units)
    pul.SetPar('pNCA',CNCT,"")      
    pul.SetPar('sCnca',SPX,"")      
    pul.SetPar('sNnca',SPY,"")      

def NCO(MAS0,MAS,units):

  p90X=pul.GetPar('pC90',"")
  ampX=pul.GetPar('aC',units)
  ampXCP=pul.GetPar('aCnco',units)
  SPX=pul.GetPar('sCnco',"")
  avgX=1.  

  p90Y=pul.GetPar('pN90',"")
  ampY=pul.GetPar('aN',units)
  ampYCP=pul.GetPar('aNnco',units)
  SPY=pul.GetPar('sNnco',"")
  avgY=1.  
  
  CNCT=pul.GetPar('pNCO',"")

  # Get the integration before possibly changing the shape.
  if SPX != "None" and SPX != None and SPX != "Unused":
    avgX=IntShape.Integrate(SPX)/100.
  if SPY == "None" or SPY == None and SPY != "Unused":
    avgY=IntShape.Integrate(SPY)/100.

  #Interact with user about MAS and power levels, likely not needed
  params = TopCmds.INPUT_DIALOG("NCO CP MAS adjustment", "NCO", \
  ["Old MAS rate","New MAS rate","Old CO power ("+pul.pulDict['aCnco']+")",\
  "Old 15N power ("+pul.pulDict['aNnco']+")","Contact Time ("+pul.pulDict['pNCO']+")",\
  "CO-Ramp ("+pul.pulDict['sCnco']+")","N-Ramp ("+pul.pulDict['sNnco']+")"],\
  [str(MAS0),str(MAS),str(ampXCP),str(ampYCP),str(CNCT),SPX,SPY],\
  ["Hz","Hz",units,units,"us","",""],\
  ["1","1","1","1","1","1","1"],\
  ["Accept","Close"], [spc,ret], 10)
 
  if params == None: TopCmds.EXIT()

  # Everything is written with dB, so we might have to convert
  if units == "W":
    params[2]=str(Setup.WtodB(float(params[2])))
    params[3]=str(Setup.WtodB(float(params[3])))
    ampX=Setup.WtodB(ampX)
    ampY=Setup.WtodB(ampY)

  pulses=p90X,ampX,p90Y,ampY,avgX,avgY
  
  SelectorText="Adjust the NCO CP parameters:","Calculate New Power Level for:",\
  ["Carbon","Nitrogen","Both"]
  
  ampXCP, ampYCP = FindMatch(params,pulses,SelectorText)

  if units == "W":
    ampXCP=Setup.dBtoW(ampXCP)
    ampYCP=Setup.dBtoW(ampYCP)
  
  value = TopCmds.SELECT("Adjusting the NCO CP parameters:",\
  "This will set\n 13C power to:  " + str('%3.2f' %ampXCP)+ " "+units+"\n \
  15N power to:  " +str('%3.2f' %ampYCP) + " "+units,["Update", "Keep Previous"])
    
  if value != 1:
    pul.SetPar('aCnco',ampXCP,units)
    pul.SetPar('aNnco',ampYCP,units)
    pul.SetPar('pNCO',CNCT,"")      
    pul.SetPar('sCnco',SPX,"")      
    pul.SetPar('sNnco',SPY,"")      

def C72(MASR,MAS,units):
  
  oldC7=pul.GetPar('aCc7',units)
  LoopC7=pul.GetPar('lC7',"")
  
  index = TopCmds.INPUT_DIALOG("POST-C7 MAS", "POST-C7 MAS change", \
  ["Old MAS rate","New MAS rate","Old 13C power ("+pul.pulDict['aCc7']+")",\
  "Mixing Loop ("+pul.pulDict['lC7']+")"],\
  [str(MASR),str(MAS),str(oldC7),str(LoopC7)],\
  ["kHz","kHz",units,""],\
  ["1","1","1","1"],\
  ["Accept","Close"], [spc,ret], 10)
  
  if index == None:TopCmds.EXIT()
  
  OldMAS=float(index[0])
  NewMAS=float(index[1])
  oldC7 =float(index[2])
  newL7 =float(index[3])

  if units == "W":
    oldC7=Setup.WtodB(oldC7)

  adjust=20*(math.log10(NewMAS/OldMAS))
  newC7=oldC7-adjust

  if units == "W":
    newC7=Setup.dBtoW(newC7)
  
  value = TopCmds.SELECT("Adjusting the POST-C7 parameters:",\
  "This will set\n 13C power "+pul.pulDict['aCc7']+" to:  " +\
  str('%3.2f' %newC7)+ " "+units+"\n"+\
  "Loop "+pul.pulDict['lC7']+" to:  "+ str(newL7)\
  ,["Update", "Keep Previous"])
    
  if value != 1:
    pul.SetPar('aCc7',newC7,units)
    pul.SetPar('lC7' ,newL7,"")
  
def SPC5(MASR,MAS,units):
  
  oldC5=pul.GetPar('aCc5',units)
  LoopC5=pul.GetPar('lC5',"")
    
  index = TopCmds.INPUT_DIALOG("SPC5 MAS", "SPC5 changes for MAS change", \
  ["Old MAS rate","New MAS rate","Old 13C power ("+pul.pulDict['aCc5']+")",\
  "Mixing Loop ("+pul.pulDict['lC5']+")"],\
  [str(MASR),str(MAS),str(oldC5),str(LoopC5)],\
  ["kHz","kHz",units,""],\
  ["1","1","1","1"],\
  ["Accept","Close"], [spc,ret], 10)
  
  if index == None:TopCmds.EXIT()
  
  OldMAS=float(index[0])
  NewMAS=float(index[1])
  oldC =float(index[2])
  newL =float(index[3])

  if units == "W":
    oldC=Setup.WtodB(oldC)

  adjust=20*(math.log10(NewMAS/OldMAS))
  newC=oldC-adjust

  if units == "W":
    newC=Setup.dBtoW(newC)
  
  value = TopCmds.SELECT("Adjusting the SPC5 parameters:",\
  "This will set\n 13C power "+pul.pulDict['aCc5']+" to:  " +\
  str('%3.2f' %newC)+ " "+units+"\n"+\
  "Loop "+pul.pulDict['lC5']+" to:  "+ str(newL)\
  ,["Update", "Keep Previous"])
    
  if value != 1:
    pul.SetPar('aCc5',newC,units)
    pul.SetPar('lC5' ,newL,"")
  
"""
def DREAM(units):
  
  Camp0=pul.GetPar('aCdrm',units)
  RAMP=pul.GetPar('sCdrm',"")
  tDream=pul.GetPar('pDRM',"")
  AvgAmp0=IntShape.Integrate(RAMP)/100.
  
  if units == "W":
    Camp0=Setup.WtodB(Camp0)

  index = TopCmds.INPUT_DIALOG("DREAM MAS", "DREAM changes for MAS change", \
  ["Old MAS rate","New MAS rate","Old 13C power ("+pul.pulDict['aCdrm']+")",\
  "Mixing time ("+pul.pulDict['pCdrm']+")","Ramp Name ("+pul.pulDict['sCdrm']+")"],\
  [str(MASR),str(MAS),str(Camp0),str(tDream),RAMP],\
  ["kHz","kHz",units,"us",""],\
  ["1","1","1","1","1"],\
  ["Accept","Close"], [spc,ret], 10)
  
  if index == None:TopCmds.EXIT()

  OldMAS=float(index[0])
  NewMAS=float(index[1])
  olddB=float(index[2])
  newmix=float(index[3])
  RAMP  =index[4]
  #AvgAmpNew=IntShape.Integrate(RAMP)/100.

  adjust=20*(math.log10(NewMAS/OldMAS))
  newdB = olddB-adjust
  adjust=20*(math.log10(AvgAmpNew/AvgAmpOld))  #in case there is a Ramp change 
  newdB = newdB-adjust  
  
  if units == "W":
    Camp=Setup.dBtoW(newdB)
    
  pul.SetPar('aCdrm',Camp,units)
  pul.SetPar('pDRM',newmix,"")
  pul.SetPar('sCdrm',RAMP,"")
  
  oldC5=pul.GetPar('aCc5',units)
  LoopC5=pul.GetPar('lC5',"")
    
  index = TopCmds.INPUT_DIALOG("SPC5 MAS", "SPC5 changes for MAS change", \
  ["Old MAS rate","New MAS rate","Old 13C power("+pul.pulDict['aCc5']+")",\
  "Mixing Loop ("+pul.pulDict['lC5']+")"],\
  [str(MASR),str(MAS),str(oldC7),str(LoopC7)],\
  ["kHz","kHz",units,""],\
  ["1","1","1","1"],\
  ["Accept","Close"], [spc,ret], 10)
  
  if index == None:TopCmds.EXIT()
  
  OldMAS=float(index[0])
  NewMAS=float(index[1])
  oldC =float(index[2])
  newL =float(index[3])

  if units == "W":
    oldC=Setup.WtodB(oldC)

  adjust=20*(math.log10(NewMAS/OldMAS))
  newC=oldC-adjust

  if units == "W":
    newC=Setup.dBtoW(newC)
  
  value = TopCmds.SELECT("Adjusting the SPC5 parameters:",\
  "This will set\n 13C power "+pul.pulDict['aCc5']+" to:  " +\
  str('%3.2f' %newC)+ " "+units+"\n"+\
  "Loop "+pul.pulDict['lC5']+" to:  "+ str(newL)\
  ,["Update", "Keep Previous"])
    
  if value != 1:
    pul.SetPar('aCc5',units)
    pul.SetPar('lC5',"")
  
"""