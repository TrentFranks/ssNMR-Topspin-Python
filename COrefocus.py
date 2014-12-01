"""
Computes various amplitudes

Arguments:
-dB:interact with db instead of watts
-qt:Do not open initial pulse window
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
  if cmd.find('-help') >=0 : Help.SelPul(); EXIT()

SelPul.S9refocus(WdB)
