"""
Computes a TANGENT pulse shape with defined Start and End
Supply d, b, and sp to silence Interaction
W.T. Franks FMP Berlin

Arguments:
-sp:shaped pulse name
-d : delta (+/- d%)
-b : beta (curvature) 
-p : number of points (default 1000) ""
-np: number of points
-sc: number of points
-name : specify name
"""

import sys
from sys import argv
sys.path.append(root.UtilPath.getTopspinHome()+ '/exp/stan/nmr/py/BioPY/modules/')
import Setup, Help
import Tangent

par=[]
d="0"
b="0"
np="1000"
sc="100."
nom="None"
sp="None"

Interactive=1

cmds=argv

i=0
while i < len(cmds):
  #print cmds[i]
  if cmds[i].find('-d') >=0: d=cmds[i+1]
  if cmds[i].find('-b') >=0: b=cmds[i+1]
  if cmds[i].find('-p') >=0: np=cmds[i+1]
  if cmds[i].find('-np') >=0: np=cmds[i+1]
  if cmds[i].find('-sc') >=0: sc=cmds[i+1]
  if cmds[i].find('-name') >=0: nom=cmds[i+1]
  if cmds[i].find('-sp') >=0: 
    sp=cmds[i+1]
    if sp.find("SPNAM") <= 0:
      sp="SPNAM "+sp
    else:
      sp="SPNAM "+sp[sp.find("M"):]
  i=i+1

if sc=="100.":
  sc=100.-float(d)
if d !="0" and b!="0" and sp != "None":
  Interactive=0

Shape=sc,np,d,b

if Interactive == 1:
  Shape=Tangent.dialog()
  Name =Tangent.name(Shape,sp)
  Wave =Tangent.make(Name,Shape[0],Shape[1],Shape[2],Shape[3])
else:
  if nom == "None": 
    nom=Tangent.name(Shape,sp)
  if sp != "None": PUTPAR(sp,nom)
  Wave =Tangent.make(nom,sc,np,d,b)
