"""
Computes a DREAM pulse shape:

W.T. Franks FMP Berlin
DREAM match condition is 0.5*wr=W1
"""
import sys
from sys import argv
sys.path.append(root.UtilPath.getTopspinHome()+ '/exp/stan/nmr/py/BioPY/modules/')

import DREAM
import Setup, Help
import TS_Version as Ver

cmds=argv
WdB="W"
if Ver.get()[1] == "2": WdB="dB"
quiet="Loud"

########################
#  Read in preferences #
########################

for cmd in cmds:
  if cmd.find('-dB') >=0 or cmd.find('-DB') >=0 or cmd.find('-db') >=0 :
    WdB="dB"
  if cmd.find('-qt') >=0 or cmd.find('-QT') >=0 or cmd.find('-Qt') >=0 :
    quiet="Quiet"
  if cmd.find('-help') >=0 : Help.CP(); EXIT()

if quiet=="Loud":DREAM.LoadFromData('13C','oCdrm',WdB)
DREAM.CC(WdB)