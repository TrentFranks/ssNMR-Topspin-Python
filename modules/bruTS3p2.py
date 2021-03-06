"""
Bruker vs FMP pulse sequence conventions

W.T.Franks FMP Berlin
"""
import TopCmds

pulDict = {\
#pulses
'pC90'   :'P 1'     , 'pC180' :'P 2'     ,'pH90'   :'P 3'     , 'pH180' :'P 4'     ,\
'pN90'   :'P 21'    , 'pN180' :'P 22'    ,'pD90'   :'P 32'    , 'pD180' :'P 33'    ,\
'pHC'    :'P 15'    , 'pHN'   :'P 25'    ,'pNCA'   :'P 16'    , 'pNCO'  :'P 17'    ,\
'pCH'    :'P 48'    , 'pNH'   :'P 46'    ,'phhC'   :'P 44'    ,\
'pCAe'   :'P 6'     , 'pCOe'  :'P 7'     ,'pCAr'   :'P 8'     ,'pCOr'   :'P 9'     ,\
'pHh2oe' :'P 23'    ,'pHh2or' :'P 24'    ,'pHnh_e' :'P 25'    ,'pHnh_r' :'P 26'    ,\
'pcpdC'  :'PCPD 4'  ,'pcpdH'  :'PCPD 2'  ,'pcpdN'  :'PCPD 3'  ,'pcpdD'  :'PCPD 5'  ,\
'pHms'   :'P 18'    ,\
#shapes
'sChc'   :'SPNAM 41','sHhc'   :'SPNAM 40','sNhn'   :'SPNAM 43','sHhn'   :'SPNAM 42',\
'sCnca'  :'SPNAM 50','sCnco'  :'SPNAM 51','sNnca'  :'Unused'  ,'sNnco'  :'Unused'  ,\
'sCAe'   :'SPNAM 6' ,'sCOe'   :'SPNAM 7' ,'sCAr'   :'SPNAM 8' ,'sCOr'   :'SPNAM 9' ,\
'sCch'   :"Unused"  ,'sNnh'   :"Unused"  ,'sChhc'  :"Unused"  ,\
'sHch'   :"SPNAM 48",'sHnh'   :"SPNAM 46",'sHhhc'  :"SPNAM 44",\
'sCdrm'  :'SPNAM 52','sCadb'  :"SPNAM 53",\
#powers (amplitudes)
'aC'     :'PL 1'    ,'aH'     :'PL 2'    ,'aN'     :'PL 21'   ,'aD'     :'PL 32'   ,\
'aNnca'  :'PL 5'    ,'aCnca'  :'SP 50'   ,'aHnca'  :'PL 33'   ,\
'aNnco'  :'PL 6'    ,'aCnco'  :'SP 51'   ,'aHnco'  :'PL 34'   ,\
'aHhc'   :'SP 40'   ,'aHhn'   :'SP 42'   ,'aHch'   :'SP 48'   ,'aHnh'   :'SP 46'   ,\
'aChc'   :'SP 41'   ,'aNhn'   :'SP 43'   ,'aCch'   :'SP 49'   ,'aNnh'   :'SP 47'   ,\
'aHhhc'  :'SP 44'   ,'aChhc'  :'SP 45'   ,\
'aHdec'  :'PL 12'   ,'aHdec2' :'PL 13'   ,'aHdec3' :'PL 14'   ,\
'aNdec'  :'PL 3'    ,'aCdec'  :'PL 4'    ,'aDdec'  :'PL 25'   ,'aHdarr' :'PL 14'   ,\
'aCc5'   :'PL 15'   ,'aCc7'   :'PL 17'   ,'aHc5'   :'PL 13'   ,'aHc7'   :'PL 13'   ,\
'aCAe'   :'PL 26'   ,'aCAr'   :'PL 28'   ,'aCOe'   :'PL 27'   ,'aCOr'   :'PL 29'   ,\
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
'fFSLG'  :'CNST 40' ,'oFSLGc' :'CNST 48' ,'oFSLGp' :'CNST 50' ,'oFSLGm' :'CNST 49' ,
#Lee-Goldburg CP
'pHCLG'  :'P 15'    , 'pHNLG' :'P 25'    ,'fHhcLG' :'CNST 41' ,'fHhnLG' :'CNST 42' ,\
'sChcLG' :'SPNAM 41','sHhcLG' :'SPNAM 40','sNhnLG' :'SPNAM 43','sHhnLG' :'SPNAM 42',\
'aChcLG' :'SP 41'   ,'aHhcLG' :'SP 40'   ,'aNhnLG' :'SP 43'   ,'aHhnLG' :'SP 42'   ,\
'oHhcLG' :'CNST 51' ,'oHhnLG' :'CNST 52' ,\
#Band Selective Homonuclear CP
'aCbsh'  :'SP 26'   ,'aHbshDc':'PL 13'   ,'pCbsh'  :'P 50'    ,'sCbsh'  :'SPNAM 60',\
'pCbshFlp':'P 28'   ,'pCbsh2kFlp':'P 29' ,\
#Miscellaneous
'MAS'    :'CNST 31' ,\
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

  if parName in pulDict:
    TopSpinName = pulDict[parName]
  else:
    TopSpinName=parName
  
  j=TopSpinName.find(" ")
  
  if TopSpinName != "Unused":
    #TopCmds.MSG(parName+" "+TopSpinName+" is Unused")
	if (TopSpinName.find("SP") >=0 and TopSpinName.find("NAM") <= 0) \
	or    TopSpinName.find("PL") >= 0 :
	  TopCmds.PUTPAR(TopSpinName[:j]+unit+TopSpinName[j:],str(value))
	else:
	  TopCmds.PUTPAR(TopSpinName,str(value))
  
def GetPar(parName, unit) :

  Thing =""
  Thing =1.

  if parName in pulDict:
    TopSpinName = pulDict[parName]
  else:
    TopSpinName=parName

  j=TopSpinName.find(" ")
  
  if TopSpinName.find("NAM") >= 0 or TopSpinName.find("PRG") >=0 :
    Thing= TopCmds.GETPAR2(TopSpinName)
  elif (TopSpinName.find("SP") >=0 and TopSpinName.find("NAM") <= 0) \
  or TopSpinName.find("PL") >= 0 :
    #TopCmds.MSG("TopSpinName= "+TopSpinName+"\nUnit= "+unit)
    Thing= float(TopCmds.GETPAR(TopSpinName[:j]+unit+TopSpinName[j:]))
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