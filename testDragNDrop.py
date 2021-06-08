# -*- coding: utf-8 -*-
"""
Created on Tue Jun 8 2021

@author: Eyal Cohen
"""

import tkinter as tk
import TkinterDnD2 as tkd
import PAFtoAF as paf



def load_text(event):
    textarea.delete("1.0","end")
    if event.data.endswith(".ptgf") or event.data.endswith(".papx"):
        with open(event.data, "r") as file:
            for line in file:
                line=line.strip()
                textarea.insert("end",f"{line}\n")
        paf.toPaf(event.data, "ptgf")
        print(paf.args)
        print(paf.attacksFrom)
        print(paf.preferences)
    elif event.data.endswith(".tgf") or event.data.endswith(".apx"):
        with open(event.data, "r") as file:
            for line in file:
                line=line.strip()
                textarea.insert("end",f"{line}\n")
        
ws = tkd.TkinterDnD.Tk()
ws.title('PythonGuides')
ws.geometry('700x325')
ws.config(bg='#fcb103')

frame = tk.Frame(ws)
frame.pack()

def ClickReduc1():
    paf.reduction1(["Reduction1-AF-tmp.tgf"], "tgf")
    with open("Reduction1-AF-tmp.tgf","r") as file:
        textareaReduc.delete("1.0", "end")
        for line in file:
            line = line.strip()
            textareaReduc.insert("end", f"{line}\n")

textarea = tk.Text(frame, height=18, width=40)
textarea.pack(side=tk.LEFT)
textarea.drop_target_register(tkd.DND_FILES)
textarea.dnd_bind('<<Drop>>', load_text)

sbv = tk.Scrollbar(frame, orient=tk.VERTICAL)
sbv.pack(side=tk.RIGHT, fill=tk.Y)

textarea.configure(yscrollcommand=sbv.set)
sbv.config(command=textarea.yview)

button = tk.Button(ws, activebackground = "red", bg = "white", text = "reduction 1", command = ClickReduc1)
button.pack(side = tk.BOTTOM)

textareaReduc = tk.Text(frame, height=18, width=40)
textareaReduc.pack(side=tk.LEFT)

ws.mainloop()