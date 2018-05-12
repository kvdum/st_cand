#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 7.07. 2017.

@author: ichet
'''

import locale
locale.setlocale(locale.LC_ALL, '')

import sys, os, errno
import winpaths
import numpy as np
import sympy as smp
from matplotlib import rcParams, gridspec
rcParams['axes.formatter.use_locale'] = True
import matplotlib.pyplot as plt
from matplotlib.cm import jet

from mpl_toolkits.mplot3d import Axes3D

L = .63
T_pov = 294.15
T_z = 254.15
F_i_ch = .1
lambda_ = 1.2
delta = .3
k = .5
alpha_i_ch = 3.8
c_0 = 5.67 * 10**(-8)
#c_pr = .08#108.3

#H = 1.6

T_pidl = smp.symbols('T_pidl', real=True)

def Tpidl(T_i_ch, H, epsilon):
    '''
    @args: H - scalar
    '''
    c_pr = epsilon * c_0 * (1/(2*np.pi) + 1/(2*np.pi*H))
    eq = c_pr * (T_pidl/100)**4 + lambda_/delta * T_pidl - \
          (k * (T_pov - T_z) + c_pr * (T_i_ch/100)**4 + lambda_/delta * T_z - \
           alpha_i_ch * (T_i_ch - T_pov) * F_i_ch / (H * (H + L)))
    res = smp.solve(eq, T_pidl)
    
    for r in res:
        if r >=0:
            return round(r, 2)

def make_data():
    H = np.array([1.6, 2.2, 2.8, 3.4, 4., 4.6, 5., 5.3, 6.])
    T_i_ch = np.array([693.15, 753.15, 793.15])
    epsilon = np.array([.92, .75, .3])
    T_pidl = {}
    for epsil in epsilon:
        T_pidl[epsil] = \
          np.array([[Tpidl(t_i_ch, h, epsil) for h in H] for t_i_ch in T_i_ch])
    
    return H, T_i_ch, T_pidl

def plot_Tpidl():
    
    H, T_i_ch, T_pidl_list = make_data()
    #T_pidl = T_pidl[.92]
    
    R = 2
    is_print = True
    
    plt.close('all')
    for epsilon, T_pidl in T_pidl_list.items():
        for i in range(4):
            if i < 3:
                if R == 1:
                    if not i:
                        rcParams.update({'font.size': 8, 'axes.titlesize' : 7})
                        fig = plt.figure()
                        gs = gridspec.GridSpec(2, 2) 
                        gs.update(left=0.07, right=0.97, wspace=0.2, top=.95, 
                                  bottom=.05, hspace=.5)
                    ax = plt.subplot(gs[i])
                else:
                    if not i:
                        rcParams.update({'font.size': 10, 'axes.titlesize' : 10, 
                                         'axes.titleweight':'bold'})
                    fig = plt.figure()
                    ax = fig.add_subplot(111)
                    if i in (1, 2):
                        plt.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.05)
                
                plt.plot(H, T_pidl[i])
                plt.title(r'$T_{підл.}$, К при $T_{і.ч.}' + (r' = {}$ К та $\varepsilon' + r' = {}$').\
                          format(T_i_ch[i], epsilon))
                plt.xticks(H)
                plt.xlabel(r'$H$, м')
                plt.ylabel(r'$T_{підл.}$, К')
            else:
                fig = plt.figure()
                ax = Axes3D(fig)
                HH, TT_i_ch = np.meshgrid(H, T_i_ch)
                ax.plot_surface(HH, TT_i_ch, T_pidl, rstride=1, cstride=1, cmap=jet)
                ax.set_title(r'Зміна температури підлоги $T_{підл.}$, К при $\epsilon' + r' = {}$'.\
                             format(epsilon))
                ax.set_xticks(H)
                ax.set_yticks(T_i_ch)
                ax.set_xlabel(r'$H$, м')
                ax.set_ylabel(r'$T_{і.ч.}$, К')
                ax.set_zlabel(r'$T_{підл.}$, К')
                
            ax.grid(True)
            
            if is_print:
                img_name = 'graph_{}__eps_{}.png'.format(i+1, epsilon)
                dir_name = 'st_Tpidls_Num'
                
                if sys.platform == 'win32':
                    winpaths.get_my_documents()
                    path_name = os.path.join(winpaths.get_my_documents(), dir_name)
                else:
                    path_name = os.path.join('/home/kavedium/Documents', dir_name)
                
                if not os.path.exists(path_name):
                    try:
                        os.makedirs(path_name)
                    except OSError as exc: # Guard against race condition
                        if exc.errno != errno.EEXIST:
                            raise
                
                plt.savefig(os.path.join(path_name, img_name), format='png')
        
    plt.show()

if __name__ == '__main__':
    print(make_data()[2])
    plot_Tpidl()
    #print(Tpidl(693.15, 1.6))