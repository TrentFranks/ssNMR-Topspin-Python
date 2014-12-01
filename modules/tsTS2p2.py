"""
Bruker vs FMP pulse sequence conventions

W.T.Franks FMP Berlin
"""
import TopCmds
import CPDtools

# pulses
pC90  ="P 1";   pC180 ="P 2"
pH90  ="P 3";   pH180 ="P 4"
pN90  ="P 21";  pN180 ="P 22"
pD90  ="P 32";  pD180 ="P 33"
pHC   ="P 15";  pHN   ="P 25"
pNCA  ="P 16";  pNCO  ="P 17"
pCH   ="P 48";  pNH   ="P 46"; phhC  ="P 44"

# Carbon soft pulses
pCAe  ="P 6";   pCOe  ="P 7"
pCAr  ="P 8";   pCOr  ="P 9"

# Proton detection soft pulses
pHmissi  ="P 18"
pH2Oe ="P 23";  pH2Or ="P 24"; 
pHoffres_e="P 25";  pHoffres_r="P 26"; 

#Shapes
sChc   ="SPNAM 41";  sHhc  ="SPNAM 40"
sNhn   ="SPNAM 43";  sHhn  ="SPNAM 42"
sCnca  ="SPNAM 50";	 sCnco ="SPNAM 51"
sCAe   ="SPNAM 6" ;  sCOe  ="SPNAM 7"
sCAr   ="SPNAM 8" ;  sCOr  ="SPNAM 9"
sCch   ="None"    ;  sNnh  ="None"        ; sChhc  ="None"
sHch   ="SPNAM 48";  sHnh  ="SPNAM 46"    ; sHhhc  ="SPNAM 44"
sCdrm  ="SPNAM 52"

#Powers
aC="PL 1"
aH="PL 2"
aN="PL 21"
aD="PL 32"


aNnca ="PL 5" ;  aCnca ="SP 50" ;  aHnca ="SP 33";
aNnco ="PL 6" ;  aCnco ="SP 51" ;  aHnco ="SP 34";
aHmissi="PL 9"
aHhc  ="SP 40";  aHhn  ="SP 42"; aChc  ="SP 41";  aNhn  ="SP 43"
aHch  ="SP 48";  aHnh  ="SP 46"; aCch  ="PL 49";  aNnh  ="PL 19"
aHhhc ="SP 44";  aChhc ="PL 45"; aHnca ="PL 33";  aHnco ="PL 34"

aHdec ="PL 12";  aHdec2="PL 13";  aHdec3="PL 14"; aHdarr="PL 14"
aNdec ="PL 3" ;  aCdec ="PL 4" ;  aDdec ="PL 25"
aCc5  ="PL 15"
aCc7  ="PL 17"
aCc7  ="PL 17"

aCAe  ="PL 26";  aCOe  ="PL 27"
aCAr  ="PL 28";  aCOr  ="PL 29"

#Decoupling
prgCDec="CPDPRG 4"; prgHDec="CPDPRG 2"; prgNDec="CPDPRG 3"; prgDDec="CPDPRG 4"
pcpdC="PCPD 4"  ; pcpdH  ="PCPD 2"; pcpdN="PCPD 3"; pcpdD="PCPD 5"

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
dDarr ="D 8"

#Offsets
oCA  ="CNST 22";oCO  ="CNST 21"

#Experiment info
MAS = "CNST 31"

pulDict = {'pC90':pC90,'pC180':pC180,'pH90':pH90,'pH180':pH180,'pN90':pN90,'pN180':pN180,'pD90':pD90,'pD180':pD180,\
           'pHC':pHC,'pHN':pHN,'pNCA':pNCA,'pNCO':pNCO,'pCH':pCH,'pNH':pNH,'phhC':phhC,\
           'pCAe':pCAe,'pCOe':pCOe,'pCAr':pCAr,'pCOr':pCOr,\
           'pH2Oe':pH2Oe,'pH2Or':pH2Or,'pHoffres_e':pHoffres_e,'pHoffres_r':pHoffres_r,'pHmissi':pHmissi,\
           'sCAe':sCAe,'sCOe':sCOe,'sCAr':sCAr,'sCOr':sCOr,\
           'sChc':sChc,'sHhc':sHhc,'sNhn':sNhn,\
           'sHhn':sHhn,'sCnca':sCnca,'sCnco':sCnco,\
           'sCch':sCch,'sNnh':sNnh,'sChhc':sChhc,\
           'sHch':sHch,'sHnh':sHnh,'sHhhc':sHhhc,\
           'aC':aC,'aH':aH,'aN':aN,'aChc':aChc,'aHhc':aHhc,'aNhn':aNhn,'aHhn':aHhn,'aHdarr':aHdarr,\
           'aC90':aC,'aH90':aH,'aN90':aN,\
           'aCnca':aCnca,'aCnco':aCnco,'aNnca':aNnca,'aNnco':aNnco,\
           'aCch':aCch,'aNnh':aNnh,'aChhc':aChhc,'aHch':aHch,'aHnh':aHnh,'aHhhc':aHhhc,\
           'aHdec':aHdec,'aHdec2':aHdec2,'aHdec3':aHdec3,'aHnca':aHnca,'aHnco':aHnco,\
           'aCc5':aCc5,'aCc7':aCc7,'aCc7':aCc7,'aCAe':aCAe,'aCOe':aCOe,'aCAr':aCAr,'aCOr':aCOr,\
           'lRFDR':lRFDR,'lREDOR':lREDOR,'lC5':lC5,'lC7':lC7,'lTOBSY':lTOBSY,\
           'dT1':dT1,'dHC':dHC,'dHC2':dHC2,'decho':decho,'dmix':dmix,'dmix2':dmix2,\
           'dSat':dSat,'dCC':dCC,'dCC2':dCC2,'dNC':dNC,'dHN':dHN,'dHN2':dHN2,'dDarr':dDarr,'MAS':MAS,\
           'prgHDec':prgHDec,'prgNDec':prgNDec,'pcpdC':pcpdC, 'pcpdH':pcpdH, 'pcpdN':pcpdN, 'pcpdD':pcpdD,\
           'oCA':oCA,'oCO':oCO}

def xcmd_name(par):
  if par in pulDict:
    Name = pulDict[par]
  else:
    Name=par
  while Name.find(" ") >=0 :
    j=Name.find(" ")
    Name=Name[:j]+Name[j+1:]
  Name=Name.lower()
  
  return Name
  

def SetPar(parName, value, unit) :

  if parName in pulDict:
    TopSpinName = pulDict[parName]
  else:
    TopSpinName=parName

  TopCmds.PUTPAR(TopSpinName,str(value))
  
def GetPar(parName, unit) :

  Thing =""
  Thing =1.

  if parName in pulDict:
    TopSpinName = pulDict[parName]
  else:
    TopSpinName=parName
  
  if TopSpinName.find("NAM") >= 0 or TopSpinName.find("PRG") >=0 :
    Thing= TopCmds.GETPAR(TopSpinName)

  else:
    Thing= float(TopCmds.GETPAR(TopSpinName))

  return Thing
  
