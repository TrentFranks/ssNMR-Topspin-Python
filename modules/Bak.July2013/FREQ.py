import de.bruker.nmr.mfw.root as root

import math
import TopCmds

class O1:
  OFFS=float(TopCmds.GETPAR("O1"))
  BF=float(TopCmds.GETPAR("BF1"))
  ref=float(TopCmds.GETPAR("SR"))
  RF=BF*1000000.
  RO=OFFS-ref

  def ppm2offs(self,ppm):
    frq=(O1.RF*ppm/1000000.)- O1.RO
    return frq

  def offs2ppm(self,frq):
    ppm=(1000000./O1.RF)*(frq+O1.RO)
    return ppm

class O2:
  OFFS=float(TopCmds.GETPAR("O2"))
  BF=float(TopCmds.GETPAR("BF2"))
  ref=float(TopCmds.GETPAR("SR"))
  RF=BF*1000000.
  RO=OFFS-ref

  def ppm2offs(self,ppm):
    frq=(O2.RF*ppm/1000000.)- O2.RO
    return frq

  def offs2ppm(self,frq):
    ppm=(1000000./O2.RF)*(frq+O2.RO)
    return ppm

class O3:
  OFFS=float(TopCmds.GETPAR("O3"))
  BF=float(TopCmds.GETPAR("BF3"))
  ref=float(TopCmds.GETPAR("SR"))
  RF=BF*1000000.
  RO=OFFS-ref

  def ppm2offs(self,ppm):
    frq=(O3.RF*ppm/1000000.)- O3.RO
    return frq

  def offs2ppm(self,frq):
    ppm=(1000000./O3.RF)*(frq+O3.RO)
    return ppm

class O4:
  OFFS=float(TopCmds.GETPAR("O4"))
  BF=float(TopCmds.GETPAR("BF4"))
  ref=float(TopCmds.GETPAR("SR"))
  RF=BF*1000000.
  RO=OFFS-ref

  def ppm2offs(self,ppm):
    frq=(O4.RF*ppm/1000000.)- O4.RO
    return frq

  def offs2ppm(self,frq):
    ppm=(1000000./O4.RF)*(frq+O4.RO)
    return ppm

