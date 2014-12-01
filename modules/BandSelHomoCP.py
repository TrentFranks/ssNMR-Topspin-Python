"""
Band Selective Homonuclear CP calculator
Created on 22.05.2014
Modified 02.07.2014 W.T. Franks FMP Berlin

@author: Venita Daebel
@copyright: Bruker Biospin Corporation
"""
# Import Important stuff

import de.bruker.nmr.mfw.root as root

import os, re, string, math, sys, copy
sys.path.append(root.UtilPath.getTopspinHome()+ '/exp/stan/nmr/py/BioPY/modules/')
import TopCmds, Setup
import IntShape
import FREQ as fq
import GetNUCs as NUC
import DREAM
from GetLib import pul
# Dictionary keys (from GetLib) that point to the actual parameter names

#'aCbsh'  :'SP 26'   ,'aHbshDc':'PL 13'   ,'pCbsh'  :'P 50'    ,'sCbsh'  :'SPNAM 44',\
#'pCbshFlp':'P 28'   ,'pCbsh2kFlp':'P 29'

# define special characters.  (I wonder if we can put the "<html><small><sup>13</sup></small>C 90&deg; pulse length</html>" here
deg=u"\u00b0"
ret=u"\u000D"
spc=u"\u0020"
unb=u"\u005f"
crt=u"\u005e"

"""
Now we define the "wrapper" function.  This is so we can re-use the same calculations,
to keep track of the variable names, and to have a convenient place to modify the text
that the user will see.

This is probably not needed in this case, but it is how most of the code is written  
  
Note, the variable "units" was "WdB" in the user script
"""
def Cmatch():
  aa, App, Bpp = DREAM.Nucl()
  #TopCmds.MSG(str(aa)+"\n"+str(App)+"\n"+str(Bpp))
  SUM=0
  for val in App:
    SUM=SUM+val
  AvgA=SUM/len(App)
  #TopCmds.MSG(str(AvgA))
  
  SUM=0
  for val in Bpp:
    SUM=SUM+val
  AvgB=SUM/len(Bpp)
  #TopCmds.MSG(str(AvgB))
  
  return math.fabs(AvgA-AvgB)
  
def CACO(units):
    
  Title="CA-CO BSH Homonuclear CP - Input"
  SuTit="Band C-C Selective CP"
  Label=["Match Field","Ramp Shape","Offset","Contact",
  "Decoupling Field"]
  In  =Title,SuTit,Label
  
  Title="BSH CP - Output"
  Label="13C","1H"
  Out =Title,Label

  ppm=Cmatch()
  
  CalBSH('pC90',ppm,'aCbsh','aHbshDc','pCbsh','sCbsh','ramp.100','pCbshFlp','pCbsh2kFlp',units,In,Out)

def CalBSH(p90,ppm,amp,ampD,Cnct,shp,dfltramp,pflp,pflp2k,units,In,Out):
  """
  p90   : Dictionary Key for Nucleus 90 degree pulse; determines Nuc (Decoupling flag)
  ppm   : float of ppm difference
  amp   : dict key for CP amp
  ampD  : dict key for Decoupler (assumed to be 1H) or "empty"
  Cnct  : dict key for CP contact
  shp   : dict key of CP shape file
  dfltshp: Default pulse shape
  pflp  : dict key for trim pulse
  pflp2k: dict key for flip back pulse
  units : Watts (W) or decibel (dB)
  In    : Title, Subtitle, and Label for Input Dialog
  Out   : Title and Label for Selection/Confirmation Window
  """  
  
  P90 =pul.GetPar(p90,"")
  P90D=pul.GetPar('pH90',"")

  if p90.find('H') >= 0:Amp=pul.GetPar('aH',units); nuc="1H"
  if p90.find('C') >= 0:Amp=pul.GetPar('aC',units); nuc="13C"
  if p90.find('N') >= 0:Amp=pul.GetPar('aN',units); nuc="15N"
  frq=fq.fq(nuc,1)

  AmpD =pul.GetPar('aH',units)

  i=0
  Nucs=NUC.list()
  for label in Nucs:
    if label==nuc:frq=fq.fq(nuc,i+1)
    i=i+1
  
  SP  =pul.GetPar(shp,"")
  MAS =pul.GetPar('MAS',"")/1000.  #kHz not Hz
  CNCT=pul.GetPar(Cnct,"")

  ## Check that the values aren't stupid
  if CNCT <= 1.    : CNCT =  1000.
  if CNCT >= 10000.: CNCT = 10000.

  MaxB1  = 1000000./4./P90
  MaxB1D = 1000000./4./P90D

  ##Set Decoupler if Appropriate
  if nuc!="1H":
    AmpD0=pul.GetPar(ampD,"dB")
    B1_0 = MaxB1D*(math.pow(10,(AmpD-AmpD0)/20.))

    if B1_0 >  100.  : Dcond='% .1f' % B1_0
    if B1_0 >  MaxB1D: Dcond='85000.0'
    if B1_0 <= 100.  : Dcond='85000.0'
  
  #Use a reasonable ramp name (passed in as dfltramp)
  if SP == "gauss" or SP == "None" or SP == "" or SP == "0" :
    pul.SetPar(shp,dfltramp,"")
    TopCmds.XCMD(pul.xcmd_name(pul.pulDict[shp]))
    SP=pul.GetPar(shp,"")

  ## change everything into dB for calculations.
  if units == "W":
    Amp =Setup.WtodB(Amp)
    AmpD=Setup.WtodB(AmpD)

  bf = math.floor(float(frq.bf))
  ppm=float(str('%.0f' %ppm))
  changedPPM='y'

  while changedPPM=='y':
    #TopCmds.MSG(str(ppm)+":ppm  bf:"+str(bf))
    DHz = ( float(ppm) * bf )/1000.
    bshkHz = round(float(((MAS*MAS)-((DHz * DHz)/4))/MAS),2)

    if nuc != "1H":
      index=TopCmds.INPUT_DIALOG(In[0],In[1],In[2],\
        [str('%.2f' %bshkHz),SP,str('%.0f' %ppm),\
        str('%.0f' %(CNCT/1000.)),str('%.2f' %(float(Dcond)/1000.))],\
        ["kHz","","ppm","ms","kHz"],\
        ["1","1","1","1","1"],\
        ["Accept","Close"], [spc,ret], 10)
      Dcond=float(index[4])*1000.

    if nuc == "1H":
      index=TopCmds.INPUT_DIALOG(In[0],In[1],In[2],\
        [str('%.2f' %bshkHz),str(SP),str('%.2f' %ppm),\
        str('%.0f' %(Cnct/1000.))],\
        ["kHz","","ppm","ms"],\
        ["1","1","1","1"],\
        ["Accept","Close"], [spc,ret], 10)

    bshkHz=float(index[0])
    SP=index[1]
    Cnct=float(index[3])*1000.

    if str('%.2f' %ppm)    == str('%.2f' %float(index[2])): changedPPM='n'
    if str('%.2f' %ppm)    != str('%.2f' %float(index[2])): changedPPM='y'; ppm=float(index[2])
 
  DHz = ( float(ppm) * bf )/1000.
  
  flip = (math.atan(DHz / bshkHz) *180) / 3.1415
  pflip = round( ((P90 * flip) / 90.) , 2)

  #TopCmds.MSG(str(P90)+" "+str(flip)+" "+str(pflip)+" "+str(DHz)+" "+str(bshkHz))
  flip2k = (DHz * DHz) / bshkHz
  pflip2k= round( ( (0.25 / flip2k) * 1000),2)

  w1bsh=float(index[0])
  adjust= 20*(math.log10(w1bsh*1000/MaxB1))
  AmpBsh= Amp-adjust
  
  # Adjust for the ramp.
  if SP == "Unused":
    AvgAmp=1.
  else:
    AvgAmp=IntShape.Integrate(SP)/100.
  AmpBsh = AmpBsh - 20*(math.log10(1./AvgAmp))
 
  # For the Decoupling
  if nuc != "1H":
    AmpDec= Setup.DecSafely(Dcond,ampD,MaxB1D,150000.,AmpD,units)

  # Convert to Watts, if wanted
  if units == "W":
    AmpBsh=Setup.dBtoW(AmpBsh)
    if nuc!="1H":Damp=Setup.dBtoW(AmpDec)

  if nuc == "1H" :
    value = TopCmds.SELECT(Out[0],"This will set\n "+\
      Out[1]+" power ("+pul.pulDict[amp]+") to: " + str('%3.2f' %AmpBsh)+" "+ units+"\n"+\
      "With shape (" + pul.pulDict[shp] + ") of "+ str(SP) +"\n"\
      "Flip pulse (" + pul.pulDict[pflp] +  ") of "+ str(pflip) +"us\n"\
      "Flip pulse 2k(" + pul.pulDict[pflp2k] +  ") of "+ str(pflip2k) +"us\n",\
      ["Update", "Keep Previous"],[spc,ret])

  else:
    value = TopCmds.SELECT(Out[0],\
      "This will set\n "+\
      Out[1][0]+" power ("+pul.pulDict[amp]+") to: " + str('%3.2f' %AmpBsh)+" "+ units+"\n"+\
      Out[1][1]+" power ("+pul.pulDict[ampD]+") to: " + str('%3.2f' %AmpD)+" "+ units+"\n"+\
      "With shape (" + pul.pulDict[shp] + ") of "+ str(SP) +"\n"\
      "Flip pulse (" + pul.pulDict[pflp] +  ") of "+ str(pflip) +"us\n"\
      "Flip pulse 2k(" + pul.pulDict[pflp2k] +  ") of "+ str(pflip2k) +"us\n",\
      ["Update", "Keep Previous"],[spc,ret])
  
  if value !=1:
    pul.SetPar(amp,AmpBsh,units)
    pul.SetPar(shp,SP,units)
    pul.SetPar(pflp,pflip,units)
    pul.SetPar(pflp2k,pflip2k,units)
    if nuc == "1H" :
      pul.SetPar(ampD,AmpD,units)

  return