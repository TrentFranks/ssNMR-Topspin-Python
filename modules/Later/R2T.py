"""
Module for a R2T pulse shape:
W.T. Franks FMP Berlin
"""
import de.bruker.nmr.mfw.root as root

#import os
import sys
from sys import argv
import TopCmds
import math

def dialog():
   MAS=float(TopCmds.GETPAR("CNST 31"))
   TauR= float(1000000/MAS)
   input = TopCmds.INPUT_DIALOG("R2T input", "", \
   ["Nominal RF ampl","MAS","R2T duration","RI,RO duration","steps","Ramp","I offset","S offset"],\
   ["85",str('%.0f' % MAS),"1.5",str( '%3.2f' % (TauR)),"1000","20","8.000","6.000"],\
   ["kHz"," Hz","ms","us","","+/- %","kHz","kHz"],\
   ["1","1","1","1","1","1","1","1"],\
   ["Accept","Close"], ['a','c'], 10)

   return  input

def name_no_confirm(input,Name,SP):
   if Name=="":
      Name = str("R2T_" + input[1] + "MAS_" + input[6] + "I_" + input[7] + "S.wave") 
   if SP=="":
      SP = str("SPNAM18")
      TopCmds.PUTPAR(str(SP),str(File))
   return Name, SP
   
def name_confirm(input):
   Name = str("R2T_" + input[1] + "MAS_" + input[6] + "I_" + input[7] + "S.wave") 
   SP = str("SPNAM18")
   Wave = str(TopCmds.INPUT_DIALOG("R2T Files", "", ["C File = ","C Wave =",],\
   [Name,SP],["",""],["1","1"],["Accept","Close"], ['a','c'], 30))
   Files = Wave[8:len(Wave)-21]  #get rid of Java formatting
   
   i = Files.find(",")
   File = Files[0:i-1]
   SP = Files[i+3:]
   TopCmds.PUTPAR(str(SP),str(File))
   return File, SP

def find_match(input):
  import math
  NomRF = 1000*float(input[0])
  MAS   = float(input[1])
  Ioffs = 1000*float(input[6])
  Soffs = 1000*float(input[7])
  
  m=1
  Match=m*MAS-Ioffs-Soffs
  if Match<0:
     m=2
     Match=m*MAS-Ioffs-Soffs
  if Match<0:
	  TopCmds.MSG("Cannot find match conditions, spinning too slowly")
	  TopCmds.EXIT()
  found=0
  for n in range(10000):
    WIeff = math.sqrt(Ioffs*Ioffs+float(n*n))
    WSeff = math.sqrt(Soffs*Soffs+float(n*n))
    Match=(m*MAS)-WIeff-WSeff
    #mm is the amplitude in Hz
    if Match > 0.0: mm=n
    if Match < 0.0: found=1
  
  if found==0:
	  TopCmds.MSG("Match condition not found within 10kHz, aborting")
	  TopCmds.EXIT()
  YorN=TopCmds.SELECT("Scaling", "The match condition is around %i Hz \n\n Which scaling should be used?" % mm , ["Calibration", "0.5" , "None(1.0)"])
#  CONFIRM("Scale Shape Pulse for Match","The amplitude should be approximately %i Hz \n \nUse scaling?" % Match)
  if YorN < 0: Scale=1.0
  if YorN == 0: Scale=float(Match)/NomRF
  if YorN == 1: Scale=0.5
  if YorN == 2: Scale=1.0
  return Scale

def make(Scale,input,name):
  import math
  ampl = [] #  normalized to 0...100
  ph = [] #  normalized to 0...100
  
  pi = 3.14159265
  
  durat = 1000*float(input[2])
  RIRO  = float(input[3])
  steps = int(input[4])
  Delta = float(input[5])
  
  RIOsteps = int(steps*RIRO/durat)
  Start=100.0-(Delta)
  End=100.0+(Delta)
  
  for i in range(steps):
    if i < RIOsteps:
      RF=1.0*i*Start/RIOsteps
    if i >= RIOsteps:
      RF=1.0*Start+(i-RIOsteps)*(End-Start)/(steps-(2*RIOsteps))
    if i > (steps-RIOsteps):
      RF=1.0*End-(i-steps+RIOsteps)*End/RIOsteps
    ampl.append(Scale*RF)
    ph.append(0.0)
  TopCmds.SAVE_SHAPE(name[0], "NoRotation", ampl,ph)
  