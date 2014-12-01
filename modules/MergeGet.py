import de.bruker.nmr.mfw.root as root

import TopCmds
import CPDtools
import Setup
from GetLib import pul

def HC(Unit):
  CNCT=pul.GetPar('pHC',"")
  plC=pul.GetPar('aChc',Unit)
  plH=pul.GetPar('aHhc',Unit)
  SPC=pul.GetPar('sChc',"")
  SPH=pul.GetPar('sHhc',"")
  return CNCT, plH, plC, SPH, SPC

def HN(Unit):
  CNCT=pul.GetPar('pHN',"")
  plH=pul.GetPar('aHhn',Unit)
  plN=pul.GetPar('aNhn',Unit)
  SPN=pul.GetPar('sNhn',"")
  SPH=pul.GetPar('sHhn',"")
  return CNCT, plH, plN, SPH, SPN

def NCA(Unit):
  CNCT=pul.GetPar('pNCA',"")
  plH =pul.GetPar('aHnca',Unit)
  plC =pul.GetPar('aCnca',Unit)
  plN =pul.GetPar('aNnca',Unit)
  SPC =pul.GetPar('sCnca',"")
  SPN =pul.GetPar('sNnca',"")
  return CNCT, plH, plC, plN, SP

def NCO(Unit):
  CNCT=pul.GetPar('pNCO',"")
  plH =pul.GetPar('aHnco',Unit)
  plC =pul.GetPar('aCnco',Unit)
  plN =pul.GetPar('aNnco',Unit)
  SPC =pul.GetPar('sCnco',"")
  SPN =pul.GetPar('sNnco',"")
  return CNCT, plH, plC, plN, SP

def MAS(Unit):
  MAS=pul.GetPar('MAS',"")
  return MAS

def HPul(Unit):
  PL=pul.GetPar('aH',Unit)
  PW=pul.GetPar('pH90',"")
  return PW, PL

def CPul(Unit):
  PL=pul.GetPar('aC',Unit)
  PW=pul.GetPar('pC90',"")
  return PW, PL

def NPul(Unit):
  PL=pul.GetPar('aN',Unit)
  PW=pul.GetPar('pN90',"")
  return PW, PL

def DPul(Unit):
  PL=pul.GetPar('aD',Unit)
  PW=pul.GetPar('pD90',"")
  return PW, PL

def CX(Unit):
  PL=pul.GetPar('aHdarr',Unit)
  PW=pul.GetPar('dDarr',"")
  return PW, PL

def Format(para,Unit):
  found=0 
  para=para.upper()
  para=para.rstrip()
  
  if para.find("PL")>=0:
    para=para[:2]+Unit+para[2:]
  j=len(para)
  
  for i in range(0,9):
    if found==0:
      if para.find(str(i)) >=0:
        j=para.find(str(i))
        found=1
   
  if found==1:
    Format=para[:j]+" "+para[j:]
  if found==0:
    Format=para
  return Format
  
def HDec(Unit):
  CPD = "None"
  CPD= pul.GetPar('prgHDec',"")

  if CPD == "" or CPD == "None":
    PWname="PCPD 2"
    PLname="PL"+Unit+" 12"
    PW="5.0"
    if Unit == "dB": PL="1000."
    if Unit == "W": PL="0.0"

  else:
    PLname, PWname=CPDtools.CPDparse(CPD,"1H")

    PLname=Format(PLname,Unit)
    PWname=Format(PWname,"")

    if PWname == "PCPD":
      PWname = "PCPD 2"

    PW=pul.GetPar('pcpdH',"")
    PL=pul.GetPar('aHdec',Unit)

  return CPD, PWname, PW, PLname, PL

def CH(Unit):
  CNCT=pul.GetPar('pCH',"")
  plH=pul.GetPar('aHch',Unit)
  plC=pul.GetPar('aCch',Unit)

  SPX="None"
  SPX=pul.GetPar('sHch',"")
  if SPX == "" or SPX == "None":
    SPX="None"
  
  SPY="None"
  SPY=pul.GetPar('sCch',"")
  if SPY == "" or SPY == "None":
    SPY="None"
  
  return CNCT, plH, plC, SPX, SPY

def hhC(Unit):
  CNCT=pul.GetPar('phhC',"")
  plH=pul.GetPar('aHhhc',Unit)
  plC=pul.GetPar('aChhc',Unit)

  SPX="None"
  SPX=pul.GetPar('sHhhC',"")
  if SPX == "" or SPX == "None":
    SPX="None"
  
  SPY="None"
  SPY=pul.GetPar('sChhC',"")
  if SPY == "" or SPY == "None":
    SPY="None"
  
  return CNCT, plH, plC, SPX, SPY

def NH(Unit):
  CNCT=pul.GetPar('pNH',"")
  plH=pul.GetPar('aHnh',Unit)
  plN=pul.GetPar('aNnh',Unit)

  SPX="None"
  SPX=pul.GetPar('sHnh',"")
  if SPX == "" or SPX == "None":
    SPX="None"
  
  SPY="None"
  SPY=pul.GetPar('sNnh',"")
  if SPY == "" or SPY == "None":
    SPY="None"
  
  return CNCT, plH, plC, SPX, SPY

def Phases():
  PH0=pul.GetPar("PHC0","")
  PH1=pul.GetPar("PHC1","")
  #TopCmds.MSG("PH0: "+str(PH0)+"\n PH1: " +str(PH1))
  return PH0, PH1

def CH2(Unit):
  CNCT=pul.GetPar('pCH2',"")
  plC=pul.GetPar('aCch2',Unit)
  plH=pul.GetPar('aHch2',Unit)
  SPX="None"
  SPX=pul.GetPar('sHch2',"")
  if SPX == "" or SPX == "None":
    SPX="None"
  
  SPY="None"
  SPY=pul.GetPar('sCch2',"")
  if SPY == "" or SPY == "None":
    SPY="None"
  return CNCT, plH, plC, SPX, SPY

def NH2(Unit):
  CNCT=pul.GetPar('pNH2',"")
  plH=pul.GetPar('aHnh2',Unit)
  plN=pul.GetPar('aNnh2',Unit)
  SPX="None"
  SPX=pul.GetPar('sHnh2',"")
  if SPX == "" or SPX == "None":
    SPX="None"
  
  SPY="None"
  SPY=pul.GetPar('sNnh2',"")
  if SPY == "" or SPY == "None":
    SPY="None"
  return CNCT, plH, plN, SPX, SPY

def CA_S90(Unit):
  CNCT=pul.GetPar('pCAe',"")
  plX=pul.GetPar('aCAe',Unit)
  SPX=pul.GetPar('sCAe',"")
  OFF=pul.GetPar('oCAe',"")
  if SPX == "" or SPX == "None":
    SPX="None"
  return CNCT, plX, SPX, OFF

def CO_S90(Unit):
  CNCT=pul.GetPar('pCOe',"")
  plX=pul.GetPar('aCOe',Unit)
  SPX=pul.GetPar('sCOe',"")
  OFF=pul.GetPar('oCOe',"")
  if SPX == "" or SPX == "None":
    SPX="None"
  return CNCT, plX, SPX, OFF

def CA_S180(Unit):
  CNCT=pul.GetPar('pCAr',"")
  plX=pul.GetPar('aCAr',Unit)
  SPX=pul.GetPar('sCAr',"")
  OFF=pul.GetPar('oCAr',"")
  if SPX == "" or SPX == "None":
    SPX="None"
  return CNCT, plX, SPX, OFF

def CO_S180(Unit):
  CNCT=pul.GetPar('pCOr',"")
  plX=pul.GetPar('aCOr',Unit)
  SPX=pul.GetPar('sCOr',"")
  OFF=pul.GetPar('oCOr',"")
  if SPX == "" or SPX == "None":
    SPX="None"
  return CNCT, plX, SPX, OFF

