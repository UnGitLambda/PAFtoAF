# -*- coding: utf-8 -*-
"""
Created on Fri May 28 2021

@author: Eyal Cohen
"""

from sys import argv
import os
from enum import Enum
import copy

class UnsupportedFormatException(Exception):
    pass

class FormatException(Exception):
    pass

class FormatSyntaxException(Exception):
    pass

class PreferenceException(Exception):
    pass

def print_help():
    """
    Invoked when the user asks for help with the [--help] prameter
    """
    print("-p <task> -f <file> -fo <format> -r <reduction> [-a <query>] [--print [-out <filename>] ] \n")
    print("<task> is the computational problem, use --problems to see the ones supported")
    print("<file> is the input, the preference-based argumentation framework")
    print("<format> file format for input PAF; for a list of available formats use option --formats")
    print("<reduction> is the reduction to use to get an AF from the input PAF, use --reductions to see the available reductions")
    print("<query> used for prblems DC and/or DS, it is the argument concerned by the problem")
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
                print("[",problem,"]", sep = '', end = (", \n", "")[problem == "SE-ID"]) #just to avoid putting a , after the last problem (SE-ID)
                if(i == "CO" or i == "PR" or i == "ST" or i == "GR"):
                    print("[", problem,"-D","]", sep = '', end = ", \n")

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
    
    args = set()
    attacksFrom = dict()
    preferences = dict()
    try:
        file = open(inputFile, "r")
    except(FileNotFoundError, OSError, IOError):
        print("Unable to open the file.")
        raise
    c = file.readline()
    if fileformat == "ptgf":
        ct = 0
        while c != "":
            if c == "\n":
                continue
            elif c == "#\n":
                if ct<2:
                    ct += 1
                else :
                    print("Error parsing the file, more than two #")
                    raise FormatException(".ptgf format Exception, more than two #")
            elif(ct == 0):
                arg = c[:c.find("\n")]
                args.add(arg)
                attacksFrom[arg] = set()
                preferences[arg] = set()
            elif ct == 1:
                arg1 = c[:c.find(" "):1]
                arg2 = c[c.find(" ")+1:c.find("\n"):1]
                if arg in args and arg2 in args:
                    attacksFrom[arg1].add(arg2)
                else:
                    print("Argument ", arg1 if arg2 in args else arg2, " is referenced in attacks but not defined.")
                    raise FormatSyntaxException("Argument referenced before initialization")
            else:
                arg1 = c[:c.find(" "):1]
                arg2 = c[c.find(" ")+1::1] if c[-1]!="\n" else c[c.find(" ")+1:-1:1]
                if arg1 in args and arg2 in args:
                    preferences[arg1].add(arg2)
                    for i in preferences[arg2]:
                        preferences[arg1].add(i)
                    for j in preferences.keys():
                        if arg1 in preferences[j]:
                            preferences[j].add(arg2)
                elif arg1 in preferences[arg2]:
                    print("Ambiguious preferences : ", arg1, " and ", arg2, " are mutually preferred over the other.")
                    raise PreferenceException("Ambiguious preferences")
                else:
                    print("Argument ", arg1 if arg2 in args else arg2, " is referenced in prefernces but not defined.")
                    raise FormatSyntaxException("Argument referenced before initialization.")
            c = file.readline()
    elif fileformat ==  "papx":
        while c != "":
            if c == "\n":
                continue
            elif c[:3:1] == "arg":
                arg = c[c.find("(")+1:c.find(")"):1]
                args.add(arg)
                attacksFrom[arg] = set()
                preferences[arg] = set()
            elif c[:3:1] == "att":
                arg1 = c[c.find("(")+1:c.find(","):1]
                arg2 = c[c.find(",")+1:c.find(")")]
                if arg1 in args and arg2 in args:
                    attacksFrom[arg1].add(arg2)
                else:
                    print("Argument ", arg1 if arg2 in args else arg2, " is referenced in prefernces but not defined.")
                    raise FormatSyntaxException("Argument referenced before initialization.")
            elif c[:4:1] == "pref":
                arg1 = c[c.find("(")+1:c.find(","):1]
                arg2 = c[c.find(",")+1:c.find(")")]
                if arg1 in args and arg2 in args and arg1 not in preferences[arg2]:
                    preferences[arg1].add(arg2)
                    for i in preferences[arg2]:
                        preferences[arg1].add(i)
                    for j in preferences.keys():
                        if arg1 in preferences[j]:
                            preferences[j].add(arg2)
                elif arg1 in preferences[arg2]:
                    print("Ambiguious preferences : ", arg1, " and ", arg2, " are mutually preferred over the other.")
                    raise PreferenceException("Ambiguious preferences")
                else:
                    print("Argument ", arg1 if arg2 in args else arg2, " is referenced in preferences but not defined.")
                    raise FormatSyntaxException("Argument referenced before initialization.")
            else:
                raise FormatException(".papx format Exception, unknown identifier")
            c = file.readline()
    else:
        print("Unsupported format ", fileformat,", suported formats are : ")
        print_formats()
        raise UnsupportedFormatException("Unsuported format : ", fileformat)
    file.flush()
    file.close()
    return(args, attacksFrom, preferences)

def toFile(args, attacksFrom, outputFile = "AF", fileformat = "tgf"):
    """
    Function writting the AF (after the reductions) in a file.
    The name of the file has to be written without the extension.
    Otherwise the name of the resulting file will be something like this : file.extension.extension.
    set*dict*str*str --> None
    """
   
    assert type(args) is set, "The first argument of this method must be the set of arguments. (type Set)"
    assert type(attacksFrom) is dict, "The second argument of this method must be the dictionary having for keys the arguments attacking and for values the arguments attacked. (type Dictionary)"
    assert type(outputFile) is str, "The third argument of this method must be the name of the outputFile. (type String)"
    assert type(fileformat) is str, "The last/fourth argument of this method method must be the extension of the outputFile. (type Dictionary)"
    
    file = open(''.join([outputFile, ".", fileformat]) , "w+")
    if fileformat == "tgf":
        for i in args:
            file.write("".join([i,"\n"]))
        file.write("#\n")
        for j in attacksFrom.keys():
            for k in attacksFrom[j]:
                file.write(''.join([j," ",k,"\n"]))
    elif fileformat == "apx":
        for i in args:
            file.write("arg({})\n".format(i))
        for j in attacksFrom.keys():
            for k in attacksFrom[j]:
                file.write("att({},{})\n".format(j,k))
    else:
        print("Unsupported format ", fileformat,", suported formats are : ")
        print_formats()
        raise UnsupportedFormatException("Unsuported format : ", fileformat)
    file.flush()
    file.close()

def reduction1(args, attacksFrom, preferences, fileformat = "tgf"):
    """
    Function applying the first reduction rule to the PAD and then creating a file containing the resulting AF in the selected format.
    dict*dict*dict*str --> file
    """
    assert type(args) is set, "The first argument of this method must be the set of arguments. (type Set)"
    assert type(attacksFrom) is dict, "The second argument of this method must be the dictionary having for keys the arguments attacking and for values the arguments attacked. (type Dictionary)"
    assert type(preferences) is dict, "The third argument of this method must be the dictionary having for keys the arguments preferred and for values the arguments preferred over. (type Dictionary)"
    assert type(fileformat) is str, "The fourth argument of this method must be the format the resulting file (containing the AF) will be. (type String)"
    
    copyAttacksFrom = copy.deepcopy(attacksFrom)
    
    for arg in attacksFrom.keys():
        for j in attacksFrom[arg]:
            if arg in preferences[j]:
                copyAttacksFrom[arg].remove(j)
                
    toFile(args, copyAttacksFrom, "Reduction1-AF", fileformat)

def reduction2(args, attacksFrom, preferences, fileformat = "tgf"):
    """
    Function applying the second reduction rule to the PAD and then creating a file containing the resulting AF in the selected format.
    dict*dict*dict*str --> file
    """
    
    assert type(args) is set, "The first argument of this method must be the set of arguments. (type Set)"
    assert type(attacksFrom) is dict, "The second argument of this method must be the dictionary having for keys the arguments attacking and for values the arguments attacked. (type Dictionary)"
    assert type(preferences) is dict, "The third argument of this method must be the dictionary having for keys the arguments preferred and for values the arguments preferred over. (type Dictionary)"
    assert type(fileformat) is str, "The fourth argument of this method must be the format the resulting file (containing the AF) will be. (type String)"
    
    copyAttacksFrom = copy.deepcopy(attacksFrom)
    
    for arg in attacksFrom.keys():
        for j in attacksFrom[arg]:
            if arg in preferences[j]:
                copyAttacksFrom[arg].remove(j)
                copyAttacksFrom[j].add(arg)
                
    toFile(args, copyAttacksFrom, "Reduction2-AF", fileformat)
    
def reduction3(args, attacksFrom, preferences, fileformat = "tgf"):
    """
    Function applying the third reduction rule to the PAD and then creating a file containing the resulting AF in the selected format.
    dict*dict*dict*str --> file
    """
    
    
    assert type(args) is set, "The first argument of this method must be the set of arguments. (type Set)"
    assert type(attacksFrom) is dict, "The second argument of this method must be the dictionary having for keys the arguments attacking and for values the arguments attacked. (type Dictionary)"
    assert type(preferences) is dict, "The third argument of this method must be the dictionary having for keys the arguments preferred and for values the arguments preferred over. (type Dictionary)"
    assert type(fileformat) is str, "The fourth argument of this method must be the format the resulting file (containing the AF) will be. (type String)"
    
    copyAttacksFrom = copy.deepcopy(attacksFrom)
    
    for arg in attacksFrom.keys():
        for j in attacksFrom[arg]:
            if arg in preferences[j] and arg in attacksFrom[j]:
                copyAttacksFrom[arg].remove(j)
                
    toFile(args, copyAttacksFrom, "Reduction3-AF", fileformat)
    
def reduction4(args, attacksFrom, preferences, fileformat = "tgf"):
    """
    Function applying the fourth reduction rule to the PAD and then creating a file containing the resulting AF in the selected format.
    dict*dict*dict*str --> file
    """
    
    
    assert type(args) is set, "The first argument of this method must be the set of arguments. (type Set)"
    assert type(attacksFrom) is dict, "The second argument of this method must be the dictionary having for keys the arguments attacking and for values the arguments attacked. (type Dictionary)"
    assert type(preferences) is dict, "The third argument of this method must be the dictionary having for keys the arguments preferred and for values the arguments preferred over. (type Dictionary)"
    assert type(fileformat) is str, "The fourth argument of this method must be the format the resulting file (containing the AF) will be. (type String)"
    
    copyAttacksFrom = copy.deepcopy(attacksFrom)
    
    for arg in attacksFrom.keys():
        for j in attacksFrom[arg]:
            if arg in preferences[j]:
                copyAttacksFrom[j].add(arg)
                
    toFile(args, copyAttacksFrom, "Reduction4-AF", fileformat)
    
#On essaie en dessous de simuler un switch case avec les dictionnaires

switcher_options = {
        "--help" : print_help,
        "--problems" : print_problems,
        "--formats" : print_formats,
        "--reductions" : print_reductions
        }

switcher_reductions = {
        1 : reduction1,
        2 : reduction2,
        3 : reduction3,
        4 : reduction4
        }

if argv.length == 2:
    switcher_options.get(argv[1])()

else:
    if "-r" in argv:
        switcher_reductions.get(argv[argv.index("-r")])()
    elif "--r" in argv:
        switcher_reductions.get(argv[argv.index("--r")])()
        
os.system("./mu-toksia")
