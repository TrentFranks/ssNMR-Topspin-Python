"""
Modules to Set default parameters:
W.T. Franks FMP Berlin
"""
import de.bruker.nmr.mfw.root as root

import math
#import os
import sys
import TopCmds
import IntShape
import CPDtools

ret=u"\u000D"
spc=u"\u0020"

def name_confirm():
   adbname=pul.GetPar('sCadb',"")
   if adbname == "gauss" : adbname = "TanhTan"

   SP=pul.pulDict['sCadb']
   
   Wave = str(TopCmds.INPUT_DIALOG("Adiabatic TOBSY", "",\
   ["SP File = ","SP Wave =",],\
   [adbname,SP],["",""],["1","1"],["Accept","Close"], [spc,ret], 30))
   
   if Wave == None:TopCmds.EXIT()

   Files = Wave[8:len(Wave)-21]  #get rid of Java formatting
   
   i = Files.find(",")
   File = Files[0:i-1]
   SP = Files[i+3:]
   pul.SetPar(SP,str(File),"")
   pul.SetPar('sCadb',File,"")

def CalC931_TOBSY(units):
   p90C=pul.GetPar('pC90',"")
   ampC=pul.GetPar('aC',units)
   MAS =pul.GetPar('MAS',"")
   Loop=pul.GetPar('lTOBSY',"")
   if Loop == 0: Loop = 25
   
   if units == "W":
     ampC=WtodB(ampC)

   MaxB1 = 1000000./4./p90C
   C9B1  = 6.0*MAS
   adjust=20*(math.log10(C9B1/MaxB1))
   condition=ampC-adjust

   if units == "W":
     condition=dBtoW(condition)
   
   pul.SetPar('aCc9',condition,"units")
   Loop=pul.GetPar('lTOBSY',Loop,"")

def CalC961_TOBSY(unit):
   p90C=pul.GetPar('pC90',"")
   ampC=pul.GetPar('aC',units)
   MAS =pul.GetPar('MAS',"")
   Loop=pul.GetPar('lTOBSY',"")
   if Loop == 0: Loop = 25
   
   if units == "W":
     ampC=WtodB(ampC)

   MaxB1 = 1000000./4./p90C
   C9B1  = 3.0*MAS
   adjust=20*(math.log10(C9B1/MaxB1))
   condition=ampC-adjust

   if units == "W":
     condition=dBtoW(condition)
   
   pul.SetPar('aCc9',condition,"units")
   Loop=pul.GetPar('lTOBSY',Loop,"")

def CalC542_adb_TOBSY():
   p90C=pul.GetPar('pC90',"")
   ampC=pul.GetPar('aC',units)
   MAS =pul.GetPar('MAS',"")
   SP = pul.GetPar('sCabd',"")
   Loop=pul.GetPar('lTOBSY',"")
   AvgAmp=IntShape.Integrate(RAMP)/100.

   if Loop == 0: Loop = 25
   
   if units == "W":
     ampC=WtodB(ampC)

   MaxB1 = 1000000./4./p90C
   C542B1= MAS*0.8/AvgAmp

   adjust=20*(math.log10(C542B1/MaxB1))
   condition=ampC-adjust

   if units == "W":
     condition=dBtoW(condition)
   
   pul.SetPar('aCadb',condition,"units")
   Loop=pul.GetPar('lTOBSY',Loop,"")
