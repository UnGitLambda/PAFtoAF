# -*- coding: utf-8 -*-
"""
Created on Tue Jun 8 2021

@author: Eyal Cohen
"""

import os
import matplotlib as plt
plt.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import TkinterDnD2 as tkd
import PAFtoAF as paf
import Graphviz as G

file = ''
fileformat = ''
reduction = 0
outs = []
task = ''

def load_text(event):
    textarea.delete("1.0","end")
    textareaReduc.delete("1.0","end")
    button1["bg"] = "white"
    button2["bg"] = "white"
    button3["bg"] = "white"
    button4["bg"] = "white"
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
ws.title('PAFtoAF')
ws.geometry('750x400')
ws.config(bg='#555555')

frame = tk.Frame(ws, height = 60, width = 82)
frame.pack()

optionframe = tk.Frame(frame, height = 10, width = 40)
optionframe.pack(side = tk.TOP)

frameDnD = tk.Frame(frame, height = 23, width = 41)
frameDnD.pack(side = tk.LEFT)

frameReduction = tk.Frame(frame, height = 23, width = 41)
frameReduction.pack(side = tk.RIGHT)

buttonframe = tk.Frame(height = 5, width = 40)
buttonframe.pack(side = tk.BOTTOM)

def show_help():
    help_window = tk.Tk()
    help_window.title("HELP")
    help_window.geometry("686x460")
    help_window.config(bg = "#dddddd")
    help_frame = tk.Frame(help_window, height = 30, width = 86)
    help_frame.pack()
    help_text = tk.Text(help_frame, height = 28, width = 84)
    help_text.pack(side = tk.TOP)
    help_text.insert("end", "This is the GUI version of PAFtoAF Version 1.0, created by Eyal Cohen.\n")
    help_text.insert("end", "\nThis application allows you to use a Preference-based Argumentation Framework\n(PAF) and transform it into an Extension-based Argumentation Framework (AF).\n")
    help_text.insert("end", "\nTo do so, please choose a file in the ptgf, papx, tgf or apx format\n(for more information please click on the formats button in the main window).\n")
    help_text.insert("end", "\nDrag you file in the area specifying so. The text in the file should now appear.\n")
    help_text.insert("end", "\nYou can generate the graph described in the file by checking\nthe box under the text area.\n")
    help_text.insert("end", "\nThen select the reduction you wish to apply, the resulting AF should\nappear in a ptg or apx format. The same chekbox is under this text area.")
    help_text.insert("end", "\nIf you want to use a solver, please enter it's name in the line all\nthe way down, in abscence of a name, mu-toksia will be selected under Linux\nand JArgSemSAT under Windows.\n")
    help_text.insert("end", "\nFinally you can select the task you would like to carry out.\nAnd all the options that you want to apply, using the buttons under\n'Solver Options :'.\n")
    help_text.insert("end", "\nThe result should appear in the figure down below, if you want to dowload it\nplease indicate the path to the directory and then press the dowload button.\n")

def show_formats():
    formats_window = tk.Tk()
    formats_window.title("HELP")
    formats_window.geometry("666x400")
    formats_window.config(bg = "#dddddd")
    formats_frame = tk.Frame(formats_window)
    formats_frame.pack()
    formats_text = tk.Text(formats_frame)
    formats_text.pack(side = tk.TOP)
    formats_text.insert("end", "hello") #TODO insert instructions aimed towards helping the user understand the ptgf, papx, tgf and apx formats
    
def ClickReduc1():
    paf.reduction1(["Reduction1-AF-tmp.tgf"], "tgf")
    with open("Reduction1-AF-tmp.tgf","r") as file:
        textareaReduc.delete("1.0", "end")
        for line in file:
            line = line.strip()
            textareaReduc.insert("end", f"{line}\n")
    os.remove("Reduction1-AF-tmp.tgf")
    button1["bg"] = "red"
    button1["state"] = tk.DISABLED
    button2["bg"] = "white"
    button2["state"] = tk.NORMAL
    button3["bg"] = "white"
    button3["state"] = tk.NORMAL
    button4["bg"] = "white"
    button4["state"] = tk.NORMAL

def ClickReduc2():
    paf.reduction2(["Reduction2-AF-tmp.tgf"], "tgf")
    with open("Reduction2-AF-tmp.tgf","r") as file:
        textareaReduc.delete("1.0", "end")
        for line in file:
            line = line.strip()
            textareaReduc.insert("end", f"{line}\n")
    os.remove("Reduction2-AF-tmp.tgf")
    button2["bg"] = "red"
    button2["state"] = tk.DISABLED
    button1["bg"] = "white"
    button1["state"] = tk.NORMAL
    button3["bg"] = "white"
    button3["state"] = tk.NORMAL
    button4["bg"] = "white"
    button4["state"] = tk.NORMAL

def ClickReduc3():
    paf.reduction3(["Reduction3-AF-tmp.tgf"], "tgf")
    with open("Reduction3-AF-tmp.tgf","r") as file:
        textareaReduc.delete("1.0", "end")
        for line in file:
            line = line.strip()
            textareaReduc.insert("end", f"{line}\n")
    os.remove("Reduction3-AF-tmp.tgf")
    button3["bg"] = "red"
    button3["state"] = tk.DISABLED
    button1["bg"] = "white"
    button1["state"] = tk.NORMAL
    button2["bg"] = "white"
    button2["state"] = tk.NORMAL
    button4["bg"] = "white"
    button4["state"] = tk.NORMAL

def ClickReduc4():
    paf.reduction4(["Reduction4-AF-tmp.tgf"], "tgf")
    with open("Reduction4-AF-tmp.tgf","r") as file:
        textareaReduc.delete("1.0", "end")
        for line in file:
            line = line.strip()
            textareaReduc.insert("end", f"{line}\n")
    os.remove("Reduction4-AF-tmp.tgf")
    button4["bg"] = "red"
    button4["state"] = tk.DISABLED
    button1["bg"] = "white"
    button1["state"] = tk.NORMAL
    button2["bg"] = "white"
    button2["state"] = tk.NORMAL
    button3["bg"] = "white"
    button3["state"] = tk.NORMAL

def show_graph(): #TODO
    if graph_check_value == 0:
        pass
    else:
        pass
    
def show_graph_reduc(): #TODO
    if graphh_value == 0:
        pass
    else:
        pass

textarea = tk.Text(frameDnD, height=18, width=41)
textarea.grid(row = 0, column = 0, rowspan = 6, columnspan = 6)
textarea.drop_target_register(tkd.DND_FILES)
textarea.dnd_bind('<<Drop>>', load_text)
textarea.insert("end", "\n\nPlease drag a file here.\n\nAccepted formats are ptgf, papx,\ntgf or apx.")

sbv = tk.Scrollbar(frameDnD, orient=tk.VERTICAL)
sbv.grid(row = 0, column = 7, rowspan = 6, columnspan = 6, sticky = tk.NS)

textarea.configure(yscrollcommand=sbv.set)
sbv.config(command=textarea.yview)

graph_check_value = tk.IntVar()
graph_check = tk.Checkbutton(frameDnD, disabledforeground = "yellow", text = "generate the graph", variable = graph_check_value, command = show_graph)
graph_check.grid(row = 7, column = 0)

help_option = tk.Button(optionframe, activebackground = "red", bg = "white", text = "Help", command = show_help)
help_option.pack(side = tk.LEFT)

formats_option = tk.Button(optionframe, activebackground = "red", bg = "white", text = "Formats", command = show_formats)
formats_option.pack(side = tk.LEFT)

button1 = tk.Button(buttonframe, activebackground = "red", bg = "white", text = "reduction 1", state = tk.DISABLED, command = ClickReduc1)
button1.pack(side = tk.LEFT)

button2 = tk.Button(buttonframe, activebackground = "red", bg = "white", text = "reduction 2", state = tk.DISABLED, command = ClickReduc2)
button2.pack(side = tk.LEFT)

button3 = tk.Button(buttonframe, activebackground = "red", bg = "white", text = "reduction 3", state = tk.DISABLED, command = ClickReduc3)
button3.pack(side = tk.LEFT,)

button4 = tk.Button(buttonframe, activebackground = "red", bg = "white", text = "reduction 4", state = tk.DISABLED, command = ClickReduc4)
button4.pack(side = tk.LEFT)

textareaReduc = tk.Text(frameReduction, height=18, width=41)
textareaReduc.grid(row = 0, column = 0, rowspan = 6, columnspan = 6)

sbvR = tk.Scrollbar(frameReduction, orient=tk.VERTICAL)
sbvR.grid(row = 0, column = 7, rowspan = 6, columnspan = 6, sticky = tk.NS)

graphh_value = tk.IntVar()
graphh = tk.Checkbutton(frameReduction, disabledforeground = "yellow", text = "generate the graph", variable = graphh_value, command = show_graph_reduc)
graphh.grid(row = 7, column = 0)

textareaReduc.configure(yscrollcommand = sbvR.set)
sbvR.config(command = textareaReduc.yview)



ws.mainloop()