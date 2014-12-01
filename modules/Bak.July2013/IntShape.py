"""
Module for shaped pulse integration:
W.T. Franks FMP Berlin 
"""

import de.bruker.nmr.mfw.root as root

import os
import TopCmds
import math

"""
Find wave file in some path
Open the wave file
Load the amplitudes and phases
Sum, then divide by steps
Excitation, Inversion, etc. 
"""
def main():
  Dirs=get_shape_dir()
  Name=find_file(Dirs,argv[1])
  Integration=AverageWave(Name)
  #print(Integration)

def Integrate(Ramp):
  Dirs=get_shape_dir()
  Name=find_file(Dirs,Ramp)
  Integration=AverageWave(Name)
  #print(Integration)
  return Integration

def get_shape_dir():
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
    if lines.find("SHAPE_DIRS") >=0:
	    #PY_DIRS
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
  
  k=0
  while k <= (len(waves)-1) :
    if waves[k][0:1] != '/' :
      #print (waves[k])
      waves[k]=str(defaultdir + waves[k]) 
    k=k+1
  #print(waves)
    
  return waves

def find_file(dirs,name):
  found=0
  i=0
  path=''
  while i <= (len(dirs) - 1):
    #print (dirs[i], found )
    if found == 0: 
      search = str(dirs[i] + '/' + name)
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

def AverageWave(name):
  
  ampl = []
  ph = []
  f = open(name, 'r')
  text=f.readlines()
  f.close()
  
  for line in text:
    lines = line.rstrip()
    if lines.find('##') >=0:
      if lines.find("EX_MODE") >=0:
        j=lines.find('=')
        Excitation=lines[j+1:]
      if lines.find("INTEGFAC") >=0:
        j=lines.find('=')
        INTEG=lines[j+1:]
      if lines.find("NPOINTS") >=0:
        j=lines.find('=')
        Points=int(lines[j+1:])
    else:
      j= lines.find(',')
      ampl.append(float(lines[0:j]))
      ph.append(float(lines[j+1:]))
  Sum=0.0
  i=0
  #print(ampl)
  while i < Points:
    #Sum=(ampl[i])*(math.cos(ph[i]))+Sum
    Sum=ampl[i]+Sum
    #print (ampl[i])
    i=i+1
  Average=Sum/Points
  #print Average
  return Average


if __name__ == "__main__":
    main()
