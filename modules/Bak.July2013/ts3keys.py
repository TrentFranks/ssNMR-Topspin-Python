"""
Bruker vs FMP pulse sequence conventions

W.T.Franks FMP Berlin
"""
import TopCmds

# pulses
pC90  ="P 1";  pC180="P 2"
pH90  ="P 3";  pH180="P 4"
pN90  ="P 21"; pN180="P 22"
pHCcp ="P 10"
pHNcp ="P 11"
pNCAcp="P 16";  pNCOcp="P 16"
pCAe  ="P 6";   pCOe  ="P 7"
pCAr  ="P 8";   pCOr  ="P 9"
pCHcp ="P 12";  pNHcp ="P 13"; phhCcp="P 14"

pHms  ="P 18"
pH2Oe ="P 23";  pH2Or ="P 24"; 
pHofre="P 25";  pHofrr="P 26"; 

#Shapes
sChccp ="SPNAM 0";  sHhccp='None"
sNhncp ="SPNAM 1";  sHhncp='None"
sNCAcp ="SPNAM 2";  sNCOcp="SPNAM 2"
sCAe   ="SPNAM 6";  sCOe  ="SPNAM 7"
sCAr   ="SPNAM 8";  sCOr  ="SPNAM 9"
sCchcp ="SPNAM 12"; sNnhcp="SPNAM 13"; sChhccp="SPNAM 14"
sHchcp ="None"    ; sHnhcp="None"    ; sChhccp="None"

keyDict = {'pC90':pC90}

def setPar(parName, value) :

  
  topSpinName = keyDict[parName]
  TopCmds.PUTPAR(topSpinName,str(value))
  

#Powers
"""
aC="PL"+units+" 1"
aH="PL"+units+" 2"
aN="PL"+units+" 21"

aCnca ="PL"+units+" 6";  aCnco ="PL"+units+" 6"
aNnca ="PL"+units+" 7";  aNnco ="PL"+units+" 7"
aHmissi="PL"+units+" 9"
aHhc  ="PL"+units+" 10";  aHhn  ="PL"+units+" 11"
aChc  ="PL"+units+" 20";  aNhn  ="PL"+units+" 19"
aHdec ="PL"+units+" 12";  aHdec2="PL"+units+" 13";  aHdec3="PL"+units+" 14"
aCc5  ="PL"+units+" 15"
aCc7  ="PL"+units+" 17"
aCc7  ="PL"+units+" 17"
aNhn  ="PL"+units+" 19";  aChc  ="PL"+units+" 20"

aCAe  ="PL"+units+" 26";  aCOe  ="PL"+units+" 27"
aCAr  ="PL"+units+" 28";  aCOr  ="PL"+units+" 29"

#Decoupling
prgHDec="CPDPRG2"
aHdec, pHdec = CPDtools.CPDparse(prgHDec)
prgNDec="CPDPRG3"
aNdec, pNdec = CPDtools.CPDparse(prgNDec)

#Loops
lRFDR ="L 3"
lREDOR="L 4"
lC5   ="L 5"
lC7   ="L 7"
lTOBSY="L 9"

#Delays
dT1   ="D 1"
dHC   ="D 4";  dHC2  ="D 5"
decho ="D 6"
dmix  ="D 8";  dmix2 ="D 9"
dSat  ="D 18"
dCC   ="D 21"; dCC2  ="D 22"; dNC   ="D 23"
dHN   ="D 26"; dHN2  ="D 27"

#Experiment info
MAS = "CNST 31"



"""