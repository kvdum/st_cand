# -*- coding: utf-8 -*-

'''
Created on 20 лист. 2017 р.

@author: ichet
'''

import locale
locale.setlocale(locale.LC_ALL, '')
import os
import numpy as np
from scipy.integrate import odeint
import sympy as smp
import shutil
from datetime import datetime
from matplotlib import pyplot as plt, rcParams, ticker
from matplotlib.colors import to_rgb
rcParams['axes.formatter.use_locale'] = True
rcParams.update({'font.family':'serif', 'mathtext.fontset': 'dejavuserif',
                 'font.size': 14, 'axes.titlesize' : 14})

#smp.init_printing(pretty_print=True, use_unicode=True)

IS_SHOW_GRAF = True
DIRECT_PATH = r'C:\Users\ichet\Dropbox\myDocs\St\Водяні баки акумулятори'
try:
    # Спочатку видаляється папка.
    shutil.rmtree(DIRECT_PATH)
except FileNotFoundError: pass
os.mkdir(DIRECT_PATH)   # Потім створюється папка.

print('Розрахунок проводиться в {}.'.format(datetime.strftime(datetime.now(),
                                                          '%d.%m.%Y %H:%M:%S')))

np.set_printoptions(precision=2)

Nn = range(2, 20+1)
tau = np.linspace(0, 24, 25)#np.linspace(0, 24*30, 31)#np.linspace(0, 24, 25)
calc_divergence = True

fig_data = dict(figsize=(12.2, 6.8), dpi=80)
grid_color = '#ABB2B9'
ax_pos = (0.09, 0.09, 0.88, .75)

if not calc_divergence:
    
    # Кількість секцій бака-акумулятора.
    n = 2
    
    #T_z, c_v, G_k, G_c, T_k_1, T_c_2, K_b, F_b, M, T_b, A_k, A_c = \
    #  smp.symbols('T_z, c_v, G_k, G_c, T_k_1, T_c_2, K_b, F_b, M, T_b, A_k, A_c')
    #print(c_v)
    
    def A_k(i):
        '''Керуюча функція для контуру геліоколектора.
        '''
        return 1 if i-1 < 1 else 0
    
    def A_c(i):
        '''Керуюча функція для контуру споживача.
        '''
        
        return 1 if i+1 > n else 0
    
    def sumA_k(i):
        '''Сумарний результат керуючих функцій для контуру геліоколектора.
        '''
        return sum(A_k(j) for j in range(1, i))
    
    def sumA_c(i):
        '''Сумарний результат керуючих функцій для контуру споживача.
        '''
        
        return sum(A_c(j) for j in range(i+1, n+1))
    
    def dTbi_TopDown(i):
        return 0 if i-1 < 1 else '(T_{}_b(tau) - T_{}_b(tau))'.format(i-1, i)
    
    def Tbi_DownTop(i):
        return 0 if i+1 > n else '(T_{}_b(tau) - T_{}_b(tau))'.format(i+1, i)
    
    eq_right_template = r'M_{i} * c_v * T_{i}_b(tau)'
    eq_left_template = (r'G_k * c_v * ({A_k} * (T_1_k '
                   r'- T_{i}_b(tau)) + {dTbi_TopDown} * {sumA_k}) + G_c * c_v * ({A_c} * '
                   r'(T_2_c - T_{i}_b(tau)) + {Tbi_DownTop} * {sumA_c}) + 3.6 * '
                   r'K_{i}_b * F_{i}_b * (T_n - T_{i}_b(tau))')
    T_tau_template = r'T_{i}_b(tau)'
    eqs = []
    #T_tau_list = []
    tau = smp.Symbol('tau')
    for i in range(1, n+1):
        eq_left = smp.S(eq_left_template.format(i=i, A_k=A_k(i), dTbi_TopDown=dTbi_TopDown(i), 
                                      sumA_k=sumA_k(i), A_c=A_c(i), 
                                      Tbi_DownTop=Tbi_DownTop(i), sumA_c=sumA_c(i)) )
        eq_right = smp.S(eq_right_template.format(i=i))
        eq = smp.Eq(eq_left, eq_right.diff(tau))
        ##T_tau = smp.Function(T_tau_template.format(i=i))
        #T_tau_list.append(T_tau)
        smp.pretty_print(eq)
        eqs.append(eq)
    
    if n == 99:
        rhs = []
        for req in smp.dsolve(eqs):
            print(req)
            rhs.append(smp.Eq(req.rhs.subs(tau, 0), 15))
        print(" Розв'язок задачі Коші: ".center(50, '-'))
        C1, C2, C3 = smp.symbol('C1 C2 C3')
        print(smp.solve(rhs), [C1, C2, C3])
        
        #smp.pretty_print()
        
        print("Розв'язок символьним (аналітичним) методом завершено!")
        raise SystemExit(0)
    
    print(" Ров'язок числовими методами для n = {} ".format(n).center(50, '-'))
    
def f2(T, tau):
    '''Для двохсекційного баку
    '''
    
    T_1_b, T_2_b = T  # Імена шуканих функцій.
    return [1/(M_1*c_v) * ( 3.6*F_1_b*K_1_b*(T_n - T_1_b) + G_c*c_v*(T_2_b - T_1_b)
                            + G_k * c_v * (T_1_k - T_1_b) ),
            1/(M_2*c_v) * ( 3.6*F_2_b*K_2_b*(T_n - T_2_b) + G_c*c_v*(T_2_c - T_2_b)
                            + G_k * c_v * (T_1_b - T_2_b) )
            ]

def f3(T, tau):
    '''Для трисекційного баку
    '''
    
    T_1_b, T_2_b, T_3_b = T  # Імена шуканих функцій.
    return [1/(M_1*c_v) * ( 3.6*F_1_b*K_1_b*(T_n - T_1_b) + G_c*c_v*(T_2_b - T_1_b) 
                            + G_k*c_v*(T_1_k - T_1_b) ),
            1/(M_2*c_v) * ( 3.6*F_2_b*K_2_b*(T_n - T_2_b) + G_c*c_v*(T_3_b - T_2_b)
                            + G_k*c_v*(T_1_b - T_2_b) ),
            1/(M_3*c_v) * ( 3.6*F_3_b*K_3_b*(T_n - T_3_b) + G_c*c_v*(T_2_c - T_3_b)
                            + G_k*c_v*(T_2_b - T_3_b) )
            ]

def f4(T, tau):
    '''Для чотирисекційного баку
    '''
    
    T_1_b, T_2_b, T_3_b, T_4_b = T  # Імена шуканих функцій.
    return [1/(M_1*c_v) * ( 3.6*F_1_b*K_1_b*(T_n - T_1_b) + G_c*c_v*(T_2_b - T_1_b)
                            + G_k*c_v*(T_1_k - T_1_b) ),
            1/(M_2*c_v) * ( 3.6*F_2_b*K_2_b*(T_n - T_2_b) + G_c*c_v*(T_3_b - T_2_b)
                            + G_k*c_v*(T_1_b - T_2_b) ),
            1/(M_3*c_v) * ( 3.6*F_3_b*K_3_b*(T_n - T_3_b) + G_c*c_v*(T_4_b - T_3_b)
                            + G_k*c_v*(T_2_b - T_3_b) ),
            1/(M_4*c_v) * ( 3.6*F_4_b*K_4_b*(T_n - T_4_b) + G_c*c_v*(T_2_c - T_4_b)
                            + G_k*c_v*(T_3_b - T_4_b) )
            ]

def f5(T, tau):
    '''Для п'ятисекційного баку
    '''
    
    T_1_b, T_2_b, T_3_b, T_4_b, T_5_b = T  # Імена шуканих функцій.
    return [1/(M_1*c_v) * ( 3.6*F_1_b*K_1_b*(T_n - T_1_b) + G_c*c_v*(T_2_b - T_1_b)
                            + G_k*c_v*(T_1_k - T_1_b) ),
            1/(M_2*c_v) * ( 3.6*F_2_b*K_2_b*(T_n - T_2_b) + G_c*c_v*(T_3_b - T_2_b)
                            + G_k*c_v*(T_1_b - T_2_b) ),
            1/(M_3*c_v) * ( 3.6*F_3_b*K_3_b*(T_n - T_3_b) + G_c*c_v*(T_4_b - T_3_b)
                            + G_k*c_v*(T_2_b - T_3_b) ),
            1/(M_4*c_v) * ( 3.6*F_4_b*K_4_b*(T_n - T_4_b) + G_c*c_v*(T_5_b - T_4_b)
                            + G_k*c_v*(T_3_b - T_4_b) ),
            1/(M_5*c_v) * ( 3.6*F_5_b*K_5_b*(T_n - T_5_b) + G_c*c_v*(T_2_c - T_5_b)
                            + G_k*c_v*(T_4_b - T_5_b) )
            ]
def f6(T, tau):
    '''Для шестисекційного баку
    '''
    
    T_1_b, T_2_b, T_3_b, T_4_b, T_5_b, T_6_b = T  # Імена шуканих функцій.
    return [1/(M_1*c_v) * ( 3.6*F_1_b*K_1_b*(T_n - T_1_b) + G_c*c_v*(T_2_b - T_1_b)
                            + G_k*c_v*(T_1_k - T_1_b) ),
            1/(M_2*c_v) * ( 3.6*F_2_b*K_2_b*(T_n - T_2_b) + G_c*c_v*(T_3_b - T_2_b)
                            + G_k*c_v*(T_1_b - T_2_b) ),
            1/(M_3*c_v) * ( 3.6*F_3_b*K_3_b*(T_n - T_3_b) + G_c*c_v*(T_4_b - T_3_b)
                            + G_k*c_v*(T_2_b - T_3_b) ),
            1/(M_4*c_v) * ( 3.6*F_4_b*K_4_b*(T_n - T_4_b) + G_c*c_v*(T_5_b - T_4_b)
                            + G_k*c_v*(T_3_b - T_4_b) ),
            1/(M_5*c_v) * ( 3.6*F_5_b*K_5_b*(T_n - T_5_b) + G_c*c_v*(T_6_b - T_5_b)
                            + G_k*c_v*(T_4_b - T_5_b) ),
            1/(M_6*c_v) * ( 3.6*F_6_b*K_6_b*(T_n - T_6_b) + G_c*c_v*(T_2_c - T_6_b)
                            + G_k*c_v*(T_5_b - T_6_b) )
            ]

def f7(T, tau):
    '''Для семисекційного баку
    '''
    
    T_1_b, T_2_b, T_3_b, T_4_b, T_5_b, T_6_b, T_7_b = T  # Імена шуканих функцій.
    return [1/(M_1*c_v) * ( 3.6*F_1_b*K_1_b*(T_n - T_1_b) + G_c*c_v*(T_2_b - T_1_b)
                            + G_k*c_v*(T_1_k - T_1_b) ),
            1/(M_2*c_v) * ( 3.6*F_2_b*K_2_b*(T_n - T_2_b) + G_c*c_v*(T_3_b - T_2_b)
                            + G_k*c_v*(T_1_b - T_2_b) ),
            1/(M_3*c_v) * ( 3.6*F_3_b*K_3_b*(T_n - T_3_b) + G_c*c_v*(T_4_b - T_3_b)
                            + G_k*c_v*(T_2_b - T_3_b) ),
            1/(M_4*c_v) * ( 3.6*F_4_b*K_4_b*(T_n - T_4_b) + G_c*c_v*(T_5_b - T_4_b)
                            + G_k*c_v*(T_3_b - T_4_b) ),
            1/(M_5*c_v) * ( 3.6*F_5_b*K_5_b*(T_n - T_5_b) + G_c*c_v*(T_6_b - T_5_b)
                            + G_k*c_v*(T_4_b - T_5_b) ),
            1/(M_6*c_v) * ( 3.6*F_6_b*K_6_b*(T_n - T_6_b) + G_c*c_v*(T_7_b - T_6_b)
                            + G_k*c_v*(T_5_b - T_6_b) ),
            1/(M_7*c_v) * ( 3.6*F_7_b*K_7_b*(T_n - T_7_b) + G_c*c_v*(T_2_c - T_7_b)
                            + G_k*c_v*(T_6_b - T_7_b) )
            ]

def f8(T, tau):
    '''Для восьмисекційного баку
    '''
    
    T_1_b, T_2_b, T_3_b, T_4_b, T_5_b, T_6_b, T_7_b, T_8_b = T  # Імена шуканих функцій.
    return [1/(M_1*c_v) * ( 3.6*F_1_b*K_1_b*(T_n - T_1_b) + G_c*c_v*(T_2_b - T_1_b)
                            + G_k*c_v*(T_1_k - T_1_b) ),
            1/(M_2*c_v) * ( 3.6*F_2_b*K_2_b*(T_n - T_2_b) + G_c*c_v*(T_3_b - T_2_b)
                            + G_k*c_v*(T_1_b - T_2_b) ),
            1/(M_3*c_v) * ( 3.6*F_3_b*K_3_b*(T_n - T_3_b) + G_c*c_v*(T_4_b - T_3_b)
                            + G_k*c_v*(T_2_b - T_3_b) ),
            1/(M_4*c_v) * ( 3.6*F_4_b*K_4_b*(T_n - T_4_b) + G_c*c_v*(T_5_b - T_4_b)
                            + G_k*c_v*(T_3_b - T_4_b) ),
            1/(M_5*c_v) * ( 3.6*F_5_b*K_5_b*(T_n - T_5_b) + G_c*c_v*(T_6_b - T_5_b)
                            + G_k*c_v*(T_4_b - T_5_b) ),
            1/(M_6*c_v) * ( 3.6*F_6_b*K_6_b*(T_n - T_6_b) + G_c*c_v*(T_7_b - T_6_b)
                            + G_k*c_v*(T_5_b - T_6_b) ),
            1/(M_7*c_v) * ( 3.6*F_7_b*K_7_b*(T_n - T_7_b) + G_c*c_v*(T_8_b - T_7_b)
                            + G_k*c_v*(T_6_b - T_7_b) ),
            1/(M_8*c_v) * ( 3.6*F_8_b*K_8_b*(T_n - T_8_b) + G_c*c_v*(T_2_c - T_8_b)
                            + G_k*c_v*(T_7_b - T_8_b) )
            ]

def f9(T, tau):
    '''Для дев'ятисекційного баку
    '''
    
    T_1_b, T_2_b, T_3_b, T_4_b, T_5_b, T_6_b, T_7_b, T_8_b, T_9_b = T  # Імена шуканих функцій.
    return [1/(M_1*c_v) * ( 3.6*F_1_b*K_1_b*(T_n - T_1_b) + G_c*c_v*(T_2_b - T_1_b)
                            + G_k*c_v*(T_1_k - T_1_b) ),
            1/(M_2*c_v) * ( 3.6*F_2_b*K_2_b*(T_n - T_2_b) + G_c*c_v*(T_3_b - T_2_b)
                            + G_k*c_v*(T_1_b - T_2_b) ),
            1/(M_3*c_v) * ( 3.6*F_3_b*K_3_b*(T_n - T_3_b) + G_c*c_v*(T_4_b - T_3_b)
                            + G_k*c_v*(T_2_b - T_3_b) ),
            1/(M_4*c_v) * ( 3.6*F_4_b*K_4_b*(T_n - T_4_b) + G_c*c_v*(T_5_b - T_4_b)
                            + G_k*c_v*(T_3_b - T_4_b) ),
            1/(M_5*c_v) * ( 3.6*F_5_b*K_5_b*(T_n - T_5_b) + G_c*c_v*(T_6_b - T_5_b)
                            + G_k*c_v*(T_4_b - T_5_b) ),
            1/(M_6*c_v) * ( 3.6*F_6_b*K_6_b*(T_n - T_6_b) + G_c*c_v*(T_7_b - T_6_b)
                            + G_k*c_v*(T_5_b - T_6_b) ),
            1/(M_7*c_v) * ( 3.6*F_7_b*K_7_b*(T_n - T_7_b) + G_c*c_v*(T_8_b - T_7_b)
                            + G_k*c_v*(T_6_b - T_7_b) ),
            1/(M_8*c_v) * ( 3.6*F_8_b*K_8_b*(T_n - T_8_b) + G_c*c_v*(T_9_b - T_8_b)
                            + G_k*c_v*(T_7_b - T_8_b) ),
            1/(M_9*c_v) * ( 3.6*F_9_b*K_9_b*(T_n - T_9_b) + G_c*c_v*(T_2_c - T_9_b)
                            + G_k*c_v*(T_8_b - T_9_b) )
            ]

def f10(T, tau):
    '''Для дев'ятисекційного баку
    '''
    
    T_1_b, T_2_b, T_3_b, T_4_b, T_5_b, T_6_b, T_7_b, T_8_b, T_9_b, T_10_b = T  # Імена шуканих функцій.
    return [1/(M_1*c_v) * ( 3.6*F_1_b*K_1_b*(T_n - T_1_b) + G_c*c_v*(T_2_b - T_1_b)
                            + G_k*c_v*(T_1_k - T_1_b) ),
            1/(M_2*c_v) * ( 3.6*F_2_b*K_2_b*(T_n - T_2_b) + G_c*c_v*(T_3_b - T_2_b)
                            + G_k*c_v*(T_1_b - T_2_b) ),
            1/(M_3*c_v) * ( 3.6*F_3_b*K_3_b*(T_n - T_3_b) + G_c*c_v*(T_4_b - T_3_b)
                            + G_k*c_v*(T_2_b - T_3_b) ),
            1/(M_4*c_v) * ( 3.6*F_4_b*K_4_b*(T_n - T_4_b) + G_c*c_v*(T_5_b - T_4_b)
                            + G_k*c_v*(T_3_b - T_4_b) ),
            1/(M_5*c_v) * ( 3.6*F_5_b*K_5_b*(T_n - T_5_b) + G_c*c_v*(T_6_b - T_5_b)
                            + G_k*c_v*(T_4_b - T_5_b) ),
            1/(M_6*c_v) * ( 3.6*F_6_b*K_6_b*(T_n - T_6_b) + G_c*c_v*(T_7_b - T_6_b)
                            + G_k*c_v*(T_5_b - T_6_b) ),
            1/(M_7*c_v) * ( 3.6*F_7_b*K_7_b*(T_n - T_7_b) + G_c*c_v*(T_8_b - T_7_b)
                            + G_k*c_v*(T_6_b - T_7_b) ),
            1/(M_8*c_v) * ( 3.6*F_8_b*K_8_b*(T_n - T_8_b) + G_c*c_v*(T_9_b - T_8_b)
                            + G_k*c_v*(T_7_b - T_8_b) ),
            1/(M_9*c_v) * ( 3.6*F_9_b*K_9_b*(T_n - T_9_b) + G_c*c_v*(T_10_b - T_9_b)
                            + G_k*c_v*(T_8_b - T_9_b) ),
            1/(M_10*c_v) * ( 3.6*F_10_b*K_10_b*(T_n - T_10_b) + G_c*c_v*(T_2_c - T_10_b)
                            + G_k*c_v*(T_9_b - T_10_b) )
            ]

def f11(T, tau):
    '''Для дев'ятисекційного баку
    '''
    
    T_1_b, T_2_b, T_3_b, T_4_b, T_5_b, T_6_b, T_7_b, T_8_b, T_9_b, T_10_b,  T_11_b = T  # Імена шуканих функцій.
    return [1/(M_1*c_v) * ( 3.6*F_1_b*K_1_b*(T_n - T_1_b) + G_c*c_v*(T_2_b - T_1_b)
                            + G_k*c_v*(T_1_k - T_1_b) ),
            1/(M_2*c_v) * ( 3.6*F_2_b*K_2_b*(T_n - T_2_b) + G_c*c_v*(T_3_b - T_2_b)
                            + G_k*c_v*(T_1_b - T_2_b) ),
            1/(M_3*c_v) * ( 3.6*F_3_b*K_3_b*(T_n - T_3_b) + G_c*c_v*(T_4_b - T_3_b)
                            + G_k*c_v*(T_2_b - T_3_b) ),
            1/(M_4*c_v) * ( 3.6*F_4_b*K_4_b*(T_n - T_4_b) + G_c*c_v*(T_5_b - T_4_b)
                            + G_k*c_v*(T_3_b - T_4_b) ),
            1/(M_5*c_v) * ( 3.6*F_5_b*K_5_b*(T_n - T_5_b) + G_c*c_v*(T_6_b - T_5_b)
                            + G_k*c_v*(T_4_b - T_5_b) ),
            1/(M_6*c_v) * ( 3.6*F_6_b*K_6_b*(T_n - T_6_b) + G_c*c_v*(T_7_b - T_6_b)
                            + G_k*c_v*(T_5_b - T_6_b) ),
            1/(M_7*c_v) * ( 3.6*F_7_b*K_7_b*(T_n - T_7_b) + G_c*c_v*(T_8_b - T_7_b)
                            + G_k*c_v*(T_6_b - T_7_b) ),
            1/(M_8*c_v) * ( 3.6*F_8_b*K_8_b*(T_n - T_8_b) + G_c*c_v*(T_9_b - T_8_b)
                            + G_k*c_v*(T_7_b - T_8_b) ),
            1/(M_9*c_v) * ( 3.6*F_9_b*K_9_b*(T_n - T_9_b) + G_c*c_v*(T_10_b - T_9_b)
                            + G_k*c_v*(T_8_b - T_9_b) ),
            1/(M_10*c_v) * ( 3.6*F_10_b*K_10_b*(T_n - T_10_b) + G_c*c_v*(T_11_b - T_10_b)
                            + G_k*c_v*(T_9_b - T_10_b) ),
            1/(M_11*c_v) * ( 3.6*F_11_b*K_11_b*(T_n - T_11_b) + G_c*c_v*(T_2_c - T_11_b)
                            + G_k*c_v*(T_10_b - T_11_b) )
            ]

def f12(T, tau):
    '''Для дев'ятисекційного баку
    '''
    
    T_1_b, T_2_b, T_3_b, T_4_b, T_5_b, T_6_b, T_7_b, T_8_b, T_9_b, T_10_b,  T_11_b,  T_12_b = T  # Імена шуканих функцій.
    return [1/(M_1*c_v) * ( 3.6*F_1_b*K_1_b*(T_n - T_1_b) + G_c*c_v*(T_2_b - T_1_b)
                            + G_k*c_v*(T_1_k - T_1_b) ),
            1/(M_2*c_v) * ( 3.6*F_2_b*K_2_b*(T_n - T_2_b) + G_c*c_v*(T_3_b - T_2_b)
                            + G_k*c_v*(T_1_b - T_2_b) ),
            1/(M_3*c_v) * ( 3.6*F_3_b*K_3_b*(T_n - T_3_b) + G_c*c_v*(T_4_b - T_3_b)
                            + G_k*c_v*(T_2_b - T_3_b) ),
            1/(M_4*c_v) * ( 3.6*F_4_b*K_4_b*(T_n - T_4_b) + G_c*c_v*(T_5_b - T_4_b)
                            + G_k*c_v*(T_3_b - T_4_b) ),
            1/(M_5*c_v) * ( 3.6*F_5_b*K_5_b*(T_n - T_5_b) + G_c*c_v*(T_6_b - T_5_b)
                            + G_k*c_v*(T_4_b - T_5_b) ),
            1/(M_6*c_v) * ( 3.6*F_6_b*K_6_b*(T_n - T_6_b) + G_c*c_v*(T_7_b - T_6_b)
                            + G_k*c_v*(T_5_b - T_6_b) ),
            1/(M_7*c_v) * ( 3.6*F_7_b*K_7_b*(T_n - T_7_b) + G_c*c_v*(T_8_b - T_7_b)
                            + G_k*c_v*(T_6_b - T_7_b) ),
            1/(M_8*c_v) * ( 3.6*F_8_b*K_8_b*(T_n - T_8_b) + G_c*c_v*(T_9_b - T_8_b)
                            + G_k*c_v*(T_7_b - T_8_b) ),
            1/(M_9*c_v) * ( 3.6*F_9_b*K_9_b*(T_n - T_9_b) + G_c*c_v*(T_10_b - T_9_b)
                            + G_k*c_v*(T_8_b - T_9_b) ),
            1/(M_10*c_v) * ( 3.6*F_10_b*K_10_b*(T_n - T_10_b) + G_c*c_v*(T_11_b - T_10_b)
                            + G_k*c_v*(T_9_b - T_10_b) ),
            1/(M_11*c_v) * ( 3.6*F_11_b*K_11_b*(T_n - T_11_b) + G_c*c_v*(T_12_b - T_11_b)
                            + G_k*c_v*(T_10_b - T_11_b) ),
            1/(M_12*c_v) * ( 3.6*F_12_b*K_12_b*(T_n - T_12_b) + G_c*c_v*(T_2_c - T_12_b)
                            + G_k*c_v*(T_11_b - T_12_b) )
            ]

def f13(T, tau):
    '''Для дев'ятисекційного баку
    '''
    
    T_1_b, T_2_b, T_3_b, T_4_b, T_5_b, T_6_b, T_7_b, T_8_b, T_9_b, T_10_b,  T_11_b,  T_12_b,  T_13_b = T  # Імена шуканих функцій.
    return [1/(M_1*c_v) * ( 3.6*F_1_b*K_1_b*(T_n - T_1_b) + G_c*c_v*(T_2_b - T_1_b)
                            + G_k*c_v*(T_1_k - T_1_b) ),
            1/(M_2*c_v) * ( 3.6*F_2_b*K_2_b*(T_n - T_2_b) + G_c*c_v*(T_3_b - T_2_b)
                            + G_k*c_v*(T_1_b - T_2_b) ),
            1/(M_3*c_v) * ( 3.6*F_3_b*K_3_b*(T_n - T_3_b) + G_c*c_v*(T_4_b - T_3_b)
                            + G_k*c_v*(T_2_b - T_3_b) ),
            1/(M_4*c_v) * ( 3.6*F_4_b*K_4_b*(T_n - T_4_b) + G_c*c_v*(T_5_b - T_4_b)
                            + G_k*c_v*(T_3_b - T_4_b) ),
            1/(M_5*c_v) * ( 3.6*F_5_b*K_5_b*(T_n - T_5_b) + G_c*c_v*(T_6_b - T_5_b)
                            + G_k*c_v*(T_4_b - T_5_b) ),
            1/(M_6*c_v) * ( 3.6*F_6_b*K_6_b*(T_n - T_6_b) + G_c*c_v*(T_7_b - T_6_b)
                            + G_k*c_v*(T_5_b - T_6_b) ),
            1/(M_7*c_v) * ( 3.6*F_7_b*K_7_b*(T_n - T_7_b) + G_c*c_v*(T_8_b - T_7_b)
                            + G_k*c_v*(T_6_b - T_7_b) ),
            1/(M_8*c_v) * ( 3.6*F_8_b*K_8_b*(T_n - T_8_b) + G_c*c_v*(T_9_b - T_8_b)
                            + G_k*c_v*(T_7_b - T_8_b) ),
            1/(M_9*c_v) * ( 3.6*F_9_b*K_9_b*(T_n - T_9_b) + G_c*c_v*(T_10_b - T_9_b)
                            + G_k*c_v*(T_8_b - T_9_b) ),
            1/(M_10*c_v) * ( 3.6*F_10_b*K_10_b*(T_n - T_10_b) + G_c*c_v*(T_11_b - T_10_b)
                            + G_k*c_v*(T_9_b - T_10_b) ),
            1/(M_11*c_v) * ( 3.6*F_11_b*K_11_b*(T_n - T_11_b) + G_c*c_v*(T_12_b - T_11_b)
                            + G_k*c_v*(T_10_b - T_11_b) ),
            1/(M_12*c_v) * ( 3.6*F_12_b*K_12_b*(T_n - T_12_b) + G_c*c_v*(T_13_b - T_12_b)
                            + G_k*c_v*(T_11_b - T_12_b) ),
            1/(M_13*c_v) * ( 3.6*F_13_b*K_13_b*(T_n - T_13_b) + G_c*c_v*(T_2_c - T_13_b)
                            + G_k*c_v*(T_12_b - T_13_b) )
            ]

def f14(T, tau):
    '''Для дев'ятисекційного баку
    '''
    
    T_1_b, T_2_b, T_3_b, T_4_b, T_5_b, T_6_b, T_7_b, T_8_b, T_9_b, T_10_b,  T_11_b,  T_12_b,  T_13_b,  T_14_b = T  # Імена шуканих функцій.
    return [1/(M_1*c_v) * ( 3.6*F_1_b*K_1_b*(T_n - T_1_b) + G_c*c_v*(T_2_b - T_1_b)
                            + G_k*c_v*(T_1_k - T_1_b) ),
            1/(M_2*c_v) * ( 3.6*F_2_b*K_2_b*(T_n - T_2_b) + G_c*c_v*(T_3_b - T_2_b)
                            + G_k*c_v*(T_1_b - T_2_b) ),
            1/(M_3*c_v) * ( 3.6*F_3_b*K_3_b*(T_n - T_3_b) + G_c*c_v*(T_4_b - T_3_b)
                            + G_k*c_v*(T_2_b - T_3_b) ),
            1/(M_4*c_v) * ( 3.6*F_4_b*K_4_b*(T_n - T_4_b) + G_c*c_v*(T_5_b - T_4_b)
                            + G_k*c_v*(T_3_b - T_4_b) ),
            1/(M_5*c_v) * ( 3.6*F_5_b*K_5_b*(T_n - T_5_b) + G_c*c_v*(T_6_b - T_5_b)
                            + G_k*c_v*(T_4_b - T_5_b) ),
            1/(M_6*c_v) * ( 3.6*F_6_b*K_6_b*(T_n - T_6_b) + G_c*c_v*(T_7_b - T_6_b)
                            + G_k*c_v*(T_5_b - T_6_b) ),
            1/(M_7*c_v) * ( 3.6*F_7_b*K_7_b*(T_n - T_7_b) + G_c*c_v*(T_8_b - T_7_b)
                            + G_k*c_v*(T_6_b - T_7_b) ),
            1/(M_8*c_v) * ( 3.6*F_8_b*K_8_b*(T_n - T_8_b) + G_c*c_v*(T_9_b - T_8_b)
                            + G_k*c_v*(T_7_b - T_8_b) ),
            1/(M_9*c_v) * ( 3.6*F_9_b*K_9_b*(T_n - T_9_b) + G_c*c_v*(T_10_b - T_9_b)
                            + G_k*c_v*(T_8_b - T_9_b) ),
            1/(M_10*c_v) * ( 3.6*F_10_b*K_10_b*(T_n - T_10_b) + G_c*c_v*(T_11_b - T_10_b)
                            + G_k*c_v*(T_9_b - T_10_b) ),
            1/(M_11*c_v) * ( 3.6*F_11_b*K_11_b*(T_n - T_11_b) + G_c*c_v*(T_12_b - T_11_b)
                            + G_k*c_v*(T_10_b - T_11_b) ),
            1/(M_12*c_v) * ( 3.6*F_12_b*K_12_b*(T_n - T_12_b) + G_c*c_v*(T_13_b - T_12_b)
                            + G_k*c_v*(T_11_b - T_12_b) ),
            1/(M_13*c_v) * ( 3.6*F_13_b*K_13_b*(T_n - T_13_b) + G_c*c_v*(T_14_b - T_13_b)
                            + G_k*c_v*(T_12_b - T_13_b) ),
            1/(M_14*c_v) * ( 3.6*F_14_b*K_14_b*(T_n - T_14_b) + G_c*c_v*(T_2_c - T_14_b)
                            + G_k*c_v*(T_13_b - T_14_b) )
            ]

def f15(T, tau):
    '''Для дев'ятисекційного баку
    '''
    
    T_1_b, T_2_b, T_3_b, T_4_b, T_5_b, T_6_b, T_7_b, T_8_b, T_9_b, T_10_b,  T_11_b,  T_12_b,  T_13_b,  T_14_b,  T_15_b = T  # Імена шуканих функцій.
    return [1/(M_1*c_v) * ( 3.6*F_1_b*K_1_b*(T_n - T_1_b) + G_c*c_v*(T_2_b - T_1_b)
                            + G_k*c_v*(T_1_k - T_1_b) ),
            1/(M_2*c_v) * ( 3.6*F_2_b*K_2_b*(T_n - T_2_b) + G_c*c_v*(T_3_b - T_2_b)
                            + G_k*c_v*(T_1_b - T_2_b) ),
            1/(M_3*c_v) * ( 3.6*F_3_b*K_3_b*(T_n - T_3_b) + G_c*c_v*(T_4_b - T_3_b)
                            + G_k*c_v*(T_2_b - T_3_b) ),
            1/(M_4*c_v) * ( 3.6*F_4_b*K_4_b*(T_n - T_4_b) + G_c*c_v*(T_5_b - T_4_b)
                            + G_k*c_v*(T_3_b - T_4_b) ),
            1/(M_5*c_v) * ( 3.6*F_5_b*K_5_b*(T_n - T_5_b) + G_c*c_v*(T_6_b - T_5_b)
                            + G_k*c_v*(T_4_b - T_5_b) ),
            1/(M_6*c_v) * ( 3.6*F_6_b*K_6_b*(T_n - T_6_b) + G_c*c_v*(T_7_b - T_6_b)
                            + G_k*c_v*(T_5_b - T_6_b) ),
            1/(M_7*c_v) * ( 3.6*F_7_b*K_7_b*(T_n - T_7_b) + G_c*c_v*(T_8_b - T_7_b)
                            + G_k*c_v*(T_6_b - T_7_b) ),
            1/(M_8*c_v) * ( 3.6*F_8_b*K_8_b*(T_n - T_8_b) + G_c*c_v*(T_9_b - T_8_b)
                            + G_k*c_v*(T_7_b - T_8_b) ),
            1/(M_9*c_v) * ( 3.6*F_9_b*K_9_b*(T_n - T_9_b) + G_c*c_v*(T_10_b - T_9_b)
                            + G_k*c_v*(T_8_b - T_9_b) ),
            1/(M_10*c_v) * ( 3.6*F_10_b*K_10_b*(T_n - T_10_b) + G_c*c_v*(T_11_b - T_10_b)
                            + G_k*c_v*(T_9_b - T_10_b) ),
            1/(M_11*c_v) * ( 3.6*F_11_b*K_11_b*(T_n - T_11_b) + G_c*c_v*(T_12_b - T_11_b)
                            + G_k*c_v*(T_10_b - T_11_b) ),
            1/(M_12*c_v) * ( 3.6*F_12_b*K_12_b*(T_n - T_12_b) + G_c*c_v*(T_13_b - T_12_b)
                            + G_k*c_v*(T_11_b - T_12_b) ),
            1/(M_13*c_v) * ( 3.6*F_13_b*K_13_b*(T_n - T_13_b) + G_c*c_v*(T_14_b - T_13_b)
                            + G_k*c_v*(T_12_b - T_13_b) ),
            1/(M_14*c_v) * ( 3.6*F_14_b*K_14_b*(T_n - T_14_b) + G_c*c_v*(T_15_b - T_14_b)
                            + G_k*c_v*(T_13_b - T_14_b) ),
            1/(M_15*c_v) * ( 3.6*F_15_b*K_15_b*(T_n - T_15_b) + G_c*c_v*(T_2_c - T_15_b)
                            + G_k*c_v*(T_14_b - T_15_b) )
            ]

def f16(T, tau):
    '''Для дев'ятисекційного баку
    '''
    
    T_1_b, T_2_b, T_3_b, T_4_b, T_5_b, T_6_b, T_7_b, T_8_b, T_9_b, T_10_b,  T_11_b,  T_12_b,  T_13_b,  T_14_b,  T_15_b,  T_16_b = T  # Імена шуканих функцій.
    return [1/(M_1*c_v) * ( 3.6*F_1_b*K_1_b*(T_n - T_1_b) + G_c*c_v*(T_2_b - T_1_b)
                            + G_k*c_v*(T_1_k - T_1_b) ),
            1/(M_2*c_v) * ( 3.6*F_2_b*K_2_b*(T_n - T_2_b) + G_c*c_v*(T_3_b - T_2_b)
                            + G_k*c_v*(T_1_b - T_2_b) ),
            1/(M_3*c_v) * ( 3.6*F_3_b*K_3_b*(T_n - T_3_b) + G_c*c_v*(T_4_b - T_3_b)
                            + G_k*c_v*(T_2_b - T_3_b) ),
            1/(M_4*c_v) * ( 3.6*F_4_b*K_4_b*(T_n - T_4_b) + G_c*c_v*(T_5_b - T_4_b)
                            + G_k*c_v*(T_3_b - T_4_b) ),
            1/(M_5*c_v) * ( 3.6*F_5_b*K_5_b*(T_n - T_5_b) + G_c*c_v*(T_6_b - T_5_b)
                            + G_k*c_v*(T_4_b - T_5_b) ),
            1/(M_6*c_v) * ( 3.6*F_6_b*K_6_b*(T_n - T_6_b) + G_c*c_v*(T_7_b - T_6_b)
                            + G_k*c_v*(T_5_b - T_6_b) ),
            1/(M_7*c_v) * ( 3.6*F_7_b*K_7_b*(T_n - T_7_b) + G_c*c_v*(T_8_b - T_7_b)
                            + G_k*c_v*(T_6_b - T_7_b) ),
            1/(M_8*c_v) * ( 3.6*F_8_b*K_8_b*(T_n - T_8_b) + G_c*c_v*(T_9_b - T_8_b)
                            + G_k*c_v*(T_7_b - T_8_b) ),
            1/(M_9*c_v) * ( 3.6*F_9_b*K_9_b*(T_n - T_9_b) + G_c*c_v*(T_10_b - T_9_b)
                            + G_k*c_v*(T_8_b - T_9_b) ),
            1/(M_10*c_v) * ( 3.6*F_10_b*K_10_b*(T_n - T_10_b) + G_c*c_v*(T_11_b - T_10_b)
                            + G_k*c_v*(T_9_b - T_10_b) ),
            1/(M_11*c_v) * ( 3.6*F_11_b*K_11_b*(T_n - T_11_b) + G_c*c_v*(T_12_b - T_11_b)
                            + G_k*c_v*(T_10_b - T_11_b) ),
            1/(M_12*c_v) * ( 3.6*F_12_b*K_12_b*(T_n - T_12_b) + G_c*c_v*(T_13_b - T_12_b)
                            + G_k*c_v*(T_11_b - T_12_b) ),
            1/(M_13*c_v) * ( 3.6*F_13_b*K_13_b*(T_n - T_13_b) + G_c*c_v*(T_14_b - T_13_b)
                            + G_k*c_v*(T_12_b - T_13_b) ),
            1/(M_14*c_v) * ( 3.6*F_14_b*K_14_b*(T_n - T_14_b) + G_c*c_v*(T_15_b - T_14_b)
                            + G_k*c_v*(T_13_b - T_14_b) ),
            1/(M_15*c_v) * ( 3.6*F_15_b*K_15_b*(T_n - T_15_b) + G_c*c_v*(T_16_b - T_15_b)
                            + G_k*c_v*(T_14_b - T_15_b) ),
            1/(M_16*c_v) * ( 3.6*F_16_b*K_16_b*(T_n - T_16_b) + G_c*c_v*(T_2_c - T_16_b)
                            + G_k*c_v*(T_15_b - T_16_b) )
            ]

def f17(T, tau):
    '''Для дев'ятисекційного баку
    '''
    
    T_1_b, T_2_b, T_3_b, T_4_b, T_5_b, T_6_b, T_7_b, T_8_b, T_9_b, T_10_b,  T_11_b,  T_12_b,  T_13_b,  T_14_b,  T_15_b,  T_16_b,  T_17_b = T  # Імена шуканих функцій.
    return [1/(M_1*c_v) * ( 3.6*F_1_b*K_1_b*(T_n - T_1_b) + G_c*c_v*(T_2_b - T_1_b)
                            + G_k*c_v*(T_1_k - T_1_b) ),
            1/(M_2*c_v) * ( 3.6*F_2_b*K_2_b*(T_n - T_2_b) + G_c*c_v*(T_3_b - T_2_b)
                            + G_k*c_v*(T_1_b - T_2_b) ),
            1/(M_3*c_v) * ( 3.6*F_3_b*K_3_b*(T_n - T_3_b) + G_c*c_v*(T_4_b - T_3_b)
                            + G_k*c_v*(T_2_b - T_3_b) ),
            1/(M_4*c_v) * ( 3.6*F_4_b*K_4_b*(T_n - T_4_b) + G_c*c_v*(T_5_b - T_4_b)
                            + G_k*c_v*(T_3_b - T_4_b) ),
            1/(M_5*c_v) * ( 3.6*F_5_b*K_5_b*(T_n - T_5_b) + G_c*c_v*(T_6_b - T_5_b)
                            + G_k*c_v*(T_4_b - T_5_b) ),
            1/(M_6*c_v) * ( 3.6*F_6_b*K_6_b*(T_n - T_6_b) + G_c*c_v*(T_7_b - T_6_b)
                            + G_k*c_v*(T_5_b - T_6_b) ),
            1/(M_7*c_v) * ( 3.6*F_7_b*K_7_b*(T_n - T_7_b) + G_c*c_v*(T_8_b - T_7_b)
                            + G_k*c_v*(T_6_b - T_7_b) ),
            1/(M_8*c_v) * ( 3.6*F_8_b*K_8_b*(T_n - T_8_b) + G_c*c_v*(T_9_b - T_8_b)
                            + G_k*c_v*(T_7_b - T_8_b) ),
            1/(M_9*c_v) * ( 3.6*F_9_b*K_9_b*(T_n - T_9_b) + G_c*c_v*(T_10_b - T_9_b)
                            + G_k*c_v*(T_8_b - T_9_b) ),
            1/(M_10*c_v) * ( 3.6*F_10_b*K_10_b*(T_n - T_10_b) + G_c*c_v*(T_11_b - T_10_b)
                            + G_k*c_v*(T_9_b - T_10_b) ),
            1/(M_11*c_v) * ( 3.6*F_11_b*K_11_b*(T_n - T_11_b) + G_c*c_v*(T_12_b - T_11_b)
                            + G_k*c_v*(T_10_b - T_11_b) ),
            1/(M_12*c_v) * ( 3.6*F_12_b*K_12_b*(T_n - T_12_b) + G_c*c_v*(T_13_b - T_12_b)
                            + G_k*c_v*(T_11_b - T_12_b) ),
            1/(M_13*c_v) * ( 3.6*F_13_b*K_13_b*(T_n - T_13_b) + G_c*c_v*(T_14_b - T_13_b)
                            + G_k*c_v*(T_12_b - T_13_b) ),
            1/(M_14*c_v) * ( 3.6*F_14_b*K_14_b*(T_n - T_14_b) + G_c*c_v*(T_15_b - T_14_b)
                            + G_k*c_v*(T_13_b - T_14_b) ),
            1/(M_15*c_v) * ( 3.6*F_15_b*K_15_b*(T_n - T_15_b) + G_c*c_v*(T_16_b - T_15_b)
                            + G_k*c_v*(T_14_b - T_15_b) ),
            1/(M_16*c_v) * ( 3.6*F_16_b*K_16_b*(T_n - T_16_b) + G_c*c_v*(T_17_b - T_16_b)
                            + G_k*c_v*(T_15_b - T_16_b) ),
            1/(M_17*c_v) * ( 3.6*F_17_b*K_17_b*(T_n - T_17_b) + G_c*c_v*(T_2_c - T_17_b)
                            + G_k*c_v*(T_16_b - T_17_b) )
            ]

def f18(T, tau):
    '''Для дев'ятисекційного баку
    '''
    
    T_1_b, T_2_b, T_3_b, T_4_b, T_5_b, T_6_b, T_7_b, T_8_b, T_9_b, T_10_b,  T_11_b,  T_12_b,  T_13_b,  T_14_b,  T_15_b,  T_16_b,  T_17_b,  T_18_b = T  # Імена шуканих функцій.
    return [1/(M_1*c_v) * ( 3.6*F_1_b*K_1_b*(T_n - T_1_b) + G_c*c_v*(T_2_b - T_1_b)
                            + G_k*c_v*(T_1_k - T_1_b) ),
            1/(M_2*c_v) * ( 3.6*F_2_b*K_2_b*(T_n - T_2_b) + G_c*c_v*(T_3_b - T_2_b)
                            + G_k*c_v*(T_1_b - T_2_b) ),
            1/(M_3*c_v) * ( 3.6*F_3_b*K_3_b*(T_n - T_3_b) + G_c*c_v*(T_4_b - T_3_b)
                            + G_k*c_v*(T_2_b - T_3_b) ),
            1/(M_4*c_v) * ( 3.6*F_4_b*K_4_b*(T_n - T_4_b) + G_c*c_v*(T_5_b - T_4_b)
                            + G_k*c_v*(T_3_b - T_4_b) ),
            1/(M_5*c_v) * ( 3.6*F_5_b*K_5_b*(T_n - T_5_b) + G_c*c_v*(T_6_b - T_5_b)
                            + G_k*c_v*(T_4_b - T_5_b) ),
            1/(M_6*c_v) * ( 3.6*F_6_b*K_6_b*(T_n - T_6_b) + G_c*c_v*(T_7_b - T_6_b)
                            + G_k*c_v*(T_5_b - T_6_b) ),
            1/(M_7*c_v) * ( 3.6*F_7_b*K_7_b*(T_n - T_7_b) + G_c*c_v*(T_8_b - T_7_b)
                            + G_k*c_v*(T_6_b - T_7_b) ),
            1/(M_8*c_v) * ( 3.6*F_8_b*K_8_b*(T_n - T_8_b) + G_c*c_v*(T_9_b - T_8_b)
                            + G_k*c_v*(T_7_b - T_8_b) ),
            1/(M_9*c_v) * ( 3.6*F_9_b*K_9_b*(T_n - T_9_b) + G_c*c_v*(T_10_b - T_9_b)
                            + G_k*c_v*(T_8_b - T_9_b) ),
            1/(M_10*c_v) * ( 3.6*F_10_b*K_10_b*(T_n - T_10_b) + G_c*c_v*(T_11_b - T_10_b)
                            + G_k*c_v*(T_9_b - T_10_b) ),
            1/(M_11*c_v) * ( 3.6*F_11_b*K_11_b*(T_n - T_11_b) + G_c*c_v*(T_12_b - T_11_b)
                            + G_k*c_v*(T_10_b - T_11_b) ),
            1/(M_12*c_v) * ( 3.6*F_12_b*K_12_b*(T_n - T_12_b) + G_c*c_v*(T_13_b - T_12_b)
                            + G_k*c_v*(T_11_b - T_12_b) ),
            1/(M_13*c_v) * ( 3.6*F_13_b*K_13_b*(T_n - T_13_b) + G_c*c_v*(T_14_b - T_13_b)
                            + G_k*c_v*(T_12_b - T_13_b) ),
            1/(M_14*c_v) * ( 3.6*F_14_b*K_14_b*(T_n - T_14_b) + G_c*c_v*(T_15_b - T_14_b)
                            + G_k*c_v*(T_13_b - T_14_b) ),
            1/(M_15*c_v) * ( 3.6*F_15_b*K_15_b*(T_n - T_15_b) + G_c*c_v*(T_16_b - T_15_b)
                            + G_k*c_v*(T_14_b - T_15_b) ),
            1/(M_16*c_v) * ( 3.6*F_16_b*K_16_b*(T_n - T_16_b) + G_c*c_v*(T_17_b - T_16_b)
                            + G_k*c_v*(T_15_b - T_16_b) ),
            1/(M_17*c_v) * ( 3.6*F_17_b*K_17_b*(T_n - T_17_b) + G_c*c_v*(T_18_b - T_17_b)
                            + G_k*c_v*(T_16_b - T_17_b) ),
            1/(M_18*c_v) * ( 3.6*F_18_b*K_18_b*(T_n - T_18_b) + G_c*c_v*(T_2_c - T_18_b)
                            + G_k*c_v*(T_17_b - T_18_b) )
            ]

def f19(T, tau):
    '''Для дев'ятисекційного баку
    '''
    
    T_1_b, T_2_b, T_3_b, T_4_b, T_5_b, T_6_b, T_7_b, T_8_b, T_9_b, T_10_b,  T_11_b,  T_12_b,  T_13_b,  T_14_b,  T_15_b,  T_16_b,  T_17_b,  T_18_b,  T_19_b = T  # Імена шуканих функцій.
    return [1/(M_1*c_v) * ( 3.6*F_1_b*K_1_b*(T_n - T_1_b) + G_c*c_v*(T_2_b - T_1_b)
                            + G_k*c_v*(T_1_k - T_1_b) ),
            1/(M_2*c_v) * ( 3.6*F_2_b*K_2_b*(T_n - T_2_b) + G_c*c_v*(T_3_b - T_2_b)
                            + G_k*c_v*(T_1_b - T_2_b) ),
            1/(M_3*c_v) * ( 3.6*F_3_b*K_3_b*(T_n - T_3_b) + G_c*c_v*(T_4_b - T_3_b)
                            + G_k*c_v*(T_2_b - T_3_b) ),
            1/(M_4*c_v) * ( 3.6*F_4_b*K_4_b*(T_n - T_4_b) + G_c*c_v*(T_5_b - T_4_b)
                            + G_k*c_v*(T_3_b - T_4_b) ),
            1/(M_5*c_v) * ( 3.6*F_5_b*K_5_b*(T_n - T_5_b) + G_c*c_v*(T_6_b - T_5_b)
                            + G_k*c_v*(T_4_b - T_5_b) ),
            1/(M_6*c_v) * ( 3.6*F_6_b*K_6_b*(T_n - T_6_b) + G_c*c_v*(T_7_b - T_6_b)
                            + G_k*c_v*(T_5_b - T_6_b) ),
            1/(M_7*c_v) * ( 3.6*F_7_b*K_7_b*(T_n - T_7_b) + G_c*c_v*(T_8_b - T_7_b)
                            + G_k*c_v*(T_6_b - T_7_b) ),
            1/(M_8*c_v) * ( 3.6*F_8_b*K_8_b*(T_n - T_8_b) + G_c*c_v*(T_9_b - T_8_b)
                            + G_k*c_v*(T_7_b - T_8_b) ),
            1/(M_9*c_v) * ( 3.6*F_9_b*K_9_b*(T_n - T_9_b) + G_c*c_v*(T_10_b - T_9_b)
                            + G_k*c_v*(T_8_b - T_9_b) ),
            1/(M_10*c_v) * ( 3.6*F_10_b*K_10_b*(T_n - T_10_b) + G_c*c_v*(T_11_b - T_10_b)
                            + G_k*c_v*(T_9_b - T_10_b) ),
            1/(M_11*c_v) * ( 3.6*F_11_b*K_11_b*(T_n - T_11_b) + G_c*c_v*(T_12_b - T_11_b)
                            + G_k*c_v*(T_10_b - T_11_b) ),
            1/(M_12*c_v) * ( 3.6*F_12_b*K_12_b*(T_n - T_12_b) + G_c*c_v*(T_13_b - T_12_b)
                            + G_k*c_v*(T_11_b - T_12_b) ),
            1/(M_13*c_v) * ( 3.6*F_13_b*K_13_b*(T_n - T_13_b) + G_c*c_v*(T_14_b - T_13_b)
                            + G_k*c_v*(T_12_b - T_13_b) ),
            1/(M_14*c_v) * ( 3.6*F_14_b*K_14_b*(T_n - T_14_b) + G_c*c_v*(T_15_b - T_14_b)
                            + G_k*c_v*(T_13_b - T_14_b) ),
            1/(M_15*c_v) * ( 3.6*F_15_b*K_15_b*(T_n - T_15_b) + G_c*c_v*(T_16_b - T_15_b)
                            + G_k*c_v*(T_14_b - T_15_b) ),
            1/(M_16*c_v) * ( 3.6*F_16_b*K_16_b*(T_n - T_16_b) + G_c*c_v*(T_17_b - T_16_b)
                            + G_k*c_v*(T_15_b - T_16_b) ),
            1/(M_17*c_v) * ( 3.6*F_17_b*K_17_b*(T_n - T_17_b) + G_c*c_v*(T_18_b - T_17_b)
                            + G_k*c_v*(T_16_b - T_17_b) ),
            1/(M_18*c_v) * ( 3.6*F_18_b*K_18_b*(T_n - T_18_b) + G_c*c_v*(T_19_b - T_18_b)
                            + G_k*c_v*(T_17_b - T_18_b) ),
            1/(M_19*c_v) * ( 3.6*F_19_b*K_19_b*(T_n - T_19_b) + G_c*c_v*(T_2_c - T_19_b)
                            + G_k*c_v*(T_18_b - T_19_b) )
            ]

def f20(T, tau):
    '''Для дев'ятисекційного баку
    '''
    
    T_1_b, T_2_b, T_3_b, T_4_b, T_5_b, T_6_b, T_7_b, T_8_b, T_9_b, T_10_b,  T_11_b,  T_12_b,  T_13_b,  T_14_b,  T_15_b,  T_16_b,  T_17_b,  T_18_b,  T_19_b,  T_20_b = T  # Імена шуканих функцій.
    return [1/(M_1*c_v) * ( 3.6*F_1_b*K_1_b*(T_n - T_1_b) + G_c*c_v*(T_2_b - T_1_b)
                            + G_k*c_v*(T_1_k - T_1_b) ),
            1/(M_2*c_v) * ( 3.6*F_2_b*K_2_b*(T_n - T_2_b) + G_c*c_v*(T_3_b - T_2_b)
                            + G_k*c_v*(T_1_b - T_2_b) ),
            1/(M_3*c_v) * ( 3.6*F_3_b*K_3_b*(T_n - T_3_b) + G_c*c_v*(T_4_b - T_3_b)
                            + G_k*c_v*(T_2_b - T_3_b) ),
            1/(M_4*c_v) * ( 3.6*F_4_b*K_4_b*(T_n - T_4_b) + G_c*c_v*(T_5_b - T_4_b)
                            + G_k*c_v*(T_3_b - T_4_b) ),
            1/(M_5*c_v) * ( 3.6*F_5_b*K_5_b*(T_n - T_5_b) + G_c*c_v*(T_6_b - T_5_b)
                            + G_k*c_v*(T_4_b - T_5_b) ),
            1/(M_6*c_v) * ( 3.6*F_6_b*K_6_b*(T_n - T_6_b) + G_c*c_v*(T_7_b - T_6_b)
                            + G_k*c_v*(T_5_b - T_6_b) ),
            1/(M_7*c_v) * ( 3.6*F_7_b*K_7_b*(T_n - T_7_b) + G_c*c_v*(T_8_b - T_7_b)
                            + G_k*c_v*(T_6_b - T_7_b) ),
            1/(M_8*c_v) * ( 3.6*F_8_b*K_8_b*(T_n - T_8_b) + G_c*c_v*(T_9_b - T_8_b)
                            + G_k*c_v*(T_7_b - T_8_b) ),
            1/(M_9*c_v) * ( 3.6*F_9_b*K_9_b*(T_n - T_9_b) + G_c*c_v*(T_10_b - T_9_b)
                            + G_k*c_v*(T_8_b - T_9_b) ),
            1/(M_10*c_v) * ( 3.6*F_10_b*K_10_b*(T_n - T_10_b) + G_c*c_v*(T_11_b - T_10_b)
                            + G_k*c_v*(T_9_b - T_10_b) ),
            1/(M_11*c_v) * ( 3.6*F_11_b*K_11_b*(T_n - T_11_b) + G_c*c_v*(T_12_b - T_11_b)
                            + G_k*c_v*(T_10_b - T_11_b) ),
            1/(M_12*c_v) * ( 3.6*F_12_b*K_12_b*(T_n - T_12_b) + G_c*c_v*(T_13_b - T_12_b)
                            + G_k*c_v*(T_11_b - T_12_b) ),
            1/(M_13*c_v) * ( 3.6*F_13_b*K_13_b*(T_n - T_13_b) + G_c*c_v*(T_14_b - T_13_b)
                            + G_k*c_v*(T_12_b - T_13_b) ),
            1/(M_14*c_v) * ( 3.6*F_14_b*K_14_b*(T_n - T_14_b) + G_c*c_v*(T_15_b - T_14_b)
                            + G_k*c_v*(T_13_b - T_14_b) ),
            1/(M_15*c_v) * ( 3.6*F_15_b*K_15_b*(T_n - T_15_b) + G_c*c_v*(T_16_b - T_15_b)
                            + G_k*c_v*(T_14_b - T_15_b) ),
            1/(M_16*c_v) * ( 3.6*F_16_b*K_16_b*(T_n - T_16_b) + G_c*c_v*(T_17_b - T_16_b)
                            + G_k*c_v*(T_15_b - T_16_b) ),
            1/(M_17*c_v) * ( 3.6*F_17_b*K_17_b*(T_n - T_17_b) + G_c*c_v*(T_18_b - T_17_b)
                            + G_k*c_v*(T_16_b - T_17_b) ),
            1/(M_18*c_v) * ( 3.6*F_18_b*K_18_b*(T_n - T_18_b) + G_c*c_v*(T_19_b - T_18_b)
                            + G_k*c_v*(T_17_b - T_18_b) ),
            1/(M_19*c_v) * ( 3.6*F_19_b*K_19_b*(T_n - T_19_b) + G_c*c_v*(T_20_b - T_19_b)
                            + G_k*c_v*(T_18_b - T_19_b) ),
            1/(M_20*c_v) * ( 3.6*F_20_b*K_20_b*(T_n - T_20_b) + G_c*c_v*(T_2_c - T_20_b)
                            + G_k*c_v*(T_19_b - T_20_b) )
            ]

for n in Nn if calc_divergence else range(n, n+1):
    # ============= Дані протягом дня =============:
    # Температура повітря, де розміщено бак-акумулятор, К.
    T_n = 20
    # Маса води в баку-акмулуяторі, кг.
    M = 50
    M_vals = [M/n] * n
    
    # Питома масова теплоємність води, кДж/(кг*К).
    c_v = 4.187
    # Масова витрата в контурі геліоколектора, кг/год.
    G_k = 300
    # Масова витрата в контурі споживача, кг/год.
    G_c = 300
    # Температура теплоносія на виході з геліоколетора, К.
    T_1_k = 45
    # Температура теплоносія зворотнього теплопроводу в контурі теплоспоживача, К.
    T_2_c = 25
    # Коефіцієнт теплопередачі, Вт/(м^2*K).
    K_0_b = 10
    
    K_vals = [K_0_b] * n
    # Площа, м^2: d = 0.8 м, h = 1.5 м, F_0 = pi * d * h_0 = pi * 0.8 * 0.5 = 1.257
    F_0_b = 1.257
    
    F_vals = [F_0_b] * n
    
    # Початкові умови:
    t_hv = 10#55   # Температура холодної води, K
    T_b_0 = [t_hv] * n
    
    if n == 2:
        M_1, M_2 = M_vals
        K_1_b, K_2_b = K_vals
        F_1_b, F_2_b = F_vals
    elif n == 3:
        M_1, M_2, M_3 = M_vals
        K_1_b, K_2_b, K_3_b = K_vals
        F_1_b, F_2_b, F_3_b = F_vals
    elif n == 4:
        M_1, M_2, M_3, M_4 = M_vals
        K_1_b, K_2_b, K_3_b, K_4_b = K_vals
        F_1_b, F_2_b, F_3_b, F_4_b = F_vals
    elif n == 5:
        M_1, M_2, M_3, M_4, M_5 = M_vals
        K_1_b, K_2_b, K_3_b, K_4_b, K_5_b = K_vals
        F_1_b, F_2_b, F_3_b, F_4_b, F_5_b = F_vals
    elif n == 6:
        M_1, M_2, M_3, M_4, M_5, M_6 = M_vals
        K_1_b, K_2_b, K_3_b, K_4_b, K_5_b, K_6_b = K_vals
        F_1_b, F_2_b, F_3_b, F_4_b, F_5_b, F_6_b = F_vals
    elif n == 7:
        M_1, M_2, M_3, M_4, M_5, M_6, M_7 = M_vals
        K_1_b, K_2_b, K_3_b, K_4_b, K_5_b, K_6_b, K_7_b = K_vals
        F_1_b, F_2_b, F_3_b, F_4_b, F_5_b, F_6_b, F_7_b = F_vals
    elif n == 8:
        M_1, M_2, M_3, M_4, M_5, M_6, M_7, M_8 = M_vals
        K_1_b, K_2_b, K_3_b, K_4_b, K_5_b, K_6_b, K_7_b, K_8_b = K_vals
        F_1_b, F_2_b, F_3_b, F_4_b, F_5_b, F_6_b, F_7_b, F_8_b = F_vals
    elif n == 9:
        M_1, M_2, M_3, M_4, M_5, M_6, M_7, M_8, M_9 = M_vals
        K_1_b, K_2_b, K_3_b, K_4_b, K_5_b, K_6_b, K_7_b, K_8_b, K_9_b = K_vals
        F_1_b, F_2_b, F_3_b, F_4_b, F_5_b, F_6_b, F_7_b, F_8_b, F_9_b = F_vals
    elif n == 10:
        M_1, M_2, M_3, M_4, M_5, M_6, M_7, M_8, M_9,  M_10 = M_vals
        K_1_b, K_2_b, K_3_b, K_4_b, K_5_b, K_6_b, K_7_b, K_8_b, K_9_b, K_10_b = K_vals
        F_1_b, F_2_b, F_3_b, F_4_b, F_5_b, F_6_b, F_7_b, F_8_b, F_9_b, F_10_b = F_vals
    elif n == 11:
        M_1, M_2, M_3, M_4, M_5, M_6, M_7, M_8, M_9,  M_10,  M_11 = M_vals
        K_1_b, K_2_b, K_3_b, K_4_b, K_5_b, K_6_b, K_7_b, K_8_b, K_9_b, K_10_b, K_11_b = K_vals
        F_1_b, F_2_b, F_3_b, F_4_b, F_5_b, F_6_b, F_7_b, F_8_b, F_9_b, F_10_b, F_11_b = F_vals
    elif n == 12:
        M_1, M_2, M_3, M_4, M_5, M_6, M_7, M_8, M_9,  M_10,  M_11, M_12 = M_vals
        K_1_b, K_2_b, K_3_b, K_4_b, K_5_b, K_6_b, K_7_b, K_8_b, K_9_b, K_10_b, K_11_b, K_12_b = K_vals
        F_1_b, F_2_b, F_3_b, F_4_b, F_5_b, F_6_b, F_7_b, F_8_b, F_9_b, F_10_b, F_11_b, F_12_b = F_vals
    elif n == 13:
        M_1, M_2, M_3, M_4, M_5, M_6, M_7, M_8, M_9,  M_10,  M_11, M_12, M_13 = M_vals
        K_1_b, K_2_b, K_3_b, K_4_b, K_5_b, K_6_b, K_7_b, K_8_b, K_9_b, K_10_b, K_11_b, K_12_b, K_13_b = K_vals
        F_1_b, F_2_b, F_3_b, F_4_b, F_5_b, F_6_b, F_7_b, F_8_b, F_9_b, F_10_b, F_11_b, F_12_b, F_13_b = F_vals
    elif n == 14:
        M_1, M_2, M_3, M_4, M_5, M_6, M_7, M_8, M_9,  M_10,  M_11, M_12, M_13, M_14 = M_vals
        K_1_b, K_2_b, K_3_b, K_4_b, K_5_b, K_6_b, K_7_b, K_8_b, K_9_b, K_10_b, K_11_b, K_12_b, K_13_b, K_14_b = K_vals
        F_1_b, F_2_b, F_3_b, F_4_b, F_5_b, F_6_b, F_7_b, F_8_b, F_9_b, F_10_b, F_11_b, F_12_b, F_13_b, F_14_b = F_vals
    elif n == 15:
        M_1, M_2, M_3, M_4, M_5, M_6, M_7, M_8, M_9,  M_10,  M_11, M_12, M_13, M_14, M_15 = M_vals
        K_1_b, K_2_b, K_3_b, K_4_b, K_5_b, K_6_b, K_7_b, K_8_b, K_9_b, K_10_b, K_11_b, K_12_b, K_13_b, K_14_b, K_15_b = K_vals
        F_1_b, F_2_b, F_3_b, F_4_b, F_5_b, F_6_b, F_7_b, F_8_b, F_9_b, F_10_b, F_11_b, F_12_b, F_13_b, F_14_b, F_15_b = F_vals
    elif n == 16:
        M_1, M_2, M_3, M_4, M_5, M_6, M_7, M_8, M_9,  M_10,  M_11, M_12, M_13, M_14, M_15, M_16 = M_vals
        K_1_b, K_2_b, K_3_b, K_4_b, K_5_b, K_6_b, K_7_b, K_8_b, K_9_b, K_10_b, K_11_b, K_12_b, K_13_b, K_14_b, K_15_b, K_16_b = K_vals
        F_1_b, F_2_b, F_3_b, F_4_b, F_5_b, F_6_b, F_7_b, F_8_b, F_9_b, F_10_b, F_11_b, F_12_b, F_13_b, F_14_b, F_15_b, F_16_b = F_vals
    elif n == 17:
        M_1, M_2, M_3, M_4, M_5, M_6, M_7, M_8, M_9,  M_10,  M_11, M_12, M_13, M_14, M_15, M_16, M_17 = M_vals
        K_1_b, K_2_b, K_3_b, K_4_b, K_5_b, K_6_b, K_7_b, K_8_b, K_9_b, K_10_b, K_11_b, K_12_b, K_13_b, K_14_b, K_15_b, K_16_b, K_17_b = K_vals
        F_1_b, F_2_b, F_3_b, F_4_b, F_5_b, F_6_b, F_7_b, F_8_b, F_9_b, F_10_b, F_11_b, F_12_b, F_13_b, F_14_b, F_15_b, F_16_b, F_17_b = F_vals
    elif n == 18:
        M_1, M_2, M_3, M_4, M_5, M_6, M_7, M_8, M_9,  M_10,  M_11, M_12, M_13, M_14, M_15, M_16, M_17, M_18 = M_vals
        K_1_b, K_2_b, K_3_b, K_4_b, K_5_b, K_6_b, K_7_b, K_8_b, K_9_b, K_10_b, K_11_b, K_12_b, K_13_b, K_14_b, K_15_b, K_16_b, K_17_b, K_18_b = K_vals
        F_1_b, F_2_b, F_3_b, F_4_b, F_5_b, F_6_b, F_7_b, F_8_b, F_9_b, F_10_b, F_11_b, F_12_b, F_13_b, F_14_b, F_15_b, F_16_b, F_17_b, F_18_b = F_vals
    elif n == 19:
        M_1, M_2, M_3, M_4, M_5, M_6, M_7, M_8, M_9,  M_10,  M_11, M_12, M_13, M_14, M_15, M_16, M_17, M_18, M_19 = M_vals
        K_1_b, K_2_b, K_3_b, K_4_b, K_5_b, K_6_b, K_7_b, K_8_b, K_9_b, K_10_b, K_11_b, K_12_b, K_13_b, K_14_b, K_15_b, K_16_b, K_17_b, K_18_b, K_19_b = K_vals
        F_1_b, F_2_b, F_3_b, F_4_b, F_5_b, F_6_b, F_7_b, F_8_b, F_9_b, F_10_b, F_11_b, F_12_b, F_13_b, F_14_b, F_15_b, F_16_b, F_17_b, F_18_b, F_19_b = F_vals
    elif n == 20:
        M_1, M_2, M_3, M_4, M_5, M_6, M_7, M_8, M_9,  M_10,  M_11, M_12, M_13, M_14, M_15, M_16, M_17, M_18, M_19, M_20 = M_vals
        K_1_b, K_2_b, K_3_b, K_4_b, K_5_b, K_6_b, K_7_b, K_8_b, K_9_b, K_10_b, K_11_b, K_12_b, K_13_b, K_14_b, K_15_b, K_16_b, K_17_b, K_18_b, K_19_b, K_20_b = K_vals
        F_1_b, F_2_b, F_3_b, F_4_b, F_5_b, F_6_b, F_7_b, F_8_b, F_9_b, F_10_b, F_11_b, F_12_b, F_13_b, F_14_b, F_15_b, F_16_b, F_17_b, F_18_b, F_19_b, F_20_b = F_vals

    if n == 2:
        f = f2
    elif n == 3:
        f = f3
    elif n == 4:
        f = f4
    elif n == 5:
        f = f5
    elif n == 6:
        f = f6
    elif n == 7:
        f = f7
    elif n == 8:
        f = f8
    elif n == 9:
        f = f9
    elif n == 10:
        f = f10
    elif n == 11:
        f = f11
    elif n == 12:
        f = f12
    elif n == 13:
        f = f13
    elif n == 14:
        f = f14
    elif n == 15:
        f = f15
    elif n == 16:
        f = f16
    elif n == 17:
        f = f17
    elif n == 18:
        f = f18
    elif n == 19:
        f = f19
    elif n == 20:
        f = f20
    T_i_b_results = odeint(f, T_b_0, tau)
    print(T_i_b_results)
    if calc_divergence:
        if n == 2:
            # Середні температури у верхньому та нижньому шарі в БА.
            t_s = T_i_b_results[-1, 0]
            t_e = T_i_b_results[-1, -1]
            T_s = [t_s]
            T_e = [t_e]
            #t_s_2, t_e_2 = T_i_b_results[-1]
            #D_s = [0]
            #D_e = [0]
            #Dd_s = [0]
            #Dd_e = [0]
        else:
            t_s = T_i_b_results[-1, 0]
            t_e = T_i_b_results[-1, -1]
            T_s = np.r_[T_s, t_s]
            T_e = np.r_[T_e, t_e]
            # Абсолютні та відносні розбіжності.
            #d_s = np.abs(t_s - t_s_2)
            #d_e = np.abs(t_e - t_e_2)
            #D_s.append(d_s)
            #D_e.append(d_e)
            #dd_s = np.abs(t_s - t_s_2) / t_s_2 * 100
            #dd_e = np.abs(t_e - t_e_2) / t_e_2 * 100
            #Dd_s.append(dd_s)
            #Dd_e.append(dd_e)
        
        T_s = np.array(T_s)
        T_e = np.array(T_e)
        t_s_N = T_s[-1]
        t_e_N = T_e[-1]
        d_s = np.abs(T_s - t_s_N)
        D_s = d_s
        d_e = np.abs(T_e - t_e_N)
        D_e = d_e
        dd_s = np.abs(T_s - t_s_N) / t_s_N * 100
        dd_e = np.abs(T_e - t_e_N) / t_e_N * 100
        Dd_s = dd_s
        Dd_e = dd_e
        
    else:
        xlabel = r'Час, $\tau$'
        ylabel = r'$t$, $\mathrm{{}^\circ C}$'
        
        fig = plt.figure(**fig_data)
        ax = fig.add_subplot(111)
        for i in range(n):
            data = T_i_b_results[..., i]
            plt.plot(tau, data, lw=2.5)
            
            ax.annotate(r'$t_{}$'.format(i+1), xy=(tau[-2], data[-2]), xycoords='data',
                            xytext=(1.025*tau[-1], data[-1]+3), textcoords='data', va='top', 
                            ha='left', arrowprops=dict(arrowstyle='-'))
            
        ax.set_xlabel(xlabel, x=1, ha="right")
        ax.set_xticks(np.linspace(0, 24, 13))#np.linspace(0, 24*30, 31))
        ax.set_ylabel(ylabel, y=1.025, va='bottom', rotation=0)
        locator_y = ticker.MultipleLocator(base=5)
        ax.yaxis.set_major_locator(locator_y)
        ax.set_ylim(.9*T_i_b_results.min(), 1.1*T_i_b_results.max())
        ax.set_title(r'Розподіл температур теплоносія в {}-секційному баку акумуляторі протягом доби'.format(n), y=1.10)
        ax.spines['top'].set_color(grid_color)
        ax.spines['right'].set_color(grid_color)
        ax.grid(color=grid_color)
        ax.set_position(ax_pos)
        
        plt.savefig(os.path.join(DIRECT_PATH, 'n = {}.png'.format(n)), format='png', 
                    dpi=fig_data['dpi'])

if calc_divergence:
    print('Абсолютні розбіжності початкових температур:\n', D_s)
    print('Абсолютні розбіжності кінцевих температур:\n', D_e)
    print('Відносні розбіжності початкових температур:\n', Dd_s)
    print('Відносні розбіжності кінцевих температур:\n', Dd_e)
    def plot_divergence(data_, y_locator_base, ylabel_, title_, file_title_):
        xlabel = r'Кількість шарів, $\mathrm{n}$'
        ylabel = ylabel_
        if type(data_[0]) is np.ndarray:
            data_2 = np.r_[data_[0], data_[1]]
        else:
            data_2 = data_[0] + data_[1]
        
        fig = plt.figure(**fig_data)
        ax = fig.add_subplot(111)
        for i, (data, t_sublabel) in enumerate(zip(data_, ('п', 'к'))):
            plt.plot(Nn, data, lw=2.5)
            
            ax.annotate(r'$t_{\mathrm{%s}}$' % t_sublabel, xy=(Nn[2], data[2]), xycoords='data',
                            xytext=(.95*Nn[3], (1.1 if i else 0.9)*data[1]), textcoords='data', va='top', 
                            ha='left', arrowprops=dict(arrowstyle='-'))
            
        ax.set_xlabel(xlabel, x=1, ha="right")
        #ax.set_xticks(np.linspace(0, 24, 13))#np.linspace(0, 24*30, 31))
        ax.set_ylabel(ylabel, y=1.025, va='bottom', rotation=0)
        
        y_min = np.floor(min(data_2))
        if y_min % y_locator_base:
            y_min -= y_locator_base
        y_max = np.ceil(max(data_2))
        if y_max % y_locator_base:
            y_max += y_locator_base
        
        locator_x = ticker.MultipleLocator(base=1)
        ax.xaxis.set_major_locator(locator_x)
        locator_y = ticker.MultipleLocator(base=y_locator_base)
        ax.yaxis.set_major_locator(locator_y)
        ax.set_ylim(y_min, y_max)
        ax.set_title(title_, y=1.11)
        ax.spines['top'].set_color(grid_color)
        ax.spines['right'].set_color(grid_color)
        ax.grid(color=grid_color)
        ax.set_position(ax_pos)
        
        plt.savefig(os.path.join(DIRECT_PATH, '{}.png'.format(file_title_)), format='png', 
                    dpi=fig_data['dpi'])
    plot_divergence((Dd_s, Dd_e), 5, r'$\mathrm{\delta}$, %', 
                    r'Відносна розбіжність, $\mathrm{\delta}$, %, температур теплоносія '
                    'в найвищому та найнижчому шарі\nв баку акумуляторі протягом доби', 
                    'delta')
    plot_divergence((D_s, D_e), 1, r'$\mathrm{\Delta t}$, $\mathrm{{}^\circ C}$', 
                    r'Абсолютна розбіжність, $\mathrm{\Delta t}$, $\mathrm{{}^\circ C}$, температур теплоносія '
                    'в найвищому та найнижчому шарі\nв баку акумуляторі протягом доби', 
                    'Delta_')

print(" Розв'язок завершено! ".center(50, '='))

if IS_SHOW_GRAF:
    plt.show()