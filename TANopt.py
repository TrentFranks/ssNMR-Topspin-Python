"""
Create a series of Tangent shapes
Run an experiment with each 
I think that's enough

W.T. Franks FMP Berlin
"""

import math
sys.path.append(root.UtilPath.getTopspinHome()+ '/exp/stan/nmr/py/BioPY/modules/')
import Tangent
import IntShape

Empty=0
B=[]
D=[]
Name=[]
"""
First, let's interact with the user to generate a series of ramps

We need to know which pulse to change, and the variables to change it.
The full list of variables is probably not necessary, as this is a touch-up
optimization. 
"""
dia = INPUT_DIALOG("Tangent Ramp Shape Optimization","",\
["SP NUM","Points","Scale","Initial Delta (+/-)", "Final Delta(+/-)", "Steps in Delta", \
"Initial Beta", "Final Beta", "Steps in Beta"],\
["0","500","75","5","25","5","-20","20","9"],\
["SPNAM #","points","%","%","%","steps","","","steps"],\
["1","1","1","1","1","1","1","1","1"],\
["Accept","Close"], ['a','c'], 10)

if dia == None: EXIT()
""" 
Let's check the scaling to make sure we don't change the condition, but we'll let it happen 
if that is what the user intends.
"""

SP=GETPAR2("SPNAM "+dia[0])
if SP == "gauss" or SP == "None" : Empty=1
  
Scale=float(dia[2])
if not Empty: 
  AvgAmp=IntShape.Integrate(SP)
  if math.fabs(AvgAmp-float(dia[2])) > 5.:
    value=SELECT("Scaling Error",\
    "The scaling and the previous power differs by more than 5%.\n\n"+\
    "This may effect the quality of the match condition, please choose how to proceed:",\
    ["Use Previous: " + str("%3.1f" %AvgAmp), "Use "+str("%3.1f" %Scale)])
  
    if not value: Scale=AvgAmp

#MSG(str(Scale)+ "  Scale")

"""
Another safety check so we don't go over 100 or under 0

"""

PNT=int(dia[1])
D0=float(dia[3])
DF=float(dia[4])
DS=int(dia[5])

B0=float(dia[6])
BF=float(dia[7])
BS=int(dia[8])

if D0 > 100. or D0 < 0. or DF > 100. or DF < 0.: 
  value=SELECT("Delta Error",\
  "The pulse shapes will cross over 0 or 100% of allowed output.Please choose how to proceed:",\
  ["I don't care, do what I say!" , "You got me, just use the natural limits"])
  
  if not value: 
    if D0 > 100.:D0 =100.
    if D0 < 0.  :D0 =0.
    if DF > 100.:DF =100.
    if DF < 0.  :D0 =0. 
"""

Let's generate the wave files, and store the names and values.

"""
DB=(BF-B0)/float(BS)

Names = []

#Set initial conditions
if DS >  1 : DD=(DF-D0)/float(DS-1)
if DS <= 1 : DD=0.0
if BS >  1 : DB=(BF-B0)/float(BS-1)
if BS <= 1 : DB=0.0

#Run experiment with 0 steps indicated (Assume no variation desired)
#Do not repeat exps. if first and last value are the same 

if DD == 0.0 : DS=1
if DB == 0.0 : BS=1

for i in range(DS):
  D.append(D0+i*DD)

for i in range(BS):
  B.append(B0+i*DB)

for i in range(DS):
  for j in range(BS):
    Name.append("Tan_"+str(D[i])+"D_"+str(B[j])+"B_"+str(PNT)+"P.wave")
    command="TAN -name "+Name[i*BS+j]+" -sp "+dia[0]+" -sc "+str(Scale)+" -b "+str(B[j])+" -d "+str(D[i])+" -np "+dia[1]
    XCMD(command)
    
"""
Files are generated from above
Lets get ready to acquire.  

Since some of this next part is general, I should make it into a subroutine.

"""
#Approximate the time for the experiment

Delay=float(GETPAR("D 1"))
NS=int(GETPAR("NS"))
Dummy=int(GETPAR("DS"))

EXPT=(DS*BS*NS*Delay)+(DS*Delay)
ExHr=math.floor(EXPT/3600.)
ExMn=math.floor((EXPT%3600)/60)
ExSc=EXPT%60

# Report Time in convenient notation
if ExHr >= 1:
  NorY=CONFIRM("Run Experiments","The Experiment requires apprx. "\
  + str(ExHr) + " hrs " + str(ExMn) + " min"\
  + " sec \nAcquire the data set?")
else:
  NorY=CONFIRM("Run Experiments","The Experiment requires apprx. "\
  + str(ExMn) + " min  \nAcquire the data set?")

if NorY:

  TakeDummy=1  #take dummy scans only for first experiment
  k=0

  for i in range(DS):
    for j in range(BS):
      PUTPAR(SP, Name[k])
        #Must set data directories properly, which is not done yet
      #RE_IEXNO RE_IPROCNO
      #WR WR_PATH
        #Displaying the data is going to be a bitch.
        #ZG()
      MSG(Name[k])
      SLEEP(1)
      if TakeDummy==1:
        PUTPAR("DS","0")
        TakeDummy=0
      SHOW_STATUS("Tangent Ramp shape optimization in progress")
      k=k+1
  
#Put back to original after experiment done.
PUTPAR("DS",str(Dummy))


def ChangeTitle(text):
  PWD=CURDATA()
  #MSG(str(PWD))
  ttl= PWD[3] + "/data/" + PWD[4]+ "/nmr/" + PWD[0]+ "/" +PWD[1]+"/pdata/"+PWD[2]+"/title"
  title= open(ttl, "w")
  title.write(text)

"""
