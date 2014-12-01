"""
Search through files to find and store from optimized parameter sets.

We need to establish which parameters to pull from which datasets.
This is done through pulprog

I'm not sure how to handle the soft pulses yet...

If parameters are doubled, but not identical, we need to ask which to keep
but once we have the correct values, it will not ask again.

Arguments:
-dB:interact with db instead of watts
-f : open and close files instead of switching windows
-EXPNO ##: grab from experiment number ##
-qt : quiet all interaction- updates by default

Note: Inputting the pulse name (hNCaCX) will grab all relevant values except the hard pulses
      Or each element can be made separately. 
      Hard pulses must be specified separately (unless you specify nothing)
H
C
N : Update hard pulses 
HC
HN
NCO 
NCA
NH
CH
hhC : Merge specified CP parameters
CX  : Grab PDSD/DARR params
HDec: Grab Decoupling params
ph  : Grab Phasing parameters


W.T. Franks FMP Berlin
"""

import math
import sys
import os
from sys import argv
sys.path.append(root.UtilPath.getTopspinHome()+ '/exp/stan/nmr/py/BioPY/modules/')

import Merge, Help
import TS_Version as Ver

WdB="W"
if Ver.get()[1] == "2": WdB="dB"

cmds=argv
Usefile=0
SkipFileDialog=0
quiet=0
KeepGoing = 1
CheckPP = 1
GetPhases=0
GetAll=0
expno=0
User=""
Dir=""
Type=""
MergedFrom = []

# Variables to track merged elements
Hhp, Chp, Nhp, HDec, hC, hN, NCa, NCo, CH, hhC, Nh, CX = 0,0,0,0,0,0,0,0,0,0,0,0
NH2, CH2, Csoft = 0,0,0
MAS, Phases = 0,0

########################
#  Read in preferences #
########################
i=2
if len(cmds) >= 2 :

	for cmd in cmds[1:]:
          if cmd.find('-help') >=0 : Help.Merger(); EXIT()
	  
	  if cmd.find('-ph') >=0 or cmd.find('-PH') >=0 or cmd.find('-Phase') >=0 :
		GetPhases=1
	  if cmd.find('-f') >=0 or cmd.find('-file') >=0 or cmd.find('-F') >=0 :
		Usefile=1
	  if cmd.find('-dB') >=0 or cmd.find('-DB') >=0 or cmd.find('-db') >=0 :
		WdB="dB"
	  if cmd.find('-ex') >=0 or cmd.find('-EXPNO') >=0 or cmd.find('-EX') >=0 :
		expno=int(cmds[i])
		SkipFileDialog=1
	  #if cmd.find('-us') >=0 or cmd.find('-user') >=0 or cmd.find('-User') >=0 :
		#User=cmds[i]
	  if cmd.find('-dir') >=0 or cmd.find('-Dir') >=0 or cmd.find('-DIR') >=0 :
		Dir=cmds[i]
	  if cmd.find('-q') >=0 or cmd.find('-Q') >=0 or cmd.find('-qt') >=0 or cmd.find('-QT') >=0 :
		quiet=1
	  i=i+1

	  # Get hard pulses on command
	  if (cmd.find('h') >= 0 or cmd.find('H') >= 0) and not\
	  (cmd.find('hC') >= 0 or cmd.find('HC') >= 0 or cmd.find('hc') >= 0 or \
	  cmd.find('hN') >= 0 or cmd.find('HN') >= 0 or cmd.find('hn') >= 0 or \
	  cmd.find('HDEC') >=0 or cmd.find('HDec') >=0 or cmd.find('hdec') >=0 or \
	  cmd.find('-ph') >=0 or cmd.find('-PH') >=0 or cmd.find('-Phase') >=0 ):
		Type=Type+"H" ; CheckPP=0; Hhp = -1

	  if (cmd.find('c') >= 0 or cmd.find('C') >= 0) and not\
	  (cmd.find('hC') >= 0 or cmd.find('HC') >= 0 or cmd.find('hc') >= 0 or \
	  cmd.find('NC') >= 0 or cmd.find('nc') >= 0 or \
	  cmd.find('HDEC') >=0 or cmd.find('HDec') >=0 or cmd.find('hdec') >=0 or \
	  cmd.find('NDEC') >=0 or cmd.find('NDec') >=0 or cmd.find('ndec') >=0 or \
	  cmd.find('CDEC') >=0 or cmd.find('CDec') >=0 or cmd.find('cdec') >=0) :
		Type=Type+"C" ; CheckPP=0; Chp = -1;

	  if (cmd.find('n') >= 0 or cmd.find('N') >= 0) and not\
	  (cmd.find('hN') >= 0 or cmd.find('HN') >= 0 or cmd.find('hn') >= 0 or \
	  cmd.find('NC') >= 0 or cmd.find('nc') >= 0 or \
	  cmd.find('NDEC') >=0 or cmd.find('NDec') >=0 or cmd.find('Ndec') >=0 ) :
		Type=Type+"N" ; CheckPP=0; Nhp = -1

	  # Get Decoupling 
  
	  if (cmd.find('HDEC') >=0 or cmd.find('HDec') >=0 or cmd.find('hdec') >=0) :
		Type=Type+"H" ; CheckPP=0; HDec = -1

	  # Get normal CP
	  if cmd.find('hc') >= 0 or cmd.find('HC') >= 0 or cmd.find('hC') >= 0 :
		Type=Type+"HC" ; CheckPP=0; hC = -1
	  if cmd.find('hn') >= 0 or cmd.find('HN') >= 0 or cmd.find('hN') >= 0 :
		Type=Type+"HN" ; CheckPP=0; hN = -1
	  if cmd.find('nco') >= 0 or cmd.find('NCo') >= 0 or cmd.find('NCO') >= 0 :
		Type=Type+"NCO"; CheckPP=0; NCo = -1
	  if cmd.find('nca') >= 0 or cmd.find('NCa') >= 0 or cmd.find('NCA') >= 0 :
		Type=Type+"NCA"; CheckPP=0; NCa = -1

	  # Get CP for XhhC exp
	  if cmd.find('nh') >= 0 or cmd.find('NH') >= 0 or cmd.find('Nh') >= 0 :
		Type=Type+"Nh" ; CheckPP=0; NH = -1
	  if cmd.find('ch') >= 0 or cmd.find('CH') >= 0 or cmd.find('Ch') >= 0 :
		Type=Type+"Ch" ; CheckPP=0; CH = -1
	  if cmd.find('hhC') >= 0 or cmd.find('hhc') >= 0 or cmd.find('HHC') >= 0 :
		Type=Type+"hhC" ; CheckPP=0; hhC = -1

	  # Get Secondary
	  if cmd.find('nH') >= 0 or cmd.find('NH') >= 0 or cmd.find('Nh') >= 0 :
		Type=Type+"NH2" ; CheckPP=0; NH2 = -1
	  if cmd.find('cH') >= 0 or cmd.find('CH') >= 0 or cmd.find('Ch') >= 0 :
		Type=Type+"CH2" ; CheckPP=0; CH2 = -1
	  
	  # Get PDSD/DARR for CX exp
	  if cmd.find('CX') >= 0 or cmd.find('cx') >= 0 or cmd.find('CC') >= 0 :
		Type=Type+"CX" ; CheckPP=0; CX = -1
	  # Get Soft Pulses
	  if cmd.find('Csoft') >= 0 or cmd.find('Soft') >= 0 :
		Type=Type+" Csoft" ; CheckPP=0; Csoft = -1
	  i=i+1
	  
	if CheckPP == 0:

	  Hhp = Hhp+1; Chp=Chp+1; Nhp=Nhp+1; HDec=HDec+1; 
	  hC=hC+1; hN=hN+1; NCa=NCa+1; NCo=NCo+1; CH=CH+1;
	  hhC=hhC+1; Nh=Nh+1; CX=CX+1; NH2=NH2+1; CH2=CH2+1;
	  Csoft=Csoft+1

	for cmd in cmds[1:]:
	  
	  if cmd.find('-all') >=0 or cmd.find('-ALL') >=0 or cmd.find('-All') >=0 :
		Type="HNHCNCANCOCXNhChhCH Csoft" ; CheckPP=0; GetPhases=1; GetAll=1;
        Hhp = 0; Chp=0; Nhp=0; HDec=0; 
        hC=0; hN=0; NCa=0; NCo=0; CH=0;
        hhC=0; Nh=0; CX=0; NH2=0; CH2=0;
	Csoft=0

	#MSG(Type)

############################################
#    Keep track of where data was pulled   #
#  Specifics are found in respective files #
############################################

#Establish the window and/or directory to merge into

if Usefile ==1: Home=CURDATA()
if Usefile ==0: Home=GETWINID()

HomeWin=GETWINID()
Source0=CURDATA()
#MSG(str(Source0))

"""
 If I specify a directory, I want to suggest the same number for the first time through,
 but the previous number if not. 
"""
i=1
if Dir=="":Dir=Source0[0];i=0
if expno==0 : expno=int(Source0[1]); i=0


while KeepGoing >= 1:
  
  # Assume the prior experiment is the starting point.
  # If it doesn't exist the dialog opens a topspin browser to the contents of the folder

  if SkipFileDialog == 1:

    name=Source0[3]+"/"+Dir+"/"+str(expno-i)
    if Merge.find([Dir,str(expno-i),Source0[2],Source0[3]]) == 1:
      if Ver.get()[1] == "3":
        SourceData=Dir,str(expno-i),Source0[2],Source0[3]
      if Ver.get()[1] == "2":
        SourceData=Dir,str(expno-i),Source0[2],Source0[3],Source0[4]
      if GetAll==1:  KeepGoing=1
      else:  KeepGoing=0
    else:
      MSG("404:   " + name + "\n\n File not found------ Exiting")
      EXIT()

  else:
    if Ver.get()[1] == "2":
      #MSG("Test")
      SourceData=DATASET_DIALOG("Merge Optimization From ",\
      [Source0[0],str(int(Source0[1])-1),Source0[2],Source0[3],Source0[4]])
    elif Ver.get()[1] =="3":
      SourceData=DATASET_DIALOG("Merge Optimization From ",\
      [Source0[0],str(int(Source0[1])-1),Source0[2],Source0[3]])

  i=1
  if SourceData == None: 
    SLEEP(0.02)
    EXIT()

  # Remember from where we pulled data 
  NEWWIN()
  WinID=GETWINID()

  RE(SourceData)
  MergedFrom.append(CURDATA())

  # Window or file?
  if Usefile ==1: Source=CURDATA()
  if Usefile ==0: Source=WinID
  
  Source0=CURDATA()
  Dir=Source0[0]
  expno=int(Source0[1])

  # Determine what variables to use
  if CheckPP:
    Type=GETPAR("PULPROG")

  """MSG("Hhp: "+str(Hhp)+"\n Chp: "+ str(Chp)+"\n Nhp: "+ str(Nhp)+"\n hC: "+ str(hC)+"\n CX: "+ str(CX)\
  +"\n NCo: "+ str(NCo)+"\n CH: "+ str(CH)+"\n hhC: "+ str(hhC)+"\n NCa: "+ str(NCa)+"\n hN: "+ str(hN)\
  +"\n Nh: "+ str(Nh))"""
  
  if MAS <= 0: MAS=Merge.MAS(Home,Source,Usefile,WdB,quiet)
  if GetPhases==1 and Phases == 0 : Phases=Merge.Phases(Home,Source,Usefile,"",quiet)

  if Type.find("h") >= 0 or Type.find("H") >= 0 :
    if Hhp <= 0:  Hhp=Merge.Hhp(Home,Source,Usefile,WdB,quiet)
    if HDec <= 0: HDec=Merge.HDec(Home,Source,Usefile,WdB,quiet)

  if Type.find("C") >= 0 or Type.find("c") >=0:
    if Chp == 0:  Chp=Merge.Chp(Home,Source,Usefile,WdB,quiet)
    #if CDec == 0: CDec=Merge.CDec(Home,Source,Usefile,WdB,quiet)
      
  if Type.find("N") >= 0 or Type.find("n") >= 0:
    if Nhp == 0: Nhp=Merge.Nhp(Home,Source,Usefile,WdB,quiet)
    #if NDec == 0: NDec=Merge.NDec(Home,Source,Usefile,WdB,quiet)
  
  if Type.find("hC")  >= 0 or Type.find("HC") >= 0 or Type.find("hc") >= 0:
    if hC == 0:  hC=Merge.HC(Home,Source,Usefile,WdB,quiet)

  if Type.find("hN")  >= 0 or Type.find("HN") >= 0 or Type.find("hn") >= 0:
    if hN == 0:  hN=Merge.HN(Home,Source,Usefile,WdB,quiet)

  if Type.find("CC") >= 0 or Type.find("CX") >= 0:
    if CX == 0:  CX = Merge.CX(Home,Source,Usefile,WdB,quiet)

  if Type.find("NCa") >= 0 or Type.find("CaN") >= 0\
  or Type.find("NCA") >= 0 or Type.find("CAN") >= 0:
    if NCa == 0: NCa=Merge.NCA(Home,Source,Usefile,WdB,quiet)

  if Type.find("NCo") >= 0 or Type.find("CoN") >= 0\
  or Type.find("NCO") >= 0 or Type.find("CON") >= 0:
    if NCo == 0: NCo=Merge.NCO(Home,Source,Usefile,WdB,quiet)

  if Type.find("hhC") >= 0:
    if hhC == 0: hhC=Merge.hhC(Home,Source,Usefile,WdB,quiet)

  if Type.find("Ch") >= 0:
    if CH == 0:  CH=Merge.CH(Home,Source,Usefile,WdB,quiet)

  if Type.find("Nh") >= 0:
    if Nh == 0:  NH=Merge.NH(Home,Source,Usefile,WdB,quiet)

  if Type.find("Ch") >= 0 or Type.find("CH") >=0 :
    if CH2 == 0:  CH2=Merge.CH2(Home,Source,Usefile,WdB,quiet)

  if Type.find("Nh") >= 0 or Type.find("NH") >=0 :
    if NH2 == 0:  NH2=Merge.NH2(Home,Source,Usefile,WdB,quiet)
  
  if Type.find("Csoft") >= 0 :
    if Csoft == 0:
      Csoft=Merge.CAe(Home,Source,Usefile,WdB,quiet)
      Csoft=Merge.CAr(Home,Source,Usefile,WdB,quiet)
      Csoft=Merge.COe(Home,Source,Usefile,WdB,quiet)
      Csoft=Merge.COr(Home,Source,Usefile,WdB,quiet)

  if Usefile != 1:
    SET_SELECTED_WIN(Source)
    CLOSEWIN(CURDATA())
    SET_SELECTED_WIN(Home)

  if Usefile == 1:
    CLOSEWIN(CURDATA())
    RE(Home)

  if SkipFileDialog == 0:
    if SELECT("Find more Files?","Continue merging parameters?",["Continue", "Finished"]) == 1:
      KeepGoing=0

SET_SELECTED_WIN(HomeWin)
