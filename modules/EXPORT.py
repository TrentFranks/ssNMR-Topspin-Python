"""
Computes a topspin3.1 EXPORT wave shape:
A.N Neilsen, L.A. Strassø, A.J. Nieuwkoop, 
C.M. Rienstra, M. Bjerring and N.C. Nielsen 
J Phys Chem Lett 1952-1956 (2010) 

WTF Adapted this for topspin3.1 Python Interface 
from ANN tcl script provided from ANN and NCN
FMP Berlin and Aarhus University
"""

import de.bruker.nmr.mfw.root as root

#import os
import sys
from sys import argv
import TopCmds

ret=u"\u000D"
spc=u"\u0020"

def dialog():
   MAS=TopCmds.GETPAR("CNST 31")
   #MSG(MAS)
   input = TopCmds.INPUT_DIALOG("EXPORTinput", "", \
   ["13C field ","15N field ","MAS ", "steps in Export Element", "C(Ix+Sx)=CFx", "B Iy", "B Sy", "Initial Phase"],\
   ["50","50",str(MAS),"100", "7.0", "0.375", "0.625", "90"],\
   ["kHz","kHz","Hz","","","","",""],\
   ["1","1", "1", "1", "1", "1", "1", "1"],\
   ["Accept","Close"], [spc,ret], 10)

   if input == None:TopCmds.EXIT()
   return input

def name(input):
   Cname = str("EXPORT_C_C" + input[4] + "_B" + input[5] + "_MAS" + input[2] + "_np" + input[3] + ".wave") 
   Nname = str("EXPORT_N_C" + input[4] + "_B" + input[6] + "_MAS" + input[2] + "_np" + input[3] + ".wave") 
   Cwave = pul.pulDict['sCexp']
   Nwave = pul.pulDict['sNexp']
   
   Wave = str(INPUT_DIALOG("EXPORT Files", "", ["C File = ","C Wave =","N File = ","N Wave =",],\
   [Cname,Cwave,Nname,Nwave],["","","",""],["1","1","1","1"],["Accept","Close"], [spc,ret], 30))
   if wave == None:TopCmds.EXIT()
   Files = Wave[8:len(Wave)-21]  #get rid of Java formatting
   
   i = Files.find(",")
   ii = Files[i+3:].find(",")+3
   iii = Files[i+ii+3:].find(",")+3

   Cfile = Files[0:i-1]
   Cwave = Files[i+3:i+ii-1]
   Nfile = Files[i+ii+3:i+ii+iii-1]
   Nwave = Files[i+ii+iii+3:]

   #MSG( Cfile )
   #MSG( Cwave )
   #MSG( Nfile )
   #MSG( Nwave )
   
   pul.SetPar(str(Cwave),str(Cfile),"")
   pul.SetPar(str(Nwave),str(Nfile),"")
   
   return Cfile, Nfile

def make(input,Names):
  import math
  Iampl = [] #  normalized to 0...100
  Sampl = [] #  normalized to 0...100
  Iphases = [] # in degrees
  Sphases = [] # in degrees
  Names = []
  iph = [] # in degrees

  pi = 3.14159265
  NomRFI= float(input[0])
  NomRFS= float(input[1])
  MAS   = float(input[2])
  steps = int(input[3])
  CF= MAS*float(input[4])
  BI= MAS*float(input[5])
  BS= MAS*float(input[6])
  Iphase= float(input[7])
  
  duration = 2.0e06/MAS
  deltaT  = duration/steps
  RFImax= 0
  RFSmax= 0
  h=0-1
  
  for i in range(steps):
    j=i+1
    k=1+math.fmod(j-1,steps)
    if (k==1):h=-1*h
   
    ti = i*deltaT
    co = math.cos(2*pi*CF*ti*1.0e-6)
    si = math.sin(2*pi*CF*ti*1.0e-6)
   
    #RF part
    RFIx = CF*(h)
    RFIy = BI*co
    RFSx = CF*(h)
    RFSy = BS*co
   
    RFI = math.sqrt(RFIx*RFIx+RFIy*RFIy)
    RFS = math.sqrt(RFSx*RFSx+RFSy*RFSy)
   
    if RFI > RFImax:
      RFImax = RFI
    if RFS > RFSmax:
      RFSmax = RFS
    if RFImax > (NomRFI*1000):
      TopCmds.ERRMSG(message="ERROR the maximum RF is above the nominal RF",\
      title="WAVE ERROR")
   
    if RFSmax > (NomRFS*1000):
      TopCmds.ERRMSG(message="ERROR the maximum RF is above the nominal RF",\
      title="WAVE ERROR")
    
    #Phase Part
    
    Iphcor=Iphase+BI*h*(co-1)/(CF)
    Sphcor=BS*h*(co-1)/(CF)
    
    Iph=(Iphcor+math.atan2(RFIy,RFIx))*180/pi
    Sph=(Sphcor+math.atan2(RFSy,RFSx))*180/pi
    
    if(Iph >= 0.0):
      Inph = int(Iph/360.0)
      Iph_int = Iph - (Inph)*360
    else:
      Inph = int(Iph/360.0)
      Iph_int = Iph - (Inph-1)*360
     
    if(Sph >= 0.0):
      Snph = int(Sph/360.0)
      Sph_int = Sph - (Snph)*360
    else:
      Snph = int(Sph/360.0)
      Sph_int = Sph - (Snph-1)*360
    Iampl.append(RFI/NomRFI/10)
    Sampl.append(RFS/NomRFS/10)
    Iphases.append(Iph_int)
    Sphases.append(Sph_int)

  TopCmds.SAVE_SHAPE(Names[0], "Excitation", Iampl, Iphases)
  TopCmds.SAVE_SHAPE(Names[1], "Excitation", Sampl, Sphases)
