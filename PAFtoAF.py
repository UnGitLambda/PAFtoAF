# -*- coding: utf-8 -*-
"""
Created in 07/2021

@author: Eyal Cohen
"""

from sys import argv, version_info
from _io import TextIOWrapper
from os import DirEntry
import os
import copy
import platform
import pathlib as pl

assert version_info >= (3,0), "PAFtoAF runs under python 3 or more. To use it please get you version of python up to date."

class UnsupportedFormatException(Exception):
    name = "Unsupported Format Exception"
    pass

class FormatException(Exception):
    name = "Format Exception"
    pass

class FormatSyntaxException(Exception):
    name = "Format Syntax Excpetion"
    pass

class PreferenceException(Exception):
    name = "Preferenec Exception"
    pass

class ParsingException(Exception):
    name = "Parsing Exception"
    pass

class CommandLineException(Exception):
    name = "Command Line Exception"
    pass

class FindingSolverException(Exception):
    name = "Finding Solver Exception"
    pass

class UnsupportedOSException(Exception):
    name = "Unsupported OS Exception"
    pass

#We define these here to share them between functions
args = set()
attacksFrom = dict()
preferences = dict()

def print_help(ret = False):
    """
    Invoked when the user asks for help with the [--help] prameter
    """
    s = ("-f <file> -fo <format> [-p <task>] [-r <reduction>] [-a <query>] [-out <filename(s)>] [-s <solvername>] [-sp <solverpath>]\n")
    s += ("\n<task> is the computational problem, use --problems to see the ones supported")
    s += ("\n<file> is the input, the preference-based argumentation framework")
    s += ("\n<format> file format for input PAF; for a list of available formats use option --formats")
    s += ("\n<reduction> is the reduction to use to get an AF from the input PAF, use --reductions to see the available reductions")
    s += ("\n<query> used for prblems DC and/or DS, it is the argument concerned by the problem")
    s += ("\n<filename(s)> is the output for the resulting AF to be printed on, if you want the output to be on the terminal use stdout as filename.")
    s += ("\nIf you wish to have multiple prints (for exemple one on the terminal and one on a file) state every file this way : [file1,file2,file3...]")
    s += ("\nThe names of the files must contain their format (Exemple : [stdout, file.tgf, file2.apx])")
    s += ("\n<solvername> is the name of the solver, if none is indicated, on linux mu-toksia will be chosen as default and on windows, jArgSemSAT will.")
    s += ("\n<solverpath> is the path from the root to acces the solver.") 
    s += ("\nIf none is entered the program will scan the current directory to find the solver mu-toksia and will raise an Exception if it does not find it.")
    s += ("\nOptions :")
    s += ("\n--help prints this message.")
    s += ("\n--problems prints the lists of available computational problems.")
    s += ("\n--formats prints the list of accepted file formats.")
    s += ("\n--reductions prints the available reductions for a PAF.")
    s += ("\n--informations for informations about the version and the author.")
    if ret:
        return(s)
    else:
        print(s)

def print_problems(ret = False):
    """
    Invoked when the user wishes to see the available prblems with the [--problems] parameter
    """
    s = ""
    for i in ["CO","PR","ST","SST","STG","GR","ID"]:
        s += "\n"
        for j in ["DC","DS","SE","CE", "EE"]:
            problem = "{}-{}".format(j,i)
            if problem == "CE-ID" or problem == "DC-ID" or problem == "EE-ID": #CE-ID = 1 so EE-ID = SE-ID and DC-ID = DS-ID so we only consider SE-ID and DS-ID
                continue
            else:
                s += "[" + problem+ "]" + (", ", "")[problem == "SE-ID"] #just to avoid putting a , after the last problem (SE-ID)
    if ret:
        return(s)
    else:
        print(s)

def print_formats(ret = False):
    form = ("Preference-based Trivial Graph Format [.ptgf]")
    form += ("\nOne argument per line, indicated by his name, followed by a #.\n Then the attacks are witten as follow : arg1 arg2, one attack per line also.")
    form += ("\nA second # indicates the beginning of the preferences' listing, they are written the same way attacks are.")
    form += ("\nHere is an exemple : \n1\n2\n3\n#\n1 2\n2 3\n2 1\n#\n1 2")
    form += ("\n\n")
    form += ("\nPreference-based ASPARTIX Format [.papx]")
    form += ("\nArguments are written as arg(1), attacks as att(1,2) and preferences as pref(1,2).")
    form += ("\nHere is an exemple :\narg(1)\narg(2)\narg(3)\natt(1,2)\natt(2,3)\natt(2,1)\npref(1,2)")
    if ret:
        return(form)
    else:
        print(form)

def print_reductions(ret = False):
    redu = ("Reductions are a way to 'extract' an AF from a PAF.")
    redu += ("\nWhen applying a reduction to a PAF we focus on a peculiar type of attack :")
    redu += ("\nThe attacks we focus on are called 'critical attacks', they correspond to A attacks B but B is prefered over A.")
    redu += ("\nThere are 4 kinds of reduction :")
    redu += ("\nThe first one nullifies critical attacks.")
    redu += ("\nThe second reduction reverses critical attacks.")
    redu += ("\nThe third option is to keep a critical attack if and only if the opposite attack does not exist.")
    redu += ("\nThe fourth one creates a symetrical attack to critical ones.")
    redu += ("\n\n")
    redu += ("\nAs an exemple lets take : \natt(1,2)\npref(2,1)")
    redu += ("\nR1 : no attack remains in the resulting AF.")
    redu += ("\nR2 : att(2,1) is in the resulting AF.")
    redu += ("\nR3 : att(1,2) is kept in the AF.")
    redu += ("\nR4 : att(1,2) and att(2,1) are in the resulting AF.\n")
    if ret:
        return(redu)
    else:
        print(redu)

def print_informations(ret = False):
    info = "PAFtoAF version 1.0\nAuthor : Eyal Cohen"
    if ret:
        return(info)
    else:
        print(info)

switcher_options = {
    "-help" : print_help,
    "--help" : print_help,
    "-problems" : print_problems,
    "--problems" : print_problems,
    "-formats" : print_formats,
    "--formats" : print_formats,
    "-reductions" : print_reductions,
    "--reductions" : print_reductions,
    "-informations" : print_informations,
    "--informations" : print_informations
    }

def outputs():
    """
    Method that uses the sys.argv list to find the indicated outputs in it (thanks to the -out <filename(s)>).
    It then reconstructs the list in a string format and parses it thanks to the parse_list method below.
    None --> List  (None because it reads the command line and does not need any other input)
    """
    outputs = ''
    if "-out" in argv:
        if "[" in argv[argv.index("-out")+1]:
            i=1
            while("]" not in outputs):
                outputs += argv[argv.index("-out")+i]
                i += 1
            return(parse_list(outputs))
        else:
            return [argv[argv.index("-out")+1]]

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
    
    args.clear()
    attacksFrom.clear()
    preferences.clear()
    
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
    n_already = False
    while c != "":
        if c == "\n":
            if n_already:
                break
            n_already= True
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
    n_already = False
    while c != "":
        if c == "\n":
            if n_already:
                break
            n_already = True
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
    
    arg1 = c[:c.find(" ")]
    arg2 = c[c.find(" ")+1:] if c[-1]!="\n" else c[c.find(" ")+1:-1]
    if arg2 == "":
        raise FormatSyntaxException("Single argument found while parsing preferences : {}.".format(arg1))
    elif arg1 in preferences[arg2] or arg1 == arg2:
        print(c, "pref : ", (arg1,arg2))
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
    elif arg1 in preferences[arg2] or arg1 == arg2:
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
    
    file.write("arg({}).\n".format(arg))

def write_att_apx(file, arg1, arg2):
    """
    Invoked to write down a sinle attack on a file to the apx format.
    dict*TextIOWrapper --> None
    """
    
    assert type(file) is TextIOWrapper, "The first argument of this method must be the file we will write on (opened by the open method). (type TextIOWrapper)"
    assert type(arg1) is str, "The second argument of this method must be the first argument in the attack to write down. (type String)"
    assert type(arg2) is str, "The third argument of this method must be the second argument in the attack to write down. (type String)"
    
    file.write("att({},{}).\n".format(arg1,arg2))

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
            print("".join([i,""]))
        print("#")
        for j in newAttacksFrom.keys():
            for k in newAttacksFrom[j]:
                print(''.join([j," ",k]))
    elif fileformat == "apx":
        for i in args:
            print("arg({})".format(i))
        for j in newAttacksFrom.keys():
            for k in newAttacksFrom[j]:
                print("att({},{})".format(j,k))
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
    
    output = ''
    try:
        output = os.popen(solverExecutableCommand(solver,path, scan, solverArgv)).readlines()
    except Exception as e:
        print(str(e))
        raise FindingSolverException("Unable to execute the solver.")
    if output == '':
        raise FindingSolverException("Unable to find the solver.")
    return(output)

def solverExecutableCommand(solver, path = ".", scan = False, Argv = argv):
    """
    Method used to create the command line to execute the solver.
    str*str*bool*list --> str
    """
    
    assert type(solver) is str, "The first argument of this method must be the name of the solver. (type String)"
    assert type(path) is str, "The second argument of this method must be the path to the solver or to the directory containing the solver (if the solver's name is indicated). (type String, default = '.')"
    assert type(scan) is bool, "The thirst argument to this method must be a boolean indicating if we must (or not) scan the directory indicated by the path (if the path is a directory indeed). (type Boolean, default = false)"
    assert type(Argv) is list, "The fourth argument of this method are the arguments to pass on to the solver in the command line. (type List)"
    
    if platform.system() == "Windows":
        Path = pl.PureWindowsPath(path)
    elif platform.system() in ["Linux", "Darwin"]:
        Path = pl.PurePosixPath(path)
    else:
        print("Your OS is not supported yet, we only work on Linux, macOS or Windows.\nSorry for the incunveniance.\nIf you want to use our application nonetheless, pleas specify a solver and/or a path.")
        raise UnsupportedOSException("Your OS is not supported yet, we only work on Linux, macOS or Windows.\nIf you want to use our application nonetheless, pleas specify a solver and/or a path.")
    paramSolver = commandLine(Argv)
    if (Path == pl.Path(".")) or scan:
        if not os.path.isdir(Path):
            execCommand = solverExecutableCommand(solver, Path, False, Argv)
        else:
            for file in os.scandir():
                if solverName(file, solver):
                    execCommand = file.path + ' ' + commandLine(Argv)
                    if solver.endswith(".jar"):
                        execCommand = "java -jar " + execCommand
                    elif solver.endswith(".py"):
                        execCommand = "python3 " + execCommand
                    else :
                        execCommand = "./" + execCommand
                    break
    elif Path is not None:
        if os.path.isdir(Path):
            try :
                os.chdir(Path)
            except:
                raise FindingSolverException("Something in the path is not right, unable to access a directory.")
            execCommand = solverExecutableCommand(solver, solver, False, Argv)
        else:
            execCommand = Path.__str__() + ' ' + paramSolver
            if Path.__str__().endswith(".jar"):
                execCommand = "java -jar " + execCommand
            elif Path.__str__().endswith(".py"):
                execCommand = "python3 " + execCommand
            else :
                execCommand = "./" + execCommand
    return(execCommand)

def solverName(file, solver):
    """
    Method checking if a file has the same name as the solver, it is basicaly just a boolean.
    DirEntry * str --> bool
    """
    
    assert type(file) is DirEntry, "The first argument in this method is the file we want to compare to the solver. (type DirEntry)"
    assert type(solver) is str, "The second argument of this method must be the name of the solver. (type String)"
    if platform.system() == "Windows":
        answer = os.fsdecode(file).replace(".\\","") == solver or os.fsdecode(file).replace(".\\","") == ''.join([solver,".exe"]) or ''.join([os.fsdecode(file).replace(".\\",""),".exe"]) == solver or os.fsdecode(file) == solver or os.fsdecode(file).replace(".jar", "") == solver or os.fsdecode(".py", "") == solver
    else:
        answer = os.fsdecode(file).replace("./","") == solver or os.fsdecode(file).replace("./","") == ''.join([solver,".exe"]) or ''.join([os.fsdecode(file).replace("./",""),".exe"]) == solver or os.fsdecode(file) == solver or os.fsdecode(file).replace(".jar", "") == solver or os.fsdecode(file).replace(".py", "") == solver
    return(answer)

def commandLine(Argv):
    """
    Method converting a list of arguments/parameter in a command line format (to include in the execution of a program for exemple).
    list --> str
    """
    
    assert type(Argv) is list, "The argument of this method are the arguments to convert in the command line format. (type List)"
    
    commandLine = ''
    for i in Argv[1::]:
        commandLine += i+" "
    return(commandLine)

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

def fileName():
    if "-f" in argv:
        return argv[argv.index("-f")+1]
    else:
        raise CommandLineException("Please specify the input file, using the -f parameter, in the command line.")

def fileformat():
    if "-fo" in argv:
        Format = argv[argv.index("-fo")+1]
        if Format not in ["papx","ptgf"]:
            raise UnsupportedFormatException("Unsupported format {}. Supported formats are papx and ptgf.\nUse --formats for more information.".format(Format))
        else:
            return Format
    else:
        print("Please specify the file's format, using the -fo parameter, in the command line.")
        print("Here are the available formats :")
        print_formats()
        raise CommandLineException("Please specify the file's format, using the -fo parameter, in the command line.")

switcher_reductions = {
        "1" : reduction1,
        "2" : reduction2,
        "3" : reduction3,
        "4" : reduction4
        }

def applyReduction(file, fileformat, solverArgv):
    if "-r" in argv:
        reduction = argv[argv.index("-r")+1]
        toPaf(file, fileformat)
        solverArgv.remove("-r")
        solverArgv.remove(reduction)
        outs = []
        if "-out" in argv:
            outs = outputs()
            i = argv.index("-out")
            if "[" in argv[argv.index("-out")+1]:
                while "]" not in argv[i]:
                    solverArgv.remove(argv[i])
                    i+=1
                solverArgv.remove(argv[i])
            else:
                solverArgv.remove("-out")
                solverArgv.remove(argv[argv.index("-out")+1])
        if "-p" in argv:
            outs.append("Reduction{}-AF-tmp.{}".format(reduction, 'tgf'if fileformat == "ptgf" else "apx"))
        switcher_reductions.get(argv[argv.index("-r")+1])(outs, 'tgf'if fileformat == "ptgf" else "apx")
    else:
        reduction = '0'
    return reduction

def Solver(solverArgv):
    if "-s" in argv:
        solver = argv[argv.index("-s")+1]
        solverArgv.remove("-s")
        solverArgv.remove(solver)
    else:
        if platform.system() in ["Linux", "Darwin"]:
            solver = "mu-toksia"
        elif platform.system() == "Windows":
            solver = "jArgSemSAT.jar"
        else :
            print("Your OS is not supported yet, we only work on Linux, macOS or Windows.\nSorry for the incunveniance.\nIf you want to use our application nonetheless, pleas specify a solver and/or a path.")
            raise UnsupportedOSException("Your OS is not supported yet, we only work on Linux, macOS or Windows.\nIf you want to use our application nonetheless, pleas specify a solver and/or a path.")
    return solver

def solverPath_scan(solverArgv):
    if "-sp" in argv:
        path = argv[argv.index("-sp")+1]
        solverArgv.remove("-sp")
        solverArgv.remove(path)
        scan = False
    else:
        path = "."
        scan = True
    return(path,scan)

def doTask(file = 'Reduction0-AF-tmp.tgf', fileformat = 'tgf', reduction = '0', solverArgv = argv, programPath = "."):
    if "-p" in argv:
        solver = Solver(solverArgv)
        path,scan = solverPath_scan(solverArgv)
        try:
            solverArgv[solverArgv.index("-f")+1] = "Reduction{}-AF-tmp.{}".format(reduction, 'tgf' if fileformat =="ptgf" else "apx")
            sysOutput = solverOutput(solver, path, scan, solverArgv)
        except(FindingSolverException):
            print("Your solver was to hard to find, please provide it's name with the -s parameter and it's path thanks to the-sp parameter.\n Also please be sure that the solver is at the right place.")
            raise FindingSolverException("Your solver was to hard to find.")
        except(RecursionError):
            print("Your solver is to hard to find, the recursion error was reached.")
            raise RecursionError("Your solver was to hard to find.")
        finally:
            os.chdir(programPath)
            os.remove("Reduction{}-AF-tmp.{}".format(reduction, 'tgf' if fileformat =="ptgf" else "apx"))
            return(sysOutput)

def main(ARGC, ARGV, ret = False):
    global argv
    global argc
    argv = copy.deepcopy(ARGV)
    argc = ARGC
    if argc == 1:
        if ret:
            return(print_informations(ret))
        print_informations(ret)

    elif argc == 2:
        if ret:
            return(switcher_options.get(argv[1])(ret))
        switcher_options.get(argv[1])(ret)

    else:
        solverArgv = argv.copy()
        programPath = pl.Path(os.getcwd())
        file = fileName()
        FileFormat = fileformat()
        solverArgv[argv.index("-fo")+1] = "tgf" if FileFormat == "ptgf" else "apx"
        reduction = applyReduction(file, FileFormat, solverArgv)
        sysOutput = doTask(file, FileFormat, reduction, solverArgv, programPath)
        if sysOutput is not None:
            if ret:
                return(sysOutput)
            else:
                for i in sysOutput:
                    print(i)

if __name__ == "__main__":
    main(len(argv), argv)