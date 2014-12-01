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

def name_confirm():
   adbname=(TopCmds.GETPAR("SPNAM 9"))
   SP="SPNAM 9"
   if adbname == "gauss" : adbname = "TanhTan"
   
   Wave = str(TopCmds.INPUT_DIALOG("Adiabatic TOBSY", "",\
   ["SP File = ","SP Wave =",],\
   [adbname,SP],["",""],["1","1"],["Accept","Close"], ['a','c'], 30))
   Files = Wave[8:len(Wave)-21]  #get rid of Java formatting
   
   i = Files.find(",")
   File = Files[0:i-1]
   SP = Files[i+3:]
   TopCmds.PUTPAR("SPNAM9",str(File))
   return File

def CalC931_TOBSY():
   p90C=float(TopCmds.GETPAR("P 1"))
   ampC=float(TopCmds.GETPAR("PLdB 1"))
   MAS =float(TopCmds.GETPAR("CNST 31"))
   Loop=float(TopCmds.GETPAR("L 9"))
   if Loop == 0: Loop = 25
   
   MaxB1 = 1000000./4./p90C
   C9B1  = 6.0*MAS
   adjust=20*(math.log10(C9B1/MaxB1))
   condition=ampC-adjust
   TopCmds.PUTPAR("PLdB 29",str('%3.2f' %condition))
   TopCmds.PUTPAR("L 9",str(Loop))

def CalC961_TOBSY():
   p90C=float(TopCmds.GETPAR("P 1"))
   ampC=float(TopCmds.GETPAR("PLdB 1"))
   MAS =float(TopCmds.GETPAR("CNST 31"))
   Loop=float(TopCmds.GETPAR("L 9"))
   if Loop == 0: Loop = 25
   
   MaxB1 = 1000000./4./p90C
   C9B1  = 3.0*MAS
   adjust=20*(math.log10(C9B1/MaxB1))
   condition=ampC-adjust
   TopCmds.PUTPAR("PLdB 29",str('%3.2f' %condition))
   TopCmds.PUTPAR("L 9",str(Loop))


def CalC542_adb_TOBSY():
   p90C=float(TopCmds.GETPAR("P 1"))
   ampC=float(TopCmds.GETPAR("PLdB 1"))
   MAS =float(TopCmds.GETPAR("CNST 31"))
   
   RAMP=TopCmds.GETPAR("SPNAM 5")
   AvgAmp=IntShape.Integrate(RAMP)/100.
   
   MaxB1 = 1000000./4./p90C
   C542B1= MAS*0.8/AvgAmp
   
   #TopCmds.MSG("C542B1 adiabatic pulse amplitude: "+str(C542B1))
   
   adjust=20*(math.log10(C542B1/MaxB1))
   condition=ampC-adjust
   TopCmds.PUTPAR("PLdB 5",str('%3.2f' %condition))
   TopCmds.PUTPAR("L 5",str(1))
