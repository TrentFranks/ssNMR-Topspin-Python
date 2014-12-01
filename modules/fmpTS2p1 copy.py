"""
Bruker vs FMP pulse sequence conventions

W.T.Franks FMP Berlin
"""
import TopCmds
import sys

pulDict = {\
#pulses
'pC90'   :'P 1'     , 'pC180' :'P 2'     ,'pH90'   :'P 3'     , 'pH180' :'P 4'     ,\
'pN90'   :'P 21'    , 'pN180' :'P 22'    ,'pD90'   :'P 32'    , 'pD180' :'P 33'    ,\
'pHC'    :'P 10'    , 'pHN'   :'P 11'    ,'pNCA'   :'P 15'    , 'pNCO'  :'P 15'    ,\
'pCH'    :'P 12'    , 'pNH'   :'P 13'    ,'phhC'   :'P 14'    ,\
'pCAe'   :'P 6'     , 'pCOe'  :'P 7'     ,'pCAr'   :'P 8'     ,'pCOr'   :'P 9'     ,\
'pHh2oe' :'P 23'    ,'pHh2or' :'P 24'    ,'pHnh_e' :'P 25'    ,'pHnh_r' :'P 26'    ,\
'pcpdC'  :'PCPD 4'  ,'pcpdH'  :'PCPD 2'  ,'pcpdN'  :'PCPD 3'  ,'pcpdD'  :'PCPD 5'  ,\
'pHms'   :'P 18'    ,\
#shapes
'sChc'   :'SPNAM 0' ,'sHhc'   :'Unused'  ,'sNhn'   :'SPNAM 1' ,'sHhn'   :'Unused'  ,\
'sCnca'  :'SPNAM 2' ,'sCnco'  :'SPNAM 2' ,'sNnca'  :'Unused'  ,'sNnco'  :'Unused'  ,\
'sCAe'   :'SPNAM 6' ,'sCOe'   :'SPNAM 7' ,'sCAr'   :'SPNAM 8' ,'sCOr'   :'SPNAM 9' ,\
'sCch'   :'SPNAM 12','sNnh'   :'SPNAM 13','sChhc'  :'SPNAM 14',\
'sHch'   :'Unused'  ,'sHnh'   :'Unused'  ,'sHhhc'  :'Unused'  ,\
'sCdrm'  :'SPNAM 5' ,'sCadb'  :"SPNAM 6" ,'sCexp'  :'SPNAM 20','sNexp'  :'SPNAM 21',\
#powers (amplitudes)
'aC'     :'PL 1'    ,'aH'     :'PL 2'    ,'aN'     :'PL 21'   ,'aD'     :'PL 32'   ,\
'aNnca'  :'PL 7'    ,'aCnca'  :'PL 6'    ,'aHnca'  :'PL 13'   ,'aHdarr' :'PL 14'   ,\
'aNnco'  :'PL 7'    ,'aCnco'  :'PL 6'    ,'aHnco'  :'PL 13'   ,\
'aHhc'   :'PL 20'   ,'aHhn'   :'PL 19'   ,'aHch'   :'PL 20'   ,'aHnh'   :'PL 19'   ,\
'aChc'   :'PL 10'   ,'aNhn'   :'PL 11'   ,'aCch'   :'PL 10'   ,'aNnh'   :'PL 11'   ,\
'aHhhc'  :'PL 20'   ,'aChhc'  :'PL 10'   ,\
'aHdec'  :'PL 12'   ,'aHdec2' :'PL 13'   ,'aHdec3' :'PL 14'   ,\
'aNdec'  :'PL 3'    ,'aCdec'  :'PL 4'    ,'aDdec'  :'PL 25'   ,\
'aCc5'   :'PL 15'   ,'aCc7'   :'PL 17'   ,'aCc9'   :'PL 19'   ,\
'aHc5'   :'PL 15'   ,'aCc7'   :'PL 17'   ,'aCc9'   :'PL 19'   ,\
'aCAe'   :'PL 26'   ,'aCOe'   :'PL 27'   ,'aCabd'  :'PL 16'   ,\
'aCAr'   :'PL 28'   ,'aCOr'   :'PL 29'   ,\
'aHms'   :'PL 9'    ,'aHDarr' :'PL 16'   ,\
#Programs and loops
'prgCDec':'CPDPRG 4','prgHDec':'CPDPRG 2','prgNDec':'CPDPRG 3','prgDDec':'CPDPRG 4',\
'lRFDR'  :'L 3'     ,'lREDOR' :'L 4'     ,'lC5'    :'L 5'     ,'lC7'    :'L 7'     ,\
'lTOBSY' :'L 9'     ,\
#delays
'dT1'    :'D 1'     ,'decho'  :'D 6'     ,'dmix'   :'D 8'     ,'dmix2'  :'D 9'     ,\
'dHC'    :'D 4'     ,'dHC2'   :'D 5'     ,'dHN'    :'D 26'    ,'dHN2'   :'D 27'    ,\
'dCC'    :'D 21'    ,'dCC2'   :'D 22'    ,'dNC'    :'D 23'    ,'dNC2'   :'D 24'    ,\
'dSat'   :'D 18'    ,'dDarr'  :'D 8'     ,\
#Offsets and Frequency Units
'oCA'    :'CNST 22' ,'oCO'    :'CNST 21' ,'oCdrm'  :'CNST 2'  , 'uoffs' :'ppm'     ,\
'oCAe'   :'CNST 22' ,'oCOe'   :'CNST 21' ,'oCAr'   :'CNST 22' , 'oCOr'  :'CNST 21' ,\
#Magic angle pulses
'pHMA'   :'P 62'    ,'pHcMA'  :'P 63'    ,\
#Freq-Switched Lee-Goldburg
'pFSLG'  :'P 5'     ,'aHfslg' :'PL 13'   ,'lFSLG'  :'L 10'    ,\
#field,              center shift,        plus offs,           minus offs
'fFSLG'  :'CNST 20' ,'oFSLGc' :'CNST 24' ,'oFSLGp' :'CNST 22' ,'oFSLGm' :'CNST 23' ,
#Lee-Goldburg CP
'pHCLG'  :'P 10'    , 'pHNLG' :'P 11'    ,'fHhcLG' :'CNST 62' ,'fHhnLG' :'CNST 63' ,\
'sChcLG' :'SPNAM 0' ,'sHhcLG' :'Unused'  ,'sNhnLG' :'SPNAM 1' ,'sHhnLG' :'Unused'  ,\
'aChcLG' :'PL 10'   ,'aHhcLG' :'PL 20'   ,'aNhnLG' :'PL 11'   ,'aHhnLG' :'PL 19'   ,\
'oHhcLG' :'CNST 25' ,'oHhnLG' :'CNST 26' ,\
#Miscellaneous
'MAS'    :'CNST 31' \
}

def xcmd_name(par):
  if pulDict.has_key(par):
    Name = pulDict[par]
  else:
    Name=par
  while Name.find(" ") >=0 :
    j=Name.find(" ")
    Name=Name[:j]+Name[j+1:]
  Name=Name.lower()
  
  return Name
  
def SetPar(parName, value, unit) :

  if pulDict.has_key(parName):
  # "has_key" is needed for Python 2.0 
  #if parName in pulDict:
    TopSpinName = pulDict[parName]
    if TopSpinName.find("NAM") >= 0 or TopSpinName.find("PRG") >=0 :
      TopSpinName=TopSpinName.replace(" ","")
  else:
    name=parName
    TopSpinName=pp_2_xcmd(name,unit)

  if TopSpinName != "Unused":
    TopCmds.PUTPAR(TopSpinName,str(value))
  
def GetPar(parName, unit) :

  Thing =""
  Thing =1.

  if pulDict.has_key(parName):
  # "has_key" is needed for Python 2.0 
  #if parName in pulDict:
    TopSpinName = pulDict[parName]
  else:
    TopSpinName = parName
  
  if TopSpinName.find("NAM") >= 0 or TopSpinName.find("PRG") >=0 :
    TopSpinName=TopSpinName.replace(" ","")
    Thing=TopCmds.GETPAR(TopSpinName)
    
  elif TopSpinName.find("Unused") >=0 :
    Thing="Unused"
  
  else:
  
    Thing= float(TopCmds.GETPAR(TopSpinName))

  return Thing
  
def pp_2_xcmd(name,Unit):
  found=0 
  name=name.upper()
  name=name.rstrip()
  
  if name.find("PL")>=0:
    name=name[:2]+Unit+name[2:]
  j=len(name)
  
  for i in range(0,9):
    if name.find(str(i)) >=0:
      found=1
      if name.find(str(i))<j:
        j=name.find(str(i))
  if found==1:
    Format=name[:j]+" "+name[j:]
  if found==0:
    Format=name
  return Format
