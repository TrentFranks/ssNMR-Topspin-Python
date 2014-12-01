"""
Bruker vs FMP pulse sequence conventions

W.T.Franks FMP Berlin
"""
import TopCmds
import CPDtools

# pulses
pC90  ="P 1";  pC180="P 2"
pH90  ="P 3";  pH180="P 4"
pN90  ="P 21"; pN180="P 22"
pHC   ="P 10"
pHN   ="P 11"
pNCA  ="P 16";  pNCO  ="P 16"
pCAe  ="P 6";   pCOe  ="P 7"
pCAr  ="P 8";   pCOr  ="P 9"
pCH   ="P 12";  pNH   ="P 13"; phhC  ="P 14"

pHmissi  ="P 18"
pH2Oe ="P 23";  pH2Or ="P 24"; 
pHoffres_e="P 25";  pHoffres_r="P 26"; 

#Shapes
sChc   ="SPNAM 0";  sHhc  ='None"
sNhn   ="SPNAM 1";  sHhn  ='None"
sNCA   ="SPNAM 2";  sNCO  ="SPNAM 2"
sCAe   ="SPNAM 6";  sCOe  ="SPNAM 7"
sCAr   ="SPNAM 8";  sCOr  ="SPNAM 9"
sCch   ="SPNAM 12"; sNnh  ="SPNAM 13"; sChhc  ="SPNAM 14"
sHch   ="None"    ; sHnh  ="None"    ; sHhhc  ="None"

#Powers
aC="PL 1"
aH="PL 2"
aN="PL 21"

aCnca ="PL 6";  aCnco ="PL 6"
aNnca ="PL 7";  aNnco ="PL 7"
aHmissi="PL 9"
aHhc  ="PL 10";  aHhn  ="PL 11"
aChc  ="PL 20";  aNhn  ="PL 19"
aHdec ="PL 12";  aHdec2="PL 13";  aHdec3="PL 14"
aCc5  ="PL 15"
aCc7  ="PL 17"
aCc7  ="PL 17"
aNhn  ="PL 19";  aChc  ="PL 20"

aCAe  ="PL 26";  aCOe  ="PL 27"
aCAr  ="PL 28";  aCOr  ="PL 29"

#Decoupling
prgHDec=TopCmds.GETPAR2("CPDPRG 2")
if prgHDec != "None" and prgHDec != "" :
  aHdec, pHdec = CPDtools.CPDparse(prgHDec,"1H")

prgNDec=TopCmds.GETPAR2("CPDPRG 3")
if prgNDec != "None" and prgNDec != "" :
  aNdec, pNdec = CPDtools.CPDparse(prgHDec,"15N")

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


pulDict = {'pC90':pC90,'pC180':pC180,'pH90':pH90,'pH180':pH180,'pN90':pN90,'pN180':pN180,\
           'pHC':pHC,'pHN':pHN,'pNCA':pNCA,'pNCO':pNCO,'pCH':pCH,'pNH':pNH,'phhC':phhC,\
           'pCAe':pCAe,'pCOe':pCOe,'pCAr':pCAr,'pCOr':pCOr,\
           'pH2Oe':pH2Oe,'pH2Or':pH2Or,'pHoffres_e':pHoffres_e,'pHoffres_r':pHoffres_r,'pHmissi':pHmissi,\
           
           'sCAe':sCAe,'sCOe':sCOe,'sCAr':sCAr,'sCOr':sCOr,\
           'sChc':sChc,'sHhc':sHhc,'sNhn':sNhn,\
           'sHhn':sHhn,'sCnca':sCnca,'sCnco':sCnco,\
           'sCch':sCch,'sNnh':sNnh,'sChhc':sChhc,\
           'sHch':sHch,'sHnh':sHnh,'sHhhc':sHhhc,\

           'aC':aC,'aH':aH,'aN':aN,'aChc':aChc,'aHhc':aHhc,'aNhn':aNhn,\
           'aChc':aChc,'aHhc':sHhc,'aNhn':sNhn,'aHhn':aHhn,\
           'aCnca':aCnca,'aCnco':aCnco,'aNnca':aNnca,'aNnco':aNnco,\
           'aCch':aCch,'aNnh':aNnh,'aChhc':aChhc,'aHch':aHch,'aHnh':aHnh,'aHhhc':aHhhc,\
           'aHdec':aHdec,'aHdec2':aHdec2,'aHdec3':aHdec3,\
           'aCc5':aCc5,'aCc7':aCc7,'aCc7':aCc7,'aCAe':aCAe,'aCOe':aCOe,'aCAr':aCAr,'aCOr':aCOr,\
           'lRFDR':lRFDR,'lREDOR':lREDOR,'lC5':lC5,'lC7':lC7,'lTOBSY':lTOBSY,\
           
           'dT1':dT1,'dHC':dHC,'dHC2':dHC2,'decho':decho,'dmix':dmix,'dmix2':dmix2,\
           'dSat':dSat,'dCC':dCC,'dCC2':dCC2,'dNC':dNC,'dHN':dHN,'dHN2':dHN2,'MAS':MAS}

def setPar(parName, value, unit) :

  TopSpinName = pulDict[parName]
  j=TopSpinName.find(" ")
  TopCmds.MSG(TopSpinName[:j]+unit+TopSpinName[j:],str(value))
  #TopCmds.PUTPAR(TopSpinName[:j]+unit+TopSpinName[j:],str(value))
  
