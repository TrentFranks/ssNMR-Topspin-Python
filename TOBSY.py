"""
Computes various amplitudes
W.T. Franks FMP Berlin
"""
import sys
from sys import argv
sys.path.append(root.UtilPath.getTopspinHome()+ '/exp/stan/nmr/py/BioPY/modules/')

import Setup, Help
import TOBSY
import TS_Version as Ver

cmds=argv
WdB="W"
if Ver.get()[1] == "2": WdB="dB"

########################
#  Read in preferences #
########################

for cmd in cmds:
  if cmd.find('-dB') >=0 or cmd.find('-DB') >=0 or cmd.find('-db') >=0 :
    WdB="dB"
  if cmd.find('-help') >=0 : Help.Sym(); EXIT()

Sym=SELECT("TOBSY Symmetry Sequences","Use C9_3^1, C9_6^1 or adiabatic", ["C931", "C961","Adiabatic"])
if   Sym == 0 : 
  TOBSY.CalC931(WdB)
if   Sym == 1 : 
  TOBSY.CalC961(WdB)
elif Sym == 2 : 
  TOBSY.name_confirm()
  TOBSY.CalC542_adb_TOBSY(WdB)
