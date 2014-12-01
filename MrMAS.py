"""
Calculate New conditions given a new and an old MAS rate

Use condition name specifically calculate that parameter,
i.e. if you only want to run a subset 

Arguments:
-n New MAS Rate
-o Old MAS Rate

Specify Conditions to calculate:
HC
HN
NCA
NCO
NC (both NCA and NCO)
"""
ret=u"\u000D"
spc=u"\u0020"

import sys
from sys import argv
sys.path.append(root.UtilPath.getTopspinHome()+ '/exp/stan/nmr/py/BioPY/modules/')

import Setup, Help
import MAS
import TS_Version as Ver

MASN=float(GETPAR("CNST 31"))
MAS0=float(GETPAR("MASR"))

GoAll=1
Interactive=1
WdB="W"
if Ver.get()[1] == "2": WdB="dB"
cmds=argv

i=0
for cmd in cmds:
  i = i+1
  #Do we like dB units better?
  if cmd.find('-dB') >=0 or cmd.find('-DB') >=0 or cmd.find('-db') >=0 :
    WdB="dB"
  #Have we already input the MAS rates?
  if cmd.find('-n') >=0: 
    MASN=float(cmds[i])
    Interactive=0
  if cmd.find('-o') >=0: 
    MAS0=float(cmds[i])
    Interactive=0

  #Are there optimizations we shouldn't touch?
  if cmd.find('HC')   >=0:GoAll=0
  if cmd.find('HN')   >=0:GoAll=0
  if cmd.find('NCA')  >=0:GoAll=0
  if cmd.find('NCO')  >=0:GoAll=0
  if cmd.find('NC ')  >=0:GoAll=0
  if cmd.find('SPC5') >=0:GoAll=0
  if cmd.find('C72')  >=0:GoAll=0

if Interactive:
  index = INPUT_DIALOG("CP MAS adjustments", "Spinning Speed", \
  ["Old MAS rate","New MAS rate"],\
  [str(MAS0),str(MASN)],\
  ["kHz","kHz"],\
  ["1","1"],\
  ["Accept","Close"], [ret,spc], 10)
  
  if index == None:EXIT()
  
  MASN=index[1]
  MAS0=index[0]

#####################################################
# Below is where the actual calculations are called #
#####################################################

#Adjust all conditions according to MAS
if GoAll == 1:
  MAS.HC(MAS0,MASN,WdB)
  MAS.HN(MAS0,MASN,WdB)
  MAS.NCA(MAS0,MASN,WdB)
  MAS.NCO(MAS0,MASN,WdB)
  #Homonuclear DQ mixing
  MAS.C72(MAS0,MASN,WdB)
  MAS.SPC5(MAS0,MASN,WdB)

#Adjust specified conditions according to MAS
else:
  for cmd in cmds:
    if cmd.find('HC')    >=0: MAS.HC(MAS0,MASN,WdB)
    if cmd.find('HN')    >=0: MAS.HN(MAS0,MASN,WdB)
    if cmd.find('NCA')   >=0: MAS.NCA(MAS0,MASN,WdB)
    if cmd.find('NCO')   >=0: MAS.NCO(MAS0,MASN,WdB)

    # NC will do both NCA and NCO, but shouldn't repeat them if both are specified
    if cmd.find('NC')    >=0:
      if cmd.find('NCA') <=0: MAS.NCA(MAS0,MASN,WdB)
      if cmd.find('NCO') <=0: MAS.NCO(MAS0,MASN,WdB)

    if cmd.find('SPC5')  >=0: MAS.SPC5(MAS0,MASN,WdB)
    #if cmd.find('C5 ')   >=0: MAS.adjC5()
    if cmd.find('C7')   >=0: MAS.C72(MAS0,MASN,WdB)

