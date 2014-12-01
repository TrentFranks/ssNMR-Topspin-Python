"""
Module for python CPD handling:
W.T. Franks FMP Berlin 
"""
from java.lang import *
import de.bruker.nmr.mfw.root as root
import sys
sys.path.append(root.UtilPath.getTopspinHome()+ '/exp/stan/nmr/py/BioPY/modules/')

import os
import TopCmds
import PProgtools
from GetLib import pul

def CPDparse(Ramp,Nuc):
  Dirs=get_dir()
  Name=find_file(Dirs,Ramp)
  
  pl_name=''
  pw_name=''
  
  # There is a problem if the files don't exist.
  if os.path.exists(Name) == 1:
    f=open(Name, 'r')
    text=f.readlines()
    f.close()
  else:
    if Nuc=="1H":
      TopCmds.XCMD(pul.pulDict['prgHDec'])
    if Nuc=="13C":
      TopCmds.XCMD(pul.pulDict['prgCDec'])
    if Nuc=="15N":
      TopCmds.XCMD(pul.pulDict['prgNDec'])
    if Nuc=="2H":
      TopCmds.XCMD(pul.pulDict['prgDDec'])
  
  for line in text:
    lines = line.rstrip()
    #print(lines)
    if lines.find("pl") >=0:
	    j=lines.find('=')
	    pl_name=lines[j+1:]
	    
    if lines.find("pcpd")>=0:
      pw_name="pcpd"
    elif lines.find("p31")>=0:
      pw_name="p31"
    elif lines.find("p62")>=0:
      pw_name="p62"
      
  # Delve into the pulse program if we didn't find our power level in the cpd file
  if pl_name == '':
    pulprog=TopCmds.GETPAR("PULPROG")
    #TopCmds.MSG(pulprog)
    ppText =PProgtools.PPparse(pulprog)
    #ppText =TopCmds.GET_PULSPROG_TEXT(pulprog)

    #TopCmds.MSG(str(ppText))
    Lines=devide_into_lines(ppText)
    pl_name=get_cpd_plnam(Lines,Nuc)
  
  return pl_name, pw_name
  
def devide_into_lines(Text):
    lines = []
    about = ''
    for letter in Text:
        about = about + letter
        if letter == '\n' :
            lines.append(about)
            #MSG(about)
            #print(about)
            about = ''
    return lines
    
# try to find power in pulse program
def get_cpd_plnam(Text,Nuc):
    
    pl_nam=''
    if Nuc=="1H" :key="cpds2","cpd2","cw"
    if Nuc=="2H" :key="cpds5","cpd5","cw"
    if Nuc=="13C":key="cpds4","cpd4","cw"
    if Nuc=="15N":key="cpds3","cpd3","cw"
    
    j=1
    for i in range(len(Text)):
      if Text[i].find(key[0]) >=0 or Text[i].find(key[1]) >=0\
      or Text[i].find(key[2]) >=0:
        j=i-5
	for i in range(j,len(Text)):
	  if Nuc=="1H" :
	    if Text[i].find("pl12:f2") >=0:pl_nam='pl12'
	    if Text[i].find("pl13:f2") >=0:pl_nam='pl13'
	    if Text[i].find("pl14:f2") >=0:pl_nam='pl14'
	    if Text[i].find("pl12:H") >=0 :pl_nam='pl12'
	    if Text[i].find("pl13:H") >=0 :pl_nam='pl13'
	    if Text[i].find("pl14:H") >=0 :pl_nam='pl14'
	    if Text[i].find("pl12):H") >=0 :pl_nam='pl12'
	    if Text[i].find("pl13):H") >=0 :pl_nam='pl13'
	    if Text[i].find("pl14):H") >=0 :pl_nam='pl14'

      if Nuc=="2H" :
        if Text[i].find("pl25:f3") >=0 :pl_nam='pl25'
        if Text[i].find("pl25:f4") >=0 :pl_nam='pl25'
        if Text[i].find("pl25:D") >=0  :pl_nam='pl25'

      if Nuc=="13C":
        if Text[i].find("pl4:f1")>=0 :pl_nam='pl4'
        if Text[i].find("pl4:C") >=0 :pl_nam='pl4'

      if Nuc=="15N":
        if Text[i].find("pl3:f2") >=0:pl_nam='pl3'
        if Text[i].find("pl3:f3") >=0:pl_nam='pl3'
        if Text[i].find("pl3:N") >=0 :pl_nam='pl3'
    if pl_nam == '':
      TopCmds.MSG('Using default decoupling name \n H=pl12 \n N=pl3 \n C=pl4 \D=pl25\
        /n/n The decoupling power was not deduced from either the CPDPRG or PULSEPROGRAM\n\
        PLEASE CONFIRM !!!')
      pl_nam='default'
    #TopCmds.MSG("I have finished the CPD parse!")
    return pl_nam
	  
def get_dir():
  waves = []
  lines = []
  l = []
  target =''
  name=root.UtilPath.getCurdir()+'/parfile-dirs.prop'
  defaultdir=root.UtilPath.getTopspinHome()+'/exp/stan/nmr/'
  
  f = open(name, 'r')
  text=f.readlines()
  f.close()
  
  i=0
  for line in text:
    lines = line.rstrip()
    if lines.find("CPD_DIRS") >=0:
      j=lines.find('=')
      Shapes=lines[j+1:] 
  #print(Shapes)
  i=0
  while i <= len(Shapes):
    #print(Shapes[i:i+1])
    if Shapes[i:i+1].find(';') >= 0 :
      l.append(i)
    i=i+1
  j=0
  k=0
  while k <= (len(l)-1) :
    waves.append(Shapes[j:l[k]])
    j=l[k]+1
    k=k+1
  waves.append(Shapes[j:])
  #TopCmds.MSG(str(waves))
  
  k=0
  while k <= (len(waves)-1) :
    if waves[k][0:1] != '/' :
      #print (waves[k])
      waves[k]=str(defaultdir + waves[k]) 
    k=k+1
  #TopCmds.MSG(str(waves))
  #print(waves)
  return waves

def find_file(dirs,name):
  found=0
  i=0
  path=''
  while i <= (len(dirs) - 1):
    #print (dirs[i], found )
    if found == 0:
      search = str(dirs[i]) + '/' + str(name)
      """
      TopCmds.MSG("This is here to remind you that the os package is removed")
      found=1
      path=search
      """
      if os.path.exists(search) == 1:
        found = 1
        path = search
    i=i+1
  if found == 0: 
    TopCmds.MSG("File named " + name + " not found\n Exiting")
    TopCmds.EXIT()
  return path

def Find_old_pl(char,unit):
  if char=='pl12':
     pl=float(pul.GetPar('aHdec',unit))
  elif char=='pl13':
     pl=float(pul.GetPar('aHdec2',unit))
  elif char=='pl14':
     pl=float(pul.GetPar('aHdec3',unit))
  elif char=='pl3':
     pl=float(pul.GetPar('aNdec',unit))
  elif char=='pl4':
     pl=float(pul.GetPar('aCdec',unit))
  elif char=='pl25':
     pl=float(pul.GetPar('aDdec',unit))
  else:
     pl=1000.
  return pl

def Find_old_pw(char,Nuc):
  if char=='pcpd':
    if Nuc=="1H" :pw=pul.GetPar('pcpdH',"")
    if Nuc=="2H" :pw=pul.GetPar('pcpdD',"")
    if Nuc=="13C" :pw=pul.GetPar('pcpdC',"")
    if Nuc=="15N" :pw=pul.GetPar('pcpdN',"")

  elif char=='p31':
     pw=pul.GetPar("P 31","")
  elif char=='p62':
     pw=pul.GetPar("P 62","")
  else:
     pw=0.03
  return pw
