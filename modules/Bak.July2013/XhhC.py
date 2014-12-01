"""
Modules to Set default parameters:
W.T. Franks FMP Berlin
"""
import de.bruker.nmr.mfw.root as root

import math
import TopCmds
import IntShape
import Setup

p90H=2.5
ampH=4.0
p90C=3.0
ampC=0.0
p90N=5.0
ampN=-2.0
MAS =10000.0

def CH(units):
  #48,49
  p90H=float(TopCmds.GETPAR("P 3"))
  ampH=float(TopCmds.GETPAR("PLdB 2"))
  p90C=float(TopCmds.GETPAR("P 1"))
  ampC=float(TopCmds.GETPAR("PLdB 1"))
  MAS =float(TopCmds.GETPAR("CNST 31"))

  SPH =TopCmds.GETPAR2("SPNAM 48")
  SPH0=TopCmds.GETPAR2("SPNAM 40")

  CNCT =float(TopCmds.GETPAR("P 48"))
  CNCT0=float(TopCmds.GETPAR("P 15"))
  
  MaxB1H=1000000./4./p90H
  MaxB1C=1000000./4./p90C

  if CNCT  <=   1.00  : CNCT = CNCT0

  if SPH == "gauss" or SPH == "None" or SPH == "" :
    SPH = SPH0
    TopCmds.PUTPAR("SPNAM 48",SPH)
    TopCmds.XCMD("spnam48")
    SPH=(TopCmds.GETPAR2("SPNAM 48"))
    SPH.join()

  Hav  = IntShape.Integrate(SPH)
  Hav0 = IntShape.Integrate(SPH0)
  Hint = 0.01*((Hav)**2)/Hav0
  #TopCmds.MSG("Hint "+str(Hint))

  Hamp0=float(TopCmds.GETPAR("SPdB 40"))
  Camp0=float(TopCmds.GETPAR("SPdB 41"))

  B1H = MaxB1H*Hint*math.pow(10,(ampH-Hamp0)/20.)
  B1C = MaxB1C*math.pow(10,(ampC-Camp0)/20.)

  index = TopCmds.INPUT_DIALOG("C-H CP", "Contact and Ramp", \
  ["Proton B1 Field","H Ramp","Carbon B1 Field","Contact Time(P48)"],\
  [str('%3.0f' %B1H),SPH,str('%3.0f' %B1C),str(CNCT)],\
  ["kHz","","kHz","us"],\
  ["1","1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)

  SP=index[1]
  CNCT=float(index[3])

  adjust=20*(math.log10(float(index[0])/MaxB1H))
  Hamp1 = ampH-adjust
  AvgAmp=IntShape.Integrate(index[1])/100.
  adjust=20*(math.log10(1./AvgAmp))
  Hamp = Hamp1-adjust

  adjust=20*(math.log10(float(index[2])/MaxB1C))
  Camp = ampC-adjust

  if units == "W":
    Hamp=dBtoW(Hamp)
    Camp=dBtoW(Camp)
  
  value = TopCmds.SELECT("Adjusting the CH CP parameters:",\
  "This will set\n 1H power to:  " + str('%3.2f' %Hamp)+" "+ units+"\n \
  13C power to:  " +str('%3.2f' %Camp) + units,["Update", "Keep Previous"])

  if value != 1:
    TopCmds.PUTPAR("SP"+units+" 48",str('%3.2f' %Hamp))
    TopCmds.PUTPAR("SP"+units+" 49",str('%3.2f' %Camp))
    TopCmds.PUTPAR("PL"+units+" 48",str('%3.2f' %Hamp))
    TopCmds.PUTPAR("PL"+units+" 49",str('%3.2f' %Camp))
    TopCmds.PUTPAR("P 48"   ,str('%3.2f' %CNCT))
    TopCmds.PUTPAR("SPNAM 48",SP)
	
def HC(units):
  #44,45
  p90H=float(TopCmds.GETPAR("P 3"))
  ampH=float(TopCmds.GETPAR("PLdB 2"))
  p90C=float(TopCmds.GETPAR("P 1"))
  ampC=float(TopCmds.GETPAR("PLdB 1"))
  MAS =float(TopCmds.GETPAR("CNST 31"))

  SPH =TopCmds.GETPAR2("SPNAM 44")
  SPH0=TopCmds.GETPAR2("SPNAM 40")

  CNCT =float(TopCmds.GETPAR("P 44"))
  CNCT0=float(TopCmds.GETPAR("P 15"))
  
  MaxB1H=1000000./4./p90H
  MaxB1C=1000000./4./p90C

  if CNCT  <=   1.00  : CNCT = CNCT0

  if SPH == "gauss" or SPH == "None" or SPH == "" :
    SPH = SPH0
    TopCmds.PUTPAR("SPNAM 44",SPH)
    TopCmds.XCMD("spnam44")
    SPH=(TopCmds.GETPAR2("SPNAM 44"))
    SPH.join()

  Hav  = IntShape.Integrate(SPH)
  Hav0 = IntShape.Integrate(SPH0)
  Hint = 0.01*((Hav)**2)/Hav0
  #TopCmds.MSG("Hint "+str(Hint))

  Hamp0=float(TopCmds.GETPAR("SPdB 40"))
  Camp0=float(TopCmds.GETPAR("SPdB 41"))

  B1H = MaxB1H*Hint*math.pow(10,(ampH-Hamp0)/20.)
  B1C = MaxB1C*math.pow(10,(ampC-Camp0)/20.)

  index = TopCmds.INPUT_DIALOG("H-C CP", "Contact and Ramp", \
  ["Proton B1 Field","H Ramp","Carbon B1 Field","Contact Time(P44)"],\
  [str('%3.0f' %B1H),SPH,str('%3.0f' %B1C),str(CNCT)],\
  ["kHz","","kHz","us"],\
  ["1","1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)

  SP=index[1]
  CNCT=float(index[3])

  adjust=20*(math.log10(float(index[0])/MaxB1H))
  Hamp1 = ampH-adjust
  AvgAmp=IntShape.Integrate(index[1])/100.
  adjust=20*(math.log10(1./AvgAmp))
  Hamp = Hamp1-adjust

  adjust=20*(math.log10(float(index[2])/MaxB1C))
  Camp = ampC-adjust

  if units == "W":
    Hamp=Setup.dBtoW(Hamp)
    Camp=Setup.dBtoW(Camp)
    
  value = TopCmds.SELECT("Adjusting the CH CP parameters:",\
  "This will set\n 1H power to:  " + str('%3.2f' %Hamp)+" "+units+"\n \
  13C power to:  " +str('%3.2f' %Camp) + units,["Update", "Keep Previous"])

  if value != 1:
    TopCmds.PUTPAR("SP"+units+" 44",str('%3.2f' %Hamp))
    TopCmds.PUTPAR("SP"+units+" 45",str('%3.2f' %Camp))
    TopCmds.PUTPAR("PL"+units+" 44",str('%3.2f' %Hamp))
    TopCmds.PUTPAR("PL"+units+" 45",str('%3.2f' %Camp))
    TopCmds.PUTPAR("P 44"   ,str('%3.2f' %CNCT))
    TopCmds.PUTPAR("SPNAM 44",SP)
	

def NH(units):
  #46,47
  p90H=float(TopCmds.GETPAR("P 3"))
  ampH=float(TopCmds.GETPAR("PLdB 2"))
  p90C=float(TopCmds.GETPAR("P 1"))
  ampC=float(TopCmds.GETPAR("PLdB 3"))
  MAS =float(TopCmds.GETPAR("CNST 31"))

  SPH =TopCmds.GETPAR2("SPNAM 46")
  SPH0=TopCmds.GETPAR2("SPNAM 40")

  CNCT =float(TopCmds.GETPAR("P 46"))
  CNCT0=float(TopCmds.GETPAR("P 15"))
  
  MaxB1H=1000000./4./p90H
  MaxB1C=1000000./4./p90C

  if CNCT  <=   1.00  : CNCT = CNCT0

  if SPH == "gauss" or SPH == "None" or SPH == "" :
    SPH = SPH0
    TopCmds.PUTPAR("SPNAM 46",SPH)
    TopCmds.XCMD("spnam46")
    SPH=(TopCmds.GETPAR2("SPNAM 46"))
    SPH.join()

  Hav  = IntShape.Integrate(SPH)
  Hav0 = IntShape.Integrate(SPH0)
  Hint = 0.01*((Hav)**2)/Hav0
  #TopCmds.MSG("Hint "+str(Hint))

  Hamp0=float(TopCmds.GETPAR("SPdB 42"))
  Camp0=float(TopCmds.GETPAR("SPdB 43"))

  B1H = MaxB1H*Hint*math.pow(10,(ampH-Hamp0)/20.)
  B1C = MaxB1C*math.pow(10,(ampC-Camp0)/20.)

  index = TopCmds.INPUT_DIALOG("N-H CP", "Contact and Ramp", \
  ["Proton B1 Field","H Ramp","Nitrogen B1 Field","Contact Time(P46)"],\
  [str('%3.0f' %B1H),SPH,str('%3.0f' %B1C),str(CNCT)],\
  ["kHz","","kHz","us"],\
  ["1","1","1","1"],\
  ["Accept","Close"], ['a','c'], 10)

  SP=index[1]
  CNCT=float(index[3])

  adjust=20*(math.log10(float(index[0])/MaxB1H))
  Hamp1 = ampH-adjust
  AvgAmp=IntShape.Integrate(index[1])/100.
  adjust=20*(math.log10(1./AvgAmp))
  Hamp = Hamp1-adjust

  adjust=20*(math.log10(float(index[2])/MaxB1C))
  Camp = ampC-adjust

  if units == "W":
    Hamp=Setup.dBtoW(Hamp)
    Camp=Setup.dBtoW(Camp)
  
  
  value = TopCmds.SELECT("Adjusting the NH CP parameters:",\
  "This will set\n 1H power to:  " + str('%3.2f' %Hamp)+ " "+units+"\n \
  15N power to:  " +str('%3.2f' %Camp) + units,["Update", "Keep Previous"])

  if value != 1:
    TopCmds.PUTPAR("SP"+units+" 46",str('%3.2f' %Hamp))
    TopCmds.PUTPAR("SP"+units+" 47",str('%3.2f' %Camp))
    TopCmds.PUTPAR("PL"+units+" 46",str('%3.2f' %Hamp))
    TopCmds.PUTPAR("PL"+units+" 47",str('%3.2f' %Camp))
    TopCmds.PUTPAR("P 46"   ,str('%3.2f' %CNCT))
    TopCmds.PUTPAR("SPNAM 44",SP)
	