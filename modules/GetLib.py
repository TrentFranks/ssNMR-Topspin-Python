#Parameter handling Bru vs FMP vs some other definition
from java.lang import *
import de.bruker.nmr.mfw.root as root

PPvers="fmp","wtf","bvr","bio"
TSvers="3.2","3.1","2.2","2.1","2.0"

import sys
sys.path.append(root.UtilPath.getTopspinHome()+ '/exp/stan/nmr/py/BioPY/modules/')

import TS_Version as Ver
import TopCmds


pp=TopCmds.GETPAR("PULPROG")

if __name__=="__main__":
  main()

def main():
  import TS_Version as Ver
  import TopCmds

  pp=TopCmds.GETPAR("PULPROG")

  found = 0
  name =""

  ver=get_PPvers(pp)
  name=get_TSver(ver)
  pul = __import__(name)

def get_PPvers(pp):

  found = 0
  for item in PPvers:
	if pp.find(item) >= 0:
	  name=item; found=1
	if found == 0:
	  name="bru"

  name = name +"TS"

  return name

def get_TSvers(vers):

  Version, Release = Ver.get()
  for item in TSvers:
	if Version.find(item) >=0 :
	  if item.find(".")>=0:nom = item[:item.find(".")]+"p"+item[item.find(".")+1:]
	  if item.find(".") <0:nom = item
	  name = vers + nom
  return name

name =""

name=get_TSvers(get_PPvers(pp))
pul = __import__(name)

