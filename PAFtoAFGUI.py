# -*- coding: utf-8 -*-
"""
Created on Tue Jun 8 2021

@author: Eyal Cohen
"""

import os
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import tkinter as tk
from PIL import (Image,ImageTk)
import networkx as nx
import TkinterDnD2 as tkd
import PAFtoAF as paf

inputfile = ''
fileformat = ''
task= ''
query = ''
outs = ["standard output"]
solver = ''
solverPath = ''
reduction = 0
fig = Figure()

def load_text(event):
    textarea.delete("1.0","end")
    textareaReduc.delete("1.0","end")
    button1["bg"] = "white"
    button2["bg"] = "white"
    button3["bg"] = "white"
    button4["bg"] = "white"
    global inputfile
    global fileformat
    if event.data.endswith(".ptgf") or event.data.endswith(".papx"):
        inputfile = event.data
        fileformat = "ptgf" if event.data.endswith(".ptgf") else "papx"
        with open(event.data, "r") as file:
            for line in file:
                line=line.strip()
                textarea.insert("end",f"{line}\n")
        paf.toPaf(event.data, "ptgf" if event.data.endswith(".ptgf") else "papx")
        button1["state"] = tk.NORMAL
        button2["state"] = tk.NORMAL
        button3["state"] = tk.NORMAL
        button4["state"] = tk.NORMAL
    elif event.data.endswith(".tgf") or event.data.endswith(".apx"):
        inputfile = event.data
        fileformat = "tgf" if event.data.endswith(".tgf") else "apx"
        with open(event.data, "r") as file:
            for line in file:
                line=line.strip()
                textarea.insert("end",f"{line}\n")
        paf.toPaf(event.data,"ptgf" if event.data.endswith(".ptgf") else "papx")
        button1["state"] = tk.NORMAL
        button2["state"] = tk.NORMAL
        button3["state"] = tk.NORMAL
        button4["state"] = tk.NORMAL
    else:
        button1["state"] = tk.DISABLED
        button2["state"] = tk.DISABLED
        button3["state"] = tk.DISABLED
        button4["state"] = tk.DISABLED
        paf.args.clear()
        paf.attacksFrom.clear()
        paf.preferences.clear()
        textarea.insert("end","Sorry this document format is not\naccepted.\nPlease use .ptgf .papx .tgf or .apx\nformats.\n\nFor help please click on the help button and to see the available formats click onthe formats button.")
    global graph_check_value
    if graph_check_value.get() == 1:
        show_graph()
        

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
    help_window.geometry("686x480")
    help_window.config(bg = "#dddddd")
    help_frame = tk.Frame(help_window, height = 30, width = 86)
    help_frame.pack()
    help_text = tk.Text(help_frame, height = 28, width = 84)
    help_text.pack(side = tk.TOP)
    help_text.insert("end", "This is the GUI version of PAFtoAF Version 1.0, created by Eyal Cohen.\n")
    help_text.insert("end", "\nThis application allows you to use a Preference-based Argumentation Framework\n(PAF) and transform it into an Extension-based Argumentation Framework (AF).\n")
    help_text.insert("end", "\nTo do so, please choose a file in the ptgf, papx, tgf or apx format\n(for more information please click on the formats button in the main window).\n")
    help_text.insert("end", "\nDrag you file in the area specifying so. The text in the file should now appear.\n")
    help_text.insert("end", "\nYou can generate the graph described in the file by checking\nthe box under the text area.\nA png file with the graph, named graph-filename.png will be saved in the folder\ncontaining this app.\n")
    help_text.insert("end", "\nThen select the reduction you wish to apply, the resulting AF should\nappear in a ptg or apx format. The same chekbox is under this text area.")
    help_text.insert("end", "\nIf you want to use a solver, please enter it's name in the line all\nthe way down, in abscence of a name, mu-toksia will be selected under Linux\nand JArgSemSAT under Windows.\n")
    help_text.insert("end", "\nFinally you can select the task you would like to carry out.\nAnd all the options that you want to apply, using the buttons under\n'Solver Options :'.\n")
    help_text.insert("end", "\nThe result should appear in the figure down below, if you want to dowload it\nplease indicate the path to the directory and then press the dowload button.\n")

def show_formats():
    def show_ptgf():
        formats_text.delete("1.0", "end")
        formats_text.insert("end", "\nThe tgf (Trivial Graph Format) is a usualformat for files\ndescipting an AF.\n")
        formats_text.insert("end", "Here we add the preference side of a Preference-base AF (PAF).\n")
        formats_text.insert("end", "\nTo do so, we add on the tgf format a second # delimiting\na third area, where the prefernces are written as attacks.\n")
        formats_text.insert("end", "So arguments are written as their names, then a # is placed,\nfollowed by the attacks where 1 2 means that 1 attacks 2.\n")
        formats_text.insert("end", "Then a second # is placed and finally the preferences\nwhere 1 2 means 1 is prefered over 2.\n")
        formats_text.insert("end", "Here is an exemple :\n1\n2\n3\n#\n1 2\n2 1\n2 3\n#\n1 2\n\nMeans that 1 and 2 attack each other, 2 attack 3, 1 is preffered\nover 2.")
        p_tgfButton["bg"] = "red"
        p_tgfButton["state"] = tk.DISABLED
        p_apxButton["bg"] = "white"
        p_apxButton["state"] = tk.NORMAL
    def show_papx():
        formats_text.delete("1.0", "end")
        formats_text.insert("end", "\nThe apx (Aspartix) is a usualformat for files\ndescipting an AF.\n")
        formats_text.insert("end", "Here we add the preference side of a Preference-base AF (PAF).\n")
        formats_text.insert("end", "\nTo do so, we add on the apx format a new keyword\nfor the prefernces : pref.\n")
        formats_text.insert("end", "So arguments are written as arg(name) followed by\nthe attacks where att(1,2) means that 1 attacks 2.\n")
        formats_text.insert("end", "Finally the preferences written pref(1,2) if 1 is prefered\nover 2.\n")
        formats_text.insert("end", "Here is an exemple :\narg(1)\narg(2)\narg(3)\natt(1,2)\natt(2,1)\natt(2,3)\npref(1,2)\n\nMeans that 1 and 2 attack each other, 2 attack 3, 1 is preffered\nover 2.")
        p_apxButton["bg"] = "red"
        p_apxButton["state"] = tk.DISABLED
        p_tgfButton["bg"] = "white"
        p_tgfButton["state"] = tk.NORMAL
    formats_window = tk.Tk()
    formats_window.title("HELP")
    formats_window.geometry("686x480")
    formats_window.config(bg = "#dddddd")
    formats_frame = tk.Frame(formats_window, height = 30, width = 86)
    formats_frame.pack()
    accepted_formats_text = tk.Text(formats_frame, height = 4, width = 84)
    accepted_formats_text.pack(side = tk.TOP)
    formats_text = tk.Text(formats_frame, height = 28, width = 84)
    buttonsframe = tk.Frame(formats_frame, height = 5, width = 84)
    buttonsframe.pack(side = tk.TOP)
    p_tgfButton = tk.Button(buttonsframe, text = "tgf and ptgf", bg = "white", activebackground = "red", command = show_ptgf)
    p_apxButton = tk.Button(buttonsframe, text = "apx and papx", bg = "white", activebackground = "red", command = show_papx)
    p_tgfButton.pack(side = tk.LEFT)
    p_apxButton.pack(side = tk.LEFT)
    formats_text.pack(side = tk.TOP)
    accepted_formats_text.insert("end", "The formats accepted are ptgf, papx, tgf, and apx.\n")
    
def ClickReduc1():
    global reduction
    reduction = 1
    paf.reduction1(["Reduction1-AF-tmp.{}".format("tgf" if (fileformat == "ptgf" or fileformat == "tgf") else "apx")], "tgf" if (fileformat == "ptgf" or fileformat == "tgf") else "apx")
    with open("Reduction1-AF-tmp.{}".format("tgf" if (fileformat == "ptgf" or fileformat == "tgf") else "apx"),"r") as file:
        textareaReduc.delete("1.0", "end")
        for line in file:
            line = line.strip()
            textareaReduc.insert("end", f"{line}\n")
    os.remove("Reduction1-AF-tmp.{}".format("tgf" if (fileformat == "ptgf" or fileformat == "tgf") else "apx"))
    button1["bg"] = "red"
    button1["state"] = tk.DISABLED
    button2["bg"] = "white"
    button2["state"] = tk.NORMAL
    button3["bg"] = "white"
    button3["state"] = tk.NORMAL
    button4["bg"] = "white"
    button4["state"] = tk.NORMAL

def ClickReduc2():
    global reduction
    reduction = 2
    paf.reduction2(["Reduction2-AF-tmp.{}".format("tgf" if (fileformat == "ptgf" or fileformat == "tgf") else "apx")], "tgf" if (fileformat == "ptgf" or fileformat == "tgf") else "apx")
    with open("Reduction2-AF-tmp.{}".format("tgf" if (fileformat == "ptgf" or fileformat == "tgf") else "apx"),"r") as file:
        textareaReduc.delete("1.0", "end")
        for line in file:
            line = line.strip()
            textareaReduc.insert("end", f"{line}\n")
    os.remove("Reduction2-AF-tmp.{}".format("tgf" if (fileformat == "ptgf" or fileformat == "tgf") else "apx"))
    button2["bg"] = "red"
    button2["state"] = tk.DISABLED
    button1["bg"] = "white"
    button1["state"] = tk.NORMAL
    button3["bg"] = "white"
    button3["state"] = tk.NORMAL
    button4["bg"] = "white"
    button4["state"] = tk.NORMAL

def ClickReduc3():
    global reduction
    reduction = 3
    paf.reduction3(["Reduction3-AF-tmp.{}".format("tgf" if (fileformat == "ptgf" or fileformat == "tgf") else "apx")], "tgf" if (fileformat == "ptgf" or fileformat == "tgf") else "apx")
    with open("Reduction3-AF-tmp.{}".format("tgf" if (fileformat == "ptgf" or fileformat == "tgf") else "apx"),"r") as file:
        textareaReduc.delete("1.0", "end")
        for line in file:
            line = line.strip()
            textareaReduc.insert("end", f"{line}\n")
    os.remove("Reduction3-AF-tmp.{}".format("tgf" if (fileformat == "ptgf" or fileformat == "tgf") else "apx"))
    button3["bg"] = "red"
    button3["state"] = tk.DISABLED
    button1["bg"] = "white"
    button1["state"] = tk.NORMAL
    button2["bg"] = "white"
    button2["state"] = tk.NORMAL
    button4["bg"] = "white"
    button4["state"] = tk.NORMAL

def ClickReduc4():
    global reduction
    reduction = 4
    paf.reduction4(["Reduction4-AF-tmp.{}".format("tgf" if (fileformat == "ptgf" or fileformat == "tgf") else "apx")], "tgf" if (fileformat == "ptgf" or fileformat == "tgf") else "apx")
    with open("Reduction4-AF-tmp.{}".format("tgf" if (fileformat == "ptgf" or fileformat == "tgf") else "apx"),"r") as file:
        textareaReduc.delete("1.0", "end")
        for line in file:
            line = line.strip()
            textareaReduc.insert("end", f"{line}\n")
    os.remove("Reduction4-AF-tmp.{}".format("tgf" if (fileformat == "ptgf" or fileformat == "tgf") else "apx"))
    button4["bg"] = "red"
    button4["state"] = tk.DISABLED
    button1["bg"] = "white"
    button1["state"] = tk.NORMAL
    button2["bg"] = "white"
    button2["state"] = tk.NORMAL
    button3["bg"] = "white"
    button3["state"] = tk.NORMAL

def show_graph(): #TODO show preferences on the graph and make it WORK and change the help def
    global fig
    global inputfile
    
    if graph_check_value.get() == 1:
        if fig == Figure():
            fig = plt.figure(figsize=(12,12))
        
        plt.clf()
        
        edgeList = []
        
        ax = plt.subplot(111)
        ax.set_title('Graph - {}'.format(inputfile), fontsize=10)
        graph = nx.DiGraph()
        
        for arg1 in paf.attacksFrom.keys():
            for arg2 in paf.attacksFrom[arg1]:
                edgeList.append((arg1,arg2))
        
        graph.add_edges_from(edgeList, color = "k", weight = 2)
        
        critical_edges = []
        
        for arg1 in paf.preferences.keys():
            for arg2 in paf.preferences[arg1]:
                if (arg2, arg1) in edgeList:
                    critical_edges.append((arg2,arg1))
                    
        graph.add_edges_from(critical_edges, color = "r", weight = 3)
        
        colors = nx.get_edge_attributes(graph,'color').values()
        weights = nx.get_edge_attributes(graph,'weight').values()
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, node_size=900, node_color='yellow', font_size=8, font_weight='bold', edge_color = colors, width = list(weights), arrowsize = 30, arrowstyle = "->", with_labels = True)
        
        plt.tight_layout()
        if fileformat in ["ptgf", "papx", "apx", "tgf"]:
            plt.savefig("Graph.png", format="PNG")

    else:
        os.remove("Graph.png")
        plt.close()
    
def show_graph_reduc(): #TODO
    if graph_reduc_value.get() == 0:
        pass
    else:
        pass

def save():
    with(open("PAFtoAFGUI-saved-{}-{}.txt".format(inputfile.replace(".{}".format(fileformat),""), reduction), "w+")) as file:
        file.write("hola")

def on_closing():
    if graph_check_value.get() == 1:
        os.remove("Graph.png")
    ws.destroy()
    ws.quit()

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
graph_check = tk.Checkbutton(frameDnD, disabledforeground = "yellow", text = "generate the graph", variable = graph_check_value, command = show_graph, onvalue = 1)
graph_check.grid(row = 7, column = 0)

help_option = tk.Button(optionframe, activebackground = "red", bg = "white", text = "Help", command = show_help)
help_option.pack(side = tk.LEFT)

formats_option = tk.Button(optionframe, activebackground = "red", bg = "white", text = "Formats", command = show_formats)
formats_option.pack(side = tk.LEFT)

save_option = tk.Button(optionframe, activebackground = "blue", bg = "white", text = "save", command = save)
save_option.pack(side = tk.LEFT)

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
textareaReduc.configure(state = "disabled")

sbvR = tk.Scrollbar(frameReduction, orient=tk.VERTICAL)
sbvR.grid(row = 0, column = 7, rowspan = 6, columnspan = 6, sticky = tk.NS)

graph_reduc_value = tk.IntVar()
graph_reduc = tk.Checkbutton(frameReduction, disabledforeground = "yellow", text = "generate the graph", variable = graph_reduc_value, command = show_graph_reduc)
graph_reduc.grid(row = 7, column = 0)

textareaReduc.configure(yscrollcommand = sbvR.set)
sbvR.config(command = textareaReduc.yview)

ws.protocol("WM_DELETE_WINDOW", on_closing)

ws.mainloop()