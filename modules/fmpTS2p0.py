"""
FMP pulse sequence conventions

W.T.Franks FMP Berlin
"""
import TopCmds, sys

pulDict = {\
#Hard Pulses
'aC'     :'PL 1'    ,'pC90'   :'P 1'     ,'pC180' :'P 2'      ,\
'aH'     :'PL 2'    ,'pH90'   :'P 3'     ,'pH180' :'P 4'      ,\
'aN'     :'PL 21'   ,'pN90'   :'P 21'    ,'pN180' :'P 22'     ,\
'aD'     :'PL 32'   ,'pD90'   :'P 32'    ,'pD180' :'P 33'     ,\
#Normal CP
'pHC'    :'P 10'    ,'aHhc'   :'PL 20'   ,'aChc'   :'PL 10'   ,\
'sChc'   :'SPNAM 0' ,'sHhc'   :'Unused'  ,
'pHN'    :'P 11'    ,'aHhn'   :'PL 19'   ,'aNhn'   :'PL 11'   ,\
'sNhn'   :'SPNAM 1' ,'sHhn'   :'Unused'  ,\
'pCH'    :'P 12'    ,'aHch'   :'PL 20'   ,'aCch'   :'PL 10'   ,\
'sCch'   :'SPNAM 12','sHch'   :'Unused'  ,\
'pNH'    :'P 13'    ,'aHnh'   :'PL 19'   ,'aNnh'   :'PL 11'   ,\
'sNnh'   :'SPNAM 13','sHnh'   :'Unused'  ,\
'phhC'   :'P 14'    ,'aHhhc'  :'PL 20'   ,'aChhc'  :'PL 10'   ,\
'sChhc'  :'SPNAM 14','sHhhc'  :'Unused'  ,\
#NC CP
'pNCA'   :'P 15'    ,'aNnca'  :'PL 7'    ,'aCnca'  :'PL 6'    ,'aHnca'  :'PL 13'   ,\
'sCnca'  :'SPNAM 2' ,'sNnca'  :'Unused'  ,\
'pNCO'   :'P 15'    ,'aNnco'  :'PL 7'    ,'aCnco'  :'PL 6'    ,'aHnco'  :'PL 13'   ,\
'sCnco'  :'SPNAM 2' ,'sNnco'  :'Unused'  ,\
#Secondary CP
'pCH2'   :'P 12'    ,'aHch2'  :'PL 23'   ,'aCch2'  :'PL 22'   ,\
'sCch2'  :'Unused'  ,'sHch2'  :'SPNAM 12',\
'pNH2'   :'P 13'    ,'aHnh2'  :'PL 25'   ,'aNnh2'  :'PL 24'   ,\
'sNnh2'  :'Unused'  ,'sHnh2'  :'SPNAM 13',\
#LG
#LG Pulses
'pFSLG'  :'P 5'     ,'aHfslg' :'PL 13'   ,'pHMA'   :'P 62'    ,'pHcMA'  :'P 63'    ,\
'lFSLG'  :'L 10'    ,'fFSLG'  :'CNST 40' ,\
'oFSLGc' :'CNST 48' ,'oFSLGp' :'CNST 50' ,'oFSLGm' :'CNST 49' ,\
#LG CP
'pHCLG'  :'P 10'    ,'aHhcLG' :'PL 20'   ,'aChcLG' :'PL 10'   ,\
'sChcLG' :'SPNAM 0' ,'sHhcLG' :'Unused'  ,\
'fHhcLG' :'CNST 41' ,'oHhcLG' :'CNST 51' ,\
'pHNLG'  :'P 11'    ,'aHhnLG' :'PL 19'   ,'aNhnLG' :'PL 11'   ,\
'sNhnLG' :'SPNAM 1' ,'sHhnLG' :'Unused'  ,\
'fHhnLG' :'CNST 42' ,'oHhnLG' :'CNST 52' ,\
#Offsets
'oCA'    :'CNST 11' ,'oCO'    :'CNST 10' ,'uoffs'  :'Hz'     ,\
#Soft Pulses
'pCAe'   :'P 6'     ,'sCAe'   :'SPNAM 6' ,'aCAe'   :'PL 26'   ,'oCAe'   :'CNST 22' ,\
'pCOe'   :'P 7'     ,'sCOe'   :'SPNAM 7' ,'aCOe'   :'PL 27'   ,'oCOe'   :'CNST 21' ,\
'pCAr'   :'P 8'     ,'sCAr'   :'SPNAM 8' ,'aCAr'   :'PL 28'   ,'oCAr'   :'CNST 22' ,\
'pCOr'   :'P 9'     ,'sCOr'   :'SPNAM 9' ,'aCOr'   :'PL 29'   ,'oCOr'   :'CNST 21' ,\
'pHh2oe' :'P 23'    ,\
'pHh2or' :'P 24'    ,\
'pHnh_e' :'P 25'    ,\
'pHnh_r' :'P 26'    ,\
#CC Mixing
#PDSD/DARR/RAD
'aHdarr' :'PL 14'   ,'aHDarr' :'PL 14'   ,'dDarr'  :'D 8'     ,\
#RFDR
'lRFDR'  :'L 3'     ,\
#SPC5
'aCc5'   :'PL 15'   ,'lC5'    :'L 5'     ,\
#POST C7
'aCc7'   :'PL 17'   ,'lC7'    :'L 7'     ,\
#TOBSY (C931)
'aCc9'   :'PL 19'   ,'lTOBSY' :'L 9'     ,\
#Adiabatic pulse TOBSY
'aCadb'  :'PL 16'   ,'sCadb'  :"SPNAM 6" ,\
#DREAM
'pCdrm'  :'P 20'    ,'aCdrm'  :'PL 23'   ,'sCdrm'  :'SPNAM 20','oCdrm'  :'CNST 2'  ,\
'aHdrmDC':'PL 13'   ,\
#EXPORT
'sCexp'  :'SPNAM 20',
'sNexp'  :'SPNAM 21',\
#DUO
#Band Selective Homonuclear CP
'pCbsh'  :'P 50'    ,'aCbsh'  :'SP 26'   ,'sCbsh'  :'SPNAM 15','aHbshDc':'PL 13'   ,\
'pCbshFlp':'P 28'   ,'pCbsh2kFlp':'P 29' ,\
#NC Mixing
#REDOR/TEDOR
'lREDOR' :'L 4'     ,
#Decoupling
'aHdec'  :'PL 12'   ,'aHdec2' :'PL 13'   ,'aHdec3' :'PL 14'   ,\
'prgHDec':'CPDPRG 2','pcpdH'  :'PCPD 2'  ,\
'aCdec'  :'PL 4'    ,'prgCDec':'CPDPRG 4','pcpdC'  :'PCPD 4'  ,\
'aNdec'  :'PL 3'    ,'prgNDec':'CPDPRG 3','pcpdN'  :'PCPD 3'  ,\
'aDdec'  :'PL 25'   ,'prgDDec':'CPDPRG 4','pcpdD'  :'PCPD 5'  ,\
#Solvent Supression
'aHms'   :'PL 9'    ,'pHms'   :'P 18'    ,\
#INEPT and other delays
'dT1'    :'D 1'     ,'decho'  :'D 6'     ,'dmix'   :'D 8'     ,'dmix2'  :'D 9'     ,\
'dHC'    :'D 4'     ,'dHC2'   :'D 5'     ,'dHN'    :'D 26'    ,'dHN2'   :'D 27'    ,\
'dCC'    :'D 21'    ,'dCC2'   :'D 22'    ,'dNC'    :'D 23'    ,'dNC2'   :'D 24'    ,\
'dSat'   :'D 18'    ,\
#Miscellaneous
'MAS'    :'CNST 31' \
}
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

  if pulDict.has_key(parName):
  # "has_key" is needed for Python 2.0 
  #if parName in pulDict:
    TopSpinName = pulDict[parName]
    if TopSpinName.find("NAM") >= 0 or TopSpinName.find("PRG") >=0 :
      TopSpinName=TopSpinName.replace(" ","")
  else:
    TopSpinName=parName

   if TopSpinName != "Unused":
    TopCmds.PUTPAR(TopSpinName,str(value))
  
def GetPar(parName, unit) :

  Thing =""
  Thing =1.
  # "has_key" is needed for Python 2.1 
  #if parName in pulDict:
  #pver=sys.version_info
  #TopCmds.MSG(str(pver))
  
  if pulDict.has_key(parName):
    TopSpinName=pulDict[parName]
  else:
    TopSpinName=parName

  if TopSpinName.find("NAM") >= 0 or TopSpinName.find("PRG") >=0 :
    TopSpinName=TopSpinName.replace(" ","")
    Thing= TopCmds.GETPAR(TopSpinName)
  
  elif TopSpinName.find("Unused") >=0 :
    Thing= "Unused"

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
    if found==0:
      if name.find(str(i)) >=0:
        j=name.find(str(i))
        found=1
  if found==1:
    Format=name[:j]+" "+name[j:]
  if found==0:
    Format=name
  return Format
