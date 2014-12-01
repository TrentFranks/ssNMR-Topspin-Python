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
import FREQ as fq
import GetNUCs as NUC

"""def dialog():
   MAS=float(TopCmds.GETPAR("CNST 31"))
   TauR=float(1000000/MAS)
   input = TopCmds.INPUT_DIALOG("DREAM input", "", \
   ["Nominal RF ampl","MAS","Total Duration","RI,RO duration","steps","Ramp","Adiabicity"],\
   ["85",str('%.0f' % MAS),"1.0",str( '%3.2f' % (TauR)),"1000","20","4"],\
   ["kHz"," Hz","ms","us","","+/- %",""],\
   ["1","1","1","1","1","1","1"],\
   ["Accept","Close"], ['a','c'], 10)
   return input
"""
def dialog(Scale, Delta, Beta):
   MAS=float(TopCmds.GETPAR("CNST 31"))
   TauR=float(1000000/MAS)

   input = TopCmds.INPUT_DIALOG("DREAM input", "", \
   ["Total Duration","RI,RO duration","Scale","Ramp","Adiabicity"],\
   ["1.0",str( '%3.2f' % TauR),str( '%3.1f' % Scale),str( '%3.1f' % Delta),str( '%3.1f' % Beta)],\
   ["ms","us","%","+/- %",""],\
   ["1","1","1","1","1","1","1"],\
   ["Accept","Close"], ['a','c'], 10)
   return input

def name_no_confirm(input,Name,SP):
   if Name=="":
      Name = str("DREAM_" + input[5] + "D_"+ input[6] + "B_" + input[1] + "MAS.wave")
   if SP=="":
      SP = str("SPNAM5")
      TopCmds.PUTPAR(str(SP),str(File))
   return Name, SP

def name_confirm(Ttot,RIRO,Sc,Del,Bet):
   Name = "DREAM_" + Del +"D_"+ Bet+ "B_" + Sc + "Sc_"+Ttot+"ms_"+ RIRO + "us_ri.wave"
   SP = "SPNAM 5"
   Wave = str(TopCmds.INPUT_DIALOG("DREAM Files", "", ["C File = ","C Wave =",],\
   [Name,SP],["",""],["1","1"],["Accept","Close"], ['a','c'], 30))
   
   Files = Wave[27:len(Wave)-3]  #get rid of Java formatting
   
   i = Files.find(",")
   File = Files[0:i-1]
   SP = Files[i+4:]
   TopCmds.PUTPAR(SP,File)
   return File, SP
  
def make(Ttot,RIRO,Sc,Del,Bet,Name):
  import math
  ampl = [] #  normalized to 0...100
  ph = [] #  normalized to 0...100
  #TopCmds.MSG(Sc+" "+Del+" "+Bet)
  
  durat = 1000.*float(Ttot)
  steps = int(1000*float(Ttot))
  Read  = float(RIRO)
  Delta = float(Del)
  Beta  = float(Bet)
  Scale = float(Sc)

  RIOsteps = int(steps*Read/durat)
  TopCmds
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
  if Nucs[0]=="13C":
    Frq=fq.O1()
  elif Nucs[1]=="13C":
    Frq=fq.O2()
  elif Nucs[2]=="13C":
    Frq=fq.O3()

  p90 =float(TopCmds.GETPAR("P 1"))
  MAS =float(TopCmds.GETPAR("CNST 31"))
  NomRF = 1000000./4./p90

  nomatch=[]
  Af=[]
  Bf=[]
  Ap=[]
  Bp=[]
  Condition=[]
  mfaa=[]
  #message=[]
    

#  It should default to CA-CB matching for DREAM, and CA-CO for R2T
#  I'm not sure the best way to select these but I'm putting it in as a dialog

  aa, Ap, Bp = Nucl()

  #TopCmds.MSG(str(aa))
  #TopCmds.MSG(str(Ap))
  #TopCmds.MSG(str(Bp))


# Now we'll convert the ppm averages from above into frequencies

  hits=0
  mm=1
  SPOFF=float(TopCmds.GETPAR("SPOFFS 5"))

  for i in range(len(aa)):
    Af.append(SPOFF+Frq.ppm2offs(Ap[i]))
    Bf.append(SPOFF+Frq.ppm2offs(Bp[i]))

# The offsets should be less than 1/2 (or 1*) the MAS frequency, or we can't match.
# We will store a list for those aa's that we can't match.
    
    m=1 
    Match=m*MAS-math.fabs(Af[i])-(math.fabs(Bf[i]))
    if Match < 0 :
      m=2; mm=2
      Match=m*MAS-(math.fabs(Af[i]))-(math.fabs(Bf[i]))
    #TopCmds.MSG(str(Match)+" "+str(math.fabs(Af[i]))+" "+str(math.fabs(Bf[i])))
    if Match < 0: nomatch.append(aa[i])
    if Match >= 0: hits=hits+1
  #TopCmds.MSG(str(len(nomatch)))

  if len(nomatch) > 0 :
    TopCmds.MSG("Cannot find match conditions for:\n "\
    + str(nomatch)+ "\n at this carrier or spinning frequency")
  if hits == 0: 
    TopCmds.MSG("Cannot find any match conditions, please consider changing frequencies")
    TopCmds.EXIT()

# Now, we want to determine the matches and store the results and extrema,
# but not for things we know can't be matched

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
        for n in range(MAS*2):
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

# Now I want to report what we've found.  I'll start with an average, deviation and the extremes, 
# And offer a detailed report after a dialog.  
# I guess these numbers could be used to generate a wave file

  Avg=0.0
  Dev=0.0
  for i in range(len(Condition)):
    Avg=Avg+float(Condition[i])
  Avg=Avg/float(len(Condition))
  for i in range(len(Condition)):
    Dev=Dev+(float(Condition[i])-Avg)**2
  Dev=math.sqrt(Dev/float(len(Condition)-1))
  #TopCmds.MSG("DEV(DONE): " + str(Dev))
  #TopCmds.MSG(str(Avg)+":Average \n"+str(Dev) +":StDev")

  Continue=TopCmds.SELECT("Scaling",\
    "The mean match is %.2f Hz" % Avg \
    + " \n With a deviation of %.2f Hz" % Dev \
    + "\n with a maximum at %i Hz " % Upper\
    + "\n and a minimum at %i Hz " % Lower\
    ,["Details","Proceed"]) #0,1

  #TopCmds.MSG(str(SeeMore))
  if not Continue:
    for i in range(math.ceil(len(mfaa)/20.)):
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

    for i in range(math.ceil(len(mfaa)/20.)):
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
  
  return AvgPC, DeltaPC, BetaPC

def Nucl():

  Amino=[]
  aa=list()
  Appm=[]
  Bppm=[]
  App=list()
  Bpp=list()
  suffix=list()
  
  Nuclei=TopCmds.SELECT("Select matching condidtion for which nuclei?",\
    "Calculate match for which nuclei?",\
    ["Aliphatics","CO-Cali","CA-CB","CB-CG","CG-CD","CO-CA","CO-CB","CO-CG","CO-CD"]) #0,1

  #CA-CB
  if Nuclei==2 or Nuclei==0 :
    Amino="A","R","D","N","C","E","Q","H","I","L","K","M","F","P","S","T","W","Y","V"
      #ALA,  ARG,  ASP,  ASN,  CYS,  GLU,  GLN,  HIS,  ILE,  LEU,  LYS,  MET,  PHE,  PRO,  SER,  THR,  TRP,  TYR,  VAL) # [w/o GLY]
    Appm=53.16,56.95,54.52,53.43,57.43,57.42,56.62,56.37,61.59,55.65,56.84,56.16,58.25,63.30,58.57,62.15,57.71,58.02,62.48
    Bppm=18.90,30.66,40.70,38.66,34.15,30.07,29.10,29.95,38.58,42.37,32.83,32.90,39.95,31.81,63.80,69.64,30.16,39.16,32.66
    
    aa.extend(Amino)
    App.extend(Appm)
    Bpp.extend(Bppm)
    
    if Nuclei!=2 :
      for i in range(len(aa)-len(Amino), len(aa)):
        aa[i]=str(aa[i])+"-cacb"
  #CB-CG
  if Nuclei==3 or Nuclei==0 :
    Amino="R","E","Q","I","I","L","K","M","P","T","V"
    #     ARG GLU GLN IG1 IG2 LEU LYS MET PRO THR VAL)
    Appm=30.66,30.07,29.10,38.58,38.58,42.37,32.83,32.90,31.81,69.64,32.66
    Bppm=27.31,36.01,33.72,27.65,17.36,26.77,24.91,32.07,27.14,21.44,21.38

    aa.extend(Amino)
    App.extend(Appm)
    Bpp.extend(Bppm)
    
    if Nuclei!=3 :
      for i in range(len(aa)-len(Amino), len(aa)):
        aa[i]=str(aa[i])+"-cbcg"
  #CG-CD
  if Nuclei==4 or Nuclei==0 :
    Amino="R","I","I","L","K","P"
    Appm=27.31,27.65,17.36,26.77,24.91,27.14
    Bppm=43.10,13.41,13.41,24.73,28.78,50.28
 
    aa.extend(Amino)
    App.extend(Appm)
    Bpp.extend(Bppm)
    
    if Nuclei!=4 :
      for i in range(len(aa)-len(Amino), len(aa)):
        aa[i]=str(aa[i])+"-cgcd"

  #CO-CA
  if Nuclei==5 or Nuclei==1  :
    Amino="A","R","D","N","C","E","Q","G","H","I","L","K","M","F","P","S","T","W","Y","V"
    #     ALA ARG ASP ASN CYS GLU GLN GLY HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL)
    Appm=53.16,56.95, 54.52, 53.43, 57.43, 57.42, 56.62, 45.33, 56.37, 61.59, 55.65, 56.84, 56.16, 58.25, 63.30, 58.57, 62.15, 57.71, 58.02, 62.48
    Bppm=177.8,176.49,176.41,175.16,174.78,176.93,176.39,174.04,175.19,175.82,176.97,176.46,176.30,175.49,176.70,174.53,174.60,176.10,175.39,175.69
    aa.extend(Amino)
    App.extend(Appm)
    Bpp.extend(Bppm)
    
    if Nuclei!=5 :
      for i in range(len(aa)-len(Amino), len(aa)):
        aa[i]=str(aa[i])+"-coca"

  #CO-CB
  if Nuclei==6 or Nuclei==1  :
    Amino="A","R","D","N","C","E","Q","H","I","L","K","M","F","P","S","T","W","Y","V"
    #     ALA ARG ASP ASN CYS GLU GLN HIS ILE LEU LYS MET PHE PRO SER THR TRP TYR VAL # [w/o GLY]
    Appm=177.8,176.49, 176.41,175.16,174.78,176.93,176.39,175.19,175.82,176.97,176.46,176.30,175.49,176.70,174.53,174.60,176.10,175.39,175.69
    Bppm=18.90,30.66,  40.70, 38.66, 34.15, 30.07, 29.10, 29.95, 38.58, 42.37, 32.83, 32.90, 39.95, 31.81, 63.80, 69.64, 30.16, 39.16, 32.66
    aa.extend(Amino)
    App.extend(Appm)
    Bpp.extend(Bppm)
    
    if Nuclei!=6 :
      for i in range(len(aa)-len(Amino), len(aa)):
        aa[i]=str(aa[i])+"-cocb"

  #CO-CG
  if Nuclei==7 or Nuclei==1  :
    Amino="R","E","Q","I","I","L","K","M","P","T","V"
    #     ARG GLU GLN IG1 IG2 LEU LYS MET PRO THR VAL
    Appm=176.49,176.93,176.39,175.82,175.82,176.97,176.46,176.30,176.70,174.60,175.69
    Bppm=27.31,36.01, 33.72, 27.65, 17.36, 26.77, 24.91, 32.07, 27.14, 21.44, 21.38

    aa.extend(Amino)
    App.extend(Appm)
    Bpp.extend(Bppm)
    
    if Nuclei!=7 :
      for i in range(len(aa)-len(Amino), len(aa)):
        aa[i]=str(aa[i])+"-cocg"

  #CO-CD
  if Nuclei==8 or Nuclei==1  :
    Amino="R","I","L","K","P"
    Appm=176.49,175.82,176.97,176.46,176.70
    Bppm=43.10, 13.41, 24.73, 28.78, 50.28
    
    aa.extend(Amino)
    App.extend(Appm)
    Bpp.extend(Bppm)
    
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
  
  
  

"""
  #YorN=TopCmds.SELECT("Scaling", "The match condition is at %i Hz \n\n Which scaling should be used?" % Upper , ["Calibration", "0.5" , "None(1.0)"])
  CONFIRM("Scale Shape Pulse for Match","The amplitude should be approximately %i Hz \n \nUse scaling?" % Match)
  #if YorN < 0: Scale=1.0
  #if YorN == 0: Scale=float(Match)/NomRF
  #if YorN == 1: Scale=0.5
  #if YorN == 2: Scale=1.0

  import math
  NomRF = 1000*float(input[0])
  MAS   = float(input[1])
  Ioffs = 1000*float(input[6])
  Soffs = 1000*float(input[7])
  
  YorN=TopCmds.SELECT("Scaling", "The match condition is around %i Hz \n\n Which scaling should be used?" % mm , ["Calibration", "0.5" , "None(1.0)"])
#  CONFIRM("Scale Shape Pulse for Match","The amplitude should be approximately %i Hz \n \nUse scaling?" % Match)
  if YorN < 0: Scale=1.0
  if YorN == 0: Scale=float(Match)/NomRF
  if YorN == 1: Scale=0.5
  if YorN == 2: Scale=1.0
  return Scale
"""  
