"""
Parse the current pulse program,
Find all active external subroutine files,
then open them into an editor.
"""

pulprog=GETPAR("PULPROG")
#MSG("The Pulse Program is " + str(pulprog) )

ppText = GET_PULSPROG_TEXT(pulprog)
#VIEWTEXT(title=str(pulprog), header="", text=ppText, modal=0)
            # View in a Text Editor    

def devide_into_lines(Text):
    lines = []
    about = ''
    for letter in Text:
        about = about + letter
	if letter == '\n' :
	    lines.append(about)
	    #MSG(about)
	    #print(about)
	    about = ''
    return lines
	
def get_all_included(Text):
    files = []
    i=0
    while i < len(Text):
       about=''
       if Text[i].find("include") >= 0 :
          j = Text[i].find("<")
          k = Text[i].find(">")
	  about = Text[i][j+1:k]
	  files.append(about)
       i=i+1

    return files
    
def get_all_active(Text):
    files = []
    i=0
    n=0
    while i < len(Text):
       about=''
       if Text[i].find("include") >= 0 : 
          if Text[i].find(";") >= 0:                    #Commented in some way
	     if Text[i].find(";") > Text[i].find(">") : #Commented after 
                j = Text[i].find("<")
                k = Text[i].find(">")
                about = Text[i][j+1:k]
                files.append(about)
          else:                      #Not Commented
             j = Text[i].find("<")
             k = Text[i].find(">")
	     about = Text[i][j+1:k]
	     files.append(about)
       i=i+1
    return files

def get_all_subr(Text):
    files = []
    i=0
    while i < len(Text):
       about=''
       if Text[i].find("include") >= 0 :
          j = Text[i].find("<")
          k = Text[i].find(">")
          l = Text[i].find(".")
          #print Text[i][k-4:k]
          if Text[i][k-4:k] == str("subr") :
             about = Text[i][j+1:k]
             files.append(about)
       i=i+1

    return files
    
def get_all_active_subr(Text):
    files = []
    i=0
    n=0
    while i < len(Text):
       about=''
       if Text[i].find("include") >= 0 : 
          if Text[i].find(";") >= 0:                   #Commented in some way
	     if Text[i].find(";") > Text[i].find(">") :#Commented after
                j = Text[i].find("<")
                k = Text[i].find(">")
		#print Text[i][l:k]
                if Text[i][k-4:k] == str("subr") :
	           about = Text[i][j+1:k]
		   files.append(about)
          else:                      #Not Commented
             j = Text[i].find("<")
             k = Text[i].find(">")
             if Text[i][k-4:k] == 'subr' :
	        about = Text[i][j+1:k]
		files.append(about)
       i=i+1
    return files


gourds = devide_into_lines(ppText)
cow    = get_all_included(gourds)
fish   = get_all_active(gourds)
fowl   = get_all_subr(gourds)
pig    = get_all_active_subr(gourds)

#MSG( "The included files are: \n " + str(cow) )
#print cow
#print
#MSG( "The uncommented files are: \n " + str(fish) )
#print fish
#print
#MSG( "The included subroutines are: \n " + str(fowl) )
#print fowl
#print
#MSG( "The uncommented files are: \n " + str(pig) )
#print pig
#print

i=0
while i < len(pig):
   incl_name=pig[i]
   command= ('edpul ' +str(incl_name) )
   XCMD(command)
   i=i+1

