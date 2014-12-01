"""
Module for python CPD handling:
W.T. Franks FMP Berlin 
"""
from java.lang import *
from de.bruker.nmr.prsc.dbxml.ParfileLocator import getParfileDirs
import de.bruker.nmr.mfw.root as root
import sys
sys.path.append(root.UtilPath.getTopspinHome()+ '/exp/stan/nmr/py/BioPY/modules/')
#sys.path.append(root.UtilPath.getBioPyDir())

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
  TopCmds.MSG(str(kkl))
  
  for line in kkl:
    lines = line.rstrip()
    
  TopCmds.MSG(lines)
  #lines.append=CPDtools.devide_into_lines(lines)
  
  TopCmds.MSG(str(lines))
  for line in text:
    lines = line.rstrip()
  
  return text
  
	  
def get_dir():#PP directories
  return getParfileDirs(0)

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
