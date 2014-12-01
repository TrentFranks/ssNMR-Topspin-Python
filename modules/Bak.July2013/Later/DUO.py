"""
Computes a topspin3.1 DUO wave shape:
L.A. Strassø and N.C. Nielsen
J Chem Phys 133 064501 (2010) 

WTF Adapted this for topspin3.1 Python Interface 
from LAS tcl script provided from Anders B. Nielsen and NCN
FMP Berlin and Aarhus University
"""
import de.bruker.nmr.mfw.root as root

#import os
import sys
from sys import argv
import TopCmds

def dialog():
   input = TopCmds.INPUT_DIALOG("DUOinput", "", \
   ["RF field = ", "MAS = ","steps" ,"B = ", "C = "], \
   ["100","10000","100","3.5","0.5"],\
   ["kHz","Hz","","lit=3.5","lit=0.5",], ["1", "1", "1", "1", "1"],\
   ["Accept","Close"], ['a','c'],10)
   return input

def name(input):
   name = str("DUO_C" + input[4] + "_B" + input[3] + "_MAS" + input[1] + "_np" + input[2] + ".wave") 
   Wavename = str(TopCmds.INPUT_DIALOG("DUO File", "", ["Filename = "],[name],[""],["1"],["Accept","Close"], ['a','c'], 30))

   Filename = Wavename[8:len(Wavename)-21]  #get rid of Java formatting
   #MSG( Filename + ' \n is the file name')
   return Filename

def make(input,name):
   import math
   amplitudes = [] #  normalized to 0...100
   phases = [] # in degrees

   pi = 3.14159265
   NomRF = float(input[0])
   MAS   = float(input[1])
   steps = int(input[2])
   DUO_B = MAS*float(input[3])
   DUO_C = MAS*float(input[4])
   duration = 2.0e06/MAS
   deltaT  = duration/steps
   RFmax = 0

   for i in range(steps):
      ti = i*deltaT
      co = math.cos(2*pi*DUO_C*ti*1.0e-6)
      si = math.sin(2*pi*DUO_C*ti*1.0e-6)

   # Calculate RF portion
      rf1 = DUO_C
      rf2 = -1.0*DUO_B*si
 
      rf = math.sqrt(rf1*rf1 + rf2*rf2)
      if rf > RFmax:
         RFmax = rf

   # Calculate Phase Portion
      phcor = -1*DUO_B*si/DUO_C
      ph    = (math.atan2(rf2,rf1)+phcor)*180/pi
      if ph >= 0.0:
         nph = int(ph/360.0)
         phint = ph-(nph)*360
      else:
         nph = int(ph/360.0)
         phint = ph-(nph-1)*360
      if RFmax > (NomRF*1000):
         TopCmds.ERRMSG(message="ERROR the maximum RF is above the nominal RF",title="WAVE ERROR")
   amplitudes.append(rf/NomRF/10)
   phases.append(phint)
   TopCmds.SAVE_SHAPE(name, "Excitation", amplitudes, phases)
   return
