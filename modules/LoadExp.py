"""
Modules to Set default parameters:
W.T. Franks FMP Berlin
"""

import de.bruker.nmr.mfw.root as root
import sys
sys.path.append(root.UtilPath.getTopspinHome()+ '/exp/stan/nmr/py/BioPY/modules/')

import math
import TopCmds
from javax.swing import *
from java.awt import *

deg=u"\u00b0"
ret=u"\u000D"
spc=u"\u0020"
unb=u"\u005f"
crt=u"\u005e"

# Actions
def DefaultMSG(event):
      TopCmds.EXEC_PYSCRIPT(str('MSG("This is Default")'))
def DefaultMSG2(event):
      TopCmds.EXEC_PYSCRIPT(str('MSG("This is Default number 2")'))


def CCpanel():
  Title= 'C-C 2D experiments'
  Buttons = ['All','C ali']
  Actions = [DefaultMSG,DefaultMSG2]
  
  pause=two_button(Title,Buttons,Actions)

# define a frame with buttons
def two_button(Title,Name,Action):
  
  button1 = JButton(Name[0], actionPerformed = Action[0]) 
  button2 = JButton(Name[1], actionPerformed = Action[1]) 

  frame = JFrame(Title) # create window with title
  frame.setSize(200, 100) # set window size x, y
  frame.setLayout(FlowLayout()) # layout manager for horizontal alignment
  frame.add(button1)
  frame.add(button2)
  frame.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE)
  frame.setVisible(True)

def Set_Cdim_All(event):
  EXEC_PYSCRIPT('TopCmds.MSG("Set_C_Dim_All", 0)')

