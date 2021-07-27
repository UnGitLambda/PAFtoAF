# -*- coding: utf-8 -*-
"""
Created in 07/2021

@author: eceya
"""

S = ''

try:
    import sys
except Exception as e:
    print("\nError message :" + str(e) + "\n")
    print("It seems that the module 'sys' is not installed on your computer (or not accessible via PATH), please install it for PAFtoAF and PAFtoAFGUI to work properly.\n")
    print("You should be able to install it using the command :\npython -m pip install sys")
    exit()

try:
    import ctypes
except Exception as e:
    print("\nError message :" + str(e) + "\n")
    print("It seems that the module 'ctypes' is not installed on your computer (or not accessible via PATH), please install it for PAFtoAFcheckup to work properly.\n")
    print("You should be able to install it using the command :\npython -m pip install ctypes")
    sys.exit()

import ctypes  # An included library with Python install.
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)
    
assert sys.version_info >= (3,0), "PAFtoAF runs under python 3 or more. To use it please get you version of python up to date."

try:
    import os
except Exception as e:
    S += "\n"
    S += str(e)
    S += "It seems that the module 'os' is not installed on your computer (or not accessible via PATH), please install it for PAFtoAF and PAFtoAFGUI to work properly.\n"
    S += "You should be able to install it using the command :\npython -m pip install os\n"

try:
    import matplotlib
except Exception as e:
    S += "\n"
    S += "Error message :"
    S += str(e)
    S += "\n"
    S += "It seems that the module 'matplotlib' is not installed on your computer (or not accessible via PATH), please install it for PAFtoAFGUI to work properly."
    S += "You should be able to install it using the command :\npython -m pip install matplotlib\n"

try:
    import copy
except Exception as e:
    S += "\n"
    S += "Error message :"
    S += str(e)
    S += "\n"
    S += "It seems that the module 'copy' is not installed on your computer (or not accessible via PATH), please install it for PAFtoAF to work properly."
    S += "You should be able to install it using the command :\npython -m pip install copy\n"

try:
    import platform
except Exception as e:
    S += "\n"
    S += "Error message :"
    S += str(e)
    S += "\n"
    S += "It seems that the module 'platform', is not installed on your computer (or not accessible via PATH), please installe it for PAFtoAF and PAFtoAFGUI to work properly."
    S += "You should be able to install it using the command :\npython -m pip install platform\n"

try:
    import pathlib
except Exception as e:
    S += "\n"
    S += "Error message :"
    S += str(e)
    S += "\n"
    S += "It seems that the module 'pathlib' is not installed on your computer (or not accessible via PATH), please install it for PAFtoAF to work properly."
    S += "You should be able to install it using the command :\npython -m pip install pathlib\n"

try:
    from _io import TextIOWrapper
except Exception as e:
    S += "\n"
    S += "Error message :"
    S += str(e)
    S += "\n"
    S += "It seems that the module '_io' is not installed on your computer (or not accessible via PATH), or has a problem with some class (TextIOWrapper), please (re)install it for PAFtoAF to work properly."
    S += "You should be able to install it using the command :\npython -m pip install _io\n"
    S += "Or you could consider reinstalling python since this is a base module, your installation might have some problems.\n"

try:
    import tkinter
except Exception as e:
    S += "\n"
    S += "Error message :"
    S += str(e)
    S += "\n"
    S += "It seems that the module 'tkinter' is not installed on your computer (or not accessible via PATH), please install it for PAFtoAFGUI to work properly."
    S += "You should be able to install it using the command :\npython -m pip install tkinter\n"

try:
    import networkx
except Exception as e:
    S += "\n"
    S += "Error message :"
    S += str(e)
    S += "\n"
    S += "It seems that the module 'networkx' is not installed on your computer (or not accessible via PATH), please install it for PAFtoAFGUI to work properly."
    S += "You should be able to install it using the command :\npython -m pip install networkx\n"

try:
    import TkinterDnD2
except Exception as e:
    S += "\n"
    S += str(e)
    S += "It seems that the module 'TkinterDnD2' is not installed on your computer (or not accessible via PATH), please install it for PAFtoAFGUI to work properly."
    S += "You should be able to install it using the command :\npython -m pip install TkinterDnD2\n"

try:
    import PAFtoAF
except Exception as e:
    S += "\n"
    S += "Error message :"
    S += str(e)
    S += "\n"
    S += "It seems that the 'PAFtoAF.py' file is not in the same directory as this one, please keep all 3 files (PAFtoAF, PAFtoAFGUI and PAFtoAFcheckup) in the same directory for them to work properly."
    S += "If you dont have the file anymore you should consider downloading it again at https://github.com/UnHommeLambda/PAFtoAF"

try:
    import PAFtoAFGUI
except Exception as e:
    S += "\n"
    S += "Error message :"
    S += str(e)
    S += "\n"
    S += "It seems that the 'PAFtoAFGUI.py' file is not in the same directory as this one, please keep all 3 files (PAFtoAF, PAFtoAFGUI and PAFtoAFcheckup) in the same directory for them to work properly."
    S += "If you dont have the file anymore you should consider downloading it again at https://github.com/UnHommeLambda/PAFtoAF"

try:
    import datetime
except Exception as e:
    S += "\n"
    S += "Error message :"
    S += str(e)
    S += "\n"
    S += "It seems that the module 'datetime' is not installed on your computer (or not accessible via PATH), please install it for PAFtoAFGUI to work properly."
    S += "You should be able to install it using the command :\npython -m pip install datetime\n"

if S != '':
    print(S)
    Mbox("Error(s)", S, 0)