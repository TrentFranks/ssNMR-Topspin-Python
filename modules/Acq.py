"""
Suggestions for acquisition parameters
"""
from java.lang import *
import de.bruker.nmr.mfw.root as root

import math
import sys
import os

sys.path.append(root.UtilPath.getTopspinHome()+ '/exp/stan/nmr/py/BioPY/modules/')

import CPDtools
import TopCmds
import GetNUCs as Nuc
import FREQ as fq

BioNuc= "H","N","C","CA","Ca","CO","Co","CB","Cb","D"

# First let's find out the dimensions of the pulsprog

def PPDIM():
  ppdim=1; aqseq=""
  ph2D=""; ph3D=""; ph4D=""
  Nucl1D=""; Nucl2D=""; Nucl3D=""; Nucl4D=""
  
  #Acquisition dimension from acq file
  Nucl1D="".join(letter for letter in Nuc.list()[0] if letter.isalpha())
  #TopCmds.MSG(Nucl1D)

  pp=TopCmds.GETPAR("PULPROG")
  dir=get_dir("PP_DIRS")
  Name=find_file(dir,pp)
  #TopCmds.MSG(Name)

  if os.path.exists(Name) == 1:
    f=open(Name, 'r')
    text=f.readlines()
    f.close()
  else:
    TopCmds.MSG("Pulse Program not found:  Exiting")
    TopCmds.EXIT()

  # Determine pulse sequence dimension and TPPI phases
  for line in text:
    lines = line.rstrip()
    
    if lines.find("aqseq") >=0:
      #Check for comments
      if lines.find(";") < 0 :
        aqseq="".join(letter for letter in lines if letter.isdigit())
      elif lines.find(";") > lines.find("aqseq"):
        aqseq="".join(letter for letter in lines if letter.isdigit())

    if lines.find("F1PH") >=0 or lines.find("F1EA") >=0 :
      if lines.find("F1PH") >=0 : search="F1PH"
      if lines.find("F1EA") >=0 : search="F1EA"
      #Check for comments
      if lines.find(";") < 0 :
		if ppdim < 2 : ppdim=2
		ph2D=find_phase(lines,search)
		ph2Dp=ph2D+")"
		ph2D=ph2D+" "
      elif lines.find(";") > lines.find(search):
		if ppdim < 2 : ppdim=2
		ph2D=find_phase(lines,search)
		ph2Dp=ph2D+")"
		ph2D=ph2D+" "

    if lines.find("F1QF") >=0:
      #Check for comments
      if lines.find(";") < 0 :
		if ppdim < 2 : ppdim = 2
		Nucl2D="_"
      elif lines.find(";") > lines.find("F1QF"):
		if ppdim < 2 : ppdim = 2
		Nucl2D="_"

    if lines.find("F2PH") >=0 or lines.find("F2EA") >=0 :
      if lines.find("F2PH") >=0 : search="F2PH"
      if lines.find("F2EA") >=0 : search="F2EA"
      #Check for comments
      if lines.find(";") < 0 :
		if ppdim < 3: ppdim = 3
		ph3D=find_phase(lines,search)
		ph3Dp=ph3D+")"
		ph3D=ph3D+" "
      elif lines.find(";") > lines.find(search):
		if ppdim < 3: ppdim = 3
		ph3D=find_phase(lines,search)
		ph3Dp=ph3D+")"
		ph3D=ph3D+" "

    if lines.find("F2QF") >=0:
      #Check for comments
      if lines.find(";") < 0 :
		if ppdim < 3 : ppdim= 3
		Nucl3D="_"
      elif lines.find(";") > lines.find("F2QF"):
		if ppdim < 3 : ppdim= 3
		Nucl3D="_"

    if lines.find("F3PH") >=0 or lines.find("F3EA") >=0 :
      if lines.find("F3PH") >=0 : search="F3PH"
      if lines.find("F3EA") >=0 : search="F3EA"
      #Check for comments
      if lines.find(";") < 0 :
		if ppdim < 4 : ppdim= 4
		ph4D=find_phase(lines,search)
		ph4Dp=ph4D+")"
		ph4D=ph4D+" "
      elif lines.find(";") > lines.find("F3PH"):
      
		if ppdim < 4 : ppdim= 4
		ph4D=find_phase(lines,search)
		ph4Dp=ph4D+")"
		ph4D=ph4D+" "

    if lines.find("F3QF") >=0:
      #Check for comments
      if lines.find(";") < 0 :
		if ppdim < 4 : ppdim = 4
		Nucl4D="_"
      elif lines.find(";") > lines.find("F3QF"):
		if ppdim < 4 : ppdim = 4
		Nucl4D="_"
		
  #TopCmds.MSG(ph2D+":2D\n"+ph3D+": 3D\n"+ph4D+": 4D")

  #TopCmds.MSG(str(ppdim)+" ppdim\n"+str(ph2D)+" ph2D")
  # From TPPI phases make a string corresponding to pulse nucleus
  for line in text:
    lines=line.rstrip()
    if ppdim >= 2 :
      if lines.find(ph2D) >= 0 and Nucl2D == "":
        #TopCmds.MSG(lines)
        Nucl2D=find_nuc(lines,ph2D)
        #TopCmds.MSG(Nucl2D)
      elif lines.find(ph2Dp) >=0 and Nucl2D == "":
        #TopCmds.MSG(lines)
        Nucl2D=find_nuc(lines,ph2Dp)
        #TopCmds.MSG(Nucl2D)

    if ppdim >= 3 :
      if lines.find(ph3D) >= 0 and Nucl3D == "": 
        #TopCmds.MSG(lines)
        Nucl3D=find_nuc(lines,ph3D)
        #TopCmds.MSG(Nucl3D)
      elif lines.find(ph3Dp) >= 0 and Nucl3D == "":
        #TopCmds.MSG(lines)
        Nucl3D=find_nuc(lines,ph3Dp)
        #TopCmds.MSG(Nucl3D)

    if ppdim >= 4 :
      if lines.find(ph4D) >= 0  and Nucl4D == "":
        #TopCmds.MSG(lines)
        Nucl4D=find_nuc(lines,ph4D)
      elif lines.find(ph4Dp) >=0  and Nucl4D == "":
        #TopCmds.MSG(lines)
        Nucl4D=find_nuc(lines,ph4Dp)
	
  #TopCmds.MSG(str(ppdim)+" :ppdim\n"+Nucl2D+" :Nucl2D\n"+Nucl3D+" :Nucl3D\n"+Nucl4D+" :Nucl4D\n")
  # Translate, Concatenate and return the Nucls

  if ppdim >= 4 and Nucl4D.isdigit(): Nucl4D="".join(letter for letter in Nuc.list()[int(Nucl4D)-1] if letter.isalpha())
  if ppdim >= 3 and Nucl3D.isdigit(): Nucl3D="".join(letter for letter in Nuc.list()[int(Nucl3D)-1] if letter.isalpha())
  if ppdim >= 2 and Nucl2D.isdigit(): Nucl2D="".join(letter for letter in Nuc.list()[int(Nucl2D)-1] if letter.isalpha())
  
  #TopCmds.MSG(Nucl1D+" :Nucl1D\n"+Nucl2D+" :Nucl2D\n"+Nucl3D+" :Nucl3D\n"+Nucl4D+" :Nucl4D\n")

  if ppdim==4:
    EXP= Nucl4D+Nucl3D+Nucl2D; aqseq="4321"

  if ppdim==3:
    if aqseq=="321": EXP= Nucl3D+Nucl2D
    if aqseq=="312": EXP= Nucl2D+Nucl3D
    if aqseq=="":    EXP= Nucl3D+Nucl2D; aqseq="321"

  if ppdim==2: EXP= Nucl2D; aqseq="21"
  
  return ppdim, aqseq, Nucl1D+EXP
	
def PPNUC(dim,fre):
  PP=TopCmds.GETPAR("PULPROG")
  ppnuc=[]
  temp_nuc=[]
  k=0

  for letter in range(len(PP)):
    if PP[letter].isupper():
      if PP[letter] != "A" and PP[letter] != "O" and PP[letter] != "X" :
        k=k+1
        if letter+1 < len(PP):
          if PP[letter+1] == "A" or PP[letter+1] == "O" or PP[letter+1] == "a" or PP[letter+1] == "o":
            ppnuc.append(PP[letter]+PP[letter+1])
          else:
            ppnuc.append(PP[letter])
        else:
          ppnuc.append(PP[letter])

  #Deal with non-standard names
  if k > dim:
    i=0; j=0 
    for letter in ppnuc:
      for item in BioNuc:
        if item == letter :
          if j == 0 or j == i-1: 
            temp_nuc.append(letter)
            j=i
          else:
            temp_nuc=[]
            j=0
      i=i+1
  if len(temp_nuc) == dim : ppnuc=temp_nuc

  if k < dim:
    ppnuc=[]
    for i in range(dim):ppnuc.append(fre[dim-1-i])

  return ppnuc, k
  
def PPACQ(aqseq,ppfre,ppnuc):
  
  ppacq=[]
  for i in range(len(ppfre)):
    ppacq.append(ppnuc[int(aqseq[i])-1])

  return ppacq

def SetInc(nuc,key,MAS):
  increment=[]
  SWNUC=key['CA']
  TauR=1000000./MAS

  for i in range(len(nuc)):

    if nuc[i].name=="CA" or  nuc[i].name=="Ca":SWNUC=key['CA']
    if nuc[i].name=="CO" or  nuc[i].name=="Co":SWNUC=key['CO']
    if nuc[i].name=="C" :SWNUC=key['C']
    if nuc[i].name=="N" :SWNUC=key['N']
    if nuc[i].name=="H" :SWNUC=key['H']

    #direct detect H exception
    if i==0 and nuc[i].name=="H": SWNUC=key['Hdet']
  
    freqhigh=nuc[i].ppm2offs(nuc[i].offsp+SWNUC/2.)
    freqlow =nuc[i].ppm2offs(nuc[i].offsp-SWNUC/2.)
    
    #TopCmds.MSG("carr "+str(nuc[i].offsp)+"\nHigh: "+str(freqhigh)+"\nLow: "+str(freqlow)+"\
    #\nBF: "+str(nuc[i].bf)+"\nOffs: "+str(nuc[i].offs))
    #TopCmds.MSG("carr "+str(nuc[i].offsp)+"\nBF: "+str(nuc[i].bf)+"\nOffs: "+str(nuc[i].offs))

    sw = (freqhigh-freqlow)
    incr=1000000./(freqhigh-freqlow)

    if incr > TauR:
      if nuc[i].name=="CO" or  nuc[i].name=="Co":
        incr=TauR*math.floor(incr/TauR)
      else :
        incr=TauR*math.floor(2*incr/TauR)
    if incr < TauR:
      incr=TauR/math.floor(TauR/incr)

    increment.append(incr)

  return increment

def find_nuc(lines,search):
  nuc=""
  if lines.find("=") < 0:
    i=lines.find(search)
    j=lines[i:].find(":")
    #TopCmds.MSG("found "+search+ "at position #"+str(i+j)+"\n"+lines)
    k=1
    nuc=lines[i+j+k]
    while nuc==" " and i+j+k+1 <= len(lines[i+j+k:]):
     k=k+1
     nuc=lines[i+j+k+1]
   
  if nuc=="f":
    nuc=lines[i+j+k+1]
  return nuc
      
def find_phase(lines,search):
	#Topspin 3 notation
	if lines.find("calph") >=0 :
	  i=lines.find(search)
	  j=lines[i:].find("calph")
	  k=lines[i+j:].find("(")+1
	  l=lines[i+j+k:].find(",")
	  ph=lines[i+j+k:i+j+k+l]
	  if ph.find(","):
		Phase=ph[:len(ph)]
	  else:
		Phase=ph

	#Topspin 2 MC notation
	else:
	  i=lines.find(search)
	  j=lines[i:].find("(")+1
	  k=lines[i+j:].find(",")
	  #TopCmds.MSG(str(i)+": i\n"+str(j)+": j\n"+str(k)+": k\n")
	  #TopCmds.MSG(lines[i+j:i+j+k])
	  #get first instance of incrementing phase
	  if lines[i+j:i+j+k].find("ip")>=0:
		l=lines[i+j:i+j+k].find("ip")
		ph=lines[i+j+l+1:i+j+l+3]
		if ph.find(","):ph=ph[:2]
		Phase=ph[:1]+"h"+ph[1:]
	  #get first instance of decrementing phase
	  if lines[i+j:i+j+k].find("dp")>=0:
		l=lines[i+j:i+j+k].find("dp")
		ph=lines[i+j+l+1:i+j+l+3]
		if ph.find(","):ph=ph[:2]
		Phase=ph[:1]+"h"+ph[1:]
	#TopCmds.MSG(search+" "+Phase)
	return Phase

def get_dir(Search):
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
    if lines.find(Search) >=0:
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
    print (dirs[i], found )
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
  
def PathAcqNuc(dim):

  dataset=TopCmds.CURDATA()
  path=dataset[3]+'/'+ dataset[0]+'/'+dataset[1]
  text=""
  if dim <= 1:
    acqu=path+'/acqu'
  if dim > 1: 
    acqu=path+'/acqu'+str(dim)
  
  return acqu
  
def GetFnMODE(dim):

  acqu=PathAcqNuc(dim)
  if os.path.exists(acqu) == 1:
    f=open(acqu, 'r')
    text=f.readlines()
    f.close()

  for line in text:
    lines = line.rstrip()
    if lines.find('##$FnMODE') >=0:
      j=lines.find('=')
      ThingIWant="".join(letter for letter in lines[j+1:] if letter.isdigit())

  #print ThingIWant
  return ThingIWant

def GetAcqNUC1(dim):

  #TopCmds.MSG(PathAcqNuc(dim))
  acqu=PathAcqNuc(dim)
  
  j=0
  k=1
  lines=" "

  if os.path.exists(acqu) == 1:
    f=open(acqu, 'r')
    text=f.readlines()
    f.close()

  for line in text:
    lines = line.rstrip()
    if lines.find('##$NUC1') >=0:
      j=lines.find('<')
      k=lines.find('>')
      ThingIWant=lines[j+1:k]

  return ThingIWant

def SetAcqNUC1(dim,Nucl):

  acqu=PathAcqNuc(dim)
  acqus=acqu+"s"
  acqu_bak=PathAcqNuc(dim)+".bak"
  
  j=0
  k=1
  lines=" "
  newline=[]

  if os.path.exists(acqu) == 1:
    #TopCmds.MSG("It opened "+str(dim))
    f=open(acqu, 'r')
    text=f.readlines()
    f.close()
  
  if os.path.exists(acqu_bak):os.remove(acqu_bak)
  os.rename(acqu,acqu_bak)
  
  file=open(acqu,'w')

  for line in text:
    lines = line.rstrip()
    if lines.find('##$NUC1') >=0:
      newline.append("##$NUC1= <"+Nucl+">\n")
    else:
      newline.append(line)

  for line in newline:
    file.write(line)

  file.close()
  return

def SetFnMODE(dim,mode):

  #TopCmds.MSG(str(dim)+" "+mode)
  
  acqu=PathAcqNuc(dim)
  acqus=acqu+"s"
  acqu_bak=PathAcqNuc(dim)+".bak"
  
  j=0
  k=1
  lines=" "
  newline=[]

  if os.path.exists(acqu) == 1:
    f=open(acqu, 'r')
    text=f.readlines()
    f.close()
  
  if os.path.exists(acqu_bak):os.remove(acqu_bak)
  os.rename(acqu,acqu_bak)
  
  file=open(acqu,'w')
  
  for line in text:
    lines = line.rstrip()
    if lines.find('##$FnMODE') >=0:
      newline.append("##$FnMODE= "+str(mode)+"\n")
    else:
      newline.append(line)

  for line in newline:
    file.write(line)

  file.close()
  return
