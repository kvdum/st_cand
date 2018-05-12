#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Created on 22 трав. 2017 р.

@author: kavedium
'''
import locale
locale.setlocale(locale.LC_ALL, '')

import sys, os
import winpaths
import errno
import numpy as np
from scipy.interpolate import interp1d
from scipy.integrate import odeint

from matplotlib import pyplot as plt, rcParams, ticker, gridspec
rcParams['axes.formatter.use_locale'] = True
rcParams.update({'font.family':'serif', 'mathtext.fontset': 'dejavuserif',
                 'font.size': 14, 'axes.titlesize' : 14})

np.set_printoptions(precision=3)

fig_data = dict(figsize=(12.2, 6.8), dpi=80)
grid_color = '#ABB2B9'
ax_pos = (0.09, 0.09, 0.88, .75)

# Потік сонячної радіації в напрямку нормалі до площини колекторів.
I_i = 300   # Вт/м2
F_gk_i = 20 # м2
M_gk_i = 40 # кг
# Витрата теплоносія через i-тий контур n-го ряду. 
G_gk_i = .017 # кг/c
# Питома теплоємність води.
c_v = 4187 # Дж/(кг*К)
# Температура нагрітого теплоносія на виході з i-го колектора n-го ряду.
t_2_gk_i = 45 # тем-ра на виході, град.С
# Температура охолодженого теплоносія на вході в i-ий колектор n-го ряду.
t_1_gk_i = 25 # т-ра на вході
# Середній коефіцієнт теплопередачі i-го колектора
K_gk_i = 6.9 # Вт/(м2 * К)
# Температура оточуючого середовища.
t_n = 25 # град. С
# Середня питома теплоємність i-го колектора.
c_gk_i = 4187#16000 # Дж/(кг*К) ? - подив. Даффі

# Витрата теплоносія в геліоконтурі
G_I = .017  # кг/с
# Середній коефіцієнт теплопередачі системи геліоконтурів.
K_sgk = 6.9 # Вт/(м2*К) # Визначити з книжки
F_sgk = 20 # м^2.
M_sgk = 40 # кг
# Середня питома теплоємність системи геліоконтурів.
c_sgk = 4187#16000   # Дж/(кг*К)
# Середній коефіцієнт теплопередачі теплообмінника.
k_B = 2256 # Вт/(м2*K)    # з курсака ГВ
# Площа теплообмінника.
F_B = 0.75    # м2
# Витрата теплоносія у споживача. 
G_p = .018 # кг/с    # з курсака ГВ

M_I_to = 20 # кг
# Питома теплоємність в теплообміннику в контурі геліоколектора.
c_I_to = 4187#16000  # Дж/(кг*К)

# Середній коефіцієнт теплопередачі ділянки від теплообмінника до системи геліоконтурів.
K_I_2 = .25 # Вт/(м2*К)
F_I_2 = 1.57
M_I_2 = 9.82
# Середня теплоємність ділянки від теплообмінника до системи геліоконтурів.
c_I_2 = 4187#3000    # Дж/(кг*К)

# Витрата теплоносія в контурі бака-акумулятора.
G_II = 0.117    # кг/с
# Середній коефіцієнт теплопередачі ділянки від баку-акумулятора до теплообмінника.
K_II_2 = .25    # Вт/(м2*К)
F_II_2 = 1.5
M_II_2 = 9.8
# Середня теплоємність ділянки від баку-акумулятора до теплообмінника.
c_II_2 = 4187#3000   # Дж/(кг*К)

# Середній коефіцієнт теплопередачі теплообмінника в контурі баку-акумулятора.
K_II_to = 2600 # Вт/(м2*К) курсак ГВ
F_II_to = 4
M_II_to = 20
# Середня питома теплоємність теплообмінника в контурі баку-акумулятора.
c_II_to = 4187#16000 # Дж/(кг*К)

# Середній коефіцієнт теплопередачі ділянки від теплообмінника до баку-акумулятора.
K_II_1 = .25    # Вт/(м2*К)
F_II_1 = 1.5
M_II_1 = 9.8
# Середня питома теплоємність ділянки від теплообмінника до баку-акумулятора.
c_II_1 = 4187#3000   # Дж/(кг*К)

# Середній коефіцієнт теплопередачі самого верхнього шару ділянки бака-акумулятора.
K_1 = 2   # Вт/(м2*К)
# Кінцева температура у споживача.
t_p = 45    # град. С.
F_1 = 1.57
M_1 = 1000/3
# Середня питома теплоємність самого верхнього шару ділянки бака-акумулятора.
#c_1 = 4187#200000    # Дж/(кг*К)

#K_2 = 3
#c_2 = 4.187

K_2 = 2
F_2 = 2.36
M_2 = 1000/3

# Витрата теплоносія в контурі споживача.
G_x = .018  # кг/с
# Температура на вході в бак-акумулятор.
t_x = 25 # град. С # то є tl_2
# Середній коефіцієнт теплопередачі самого нижнього шару ділянки бака-акумулятора.
K_m2 = 2  # Вт/(м2*К)
F_m2 = 1.57
M_m2 = 1000/3
# Середня питома теплоємність самого нижнього шару ділянки бака-акумулятора.
c_m2 = 4187#200000   # Дж/(кг*К)

def f(y, tau, params):
    """
    y - початкові умови.
    tau - часовий ряд.
    """
    
    t_gk_i, t_sgk, t_I_to, t_I_2, t_II_2, t_II_to, t_II_1, t_1, t_2, t_m2 = y
    
    # Закон збереження енергії (ЗЗЕ) системи плоских колекторів.
    out_1 = (I_i * F_gk_i - (G_gk_i * c_v * (t_2_gk_i - t_1_gk_i) + \
                                   K_gk_i * F_gk_i * (t_gk_i - t_n))) / (c_gk_i * M_gk_i)
    
    # ЗЗЕ для теплопроводу, який з'єднує вихід системи сонячних колекторів
    # із входом у теплообмінник.
    out_2 = (G_I * c_v * (t_gk_i - t_sgk) - \
        (K_sgk * F_sgk * (t_sgk - t_n) + G_I * c_v * (t_sgk - t_I_to) )) \
         /  (c_sgk * M_sgk)
    
    # ЗЗЕ роботи теплообмінника.
    out_3 = G_I * (1 - np.exp((-K_sgk*F_sgk)/(G_I*c_sgk))) * \
                  (1 - np.exp((-k_B*F_B)/(G_p*c_I_to))) / \
                  (1 - np.exp( -((K_sgk*F_sgk)/(G_I*c_sgk) + (k_B*F_B)/(G_p*c_I_to)) )) \
                  * c_I_to * (t_II_to - t_I_to) / (c_I_to * M_I_to)
    
    # ЗЗЕ для трубопроводу, який з'єднує вихід теплообмінника із входом до 
    # системи геліоколекторів.
    out_4 = (G_I * c_v * (t_I_to- t_I_2) - \
        K_I_2 * F_I_2 * (t_I_to - t_n)) / (c_I_2 * M_I_2)
    
    # ЗЗЕ для теплопроводу, який з'єднує вихід бака-акумулятора  із входом до 
    # теплообмінника.
    out_5 = (G_II * c_v * (t_m2 - t_II_2) - \
        K_II_2 * F_II_2 * (t_II_2 - t_n)) / (c_II_2 * M_II_2)
    
    # Описує роботу теплообмінника.
    out_6 = (G_I * c_v * (t_II_to - t_I_2) - \
        (K_II_to * F_II_to * (t_II_to - t_n) + G_II * c_v * \
        (t_II_to - t_II_2))) / (c_II_to * M_II_to)
    
    # ЗЗЕ для трубопроводу, який з'єднує вихід теплообмінника із баком-акумулятором.
    out_7 = (G_II * c_v * (t_II_to - t_II_1) - \
        (K_II_1 * F_II_1 * (t_II_1 - t_n) + G_II * c_v * \
        (t_II_1 - t_1))) / (c_II_1 * M_II_1)
    
    # Робота бака-акумулятора при наявності в ньому вертикальної стратифікації 
    # температури рідини.
    #out_8 = (G_II * c_v * (t_II_2 - t_1) - \
    #    K_1 * F_1 * (t_1 - t_n) + G_p * c_v * (t_1 - t_p)) / (c_1 * M_1)
    
    # Робота бака-акумулятора при наявності в ньому вертикальної стратифікації 
    # температури рідини.
    #out_9 = (G_II * c_v * (t_1 - t_m2) + \
    #    G_x * c_v * (t_x - t_m2) - K_m2 * F_m2 * (t_m2 - t_n)) / (c_m2 * M_m2)
    
    out_8 = 1/(M_1*c_v) * ( F_1*K_1*(t_n - t_1) + G_p*c_v*(t_p - t_1) 
                            + G_II*c_v*(t_II_1 - t_1) )
    out_9 = 1/(M_2*c_v) * ( F_2*K_2*(t_n - t_2) + G_p*c_v*(t_m2 - t_2)
                            + G_II*c_v*(t_1 - t_2) )
    out_10 = 1/(M_m2*c_v) * ( F_m2*K_m2*(t_n - t_m2) + G_x*c_v*(t_x - t_m2)
                            + G_II*c_v*(t_2 - t_m2) )
    
    
    #out_8 = 1/(M_1*c_v) * ( F_1*K_1*(t_n - t_1) + G_p*c_v*(t_m2 - t_1)
     #                       + G_II * c_v * (t_II_1 - t_1) )
    #out_9 = 1/(M_m2*c_v) * ( F_m2*K_m2*(t_n - t_m2) + G_x*c_v*(t_x - t_m2)
    #                        + G_II * c_v * (t_1 - t_m2) )
            
    
    #if Z == 1:
    return [out_1, out_2, out_3, out_4, out_5, out_6, out_7, out_8, out_9, out_10]
    #else:
    #    return [out_1, out_3, out_4, out_5, out_6, out_7, out_8, out_9]
    
#eq1 = Eq(t_gk_i(tau).diff(tau), )

#eq2 = Eq((tau).diff(tau), )

#eq3 = Eq((tau).diff(tau), )

#eq4 = Eq((tau).diff(tau), )

#eq5 = Eq((tau).diff(tau), )

#eq6 = Eq((tau).diff(tau), )

#eq7 = Eq((tau).diff(tau), )

#eq8 = Eq((tau).diff(tau), )

#eq9 = Eq(t_2(tau).diff(tau), (G_II * c_v * (t_1(tau) - t_2(tau)) - \
 #       K_2 * (t_2(tau) - t_n)) / c_2)

#eq10 = Eq(t_3(tau).diff(tau), (G_II * c_v * (t_2(tau) - t_3(tau)) - \
 #       K_3 * (t_3(tau) - t_n)) / c_2)

#eq11 = Eq((tau).diff(tau), (G_II * c_v * (t_3(tau) - t_m2(tau)) + \
 #       G_x * c_v * (t_x - t_m2(tau)) - K_m2 * (t_m2(tau) - t_n)) / c_m2)

#eq12 = Eq(S_I * G_I**2, H_I)

if __name__ == '__main__':
    #Z = 1   # Z = 1 - із врахування рівнняння (2), де є t_sgk
    R = 2   # R = 1 - графіки в одному вікні, R = 2 - графіки виводяться окремо.
    
    is_print = True    # True - виводить графіки на диск.
    
    # Часовий ряд роботи геліосистеми в секундах..
    tau = np.linspace(0, 6*60*60, 60)
    
    #t_gk_i_0, t_sgk_0, t_I_to_0, t_I_2_0, t_II_2_0, t_II_to_0, t_II_1_0, t_1_0, \
    #t_m2_0
    #if Z == 1:
    y0 = 10 * [t_n]
    #else:
    #    y0 = [25, 25, 25, 25, 25, 25, 25, 25]
    
    res = odeint(f, y0=y0, t=tau, args=([],))
    
    print(res)
    
    ylabels = (r'$t_{гк},\,{}^{\circ}C$', r'$t_{сгк},\,{}^{\circ}C$', 
               r'$t_{I_{ТО}},\,{}^{\circ}C$',
               r'$t_{I_2},\,{}^{\circ}C$', r'$t_{II_2},\,{}^{\circ}C$',
               r'$t_{II_{ТО}},\,{}^{\circ}C$', r'$t_{II_I},\,{}^{\circ}C$',
               r'$t_1,\,{}^{\circ}C$', r'$t_2,\,{}^{\circ}C$', 
               r'$t_{m_2},\,{}^{\circ}C$')
    titles = (r'Зміна середньої температури колектора, {} ',
              r'Зміна середньої температури системи геліоколекторів, {} протягом часу',
              r'''Зміна температури в теплообміннику
в контурі геліоколектора, {}, протягом часу''',
              r'''Зміна температури в контурі бака-акумулятора, {},
після теплообмінника до геліоколектора протягом часу''',
              r'''Зміна температури в контурі бака-акумулятора, {},
після бака-акамулятора до теплообмінника протягом часу''',
              r'''Зміна температури в теплообміннику
в контурі бака-аумулятора {}, протягом часу''',
              r'''Зміна температури в контурі бака-акумулятора, {},
після бака-акумулятора до теплообмінника протягом часу''',
              r'Зміна температури в першому шарі, {}, бака-акумулятора',
              r'Зміна температури в другому шарі, {}, бака-акумулятора',
              r'Зміна температури в останньому шарі, {}, бака-акумулятора'
              )
    plt.close('all')
    for i, (yl, title) in enumerate(zip(ylabels, titles)):
        if R == 1:
            if not i:
                rcParams.update({'font.size': 8, 'axes.titlesize' : 7})
                fig = plt.figure()
                gs = gridspec.GridSpec(4, 3) 
                gs.update(left=0.06, right=0.97, wspace=0.2, top=.94, bottom=.05, hspace=.5)
            ax = plt.subplot(gs[i])
        else:
            #if not i:
            #    rcParams.update({'font.size': 14, 'axes.titlesize' : 10, 
            #                     'axes.titleweight':'bold'})
            fig = plt.figure(**fig_data)
            ax = fig.add_subplot(111)
            #if i in (1, 2):
            #    plt.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.1)
        
        x = tau/60
        y = res[...,i]
        
        x_locator_base = 30
        y_locator_base = .5
        
        ax.plot(x, y, lw=3)
        
        x_min = np.floor(min(x))
        x_min_delta = x_min % x_locator_base
        if x_min_delta:
            x_min -= x_min_delta
        x_max = np.ceil(max(tau/60))
        x_max_k, x_max_delta = divmod(x_max, x_locator_base)
        if x_max_delta:
            x_max = x_locator_base * (x_max_k+1)
        locator_x = ticker.MultipleLocator(base=x_locator_base)
        ax.xaxis.set_major_locator(locator_x)
        ax.set_xlim(x_min, x_max)
        
        ax.set_xlabel(r'$\tau, хв$', x=1, ha="right")
        
        y_min = np.floor(min(y))
        y_min_delta = y_min % y_locator_base
        if y_min_delta:
            y_min -= y_min_delta
        y_max_0 = max(y)
        y_max = np.ceil(y_max_0)
        if (y_max - y_locator_base) > y_max_0:
            y_max -= y_locator_base
            
        y_max_k, y_max_delta = divmod(y_max, y_locator_base)
        if y_max_delta:
            y_max = y_locator_base * (y_max_k+1)
        locator_y = ticker.MultipleLocator(base=y_locator_base)
        ax.yaxis.set_major_locator(locator_y)
        ax.set_ylim(y_min, y_max)
        
        ax.set_ylabel(yl, y=1.025, va='bottom', rotation=0)
        
        title = title.format(yl)
        if i == 0:
            title += (r"($t'=%s^{\circ}C, t''=%s^{\circ}C$), протягом часу"
                      % (t_1_gk_i, t_2_gk_i))
        ax.set_title(title, y=1.10)
        ax.spines['top'].set_color(grid_color)
        ax.spines['right'].set_color(grid_color)
        ax.grid(color=grid_color)
        ax.set_position(ax_pos)
        
        if is_print:
            img_name = 'graph_{}.png'.format(i+1)
            dir_name = 'st'
            
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
            
            with open(os.path.join(path_name, 'data.txt'), 'w') as f:
                for row in res:
                    f.write('{}\n'.format('\t'.join([str(v) for v in row])))
            
            plt.savefig(os.path.join(path_name, img_name), format='png')
        
    plt.show()
    
    print('Завдання закінчено!')
