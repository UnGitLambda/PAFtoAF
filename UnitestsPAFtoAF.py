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

nodes = 3
edges = 0
preferences = 0
count = 0
actual_PAF = (paf.args, paf.attacksFrom, paf.preferences)
error = None

def generate_PAF():
    global nodes
    global edges
    global preferences
    global error
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
        lim = 0
        if r.random()>0.25:
            att = r.choice(edge_list)
            edge_list.remove(att)
            attsFrom[att[0]].add(att[1])
            lim = 0.55
            edges += 1
        if r.random()>lim:
            pref = r.choice(pref_list)
            pref_list.remove(pref)
            prefs[pref[0]].add(pref[1])
            if pref[0] in prefs[pref[1]] or pref[0] == pref[1]:
                error = paf.PreferenceException
            preferences += 1
        yield((arg_gen, attsFrom, prefs))
        if error is paf.PreferenceException:
            prefs[pref[0]].remove(pref[1])
            error = None

def toFILE(PAF, fileformat):
    if fileformat == "ptgf":
        toPTGF(PAF)
    elif fileformat == "papx":
        toPAPX(PAF)
    else: raise paf.FormatException("Wrong Format while testing")

def toPTGF(PAF):
    global count
    with open("test{count}.ptgf", "w+") as file:
        for arg in PAF[0]:
            file.write(f'{arg}\n')
        file.write("#\n")
        for arg1 in  PAF[1].keys():
            for arg2 in PAF[1][arg1]:
                file.write(f"{arg1} {arg2}\n")
        file.write("#\n")
        for arg1 in PAF[2].keys():
            for arg2 in PAF[2][arg1]:
                file.write(f"{arg1} {arg2}\n")
                
def addPTGF(file, relation, name):
    if name == "argument":
        with open(file, "r+") as openfile:
            content = openfile.read()
            openfile.seek(0,0)
            openfile.write(f"{relation}\n{content}")
    elif name == "attack":
# ============================================================================= #TODO
#         with open(file, "r+") as openfile:
#             content = openfile.read()
#             att_index = content.index("#")
#             openfile.seek(att_index+2, 0)
#             content = content[att_index+2::]
#             openfile.write(f"{relation[0]} {relation[1]}")
#             openfile.write(content)
# =============================================================================
        print("todo")
    elif name == "pref":
        with open(file, "a") as openfile:
            openfile.write(f"{relation[0]} {relation[1]}")
        

def toPAPX(PAF):
    global count
    with open(f"test{count}.papx", "w+") as file:
        for arg in PAF[0]:
            file.write(f'arg({arg})\n')
        for arg1 in  PAF[1].keys():
            for arg2 in PAF[1][arg1]:
                file.write(f"att({arg1},{arg2})\n")
        for arg1 in PAF[2].keys():
            for arg2 in PAF[2][arg1]:
                file.write(f"pref({arg1},{arg2})\n")

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
            elif name == "pref":
                openfile.write(f"pref({relation[0]},{relation[1]})")
            else: raise paf.FormatSyntaxException("Format Syntax Error while testing.")

def test(timeout):
    global count
    start = time.time()
    while (time.time()-start)<=timeout:
        count += 1
        for actual_PAF in generate_PAF():
            print(actual_PAF[0])
            print(actual_PAF[1])
            print(actual_PAF[2])
            print(error)


os.mkdir("temp_unitest_PAFtoAF")

os.chdir("temp_unitest_PAFtoAF")

os.chdir("..")

for file in os.scandir("temp_unitest_PAFtoAF"):
    os.remove(file)
    
os.rmdir("temp_unitest_PAFtoAF")
