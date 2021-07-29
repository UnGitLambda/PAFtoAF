# PAFtoAF
#### by Eyal Cohen
Currently student in Université de Paris  
eyal.cohen@etu.u-paris.fr

## Introduction

PAFtoAF is a tool, written in python, used to reduce a Preference-based Argumentation Framework (into an Argumentation Framwork).  
PAFtoAF can be used in two ways :

* Using the terminal.
* Using the PAFtoAFGUI.

### File formats  

PAFtoAF reads Preference-based Argumentation Framework (PAF) and 'reduces' them, meaning it combines the attack and preference relations into a new one (sometimes called defeat relation).  
The formats of Argumentation Framework (AF) so far were Trivial Graph Format (TGF) and Aspartix (APX).  
For the sake of the project I had to adapt these format to PAFs, creating the Preference-Based Trivial Graph Format (PTGF) and the Preference-Based Aspartix (PAPX).  
Here is how it was done :

- The .tgf format is written as follows : every argument is indicated (by its name)  
then a \# is put and every attack is written under the \# as : arg1 arg2.  
So for the .ptgf format all I did was add a second # after listing every attack  
and writing the preferences under this second \# the same way as with attacks.  
Here is an exemple :  
1  
2  
3  
\#  
1 2  
2 3  
\#  
2 1  

- The .apx format is quite different than the .tgf.  
Every argument a is written this way : 'arg(a).'  
Every attack is like this : 'att(a,b).'  
So in the .papx, every preference is written 'pref(a,b).'  
Here is the same PAF as above but in papx instead of ptgf :  
arg(1).  
arg(2).  
arg(3).  
att(1,2).  
att(2,3).  
pref(2,1).  
  
The only thing that matters, regarding the papx format, is that an attack att(a,b). or a preference pref(a,b). must be declared after the arguments arg(a). and arg(b).  
But you can write the same PAF by writing : 
  
arg(1).  
arg(2).  
att(1,2).  
pref(2,1).  
arg(3).  
att(2,3).  

## Installation and requirements

PAFtoAF can be installed with the GUI on github at <https://github.com/UnHommeLambda/PAFtoAF>.  
PAFtoAF requires python 3.X, the python libraries : sys, os, copy, platform, pathlib.  
PAFtoAFGUI also requires the libraries : matplotlib, tkinter, networkx, TkinterDnD2, datetime.  
Make sure to keep both files in the same directory or the GUI might not work.  

#### PAFtoAFcheckup  

To make sure every python library is installed (and accessible) and that python's version is up to date  
please run the PAFtoAFcheckup.py file that will inform you of every missing module.

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
  jArgSemSAT will be chosen as default on windows and mu-toksia on Linux and MacOS).  
  - [-sp \<solverpath\>], the path to the solver, if none is indicated the program will 
  scan the current directory to find the solver indicated by the -s and will raise an Exception if it does not find it.  
  Options :
  - --help prints this message.  
  - --problems prints the lists of available computational problems.  
  - --formats prints the list of accepted file formats.  
  - --informations for informations about the version and the author.  

### The GUI : PAFtoAFGUI.py

To use the GUI make sure that the file PAFtoAF.py and the file PAFtoAFGUI.py are in the same folder.  
Then you have 2 ways of doing it :  
  - Using a terminal (or command Prompt) and typing python (or python3, depending on you installation) followed by PAFtoAFGUI.py as :  
  python PAFtoAFGUI.py  
  - Using an IDE (such as the IDLE python, Spyder, Visual, etc...) opening the file in the IDE and then running it.  
#### The help button  
A 'Help' button (at the top) is here if you need more information on how it works. 
#### The formats button 
There is also a 'Formats' button next to the 'Help' button to have a better understanding of the accepted formats.  
#### The problems button
The 'Problems' button next to it is here to see about the available tasks and their meanings.  
#### The save button  
The 'save' button is the last on the option buttons line and allows you to save the parameters you entered in the GUI as the corresponding command line in a text file. 
#### The show graph checkbox  
The checkbox  under the left text area, allows you to see the graph representing the PAF (if no reduction is applied yet) or the resulting AF.  
The problem with the API used (networkx) is that edges are considered as lines between 2 nodes.  
So self loop are considered as a line between a point and itself, in other world, nothing.  
That is why if your graph contains a self attack it won't be shown on the graph.  
I you find a way to change that, feel free to implement it and maybe send me an email with the solution you have found.   
#### The reload button  
The 'reload' button is over the left text area. It is here if you want to modify the PAF in the text area (or write a new PAF on the fly),  
after doing so, hit the button to let the software know that this is what it needs to read and not the file you selected before.  
The realoading_text file will be located in the temp directory, explained a bit further.
#### The download button  
This button is over the right text area and allows you to save the AF (resulting from the reduction) into a new file.  
#### The temp directory  
When you start the GUI a directory is created, in the current directory, called 'temp'.  
This directory will contain 2 files called reload_text.ptgf and reload_text.papx.  
These files are used if the button reload is clicked :  
the text in the text area will be read and if it is in one of the accepted format it will be written in the according file.  
Also in the temp directory will be stored a file per reduction you do and a file containing the graph if you check the 'show the graph' box.  
Please refrain from withdrawing a file from this directory.  
You can copy files but removing/deleting one may lead to an error or, in the worst case, a crash.  

### Bugs  
To file bugs reports, or feature requests, please send an email to <eyal.cohen@etu.u-paris.fr>.  

## Licence  
Copyright (c) 2021 Cohen Eyal, LIPADE  
  
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
