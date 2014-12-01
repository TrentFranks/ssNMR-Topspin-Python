"""
Computes an R2T pulse shape:
W.T. Franks FMP Berlin
R2T match condition is [1 or 2]*wr - W_I_eff - W_S_eff = 0
"""
import sys
sys.path.append(root.UtilPath.getTopspinHome()+ '/exp/stan/nmr/py/BioPY/modules/')

import R2T

Shape=R2T.dialog()
Scale=R2T.find_match(Shape)
Names=R2T.name_confirm(Shape)
Wave =R2T.make(Scale,Shape,Names)
