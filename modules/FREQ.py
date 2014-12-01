import de.bruker.nmr.mfw.root as root

import math
import TopCmds

class fq:
  def __init__(self,name,channel):
    #initialize the frequency
    self.name   = name
    self.offsp  = float(TopCmds.GETPAR("O"+str(channel)+"P"))
    self.offs   = float(TopCmds.GETPAR("O"+str(channel)))
    self.bf     = float(TopCmds.GETPAR("BF"+str(channel)))
    #self.bf     = float(TopCmds.GETPAR("1 BF"+str(channel)))
    self.sf     = float(TopCmds.GETPAR("SFO"+str(channel)))
    self.rf     = self.bf*1000000.
    if TopCmds.GETPROCDIM() >= channel:
      self.ref  = float(TopCmds.GETPAR(str(channel)+" SR"))
    else:
      self.ref  = 0.
    self.ro     = self.offs-self.ref
    #self.carr   = 

    if self.name.find("1H")>=0: self.nucl="1H"
    if self.name.find("C")>=0: self.nucl="13C"
    if self.name.find("2H")>=0: self.nucl="2H"
    if self.name.find("D")>=0: self.nucl="2H"
    if self.name.find("N")>=0: self.nucl="15N"

  def ppm2offs(self,ppm):
    frq=((self.rf)*ppm/1000000) - self.ro
    #frq= ppm - self.ro 
    #frq = (self.bf-(self.bf*ppm/1000000.)) - self.bf
    #frq = (self.bf - 
    return frq

  def offs2ppm(self,frq):
    ppm=(1000000./self.rf)*(frq+self.ro)
    return ppm
