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
import CPDtools

def PPparse(pp):

  Dirs=get_dir()
  Name=find_file(Dirs,pp)
  #TopCmds.MSG(str(Dirs))
  #TopCmds.MSG(str(Name))
  
  # There is a problem if the files don't exist.
  if os.path.exists(Name) == 1:
    f=open(Name, 'r')
    text=f.readlines()
    f.close()
  else:
    while os.path.exists(Name) != 1:
      TopCmds.XCMD('edpul')
      pp=TopCmds.GETPAR("PULPROG")
      Name=find_file(Dirs,pp)
    
      if os.path.exists(Name) == 1:
        f=open(Name, 'r')
        text=f.readlines()
        f.close()
        
  kkl=CPDtools.devide_into_lines(text)
  #TopCmds.MSG(str(kkl))
  
  for line in kkl:
    lines = line.rstrip()
    
  #TopCmds.MSG(lines)
  #lines.append=CPDtools.devide_into_lines(lines)
  
  #TopCmds.MSG(str(lines))
  for line in text:
    lines = line.rstrip()
  
  return text
  
	  
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
    if lines.find("PP_DIRS") >=0:
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
