"""
Computes various amplitudes
W.T. Franks FMP Berlin
"""
import math
import sys
sys.path.append(root.UtilPath.getTopspinHome()+ '/exp/stan/nmr/py/BioPY/modules/')

import Setup

MAS=float(GETPAR("CNST 31"))
TauR= 1000./MAS

# Double the time each step, unless we go over 10ms, then adjust accordingly

Text = []
i=1
Time= TauR

Ntr=math.floor(10./Time)

MSG("N_TauR possible  "+str(Ntr))

dbl=1
k=0
while dbl*2 <= Ntr:
  dbl=dbl*2
  k=k+1

if k>=7: mult=2.,4.,8.,16.,32.,64.,128.  
if k==6: mult=2.,4.,8.,16.,32.,48.,64.  
if k==5: mult=2.,4.,8.,12.,16.,24.,32.
if k==4: mult=2.,4.,6., 8.,10.,12.,16.
if k<=3:
  MSG("Spinning, or CNST31 set too low, cannot generate list./n  Exiting")
  EXIT()  

Text.append('0.001m')
MSG(str(Text))

i=1
while i<8:
  Time=mult[i-1]*TauR
  i=i+1
  MSG(str('%6.3f' %Time))
  Text.append(str('%6.3f' %Time)+'m')

MSG(str(Text))
EXIT()
