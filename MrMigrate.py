"""
Search through files to find and store from optimized parameter sets.

Migrate from one parameter convention to another

Use the pulprog for each experiment, but override if a parameter convention 
is specified in arguments

A simple dictionary key lookup then gets it done (with some service to shape variables in CP)

There might be a bug if a dictionary contains additional keys

Arguments:
-o; -s : original/source (old) parameter table
-d; -n : destination/new paramter table

-dB:interact with db instead of watts
-f : open and close files instead of switching windows
-EXPNO ##: grab from experiment number ##
-qt : quiet all interaction- updates by default

W.T. Franks FMP Berlin
"""
SHOW_STATUS("Migrating Parameters")

import math
import sys
import os
from sys import argv
sys.path.append(root.UtilPath.getTopspinHome()+ '/exp/stan/nmr/py/BioPY/modules/')

import Merge
import TS_Version as Ver
import GetLib

WdB="dB"

cmds=argv
Usefile=0
SkipFileDialog=0
quiet=0
KeepGoing = 1
CheckPP = 1
Type=""
MergedFrom = []

########################
#  Read in preferences #
########################
i=2

Conv_Old=""
Conv_New=""
if len(cmds) >= 2 :

	for cmd in cmds[1:]:
	  
	  if cmd.find('-f') >=0 or cmd.find('-file') >=0 or cmd.find('-F') >=0 :
		Usefile=1
	  if cmd.find('-dB') >=0 or cmd.find('-DB') >=0 or cmd.find('-db') >=0 :
		WdB="dB"
	  if cmd.find('-ex') >=0 or cmd.find('-EXPNO') >=0 or cmd.find('-EX') >=0 :
		expno=cmds[i]
		SkipFileDialog=1
	  if cmd.find('-q') >=0 or cmd.find('-Q') >=0 or cmd.find('-qt') >=0 or cmd.find('-QT') >=0 :
		quiet=1
	  if cmd.find('-o') >=0 or cmd.find('-O') >=0 or cmd.find('-s') >=0 or cmd.find('-S') >=0 :
		Conv_Old=cmds[i]
	  if cmd.find('-n') >=0 or cmd.find('-N') >=0 or cmd.find('-d') >=0 or cmd.find('-D') >=0 :
		Conv_New=cmds[i]

#Establish the window and/or directory to merge into

if Usefile ==1: Home=CURDATA()
if Usefile ==0: Home=GETWINID()

HomeWin=GETWINID()
Source0=CURDATA()

if Usefile ==0 :SET_SELECTED_WIN(Home)
if Usefile ==1 :RE(Home,"n")

ppn=GETPAR("PULPROG")

if Conv_New != "": ppn = Conv_New
ver    = GetLib.get_PPvers(ppn)
name   = GetLib.get_TSvers(ver)
newpul = __import__(name)

# Assume the prior experiment is the starting point.
# If it doesn't exist the dialog opens a topspin browser to the contents of the folder

if SkipFileDialog == 1:
  name=Source0[3]+"/"+Source0[0]+"/"+str(expno)
  if Merge.find([Source0[0],str(expno),Source0[2],Source0[3]]) == 1:
	SourceData=Source0[0],str(expno),Source0[2],Source0[3]
	KeepGoing=0
  else:
	MSG("404:   " + name + "\n\n File not found------ Exiting")
	EXIT()

else:
  SourceData=DATASET_DIALOG("Migrate Parameters From ",[Source0[0],str(int(Source0[1])-1),Source0[2],Source0[3]])

if SourceData == None: 
  SLEEP(0.02)
  EXIT()

# Remember from where we pulled data 
NEWWIN()
WinID=GETWINID()

#We move into the source file
RE(SourceData)
MergedFrom.append(CURDATA())

if Usefile ==0: Source=WinID
if Usefile ==1: Source=CURDATA()

# I am in the source file
pps=GETPAR("PULPROG")

if Conv_Old != "" : pps = Conv_Old
ver    = GetLib.get_PPvers(pps)
name   = GetLib.get_TSvers(ver)
oldpul = __import__(name)

# Now I have oldpul and newpul as dicts I just need to compare move into the new
# I need to control for Unused variables (names)
  
for key in oldpul.pulDict.keys():
  SLEEP(0.2)

  #Setup Complementary key
  found=0; chan="";newchan=""
  for letter in key:
	if letter.isupper() and found==0: chan=letter; found=1
	if letter.islower() and chan.lower() != letter and\
	   letter != "a" and letter != "o":
		 newchan=letter.upper()
  cmplkey=""
  for letter in key:
	if letter.isupper():cmplkey=cmplkey+newchan
	else:               cmplkey=cmplkey+letter

  # Go into source (old)
  if Usefile ==0 :SET_SELECTED_WIN(Source)
  if Usefile ==1 :RE(Source,"n")

  cmplval=""
  #Grab the old parameter from source
  oldval=oldpul.GetPar(key,WdB)
  if oldpul.pulDict[key] == "Unused":
    cmplval=str(oldpul.GetPar(cmplkey,WdB))

  # Go into home (new)
  if Usefile ==0 :SET_SELECTED_WIN(Home)
  if Usefile ==1 :RE(Home,"n")

  #old was active, new might not be

  val = ""
  if oldpul.pulDict[key] != "Unused":
    #new is active too
    if newpul.pulDict[key] != "Unused":
      newpul.SetPar(key,oldval,WdB)
    #if new is not active either, do nothing

  #old was not active, new might be
  #This situation should only happen with CP shapes
  elif oldpul.pulDict[key] == "Unused":

    #Neither pulse in source is used
    if oldpul.pulDict[cmplkey]=="Unused":
      val="square.100"
    #The other channel is indeed ramped in the old exp.
    elif oldpul.pulDict[cmplkey] != "Unused":
      if cmplval == "" or cmplval == "None" or cmplval == "0":
        val ="square.100"
      else:
        val=cmplval
    
    #The new experiment is active, let's put in the value
    if newpul.pulDict[cmplkey] != "Unused":
      newpul.SetPar(cmplkey,val,WdB)
    #If new is not active, do nothing
    
if Usefile != 1:
  SET_SELECTED_WIN(Source)
  CLOSEWIN(CURDATA())
  SET_SELECTED_WIN(Home)

if Usefile == 1:
  CLOSEWIN(CURDATA())
  RE(Home)

MSG("Migration from "+pps+" to "+ppn+" is complete!\n\n\
 But be careful, it may not have moved everything to the right place\n\
 Be especially wary of the CP shapes.")

#if SkipFileDialog == 0:
#  if SELECT("Find more Files?","Continue migrating parameters?",["Continue", "Finished"]) == 1:
#	KeepGoing=0
