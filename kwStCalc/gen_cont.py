# -*- coding: utf-8 -*-
import os
import winshell
import codecs

'''Генерація вмісту NSIS-файлу'''

curent_directory = (r"C:\Users\ichet\YandexDisk\MyApps\MyPreDists\NewDists\kwCalcGQ")

with codecs.open(os.path.join(winshell.desktop(), 'root.txt'), 'w', 'utf-8') as f:
    inst_dir = u"$INSTDIR"
    f.write(u'  SetOutPath "{0}"\n'.format(inst_dir))
    def dircont(dir, inst_path):
        for cont in os.listdir(dir):
            cont = os.path.join(dir, cont)
            if os.path.isfile(cont):
                f.write(u'  File "{0}"\n'.format(cont))
            elif os.path.isdir(cont):
                new_inst_dir = os.path.join(inst_path, os.path.basename(cont))
                f.write(u'  SetOutPath "{0}"\n'.format(new_inst_dir))
                dircont(cont, new_inst_dir)
                f.write(u'  SetOutPath "{0}"\n'.format(inst_path))
            else:
                raise ValueError('Type Error Uses')
                sys.exit()
    dircont(curent_directory, inst_dir)
            
            