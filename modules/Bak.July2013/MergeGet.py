import de.bruker.nmr.mfw.root as root

import TopCmds
import CPDtools
import Setup

def HC(Unit):
  CNCT=TopCmds.GETPAR("P 15")
  #plC=TopCmds.GETPAR("PL"+Unit+" 40")
  #plH=TopCmds.GETPAR("PL"+Unit+" 41")
  plC=TopCmds.GETPAR("SP"+Unit+" 40")
  plH=TopCmds.GETPAR("SP"+Unit+" 41")
  SPC=TopCmds.GETPAR2("SPNAM 40")
  SPH=TopCmds.GETPAR2("SPNAM 41")
  #TopCmds.MSG("CNCT: "+CNCT+"\n plH: "+plH+"\n plC: "+plC+"\n SPH: "+SPH+"\n SPC: "+SPC)
  return CNCT, plH, plC, SPH, SPC

def HN(Unit):
  CNCT=TopCmds.GETPAR("P 25")
  #plN=TopCmds.GETPAR("PL"+Unit+" 42")
  #plH=TopCmds.GETPAR("PL"+Unit+" 43")
  plH=TopCmds.GETPAR("SP"+Unit+" 42")
  plN=TopCmds.GETPAR("SP"+Unit+" 43")
  #TopCmds.MSG(TopCmds.GETPAR2("SPNAM 42"))
  SPN=TopCmds.GETPAR2("SPNAM 42")
  #TopCmds.MSG(TopCmds.GETPAR2("SPNAM 43"))
  SPH=TopCmds.GETPAR2("SPNAM 43")
  #TopCmds.MSG("CNCT: "+CNCT+"\n plH: "+plH+"\n plN: "+plN+"\n SPH: "+SPH+"\n SPN: "+SPN)
  return CNCT, plH, plN, SPH, SPN

def NCA(Unit):
  CNCT=TopCmds.GETPAR("P 16")
  plH =TopCmds.GETPAR("PL"+Unit+" 33")
  plC =TopCmds.GETPAR("SP"+Unit+" 50")
  plN =TopCmds.GETPAR("PL"+Unit+" 5")
  SP  =TopCmds.GETPAR2("SPNAM 50")
  #TopCmds.MSG("CNCT: "+CNCT+"\n plH: "+plH+"\n plN: "+plN+"\n plC: "+plC+"\n SP: "+SP)
  return CNCT, plH, plC, plN, SP

def NCO(Unit):
  CNCT=TopCmds.GETPAR("P 17")
  plH=TopCmds.GETPAR("PL"+Unit+" 34")
  plN=TopCmds.GETPAR("PL"+Unit+" 6")
  plC=TopCmds.GETPAR("SP"+Unit+" 51")
  SP=TopCmds.GETPAR2("SPNAM 51")
  return CNCT, plH, plC, plN, SP

def HPul(Unit):
  PW=TopCmds.GETPAR("P 3")
  PL=TopCmds.GETPAR("PL"+Unit+" 2")
  return PW, PL

def CPul(Unit):
  PW=TopCmds.GETPAR("P 1")
  PL=TopCmds.GETPAR("PL"+Unit+" 1")
  return PW, PL

def NPul(Unit):
  PW=TopCmds.GETPAR("P 21")
  #PL=TopCmds.GETPAR("PL"+Unit+" 21")
  PL=TopCmds.GETPAR("PL"+Unit+" 3")
  return PW, PL

def DPul(Unit):
  PW=TopCmds.GETPAR("P X")
  PL=TopCmds.GETPAR("PL"+Unit+" X")
  return PW, PL

def CX(Unit):
  PW=TopCmds.GETPAR("D 8")
  PL=TopCmds.GETPAR("PL"+Unit+" 14")
  return PW, PL

def Format(para,Unit):
  found=0 
  para=para.upper()
  para=para.rstrip()
  
  if para.find("PL")>=0:
    para=para[:2]+Unit+para[2:]
  j=len(para)
  
  for i in range(0,10):
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
  CPD=TopCmds.GETPAR2("CPDPRG 2")

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

    PW=TopCmds.GETPAR(PWname)
    PL=TopCmds.GETPAR(PLname)
  #TopCmds.MSG(PWname+"  "+PLname+"  "+str(PW)+"  "+str(PL))
  
  return CPD, PWname, PW, PLname, PL


def CH(Unit):
  CNCT=TopCmds.GETPAR("P 48")
  plH=TopCmds.GETPAR("SP"+Unit+" 48")
  plC=TopCmds.GETPAR("PL"+Unit+" 49")

  SP="None"
  SP =TopCmds.GETPAR2("SPNAM 48")
  if SP == "" or SP == "None":
    SP="None"
  return CNCT, plH, plC, SP

def hhC(Unit):
  CNCT=TopCmds.GETPAR("P 44")
  plH=TopCmds.GETPAR("PL"+Unit+" 44")
  plC=TopCmds.GETPAR("PL"+Unit+" 45")

  SP="None"
  SP =TopCmds.GETPAR2("SPNAM 44")
  if SP == "" or SP == "None":
    SP="None"
  return CNCT, plH, plC, SP

def NH(Unit):
  CNCT=TopCmds.GETPAR("P 46")
  plH=TopCmds.GETPAR("SP"+Unit+" 46")
  plN=TopCmds.GETPAR("PL"+Unit+" 47")

  SP="None"
  SP =TopCmds.GETPAR2("SPNAM 46")
  if SP == "" or SP == "None":
    SP="None"
  return CNCT, plH, plN, SP

def C_Soft(Unit):
  return

