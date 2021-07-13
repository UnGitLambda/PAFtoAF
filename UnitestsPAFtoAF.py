# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 19:22:14 2021

@author: Eyal Cohen
"""

import PAFtoAF as paf
import time
from copy import deepcopy
import random as r
import os
from shutil import copyfile
from datetime import datetime
from PAFtoAF import UnsupportedFormatException, FormatSyntaxException,  PreferenceException#, FormatException, CommandLineException, FindingSolverException, UnsupportedOSException

if os.path.exists("temp_unitest_PAFtoAF"):
    if os.path.isdir("temp_unitest_PAFtoAF"):
        dir_name = "temp_unitest_PAFtoAF"
        for file in os.scandir(dir_name):
            os.remove(file)
        os.rmdir(dir_name)
    else:
        dir_name = "temp_unitest_PAFtoAF_dir"
else:
    dir_name = "temp_unitest_PAFtoAF"

count = 0
error = None
suppress = True
file = ''
keep = False

test_time = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

def try_toPaf(file, fileformat = ''):
    """
    This method is just a toPaf that can manage the different possible Exceptions.
    It is invoked every time we want to convert something to the PAF format in PAFtoAF : (set, dict, dict).
    str * str -> None
    """
    
    assert type(file) is str, "The first argument must be the name of the file. (type String)"
    assert type(fileformat) is str, "The second argument must be the format of the file. (type String)"
    
    global error
    global suppress
    global keep
    if fileformat == '':
        try:
            paf.toPaf(file, "ptgf" if file.endswith(".ptgf") or file.endswith(".tgf") else "papx")
            if error is None:
                keep = False
                suppress = True
            else:
                keep = True
                suppress = False
        except FileNotFoundError as e:
            if error != FileNotFoundError:
                suppress = False
                keep = True
                with open(file, "a+") as openfile:
                    openfile.write(str(e))
            else:
                suppress = True
                keep = False
            print("It seems that the file you used as input can not be found anymore.")
        except (IOError, OSError) as e:
            if error != IOError or error != OSError:
                suppress = False
                keep = True
                with open(file, "a+") as openfile:
                    openfile.write(str(e))
            else:
                suppress = True
                keep = False
            print("System Error")
        except FormatSyntaxException as e:
            if error != FormatSyntaxException:
                suppress = False
                keep = True
                with open(file, "a+") as openfile:
                    openfile.write(str(e))
            else:
                suppress = True
                keep = False
        except PreferenceException as e:
            if error != PreferenceException:
                suppress = False
                keep = True
                with open(file, "a+") as openfile:
                    openfile.write(str(e))
            else:
                suppress = True
                keep = False
        except UnsupportedFormatException as e:
            if error != UnsupportedFormatException:
                suppress = False
                keep = True
                with open(file, "a+") as openfile:
                    openfile.write(str(e))
            else:
                suppress = True
                keep = False
    elif fileformat in ["ptgf", "tgf", "papx", "apx"]:
        try:
            paf.toPaf(file, "ptgf" if fileformat in ["ptgf", "tgf"] else "papx")
        except FileNotFoundError as e:
            if error != FileNotFoundError:
                suppress = False
                keep = True
                with open(file, "a+") as openfile:
                    openfile.write(str(e))
            else:
                suppress = True
                keep = False
            print("It seems that the file you used as input can not be found anymore.")
            
        except (IOError, OSError) as e:
            if error != IOError or error != OSError:
                suppress = False
                keep = True
                with open(file, "a+") as openfile:
                    openfile.write(str(e))
            else:
                suppress = True
                keep = False
            print("System Error")
            
        except FormatSyntaxException as e:
            if error != FormatSyntaxException:
                suppress = False
                keep = True
                with open(file, "a+") as openfile:
                    openfile.write(str(e))
            else:
                suppress = True
                keep = False
        except PreferenceException as e:
            if error != PreferenceException:
                suppress = False
                keep = True
                with open(file, "a+") as openfile:
                    openfile.write(str(e))
            else:
                suppress = True
                keep = False
    else:
        print("Unaccepted fileformat")
        paf.print_formats()

def generate_PAF(nodes, fileformat = "ptgf"):
    """
    This is a graph generator, it generates a graph having nodes 
    It generates 1 graph if nodes = 0 and 2^n + 1 graphs if not.
    It also affects the global variable 'error' if a preference error is in 
    the generated graph and then suppress it and generates a new one.
    Int * str -> generator of (set, dict, dict)
    """
    global error
    global count
    global file
    copy_prefs = dict()
    edges = 0
    preferences = 0
    attsFrom = dict()
    prefs = dict()
    arg_gen = set([arg for arg in range(nodes+1)])
    for arg in arg_gen :
        attsFrom[arg] = set()
        prefs[arg] = set()
    edge_list = []
    #file = toFILE((arg_gen, attsFrom, prefs), fileformat)
    yield(arg_gen, attsFrom, prefs)
    for arg1 in range(nodes+1):
        for arg2 in range(nodes+1):
            edge_list.append((arg1,arg2))
    pref_list = edge_list.copy()
    for i in range(nodes+1):
        pref_list.remove((i,i))
    num_PAF = (1, 2**nodes + 1)[nodes != 0]
    for i in range(num_PAF):
        copy_prefs.clear()
        add_pref = False
        lim = 0
        if r.random()>0.25 and len(edge_list)!=0:
                att = r.choice(edge_list)
                edge_list.remove(att)
                attsFrom[att[0]].add(att[1])
                lim = 0.55
                edges += 1
        if r.random()>lim and len(edge_list) !=0:
            try:
                add_pref = True
                pref = r.choice(pref_list)
                pref_list.remove(pref)
                prefs[pref[0]].add(pref[1])
                copy_prefs = deepcopy(prefs)
                for i in copy_prefs[pref[1]]:
                    copy_prefs[pref[0]].add(i)
                for j in copy_prefs.keys():
                    if pref[0] in copy_prefs[j]:
                        copy_prefs[j].add(pref[1])
                if pref[0] in copy_prefs[pref[1]] or pref[0] == pref[1]:
                    error = PreferenceException
                    fileformat = ("ptgf", "papx")[file.endswith("papx") or file.endswith("apx")]
                    errfile = toFILE((arg_gen, attsFrom, prefs), fileformat, "pref_error")
                preferences += 1
            except(IndexError):
                continue
        yield((arg_gen, attsFrom, prefs))
        if error is None and add_pref:
            prefs = deepcopy(copy_prefs)
        elif error is PreferenceException:
            global suppress
            prefs[pref[0]].remove(pref[1])
            copy_prefs.clear()
            if suppress:
                os.remove(errfile)
            else:
                os.rename(errfile, errfile+".logerr")
            error = None

def new_file():
    """
    This method just modify the name of the old file by replacing the old count by the new count.
    """
    global file
    global count
    global keep
    global error
    new_file = file.replace(str(count-1), str(count))
    if keep:
        if error is None:
            copyfile(file, f"{file}.log")
    os.rename(file, new_file)
    file = new_file

# =============================================================================
# def toFILE(PAF, fileformat, offset = None):
#     if fileformat == "ptgf":
#         file = toPTGF(PAF, offset)
#     elif fileformat == "papx":
#         file = toPAPX(PAF, offset)
#     else: raise paf.FormatException("Wrong Format while testing. Please use ptgf or papx format.")
#     return(file)
# =============================================================================

def toFILE(PAF, fileformat, offset = None):
    if fileformat == "ptgf":
        file = toPTGF(PAF, offset)
    elif fileformat == "papx":
        file = toPAPX(PAF, offset)
    else: raise paf.FormatException("Wrong Format while testing. Please use ptgf or papx format.")
    return(file)

def toPTGF(PAF, offset):
    global count
    file = "test{}-{}.ptgf".format(count, ("","".join(["",str(offset)]))[offset is not None])
    with open(file, "w+") as openfile:
        for arg in PAF[0]:
            openfile.write(f'{arg}\n')
        openfile.write("#\n")
        for arg1 in  PAF[1].keys():
            for arg2 in PAF[1][arg1]:
                openfile.write(f"{arg1} {arg2}\n")
        openfile.write("#\n")
        for arg1 in PAF[2].keys():
            for arg2 in PAF[2][arg1]:
                openfile.write(f"{arg1} {arg2}\n")
    return(file)    

# =============================================================================
# def addPTGF(file, relation, name):
#     if name == "argument":
#         with open(file, "w+") as openfile:
#             openfile.seek(0,0)
#             for arg in range(relation):
#                 openfile.write(f"{arg}\n")
#             openfile.write("#\n#\n")
#     elif name == "attack":
#         with open(file, "r+") as openfile:
#             openfile.seek(0,0)
#             content = openfile.read()
#             openfile.seek(0,0)
#             att_index = content.rindex("#")
#             beginning_content = content[:att_index:]
#             end_content = content[att_index::]
#             openfile.write(f"{beginning_content}{relation[0]} {relation[1]}\n{end_content}")
#     elif name == "preference":
#         with open(file, "a+") as openfile:
#             openfile.write(f"{relation[0]} {relation[1]}\n")
#     else: raise paf.FormatSyntaxException("Format Syntax Error while testing.")
# =============================================================================

def toPAPX(PAF, offset):
    global count
    file = "test{}{}.papx".format(count, ("","".join(["",str(offset)]))[offset is not None])
    with open(file, "w+") as openfile:
        for arg in PAF[0]:
            openfile.write(f'arg({arg})\n')
        for arg1 in  PAF[1].keys():
            for arg2 in PAF[1][arg1]:
                openfile.write(f"att({arg1},{arg2})\n")
        for arg1 in PAF[2].keys():
            for arg2 in PAF[2][arg1]:
                openfile.write(f"pref({arg1},{arg2})\n")
    return(file)

# =============================================================================
# def addPAPX(file, relation, name):
#     if name == "argument":
#         with open(file, "w+") as openfile:
#             openfile.seek(0,0)
#             for arg in range(relation):
#                 openfile.write(f"arg({relation})\n")
#     else:
#         with open(file, "a") as openfile:
#             if name == "attack":
#                 openfile.write(f"att({relation[0]},{relation[1]})")
#             elif name == "preference":
#                 openfile.write(f"pref({relation[0]},{relation[1]})")
#             else: raise paf.FormatSyntaxException("Format Syntax Error while testing.")
# =============================================================================

def test_toPAF(timeout, start_nodes = 0, fileformat = "ptgf"):
    global count
    global file
    nodes = start_nodes
    start = time.time()
    file = toFILE(([arg for arg in range(nodes+1)], dict(), dict()), fileformat)
    while (time.time()-start)<=timeout:
        for actual_PAF in generate_PAF(nodes, fileformat):
            sortie = time.time()-start>timeout
            file = toFILE(actual_PAF, fileformat)
            try_toPaf(file, fileformat)
            if error is not None:
                os.remove(file)
            elif not keep:
                os.remove(file)
            else:
                os.rename(file, f"{file}.log")
            count += 1
            if(sortie):break
        nodes += 1
    print(count)

os.mkdir(dir_name)

os.chdir(dir_name)

test_toPAF(10)

os.chdir("..")
    
if len(os.listdir()) == 0:
    os.rmdir(dir_name)
