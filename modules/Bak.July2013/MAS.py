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

def FindMatch(params,pulses,Dia):

  p90H,ampHdB,p90X,ampXdB,avgH0,avgX0=pulses

  MAS0 =float(params[0])
  MAS  =float(params[1])
  ampXCP0dB=float(params[2])
  ampHCP0dB=float(params[3])
  CNCT =float(params[4])
  SPH  =params[5]
  SPX  =params[6]

  avgH=1.
  avgX=1.

  if SPH != "None" and SPH != None:
    avgH=IntShape.Integrate(SPH)/100.
  if SPH == "None" or SPH == None:
    avgH=1.
    
  if SPX != "None" and SPX != None:
    avgX=IntShape.Integrate(SPX)/100.
  if SPX == "None" or SPX == None:
    avgX=1.
  
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
  p90H=float(TopCmds.GETPAR("P 3"))
  ampH=float(TopCmds.GETPAR("PL"+units+" 2"))
  ampHdB=float(TopCmds.GETPAR("PLdB 2"))
  
  ampHCP0=float(TopCmds.GETPAR("SP"+units+" 40"))
  ampHCP0dB=float(TopCmds.GETPAR("SPdB 40"))
  #ampHCP0=float(TopCmds.GETPAR("PL"+units+" 10"))
  #ampHCP0dB=float(TopCmds.GETPAR("PLdB 10"))
  SPH=TopCmds.GETPAR2("SPNAM 40")
  
  p90X=float(TopCmds.GETPAR("P 1"))
  ampX=float(TopCmds.GETPAR("PL"+units+" 1"))
  ampXdB=float(TopCmds.GETPAR("PLdB 1"))
  
  ampXCP0=float(TopCmds.GETPAR("SP"+units+" 41"))
  ampXCP0dB=float(TopCmds.GETPAR("SPdB 41"))
  #ampXCP0=float(TopCmds.GETPAR("PL"+units+" 20"))
  #ampXCP0dB=float(TopCmds.GETPAR("PLdB 20"))
  SPX=TopCmds.GETPAR2("SPNAM 41")
  
  CNCT=float(TopCmds.GETPAR("P 15"))

  params = TopCmds.INPUT_DIALOG("HC CP MAS adjustment", "Proton Carbon Cross Polarization", \
  ["Old MAS rate","New MAS rate","Old 13C power","Old 1H power","Contact Time(P15)","H-Ramp","C-Ramp"],\
  [str(MAS0),str(MAS),str(ampXCP0),str(ampHCP0),str(CNCT),SPH,SPX],\
  ["Hz","Hz",units,units,"us","",""],\
  ["1","1","1","1","1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)

  if units == "W":
    params[2]=str(Setup.WtodB(float(params[2])))
    params[3]=str(Setup.WtodB(float(params[3])))

  if SPH != "None" and SPH != None:
    avgH0=IntShape.Integrate(SPH)/100.
  if SPX != "None" and SPX != None:
    avgX0=IntShape.Integrate(SPX)/100.
  
  pulses=p90H,ampHdB,p90X,ampXdB,avgH0,avgX0
  
  SelectorText="Adjust the HC CP parameters:","Calculate New Match for:",\
  ["Proton","Carbon","Maximum for Both"]
  
  ampHCPdB, ampXCPdB = FindMatch(params,pulses,SelectorText)

  if units == "W":
    ampXCP=Setup.dBtoW(ampXCPdB)
    ampHCP=Setup.dBtoW(ampHCPdB)
  
  value = TopCmds.SELECT("Adjusting the HC CP parameters:",\
  "This will set\n 1H power to:  " + str('%3.2f' %ampHCP)+ " "+units+"\n \
  13C power to:  " +str('%3.2f' %ampXCP) + " "+units,["Update", "Keep Previous"])
    
  if value != 1:
    TopCmds.PUTPAR("PLdB 40",str('%3.2f' %ampHCPdB))
    TopCmds.PUTPAR("SPdB 40",str('%3.2f' %ampHCPdB))
    TopCmds.PUTPAR("PLdB 41",str('%3.2f' %ampXCPdB))
    TopCmds.PUTPAR("SPdB 41",str('%3.2f' %ampXCPdB))
    TopCmds.PUTPAR("P 15" ,params[4])
    TopCmds.PUTPAR("SPNAM 40",params[5])
    TopCmds.PUTPAR("SPNAM 41",params[6])


def HN(MAS0,MAS,units):

  p90H=float(TopCmds.GETPAR("P 3"))
  ampH=float(TopCmds.GETPAR("PL"+units+" 2"))
  ampHdB=float(TopCmds.GETPAR("PLdB 2"))
  
  ampHCP0=float(TopCmds.GETPAR("SP"+units+" 42"))
  ampHCP0dB=float(TopCmds.GETPAR("SPdB 42"))
  #ampHCP0=float(TopCmds.GETPAR("PL"+units+" 42"))
  #ampHCP0dB=float(TopCmds.GETPAR("PLdB 42"))
  SPH=TopCmds.GETPAR2("SPNAM 42")
  
  p90X=float(TopCmds.GETPAR("P 21"))
  ampX=float(TopCmds.GETPAR("PL"+units+" 3"))
  ampXdB=float(TopCmds.GETPAR("PLdB 3"))
  
  ampXCP0=float(TopCmds.GETPAR("SP"+units+" 43"))
  ampXCP0dB=float(TopCmds.GETPAR("SPdB 43"))
  #ampXCP0=float(TopCmds.GETPAR("PL"+units+" 43"))
  #ampXCP0dB=float(TopCmds.GETPAR("PLdB 43"))
  SPX=TopCmds.GETPAR2("SPNAM 43")
  CNCT=float(TopCmds.GETPAR("P 25"))
  
  #Interact with user about MAS and power levels, likely not needed
  params = TopCmds.INPUT_DIALOG("HN CP MAS adjustment", "Proton Nitrogen Cross Polarization", \
  ["Old MAS rate","New MAS rate","Old 15N power","Old 1H power","Contact Time(P15)","H-Ramp","N-Ramp"],\
  [str(MAS0),str(MAS),str(ampXCP0),str(ampHCP0),str(CNCT),SPH,SPX],\
  ["kHz","kHz",units,units,"us","",""],\
  ["1","1","1","1","1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)
  
  if params == None: TopCmds.EXIT()

  # Everything is written with dB, so we might have to convert
  if units == "W":
    params[2]=str(Setup.WtodB(float(params[2])))
    params[3]=str(Setup.WtodB(float(params[3])))

  if SPH != "None" and SPH != None:
    avgH0=1.
    avgH0=IntShape.Integrate(SPH)/100.
  if SPX != "None" and SPX != None:
    avgX0=1.
    avgX0=IntShape.Integrate(SPX)/100.
  
  pulses=p90H,ampHdB,p90X,ampXdB,avgH0,avgX0
  
  SelectorText="Adjust the HN CP parameters:","Calculate New Match for:",\
  ["Proton","Nitrogen","Maximum for Both"]
  
  ampHCPdB, ampXCPdB = FindMatch(params,pulses,SelectorText)

  if units == "W":
    ampXCP=Setup.dBtoW(ampXCPdB)
    ampHCP=Setup.dBtoW(ampHCPdB)
  
  value = TopCmds.SELECT("Adjusting the HN CP parameters:",\
  "This will set\n 1H power to:  " + str('%3.2f' %ampHCP)+ " "+units+"\n \
  15N power to:  " +str('%3.2f' %ampXCP) + " "+units,["Update", "Keep Previous"])
    
  if value != 1:
    TopCmds.PUTPAR("PLdB 42",str('%3.2f' %ampHCPdB))
    TopCmds.PUTPAR("SPdB 42",str('%3.2f' %ampHCPdB))
    TopCmds.PUTPAR("PLdB 43",str('%3.2f' %ampXCPdB))
    TopCmds.PUTPAR("SPdB 43",str('%3.2f' %ampXCPdB))
    TopCmds.PUTPAR("P 25" ,str('%3.2f' %CNCT))
    TopCmds.PUTPAR("SPNAM 42",SPH)
    TopCmds.PUTPAR("SPNAM 43",SPX)

def NCA(MAS0,MAS,units):

  p90X=float(TopCmds.GETPAR("P 1"))
  ampX=float(TopCmds.GETPAR("PL"+units+" 1"))
  ampXdB=float(TopCmds.GETPAR("PLdB 1"))
  
  ampXCP0=float(TopCmds.GETPAR("SP"+units+" 50"))
  ampXCP0dB=float(TopCmds.GETPAR("SPdB 50"))
  #ampXCP0=float(TopCmds.GETPAR("PL"+units+" 50"))
  #ampXCP0dB=float(TopCmds.GETPAR("PLdB 50"))
  SPX=TopCmds.GETPAR2("SPNAM 50")
  

  p90Y=float(TopCmds.GETPAR("P 3"))
  ampY=float(TopCmds.GETPAR("PL"+units+" 2"))
  ampYdB=float(TopCmds.GETPAR("PLdB 2"))
  
  ampYCP0=float(TopCmds.GETPAR("PL"+units+" 5"))
  ampYCP0dB=float(TopCmds.GETPAR("PLdB 5"))
  SPY="None"
  avgY0=1.  
  
  CNCT=float(TopCmds.GETPAR("P 16"))

  # Get the integration before possibly changing the shape.
  if SPX != "None" and SPX != None:
    avgX0=IntShape.Integrate(SPX)/100.
  if SPX == "None" or SPX == None:
    avgX0=1.

  #Interact with user about MAS and power levels, likely not needed
  params = TopCmds.INPUT_DIALOG("NCA CP MAS adjustment", "Proton Nitrogen Cross Polarization", \
  ["Old MAS rate","New MAS rate","Old 13C power","Old 15N power","Contact Time(P16)","C-Ramp"],\
  [str(MAS0),str(MAS),str(ampXCP0),str(ampYCP0),str(CNCT),SPX],\
  ["kHz","kHz",units,units,"us",""],\
  ["1","1","1","1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)
  
  if params == None: TopCmds.EXIT()
  params.append(SPY)

  # Everything is written with dB, so we might have to convert
  if units == "W":
    params[2]=str(Setup.WtodB(float(params[2])))
    params[3]=str(Setup.WtodB(float(params[3])))

  pulses=p90X,ampXdB,p90Y,ampYdB,avgX0,avgY0
  
  SelectorText="Adjust the NCA CP parameters:","Calculate New Power Level for:",\
  ["Carbon","Nitrogen","Both"]
  
  ampXCPdB, ampYCPdB = FindMatch(params,pulses,SelectorText)

  if units == "W":
    ampXCP=Setup.dBtoW(ampXCPdB)
    ampYCP=Setup.dBtoW(ampYCPdB)
  
  value = TopCmds.SELECT("Adjusting the NCA CP parameters:",\
  "This will set\n 13C power to:  " + str('%3.2f' %ampXCP)+ " "+units+"\n \
  15N power to:  " +str('%3.2f' %ampYCP) + " "+units,["Update", "Keep Previous"])
    
  if value != 1:
    TopCmds.PUTPAR("PLdB 50",str('%3.2f' %ampXCPdB))
    TopCmds.PUTPAR("SPdB 50",str('%3.2f' %ampXCPdB))
    TopCmds.PUTPAR("PLdB 5",str('%3.2f' %ampYCPdB))
    TopCmds.PUTPAR("P 16" ,str('%3.2f' %CNCT))
    TopCmds.PUTPAR("SPNAM 50",SPX)

def NCO(MAS0,MAS,units):

  p90X=float(TopCmds.GETPAR("P 1"))
  ampX=float(TopCmds.GETPAR("PL"+units+" 1"))
  ampXdB=float(TopCmds.GETPAR("PLdB 1"))
  
  ampXCP0=float(TopCmds.GETPAR("SP"+units+" 51"))
  ampXCP0dB=float(TopCmds.GETPAR("SPdB 51"))
  #ampXCP0=float(TopCmds.GETPAR("PL"+units+" 50"))
  #ampXCP0dB=float(TopCmds.GETPAR("PLdB 50"))
  SPX=TopCmds.GETPAR2("SPNAM 51")
  
  p90Y=float(TopCmds.GETPAR("P 21"))
  ampY=float(TopCmds.GETPAR("PL"+units+" 3"))
  ampYdB=float(TopCmds.GETPAR("PLdB 3"))
  
  ampYCP0=float(TopCmds.GETPAR("PL"+units+" 6"))
  ampYCP0dB=float(TopCmds.GETPAR("PLdB 6"))

  SPY="None"
  avgY0=1.  
  
  # Get the integration before possibly changing the shape.
  if SPX != "None" and SPX != None:
    avgX0=IntShape.Integrate(SPX)/100.
  if SPX == "None" or SPX == None:
    avgX0=1.

  CNCT=float(TopCmds.GETPAR("P 17"))


  #Interact with user about MAS and power levels, likely not needed
  params = TopCmds.INPUT_DIALOG("NCO CP MAS adjustment", "Nitrogen Carbonyl Cross Polarization", \
  ["Old MAS rate","New MAS rate","Old 13C power","Old 15N power","Contact Time(P16)","C-Ramp"],\
  [str(MAS0),str(MAS),str(ampXCP0),str(ampYCP0),str(CNCT),SPX],\
  ["kHz","kHz",units,units,"us",""],\
  ["1","1","1","1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)
  
  if params == None: TopCmds.EXIT()
  params.append(SPY)

  # Everything is written with dB, so we might have to convert
  if units == "W":
    params[2]=str(Setup.WtodB(float(params[2])))
    params[3]=str(Setup.WtodB(float(params[3])))

  if SPX != "None" and SPX != None:
    avgX0=IntShape.Integrate(SPX)/100.
  if SPX == "None" or SPX == None:
    avgX0=1.

  pulses=p90X,ampXdB,p90Y,ampYdB,avgX0,avgY0
  
  SelectorText="Adjust the NCA CP parameters:","Calculate New Power Level for:",\
  ["Carbon","Nitrogen","Both"]
  
  ampXCPdB, ampYCPdB = FindMatch(params,pulses,SelectorText)

  if units == "W":
    ampXCP=Setup.dBtoW(ampXCPdB)
    ampYCP=Setup.dBtoW(ampYCPdB)
  
  value = TopCmds.SELECT("Adjusting the NCO CP parameters:",\
  "This will set\n 13C power to:  " + str('%3.2f' %ampXCP)+ " "+units+"\n \
  15N power to:  " +str('%3.2f' %ampYCP) + " "+units,["Update", "Keep Previous"])
    
  if value != 1:
    TopCmds.PUTPAR("PLdB 51",str('%3.2f' %ampXCPdB))
    TopCmds.PUTPAR("SPdB 51",str('%3.2f' %ampXCPdB))
    TopCmds.PUTPAR("PLdB 6",str('%3.2f' %ampYCPdB))
    TopCmds.PUTPAR("P 17" ,str('%3.2f' %CNCT))
    TopCmds.PUTPAR("SPNAM 51",SPX)

def C72():
  
  oldC7=float(TopCmds.GETPAR("PLdB 17"))
  LoopC7=float(TopCmds.GETPAR("L 7"))
  
  index = TopCmds.INPUT_DIALOG("POST-C7 MAS", "POST-C7 changes for MAS change", \
  ["Old MAS rate","New MAS rate","Old 13C power","Mixing Loop (L7)"],\
  [str(MASR),str(MAS),str(ampC7),str(LoopC7)],\
  ["kHz","kHz","dB",""],\
  ["1","1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)
  
  OldMAS=float(index[0])
  NewMAS=float(index[1])
  oldC7=float(index[2])
  newL7 =float(index[3])

  adjust=20*(math.log10(NewMAS/OldMAS))
  newC7=oldC7-adjust
  TopCmds.PUTPAR("PLdB 17",str('%3.2f' %Condition))
  TopCmds.PUTPAR("L 7",str(14))
  
def SPC5():
  
  oldC5=float(TopCmds.GETPAR("PLdB 15"))
  LoopC5=float(TopCmds.GETPAR("L 5"))
  
  index = TopCmds.INPUT_DIALOG("SPC5 MAS", "SPC5_2,3 changes for MAS change", \
  ["Old MAS rate","New MAS rate","Old 13C power","Mixing Loop (L5)"],\
  [str(MASR),str(MAS),str(ampC5),str(LoopC5)],\
  ["kHz","kHz","dB",""],\
  ["1","1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)
  
  OldMAS=float(index[0])
  NewMAS=float(index[1])
  oldC5=float(index[2])
  newL5 =float(index[3])
 
  adjust=20*(math.log10(NewMAS/OldMAS))
  newC5=oldC5-adjust
  TopCmds.PUTPAR("PLdB 15",str('%3.2f' %newC5))
  TopCmds.PUTPAR("L 5",str(newL5))

def DREAM():
  
  oldCDREAM=float(TopCmds.GETPAR("PLdB 22"))
  RAMP=TopCmds.GETPAR("SPNAM5")
  #AvgAmpOld=IntShape.Integrate(RAMP)/100.
  
  index = TopCmds.INPUT_DIALOG("DREAM MAS", "DREAM changes for MAS change", \
  ["Old MAS rate","New MAS rate","Old 13C power","Mixing time (p20)","Ramp Name"],\
  [str(MASR),str(MAS),str(ampC5),str(LoopC5),RAMP],\
  ["kHz","kHz","dB",""],\
  ["1","1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)
  
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
  
  TopCmds.PUTPAR("PLdB 22",str('%3.2f' %newdB))
  TopCmds.PUTPAR("P  20",str('%3.2f' %newmix))
  TopCmds.PUTPAR("SPNAM5",RAMP)