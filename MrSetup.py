"""
Computes various amplitudes

Arguments:
-dB:interact with db instead of watts

W.T. Franks FMP Berlin
"""

import sys
from sys import argv
sys.path.append(root.UtilPath.getTopspinHome()+ '/exp/stan/nmr/py/BioPY/modules/')

import Setup, Help
import SelPul
import TS_Version as Ver

cmds=argv
WdB="W"
ret=u"\u000D"
spc=u"\u0020"

if Ver.get()[1] == "2": WdB="dB"

########################
#  Read in preferences #
########################

for cmd in cmds:
  if cmd.find('-dB') >=0 or cmd.find('-DB') >=0 or cmd.find('-db') >=0 :
    WdB="dB"

#PrevDef=SELECT("Use dataset", "Overwrite with Default", ["Use Data", "Default"],[ret,'d'])
#if   PrevDef == 0 : 
Setup.LoadFromData(WdB)
#elif PrevDef == 1 : Setup.LoadDefault(WdB)
#else : EXIT()

#CP conditions
Setup.HC(WdB)
Setup.HN(WdB)
Setup.HDec(WdB)
Setup.NCA(WdB)
Setup.NCO(WdB)

#EXIT()
#Homonuclear DQ mixing
Setup.C72(WdB)

C52o3=SELECT("Symmetry sequences","Use SPC5_2 (broadband) or SPC5_3 (narrowband)", ["SPC5 3", "SPC5_2"])
if   C52o3 == 1 : Setup.SPC5_3(WdB)
elif C52o3 == 0 : Setup.SPC5_2(WdB)
elif C52o3 <  0 : EXIT()

#XhhC type experiments
import XhhC

XhhC.CH(WdB)
XhhC.NH(WdB)
XhhC.HC(WdB)

#Soft Pulses s6,7,8, and 9
SelPul.S6purge(WdB)
SelPul.S7purge(WdB)
SelPul.S8refocus(WdB)
SelPul.S9refocus(WdB)

EXIT()

#Homonuclear TOBSY mixing
#TOBSY.name_confirm(WdB)
#TOBSY.CalC961_TOBSY(WdB)
#TOBSY.CalC542_adb_TOBSY(WdB)

