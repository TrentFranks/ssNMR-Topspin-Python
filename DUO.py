"""
Computes a TopSpin DUO wave shape:
L.A. Strassø and N.C. Nielsen
J Chem Phys 133 064501 (2010) 

WTF Adapted this for Topspin Python Interface 
from LAS tcl script provided from Anders B. Nielsen and NCN
FMP Berlin and Aarhus University
"""
import sys
sys.path.append(root.UtilPath.getTopspinHome()+ '/exp/stan/nmr/py/BioPY/modules/')

import DUO

Stuff=DUO.dialog()
name=DUO.name(Stuff)
DUO.make(Stuff,name)
