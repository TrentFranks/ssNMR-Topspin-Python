"""
Dialog/interaction for merger
W.T. Franks FMP Berlin

Must display experiment if pulling names (SP, CPD, etc)
Not needed if pulling pulses or delays

Might need to load in as a new window, maybe it helps?
"""
import de.bruker.nmr.mfw.root as root
import math
import os

import TopCmds
import MergeGet as Get
import MergePut as Put
from GetLib import pul

deg=u"\u00b0"
ret=u"\u000D"
spc=u"\u0020"

def abort(Home, Source, winfil):
  if winfil ==0 :
	TopCmds.SET_SELECTED_WIN(Source)
	TopCmds.CLOSEWIN(TopCmds.CURDATA())
	TopCmds.SET_SELECTED_WIN(Home)
	TopCmds.EXIT()
  if winfil ==1 :
	TopCmds.RE(Source)
	TopCmds.CLOSEWIN(TopCmds.CURDATA())
	TopCmds.RE(Home)
	TopCmds.EXIT()

def find(path):
  found=0
  if os.path.exists(path[3]+'/'+path[0]+'/'+path[1])==1:
    found=1
  return found

def MAS(Home,Source,winfil,unit,qt):
	MAS=0
	
	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Source)
	if winfil ==1 :TopCmds.RE(Source,"n")
	MAS0 = Get.MAS(unit)

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Home)
	if winfil ==1 :TopCmds.RE(Home,"n")
	MAS1 = Get.MAS(unit)
	if MAS1 != MAS0 :
	  Put.MAS(MAS0,"")
	MAS=1

	return MAS


def Hhp(Home,Source,winfil,unit,qt):
	Hhp=0
	
	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Source)
	if winfil ==1 :TopCmds.RE(Source,"n")
	p90, pamp = Get.HPul(unit)

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Home)
	if winfil ==1 :TopCmds.RE(Home,"n")
	p90_0, pamp0 = Get.HPul(unit)

	if p90_0 != p90 or pamp != pamp0:

		Title="Proton Hard Pulse Merger"
		Header=""
		Inputs=\
		"1H 90"+deg+" pulse : "+str(p90_0)+" us ("+str(pul.pulDict['pH90'])+")",\
		"1H 90"+deg+" pwr   : "+str(pamp0)+unit+" ("+str(pul.pulDict['aH'])+")"

		Values=str(p90),str(pamp)
		Comments="us",unit
		Types="1","1"
		Buttons="Accept","Cancel"
		ShortCuts='a','c'
		columns=5
		
		if qt == 0:
		  result=TopCmds.INPUT_DIALOG(Title,Header,Inputs,Values,Comments,Types,Buttons,ShortCuts,columns)
		
		  if result != None:
		    p90, pamp = result
		    Hhp=1
		    Put.HPul(p90, pamp, unit)
		  else:
		    abort(Home,Source,winfil)
		if qt != 0:
		  Put.HPul(p90, pamp, unit)
		  Hhp=1
	return Hhp

def Chp(Home,Source,winfil,unit,qt):
	Chp=0

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Source)
	if winfil ==1 :TopCmds.RE(Source,"n")
	p90, pamp = Get.CPul(unit)

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Home)
	if winfil ==1 :TopCmds.RE(Home,"n")
	p90_0, pamp0 = Get.CPul(unit)

	if p90_0 != p90 or pamp != pamp0:

		Title="Carbon Hard Pulse Merger"
		Header=""
		Inputs=\
		"13C 90"+deg+" pulse : "+str(p90_0)+" us ("+str(pul.pulDict['pC90'])+")",\
		"13C 90"+deg+" pwr   : "+str(pamp0)+unit+" ("+str(pul.pulDict['aC'])+")"

		Values=str(p90),str(pamp)
		Comments="us",unit
		Types="1","1"
		Buttons="Accept","Cancel"
		ShortCuts='a','c'
		columns=5
		
		if qt == 0:
		  result=TopCmds.INPUT_DIALOG(Title,Header,Inputs,Values,Comments,Types,Buttons,ShortCuts,columns)
		
		  if result != None:
		    p90, pamp = result
		    Chp=1
		    Put.CPul(p90, pamp, unit)
		  else:
		    abort(Home,Source,winfil)
		if qt != 0:
		  Put.CPul(p90, pamp, unit)
		  Chp=1
	return Chp

def Nhp(Home,Source,winfil,unit,qt):
	Nhp=0

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Source)
	if winfil ==1 :TopCmds.RE(Source,"n")
	p90, pamp = Get.NPul(unit)
	#TopCmds.MSG("From:\np90= "+str(p90)+"\npamp= "+str(pamp))

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Home)
	if winfil ==1 :TopCmds.RE(Home,"n")
	p90_0, pamp0 = Get.NPul(unit)
	#TopCmds.MSG("Home:\np90_0= "+str(p90_0)+"\npamp_0= "+str(pamp0))

	if p90_0 != p90 or pamp != pamp0:

		Title="Nitrogen Hard Pulse Merger"
		Header=""
		Inputs=\
		"15N 90"+deg+" pulse : "+str(p90_0)+" us ("+str(pul.pulDict['pN90'])+")",\
		"15N 90"+deg+" pwr   : "+str(pamp0)+unit+" ("+str(pul.pulDict['aN'])+")"

		Values=str(p90),str(pamp)
		Comments="us",unit
		Types="1","1"
		Buttons="Accept","Cancel"
		ShortCuts='a','c'
		columns=5
		
		if qt == 0:
		  result=TopCmds.INPUT_DIALOG(Title,Header,Inputs,Values,Comments,Types,Buttons,ShortCuts,columns)
		
		  if result != None:
		    p90, pamp = result
		    Nhp=1
		    Put.NPul(p90, pamp, unit)
		  else:
		    abort(Home,Source,winfil)
		if qt != 0:
		  Put.NPul(p90, pamp, unit)
		  Nhp=1
		    
	return Nhp

def HC(Home,Source,winfil,unit,qt):
	HC=0

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Source)
	if winfil ==1 :TopCmds.RE(Source,"n")
	CPcnct, aHcp, aXcp, SPH, SPX = Get.HC(unit)

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Home)
	if winfil ==1 :TopCmds.RE(Home,"n")
	CPcnct0, aHcp0, aXcp0, SPH0, SPX0 = Get.HC(unit)

	if CPcnct!=CPcnct0 or aHcp!=aHcp0 or  aXcp!=aXcp0 or SPH!=SPH0 or SPX!=SPX0 :
		Title="UPDATE H-C CP"
		Header=""
		Inputs=\
		"Contact   : "+str(CPcnct0)+" us ("+str(pul.pulDict['pHC'])+")",\
		"1H pwr    : "+str(aHcp0)+" "+unit+" ("+str(pul.pulDict['aHhc'])+")",\
		"13C pwr   : "+str(aXcp0)+" "+unit+" ("+str(pul.pulDict['aChc'])+")",\
		"1H shape  : "+str(SPH0)+" ("+str(pul.pulDict['sHhc'])+")",\
		"13C shape : "+str(SPX0)+" ("+str(pul.pulDict['sChc'])+")"

		Values=str(CPcnct),str(aHcp),str(aXcp),str(SPH),str(SPX)
		Comments="us",unit,unit,"",""
		Types="1","1","1","1","1"
		Buttons="Accept","Cancel"
		ShortCuts='a','c'
		columns=15
		
		if qt==0:
		  result=TopCmds.INPUT_DIALOG(Title,Header,Inputs,Values,Comments,Types,Buttons,ShortCuts,columns)
		
		  if result != None:
		    CPcnct, aHcp, aXcp, SPH, SPX = result
		    HC=1
		    Put.HC(CPcnct, aHcp, aXcp, SPH, SPX, unit)
		  else:
		    abort(Home,Source,winfil)

		if qt != 0:
		    HC=1
		    Put.HC(CPcnct, aHcp, aXcp, SPH, SPX, unit)
	return HC


def HN(Home,Source,winfil,unit,qt):	
	HN=0

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Source)
	if winfil ==1 :TopCmds.RE(Source,"n")
	CPcnct, aHcp, aXcp, SPH, SPX = Get.HN(unit)

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Home)
	if winfil ==1 :TopCmds.RE(Home,"n")
	CPcnct0, aHcp0, aXcp0, SPH0, SPX0 = Get.HN(unit)

	if CPcnct!=CPcnct0 or aHcp!=aHcp0 or  aXcp!=aXcp0 or SPH!=SPH0 or SPX!=SPX0 :
		
		Title="UPDATE H-N CP"
		Header=""
		Inputs=\
		"Contact   : "+str(CPcnct0)+" us ("+str(pul.pulDict['pHC'])+")",\
		"1H pwr    : "+str(aHcp0)+" "+unit+" ("+str(pul.pulDict['aHhn'])+")",\
		"15N pwr   : "+str(aXcp0)+" "+unit+" ("+str(pul.pulDict['aNhn'])+")",\
		"1H shape  : "+str(SPH0)+" ("+str(pul.pulDict['sHhn'])+")",\
		"15N shape : "+str(SPX0)+" ("+str(pul.pulDict['sNhn'])+")"

		Values=str(CPcnct),str(aHcp),str(aXcp),str(SPH),str(SPX)
		Comments="us",unit,unit,"",""
		Types="1","1","1","1","1"
		Buttons="Accept","Cancel"
		ShortCuts='a','c'
		columns=15
		
		if qt==0:
		  result=TopCmds.INPUT_DIALOG(Title,Header,Inputs,Values,Comments,Types,Buttons,ShortCuts,columns)
		
		  if result != None:
		    CPcnct, aHcp, aXcp, SPH, SPX = result
		    HN=1
		    Put.HN(CPcnct, aHcp, aXcp, SPH, SPX, unit)
		  else:
		    abort(Home,Source,winfil)
		if qt != 0:
		  HN=1
		  Put.HN(CPcnct, aHcp, aXcp, SPH, SPX, unit)
	return HN
	
def CX(Home,Source,winfil,unit,qt):
	CX=0

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Source)
	if winfil ==1 :TopCmds.RE(Source)
	p90, pamp = Get.CX(unit)

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Home)
	if winfil ==1 :TopCmds.RE(Home)
	p90_0, pamp0 = Get.CX(unit)

	if p90_0 != p90 or pamp != pamp0:
		Title="Carbon DARR/PDSD/NOE Merger"
		Header=""
		Inputs=\
		"Spin Diffusion Mixing Time : "+str(p90_0)+" s ("+str(pul.pulDict['dDarr'])+")",\
		"1H field during mixing     : "+str(pamp0)+unit+" ("+str(pul.pulDict['aHdarr'])+")"

		Values=str(p90),str(pamp)
		Comments="s",unit
		Types="1","1"
		Buttons="Accept","Cancel"
		ShortCuts='a','c'
		columns=5
		
		if qt==0:
		  result=TopCmds.INPUT_DIALOG(Title,Header,Inputs,Values,Comments,Types,Buttons,ShortCuts,columns)
		
		  if result != None:
		    p90, pamp = result
		    CX=1
		    Put.CX(p90, pamp, unit)
		  else:
		    abort(Home,Source,winfil)
		if qt != 0:
		  CX=1
		  Put.CX(p90, pamp, unit)
	return CX

def NCA(Home,Source,winfil,unit,qt):
	NCA=0
	
	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Source)
	if winfil ==1 :TopCmds.RE(Source)
	CPcnct, aH, aX, aY, SPX, SPY = Get.NCA(unit)

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Home)
	if winfil ==1 :TopCmds.RE(Home)
	CPcnct0, aH0, aX0, aY0, SPX0, SPY0 = Get.NCA(unit)

	if CPcnct!=CPcnct0 or aH!=aH0 or  aX!=aX0 or aY != aY0 or SP!=SP0 :
		Title="UPDATE N-CA CP"
		Header=""
		Inputs=\
		"Contact    : "+str(CPcnct0)+" us ("+str(pul.pulDict['pNCA'])+")",\
		"1H dec pwr : "+str(aH0)+" "+unit+" ("+str(pul.pulDict['aHnca'])+")",\
		"13C pwr    : "+str(aX0)+" "+unit+" ("+str(pul.pulDict['aCnca'])+")",\
		"15N pwr    : "+str(aY0)+" "+unit+" ("+str(pul.pulDict['aNnca'])+")",\
		"13C shape  : "+str(SP0)+" ("+str(pul.pulDict['sCnca'])+")"
		"15N shape  : "+str(SP0)+" ("+str(pul.pulDict['aNnca'])+")"

		Values=str(CPcnct),str(aH),str(aX),str(aY),str(SPX),str(SPY)
		Comments="us",unit,unit,unit,"",""
		Types="1","1","1","1","1","1"
		Buttons="Accept","Cancel"
		ShortCuts='a','c'
		columns=15
		
		if qt==0:
		  result=TopCmds.INPUT_DIALOG(Title,Header,Inputs,Values,Comments,Types,Buttons,ShortCuts,columns)
		
		  if result != None:
		    CPcnct, aH, aX, aY, SPX, SPY = result
		    NCA=1
		    Put.NCA(CPcnct, aH, aX, aY, SPX, SPY, unit)
		  else:
		    abort(Home,Source,winfil)
		else:
		  NCA=1
		  Put.NCA(CPcnct, aH, aX, aY, SPX, SPY, unit)
	return NCA

def NCO(Home,Source,winfil,unit,qt):
	NC=0
	
	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Source)
	if winfil ==1 :TopCmds.RE(Source)
	CPcnct, aH, aX, aY, SPX, SPY = Get.NCO(unit)

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Home)
	if winfil ==1 :TopCmds.RE(Home)
	CPcnct0, aH0, aX0, aY0, SPX0, SPY0 = Get.NCO(unit)

	if CPcnct!=CPcnct0 or aH!=aH0 or  aX!=aX0 or aY != aY0 or SP!=SP0 :
		Title="UPDATE N-CO CP"
		Header=""
		Inputs=\
		"Contact    : "+str(CPcnct0)+" us ("+str(pul.pulDict['pNCO'])+")",\
		"1H dec pwr : "+str(aH0)+" "+unit+" ("+str(pul.pulDict['aHnco'])+")",\
		"13C pwr    : "+str(aX0)+" "+unit+" ("+str(pul.pulDict['aCnco'])+")",\
		"15N pwr    : "+str(aY0)+" "+unit+" ("+str(pul.pulDict['aNnco'])+")",\
		"13C shape  : "+str(SP0)+" ("+str(pul.pulDict['sCnco'])+")"
		"15N shape  : "+str(SP0)+" ("+str(pul.pulDict['aNnco'])+")"

		Values=str(CPcnct),str(aH),str(aX),str(aY),str(SPX),str(SPY)
		Comments="us",unit,unit,unit,"",""
		Types="1","1","1","1","1","1"
		Buttons="Accept","Cancel"
		ShortCuts='a','c'
		columns=15
		
		if qt==0:
		  result=TopCmds.INPUT_DIALOG(Title,Header,Inputs,Values,Comments,Types,Buttons,ShortCuts,columns)
		
		  if result != None:
		    CPcnct, aH, aX, aY, SPX, SPY = result
		    NC=1
		    Put.NCO(CPcnct, aH, aX, aY, SPX, SPY, unit)
		  else:
		    abort(Home,Source,winfil)
		else:
		  NCA=1
		  Put.NCO(CPcnct, aH, aX, aY, SPX, SPY, unit)
	return NC


def CH(Home,Source,winfil,unit,qt):
	HC=0

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Source)
	if winfil ==1 :TopCmds.RE(Source,"n")
	CPcnct, aHcp, aXcp, SPH, SPX = Get.CH(unit)

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Home)
	if winfil ==1 :TopCmds.RE(Home,"n")
	CPcnct0, aHcp0, aXcp0, SPH0, SPX0 = Get.CH(unit)

	if CPcnct!=CPcnct0 or aHcp!=aHcp0 or  aXcp!=aXcp0 or SPH!=SPH0 or SPX!=SPX0 :
		Title="UPDATE C-H CP"
		Header=""
		Inputs=\
		"Contact   : "+str(CPcnct0)+" us ("+str(pul.pulDict['pCH'])+")",\
		"1H pwr    : "+str(aHcp0)+" "+unit+" ("+str(pul.pulDict['aHch'])+")",\
		"13C pwr   : "+str(aXcp0)+" "+unit+" ("+str(pul.pulDict['aCch'])+")",\
		"1H shape  : "+str(SPH0)+" ("+str(pul.pulDict['sHch'])+")",\
		"13C shape : "+str(SPX0)+" ("+str(pul.pulDict['sCch'])+")"

		Values=str(CPcnct),str(aHcp),str(aXcp),str(SPH),str(SPX)
		Comments="us",unit,unit,"",""
		Types="1","1","1","1","1"
		Buttons="Accept","Cancel"
		ShortCuts='a','c'
		columns=15
		
		if qt==0:
		  result=TopCmds.INPUT_DIALOG(Title,Header,Inputs,Values,Comments,Types,Buttons,ShortCuts,columns)
		
		  if result != None:
		    CPcnct, aHcp, aXcp, SPH, SPX = result
		    HC=1
		    Put.CH(CPcnct, aHcp, aXcp, SPH, SPX, unit)
		  else:
		    abort(Home,Source,winfil)

		if qt != 0:
		    HC=1
		    Put.CH(CPcnct, aHcp, aXcp, SPH, SPX, unit)
	return HC

def hhC(Home,Source,winfil,unit,qt):
	hhC=0

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Source)
	if winfil ==1 :TopCmds.RE(Source,"n")
	CPcnct, aHcp, aXcp, SPH, SPX = Get.hhC(unit)

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Home)
	if winfil ==1 :TopCmds.RE(Home,"n")
	CPcnct0, aHcp0, aXcp0, SPH0, SPX0 = Get.hhC(unit)

	if CPcnct!=CPcnct0 or aHcp!=aHcp0 or  aXcp!=aXcp0 or SPH!=SPH0 or SPX!=SPX0 :
		Title="UPDATE HC (in XhhC) CP"
		Header=""
		Inputs=\
		"Contact   : "+str(CPcnct0)+" us ("+str(pul.pulDict['phhC'])+")",\
		"1H pwr    : "+str(aHcp0)+" "+unit+" ("+str(pul.pulDict['aHhhC'])+")",\
		"13C pwr   : "+str(aXcp0)+" "+unit+" ("+str(pul.pulDict['aChhc'])+")",\
		"1H shape  : "+str(SPH0)+" ("+str(pul.pulDict['sHhhc'])+")",\
		"13C shape : "+str(SPX0)+" ("+str(pul.pulDict['sChhc'])+")"

		Values=str(CPcnct),str(aHcp),str(aXcp),str(SPH),str(SPX)
		Comments="us",unit,unit,"",""
		Types="1","1","1","1","1"
		Buttons="Accept","Cancel"
		ShortCuts='a','c'
		columns=15
		
		if qt==0:
		  result=TopCmds.INPUT_DIALOG(Title,Header,Inputs,Values,Comments,Types,Buttons,ShortCuts,columns)
		
		  if result != None:
		    CPcnct, aHcp, aXcp, SPH, SPX = result
		    hhC=1
		    Put.hhC(CPcnct, aHcp, aXcp, SPH, SPX, unit)
		  else:
		    abort(Home,Source,winfil)

		if qt != 0:
		    hhC=1
		    Put.hhC(CPcnct, aHcp, aXcp, SPH, SPX, unit)
	return hhC

def NH(Home,Source,winfil,unit,qt):
	NH=0

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Source)
	if winfil ==1 :TopCmds.RE(Source,"n")
	CPcnct, aHcp, aXcp, SPH, SPX = Get.NH(unit)

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Home)
	if winfil ==1 :TopCmds.RE(Home,"n")
	CPcnct0, aHcp0, aXcp0, SPH0, SPX0 = Get.NH(unit)

	if CPcnct!=CPcnct0 or aHcp!=aHcp0 or  aXcp!=aXcp0 or SPH!=SPH0 or SPX!=SPX0 :
		Title="UPDATE N-H CP"
		Header=""
		Inputs=\
		"Contact   : "+str(CPcnct0)+" us ("+str(pul.pulDict['pNH'])+")",\
		"1H pwr    : "+str(aHcp0)+" "+unit+" ("+str(pul.pulDict['aHnh'])+")",\
		"15N pwr   : "+str(aXcp0)+" "+unit+" ("+str(pul.pulDict['aNnh'])+")",\
		"1H shape  : "+str(SPH0)+" ("+str(pul.pulDict['sHnh'])+")",\
		"15N shape : "+str(SPX0)+" ("+str(pul.pulDict['sNnh'])+")"

		Values=str(CPcnct),str(aHcp),str(aXcp),str(SPH),str(SPX)
		Comments="us",unit,unit,"",""
		Types="1","1","1","1","1"
		Buttons="Accept","Cancel"
		ShortCuts='a','c'
		columns=15
		
		if qt==0:
		  result=TopCmds.INPUT_DIALOG(Title,Header,Inputs,Values,Comments,Types,Buttons,ShortCuts,columns)
		
		  if result != None:
		    CPcnct, aHcp, aXcp, SPH, SPX = result
		    NH=1
		    Put.NH(CPcnct, aHcp, aXcp, SPH, SPX, unit)
		  else:
		    abort(Home,Source,winfil)

		if qt != 0:
		    NH=1
		    Put.NH(CPcnct, aHcp, aXcp, SPH, SPX, unit)
	return NH
	
def HDec(Home,Source,winfil,unit,qt):
	HDec=0
	
	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Source)
	if winfil ==1 :TopCmds.RE(Source)
	cpd, pwname, pw, pampname, pamp = Get.HDec(unit)
	#TopCmds.MSG(cpd+pwname+str(pw)+pampname+str(pamp))

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Home)
	if winfil ==1 :TopCmds.RE(Home)
	cpd0, pw0name, pw0, pamp0name, pamp0 = Get.HDec(unit)
	#TopCmds.MSG(cpd0+pw0name+str(pw0)+pamp0name+str(pamp0))
	
	if cpd0 != cpd or pamp != pamp0 or pw != pw0 or pwname != pw0name or pampname != pamp0name:
		Title="UPDATE Proton Decoupling parameters"
		Header="(pl12, pcpd2, cpdprg2 only)"
		Inputs=\
		"Compound pulse : "+str(cpd0),\
		pwname+"  : "+str(pw0)+" us ",\
		pampname+"  : "+str(pamp0)+unit

		Values=str(cpd),str(pw),str(pamp)
		Comments="","us",unit
		Types="1","1","1"
		Buttons="Accept","Cancel"
		ShortCuts='a','c'
		columns=15
		
		if qt==0:
		  result=TopCmds.INPUT_DIALOG(Title,Header,Inputs,Values,Comments,Types,Buttons,ShortCuts,columns)
		
		  if result != None:
		    cpd, pw, pamp = result
		    HDec=1
		    Put.HDec(cpd, pwname, pw, pampname, pamp, unit)
		  else:
		    abort(Home,Source,winfil)
		if qt != 0:
		  HDec=1
		  Put.HDec(cpd, pwname, pw, pampname, pamp, unit)
	return HDec

def Phases(Home,Source,winfil,unit,qt):
	Phases=0
	
	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Source)
	if winfil ==1 :TopCmds.RE(Source)
	Phase = Get.Phases()

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Home)
	if winfil ==1 :TopCmds.RE(Home)
	Phase0 = Get.Phases()

	if Phase!=Phase0:
		Title="UPDATE Phaseing"
		Header=""
		Inputs=\
		"PH0 : "+str(Phase0[0])+deg,\
		"PH1 : "+str(Phase0[1])+deg

		Values=str(Phase[0]),str(Phase[1])
		Comments=deg,deg
		Types="1","1"
		Buttons="Accept","Cancel"
		ShortCuts='a','c'
		columns=8
				
		if qt==0:
		  result=TopCmds.INPUT_DIALOG(Title,Header,Inputs,Values,Comments,Types,Buttons,ShortCuts,columns)
		
		  if result != None:
		    Phase = result
		    Put.Phases(Phase)
		    Phases=1
		  else:
		    abort(Home,Source,winfil)
		if qt != 0:
		  Phases=1
		  Put.Phases(Phase)
		  
	return Phases
	
def CH2(Home,Source,winfil,unit,qt):
	CH2=0

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Source)
	if winfil ==1 :TopCmds.RE(Source,"n")
	CPcnct, aHcp, aXcp, SPH, SPX = Get.CH2(unit)

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Home)
	if winfil ==1 :TopCmds.RE(Home,"n")
	CPcnct0, aHcp0, aXcp0, SPH0, SPX0 = Get.CH2(unit)

	if CPcnct!=CPcnct0 or aHcp!=aHcp0 or  aXcp!=aXcp0 or SPH!=SPH0 or SPX!=SPX0 :
		Title="UPDATE C-H CP (H-detect)"
		Header=""
		Inputs=\
		"Contact   : "+str(CPcnct0)+" us ("+str(pul.pulDict['pCH2'])+")",\
		"1H pwr    : "+str(aHcp0)+" "+unit+" ("+str(pul.pulDict['aHch2'])+")",\
		"13C pwr   : "+str(aXcp0)+" "+unit+" ("+str(pul.pulDict['aCch2'])+")",\
		"1H shape  : "+str(SPH0)+" ("+str(pul.pulDict['sHch2'])+")",\
		"13C shape : "+str(SPX0)+" ("+str(pul.pulDict['sCch2'])+")"
		
		Values=str(CPcnct),str(aHcp),str(aXcp),str(SPH),str(SPX)
		Comments="us",unit,unit,"",""
		Types="1","1","1","1","1"
		Buttons="Accept","Cancel"
		ShortCuts='a','c'
		columns=15
		
		if qt==0:
		  result=TopCmds.INPUT_DIALOG(Title,Header,Inputs,Values,Comments,Types,Buttons,ShortCuts,columns)
		
		  if result != None:
		    CPcnct, aHcp, aXcp, SPH, SPX = result
		    CH2=1
		    Put.CH2(CPcnct, aHcp, aXcp, SPH, SPX, unit)
		  else:
		    abort(Home,Source,winfil)

		if qt != 0:
		    CH2=1
		    Put.CH2(CPcnct, aHcp, aXcp, SPH, SPX, unit)
	return CH2


def NH2(Home,Source,winfil,unit,qt):	
	NH2=0

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Source)
	if winfil ==1 :TopCmds.RE(Source,"n")
	CPcnct, aHcp, aXcp, SPH, SPX = Get.NH2(unit)

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Home)
	if winfil ==1 :TopCmds.RE(Home,"n")
	CPcnct0, aHcp0, aXcp0, SPH0, SPX0 = Get.NH2(unit)

	if CPcnct!=CPcnct0 or aHcp!=aHcp0 or  aXcp!=aXcp0 or SPH!=SPH0 or SPX!=SPX0 :
		
		Title="UPDATE N-H CP (H-detect)"
		Header=""
		Inputs=\
		"Contact   : "+str(CPcnct0)+" us ("+str(pul.pulDict['pNH2'])+")",\
		"1H pwr    : "+str(aHcp0)+" "+unit+" ("+str(pul.pulDict['aHnh2'])+")",\
		"15N pwr   : "+str(aXcp0)+" "+unit+" ("+str(pul.pulDict['aNnh2'])+")",\
		"1H shape  : "+str(SPH0)+" ("+str(pul.pulDict['sHnh2'])+")",\
		"15N shape : "+str(SPX0)+" ("+str(pul.pulDict['sNnh2'])+")"

		Values=str(CPcnct),str(aHcp),str(aXcp),str(SPH),str(SPX)
		Comments="us",unit,unit,"",""
		Types="1","1","1","1","1"
		Buttons="Accept","Cancel"
		ShortCuts='a','c'
		columns=15
		
		if qt==0:
		  result=TopCmds.INPUT_DIALOG(Title,Header,Inputs,Values,Comments,Types,Buttons,ShortCuts,columns)
		
		  if result != None:
		    CPcnct, aHcp, aXcp, SPH, SPX = result
		    NH2=1
		    Put.NH2(CPcnct, aHcp, aXcp, SPH, SPX, unit)
		  else:
		    abort(Home,Source,winfil)
		if qt != 0:
		  NH2=1
		  Put.NH2(CPcnct, aHcp, aXcp, SPH, SPX, unit)
	return NH2
	

def CAs90(Home,Source,winfil,unit,qt):	
	done=0

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Source)
	if winfil ==1 :TopCmds.RE(Source,"n")
	PW, Amp, SP, Off = Get.CA_S90(unit)

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Home)
	if winfil ==1 :TopCmds.RE(Home,"n")
	PW0, Amp0, SP0, Off0 = Get.CA_S90(unit)

	if CPcnct!=CPcnct0 or aHcp!=aHcp0 or  aXcp!=aXcp0 or SPH!=SPH0 or SPX!=SPX0 :
		
		Title="UPDATE CA soft 90 pulse"
		Header=""
		Inputs=\
		"Pulse   : "+str(PW0)+" us ("+str(pul.pulDict['pCAe'])+")",\
		"Ampl    : "+str(Amp0)+" "+unit+" ("+str(pul.pulDict['aCAe'])+")",\
		"Shape   : "+str(SP0)+" ("+str(pul.pulDict['sCAe'])+")",\
		"Offset  : "+str(Off0)+" ("+str(pul.pulDict['oCAe'])+")"

		Values=str(PW),str(Amp),str(SP),str(Off)
		Comments="us",unit,"",str(pul.pulDict['uoffs'])
		Types="1","1","1","1"
		Buttons="Accept","Cancel"
		ShortCuts='a','c'
		columns=15
		
		if qt==0:
		  result=TopCmds.INPUT_DIALOG(Title,Header,Inputs,Values,Comments,Types,Buttons,ShortCuts,columns)
		
		  if result != None:
		    PW, Amp,SP,Off = result
		    done=1
		    Put.CA_S90(CPW,Amp,SP,Off,unit)
		  else:
		    abort(Home,Source,winfil)
		if qt != 0:
		  done=1
		  Put.CA_S90(CPW,Amp,SP,Off,unit)
	return done
		
def COs90(Home,Source,winfil,unit,qt):	
	done=0

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Source)
	if winfil ==1 :TopCmds.RE(Source,"n")
	PW, Amp, SP, Off = Get.CO_S90(unit)

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Home)
	if winfil ==1 :TopCmds.RE(Home,"n")
	PW0, Amp0, SP0, Off0 = Get.CO_S90(unit)

	if CPcnct!=CPcnct0 or aHcp!=aHcp0 or  aXcp!=aXcp0 or SPH!=SPH0 or SPX!=SPX0 :
		
		Title="UPDATE CO soft 90 pulse"
		Header=""
		Inputs=\
		"Pulse   : "+str(PW0)+" us ("+str(pul.pulDict['pCOe'])+")",\
		"Ampl    : "+str(Amp0)+" "+unit+" ("+str(pul.pulDict['aCOe'])+")",\
		"Shape   : "+str(SP0)+" ("+str(pul.pulDict['sCOe'])+")",\
		"Offset  : "+str(Off0)+" ("+str(pul.pulDict['oCOe'])+")"

		Values=str(PW),str(Amp),str(SP),str(Off)
		Comments="us",unit,"",str(pul.pulDict['uoffs'])
		Types="1","1","1","1"
		Buttons="Accept","Cancel"
		ShortCuts='a','c'
		columns=15
		
		if qt==0:
		  result=TopCmds.INPUT_DIALOG(Title,Header,Inputs,Values,Comments,Types,Buttons,ShortCuts,columns)
		
		  if result != None:
		    PW, Amp,SP,Off = result
		    done=1
		    Put.CO_S90(PW,Amp,SP,Off,unit)
		  else:
		    abort(Home,Source,winfil)
		if qt != 0:
		  done=1
		  Put.CO_S90(PW,Amp,SP,Off,unit)
	return done
		
def CAs180(Home,Source,winfil,unit,qt):	
	done=0

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Source)
	if winfil ==1 :TopCmds.RE(Source,"n")
	PW, Amp, SP, Off = Get.CA_S180(unit)

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Home)
	if winfil ==1 :TopCmds.RE(Home,"n")
	PW0, Amp0, SP0, Off0 = Get.CA_S180(unit)

	if CPcnct!=CPcnct0 or aHcp!=aHcp0 or  aXcp!=aXcp0 or SPH!=SPH0 or SPX!=SPX0 :
		
		Title="UPDATE CA soft 180 pulse"
		Header=""
		Inputs=\
		"Pulse   : "+str(PW0)+" us ("+str(pul.pulDict['pCAr'])+")",\
		"Ampl    : "+str(Amp0)+" "+unit+" ("+str(pul.pulDict['aCAr'])+")",\
		"Shape   : "+str(SP0)+" ("+str(pul.pulDict['sCAr'])+")",\
		"Offset  : "+str(Off0)+" ("+str(pul.pulDict['oCAr'])+")"

		Values=str(PW),str(Amp),str(SP),str(Off)
		Comments="us",unit,"",str(pul.pulDict['uoffs'])
		Types="1","1","1","1"
		Buttons="Accept","Cancel"
		ShortCuts='a','c'
		columns=15
		
		if qt==0:
		  result=TopCmds.INPUT_DIALOG(Title,Header,Inputs,Values,Comments,Types,Buttons,ShortCuts,columns)
		
		  if result != None:
		    PW, Amp,SP,Off = result
		    done=1
		    Put.CA_S180(PW,Amp,SP,Off,unit)
		  else:
		    abort(Home,Source,winfil)
		if qt != 0:
		  done=1
		  Put.CA_S180(PW,Amp,SP,Off,unit)
	return done
		
def COs180(Home,Source,winfil,unit,qt):
	done=0

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Source)
	if winfil ==1 :TopCmds.RE(Source,"n")
	PW, Amp, SP, Off = Get.CO_S180(unit)

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Home)
	if winfil ==1 :TopCmds.RE(Home,"n")
	PW0, Amp0, SP0, Off0 = Get.CO_S180(unit)

	if CPcnct!=CPcnct0 or aHcp!=aHcp0 or  aXcp!=aXcp0 or SPH!=SPH0 or SPX!=SPX0 :
		
		Title="UPDATE CO soft 180 pulse"
		Header=""
		Inputs=\
		"Pulse   : "+str(PW0)+" us ("+str(pul.pulDict['pCOr'])+")",\
		"Ampl    : "+str(Amp0)+" "+unit+" ("+str(pul.pulDict['aCOr'])+")",\
		"Shape   : "+str(SP0)+" ("+str(pul.pulDict['sCOr'])+")",\
		"Offset  : "+str(Off0)+" ("+str(pul.pulDict['oCOr'])+")"

		Values=str(PW),str(Amp),str(SP),str(Off)
		Comments="us",unit,"",str(pul.pulDict['uoffs'])
		Types="1","1","1","1"
		Buttons="Accept","Cancel"
		ShortCuts='a','c'
		columns=15
		
		if qt==0:
		  result=TopCmds.INPUT_DIALOG(Title,Header,Inputs,Values,Comments,Types,Buttons,ShortCuts,columns)
		
		  if result != None:
		    PW, Amp,SP,Off = result
		    done=1
		    Put.CO_S18(PW,Amp,SP,Off,unit)
		  else:
		    abort(Home,Source,winfil)
		if qt != 0:
		  done=1
		  Put.CO_S180(PW,Amp,SP,Off,unit)
	return done
		
