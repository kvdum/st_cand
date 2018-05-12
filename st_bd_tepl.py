# -*- coding: utf-8 -*-

'''
Created on 21.04.2018.

@author: ichet
'''

import locale
locale.setlocale(locale.LC_ALL, '')

import os
from copy import deepcopy
from datetime import datetime
import shutil
import numpy as np
import math
import sympy as smp

import matplotlib as mpl
from matplotlib import pyplot as plt, rcParams, ticker
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import to_rgb
rcParams['axes.formatter.use_locale'] = True
rcParams.update({'font.family':'serif', 'mathtext.fontset': 'dejavuserif',
                 'font.size': 14, 'axes.titlesize' : 14})

np.set_printoptions(precision=4)

IS_SHOW_GRAF = True
DIRECT_PATH = r'C:\Users\ichet\Dropbox\myDocs\St\bd_tepl'
try:
    # Спочатку видаляється папка.
    shutil.rmtree(DIRECT_PATH)
except FileNotFoundError: pass
os.mkdir(DIRECT_PATH)   # Потім створюється папка.

v = 4.2
alpha_v = 8.7
A_t_z = 19.3
rho = .7
I_max = 657
I_avg = 159

alpha_z_ = 1.16 * (5 + 10*np.sqrt(v))

def nu(R, S):
    #R_1 = R_2 = R_3 = R_4 = R
    #S_1 = S_2 = S_3 = S_4 = S
    
    R_1 = .02 / .81
    R_2 = .51 / .81
    R_3 = R#.15 / .052
    R_4 = .02 / .81
    
    S_1 = 9.76
    S_2 = S#10.12
    S_3 = .82
    S_4 = 9.76
    
    Y_1 = (R_1 * S_1**2 + alpha_v) / (1 + R_1 * alpha_v)
    Y_2 = (R_2 * S_2**2 + Y_1) / (1 + R_2 * Y_1)
    Y_3 = (R_3 * S_3**2 + Y_2) / (1 + R_3 * Y_2)
    Y_4 = (R_4 * S_4**2 + Y_3) / (1 + R_4 * Y_3)
    D = R_1 * S_1 + R_2 * S_2 + R_3 * S_3 + R_4 * S_4
    return .9 * np.exp(D/np.sqrt(2)) * ((S_1 + alpha_v) * (S_2 + Y_1) * 
             (S_3 + Y_2) * (S_4 + Y_3) * (alpha_z_ + Y_4) / ((S_1 + Y_1) * 
             (S_2 + Y_2) * (S_3 + Y_3) * (S_4 + Y_4) * alpha_z_))


#ax.plot_wireframe(R, S, q_max, rstride=1, cstride=1, color='k')

#surf = ax.plot3D(R, S, q_max)#, rstride=1, cstride=1, linewidth=1, 
                       #cmap=mpl.cm.hsv)
#fig.colorbar(surf, shrink=.75, aspect=15)
#ax.set_xlabel(xlabel, x=1, ha="right")
#        ax.set_ylabel(ylabel, y=1.025, va='bottom', rotation=0)
def plot_q_max(R, S):
    fig = plt.figure(figsize=(12.2, 6.8), dpi=80)
    ax = Axes3D(fig)
    ax.view_init(elev=35, azim=75)
    
    R, S = np.meshgrid(r, s)
    nu_result = nu(R, S)
    
    A_tau_z = .5 * A_t_z + rho * (I_max - I_avg) / alpha_z_
    A_tau_v = A_tau_z / nu_result
    
    q_max = alpha_v * A_tau_v
    
    surf = ax.plot_surface(R, S, q_max, rstride=1, cstride=1, lw=2, color='k', 
                           cmap=mpl.cm.hsv)
    cb = fig.colorbar(surf, shrink=.75, aspect=25, anchor=(.7, .35))
    
    ax.xaxis.labelpad = 22
    ax.yaxis.labelpad = 12
    ax.zaxis.labelpad = 5
    ax.set_xlabel(r'$R,\frac{\mathrm{м}^2\cdot{}^\circ \mathrm{C}}{\mathrm{Вт}}$')
    ax.set_ylabel(r'$S,\frac{\mathrm{Вт}}{\mathrm{м}^2\cdot{}^\circ \mathrm{C}}$')
    ax.zaxis.set_rotate_label(False)
    
    #ax.set_zlabel(r'$q_{\mathrm{max}},\frac{\mathrm{Вт}}{\mathrm{м}^2}$', y=.1)#, ha='left')#y=1.1)
    #ax.azim = 225
    ax.set_title(r'Максимальний питомий тепловий потік, $q_{\mathrm{max}},\frac{\mathrm{Вт}}{\mathrm{м}^2}$,' 
                 + '\n' + r'який віддає внутрішня поверхня зовнішьої стіни внутрішньому '
                 r'повітрю при $R = ' + '{}\,\dots\,{}\;'.format(int(R[0, 0]), int(R[-1, -1])) + 
                 r'\frac{\mathrm{м}^2\cdot{}^\circ \mathrm{C}}{\mathrm{Вт}}$', y=1.03)
    ax.set_position([-.10, 0, 1.15, .94])
    plt.savefig(os.path.join(DIRECT_PATH, 'R_yt = {}-{}.png'.format(
        int(R[0, 0]), int(R[-1, -1]))), format='png')
    
    return ax

r = np.linspace(1, 5, 30, endpoint=True)
s = np.linspace(1, 12, 30, endpoint=True)
ax = plot_q_max(r, s)
ax.text(5.6, -1.0, 10.8, r'$q_{\mathrm{max}},\frac{\mathrm{Вт}}{\mathrm{м}^2}$')

r = np.linspace(5, 9, 25)
s = np.linspace(1, 13, 25)
ax = plot_q_max(r, s)
ax.text(9.6, -1.1, 0.9, r'$q_{\mathrm{max}},\frac{\mathrm{Вт}}{\mathrm{м}^2}$')

print(' Роботу завершено! '.center(80, '='))

if IS_SHOW_GRAF:
    plt.show()