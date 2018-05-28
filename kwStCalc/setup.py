from cx_Freeze import setup, Executable
from numpy._distributor_init import NUMPY_MKL  # requires numpy+mkl
import os
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

import glob
files = glob.glob(os.path.join(PYTHON_INSTALL_DIR, 'Lib', 'site-packages', 
                               'numpy', 'core', '*.dll'))

#exludes = ['email', 'IPython', 'unittest',
#                                  'urllib', 'setuptools', 'sqlite3', 'pygments',
#                                  'pkg_resources', 'psutil', 'pydoc_data',
#                                  'pandas', 'multiprocessing', 'lxml', 'logging',
#                                  'docutils', 'PIL', 'bs4', 'colorama']

additional_mods = ['numpy.core._methods', 'numpy.linalg._umath_linalg',
                   'numpy.lib.format']

build_exe_options = {'packages': ['numpy', 'numpy'], "includes": additional_mods,
                     'include_files': files,
                      "zip_include_packages": "*",
                      "zip_exclude_packages": "openpyxl"}

setup(
    name = "Assignment4_5PythonExe",
    version = "0.1",
    description = "Sort Methods",
    options = {"build_exe": build_exe_options},
    executables = [Executable("kwCalcGQ.py")]
    )