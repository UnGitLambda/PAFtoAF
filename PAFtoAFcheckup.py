# -*- coding: utf-8 -*-
"""
Created in 07/2021

@author: eceya
"""

try:
    import sys
except Exception as e:
    print(str(e))
    print("It seems that the module 'sys' is not installed on your computer (or not accessible via PATH), please install it for PAFtoAF and PAFtoAFGUI to work properly.")
    
assert sys.version_info >= (3,0), "PAFtoAF runs under python 3 or more. To use it please get you version of python up to date."

try:
    import os
except Exception as e:
    print(str(e))
    print("It seems that the module 'os' is not installed on your computer (or not accessible via PATH), please install it for PAFtoAF and PAFtoAFGUI to work properly.")

try:
    import matplotlib
except Exception as e:
    print(str(e))
    print("It seems that the module 'matplotlib' is not installed on your computer (or not accessible via PATH), please install it for PAFtoAFGUI to work properly.")

try:
    import copy
except Exception as e:
    print(str(e))
    print("It seems that the module 'copy' is not installed on your computer (or not accessible via PATH), please install it for PAFtoAF to work properly.")

try:
    import platform
except Exception as e:
    print(str(e))
    print("It seems that the module 'platform', is not installed on your computer (or not accessible via PATH), please installe it for PAFtoAF and PAFtoAFGUI to work properly.")

try:
    import pathlib
except Exception as e:
    print(str(e))
    print("It seems that the module 'pathlib' is not installed on your computer (or not accessible via PATH), please install it for PAFtoAF to work properly.")

try:
    from _io import TextIOWrapper
except Exception as e:
    print(str(e))
    print("It seems that the module '_io' is not installed on your computer (or not accessible via PATH), or has a problem with some class (TextIOWrapper), please (re)install it for PAFtoAF to work properly.")

try:
    import tkinter
except Exception as e:
    print(str(e))
    print("It seems that the module 'tkinter' is not installed on your computer (or not accessible via PATH), please install it for PAFtoAFGUI to work properly.")

try:
    import networkx
except Exception as e:
    print(str(e))
    print("It seems that the module 'networkx' is not installed on your computer (or not accessible via PATH), please install it for PAFtoAFGUI to work properly.")

try:
    import TkinterDnD2
except Exception as e:
    print(str(e))
    print("It seems that the module 'TkinterDnD2' is not installed on your computer (or not accessible via PATH), please install it for PAFtoAFGUI to work properly.")

try:
    import PAFtoAF
except Exception as e:
    print(str(e))
    print("It seems that the 'PAFtoAF.py' file is not in the same directory as this one, please keep all 3 files (PAFtoAF, PAFtoAFGUI and PAFtoAFcheckup) in the same directory for them to work properly.")
    
try:
    import PAFtoAFGUI
except Exception as e:
    print(str(e))
    print("It seems that the 'PAFtoAFGUI.py' file is not in the same directory as this one, please keep all 3 files (PAFtoAF, PAFtoAFGUI and PAFtoAFcheckup) in the same directory for them to work properly.")
    
try:
    import datetime
except Exception as e:
    print(str(e))
    print("It seems that the module 'datetime' is not installed on your computer (or not accessible via PATH), please install it for PAFtoAFGUI to work properly.")