# -*- mode: python -*-

block_cipher = None


a = Analysis(['kwCalcGQ.py'],
             pathex=['C:\\Users\\ichet\\Dropbox\\MyApps\\workspace4.6\\edu_work\\kwStCalc'],
             binaries=[],
             datas=[('antStepClimaData.txt', '.'), ('class_x24.ico', '.'), ('class_x24.png', '.'), ('Hack-Regular.ttf', '.'), ('matplotlibrc', '.'), ('splitter.png', '.'), ('splitter_pressed.png', '.'), ('splitter_pressed_vertical.png', '.'), ('splitter_vertical.png', '.'), ('ww_style.css', '.'), ('DSTU-H_B_V.1.1-27_2010.xlsx', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='kwCalcGQ',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='class_x24.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='kwCalcGQ')
