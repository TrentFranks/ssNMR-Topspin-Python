"""
Module for a TANGENT pulse shape:
W.T. Franks FMP Berlin 
"""
import de.bruker.nmr.mfw.root as root

import math
import TopCmds
import sys
from sys import argv

cmds=argv
#TopCmds.MSG(str(cmds))

def dialog():
   MAS=float(TopCmds.GETPAR("CNST 31"))
   TauR=float(1000000/MAS)
   Data = TopCmds.INPUT_DIALOG("Tangent Ramp Input", "", \
   ["Scaling","steps","Ramp (Delta)","Adiabicity (Beta)"],\
   ["50","500","20","4"],\
   ["%","","%",""],\
   ["1","1","1","1"],\
   ["Accept","Close"], ['a','c'], 10)

   return Data

def name(input,SP):
   Name = str("TAN_" + input[2] + "D_" + input[3] + "B.wave") 
   
   Wave = str(TopCmds.INPUT_DIALOG("TAN ramp Files", "", ["C File = ","C Wave =",],\
   [Name,SP],["",""],["1","1"],["Accept","Close"], ['a','c'], 30))
   Files = Wave[27:len(Wave)-3]  #get rid of Java formatting
   
   #TopCmds.MSG(Wave)
   #TopCmds.MSG(Files)
   
   i = Files.find(",")
   File = Files[0:i-1]
   #TopCmds.MSG(File)
   SP = Files[i+4:]
   #TopCmds.MSG(SP)
   if SP.find("SPNAM ") >= 0:
     TopCmds.PUTPAR(str(SP),str(File))
   return File

def make(Name,Sc,Stps,Del,Be):
  import math
  ampl = [] #  normalized to 0...100
  ph = [] #  normalized to 0...100

  Scale=float(Sc)
  steps=int(Stps)
  Delta=float(Del)
  Beta =float(Be)
  
  pi = 3.14159265
  
  k=(steps-1)/2.0
  if Beta==0.:
    alpha=0.  #No division by Zero
  else:
    alpha=(2.0/(steps-1))*math.atan(Delta/Beta)
  absBeta=math.fabs(Beta)
  
  for i in range(steps):
      di=absBeta*math.tan(alpha*(float(i-k)))
      di=di
      ampl.append(Scale*(100.+di)/100.)
      ph.append(0.0)
  TopCmds.SAVE_SHAPE(Name, "NoRotation", ampl,ph)
