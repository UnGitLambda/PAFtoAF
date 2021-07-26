# PAFtoAF
#### by Eyal Cohen
Currently student in Université de Paris  
eyal.cohen@etu.u-paris.fr

## Introduction

PAFtoAF is a tool, written in python, used to reduce a Preference-based Argumentation Framework (into an Argumentation Framwork).  
PAFtoAF can be used in two ways :

* Using the terminal.
* Using the PAFtoAFGUI.

## Installation and requirements

PAFtoAF can be installed with the GUI on github at <https://github.com/UnHommeLambda/PAFtoAF>.  
PAFtoAF requires python 3.X, the python libraries : sys, os, copy, platform, pathlib.  
PAFtoAFGUI also requires the libraries : matplotlib, tkinter, networkx, TkinterDnD2, datetime.  
Make sure to keep both files in the same directory or the GUI might not work.  

## How to use it

### Command Line

To use PAFtoAF using a terminal here is the list of parameters and options you can use :  
  - -f \<file\>, the input, the preference-based argumentation framework.  
  - -fo \<format\>, the format of the input file, for a list of supported formats use the option --formats.  
  - [-p \<task\>], the computational problem, use --problems to see the ones supported.  
  - [-r \<reduction\>], the reduction you want to use on the PAF, use --reductions to see the available reductions.  
  - [-a \<query\>], used for prblems DC and/or DS, it is the argument concerned by the problem.  
  - [-out \<filename(s)\>], the output for the resulting AF to be printed on,
  if you want the output to be on the terminal use stdout as filename, if you wish to have the AF printed to  multiple files,
  state every file this way : [file1, file2, file3...].  
  - [-s \<solvername\>], the name of the solver you want to use to compute your task (if none is indicated,
  mu-toksia will be chosen as default on windows and jArgSemSAT on Linux and MacOS.  
  - [-sp \<solverpath\>], the path to the solver, if none is indicated the program will 
  scan the current directory to find the solver mu-toksia and will raise an Exception if it does not find it.  
  Options :
  - --help prints this message.  
  - --problems prints the lists of available computational problems.  
  - --formats prints the list of accepted file formats.  
  - --informations for informations about the version and the author.  

### The GUI : PAFtoAFGUI.py

To use the GUI make sure that the file PAFtoAF.py and the file PAFtoAFGUI.py are in the same folder.  
Then you have 3 ways of doing it :  
  - Executing the PAFtoAFGUI executable file.  
  - Using a terminal (or command Prompt) and typing python (or python3, depending on you installation) followed by PAFtoAFGUI.py as :  
  python PAFtoAFGUI.py  
  - Using an IDE (such as the IDLE python, Spyder, Visual, etc...) opening the file in the IDE and then running it.  
Then on the GUI you can click the Help button (at the top) for more help on how it works, the formats button to have
a better understanding of the accepted formats, the problems buttons to see about the available tasks and their meanings.  
##### The save button  
It allows you to save the parameters you entered in the GUI as the corresponding command line in a text file.  
##### The download button  
It allows you to save the AF (resulting from the reduction) into a new file.  

### Bugs  
To file bugs reports, or feature requests, please send an email to <eyal.cohen@etu.u-paris.fr>.  

## Licence  
#TODO

