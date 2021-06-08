# -*- coding: utf-8 -*-
"""
Created on Tue Jun 8 2021

@author: Eyal Cohen
"""

import os
import tkinter as tk
import TkinterDnD2 as tkd
import PAFtoAF as paf

file = ''
fileformat = ''
reduction = 0
outs = []
task = ''

def load_text(event):
    textarea.delete("1.0","end")
    if event.data.endswith(".ptgf") or event.data.endswith(".papx"):
        with open(event.data, "r") as file:
            for line in file:
                line=line.strip()
                textarea.insert("end",f"{line}\n")
        paf.toPaf(event.data, "ptgf")
        button1["state"] = tk.NORMAL
        button2["state"] = tk.NORMAL
        button3["state"] = tk.NORMAL
        button4["state"] = tk.NORMAL
    elif event.data.endswith(".tgf") or event.data.endswith(".apx"):
        with open(event.data, "r") as file:
            for line in file:
                line=line.strip()
                textarea.insert("end",f"{line}\n")
        button1["state"] = tk.NORMAL
        button2["state"] = tk.NORMAL
        button3["state"] = tk.NORMAL
        button4["state"] = tk.NORMAL
    else:
        button1["state"] = tk.DISABLED
        button2["state"] = tk.DISABLED
        button3["state"] = tk.DISABLED
        button4["state"] = tk.DISABLED
        textarea.insert("end","Sorry this document format is not\naccepted.\nPlease use .ptgf .papx .tgf or .apx\nformats.\n\nFor help please click on the help button and to see the available formats click onthe formats button.")
        
ws = tkd.TkinterDnD.Tk()
ws.title('PythonGuides')
ws.geometry('698x319')
ws.config(bg='#fcb103')

frame = tk.Frame(ws)
frame.pack()

frameDnD = tk.Frame(frame)
frameDnD.pack(side = tk.LEFT)

frameReduction = tk.Frame(frame)
frameReduction.pack(side = tk.RIGHT)

def ClickReduc1():
    paf.reduction1(["Reduction1-AF-tmp.tgf"], "tgf")
    with open("Reduction1-AF-tmp.tgf","r") as file:
        textareaReduc.delete("1.0", "end")
        for line in file:
            line = line.strip()
            textareaReduc.insert("end", f"{line}\n")
    os.remove("Reduction1-AF-tmp.tgf")
    button1["state"] = tk.DISABLED
    button2["state"] = tk.NORMAL
    button3["state"] = tk.NORMAL
    button4["state"] = tk.NORMAL

def ClickReduc2():
    paf.reduction2(["Reduction2-AF-tmp.tgf"], "tgf")
    with open("Reduction2-AF-tmp.tgf","r") as file:
        textareaReduc.delete("1.0", "end")
        for line in file:
            line = line.strip()
            textareaReduc.insert("end", f"{line}\n")
    os.remove("Reduction2-AF-tmp.tgf")
    button2["state"] = tk.DISABLED
    button1["state"] = tk.NORMAL
    button3["state"] = tk.NORMAL
    button4["state"] = tk.NORMAL

def ClickReduc3():
    paf.reduction3(["Reduction3-AF-tmp.tgf"], "tgf")
    with open("Reduction3-AF-tmp.tgf","r") as file:
        textareaReduc.delete("1.0", "end")
        for line in file:
            line = line.strip()
            textareaReduc.insert("end", f"{line}\n")
    os.remove("Reduction3-AF-tmp.tgf")
    button3["state"] = tk.DISABLED
    button1["state"] = tk.NORMAL
    button2["state"] = tk.NORMAL
    button4["state"] = tk.NORMAL

def ClickReduc4():
    paf.reduction4(["Reduction4-AF-tmp.tgf"], "tgf")
    with open("Reduction4-AF-tmp.tgf","r") as file:
        textareaReduc.delete("1.0", "end")
        for line in file:
            line = line.strip()
            textareaReduc.insert("end", f"{line}\n")
    os.remove("Reduction4-AF-tmp.tgf")
    button4["state"] = tk.DISABLED
    button1["state"] = tk.NORMAL
    button2["state"] = tk.NORMAL
    button3["state"] = tk.NORMAL

textarea = tk.Text(frameDnD, height=18, width=41)
textarea.pack(side=tk.LEFT)
textarea.drop_target_register(tkd.DND_FILES)
textarea.dnd_bind('<<Drop>>', load_text)
textarea.insert("end", "\n\nPlease drag a file here.\n\nAccepted formats are ptgf, papx,\ntgf or apx.")

sbv = tk.Scrollbar(frameDnD, orient=tk.VERTICAL)
sbv.pack(side=tk.RIGHT, fill=tk.Y)

sbvR = tk.Scrollbar(frameReduction, orient=tk.VERTICAL)
sbvR.pack(side=tk.RIGHT, fill=tk.Y)

textarea.configure(yscrollcommand=sbv.set)
sbv.config(command=textarea.yview)

buttonframe = tk.Frame(height = 5, width = 40)
buttonframe.pack(side = tk.BOTTOM)

button1 = tk.Button(buttonframe, activebackground = "red", bg = "white", text = "reduction 1", state = tk.DISABLED, command = ClickReduc1)
button1.pack(side = tk.LEFT)

button2 = tk.Button(buttonframe, activebackground = "red", bg = "white", text = "reduction 2", state = tk.DISABLED, command = ClickReduc2)
button2.pack(side = tk.LEFT)

button3 = tk.Button(buttonframe, activebackground = "red", bg = "white", text = "reduction 3", state = tk.DISABLED, command = ClickReduc3)
button3.pack(side = tk.LEFT)

button4 = tk.Button(buttonframe, activebackground = "red", bg = "white", text = "reduction 4", state = tk.DISABLED, command = ClickReduc4)
button4.pack(side = tk.LEFT)

textareaReduc = tk.Text(frameReduction, height=18, width=41)
textareaReduc.pack(side=tk.LEFT)

textareaReduc.configure(yscrollcommand = sbvR.set)
sbvR.config(command = textareaReduc.yview)

ws.mainloop()