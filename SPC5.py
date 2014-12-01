"""
Computes various amplitudes
W.T. Franks FMP Berlin
"""
import sys
from sys import argv
sys.path.append(root.UtilPath.getTopspinHome()+ '/exp/stan/nmr/py/BioPY/modules/')

import Setup, Help
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
  if cmd.find('-qt') >=0 or cmd.find('-QT') >=0 or cmd.find('-Qt') >=0 :
    quiet="Quiet"
  if cmd.find('-help') >=0 : Help.Sym(); EXIT()

if quiet=="Loud":Setup.LoadFromData(WdB)

C52o3=SELECT("Symmetry sequences","Use SPC5_2 (broadband) or SPC5_3 (narrowband)", ["SPC5 3", "SPC5 2"])
if   C52o3 == 0 : Setup.SPC5_3(WdB)
elif C52o3 == 1 : Setup.SPC5_2(WdB)
