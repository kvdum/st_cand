# coding: utf-8

from cx_Freeze import setup, Executable

executables = [Executable('example_12.py',
                          targetName='hello_pyqt.exe',
                          base='Win32GUI',
                          icon='class_x24.ico',
                          shortcutName='Hello PyQt5 Application',
                          shortcutDir='ProgramMenuFolder')]

excludes = ['logging', 'unittest', 'email', 'html', 'urllib', 'xml',
            'unicodedata', 'bz2', 'select']

includes = ['json']

zip_include_packages = ['collections', 'encodings', 'importlib', 'PyQt5']

include_files = ['data',
                 'readme.txt',
                 ('documentation.txt', 'doc/doc.txt'),
                 'class_x24.ico'
                ]

options = {
    'build_exe': {
        'include_msvcr': True,
        'excludes': excludes,
        'includes': includes,
        'zip_include_packages': zip_include_packages,
        'include_files': include_files,
    }
}

setup(name="hello_world",
      version='0.0.15',
      description="My Hello World App!",
      executables=executables,
      options=options)