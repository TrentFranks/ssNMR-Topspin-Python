"""
SOL_bsh.py
Created on 22.05.2014
Modified 02.07.2014 W.T. Franks FMP Berlin


Arguments:
-dB:interact with db instead of watts
-qt:Do not open initial pulse window

@author: Venita Daebel
@copyright: Bruker Biospin Corporation
"""

# sys gets us the arguments for dB or watts and quiet or loud and load the modules.
import sys
from sys import argv
sys.path.append(root.UtilPath.getTopspinHome()+ '/exp/stan/nmr/py/BioPY/modules/')

# load the calculations
import BandSelHomoCP as BSH
# determines which Topspin version is running, i.e. 2.1, 2.2, 3.1 etc.  
# Some parameter naming and python commands change accd. to TS version.
import TS_Version as Ver

# Get preferences, set "WdB" (Watts or Decibel) according to TS Version or preference
cmds=argv
WdB="W"
if Ver.get()[1] == "2": WdB="dB"

########################
#  Read in preferences #
########################

for cmd in cmds:
  if cmd.find('-dB') >=0 or cmd.find('-DB') >=0 or cmd.find('-db') >=0 :
    WdB="dB"
  #if cmd.find('-help'): Help.CP(); EXIT()


# Call the module to do the calculations
BSH.CACO(WdB)


"""
import os, re, string, math, sys, copy
import TopCmds

input = INPUT_DIALOG("BSH CP - Input",\
"Please enter the following parameters.",\
["MAS rate", "<html><small><sup>13</sup></small>C 90&deg; pulse length</html>",\
"<html><small><sup>13</sup></small>C 90&deg; power level in W </html>"],\
["", "", ""], ["kHz","us", "W"], ["1", "1", "1"],\
["Calculate","Quit"], ['c','q'], 10)
	
if input == None:TopCmds.EXIT()

# convert masr to integer	
masr = int(input[0])
if masr > 999.: masr = masr/1000		# ensure to work with mas in kHz, not in Hz
p1 =	float(input[1])
plw1 = float(input[2])

pldb1 = 10 * math.log10(1/plw1)

bfC =GETPAR("BF1")
bfC =math.floor(float(bfC))

# calculate the CO - Ca chemical shift difference in kHz
DHz = (120. * bfC)/1000

# BSH CP field strength calculation in kHz
bshkHz = ((masr*masr)-((DHz * DHz)/4))/masr
bshkHz = float(bshkHz)
BSHkHz = round(bshkHz, 2)	# round to a.xx

# calculation of CO flip angle and pulse length before BSH CP
flip = (math.atan(DHz / bshkHz) *180) / 3.1415
p28flip = round(flip, 2)	# round to a.xx	
p28 = (p1 * flip) / 90.
p28length = round(p28, 2) # round to a.xx

# calculation of BSH CP power in dB and Watts 
p1kHz = (1/(4 * p1)) * 1000
x = bshkHz / p1kHz
bshdB = -20 * (math.log10 (x)) + pldb1
BSHdB = round(bshdB, 2)	# round to a.xx
y = -0.1 * bshdB
bshW = math.pow(10., y) 
BSHW = round(bshW, 2)	# round to a.xx

# calculation of 2nd flip pulse length p29
flip2kHz = (DHz * DHz) / bshkHz
p29 = (0.25 / flip2kHz) * 1000
p29length = round(p29, 2)	# round to a.xx

input = INPUT_DIALOG("BSH CP - Output",\
"Please optimize around the following parameters.",\
["BSH CP field strength", "spdb26 / spdb27", "spw26 / spw27", "p28 (trim pulse)", "p29 (flip-back)"],\
["" + str(BSHkHz), "" + str(BSHdB), "" + str(BSHW), "" + str(p28length), "" + str(p29length)],\
["kHz","dB", "W", "us", "us"], ["1", "1", "1", "1", "1"],\
["Seen"], ['s'], 10)
	
if input == None:TopCmds.EXIT()
"""