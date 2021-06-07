# -*- coding: utf-8 -*-
"""
Created on Mon May 31 2021

@author: Eyal Cohen
"""

from sys import argv
from _io import TextIOWrapper
import os
import copy
import platform
import pathlib as pl

class UnsupportedFormatException(Exception):
    pass

class FormatException(Exception):
    pass

class FormatSyntaxException(Exception):
    pass

class PreferenceException(Exception):
    pass

class ParsingException(Exception):
    pass

class CommandLineException(Exception):
    pass

class FindingSolverException(Exception):
    pass

class UnsupportedOSException(Exception):
    pass

#We define these here to share them between functions
args = set()
attacksFrom = dict()
preferences = dict()
   
def print_help():
    """
    Invoked when the user asks for help with the [--help] prameter
    """
    print("-p <task> -f <file> -fo <format> [-r <reduction>] [-a <query>] [-out <filename(s)>] [-s <solvername>] [-sp <solverpath>]\n")
    print("<task> is the computational problem, use --problems to see the ones supported")
    print("<file> is the input, the preference-based argumentation framework")
    print("<format> file format for input PAF; for a list of available formats use option --formats")
    print("<reduction> is the reduction to use to get an AF from the input PAF, use --reductions to see the available reductions")
    print("<query> used for prblems DC and/or DS, it is the argument concerned by the problem")
    print("<filename> is the output for the resulting AF to be printed on, if you want the output to be on the terminal use stdout as filename.")
    print("If you wish to have multiple prints (for exemple one on the terminal and one on a file) state every file this way : [file1,file2,file3...]")
    print("The names of the files must contain their format (Exemple : [stdout, file.tgf, file2.apx])")
    print("<solvername> is the name of the solver, if none is indicated, on linux mu-toksia will be chosen as default and on windows, jArgSemSAT will.")
    print("<solverpath> is the path from the root to acces the solver.") 
    print("If none is entered the program will scan the current directory to find the solver mu-toksia and will raise an Exception if it does not find it.")
    print("Options :")
    print("--help prints this message")
    print("--problems prints the lists of available computational problems")
    print("--formats prints the list of accepted file formats")
    print("--reductions prints the available reductions for a PAF")
    
def print_problems():
    """
    Invoked when the user wishes to see the available prblems with the [--problems] parameter
    """
    for i in ["CO","PR","ST","SST","STG","GR","ID"]:
        for j in ["DC","DS","SE","CE", "EE"]:
            problem = "{}-{}".format(j,i)
            if problem == "CE-ID" or problem == "DC-ID" or problem == "EE-ID": #CE-ID = 1 so EE-ID = SE-ID and DC-ID = DS-ID so we only consider SE-ID and DS-ID
                continue
            else:
                print("[",problem,"]", sep = '', end = (", ", "")[problem == "SE-ID"]) #just to avoid putting a , after the last problem (SE-ID)

def print_formats():
    print("Preference-based Trivial Graph Format [.ptgf]")
    print("One argument per line, indicated by his name, followed by a #.\n Then the attacks are witten as follow : arg1 arg2, one attack per line also.")
    print("A second # indicates the beginning of the preferences' listing, they are written the same way attacks are.")
    print("Here is an exemple : \n1\n2\n3\n#\n1 2\n2 3\n2 1\n#\n1 2")
    print("\n")
    print("Preference-based ASPARTIX Format [.papx]")
    print("Arguments are written as arg(1), attacks as att(1,2) and preferences as pref(1,2).")
    print("Here is an exemple :\narg(1)\narg(2)\narg(3)\natt(1,2)\natt(2,3)\natt(2,1)\npref(1,2)")
    
def print_reductions():
    print("Reductions are a way to 'extract' an AF from a PAF.")
    print("When applying a reduction to a PAF we focus on a peculiar type of attack :")
    print("The attacks we focus on are called 'critical attacks', they correspond to A attacks B but B is prefered over A.")
    print("There are 4 kinds of reduction :")
    print("The first one nullifies critical attacks.")
    print("The second reduction reverses critical attacks.")
    print("The third option is to keep a critical attack if and only if the opposite attack does not exist.")
    print("The fourth one creates a symetrical attack to critical ones.")
    print("\n")
    print("As an exemple lets take : \natt(1,2)\npref(2,1)")
    print("R1 : no attack remains in the resulting AF.")
    print("R2 : att(2,1) is in the resulting AF.")
    print("R3 : att(1,2) is kept in the AF.")
    print("R4 : att(1,2) and att(2,1) are in the resulting AF.\n")

def print_informations():
    print("PAFtoAF version 1.0")
    print("Author : Eyal Cohen")

def outputs():
    """
    Method that uses the sys.argv list to find the indicated outputs in it (thanks to the -out <filename(s)>).
    It then reconstructs the list in a string format and parses it thanks to the parse_list method below.
    None --> List  (None because it reads the command line and does not need any other input)
    """
    outputs = ''
    if "-out" in argv:
        i=1
        while("]" not in outputs):
            outputs += argv[argv.index("-out")+i]
            i += 1
    return(parse_list(outputs))
            
def toPaf(inputFile, fileformat):
    """
    This function converts the file (input) into a Preference-based Argumentation Framework.
    Here the PAF is represented by one set and 3 dictionnaries:
        - the set contains the arguments
        - the first dictionnary contains the attacks from an argument a to another
        - the second one is filled with the opposite relation, it is used to go faster when searching 'who is attacking this argument'
        - the last one contains the preferences, the keys are the prefered arguments and the values are the one they are prefered over
    file --> set*dict*dict*dict
    """
    
    assert type(inputFile) is str, "The first argument of this method must be the name of the inputFile. (type String)"
    assert type(fileformat) is str, "The second argument of this method must be the extension of the inputFile. (type String)"
    
    try:
        file = open(inputFile, "r")
    except FileNotFoundError:
        print("Unable to open the file.")
        raise FileNotFoundError("Unable to find the file.")
    except(OSError, IOError):
        print("System error")
        raise
    if fileformat == "ptgf":
        parse_ptgf(file)
    elif fileformat ==  "papx":
        parse_papx(file)
    else:
        print("Unsupported format ", fileformat,", suported formats are : ")
        print_formats()
        raise UnsupportedFormatException("Unsuported format : ", fileformat)
    file.flush()
    file.close()

def parse_ptgf(file):
    """
    Parser allowing to extract a PAF from a file (opened using the open method) in the ptgf format.
    For the method to work you must have :
        -a global set called args, representing the arguments
        -a global dictionary called attacksFrom, where arg1 attacks arg2 is represented by arg2 in attacksFrom[arg1]
        -a global dictionary called prefernces, where arg1>arg2 is representedby arg2 in preferences[arg1]
    (global here is used to imply "global in front of this method")
    TextIoWrapper -> None (because it writes on the already existing set and dictionaries)
    """
    
    assert type(file) is TextIOWrapper, "The agument of this method must be a file, opened using the open function, on which this will parse a PAF in the ptgf format. (type TextIOWrapper)"
    
    c = file.readline()
    ct = 0
    while c != "":
        if c == "\n":
            continue
        elif c == "#\n":
            if ct<2:
                ct += 1
            else :
                print("Error parsing the file, more than two #")
                raise FormatSyntaxException(".ptgf format Exception, more than two #")
        elif(ct == 0):
            parse_argument_ptgf(c)
        elif ct == 1:
            parse_attack_ptgf(c)
        else:
            parse_preference_ptgf(c)
        c = file.readline()

def parse_papx(file):
    """
    Parser allowing to extract a PAF from a file (opened using the open method) in the papx format.
    For the method to work you must have :
        -a global set called args, representing the arguments
        -a global dictionary called attacksFrom, where arg1 attacks arg2 is represented by arg2 in attacksFrom[arg1]
        -a global dictionary called prefernces, where arg1>arg2 is representedby arg2 in preferences[arg1]
    (global here is used to imply "global in front of this method")
    TextIoWrapper -> None (because it writes on the already existing set and dictionaries)
    """
    
    assert type(file) is TextIOWrapper, "The agument of this method must be a file, opened using the open function, on which this will parse a PAF in the ptgf format. (type TextIOWrapper)"
    
    c = file.readline()
    while c != "":
        if c == "\n":
            continue
        elif c[:3:1] == "arg":
            parse_argument_papx(c)
        elif c[:3:1] == "att":
            parse_attack_papx(c)
        elif c[:4:1] == "pref":
            parse_preference_papx(c)
        else:
            raise FormatSyntaxException(".papx format Exception, unknown identifier")
        c = file.readline()

def parse_argument_ptgf(c):
    """
    Parser allowing to extract an argument from a string in the ptgf (or tgf) format.
    This method is invoked in parse_ptgf, and for it to work the condition stipulated in the latter must be respected.
    str-->None
    """
    
    assert type(c) is str, "The argument in this method must be a string containing an argument in the format ptgf (or tgf). (type String)"
    
    arg = c[:c.find("\n")]
    args.add(arg)
    attacksFrom[arg] = set()
    preferences[arg] = set()
    
def parse_argument_papx(c):
    """
    Parser allowing to extract an argument from a string in the papx (or apx) format.
    This method is invoked in parse_papx, and for it to work the condition stipulated in the latter must be respected.
    str-->None
    """
    
    assert type(c) is str, "The argument in this method must be a string containing an argument in the format papx (or apx). (type String)"
    
    arg = c[c.find("(")+1:c.find(")"):1]
    args.add(arg)
    attacksFrom[arg] = set()
    preferences[arg] = set()
    
def parse_attack_ptgf(c):
    """
    Parser allowing to extract an attack from a string in the ptgf (or tgf) format.
    This method is invoked in parse_ptgf, and for it to work the condition stipulated in the latter must be respected.
    str-->None
    """
    
    assert type(c) is str, "The argument in this method must be a string containing an argument in the format ptgf (or tgf). (type String)"
    
    arg1 = c[:c.find(" "):1]
    arg2 = c[c.find(" ")+1:c.find("\n"):1]
    if arg2 == "":
        raise FormatSyntaxException("Single argument found while parsing attacks : {}.".format(arg1))
    elif arg1 in args and arg2 in args:
        attacksFrom[arg1].add(arg2)
    else:
        print("Argument ", arg1 if arg2 in args else arg2, " is referenced in attacks but not defined.")
        raise FormatSyntaxException("Argument referenced before initialization")

def parse_attack_papx(c):
    """
    Parser allowing to extract an attack from a string in the papx (or apx) format.
    This method is invoked in parse_papx, and for it to work the condition stipulated in the latter must be respected.
    str-->None
    """
    
    assert type(c) is str, "The argument in this method must be a string containing an argument in the format papx (or apx). (type String)"
    
    arg1 = c[c.find("(")+1:c.find(","):1]
    arg2 = c[c.find(",")+1:c.find(")")]
    if arg1 == "" or arg2 == "":
        raise FormatSyntaxException("Single argument found while parsing attacks : att({},{}).".format(arg1,arg2))
    elif arg1 in args and arg2 in args:
        attacksFrom[arg1].add(arg2)
    else:
        print("Argument ", arg1 if arg2 in args else arg2, " is referenced in prefernces but not defined.")
        raise FormatSyntaxException("Argument referenced before initialization.")

def parse_preference_ptgf(c):
    """
    Parser allowing to extract a preference from a string in the ptgf (or tgf) format.
    This method is invoked in parse_ptgf, and for it to work the condition stipulated in the latter must be respected.
    str-->None
    """
    
    assert type(c) is str, "The argument in this method must be a string containing an argument in the format ptgf (or tgf). (type String)"
    
    arg1 = c[:c.find(" "):1]
    arg2 = c[c.find(" ")+1::1] if c[-1]!="\n" else c[c.find(" ")+1:-1:1]
    if arg2 == "":
        raise FormatSyntaxException("Single argument found while parsing preferences : {}.".format(arg1))
    elif arg1 in preferences[arg2]:
        print("Ambiguious preferences : ", arg1, " and ", arg2, " are mutually preferred over the other.")
        raise PreferenceException("Ambiguious preferences")
    elif arg1 in args and arg2 in args:
        preferences[arg1].add(arg2)
        for i in preferences[arg2]:
            preferences[arg1].add(i)
        for j in preferences.keys():
            if arg1 in preferences[j]:
                preferences[j].add(arg2)
    else:
        print("Argument ", arg1 if arg2 in args else arg2, " is referenced in prefernces but not defined.")
        raise FormatSyntaxException("Argument referenced before initialization.")

def parse_preference_papx(c):
    """
    Parser allowing to extract a perference from a string in the papx (or apx) format.
    This method is invoked in parse_papx, and for it to work the condition stipulated in the latter must be respected.
    str-->None
    """
    
    assert type(c) is str, "The argument in this method must be a string containing an argument in the format papx (or apx). (type String)"
    
    arg1 = c[c.find("(")+1:c.find(","):1]
    arg2 = c[c.find(",")+1:c.find(")")]
    if arg1 == "" or arg2 == "":
        raise FormatSyntaxException("Single argument found while parsing attacks : pref({},{}).".format(arg1,arg2))
    elif arg1 in preferences[arg2]:
        print("Ambiguious preferences : ", arg1, " and ", arg2, " are mutually preferred over the other.")
        raise PreferenceException("Ambiguious preferences")
    elif arg1 in args and arg2 in args:
        preferences[arg1].add(arg2)
        for i in preferences[arg2]:
            preferences[arg1].add(i)
        for j in preferences.keys():
            if arg1 in preferences[j]:
                preferences[j].add(arg2)
    else:
        print("Argument ", arg1 if arg2 in args else arg2, " is referenced in preferences but not defined.")
        raise FormatSyntaxException("Argument referenced before initialization.")
                    
def toFile(newAttacksFrom, outputFile = "AF", fileformat = "tgf"):
    """
    Function writting the AF (after the reductions) in a file.
    set*dict*str*str --> None
    """
   
    assert type(args) is set, "The first argument of this method must be the set of arguments. (type Set)"
    assert type(attacksFrom) is dict, "The second argument of this method must be the dictionary having for keys the arguments attacking and for values the arguments attacked. (type Dictionary)"
    assert type(outputFile) is str, "The third argument of this method must be the name of the outputFile. (type String)"
    assert type(fileformat) is str, "The last/fourth argument of this method method must be the extension of the outputFile. (type Dictionary)"
    
    file = open(outputFile , "w+")
    if fileformat == "tgf":
        write_tgf(newAttacksFrom, file)
    elif fileformat == "apx":
        write_apx(newAttacksFrom, file)
    else:
        print("Unsupported format ", fileformat,", suported formats are : ")
        print_formats()
        raise UnsupportedFormatException("Unsuported format : ", fileformat)
    file.flush()
    file.close()

def write_tgf(newAttacksFrom, file):
    """
    Invoked to write down an AF on a file to the tgf format.
    dict*TextIOWrapper --> file
    """
    
    assert type(attacksFrom) is dict, "The first argument of this method must be the dictionary having for keys the arguments attacking and for values the arguments attacked. (type Dictionary)"
    assert type(file) is TextIOWrapper, "The second argument of this method must be the file we will write on (opened by the open method). (type TextIOWrapper)"
     
    for i in args:
        write_arg_tgf(file,i)
    file.write("#\n")
    for j in newAttacksFrom.keys():
        for k in newAttacksFrom[j]:
            write_att_tgf(file,j,k)

def write_arg_tgf(file, arg):
    """
    Invoked to write down a sinle argument on a file to the tgf format.
    dict*TextIOWrapper --> None
    """
    assert type(file) is TextIOWrapper, "The first argument of this method must be the file we will write on (opened by the open method). (type TextIOWrapper)"
    assert type(arg) is str, "The second argument of this method must be the argument to write down. (type String)"
    
    file.write("".join([arg,"\n"]))

def write_att_tgf(file, arg1, arg2):
    """
    Invoked to write down a sinle attack on a file to the tgf format.
    dict*TextIOWrapper --> None
    """
    
    assert type(file) is TextIOWrapper, "The first argument of this method must be the file we will write on (opened by the open method). (type TextIOWrapper)"
    assert type(arg1) is str, "The second argument of this method must be the first argument in the attack to write down. (type String)"
    assert type(arg2) is str, "The third argument of this method must be the second argument in the attack to write down. (type String)"
    
    file.write(''.join([arg1," ",arg2,"\n"]))

def write_apx(newAttacksFrom, file):
    """
    Invoked to write down an AF on a file to the apx format.
    dict*TextIOWrapper --> file
    """
    
    assert type(attacksFrom) is dict, "The first argument of this method must be the dictionary having for keys the arguments attacking and for values the arguments attacked. (type Dictionary)"
    assert type(file) is TextIOWrapper, "The second argument of this method must be the file we will write on (opened by the open method). (type TextIOWrapper)"
    
    for i in args:
        write_arg_apx(file, i)
    for j in newAttacksFrom.keys():
        for k in newAttacksFrom[j]:
            write_att_apx(file,j,k)

def write_arg_apx(file, arg):
    """
    Invoked to write down a sinle argument on a file to the apx format.
    dict*TextIOWrapper --> None
    """
    
    assert type(file) is TextIOWrapper, "The first argument of this method must be the file we will write on (opened by the open method). (type TextIOWrapper)"
    assert type(arg) is str, "The second argument of this method must be the argument to write down. (type String)"
    
    file.write("arg({})\n".format(arg))

def write_att_apx(file, arg1, arg2):
    """
    Invoked to write down a sinle attack on a file to the apx format.
    dict*TextIOWrapper --> None
    """
    
    assert type(file) is TextIOWrapper, "The first argument of this method must be the file we will write on (opened by the open method). (type TextIOWrapper)"
    assert type(arg1) is str, "The second argument of this method must be the first argument in the attack to write down. (type String)"
    assert type(arg2) is str, "The third argument of this method must be the second argument in the attack to write down. (type String)"
    
    file.write("att({},{})\n".format(arg1,arg2))

def print_AF(newAttacksFrom, fileformat):
    """
    Invoked when the user uses stdout as a wanted output.
    This method prints the AF resulting from the reductions asked on the terminal.
    dict*str --> None
    """
    
    assert type(newAttacksFrom) is dict, "The first argument ofthis method must be a dictionary containing the attacks in the AF, needed to be printed. (type Dict)"
    assert type(fileformat) is str, "The second argument of this method method must be the extension of the outputFile. (type Dictionary)"
    
    if fileformat == "tgf":
        for i in args:
            print("".join([i,"\n"]))
        print("#\n")
        for j in newAttacksFrom.keys():
            for k in newAttacksFrom[j]:
                print(''.join([j," ",k,"\n"]))
    elif fileformat == "apx":
        for i in args:
            print("arg({})\n".format(i))
        for j in newAttacksFrom.keys():
            for k in newAttacksFrom[j]:
                print("att({},{})\n".format(j,k))
    else:
        print("Unsupported format ", fileformat,", suported formats are : ")
        print_formats()
        raise UnsupportedFormatException("Unsuported format : ", fileformat)

def reduction1(outs = ["Reduction1-AF.tgf"], fileformat = "tgf"):
    """
    Function applying the first reduction rule to the PAD and then creating a file containing the resulting AF in the selected format.
    dict*dict*dict*str --> file
    """
    
    assert type(outs) is list, "The first argument of this method must be the list of every file the resulting AF is to be written on. (type List)"
    assert type(fileformat) is str, "The second argument of this method must be the format the resulting file (containing the AF) will be. (type String)"
    
    copyAttacksFrom = copy.deepcopy(attacksFrom)
    
    for arg in attacksFrom.keys():
        for j in attacksFrom[arg]:
            if arg in preferences[j]:
                copyAttacksFrom[arg].remove(j)
                
    for output in outs:
        if output == "stdout":
            print_AF(copyAttacksFrom, fileformat)
            continue
        toFile(copyAttacksFrom, output, fileformat)

def reduction2(outs = ["Reduction2-AF.tgf"], fileformat = "tgf"):
    """
    Function applying the second reduction rule to the PAD and then creating a file containing the resulting AF in the selected format.
    dict*dict*dict*str --> file
    """
    
    assert type(outs) is list, "The first argument of this method must be the list of every file the resulting AF is to be written on. (type List)"
    assert type(fileformat) is str, "The second argument of this method must be the format the resulting file (containing the AF) will be. (type String)"
    
    copyAttacksFrom = copy.deepcopy(attacksFrom)
    
    for arg in attacksFrom.keys():
        for j in attacksFrom[arg]:
            if arg in preferences[j]:
                copyAttacksFrom[arg].remove(j)
                copyAttacksFrom[j].add(arg)
                
    for output in outs:
        if output == "stdout":
            print_AF(copyAttacksFrom, fileformat)
            continue
        toFile(copyAttacksFrom, output, fileformat)
    
def reduction3(outs = ["Reduction3-AF.tgf"], fileformat = "tgf"):
    """
    Function applying the third reduction rule to the PAD and then creating a file containing the resulting AF in the selected format.
    dict*dict*dict*str --> file
    """
    
    assert type(outs) is list, "The first argument of this method must be the list of every file the resulting AF is to be written on. (type List)"
    assert type(fileformat) is str, "The second argument of this method must be the format the resulting file (containing the AF) will be. (type String)"
    
    copyAttacksFrom = copy.deepcopy(attacksFrom)
    
    for arg in attacksFrom.keys():
        for j in attacksFrom[arg]:
            if arg in preferences[j] and arg in attacksFrom[j]:
                copyAttacksFrom[arg].remove(j)
                
    for output in outs:
        if output == "stdout":
            print_AF(copyAttacksFrom, fileformat)
            continue
        toFile(copyAttacksFrom, output, fileformat)
    
def reduction4(outs = ["Reduction4-AF.tgf"], fileformat = "tgf"):
    """
    Function applying the fourth reduction rule to the PAD and then creating a file containing the resulting AF in the selected format.
    dict*dict*dict*str --> file
    """
    
    assert type(outs) is list, "The first argument of this method must be the list of every file the resulting AF is to be written on. (type List)"
    assert type(fileformat) is str, "The second argument of this method must be the format the resulting file (containing the AF) will be. (type String)"
    
    copyAttacksFrom = copy.deepcopy(attacksFrom)
    
    for arg in attacksFrom.keys():
        for j in attacksFrom[arg]:
            if arg in preferences[j]:
                copyAttacksFrom[j].add(arg)
                
    for output in outs:
        if output == "stdout":
            print_AF(copyAttacksFrom, fileformat)
            continue
        toFile(copyAttacksFrom, output, fileformat)
    
def solverOutput(solver, path = ".", scan = False, solverArgv = argv):
    """
    Invoked when the -p parameter is used.
    The script then looks for the solver and executes it.
    This method does this part and then return a list of strings, containing the lines composing the output of the solver.
    str*str*bool-->str*
    """
    
    assert type(solver) is str, "The first argument of this method must be the name of the solver. (type String)"
    assert type(path) is str, "The second argument of this method must be the path to the solver or to the directory containing the solver (if the solver's name is indicated). (type String, default = '.')"
    assert type(scan) is bool, "The thirst argument to this method must be a boolean indicating if we must (or not) scan the directory indicated by the path (if the path is a directory indeed). (type Boolean, default = false)"
    assert type(solverArgv) is list, "The fourth argument of this method are the arguments to pass on to the solver in the command line. (type List)"
    
    Path = pl.PureWindowsPath(path)
    output = ''
    commandLine = ''
    for i in solverArgv[1::]:
        commandLine += i+" "
    if (Path == ".") or scan:
        scan = True
        if not os.path.isdir(Path):
            output = solverOutput(solver, Path, False, solverArgv)
        else:
            for file in os.scandir():
                if os.fsdecode(file).replace(".\\","") == solver or os.fsdecode(file).replace(".\\","") == ''.join([solver,".exe"]) or ''.join([os.fsdecode(file).replace(".\\",""),".exe"]) == solver:
                    try:
                        output = os.popen(file.path + ' ' + commandLine).readlines()
                    except:
                        raise FindingSolverException("Unable to find the solver.")
    elif(Path is not None):
        if os.path.isdir(Path):
            try :
                os.chdir(Path)
                dirPath = Path[:Path.find(solver)+1]
                Path = Path[len(dirPath)::]
            except:
                raise FindingSolverException("Something in the path is not right, unable to access a directory.")
            output = solverOutput(solver, solver, False, solverArgv)
        else :
            dirPath = Path.parent
            try :
                os.chdir(dirPath)
            except:
                raise FindingSolverException("Something in the path is not right, unable to access a directory.")
            output = os.popen(Path.__str__() + ' ' + commandLine).readlines()
    if output=='' :
        raise FindingSolverException("Unable to find the solver.")
    return(output)
     
        
def parse_list(string):
    """
    Parser allowing to extract the first appearing list in a String.
    If there is no list in the string, the return will be an empty list.
    The elements of the list will be strings, stripped of the spaces, tabs and charriots.
    str --> list
    """
    
    assert type(string) is str, "This method parses a string and returns the first list it founds inside of it.\nHenceforth the argument must be a string to parse. (type String)"
    
    start = False
    elemList = False #if an element of the list to parse is a list (in a string format)
    out = []
    arg = ''
    for i in string:
        if i == "[" and not start:
            start = True
        elif i == "[":
            elemList = True
        elif i == "]" and start:
            if elemList:
                elemList = False
            else:
                out.append(arg)
                arg = ''
                start = False
                break
        elif i == ",":
           if not elemList: 
                out.append(arg)
                arg = ''
        elif start:
            arg += i
    if start:
        raise ParsingException("Never ending list to parse.")
    return out
            
#We try to simulate a switch case function using dictionaries.

switcher_options = {
        "--help" : print_help,
        "--problems" : print_problems,
        "--formats" : print_formats,
        "--reductions" : print_reductions,
        "--informations" : print_informations
        }

switcher_reductions = {
        "1" : reduction1,
        "2" : reduction2,
        "3" : reduction3,
        "4" : reduction4
        }

if len(argv) == 1:
    print_informations()

elif len(argv) == 2:
    switcher_options.get(argv[1])()

else:
    solverArgv = argv.copy()
    if "-f" in argv:
        file = argv[argv.index("-f")+1]
    else:
        raise CommandLineException("Please specify the input file, using the -f parameter, in the command line.")
    if "-fo" in argv:
        fileformat = argv[argv.index("-fo")+1]
        if fileformat not in ["papx","ptgf"]:
            raise UnsupportedFormatException("Unsupported format {}. Supported formats are papx and ptgf.\nUse --formats for more information.".format(fileformat))
        solverArgv[argv.index("-fo")+1] = "tgf" if fileformat == "ptgf" else "apx"
    else:
        print("Please specify the file's format, using the -fo parameter, in the command line.")
        print("Here are the available formats :")
        print_formats()
        raise CommandLineException("Please specify the file's format, using the -fo parameter, in the command line.")
    if "-r" in argv:
        reduction = argv[argv.index("-r")+1]
        toPaf(file, fileformat)
        solverArgv.remove("-r")
        solverArgv.remove(reduction)
        outs = []
        if "-out" in argv:
            outs = outputs()
            i = argv.index("-out")
            while "]" not in argv[i]:
                solverArgv.remove(argv[i])
                i+=1
            solverArgv.remove(argv[i])
        if "-p" in argv:
            task = argv[argv.index("-p")+1]
            outs.append("Reduction{}-AF-tmp.{}".format(reduction, 'tgf'if fileformat == "ptgf" else "apx"))
        switcher_reductions.get(argv[argv.index("-r")+1])(outs, 'tgf'if fileformat == "ptgf" else "apx")
    if "-p" in argv:
        if "-s" in argv:
            solver = argv[argv.index("-s")+1]
            solverArgv.remove("-s")
            solverArgv.remove(solver)
        else:
            if platform.system() in ["Linux", "Darwin"]:
                solver = "mu-toksia.exe"
            elif platform.system() == "Windows":
                solver = "jArgSemSAT.java"
            else :
                print("Your OS is not supported yet, we only work on Linux, macOS or Windows.\nSorry for the incunveniance.")
                raise UnsupportedOSException("Your OS is not supported yet, we only work on Linux, macOS or Windows.")
        if "-sp" in argv:
            path = argv[argv.index("-sp")+1]
            solverArgv.remove("-sp")
            solverArgv.remove(path)
            scan = False
        else:
            path = "."
            scan = True
        try:
            solverArgv[solverArgv.index("-f")+1] = "Reduction{}-AF-tmp.{}".format(reduction, 'tgf' if fileformat =="ptgf" else "apx")
            sysOutput = solverOutput(solver, path, scan, solverArgv)
            for i in sysOutput:
                print(i)
        except(FindingSolverException):
            print("Your solver was to hard to find, please provide it's name with the -s parameter and it's path thanks to the-sp parameter.\n Also please be sure that the solver is at the right place.")
            raise FindingSolverException("Your solver was to hard to find.")
        except(RecursionError):
            print("Your solver is to hard to find, the recursion error was reached.")
            raise RecursionError("Your solver was to hard to find.")
        finally:
            os.remove("Reduction{}-AF-tmp.{}".format(reduction, 'tgf' if fileformat =="ptgf" else "apx"))
            
        #TODO try working on subdividing existing methods in smaller and easier ones to improve the code readability, transportability and ability to be modified