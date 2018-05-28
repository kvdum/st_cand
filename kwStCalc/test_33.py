# -*- coding: utf-8 -*-

'''
Created on 9.03.2018.

@author: ichet
@version: 1.2.0

Тема: Визначення теплових потоків від системи нетрадиційного теплопостачання 
(методика Львівського державного аграрного університету)
'''

#import os
import shutil
from enum import Enum
from datetime import datetime
from dashtable import data2rst
import numpy as np

#np.set_printoptions(precision=4)

class TargetGraph(Enum):
    no_showsave = 0
    save = 1
    show = 2
    show_and_save = 3

FLOAT_DEC_4 = '.4f'

def print_table_2(label, array_, row_start=1, fmt=None): 
    print(data2rst([['№ вар.', label], *[[i, v if fmt is None else ('{0:%s}' % fmt)
                                    .format(v)] for i, v in enumerate(array_,
                                                         start=row_start)]],
                                                        center_cells=True))

def print_table_13(label, array_, row_start=1, fmt=None): 
    print(data2rst([[label, '', '', '', '', '', '', '', '', '', '', '', ''],
                    ['№ вар.', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII',
                     'IX', 'X', 'XI', 'XII'],*[[i, *(v if fmt is None else 
        [('{0:%s}' % fmt).format(x) for x in v]) ] for i, v in enumerate(array_,
                                                            start=row_start)]],
                    spans=[ [ [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5],
                              [0, 6], [0, 7], [0, 8], [0, 9], [0, 10], [0, 11],
                              [0, 12] ] ], center_cells=True))

def print_table_12_2(label, array_, fmt=None): 
    print(data2rst([[label, '', '', '', '', '', '', '', '', '', '', ''],
                    ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII',
                     'IX', 'X', 'XI', 'XII'], list(array_) if fmt is None else
                     [('{0:%s}' % fmt).format(v) for v in array_] ],
                    spans=[ [ [0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5],
                              [0, 6], [0, 7], [0, 8], [0, 9], [0, 10], [0, 11] ] ],
                    center_cells=True))

def home_energy_class(Q_e):
    '''Повертає клас енергоспоживання будинку
    '''
    
    if Q_e >= 250: result = 'F'
    elif 150 <= Q_e < 250: result = 'E'
    elif 100 <= Q_e < 150: result = 'D'
    elif 80 <= Q_e < 100: result = 'C'
    elif 45 <= Q_e < 80: result = 'B'
    elif 15 <= Q_e < 45: result = 'A'
    else: result = 'A+'
    
    return result

def get_figure_data():
    return dict(figsize=(12.5, 6), dpi=100)

def get_show_own_frame_params(show_own_frame):
    '''Повертає деякі налаштування вигляду графіків
    '''
    
    if show_own_frame:
        font_size = 14
        ax_titlesize = 14
        ax_pos = (0.12, .14, .8, .72)
        ax_title_y = -.19
        ax_ha = 'right'
    else:
        font_size = 10
        ax_titlesize = 10
        ax_pos = (0.11, .13, .81, .75)
        ax_title_y = -.17
        ax_ha = 'left'
        
    return {'font_size': font_size, 'ax_titlesize': ax_titlesize, 
            'ax_pos': ax_pos, 'ax_title_y': ax_title_y, 'ax_ha': ax_ha}
 
if __name__ == '__main__':
    print('Anton Cheterbok!')
    
    input('Input <Enter> ...')