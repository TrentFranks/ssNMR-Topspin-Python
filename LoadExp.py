"""
Load appropriate Pulse Program and acquisition parameters 

Arguments:
-1D: load nD experiment as a 1D
-2D: load nD experiment as a 2D (unless 1D experiment)
-3D: load nD experiment as a 3D (unless 1D, or 2D then highest)

-CC, hCC: load a 2D CC experiment (default to DARR)

More to come when it starts working

W.T. Franks FMP Berlin
"""

import math
import sys
import os
from sys import argv
sys.path.append(root.UtilPath.getTopspinHome()+ '/exp/stan/nmr/py/BioPY/modules/')

import LoadExp as Load
import TS_Version as Ver

WdB="W"
if Ver.get()[1] == "2": WdB="dB"

cmds=argv
# JAVA GUI 


Load.CCpanel()


"""
# define a frame with buttons
button1 = JButton('FT', actionPerformed = execute_ft) 
button2 = JButton('TD', actionPerformed = get_td)
frame = JFrame('TopSpin / Python GUI Example') # create window with title
frame.setSize(200, 100) # set window size x, y
frame.setLayout(FlowLayout()) # layout manager for horizontal alignment
frame.add(button1)
frame.add(button2)
frame.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE)
frame.setVisible(True)  SELECT("Holy Buttons Batman","Stuff",\
         ["Continue", "Finished","Button1","Button2"]) == 1

# Variables to track merged elements
Hhp, Chp, Nhp, HDec, hC, hN, NCa, NCo, CH, hhC, Nh, CX = 0,0,0,0,0,0,0,0,0,0,0,0
MAS, Phases = 0,0

########################
#  Read in preferences #
########################
i=2
if len(cmds) <= 2 : help()
if len(cmds) >= 2 :

	for cmd in cmds[1:]:
	  
	  if cmd.find('-1D') >=0 or cmd.find('-1d') >=0:
		nD=1
	  if cmd.find('-2D') >=0 or cmd.find('-2d') >=0:
		nD=2
	  if cmd.find('-3D') >=0 or cmd.find('-3d') >=0:
		nD=3
	  if cmd.find('-ex') >=0 or cmd.find('-EXPNO') >=0 or cmd.find('-EX') >=0 :
		expno=int(cmds[i])
		SkipFileDialog=1
	  if cmd.find('-q') >=0 or cmd.find('-Q') >=0 or cmd.find('-qt') >=0 or cmd.find('-QT') >=0 :
		quiet=1
	  i=i+1


"""