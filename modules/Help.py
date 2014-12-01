"""
Help interaction Modules:
W.T. Franks FMP Berlin
"""
import de.bruker.nmr.mfw.root as root
import TopCmds

def CP():
  
  TopCmds.MSG("<html><p style='text-align: center;'><font size=14><font color=\'0000FF\'>"+\
  "Cross-Polarization Setup Help</p></font><br>"+\
  "\n\nCalculate Amplitudes for CP Match Conditions\n"+\
  "Hard pulse power, duration, and shapes are needed\n"+\
  "\n"+\
  "Arguments:\n"+\
  "-dB  : interact with db instead of watts (TS3+)\n"+\
  "-qt  : Quiet the initial Hard-pulse input\n"+\
  "-help: This Window\n"+\
  "\n"+\
  "Adjusts amplitude for shaped pulses\n"+\
  "Suggests an appropriate match condition for your MAS Rate\n"+\
  "Suggests an appropriate decoupling field if warranted\n"+\
  "\n"+\
  "Path : "+str(root.UtilPath.getTopspinHome())+ "/exp/stan/nmr/py/BioPY/modules/Setup.py\n"+\
  "modules: CalCP\n"+\
  "wrappers:HC, HN, NCA, NCO, NH, CH, see also LG \n"+\
  "\n"+\
  "Faults:\n"+\
  "May guess too low by one rotor frequency.\n"+\
  "Failures:\n"+\
  "Shape is not specified (dialog pops up) or does not exist.")

def Dec():
  
  TopCmds.MSG("<html><p style='text-align: center;'><font size=14><font color=\'0000FF\'>"+\
  "Decoupling Setup Help</p></font><br>"+\
  "\n\nCalculate amplitude for CPD Decoupling\n"+\
  "Hard pulse power, duration, and cpdprg are needed\n"+\
  "\n"+\
  "Arguments:\n"+\
  "-dB  : interact with db instead of watts (TS3+)\n"+\
  "-qt  : Quiet the initial Hard-pulse input\n"+\
  "-help: This Window\n"+\
  "\n"+\
  "Determines previous decoupling field for first suggestion,\n"+\
  "Gives warnings if the field is higher than the hard pulse field,\n"+\
  "It will not set conditions higher than a defined level\n"+\
  "\n"+\
  "Path : "+str(root.UtilPath.getTopspinHome())+ "/exp/stan/nmr/py/BioPY/modules/Setup.py\n"+\
  "modules: CalDec, DecSafely\n"+\
  "wrappers: HDec, Cdec, NDec\n"+\
  "Defaults are defined in wrappers\n"+\
  "Faults:\n"+\
  "The decoupling tip angle is pre-assumed; it may be wrong for your cpdprg \n"+\
  "Channel specific parameter definitions in wrappers")
  
def Sym():
  
  TopCmds.MSG("<html><p style='text-align: center;'><font size=14><font color=\'0000FF\'>"+\
  "Symmetry-based Recoupling Setup Help</p></font><br>"+\
  "\n\nCalculate match amplitude for C and R sequences\n"+\
  "Hard pulse power and duration are needed\n"+\
  "\n"+\
  "Arguments:\n"+\
  "-dB  : interact with db instead of watts (TS3+)\n"+\
  "-qt  : Quiet the initial Hard-pulse input\n"+\
  "-help: This Window\n"+\
  "\n"+\
  "Can be used for experiments that can be descrbed by symmetry numbers\n"+\
  "Gives warnings if the field is higher than the hard pulse field,\n"+\
  "And will not set powers greater than hard pulse field\n"+\
  "\n"+\
  "Path : "+str(root.UtilPath.getTopspinHome())+ "/exp/stan/nmr/py/BioPY/modules/Setup.py\n"+\
  "modules: CalcSym \n"+\
  "wrapper: C72, SPC5_2, DARR, etc.\n"+\
  "Limitations: One channel + CW Decoupler only")

def SelPul():
  
  TopCmds.MSG("<html><p style='text-align: center;'><font size=14><font color=\'0000FF\'>"+\
  "Soft Pulse Setup Help</p></font><br>"+\
  "\n\nCalculate amplitude for Soft Pulses\n"+\
  "Requirements: Hard Pulse Parameters, Soft Pulse Shape\n"+\
  "\n"+\
  "Arguments:\n"+\
  "-dB  : interact with db instead of watts (TS3+)\n"+\
  "-help: This Window\n"+\
  "\n"+\
  "Adjusts amplitude for shaped pulses\n"+\
  "Suggests an Tau_R*(N+1/2) pulse time if not already set.\n"+\
  "\n"+\
  "Path : "+str(root.UtilPath.getTopspinHome())+ "/exp/stan/nmr/py/BioPY/modules/SelPul.py\n"+\
  "modules: CalSP\n"+\
  "wrappers: CAexc, CAref, COexc, COref\n"+\
  "Faults:\n"+\
  "May guess timing to be too short.\n"+\
  "Failures:\n"+\
  "If shape is not specified (dialog pops up) or does not exist.\n"+\
  "if the shape exists, the next calculation will be successful.")
  
def XhhC():

  TopCmds.MSG("<html><p style='text-align: center;'><font size=14><font color=\'0000FF\'>"+\
  "XhhC Setup Help</p></font><br>"+\
  "\n\nCopy CP amplitudes, adjust conditions for ramps\n"+\
  "Hard pulse power, duration, and shapes are needed\n"+\
  "\n"+\
  "Arguments:\n"+\
  "-dB  : interact with db instead of watts (TS3+)\n"+\
  "-help: This Window\n"+\
  "\n"+\
  "Adjusts amplitude for shaped pulses\n"+\
  "Copies HX match condition from previous set-ups\n"+\
  "\n"+\
  "Path : "+str(root.UtilPath.getTopspinHome())+ "/exp/stan/nmr/py/BioPY/modules/XhhC.py\n"+\
  "modules: copyCP\n"+\
  "wrappers: CH,NH,HC \n"+\
  "\n"+\
  "Failures:\n"+\
  "Shape is not specified (dialog pops up) or does not exist.")

def Dream():
  TopCmds.MSG("<html><p style='text-align: center;'><font size=14><font color=\'0000FF\'>"+\
  "DREAM Setup Help</p></font><br>"+\
  "\n\nThere is nothing here")

def TAN():
  TopCmds.MSG("<html><p style='text-align: center;'><font size=14><font color=\'0000FF\'>"+\
  "Tan Ramp Calculator Help</p></font><br>"+\
  "\n\nComputes a TANGENT pulse shape with defined Start and End"+\
  "Requirements: \n"+\
  "\n"+\
  "Arguments:\n"+\
  "-sp:shaped pulse name\n"+\
  "-d : delta (+/- d%)\n"+\
  "-b : beta (curvature)\n"+\
  "-p : number of points (default 1000)\n"+\
  "-np: number of points\n"+\
  "-sc: number of points\n"+\
  "-name : specify name\n"+\
  "\n"+\
  "Path : "+str(root.UtilPath.getTopspinHome())+ "/exp/stan/nmr/py/BioPY/modules/TAN.py\n"+\
  "modules: TAN.py\n"+\
  "wrappers: none \n"+\
  "\n"+\
  "Failures:\n"+\
  "")

def LG():
  TopCmds.MSG("<html><p style='text-align: center;'><font size=14><font color=\'0000FF\'>"+\
  "LG Setup Help</p></font><br>"+\
  "\n\nComputes Various Lee-Goldburg conditions"+\
  "Requirements:  Hard pulse power, duration, and possibly shapes are needed\n"+\
  "\n"+\
  "Arguments:\n"+\
  "-dB  : interact with db instead of watts (TS3+)\n"+\
  "-qt  : Quiet the initial Hard-pulse input\n"+\
  "-help: This Window\n"+\
  "\n"+\
  "-SW  : Determine LG parameters given a set sweep width \n"+\
  "-Fld : Determine LG parameters given a set B1eff field \n"+\
  "-pul : Determine LG parameters given a set FSLG 90 pulse \n"+\
  "Default is to set a B1 field \n"+\
  "\n"+\
  "Path : "+str(root.UtilPath.getTopspinHome())+ "/exp/stan/nmr/py/BioPY/modules/LeeGoldburg.py\n"+\
  "modules: LeeGoldburg, Setup.CalcCP\n"+\
  "wrappers: none \n"+\
  "\n"+\
  "Failures:\n"+\
  "")
  
def Merger():
  TopCmds.MSG("<html><p style='text-align: center;'><font size=14><font color=\'0000FF\'>"+\
  "Merging Help</p></font><br>"+\
  "\n\nMerge Parameters Between Experiments"+\
  "Requirements: Previous Experiments\n"+\
  "\n"+\
  "Arguments:\n"+\
  "-dB  : interact with db instead of watts (TS3+)\n"+\
  "-f   : open and close files instead of switching windows\n"+\
  "-EXPNO ##: grab from experiment number ## (default to n-1)\n"+\
  "-qt  : quiet all interaction- \n\n"+\
  "By default, the pulse program name is used to determine parameter\n"+\
  "To Specify Parameters input the elements separately or in a string.\n"+\
  "      Specify Hard pulses separately (hNCA H C)\n"+\
  "      H C N : Update hard pulses \n"+\
  "      HC HN NCO NCA NH CH hhC : Specified CP parameters\n"+\
  "      CX: PDSD/DARR \n"+\
  "      HDec: H-Dec\n"+\
  "      ph  : Phasing \n"+\
  "\nPath : "+str(root.UtilPath.getTopspinHome())+ "/exp/stan/nmr/py/BioPY/modules/\n"+\
  "modules: Merge, MergeGet, MergePut\n"+\
  "wrappers: MrMerger \n"+\
  "\n"+\
  "Failures: Incorrect dict keys\n"+\
  "")
