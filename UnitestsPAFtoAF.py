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

if os.path.exists("temp_unitest_PAFtoAF"):
    if os.path.isdir("temp_unitest_PAFtoAF"):
        dir_name = "temp_unitest_PAFtoAF"
        create = False
    else:
        dir_name = "temp_unitest_PAFtoAF_dir"
        create = True
else:
    dir_name = "temp_unitest_PAFtoAF"
    create = True

count = 0
actual_PAF = (paf.args, paf.attacksFrom, paf.preferences)
error = None
suppress = False
file = ''

def generate_PAF(nodes, function = print):
    global error
    global count
    global file
    edges = 0
    preferences = 0
    attsFrom = dict()
    prefs = dict()
    arg_gen = set([arg for arg in range(nodes+1)])
    for arg in arg_gen :
        attsFrom[arg] = set()
        prefs[arg] = set()
    edge_list = []
    yield(arg_gen, attsFrom, prefs)
    for arg1 in range(nodes+1):
        for arg2 in range(nodes+1):
            edge_list.append((arg1,arg2))
    pref_list = edge_list.copy()
    for i in range(2**nodes + 1):
        new_file()
        lim = 0
        if r.random()>0.25:
            try:
                att = r.choice(edge_list)
                edge_list.remove(att)
                attsFrom[att[0]].add(att[1])
                function(file, att, "attack")
                lim = 0.55
                edges += 1
            except(IndexError):
                continue
        if r.random()>lim:
            try:
                pref = r.choice(pref_list)
                pref_list.remove(pref)
                prefs[pref[0]].add(pref[1])
                if pref[0] in prefs[pref[1]] or pref[0] == pref[1]:
                    error = paf.PreferenceException
                    fileformat = ("ptgf", "papx")[file.endswith("papx") or file.endswith("apx")]
                    errfile = toFILE((arg_gen, attsFrom, prefs), fileformat, "pref_error")
                else:
                    function(file, pref, "preference")
                preferences += 1
            except(IndexError):
                continue
        yield((arg_gen, attsFrom, prefs))
        if error is paf.PreferenceException:
            global suppress
            prefs[pref[0]].remove(pref[1])
            if suppress:
                os.remove(errfile)
            error = None

def new_file(): #TODO ?????
    global file
    global count
    new_file = file.replace(str(count-1), str(count))
    with open(file, "r") as openfile:
        content = openfile.read()
    with open(new_file, "w+") as openfile:
        openfile.write(content)
    #os.rename(file, new_file)
    file = new_file

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
                
def addPTGF(file, relation, name):
    if name == "argument":
        with open(file, "r+") as openfile:
            content = openfile.read()
            openfile.seek(0,0)
            openfile.write(f"{relation}\n{content}")
    elif name == "attack":
        with open(file, "r+") as openfile:
            openfile.seek(0,0)
            content = openfile.read()
            openfile.seek(0,0)
            att_index = content.rindex("#")
            beginning_content = content[:att_index:]
            end_content = content[att_index::]
            openfile.write(f"{beginning_content}{relation[0]} {relation[1]}\n{end_content}")
    elif name == "preference":
        with open(file, "a+") as openfile:
            openfile.write(f"{relation[0]} {relation[1]}\n")
    else: raise paf.FormatSyntaxException("Format Syntax Error while testing.")
        

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

def addPAPX(file, relation, name):
    if name == "argument":
        with open(file, "r+") as openfile:
            content = openfile.read()
            openfile.seek(0,0)
            openfile.write(f"arg({relation})\n{content}")
    else:
        with open(file, "a") as openfile:
            if name == "attack":
                openfile.write(f"att({relation[0]},{relation[1]})")
            elif name == "preference":
                openfile.write(f"pref({relation[0]},{relation[1]})")
            else: raise paf.FormatSyntaxException("Format Syntax Error while testing.")

def test(timeout, start_nodes = 0, fileformat = "ptgf"):
    global count
    global file
    nodes = start_nodes
    start = time.time()
    file = toFILE(([arg for arg in range(nodes+1)], dict(), dict()), fileformat)
    if fileformat == "ptgf":
        function = addPTGF
    elif fileformat == "papx":
        function = addPAPX
    else: raise paf.FormatException("Format Exception while testing. Please use ptgf or papx as file format.")
    while (time.time()-start)<=timeout:
        for actual_PAF in generate_PAF(nodes, function = function):
            print(actual_PAF)
            print(error)
            count += 1
            if(time.time()-start>timeout):break
        nodes += 1
        function(file, nodes, "argument")
    print(count)

if create:
    os.mkdir(dir_name)

os.chdir(dir_name)

test(1)
time.sleep(60)

os.chdir("..")

for file in os.scandir(dir_name):
    os.remove(file)
    
os.rmdir(dir_name)
