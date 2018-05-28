# /usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from cx_Freeze import setup, Executable
import numpy.core._methods
import numpy.lib.format


PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

base = None

if sys.platform[:3] == "win":
    base = "Console"#"Win32GUI"

# ==============================================================================
def shortcut_path_dir():
    if sys.platform[:3] == 'win':
        import winshell
        return winshell.desktop().encode('utf-8')
    else:
        return os.path.expanduser('~')
# ==============================================================================

executables = [Executable("test_33.py",
                          targetName = "kwCalcGQ.exe",
                          base=base, 
                          icon="class_x24.ico", 
                          shortcutName="kwCalcGQ", 
                          shortcutDir=shortcut_path_dir(),
                          copyright='Kavedium Ltd.')]

excludes = ["pyzmq", "zmq", "wxpython", "wx", "tables", "Tkinter", 'logging', 
            'unittest', 'email', 'html', 'http', 'urllib', 'xml', 'unicodedata', 
            'bz2', 'select', 'notebook', 'IPython', 'jupyter', 'pandas', 'PIL', 'sqlite3',
            'tornado']

includes = ['numpy.core._methods',
              "numpy.lib.format",
              "numpy.linalg",
              "numpy.linalg._umath_linalg",
              "numpy.linalg.lapack_lite",
              "scipy.io.matlab.streams",
              "scipy.integrate",
              "scipy.integrate.vode",
              "scipy.integrate.lsoda",
              "scipy.special",
              "scipy.linalg",
              "scipy.special._ufuncs_cxx",
              "scipy.sparse.csgraph._validation",
              "matplotlib.pyplot",
              "matplotlib.backends",
              "matplotlib.backends.backend_qt5agg",]

zip_include_packages = []

include_files = ["antStepClimaData.txt",
                 "ДСТУ-Н Б В.1.1-27_2010.xlsx",
                 "matplotlibrc",
                 "Hack-Regular.ttf",
                 "ww_style.css",
                 "class_x24.ico",
                 "class_x24.png",
                 "splitter.png",
                 "splitter_pressed.png",
                 "splitter_pressed_vertical.png",
                 "splitter_vertical.png",
                 #os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
                 #os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
                ]

options = {
    'build_exe': {
        'include_msvcr': True,
        'excludes': excludes,
        'includes': includes,
        'zip_include_packages': zip_include_packages,
        #'build_exe': 'build_windows',
        'include_files': include_files
    }
}

build_exe_options = {
                     "optimize": 2, 
                     #"create_shared_zip": True, 
                     #"copy_dependent_files": True, 
                     "packages": [], 
                     "include_files" : [
                                        
                                       ], 
                     #"excludes": ["pyzmq",
                     #             "wxpython",
                     #             "tables",
                     #             "zmq",
                     #             "wx",
                     #             "Tkinter"]
                    }

setup(name = u"kwCalcGQ", 
      version = "0.1.0", 
      description = ("Визначення теплових потоків від системи нетрадиційного "
                     "теплопостачання"), 
      executables=executables,
      options = {"build_exe": build_exe_options},
)
