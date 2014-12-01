from java.lang import *
import de.bruker.nmr.mfw.root as root

import TopCmds
import TS_Version as Ver


def list():
  Nucl=[]
  vers=Ver.get()
  
  dataset=TopCmds.CURDATA() 
  if vers[1]=="2":
    path=dataset[3]+'/data/'+dataset[4]+'/nmr/'+ dataset[0]+'/'+dataset[1]
  if vers[1]=="3":
    path=dataset[3]+ '/'+dataset[0]+'/'+dataset[1]

  acqu=path+'/acqu'

  #TopCmds.MSG(acqu)

  f = open(acqu, 'r')
  text=f.readlines()
  f.close
  i=0
  for line in text:
  	lines = line.rstrip()
	if lines.find('##$NUC') >=0:
	  #  MSG("I found something: " + lines)
	  j=lines.find('<')
	  k=lines.find('>')
	  if lines.find('off') <=0: 
	    Nucl.append(lines[j+1:k])
  return Nucl

