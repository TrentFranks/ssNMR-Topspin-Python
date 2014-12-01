# Simple GUI example
from javax.swing import *
from java.awt import *
def execute_ft(event):
      # execute command "ft" in a command thread
      EXEC_PYSCRIPT('XCMD("ft", 0)')
def get_td(event): # executes TD button
      # get TD and save it as a global property "MY_TD" of TopSpin
      ct = EXEC_PYSCRIPT('root.Globals.globalProp.setProperty("MY_TD",GETPAR("TD"))')
      ct.join() # wait until EXEC_PYSCRIPT is done
      td = root.Globals.globalProp.getProperty("MY_TD") # get "MY_TD" back from the globals properties
      EXEC_PYSCRIPT('MSG(str(' + td + '))') # show message dialog


# define a frame with buttons
button1 = JButton('FT', actionPerformed = execute_ft) 
button2 = JButton('TD', actionPerformed = get_td)
frame = JFrame('TopSpin / Python GUI Example') # create window with title
frame.setSize(200, 100) # set window size x, y
frame.setLayout(FlowLayout()) # layout manager for horizontal alignment
frame.add(button1)
frame.add(button2)
frame.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE)
frame.setVisible(True)