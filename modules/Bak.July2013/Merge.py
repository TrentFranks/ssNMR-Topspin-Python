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

deg=u"\u00b0"

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
		"1H 90"+deg+" pulse : "+p90_0+" us ",\
		"1H 90"+deg+" pwr   : "+pamp0+unit

		Values=p90,pamp
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
		else:
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
		"13C 90"+deg+" pulse : "+p90_0+" us ",\
		"13C 90"+deg+" pwr   : "+pamp0+unit

		Values=p90,pamp
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
		if qt == 0:
		  Put.CPul(p90, pamp, unit)
		  Chp=1
	return Chp

def Nhp(Home,Source,winfil,unit,qt):
	Nhp=0

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Source)
	if winfil ==1 :TopCmds.RE(Source,"n")
	p90, pamp = Get.NPul(unit)

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Home)
	if winfil ==1 :TopCmds.RE(Home,"n")
	p90_0, pamp0 = Get.NPul(unit)

	if p90_0 != p90 or pamp != pamp0:

		Title="Nitrogen Hard Pulse Merger"
		Header=""
		Inputs=\
		"15N 90"+deg+" pulse : "+p90_0+" us ",\
		"15N 90"+deg+" pwr   : "+pamp0+unit

		Values=p90,pamp
		Comments="us",unit
		Types="1","1"
		Buttons="Accept","Cancel"
		ShortCuts='a','c'
		columns=5
		
		if qt==0:
		  result=TopCmds.INPUT_DIALOG(Title,Header,Inputs,Values,Comments,Types,Buttons,ShortCuts,columns)
		
		  if result != None:
		    p90, pamp = result
		    Nhp=1
		    Put.NPul(p90, pamp, unit)
		  else:
		    abort(Home,Source,winfil)
		else:
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
		"Contact   : "+CPcnct0+" us ",\
		"1H pwr    : "+aHcp0+" "+unit,\
		"13C pwr   : "+aXcp0+" "+unit,\
		"1H shape  : "+SPH0,\
		"13C shape : "+SPX0

		Values=CPcnct,aHcp,aXcp,SPH,SPX
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

		else:
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
		"Contact   : "+CPcnct0+" us ",\
		"1H pwr    : "+aHcp0+" "+unit,\
		"13C pwr   : "+aXcp0+" "+unit,\
		"1H shape  : "+SPH0,\
		"13C shape : "+SPX0

		Values=CPcnct,aHcp,aXcp,SPH,SPX
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
		else:
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
		"Spin Diffusion Mixing Time : "+p90_0+" s ",\
		"1H field during mixing     : "+pamp0+unit

		Values=p90,pamp
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
		else:
		  CX=1
		  Put.CX(p90, pamp, unit)
	return CX

def NCA(Home,Source,winfil,unit,qt):
	NCA=0
	
	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Source)
	if winfil ==1 :TopCmds.RE(Source)
	CPcnct, aH, aX, aY, SP = Get.NCA(unit)

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Home)
	if winfil ==1 :TopCmds.RE(Home)
	CPcnct0, aH0, aX0, aY0, SP0 = Get.NCA(unit)

	if CPcnct!=CPcnct0 or aH!=aH0 or  aX!=aX0 or aY != aY0 or SP!=SP0 :
		Title="UPDATE N-CA CP"
		Header=""
		Inputs=\
		"Contact    : "+CPcnct0+" us ",\
		"1H dec pwr : "+aH0+" "+unit,\
		"13C pwr    : "+aX0+" "+unit,\
		"15N pwr    : "+aY0+" "+unit,\
		"13C shape  : "+SP0

		Values=CPcnct,aH,aX,aY,SP
		Comments="us",unit,unit,unit,""
		Types="1","1","1","1","1"
		Buttons="Accept","Cancel"
		ShortCuts='a','c'
		columns=15
		
		if qt==0:
		  result=TopCmds.INPUT_DIALOG(Title,Header,Inputs,Values,Comments,Types,Buttons,ShortCuts,columns)
		
		  if result != None:
		    CPcnct, aH, aX, aY, SP = result
		    NCA=1
		    Put.NCA(CPcnct, aH, aX, aY, SP, unit)
		  else:
		    abort(Home,Source,winfil)
		else:
		  NCA=1
		  Put.NCA(CPcnct, aH, aX, aY, SP, unit)
	return NCA

def NCO(Home,Source,winfil,unit,qt):
	NCO=0
	
	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Source)
	if winfil ==1 :TopCmds.RE(Source)
	CPcnct, aH, aX, aY, SP = Get.NCO(unit)

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Home)
	if winfil ==1 :TopCmds.RE(Home)
	CPcnct0, aH0, aX0, aY0, SP0 = Get.NCO(unit)
	
	if CPcnct!=CPcnct0 or aH!=aH0 or  aX!=aX0 or aY != aY0 or SP!=SP0 :
		Title="UPDATE N-CO CP"
		Header=""
		Inputs=\
		"Contact    : "+CPcnct0+" us ",\
		"1H dec pwr : "+aH0+" "+unit,\
		"13C pwr    : "+aX0+" "+unit,\
		"15N pwr    : "+aY0+" "+unit,\
		"13C shape  : "+SP0

		Values=CPcnct,aH,aX,aY,SP
		Comments="us",unit,unit,unit,""
		Types="1","1","1","1","1"
		Buttons="Accept","Cancel"
		ShortCuts='a','c'
		columns=15
		
		if qt==0:
		  result=TopCmds.INPUT_DIALOG(Title,Header,Inputs,Values,Comments,Types,Buttons,ShortCuts,columns)
		
		  if result != None:
		    CPcnct, aH, aX, aY, SP = result
		    NCO=1
		    Put.NCO(CPcnct, aH, aX, aY, SP, unit)
		  else:
		    abort(Home,Source,winfil)
		else:
		  NCO=1
		  Put.NCO(CPcnct, aH, aX, aY, SP, unit)
	return NCO

def CH(Home,Source,winfil,unit,qt):
	CH=0
	
	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Source)
	if winfil ==1 :TopCmds.RE(Source)
	cnct, aH, aX, SP = Get.CH(unit)

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Home)
	if winfil ==1 :TopCmds.RE(Home)
	cnct0, aH0, aX0, SP0 = Get.CH(unit)

	if cnct!=cnct0 or aH!=aH0 or  aX!=aX0 or SP!=SP0 :
		Title="UPDATE C-H CP for XhhC experiments"
		Header=""
		Inputs=\
		"Contact    : "+cnct0+" us ",\
		"1H pwr     : "+aH0+" "+unit,\
		"13C pwr    : "+aX0+" "+unit,\
		"13C shape  : "+SP0

		Values=cnct,aH,aX,SP
		Comments="us",unit,unit,""
		Types="1","1","1","1"
		Buttons="Accept","Cancel"
		ShortCuts='a','c'
		columns=15
		
		if qt==0:
		  result=TopCmds.INPUT_DIALOG(Title,Header,Inputs,Values,Comments,Types,Buttons,ShortCuts,columns)
		
		  if result != None:
		    CPcnct, aH, aX, SP = result
		    CH=1
		    Put.CH(cnct, aH, aX, SP, unit)
		  else:
		    abort(Home,Source,winfil)
		else:
		  CH=1
		  Put.CH(cnct, aH, aX, SP, unit)
	return CH

def hhC(Home,Source,winfil,unit,qt):
	hhC=0
	
	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Source)
	if winfil ==1 :TopCmds.RE(Source)
	cnct, aH, aX, SP = Get.hhC(unit)

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Home)
	if winfil ==1 :TopCmds.RE(Home)
	cnct0, aH0, aX0, SP0 = Get.hhC(unit)

	if cnct!=cnct0 or aH!=aH0 or  aX!=aX0 or SP!=SP0 :
		Title="UPDATE HC CP for XhhC experiments"
		Header=""
		Inputs=\
		"Contact    : "+cnct0+" us ",\
		"1H pwr     : "+aH0+" "+unit,\
		"13C pwr    : "+aX0+" "+unit,\
		"13C shape  : "+SP0

		Values=cnct,aH,aX,SP
		Comments="us",unit,unit,""
		Types="1","1","1","1"
		Buttons="Accept","Cancel"
		ShortCuts='a','c'
		columns=15
		
		if qt==0:
		  result=TopCmds.INPUT_DIALOG(Title,Header,Inputs,Values,Comments,Types,Buttons,ShortCuts,columns)
		
		  if result != None:
		    CPcnct, aH, aX, SP = result
		    hhC=1
		    Put.hhC(cnct, aH, aX, SP, unit)
		  else:
		    abort(Home,Source,winfil)
		else:
		  hhC=1
		  Put.hhC(cnct, aH, aX, SP, unit)	
	return hhC

def NH(Home,Source,winfil,unit,qt):
	NH=0
	
	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Source)
	if winfil ==1 :TopCmds.RE(Source)
	cnct, aH, aX, SP = Get.NH(unit)

	if winfil ==0 :TopCmds.SET_SELECTED_WIN(Home)
	if winfil ==1 :TopCmds.RE(Home)
	cnct0, aH0, aX0, SP0 = Get.NH(unit)

	if cnct!=cnct0 or aH!=aH0 or  aX!=aX0 or SP!=SP0 :
		Title="UPDATE N->H CP for XhhC experiments"
		Header=""
		Inputs=\
		"Contact    : "+cnct0+" us ",\
		"1H pwr     : "+aH0+" "+unit,\
		"15N pwr    : "+aX0+" "+unit,\
		"15N shape  : "+SP0

		Values=cnct,aH,aX,SP
		Comments="us",unit,unit,""
		Types="1","1","1","1"
		Buttons="Accept","Cancel"
		ShortCuts='a','c'
		columns=15
		
		if qt==0:
		  result=TopCmds.INPUT_DIALOG(Title,Header,Inputs,Values,Comments,Types,Buttons,ShortCuts,columns)
		
		  if result != None:
		    CPcnct, aH, aX, SP = result
		    NH=1
		    Put.NH(cnct, aH, aX, SP, unit)
		  else:
		    abort(Home,Source,winfil)
		else:
		  NH=1
		  Put.NH(cnct, aH, aX, SP, unit)	
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
		"Compound pulse : "+cpd0,\
		pwname+"  : "+pw0+" us ",\
		pampname+"  : "+pamp0+unit

		Values=cpd,pw,pamp
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
		else:
		  HDec=1
		  Put.HDec(cpd, pwname, pw, pampname, pamp, unit)
	return HDec

