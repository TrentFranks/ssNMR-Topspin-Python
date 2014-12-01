"""
Calculate actual VT temp with Ethylene Glycol

Arguments:
-u Upfield Peak
-d Downfield Peak
"""
import sys
sys.path.append('/opt/topspin2.1/exp/stan/nmr/py/user/modules/')
#sys.path.append('/opt/topspin/exp/stan/nmr/py/user/modules/')
from sys import argv

#MSG(str(argv))

Interactive=1
up=3.8
down=5.2

cmds=argv
#MSG(str(cmds))
#print len(cmds)
i=0
while i < len(cmds):
  #print cmds[i]
  if cmds[i].find('-u') >=0: 
    up=float(cmds[i+1])
    Interactive=0
  if cmds[i].find('-p') >=0: 
    down=float(cmds[i+1])
    Interactive=0
  i=i+1  

#MSG(str(Interactive))

if Interactive==1:
  index = INPUT_DIALOG("VT Calibration", "Ethylene Glycol", \
  ["Upfield Peak","Downfield Peak"],\
  [str(up),str(down)],\
  ["ppm","ppm"],\
  ["1","1"],\
  ["Accept","Close"], ['a','c'], 10)
  
  down=float(index[1])
  up=float(index[0])

TEMP = (((down-up)*(-102.24))+466.15)

MSG("Actual temperature of sample: "+str('%5.1f' %TEMP))
