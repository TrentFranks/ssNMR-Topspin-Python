"""
Module for a TANGENT pulse shape:
W.T. Franks FMP Berlin 
"""
import de.bruker.nmr.mfw.root as root

import math
import TopCmds
import sys
from sys import argv

ret=u"\u000D"
spc=u"\u0020"

cmds=argv
#TopCmds.MSG(str(cmds))

def dialog():
   MAS =pul.GetPar('MAS',"")
   TauR=float(1000000/MAS)
   Data = TopCmds.INPUT_DIALOG("Tangent Ramp Input", "", \
   ["Scaling","steps","Ramp (Delta)","Adiabicity (Beta)"],\
   ["50","500","20","4"],\
   ["%","","%",""],\
   ["1","1","1","1"],\
   ["Accept","Close"], [spc,ret], 10)

   if Data == None:TopCmds.EXIT()

   return Data

def name(input,SP):
   Name = str("TAN_" + input[2] + "D_" + input[3] + "B.wave") 
   
   index = str(TopCmds.INPUT_DIALOG("TAN ramp Files", "", ["File = ","edWave =",],\
   [Name,SP],["",""],["1","1"],["Accept","Close"], [spc,ret], 30))
   
   File, SP = index
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
