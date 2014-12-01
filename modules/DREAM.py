"""
DREAM module
Match condition adapted from Donghua H Zhou, Oklahoma State U.
W.T. Franks FMP Berlin

Need to account for offset of pulse (SPOFFS)
Need to change frequency if no matches found

"""
import de.bruker.nmr.mfw.root as root

import sys
import math
from sys import argv
import TopCmds
import Setup, IntShape
import FREQ as fq
import GetNUCs as NUC
import TS_Version as Ver
from GetLib import pul

ret=u"\u000D"
spc=u"\u0020"

"""Nucs=NUC.list()
MaxDim=TopCmds.GETPROCDIM()
i=0
for item in Nucs:
  if i < MaxDim:
    if item =='13C':Cfrq=fq.fq(item,i+1); TopCmds.MSG("Trent Rules!")
    if item =='1H': Hfrq=fq.fq(item,i+1)
    if item =='15N':Nfrq=fq.fq(item,i+1)
    if item =='2H': Dfrq=fq.fq(item,i+1)
  i=i+1
"""
def LoadFromData(Nuc,offs,units):
  """
  Nuc  : Nucleus for DREAM mixing
  offs : dict key for Dream offset
  units: dB or Watts
  """

  p90H, p90C, p90N, ampH, ampC, ampN, MAS = Setup.ReadHPFromData(units)

  #Define frequencies
  Nucs=NUC.list()
  i=0
  for item in Nucs:
    if item==Nuc:
      if item =='13C':Frq=fq.fq(item,i+1)
      if item =='15N':Frq=fq.fq(item,i+1)
      if item =='1H' :Frq=fq.fq(item,i+1)
      if item =='2H' :Frq=fq.fq(item,i+1)
    i=i+1

  FqUnit=pul.GetPar('uoffs',"")
  FqMeth=pul.GetPar('oFrom',"")

  #TopCmds.MSG(FqUnit + "  "+FqMeth+"  "+str(Frq.bf))
  # Everything in absolute PPM
  if FqMeth=="Carrier":
    if FqUnit=="Hz" :OffsPPM=Frq.offs2ppm(pul.GetPar(offs,""))
    if FqUnit=="ppm":OffsPPM=Frq.offsp-pul.GetPar(offs,"")
  else:
    if FqUnit=="Hz" :OffsPPM=Frq.offs2ppm(pul.GetPar(offs,"")-Frq.offs)
    if FqUnit=="ppm":OffsPPM=pul.GetPar(offsp,"")

  index = TopCmds.INPUT_DIALOG("Mr Setup Input", "Pulse Widths and Power", \
  ["1H 90 pw","1H ampl","13C 90 pw","13C ampl","15N 90 pw","15N ampl","DREAM Offset","MAS"],\
  [str('%.2f' %p90H),str('%.2f' %ampH),str('%.2f' %p90C),str('%.2f' %ampC),\
  str('%.2f' %p90N),str('%.2f' %ampN),str('%.2f' %Offsppm),str('%.2f' %MAS)],\
  ["us",units,"us",units,"us",units,"ppm"," Hz"],\
  ["1","1","1","1","1","1","1","1"],\
  ["Accept","Close"], [spc,ret], 10)
  
  if index == None:TopCmds.EXIT()
    
  p90H=float(index[0])
  ampH=float(index[1])
  p90C=float(index[2])
  ampC=float(index[3])
  p90N=float(index[4])
  ampN=float(index[5])
  MAS =float(index[7])
  TauR= 1000000./MAS
  Setup.PutPars(p90H,ampH,p90C,ampC,p90N,ampN,MAS,units)

  if FqMeth=="Carrier":
    if FqUnit=="Hz" :OffsPPM=Frq.offsp-float(index[6])
    2ppm(pul.GetPar(offs,""))
    if FqUnit=="ppm":OffsPPM=Frq.offsp-pul.GetPar(offs,"")
  else:
    if FqUnit=="Hz" :OffsPPM=Frq.offs2ppm(pul.GetPar(offs,"")-Frq.offs)
    if FqUnit=="ppm":OffsPPM=pul.GetPar(offsp,"")
  
  if FqMeth=="Zero"   : Offsppm=
  if FqMeth=="Carrier": Offsppm=Frq.offsp+float(index[6])

  # Everything in the right units
  if FqUnit=="Hz" :pul.Setpar(offs,Frq.ppm2offs(Offsppm,""),"")
  if FqUnit=="ppm":pul.Setpar(offs,Offsppm,"")


def CC(units):
  
  dfltSP = "square.100"
  
  Title="CC DREAM Input"; SuTit="Carbon Carbon Adiabatic Mixing"
  Label=["Carbon B1 Field","C Ramp","Contact Time",\
         "H Decoupling"]

  In  =Title,SuTit,Label
  
  Title="Adjusting the DREAM parameters:"; Label="1H","13C"
  Out =Title,Label

  Match, Delta, Devia = CMatch()  #In Hz

  Ramp=pul.GetPar('sCdrm',"")
  GoRamp=TopCmds.SELECT("Ramp",\
    "Would you like to use the ramp: "+Ramp+\
    " \n Or make a new Tangent Ramp?",\
    ["Use Current","Make New"])
    
  if GoRamp:
    SP,Time=MakeRamp(Match,Delta,Devia,"13C")
  else:
    SP=Ramp; Time=pul.GetPar('pCdrm',"")

  CalDREAM('pC90',Match,'aCdrm','aHdrmDC','pCdrm',SP,'sCdrm',dfltSP,units,In,Out)
  
def CalDREAM(p90,match,amp,ampD,Cnct,SP,dfltSP,shpdict,units,In,Out):
  """
  p90   : Dictionary Key for Nucleus 90 degree pulse; determines Nuc (Decoupling flag)
  match : float of precalculated match
  amp   : dict key for DREAM amp
  ampD  : dict key for Decoupler (assumed to be 1H) or "empty"
  Cnct  : dict key for DREAM contact
  shp   : dict key of DREAM shape file
  dfltSP: Default pulse shape
  shpdict:dict key for DREAM shape
  units : Watts (W) or decibel (dB)
  In    : Title, Subtitle, and Label for Input Dialog
  Out   : Title and Label for Selection/Confirmation Window
  """

  MAS=pul.GetPar('MAS',"")
  TauR=float(1000000/MAS)
  P90D=pul.GetPar('pH90',"")
  AmpD =pul.GetPar('aH',"dB")
  MaxB1D = 1000000./4./P90D

  if p90.find('H') >=0:MaxB1=1000000./4./(pul.GetPar('pH90',""));Amp=pul.GetPar('aH','dB')
  if p90.find('C') >=0:MaxB1=1000000./4./(pul.GetPar('pC90',""));Amp=pul.GetPar('aC','dB')

  CNCT=pul.GetPar(Cnct,"")

  if CNCT <= 1.    : CNCT =  1000.
  if CNCT >= 10000.: CNCT = 10000.

  if p90.find('H') <=0:
    AmpD0=pul.GetPar(ampD,'dB')
    B1_0 = MaxB1D*(math.pow(10,(AmpD-AmpD0)/20.))
    if B1_0 >  100.  : Dcond='% .1f' % B1_0
    if B1_0 >  MaxB1D: Dcond='85000.0'
    if B1_0 <= 100.  : Dcond='85000.0'
  
  if units == "W":
    Amp=WtodB(Amp)

  if SP == "gauss" or SP == "None" or SP=="" or SP == "0" :
    SP=dfltSP
    pul.SetPar(shpdict,SP,"")
    TopCmds.XCMD(pul.xcmd_name(pul.pulDict[shpdict]))
    SP=pul.GetPar(shp,"")

  if p90.find('H') >=0:
    index=TopCmds.INPUT_DIALOG(In[0],In[1],In[2],\
    [str('%.3f' %(match/1000.)),str(SP),str('%.3f' %(CNCT/1000.))],\
    ["kHz","","ms"],\
    ["1","1","1"],\
    ["Accept","Close"], [spc,ret], 10)
    if index== None: TopCmds.EXIT()
  else:
    index=TopCmds.INPUT_DIALOG(In[0],In[1],In[2],\
    [str('%.3f' %(match/1000.)),str(SP),str('%.3f' %(CNCT/1000.)),\
    str('%.3f' %(float(Dcond)/1000.))],\
    ["kHz","","ms","kHz"],\
    ["1","1","1","1"],\
    ["Accept","Close"], [spc,ret], 10)
    if index== None: TopCmds.EXIT()
    wD=float(index[3])

  w1=float(index[0])
  SP=index[1]
  CNCT=float(index[2])*1000.

  #Integrate Dream ramp
  adjust=20*(math.log10(w1*1000./MaxB1))
  Amp1 = Amp-adjust
  AvgAmp=(IntShape.Integrate(SP))/100.
  adjust=20*(math.log10(1./AvgAmp))
  AmpX = Amp1-adjust

  if units == "W": AmpX=dBtoW(AmpX)

  #TopCmds.MSG(str(Out))
  if p90.find('H') <=0:
    AmpD = Setup.DecSafely(1000.*wD,ampD,MaxB1D,150000.,AmpD,units)

    value = TopCmds.SELECT(Out[0],\
    "This will set\n "+\
    Out[1][1]+" power ("+ pul.pulDict[amp] +") to:  " + str('%3.2f' %AmpX)+" "+ units+"\n"+\
    Out[1][0]+" power ("+ pul.pulDict[ampD] +") to:  " + str('%3.2f' %AmpD)+" "+ units,\
    ["Update", "Keep Previous"],[spc,ret])
  else:
    value = TopCmds.SELECT(Out[0],\
    "This will set\n "+\
    Out[1][0]+" power ("+ pul.pulDict[amp] +") to:  " + str('%3.2f' %Hamp)+" "+ units+"\n"+\
    ["Update", "Keep Previous"],[spc,ret])

  if value != 1:
    pul.SetPar(amp,AmpX,units)
    pul.SetPar(Cnct,CNCT,"")

    if p90.find('H') <=0:
      pul.SetPar(ampD,AmpD,"dB")

def MakeRamp(Scale, Delta, Beta, Nuc):

   MAS =pul.GetPar('MAS',"")
   TauR=float(1000000/MAS)
   
   if Nuc=="1H" :
     MaxB1=1000./4./(pul.GetPar('pH90',""))
     Amp=pul.GetPar('aH','dB')
     Time=pul.GetPar('pHdrm',"")
     TimeKey='pHdrm'
     key='sHdrm'
   if Nuc=="13C":
     MaxB1=1000./4./(pul.GetPar('pC90',""))
     Amp=pul.GetPar('aC','dB')
     Time=pul.GetPar('pCdrm',"")
     TimeKey='pCdrm'
     key='sCdrm'

   PctScal=Scale/MaxB1
   PctRamp=2.*Delta/MaxB1
   PctAdia=Beta/MaxB1
   
   Index = TopCmds.INPUT_DIALOG("DREAM RAMP", "", \
   ["Total Contact","Read-In/Out","Ampl","Ramp","Adiabicity"],\
   [str(Time/1000.),str( '%3.2f' % (2*TauR)),str('%3.1f'%(Scale/1000.)),\
   str('%3.1f'%(Delta/1000.)),str('%3.1f' % Beta)],\
   ["ms"           ,"us"         ,"kHz" ,"+/- kHz","Hz"],\
   ["1"            ,"1"          ,"1"   ,"1"      ,"1"],\
   ["Accept","Close"], [spc,ret], 10)
   if Index == None:TopCmds.EXIT()
   
   PctAmpl=100.*float(Index[2])/MaxB1
   PctDel=PctAmpl*float(Index[3])
   PctBet=float(Index[2])*float(Index[4])/MaxB1/10.
   
   Name=name_confirm(Index[0],Index[1],str(PctAmpl),str(PctDel),str(PctBet),key)
   make(Index[0],Index[1],str(PctAmpl),str(PctRamp),PctBet,Name,key)

   pul.SetPar(TimeKey,1000.*float(Index[0]),"")
   
   return Name, Index[0]

def name_confirm(Ttot,RIRO,Sc,Del,Bet,key):
   Name = "DRM_" + str('%.0f'%Sc) +"Sc_"+str('%.0f'%Del)+"D_"+str('%.0f'%Bet)+"B.wave"
   SP=pul.pulDict[key]
   
   index=TopCmds.INPUT_DIALOG("DREAM Files", "", \
   ["File = ","Wave =",],[Name,SP],["",""],["1","1"],\
   ["Accept","Close"], [spc,ret], 30)

   if index == None:TopCmds.EXIT()

   pul.SetPar(key,index[0],"")

   return index[0]
  
def make(Ttot,RIRO,Sc,Del,Bet,Name,key):
  import math
  ampl = [] #  normalized to 0...100
  ph = [] #  normalized to 0...100
  #TopCmds.MSG(Sc+" "+Del+" "+Bet)
  
  durat = 1000.*float(Ttot)
  steps = int(300*float(Ttot))
  Read  = float(RIRO)
  Delta = float(Del)
  Beta  = float(Bet)
  Scale = float(Sc)

  RIOsteps = int(steps*Read/durat)
  tansteps = steps-2*RIOsteps
  
  Start=100.-(Delta*(Beta/math.fabs(Beta)))
  End  =100.+(Delta*(Beta/math.fabs(Beta)))
  
  k=(tansteps-1)/2
  alpha=(2.0/(tansteps-1))*math.atan(Delta/Beta)
  absBeta=math.fabs(Beta)
  
  for i in range(steps):
    if i < RIOsteps:
      RF=1.0*i*Start/RIOsteps
    if i >= RIOsteps:
      j=i-RIOsteps
      di=absBeta*math.tan(alpha*float(j-k))
      RF=100.+di
    if i > (steps-RIOsteps):
      j=i-steps+RIOsteps
      RF=1.0*End-j*End/RIOsteps
    ampl.append(Scale*RF/100)
    ph.append(0.0)
  TopCmds.SAVE_SHAPE(Name[0], "NoRotation", ampl,ph)

def CMatch():
  #Nuc is a string such as 1H or 13C 
  Nucs=NUC.list()
  for i in range(len(Nucs)):
    if Nucs[i]=='13C':Frq=fq.fq(Nucs[i],i+1)

  p90 =pul.GetPar('pC90',"")
  MAS =pul.GetPar('MAS',"")
  NomRF = 1000000./4./p90

  nomatch=[]
  Af=[]
  Bf=[]
  Ap=[]
  Bp=[]
  Condition=[]
  mfaa=[]
  #message=[]

  aa, Ap, Bp = Nucl()

  hits=0
  mm=1
  SPOFF=pul.GetPar('oCdrm',"")-Frq.offs
  #TopCmds.MSG(str(SPOFF))

  for i in range(len(aa)):
    Af.append(Frq.ppm2offs(Ap[i])-SPOFF)
    Bf.append(Frq.ppm2offs(Bp[i])-SPOFF)

    m=1 
    Match=m*MAS-math.fabs(Af[i])-(math.fabs(Bf[i]))
    #if Match < 0 :
    #  m=2; mm=2
    #  Match=m*MAS-(math.fabs(Af[i]))-(math.fabs(Bf[i]))
    if Match < 0: nomatch.append(aa[i])
    if Match >= 0: hits=hits+1

  if len(nomatch) > 0 :
    TopCmds.MSG("Cannot find match conditions for:\n "\
    + str(nomatch)+ "\n at this carrier or spinning frequency")
  if hits == 0: 
    TopCmds.MSG("Cannot find any match conditions, please consider changing frequencies")
    TopCmds.EXIT()

  Upper=0
  Lower=MAS*2
  NotCount=len(nomatch)
  
  #Determine if we want to skip
  for i in range(len(aa)):
      skip=0
      found=0
      for j in range(NotCount):
        if nomatch[j] == aa[i]: skip=1
      if not skip:
        for n in range(int(MAS*2)):
          if not found :
            WAeff = math.sqrt(Af[i]*Af[i]+float(n*n))
            WBeff = math.sqrt(Bf[i]*Bf[i]+float(n*n))
            Match=(mm*MAS)-WAeff-WBeff
            #mm is the match multiplier
            if Match <= 0.0: 
              found=1
              mfaa.append(aa[i])
              Condition.append(n)
              if n > Upper : Upper=n
              if n < Lower : Lower=n
        if not found: 
          nomatch.append(aa[i])
          #Condition.append('N/A')
          #TopCmds.MSG(str(nomatch))
        
      #TopCmds.MSG(aa[i]+ " " + str(Ap[i]) + " " +str(Bp[i]) + " " + str(Upper) + " " +str(Lower))

  if len(nomatch) > 0 :
    TopCmds.MSG("Cannot find match conditions for:\n "\
    + str(nomatch)+ "\n at this carrier or spinning frequency")

  # Report average, deviation and the extremes, 
  # Offer a detailed report after a dialog.  
  # These numbers are used to generate a wave file

  Avg=0.0
  Dev=0.0
  for i in range(len(Condition)):
    Avg=Avg+float(Condition[i])
  Avg=Avg/float(len(Condition))
  for i in range(len(Condition)):
    Dev=Dev+(float(Condition[i])-Avg)**2
  Dev=math.sqrt(Dev/float(len(Condition)-1))

  Continue=TopCmds.SELECT("Scaling",\
    "The mean match is %.2f Hz" % Avg \
    + " \n With a deviation of %.2f Hz" % Dev \
    + "\n with a maximum at %i Hz " % Upper\
    + "\n and a minimum at %i Hz " % Lower\
    ,["Details","Proceed"]) #0,1

  #TopCmds.MSG(str(SeeMore))
  if not Continue:
    for i in range(int(math.ceil(len(mfaa)/20.))):
      message="Here is set #"+str(i+1)+" of the match conditions alphabetically by nucleus\n\n"
      
      for j in range(i*20,min((i+1)*20,len(mfaa))):
        message=message+str(mfaa[j])+":  "+ str(Condition[j]) + "Hz\n "
      TopCmds.MSG(message)

  # Now I want to sort into order by increasing match
    for i in range(len(aa)):
      for j in range(len(aa)):
        if Condition[j] > Condition[i]:
          Condition[j], Condition[i] = Condition[i], Condition[j]
          mfaa[j], mfaa[i] = mfaa[i], mfaa[j]

    for i in range(int(math.ceil(len(mfaa)/20.))):
      message="Here is set #"+str(i+1)+" of the match conditions by match\n\n"
      
      for j in range(i*20,min((i+1)*20,len(mfaa))):
        message=message + str(Condition[j]) + " Hz : "+str(mfaa[j])+"\n "
      TopCmds.MSG(message)

  #TopCmds.MSG(str(NomRF))
  
  # Finally I'm going to pass the result back
  # It is best to do this as a percentage to suggest a pulse shape.
  # I need a delta, beta, and scale.  

  #TopCmds.MSG(str(Avg))
  AvgPC  =100.*Avg/NomRF
  DeltaPC=100.*(Upper-Lower)/NomRF
  BetaPC =100.*Dev/NomRF
  
  #return AvgPC, DeltaPC, BetaPC
  return Avg, Upper-Lower, Dev

def Nucl():

  Amino=[]
  aa=[]
  Appm=[]
  Bppm=[]
  App=[]
  Bpp=[]
  suffix=[]
  
  Nuclei=TopCmds.SELECT("Select matching condidtion for which nuclei?",\
    "Calculate match for which nuclei?",\
    ["Aliph","CO-Cali","CA-CB","CB-CG","CG-CD","CO-CA","CO-CB","CO-CG","CO-CD"]) #0,1

  #CA-CB
  if Nuclei==2 or Nuclei==0 :
    Amino="A","R","D","N","C","E","Q","H","I","L","K","M","F","P","S","T","W","Y","V"
      #ALA,  ARG,  ASP,  ASN,  CYS,  GLU,  GLN,  HIS,  ILE,  LEU,  LYS,  MET,  PHE,  PRO,  SER,  THR,  TRP,  TYR,  VAL) # [w/o GLY]
    Appm=53.16,56.95,54.52,53.43,57.43,57.42,56.62,56.37,61.59,55.65,56.84,56.16,58.25,63.30,58.57,62.15,57.71,58.02,62.48
    Bppm=18.90,30.66,40.70,38.66,34.15,30.07,29.10,29.95,38.58,42.37,32.83,32.90,39.95,31.81,63.80,69.64,30.16,39.16,32.66
    
    aa.extend(list(Amino))
    App.extend(list(Appm))
    Bpp.extend(list(Bppm))
    
    if Nuclei!=2 :
      for i in range(len(aa)-len(Amino), len(aa)):
        aa[i]=str(aa[i])+"-cacb"
  #CB-CG
  if Nuclei==3 or Nuclei==0 :
    Amino="R","E","Q","I","I","L","K","M","P","T","V"
    #     ARG GLU GLN IG1 IG2 LEU LYS MET PRO THR VAL)
    Appm=30.66,30.07,29.10,38.58,38.58,42.37,32.83,32.90,31.81,69.64,32.66
    Bppm=27.31,36.01,33.72,27.65,17.36,26.77,24.91,32.07,27.14,21.44,21.38

    aa.extend(list(Amino))
    App.extend(list(Appm))
    Bpp.extend(list(Bppm))
    
    if Nuclei!=3 :
      for i in range(len(aa)-len(Amino), len(aa)):
        aa[i]=str(aa[i])+"-cbcg"
  #CG-CD
  if Nuclei==4 or Nuclei==0 :
    Amino="R","I","I","L","K","P"
    Appm=27.31,27.65,17.36,26.77,24.91,27.14
    Bppm=43.10,13.41,13.41,24.73,28.78,50.28
 
    aa.extend(list(Amino))
    App.extend(list(Appm))
    Bpp.extend(list(Bppm))
    
    if Nuclei!=4 :
      for i in range(len(aa)-len(Amino), len(aa)):
        aa[i]=str(aa[i])+"-cgcd"

  #CO-CA
  if Nuclei==5 or Nuclei==1  :
    Amino="A","R","D","N","C","E","Q","G","H","I","L","K","M","F","P","S","T","W","Y","V"
    #     ALA ARG ASP ASN CYS GLU GLN GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL)
    Appm=53.16,56.95, 54.52, 53.43, 57.43, 57.42, 56.62, 45.33, 56.37, 61.59, 55.65, 56.84, 56.16, 58.25, 63.30, 58.57, 62.15, 57.71, 58.02, 62.48
    Bppm=177.8,176.49,176.41,175.16,174.78,176.93,176.39,174.04,175.19,175.82,176.97,176.46,176.30,175.49,176.70,174.53,174.60,176.10,175.39,175.69
    aa.extend(list(Amino))
    App.extend(list(Appm))
    Bpp.extend(list(Bppm))
    
    if Nuclei!=5 :
      for i in range(len(aa)-len(Amino), len(aa)):
        aa[i]=str(aa[i])+"-coca"

  #CO-CB
  if Nuclei==6 or Nuclei==1  :
    Amino="A","R","D","N","C","E","Q","H","I","L","K","M","F","P","S","T","W","Y","V"
    #     ALA ARG ASP ASN CYS GLU GLN HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL # [w/o GLY]
    Appm=177.8,176.49, 176.41,175.16,174.78,176.93,176.39,175.19,175.82,176.97,176.46,176.30,175.49,176.70,174.53,174.60,176.10,175.39,175.69
    Bppm=18.90,30.66,  40.70, 38.66, 34.15, 30.07, 29.10, 29.95, 38.58, 42.37, 32.83, 32.90, 39.95, 31.81, 63.80, 69.64, 30.16, 39.16, 32.66
    aa.extend(list(Amino))
    App.extend(list(Appm))
    Bpp.extend(list(Bppm))
    
    if Nuclei!=6 :
      for i in range(len(aa)-len(Amino), len(aa)):
        aa[i]=str(aa[i])+"-cocb"

  #CO-CG
  if Nuclei==7 or Nuclei==1  :
    Amino="R","E","Q","I","I","L","K","M","P","T","V"
    #     ARG GLU GLN IG1 IG2 LEU LYS MET PRO THR VAL
    Appm=176.49,176.93,176.39,175.82,175.82,176.97,176.46,176.30,176.70,174.60,175.69
    Bppm=27.31,36.01, 33.72, 27.65, 17.36, 26.77, 24.91, 32.07, 27.14, 21.44, 21.38

    aa.extend(list(Amino))
    App.extend(list(Appm))
    Bpp.extend(list(Bppm))
    
    if Nuclei!=7 :
      for i in range(len(aa)-len(Amino), len(aa)):
        aa[i]=str(aa[i])+"-cocg"

  #CO-CD
  if Nuclei==8 or Nuclei==1  :
    Amino="R","I","L","K","P"
    Appm=176.49,175.82,176.97,176.46,176.70
    Bppm=43.10, 13.41, 24.73, 28.78, 50.28
    
    aa.extend(list(Amino))
    App.extend(list(Appm))
    Bpp.extend(list(Bppm))
    
    if Nuclei!=8 :
      for i in range(len(aa)-len(Amino), len(aa)):
        aa[i]=str(aa[i])+"-cocd"

# Now I want to sort into ABC order
  name=aa
  Count=len(aa)
  for i in range(Count):
    for j in range(Count):
      if aa[j] > aa[i]:
        aa[j], aa[i] = aa[i], aa[j]
        App[j], App[i] = App[i], App[j]
        Bpp[j], Bpp[i] = Bpp[i], Bpp[j]

  return aa, App, Bpp
  