"""
Modules to Set default parameters:
W.T. Franks FMP Berlin
"""
import de.bruker.nmr.mfw.root as root
import de.bruker.nmr.prsc.toplib as top
import os
import sys

sys.path.append(root.UtilPath.getTopspinHome()+ '/exp/stan/nmr/py/BioPY/modules/')

import TopCmds
import math
import Setup

import FREQ as fq
import GetNUCs as NUC

from GetLib import pul
from sys import argv

WAIT_TILL_DONE = 1;

Nucs=NUC.list()

deg=u"\u00b0"
ret=u"\u000D"
spc=u"\u0020"
unb=u"\u005f"
crt=u"\u005e"

class FSLG:
  def __init__(self,units):
    self.units = units
    self.mul   = pul.GetPar('lFSLG',"")
    self.pFLSG = pul.GetPar('pFSLG',"")
    self.B1cntr= pul.GetPar('fFSLG',"")
    self.pMAX  = pul.GetPar('pH90',"")
    self.aMAX  = pul.GetPar('aH',self.units)  
    self.MAS   = pul.GetPar('MAS',"")
    self.offs  = pul.GetPar('oFSLGc',"")
      
  def ByPulse(self):
    """
    Useful for rotor synchronizing
    """
    
    pulse=1000000.*math.sqrt(2./3.)/self.B1cntr
  
    Title ="Frequency Switched Lee-Goldburg (FSLG)"
    Sutit ="Known Lee-Golberg Pulse"
    Label =["LG Pulse","Center Shift","Increment Multiplier"]
    Values=[str('%.2f' %pulse),str(self.offs/1000.),str(self.mul)]
    Units =["us","kHz",""]
    Window=["1","1","1"]
  
    confirm = 1
    while confirm == 1:
      index=TopCmds.INPUT_DIALOG(Title,Sutit,Label,\
        Values,Units,Window,["Accept","Close"], [spc,ret], 10)

      if index==None: TopCmds.EXIT()
    
      pulse= float(index[0])
      shift=1000*float(index[1])
      Mult = float(index[2])
      
      B1   = 1000.*math.sqrt(2./3.)/pulse
      
      #TopCmds.MSG(str(B1))
      confirm=self.Check(B1,shift,Mult)
    
    self.CalAndSet(B1,shift,Mult)
      
  def ByField(self):
    
    Title ="Frequency Switched Lee-Goldburg (FSLG)"
    Sutit ="Lee-Golberg Field"
    Label =["LG Field","Center Shift","Increment Multiplier"]
    Values=[str(self.B1cntr/1000.),str((self.offs)/1000.),str(self.mul)]
    Units =["kHz","kHz",""]
    Window=["1","1","1"]
  
    confirm = 1
    while confirm == 1:
      index=TopCmds.INPUT_DIALOG(Title,Sutit,Label,\
        Values,Units,Window,["Accept","Close"], [spc,ret], 10)

      if index==None: TopCmds.EXIT()
    
      B1   = float(index[0])
      shift= 1000*float(index[1])
      Mult = float(index[2])
      
      confirm=self.Check(B1,shift,Mult)
    
    self.CalAndSet(B1,shift,Mult)
  
  def ByAmpl(self):
    p90=pul.GetPar('pH90',"")
    amp=pul.GetPar('aH',self.units)  
  
    if self.units == "W":
      amp=Setup.WtodB(amp)  

    MaxB1 = 1000000./4./p90
    aFSLG = pul.GetPar('aHfslg',"dB")
    #Convert amplitude to field

    B1=MaxB1*(math.pow(10,(amp-aFSLG)/20.))/1000.
    if B1 > 1.         : B1out='% .3f' % B1
    if B1 > MaxB1/1000.: B1out='% .3f' % (MaxB1/1000.)
    if B1 <= 1.        : B1out='% .3f' % (MaxB1/1000.)
    B1   = float(B1out)
   
    Title ="Frequency Switched Lee-Goldburg (FSLG)"
    Sutit ="Lee-Golberg Feild Amplitude"
    Label =["LG Field","Center Shift","Increment Multiplier"]
    Values=[str(B1),str((self.offs)/1000.),str(self.mul)]
    Units =["kHz","kHz",""]
    Window=["1","1","1"]
  
    confirm = 1
    while confirm == 1:
      index=TopCmds.INPUT_DIALOG(Title,Sutit,Label,\
        Values,Units,Window,["Accept","Close"], [spc,ret], 10)

      if index==None: TopCmds.EXIT()
    
      B1   = float(index[0])
      shift=1000*float(index[1])
      Mult = float(index[2])
    
      confirm=self.Check(B1,shift,Mult)
    
    self.CalAndSet(B1,shift,Mult)
    return
 
  def BySW(self):
    
    #pulse=1000000.*math.sqrt(1.5)/self.B1cntr
    pulse=1000000./self.B1cntr
    sw   = self.mul*250000./pulse   #in Hz

    Title ="Frequency Switched Lee-Goldburg (FSLG)"
    Sutit ="Desired Lee-Golberg Sweep Width"
    Label =["LG SW","Center Shift","Increment Multiplier"]
    Values=[str('%.2f' %sw),str((self.offs)/1000.),str(self.mul)]
    Units =["Hz","kHz",""]
    Window=["1","1","1"]
  
    confirm = 1
    while confirm == 1:
      index=TopCmds.INPUT_DIALOG(Title,Sutit,Label,\
        Values,Units,Window,["Accept","Close"], [spc,ret], 10)
      if index==None: TopCmds.EXIT()
    
      sw   = float(index[0])
      shift=1000*float(index[1])
      Mult = float(index[2])
      
      pulse= 1000000./(4.*Mult*sw)
      
      B1   = 1000.*math.sqrt(2./3.)/pulse
      
      confirm=self.Check(B1,shift,Mult)
    
    self.CalAndSet(B1,shift,Mult)
    return
    
  def Check(self,B1,shift,Mult):
           
    B1LG = B1/math.sqrt(2.)
    B1eff= B1*math.sqrt(3./2.)
    field= int(1000*B1)
    pulse= 1000./B1eff
    sw   = 1000000./(4.*Mult*pulse)
    
    confirm=TopCmds.SELECT("Adjusting the 1H FSLG Parameters",\
        "The sweep width is: "+ str('%.3f' %sw) + " Hz\n"+\
        "The FSLG offset is:  " + str('%.3f' %B1LG) +" kHz\n"+\
        "The effective FSLG decoupling is:  " + str('%.3f' %B1eff) +" kHz\n"+\
        "The Applied Field is: " + str('%.3f' %B1) +" kHz\n"+\
        "The shift from center is: "+str(shift/1000.)+" kHz",\
        ["Continue", "Retry"],[spc,ret])
    
    return confirm
  
  def CalAndSet(self,B1,shift,Mult):
    p90=pul.GetPar('pH90',"")
    amp=pul.GetPar('aH','dB') 
    MaxB1 = 1000000./4./p90
    field= int(1000*B1)
    
    B1eff= B1*math.sqrt(3./2.)
    sw=Mult*250.*B1*math.sqrt(1.5)
    pulse= 1000./B1eff
    
    
    Hamp=Setup.DecSafely(B1*1000,'aHfslg',MaxB1,150000,amp,"dB")
    offsp=field/math.sqrt(2)+shift+2000.
    offsm=field/math.sqrt(2)-shift+2000.
  
    if self.units == "W":
      Hamp=Setup.dBtoW(Hamp)  

    value= TopCmds.SELECT("FSLG parameters set to:",\
      "1H power ("+ pul.pulDict['aHfslg'] +") to:  "+ str('%.2f' %Hamp)+" "+ self.units+"\n"+\
      "Applied field ("+ pul.pulDict['fFSLG'] + ") to:  "+ str('%.2f' %B1)+" kHz\n"+\
      "Sweep width (1/in0) to: "+ str('%.2f' %sw)+" Hz\n"+\
      "FSLG pulse ("+ pul.pulDict['pFSLG'] + ") to:  "+ str('%.2f' %pulse)+" us\n"+\
      "1H center shift ("+ pul.pulDict['oFSLGc'] + ") to:  "+ str('%.2f' %shift)+" Hz\n"+\
      "positive offset ("+ pul.pulDict['oFSLGp'] + ") to:  "+ str('%.2f' %offsp)+" Hz\n"+\
      "negative offset (-"+ pul.pulDict['oFSLGm'] + ") to:  "+ str('%.2f' %offsm)+" Hz\n"\
      ,["Update", "Keep Previous"])

    if value != 1:
      pul.SetPar('aHfslg',Hamp,self.units)
      pul.SetPar('fFSLG',1000.*float(B1),"")
      pul.SetPar('IN 0',0.000004*Mult*pulse,"")
      pul.SetPar('pFSLG',pulse,"")
      pul.SetPar('oFSLGc',shift,"")
      pul.SetPar('oFSLGp',offsp,"")
      pul.SetPar('oFSLGm',offsm,"")

    return
  
def pulses():
  pMA =pul.GetPar('pH90')*547./900.
  pcMA=pul.GetPar('pH90')*353./900.
  pul.SetPar('pHMA',pMA,"")
  pul.SetPar('pHcMA',pcMA,"")
  
  return

def HC(units):
  """
  Normal Hartmann-Hahn procedure adjusted for LG (see Setup module), 
  """

  Title="HC LG-CP Input"; SuTit="Proton Carbon Lee-Goldburg Cross Polarization"
  Label=["Proton B1 Field","H Ramp","Carbon B1 Field","C Ramp",\
         "Contact Time ("+str(pul.pulDict['pHCLG'])+")"]
  In  =Title,SuTit,Label
  
  Title="Adjusting the HC CP parameters:"; Label="1H","13C"
  Out =Title,Label

  Setup.CalCP('pH90','pC90','aHhcLG','aChcLG','empty','pHCLG','sHhc','sChc',"HX","LG"\
    ,units,'oHhcLG',In,Out)

  return
  
def HN(units):
  """
  Normal Hartmann-Hahn procedure adjusted for LG (see Setup module), 
  """

  Title="HN LG-CP Input"; SuTit="Proton Nitrogen Lee-Goldburg Cross Polarization"
  Label=["Proton B1 Field","H Ramp","Nitrogen B1 Field","N Ramp",\
         "Contact Time ("+str(pul.pulDict['pHNLG'])+")"]
  In  =Title,SuTit,Label
  
  Title="Adjusting the HN CP parameters:"; Label="1H","15N"
  Out =Title,Label

  Setup.CalCP('pH90','pN90','aHhnLG','aNhnLG','empty','pHNLG','sHhn','sNhn',"HX","LG"\
    ,units,'oHhnLG',In,Out)

  return
  
