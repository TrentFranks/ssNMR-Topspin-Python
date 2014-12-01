import de.bruker.nmr.mfw.root as root
import TopCmds

def HPul(PW, PL, Unit):
  TopCmds.PUTPAR("P 3",str(PW))
  TopCmds.PUTPAR("P 4",str(2*float(PW)))
  TopCmds.PUTPAR("PL"+Unit+" 2",PL)
  return 

def CPul(PW, PL, Unit):
  TopCmds.PUTPAR("P 1",PW)
  TopCmds.PUTPAR("P 2",str(2*float(PW)))
  TopCmds.PUTPAR("PL"+Unit+" 1", PL)
  return 

def NPul(PW, PL, Unit):
  TopCmds.PUTPAR("P 21",PW)
  TopCmds.PUTPAR("P 22",str(2*float(PW)))
  #PL=TopCmds.PUTPAR("PL"+Unit+" 21")
  TopCmds.PUTPAR("PL"+Unit+" 3",PL)
  return 

def DPul(PW, PL, Unit):
  TopCmds.PUTPAR("P X",PW)
  TopCmds.PUTPAR("P X+1",str(2*float(PW)))
  TopCmds.PUTPAR("PL"+Unit+" X",PL)
  return PW, PL

def CX(PW, PL, Unit):
  TopCmds.PUTPAR("D 8",PW)
  TopCmds.PUTPAR("PL"+Unit+" 14", PL)
  return 

def HDec(CPD, PWNAME, PW, PLNAME, PL, Unit):
  TopCmds.PUTPAR("CPDPRG 2",CPD)
  TopCmds.PUTPAR(PWNAME,PW)
  TopCmds.PUTPAR(PLNAME,PL)
  return 

def HC(CNCT, plH, plX, SPH, SPX, Unit):
  TopCmds.PUTPAR("P 15",CNCT)
  TopCmds.PUTPAR("PL"+Unit+" 40",plX)
  TopCmds.PUTPAR("PL"+Unit+" 41",plH)
  TopCmds.PUTPAR("SP"+Unit+" 40",plX)
  TopCmds.PUTPAR("SP"+Unit+" 41",plH)
  TopCmds.PUTPAR("SPNAM 40",SPX)
  TopCmds.PUTPAR("SPNAM 41",SPH)
  return 

def HN(CNCT, plH, plX, SPH, SPX, Unit):
  TopCmds.PUTPAR("P 25",CNCT)
  TopCmds.PUTPAR("PL"+Unit+" 42",plX)
  TopCmds.PUTPAR("PL"+Unit+" 43",plH)
  TopCmds.PUTPAR("SP"+Unit+" 42",plH)
  TopCmds.PUTPAR("SP"+Unit+" 43",plX)
  TopCmds.PUTPAR("SPNAM 42",SPX)
  TopCmds.PUTPAR("SPNAM 43",SPH)
  return 

def NCA(CNCT, plH, plC, plN, SP, Unit):
  TopCmds.PUTPAR("PL"+Unit+" 5",plN)
  TopCmds.PUTPAR("PL"+Unit+" 50",plC)
  TopCmds.PUTPAR("SP"+Unit+" 50",plC)
  TopCmds.PUTPAR("PL"+Unit+" 33",plH)
  TopCmds.PUTPAR("P 16",CNCT)
  TopCmds.PUTPAR("SPNAM 50",SP)
  return 

def NCO(CNCT, plH, plC, plN, SP, Unit):
  TopCmds.PUTPAR("PL"+Unit+" 6",plN)
  TopCmds.PUTPAR("PL"+Unit+" 51",plC)
  TopCmds.PUTPAR("SP"+Unit+" 51",plC)
  TopCmds.PUTPAR("PL"+Unit+" 34",plH)
  TopCmds.PUTPAR("P 17",CNCT)
  TopCmds.PUTPAR("SPNAM 51",SP)
  return 

def CH( CNCT, plH, plC, SP, Unit):
  TopCmds.PUTPAR("SP"+Unit+" 48",plH)
  TopCmds.PUTPAR("PL"+Unit+" 48",plH)
  TopCmds.PUTPAR("PL"+Unit+" 49",plC)
  TopCmds.PUTPAR("P 48"   ,CNCT)
  TopCmds.PUTPAR("SPNAM 48",SP)
  return

def hhC( CNCT, plH, plC, SP, Unit):
  TopCmds.PUTPAR("SP"+Unit+" 44",plH)
  TopCmds.PUTPAR("PL"+Unit+" 44",plH)
  TopCmds.PUTPAR("PL"+Unit+" 45",plC)
  TopCmds.PUTPAR("P 44"   ,CNCT)
  TopCmds.PUTPAR("SPNAM 44",SP)
  return

def NH( CNCT, plH, plN, SP, Unit):
  TopCmds.PUTPAR("SP"+Unit+" 46",plH)
  TopCmds.PUTPAR("PL"+Unit+" 46",plH)
  TopCmds.PUTPAR("PL"+Unit+" 47",plC)
  TopCmds.PUTPAR("P 46"   ,CNCT)
  TopCmds.PUTPAR("SPNAM 46",SP)
  return

def C_Soft(PW, PL, Unit):
  return
