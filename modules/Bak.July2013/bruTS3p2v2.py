"""
Bruker vs FMP self.pulse sequence conventions

W.T.Franks FMP Berlin
"""
import TopCmds
import CPDtools

class lib:
  __init__(self,name):
    self.name=name
    
    # self.pulses
    self.pC90  ="P 1";   self.pC180 ="P 2"
    self.pH90  ="P 3";   self.pH180 ="P 4"
    self.pN90  ="P 21";  self.pN180 ="P 22"
    self.pD90  ="P 32";  self.pD180 ="P 33"
    self.pHC   ="P 15";  self.pHN   ="P 25"
    self.pNCA  ="P 16";  self.pNCO  ="P 17"
    self.pCAe  ="P 6";   self.pCOe  ="P 7"
    self.pCAr  ="P 8";   self.pCOr  ="P 9"
    self.pCH   ="P 12";  self.pNH   ="P 13"; self.phhC  ="P 14"

    self.pHmissi  ="P 18"
    self.pH2Oe ="P 23";  self.pH2Or ="P 24"; 
    self.pHoffres_e="P 25";  self.pHoffres_r="P 26"; 

    #Shapes
    self.sChc   ="SPNAM 41";  self.sHhc  ="SPNAM 40"
    self.sNhn   ="SPNAM 43";  self.sHhn  ="SPNAM 42"
    self.sCnca  ="SPNAM 50";  self.sCnco ="SPNAM 51"
    self.sCAe   ="SPNAM 6";   self.sCOe  ="SPNAM 7"
    self.sCAr   ="SPNAM 8";   self.sCOr  ="SPNAM 9"
    self.sCch   ="SPNAM 12";  self.sNnh  ="SPNAM 13"; self.sChhc  ="SPNAM 14"
    self.sHch   ="None"    ;  self.sHnh  ="None"    ; self.sHhhc  ="None"

    #Powers
    self.aC="PL 1"
    self.aH="PL 2"
    self.aN="PL 21"
    self.aD="PL 32"

    self.aCnca ="PL 6";  self.aCnco ="PL 6"
    self.aNnca ="PL 7";  self.aNnco ="PL 7"
    self.aHmissi="PL 9"
    self.aHhc  ="SP 40";  self.aHhn  ="SP 42"; self.aChc  ="SP 41";  self.aNhn  ="SP 43"
    self.aHch  ="SP 44";  self.aHnh  ="SP 46"; self.aCch  ="PL 20";  self.aNnh  ="PL 19"
    self.aHhhc ="PL 10";  self.aChhc ="PL 11"

    self.aHdec ="PL 12";  self.aHdec2="PL 13";  self.aHdec3="PL 14";  
    self.aNdec ="PL 3" ;  self.aCdec ="PL 4" ;  self.aDdec ="PL 25"
    self.aCc5  ="PL 15"
    self.aCc7  ="PL 17"
    self.aCc7  ="PL 17"
    self.aNhn  ="PL 19";  self.aChc  ="PL 20"

    self.aCAe  ="PL 26";  self.aCOe  ="PL 27"
    self.aCAr  ="PL 28";  self.aCOr  ="PL 29"

    #Decouself.pling
    self.prgCDec="CPDPRG 4"; self.prgHDec="CPDPRG 2"; self.prgNDec="CPDPRG 3"; self.prgDDec="CPDPRG 4"
    self.pcself.pdC="PCPD 4"  ; self.pcself.pdH  ="PCPD 2"; self.pcself.pdN="PCPD 3"; self.pcself.pdD="PCPD 5"

    #Looself.ps
    self.lRFDR ="L 3"
    self.lREDOR="L 4"
    self.lC5   ="L 5"
    self.lC7   ="L 7"
    self.lTOBSY="L 9"

    #Delays
    self.dT1   ="D 1"
    self.dHC   ="D 4";  self.dHC2  ="D 5"
    self.decho ="D 6"
    self.dmix  ="D 8";  self.dmix2 ="D 9"
    self.dSat  ="D 18"
    self.dCC   ="D 21"; self.dCC2  ="D 22"; self.dNC   ="D 23"
    self.dHN   ="D 26"; self.dHN2  ="D 27"

    #Exself.periment info
    self.MAS = "CNST 31"

    self.pulDict = {'pC90':pC90,'pC180':pC180,'pH90':pH90,'pH180':pH180,'pN90':pN90,'pN180':pN180,'pD90':pD90,'pD180':pD180,\
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
       'dSat':dSat,'dCC':dCC,'dCC2':dCC2,'dNC':dNC,'dHN':dHN,'dHN2':dHN2,'MAS':MAS,\
       'prgHDec':prgHDec,'prgNDec':prgNDec}


  """
  def SetPar(parName, value, unit) :

  if parName in pulDict:
  TopSpinName = pulDict[parName]
  else:
  TopSpinName=parName

  j=TopSpinName.find(" ")
  #TopCmds.MSG(TopSpinName[:j]+unit+TopSpinName[j:],str(value))

  if TopSpinName.find("NAM") >= 0 or TopSpinName.find("PRG") >=0 :
  TopCmds.PUTPAR(TopSpinName,str(value))
  else:
  TopCmds.PUTPAR(TopSpinName[:j]+unit+TopSpinName[j:],str(value))

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
  #TopCmds.MSG(TopSpinName+" is a String")

  else:
  #if TopSpinName[:j].find("NAM") < 0 or TopSpinName[:j].find("PRG") < 0 :
  Thing= float(TopCmds.GETPAR(TopSpinName[:j]+unit+TopSpinName[j:]))
  #TopCmds.MSG(TopSpinName+" is NOT a String")
  return Thing

  """