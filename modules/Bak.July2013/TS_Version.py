import de.bruker.nmr.mfw.root as root
import sys

def get():
	CurInst=root.UtilPath.getTopspinHome()
	CurFile=CurInst+"/conf/instr/curinst"

	#MSG(CurFile)

	f=open(CurFile, 'r')
	text=f.readlines()
	f.close()

	for line in text:
	  CurFile = CurInst+"/conf/instr/"+line.rstrip()+"/uxnmr.info"

	#MSG(CurFile)
	f=open(CurFile,'r')
	text=f.readlines()
	f.close

	Version=""

	for lines in text:
	  line = lines.rstrip()
	  if line.find("Release")>=0:
		j=line.find("Version")
		Version=line[j+8:]

	if Version.find("3.2") >=0:
	  Release="3"

	if Version.find("2.0") >=0 or Version.find("2.1") >=0 \
	or Version.find("2.2") >=0 or Version.find("2.3") >=0:
	  Release="2"

	return Version, Release
