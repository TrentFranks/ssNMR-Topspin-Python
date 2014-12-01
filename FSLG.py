"""
Computes FSLG amplitudes and offsets

Arguments:
-dB:interact with db instead of watts
-qt:Do not open initial pulse window

W.T. Franks FMP Berlin
"""

import sys
from sys import argv
sys.path.append(root.UtilPath.getTopspinHome()+ '/exp/stan/nmr/py/BioPY/modules/')

import Setup, Help
import LeeGoldburg as LG
import TS_Version as Ver

cmds=argv
WdB="W"
if Ver.get()[1] == "2": WdB="dB"
quiet="Loud"

########################
#  Read in preferences #
########################
Mode="Ampl"

for cmd in cmds:
  if cmd.find('-dB') >=0 or cmd.find('-DB') >=0 or cmd.find('-db') >=0 :
    WdB="dB"
  if cmd.find('-qt') >=0 or cmd.find('-QT') >=0 or cmd.find('-Qt') >=0 :
    quiet="Quiet"
  if cmd.find('-SW') >=0:
    Mode="Sweep"
  if cmd.find('-Fld') >=0:
    Mode="Field"
  if cmd.find('-pul') >=0:
    Mode="Pulse"
  if cmd.find('-help') >=0: Help.LG(); EXIT()

if quiet=="Loud":Setup.LoadFromData(WdB)
Cal=LG.FSLG(WdB)

#Cal.ByAmpl()
#Cal.ByPulse()
#Cal.ByField()
#Cal.BySW()
if Mode=="Pulse":Cal.ByPulse()
if Mode=="Field":Cal.ByField()
if Mode=="Sweep":Cal.BySW()
if Mode=="Ampl" :Cal.ByAmpl()
#LGCal.ByAmpl(WdB)
