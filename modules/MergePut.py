import de.bruker.nmr.mfw.root as root
import TopCmds
from GetLib import pul

def MAS(MAS, Unit):
  pul.SetPar('MAS',MAS,"")
  return 

def HPul(PW, PL, Unit):
  pul.SetPar('pH90',PW,"")
  pul.SetPar('pH180',str(2*float(PW)),"")
  pul.SetPar('aH',PL,Unit)
  return 

def CPul(PW, PL, Unit):
  pul.SetPar('pC90',PW,"")
  pul.SetPar('pC180',str(2.*float(PW)),"")
  pul.SetPar('aC',PL,Unit)
  return 

def NPul(PW, PL, Unit):
  pul.SetPar('pN90',PW,"")
  pul.SetPar('pN180',str(2*float(PW)),"")
  pul.SetPar('aN',PL,Unit)
  #pul.SetPar('',,"")
  return 

def DPul(PW, PL, Unit):
  pul.SetPar('pD90',PW,"")
  pul.SetPar('pD180',str(2*float(PW)),"")
  pul.SetPar('aD',PL,Unit)
  return PW, PL

def CX(PW, PL, Unit):
  pul.SetPar('dDarr',PW,"")
  pul.SetPar('aHdarr',PL,Unit)
  return 

def HDec(CPD, PWNAME, PW, PLNAME, PL, Unit):
  pul.SetPar('prgHDec',CPD,"")
  pul.SetPar(PWNAME,PW,"")
  pul.SetPar('aHdec',PL,Unit)
  return 

def HC(CNCT, plH, plX, SPH, SPX, Unit):
  pul.SetPar('pHC',CNCT,"")
  pul.SetPar('aHhc',plH,Unit)
  pul.SetPar('aChc',plX,Unit)
  pul.SetPar('sHhc',SPH,"")
  pul.SetPar('sChc',SPX,"")
  return 

def HN(CNCT, plH, plX, SPH, SPX, Unit):
  pul.SetPar('pHN',CNCT,"")
  pul.SetPar('aHhn',plH,Unit)
  pul.SetPar('aNhn',plX,Unit)
  pul.SetPar('sHhn',SPH,"")
  pul.SetPar('sNhn',SPX,"")
  return 

def NCA(CNCT, plH, plC, plN, SPX, SPY, Unit):
  pul.SetPar('pNCA',CNCT,"")  
  pul.SetPar('aHnca',plH,Unit)
  pul.SetPar('aNnca',plN,Unit)
  pul.SetPar('aCnca',plC,Unit)
  pul.SetPar('sCnca',SPX,"")
  pul.SetPar('sNnca',SPY,"")
  return 

def NCO(CNCT, plH, plC, plN, SPX, SPY, Unit):
  pul.SetPar('pNCO',CNCT,"")  
  pul.SetPar('aHnco',plH,Unit)
  pul.SetPar('aNnco',plN,Unit)
  pul.SetPar('aCnco',plC,Unit)
  pul.SetPar('sCnco',SPX,"")
  pul.SetPar('sNnco',SPY,"")
  return 

def CH( CNCT, plH, plC, SPX, SPY, Unit):
  pul.SetPar('pCH',CNCT,"")
  pul.SetPar('aHch',plH,Unit)
  pul.SetPar('aCch',plC,Unit)
  pul.SetPar('sHch',SPX,"")
  pul.SetPar('sCch',SPY,"")
  return

def hhC( CNCT, plH, plC, SPX, SPY, Unit):
  pul.SetPar('phhC',CNCT,"")
  pul.SetPar('aHhhc',plH,Unit)
  pul.SetPar('aChhc',plC,Unit)
  pul.SetPar('sHhhc',SPX,"")
  pul.SetPar('sChhc',SPY,"")
  return

def NH( CNCT, plH, plN, SPX, SPY, Unit):
  pul.SetPar('pNH',CNCT,"")
  pul.SetPar('aHnh',plH,Unit)
  pul.SetPar('aNnh',plN,Unit)
  pul.SetPar('sHnh',SPX,"")
  pul.SetPar('sNnh',SPY,"")
  return

def Phases(Phase):
  pul.SetPar('PHC0',Phase[0],"")
  pul.SetPar('PHC1',Phase[1],"")
  #Reload so everything updates.
  TopCmds.SLEEP(0.05)
  TopCmds.RE(TopCmds.CURDATA())
  TopCmds.SLEEP(0.05)
  return

def C_Soft(PW, PL, Unit):
  return

def CH2(CNCT, plH, plX, SPH, SPX, Unit):
  pul.SetPar('pCH2',CNCT,"")
  pul.SetPar('aHch2',plH,Unit)
  pul.SetPar('aCch2',plX,Unit)
  pul.SetPar('sHch2',SPH,"")
  pul.SetPar('sCch2',SPX,"")
  return 

def NH2(CNCT, plH, plX, SPH, SPX, Unit):
  pul.SetPar('pNH2',CNCT,"")
  pul.SetPar('aHnh2',plH,Unit)
  pul.SetPar('aNnh2',plX,Unit)
  pul.SetPar('sHnh2',SPH,"")
  pul.SetPar('sNnh2',SPX,"")
  return 

def CA_S90(CNCT, plX, SPX, Offs, Unit):
  pul.SetPar('pCAe',CNCT,"")
  pul.SetPar('aCAe',plH,Unit)
  pul.SetPar('sCAe',SPX,"")
  pul.SetPar('oCAe',Offs,"")
  return 

def CO_S90(CNCT, plX, SPX, Offs, Unit):
  pul.SetPar('pCOe',CNCT,"")
  pul.SetPar('aCOe',plH,Unit)
  pul.SetPar('sCOe',SPX,"")
  pul.SetPar('oCOe',Offs,"")
  return 

def CA_S180(CNCT, plX, SPX, Offs, Unit):
  pul.SetPar('pCAr',CNCT,"")
  pul.SetPar('aCAr',plH,Unit)
  pul.SetPar('sCAr',SPX,"")
  pul.SetPar('oCAr',Offs,"")
  return 

def CO_S180(CNCT, plX, SPX, Offs, Unit):
  pul.SetPar('pCOr',CNCT,"")
  pul.SetPar('aCOr',plH,Unit)
  pul.SetPar('sCOr',SPX,"")
  pul.SetPar('oCOr',Offs,"")
  return 
