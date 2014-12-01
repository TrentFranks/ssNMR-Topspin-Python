import math
import sys
import os
from sys import argv
sys.path.append(root.UtilPath.getTopspinHome()+ '/exp/stan/nmr/py/BioPY/modules/')

import GetNUCs as Nuc
import FREQ as freq
import Acq
from GetLib import pul

ret=u"\u000D"
spc=u"\u0020"

NamedNuc= "CA","Ca","CO","Co","CB","Cb"

cmds=argv

CA = 45.;CO = 20.;N = 50.;H = 15.;C = 350.; CB=80.; Hdet= 50.
key = {'CA':CA,'CO':CO,'N':N,'H':H,'C':C,'Hdet':Hdet,'CB':CB}
FnMODE="5"
AQ=""

i=1
if len(cmds) >= 2 :
  for cmd in cmds[1:]:
    if cmd.find('-q') >=0 or cmd.find('-Q') >=0 or cmd.find('-qt') >=0 or cmd.find('-QT') >=0 :
	  quiet=1
    if   cmd.find('CA') >=0 :
	  if cmds[i].isdigit(): CA=cmds[i]
    elif cmd.find('CO') >=0 :
	  if cmds[i].isdigit(): CO=cmds[i]
    elif cmd.find('C') >=0 :
	  if cmds[i].isdigit(): C=cmds[i]
    elif cmd.find('N') >=0 :
	  if cmds[i].isdigit(): N=cmds[i]
    elif cmd.find('H') >=0 :
	  if cmds[i].isdigit(): H=cmds[i]
    elif cmd.find('Hdet') >=0 :
	  if cmds[i].isdigit(): Hdet=cmds[i]
    if cmd.find('aq') >=0 or cmd.find('AQ') >=0 or cmd.find('ACQ') >=0 or cmd.find('acq') >=0 :
      if cmds[i].isalpha(): AQ=cmds[i]
    i=i+1
	  
Channels=Nuc.list()
#MSG("Channels :\n"+str(Channels))
Dim=[]
NucDim=[]
ppnuc=[]
ppacq=[]
sw=[]
increment=[]

ppdim, aqseq, ppfre = Acq.PPDIM()

#MSG(str(ppdim)+" "+str(aqseq)+" "+str(ppfre))
#EXIT()

MAS=pul.GetPar('MAS',"")  # float(GETPAR("CNST 31"))

aqdim=GETACQUDIM()
aqtime=GETPAR(str(aqdim) +" AQ")

# So far, I know max dims in pp (ppdim), which nuclei correspond to which dims(ppfre)
# which dims are evolved first (aqseq), the name of the pulse program (PP)
# and what I'm set up to acquire (aqdim).

# Now lets take clues from the ppname to see if we can be more specific

ppnuc, n_nuc= Acq.PPNUC(ppdim,ppfre)
#MSG("n_nuc is: "+str(n_nuc))

#Now if we've entered arguments we want to plug it into the previous
foo=[]
for item in NamedNuc:
  i=0
  while i < len(AQ):
    if AQ[i:].find(item)>=0:
      i=i+len(item)
      foo.append(item)
    i=i+1
#MSG(str(foo)+" "+str(ppnuc))

#replace argument names if appropriate, but always leave the last
for i in range(len(foo)):
  replaced=0
  for j in range(len(ppnuc)-1):
    if foo[i][0].find(ppnuc[j])>=0 and replaced == 0:
      ppnuc[j]=foo[i]; replaced=1; 
  
# Now we arrange according to order of acquisition
ppacq= Acq.PPACQ(aqseq,ppfre,ppnuc)

#MSG(str(ppdim) +" "+str(aqseq)+" "+str(ppfre)+" "+str(ppnuc)+" "+str(ppacq))

"""
Indirect dimension SW lists
"""

# Initialize Classes named Dim and ppnuc 
# Since proc and acq files only exist up to acqdim, We'll only fill up to acqdim

for i in range(aqdim):
  Dim.append(freq.fq(Channels[i],i+1))

j=0; k=0
for fre in ppacq:
  found=0
  #MSG(fre+str(ppacq))
  if fre.find("H") >= 0:
    for i in range(len(Dim)):
      if Dim[i].name.find("H")>=0 and found ==0: 
        #MSG(fre+" is fre in ppacq\n"+str(Dim[i].name))
        j=i; found =1
    ppnuc[k]=freq.fq(fre,j+1)
  elif fre.find("C") >= 0: 
    for i in range(len(Dim)):
      if Dim[i].name.find("C")>=0 and found ==0: 
        #MSG(fre+" is fre in ppacq\n"+str(Dim[i].name))
        j=i; found =1
    ppnuc[k]=freq.fq(fre,j+1)
  elif fre.find("N") >= 0:
    for i in range(len(Dim)):
      if Dim[i].name.find("N")>=0 and found ==0: 
        #MSG(fre+" is fre in ppacq\n"+str(Dim[i].name))
        j=i; found =1
    ppnuc[k]=freq.fq(fre,j+1)
  k=k+1

# Take care of Acquisition types
#MSG("I'll start it again!")
for i in range (aqdim):
  #MSG(str(i))
  if Acq.GetAcqNUC1(i+1) != ppnuc[i].nucl :
    Acq.SetAcqNUC1(i+1,ppnuc[i].nucl); SLEEP(0.25)
  if i+1 > 1 :
    Acq.SetFnMODE(i+1,FnMODE); SLEEP(0.25)
  if i+1 < aqdim:
    XCMD(str(i+1)+" TD 1"); SLEEP(0.25)

#Reload so everything updates.
RE(CURDATA()); SLEEP(0.25); XCMD('eda'); SLEEP(0.25)

increment=Acq.SetInc(ppnuc,key,MAS)

# Prepare the interaction Box for User

if aqdim == 1 :  Title="1D Acquisition Parameters"
if aqdim == 2 :  Title="2D Acquisition Parameters"
if aqdim == 3 :  Title="3D Acquisition Parameters"
if aqdim == 4 :  Title="4D Acquisition Parameters"

Header = ppnuc[0].name + " Detected"

items=[]
value=[]
value0=[]
units=[]
place=[]

for dim in range(aqdim):

  swh=str('%.2f' %(1000000.0/increment[dim]))
  ppm=((ppnuc[dim].offs2ppm(float(swh)/2))-(ppnuc[dim].offs2ppm(-float(swh)/2)))
  inf=str('%.2f' %(increment[dim]))
  swp=str('%.2f' %ppm)

  if dim==0:
    inf0=str('%.2f' %float(GETPAR("DW")))
    swh0=str('%.2f' %float(GETPAR(str(aqdim)+" SWH" )))
    swp0=str('%.2f' %float(GETPAR(str(aqdim)+" SW" )))
    #MSG(inf0 + " " + swh0 + " " + swp0)

    inf=str('%.2f' %(float(inf)/2.))
    items.append(ppnuc[dim].name+"\nAqDW");items.append("AqSWH");items.append("AqSW")
    value.append(inf);   value.append(swh)    ;value.append(swp)
    units.append("us");   units.append("Hz")    ;units.append("ppm")
    place.append("1");    place.append("1")     ;place.append("1")
    value0.append(inf0); value0.append(swh0)  ;value0.append(swp0)
    
  else:
    inf0=str('%.2f' %float(GETPAR(str(aqdim-dim)+" IN_F")))
    swh0=str('%.2f' %float(GETPAR(str(aqdim-dim)+" SWH" )))
    swp0=str('%.2f' %float(GETPAR(str(aqdim-dim)+" SW" )))
    #MSG(inf0 + " " + swh0 + " " + swp0)
    
    items.append(ppnuc[dim].name+"\n INF "+str(len(increment)-dim))
    items.append(" SWH "+str(len(increment)-dim))
    items.append(" SW " +str(len(increment)-dim))
    value.append(inf);   value.append(swh)   ;value.append(swp)
    units.append("us");   units.append("Hz")   ;units.append("ppm")
    place.append("1");    place.append("1")    ;place.append("1")
    value0.append(inf0); value0.append(swh0) ;value0.append(swp0)
    
Stuff=INPUT_DIALOG(Title,Header,items,value,units,place,\
  ["Accept","Close"], [ret,spc], 10)
  
if Stuff == None : EXIT()
  
i=0
Changeit=1

for item in Stuff:
  if i%3==0 : Changeit=1 #reset every group of 3

  if (item != value[i]) or (value[i] != value0[i]) :
    if i%3==0 :
      if i==0:
        #MSG('%i' %((len(Stuff)/3)-math.floor(i/3))+" DW "+item )
        XCMD('%i' %((len(Stuff)/3)-math.floor(i/3))+" DW "+item )
        if (item != value[i]): Changeit=0
      else :
        #MSG(str('%i' %((len(Stuff)/3)-math.floor(i/3))+" INF "+item ))
        XCMD(str('%i' %((len(Stuff)/3)-math.floor(i/3))+" INF "+item ))
        if (item != value[i]): Changeit=0
    elif (i-1)%3==0 :
      if Changeit==1:
        #MSG(str('%i' %((len(Stuff)/3)-math.floor(i/3))+" SWH "+item ))
        XCMD(str('%i' %((len(Stuff)/3)-math.floor(i/3))+" SWH "+item ))
        if (item != value[i]): Changeit=0
    elif (i-2)%3==0 :
      if Changeit==1:
        #MSG(str('%i' %((len(Stuff)/3)-math.floor(i/3))+" SW "+item ))
        XCMD(str('%i' %((len(Stuff)/3)-math.floor(i/3))+" SW "+item ))
        if (item != value[i]): Changeit=0
  i=i+1

PUTPAR(str(aqdim)+" AQ",aqtime)
