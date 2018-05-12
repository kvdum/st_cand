# -*- coding: utf-8 -*-

'''
Created on 6.03.2018.

@author: ichet
@version: 1.1

Тема: Тепловий розрахунок 2-поверхового сімейного будинку

Економічний розрахунок геліоколектора, його потужність та теплове навантаження
системи теплопостачання. Визначення коефіцієнту заміщення.
'''

import os
import shutil
from datetime import datetime
from dashtable import data2rst
import numpy as np
import sympy as smp
from matplotlib import pyplot as plt, rcParams

rcParams['axes.formatter.use_locale'] = True
rcParams.update({'font.family':'serif', 'mathtext.fontset': 'dejavuserif',
                 'font.size': 12, 'axes.titlesize' : 12})

np.set_printoptions(precision=4)

FLOAT_DEC_4 = '.4f'
IS_SHOW_GRAF = False
DIRECT_PATH = r'C:\Users\ichet\Dropbox\myDocs\St\data_antTermCalc1'
try:
    shutil.rmtree(DIRECT_PATH)
except FileNotFoundError: pass
os.mkdir(DIRECT_PATH)

fig_data = dict(figsize=(12.2, 6.8), dpi=80)
grid_color = '#ABB2B9'

smp.var('R_st R_v R_p R_g R_d q_st q_v q_p q_g q_d R_st_1 R_v_1 R_p_1 R_g_1 R_d_1')
smp.var('dQ_osn')

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
                    spans=[([0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5],
                            [0, 6], [0, 7], [0, 8], [0, 9], [0, 10], [0, 11],
                            [0, 12])], center_cells=True))

def print_table_12_2(label, array_, fmt=None): 
    print(data2rst([[label, '', '', '', '', '', '', '', '', '', '', ''],
                    ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII',
                     'IX', 'X', 'XI', 'XII'], list(array_) if fmt is None else
                     [('{0:%s}' % fmt).format(v) for v in array_] ],
                    spans=[([0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5],
                            [0, 6], [0, 7], [0, 8], [0, 9], [0, 10], [0, 11])],
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

print('Розрахунок виконано: {}.'.format(datetime.strftime(datetime.now(),
                                                          '%d.%m.%Y %H:%M:%S')))    

print(' Вихідні дані: '.center(80, '='))
mis = np.arange(1, 13)
data_dni_mis = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 
                10: 31, 11: 30, 12: 31}
data_t_n_s = {1: -5.0, 2: -4.2, 3: 0.3, 4: 6.7, 5: 12.7, 6: 15.2, 7: 17.4, 8: 16.5,
              9: 13.0, 10: 7.7, 11: 2.4, 12: -2.6} # Середньомісячна температура зовн. пов.
t_v_s = 19   # Середня температура внутрішнього повітря в будинку.
t_z_h5 = -19 # Температура холодної п'ятиденки із забезпеченням 0,92.
fi = 48 # Географічна широта, град.
F_bud = 356.38  # Площа будинку в м^2.
system_vent_var = 3 # № вар., коли починається рекуперація повітря.
system_func = 'c'   # Використання геліоустановки: с - протягом року, s - сезонна.
Q_vent = 9161   # Витрати тепла на вентиляцію.
f = 0.9 # Коефіцієнт рекуперації.

t_gv = 45   # Температура гарячої води, град.С.
a_gv = 105  # Добова витрата гарячої води на 1 особу, л/добу.
data_t_hv = {1: 5, 2: 4, 3: 3, 4: 4, 5: 6, 6: 10, 7: 16, 8: 17, 9: 14, 10: 11,
             11: 8, 12: 6}  # Температура холодної води по місяцях, град.С.
N = 6   # Кількість мешканців у будинку.
fname_climate = r'C:\Users\ichet\Dropbox\myDocs\St\antStepClimaData.txt'
f_z = 0.33    # Ступінь заміщення тепловитрат СГВ.
vartheta = 0.5  # Параметр.
S_0 = 1.723 # площа одного геліоколектору, м^2.
F_r = 1
eta_0 = 0.813   # Оптичний ККД.
UL = 4.6
a = 0.007
b = 1.27 * 10**(-5)
c_pa = 3.16

val_q_st=12455.21
val_q_v=2537.86
val_q_p=4059.11
val_q_g=6248.04
val_q_d=176.82
# Нормативні значення.
val_R_st=2.5
val_R_v=0.56
val_R_p=4.65
val_R_g=4.5
val_R_d=0.56

dni_mis = np.array(list(data_dni_mis.values())) # Дні місяця протягом року.
t_n_s = np.array(list(data_t_n_s.values())) # Середньомісячні температури.
t_hv = np.array(list(data_t_hv.values()))   # Температура холодної води.

print('Середні температури зовнішнього повітря, t_n_s, град.С:')
print_table_12_2('t_n_s, град.С', dni_mis)
print('Середня температура внутрішнього повітря в будинку, t_v_s = {} град.С.'
      .format(t_v_s))
print("Середня температура найхолоднішої п'ятиденки, t_z_h5 = {} град.С."
      .format(t_z_h5))
print('Географічна широта, fi = {} пн. ш.'.format(fi))
print('Загальна площа будинку, F_bud = {} м^2.'.format(F_bud))
print('Номер варіанту, від коли починається рекуперація повітря, № = {}.'.format(
    system_vent_var))
print('Варіант використання геліоустановки: {}.'.format(system_func))
print('Вентиляційні тепловтрати, Q_vent = {} Вт.'.format(Q_vent))
print('Коефіцієнт, f = {}.'.format(f))
print('Температура гарячої води, t_gv = {} град.С.'.format(t_gv))
print('Добова витрата гарячої води на 1 особу, a_gv = {} л/добу.'.format(a_gv))
print('Температура холодної води по місяцях, t_hv, град.С:')
print_table_12_2('t_hv, град.С', t_hv)
print('Кількість мешканців у будинку, N = {}.'.format(N))
print('Шлях до файлу з джерелом кліматичних даних: "{}".'.format(fname_climate))
print('Ступінь заміщення тепловитрат СГВ, f_z = {}.'.format(f_z))
print('Параметр, vartheta = {}.'.format(vartheta))
print('Площа 1-го геліоколектору, S_0 = {} м^2.'.format(S_0))
print('F_r = {}.'.format(F_r))
print('Оптичний к.к.д., eta_0 = {}.'.format(eta_0))
print('UL = {}'.format(UL))
print('a = {}, b = {}.'.format(a, b))
print('c_pa = {}.'.format(c_pa))

c_pv=4.19   # Питома теплоємність води, КДж/(кг*К).
ro_v = 1000 # Густина води за нормальних умов, кг/м^3.

print(' Розрахунки: '.center(80, '='))
Eq_dQ_osn = smp.Eq(dQ_osn, q_st * (1/R_st - 1/R_st_1) + q_v * (1/R_v - 1/R_v_1) + 
                   q_p * (1/R_p - 1/R_p_1) + q_g * (1/R_g - 1/R_g_1) + q_d * 
                   (1/R_d - 1/R_d_1))
print('Зміна максимальних основних тепловтрат будинку, dQ_osn, Вт, залежно '
      'від коефіцієнтів тепловтрат захищень, K, Вт/(м^2*град.С), визначаються '
      'за формулою:')
print(Eq_dQ_osn)

print('Введені максимальні витрати тепла захищеннями будинку '
      'при K = 1 Вт/(м^2*град.С), q, м^2*град.С:')
print(data2rst([['Огородження', 'Позначення', 'q, м^2*град.С'],
                ['Зовнішні стіни', q_st, val_q_st],
                ['Вікна', q_v, val_q_v],
                ['Підвальне перекриття', q_p, val_q_p],
                ['Горищне перекриття', q_g, val_q_g],
                ['Вхідні двері', q_d, val_q_d]], center_cells=True))
print('Введені нормативні опори теплопередачі захищень будинку, R, (м^2*град.С)/Вт:')
print(data2rst([['Огородження', 'Позначення', 'R, (м^2*град.С)/Вт'],
                ['Зовнішні стіни', R_st, val_R_st],
                ['Вікна', R_v, val_R_v],
                ['Підвальне перекриття', R_p, val_R_p],
                ['Горищне перекриття', R_g, val_R_g],
                ['Вхідні двері', R_d, val_R_d]], center_cells=True))

# Основні максимальні тепловтрати будинку.
val_R_st_1 = smp.oo
val_R_v_1 = smp.oo
val_R_p_1 = smp.oo
val_R_g_1 = smp.oo
val_R_d_1 = smp.oo

val_Q_osn = round(Eq_dQ_osn.subs({q_st: val_q_st, R_st: val_R_st, R_st_1: val_R_st_1,
                            q_v: val_q_v, R_v: val_R_v, R_v_1: val_R_v_1,
                            q_p: val_q_p, R_p: val_R_p, R_p_1: val_R_p_1,
                            q_g: val_q_g, R_g: val_R_g, R_g_1: val_R_g_1,
                            q_d: val_q_d, R_d: val_R_d, R_d_1: val_R_d_1}).rhs)
print('Основні максимальні тепловитрати будинку, Q_osn = {} Вт.'.format(val_Q_osn))

# Варіанти реальних значень.
val_R_st_1 = np.array([5, 6.0, 7.5, 10])
val_R_v_1 = np.array([0.75, 0.85, 1.0, 1.25])
val_R_p_1 = np.array([5.5, 6.0, 6.5, 7.3])
val_R_g_1 = np.array([6, 7.0, 8.0, 10])
val_R_d_1 = np.array([0.75, .85, 1.0, 1.25])

N_var = len(val_R_st_1) + 1 # Кількість варіантів.

print('Варіанти термічних опорів захищень:')
print(data2rst([['№ вар.', 'R_st_1,\n(м^2*град.С)/Вт', 'R_v_1,\n(м^2*град.С)/Вт',
                 'R_p_1,\n(м^2*град.С)/Вт', 'R_g_1,\n(м^2*град.С)/Вт',
                 'R_d_1,\n(м^2*град.С)/Вт'],
                 *[[int(x[0]), *list(x[1:])] for x in (np.vstack(
                     (np.arange(2, 1+N_var),
                                                val_R_st_1,
                                                val_R_v_1,
                                                val_R_p_1,
                                                val_R_g_1,
                                                val_R_d_1)).transpose())]],
                 center_cells=True))

print('Зміна максимальних основних тепловтрат, dQ_osn, Вт:')
temp_Eq_dQ_osn = Eq_dQ_osn.subs({q_st: val_q_st, q_v: val_q_v, q_p: val_q_p,
                                 q_g: val_q_g, q_d: val_q_d,
                                 R_st: val_R_st, R_v: val_R_v, R_p: val_R_p,
                                 R_g: val_R_g, R_d: val_R_d})
f_dQ_osn = lambda x: round(temp_Eq_dQ_osn.subs(x).rhs)
vec_dQ_osn = np.vectorize(f_dQ_osn)
val_dQ_osn = vec_dQ_osn([{R_st_1: v[0], R_v_1: v[1], R_p_1: v[2], R_g_1: v[3],
                          R_d_1: v[4]} for v in zip(val_R_st_1, val_R_v_1,
                                                    val_R_p_1, val_R_g_1,
                                                    val_R_d_1)])
print_table_2('dQ_osn, Вт', val_dQ_osn, 2)

print('Витрати тепла на вентиляцію, Q_вент, Вт, (>= {} варіанту) із рекуперацією '
      'теплоти із коефіцієнтом рекуперації f={}:'.format(system_vent_var, f))
val_Q_vent_co = np.array([Q_vent if i < system_vent_var else round((1-f) * Q_vent) 
                                for i in range(1, N_var+1)])
print_table_2('dQ_vent, Вт', val_Q_vent_co)

print('Загальне максимальне навантаження на систему опалення будинку, Q_co, Вт:')
val_Q_op_rz = np.array([val_Q_osn, *(val_Q_osn - val_dQ_osn)]) + val_Q_vent_co
print_table_2('Q_op_rz, Вт', val_Q_op_rz)

print(' Розрахунок помісячного та річного теплового навантаження системи опалення: '
      .center(80, '='))
# Алгоритм для функціонування системи опалення в опалювальний період.
l = np.ones((1, mis.size)); l[..., (3, 9)] = .5; l[..., 4:9] = 0
k = np.ones((N_var, 1)) * l

print('Середньодобове теплове навантаження системи опалення, Q_op_d, кДж, '
      'при середній температурі внутрішнього повітря приміщень t_v_s = {} град.С:'
      .format(t_v_s))
val_Q_op_d = np.around(k * 3.6 * 24 * val_Q_op_rz[..., np.newaxis] / 
                       (t_v_s - t_z_h5) * (t_v_s - t_n_s) )
print_table_13('Q_op_d, кДж', val_Q_op_d)

print('Середньомісячне теплове навантаження, Q_op_mis, кДж:')
val_Q_op_mis = val_Q_op_d * dni_mis
print_table_13('Q_op_mis, кДж', val_Q_op_mis)

print('Річне теплове навантаження на систему опалення, Q_op_r, кДж:')
val_Q_op_r = val_Q_op_d.dot(dni_mis)
print_table_2('Q_op_r, кДж', val_Q_op_r)
del k, l, f_dQ_osn, vec_dQ_osn

print(' Розрахунок теплового навантаження системи гарячого водопостачання: '
      .center(80, '='))
print('Кількість мешканців у будинку N = {} чол.,\nТемпература гарячої води '
      't_gv = {} град.С.'.format(N, t_gv))
print('Норма витрати гарячої води на одну особу a = {} л/добу.'.format(a_gv))

print('Помісячне середньодобове теплове навантаження системи гарячого '
      'водопостачання (СГВ), Q_gv_d, кДж:')
val_Q_gv_d = np.ones((N_var, 1)) * np.around(1.2 * a_gv / 1000 * c_pv * ro_v * 
                                             (t_gv - t_hv) * N)
print_table_13('Q_gv_d, кДж', val_Q_gv_d)

print('Середньомісячне значення потужності системи гарячого водопостачання, '
      'P_gv_mis, кВт:')
val_P_gv_mis = val_Q_gv_d / (3600 * 24)
print_table_13('P_gv_mis, кВт', val_P_gv_mis, fmt=FLOAT_DEC_4)

t_hv_min = t_hv.min(); n = t_hv.argmin()
print('Потужність резервного водонагрівача для n = {} міс. із t_hv_min = {} град.С, '
      'P_rez_mis_max, кВт:'.format(n+1, t_hv_min))
val_P_rez_mis_max = 24 / 6 * val_P_gv_mis[..., n]
print_table_2('P_rez_mis_max, кВт', val_P_rez_mis_max.transpose(), fmt=FLOAT_DEC_4)

print('Місячне навантаження СГВ, Q_gv_mis, кДж:')
val_Q_gv_mis = np.around(val_Q_gv_d * dni_mis)
print_table_13('Q_gv_mis, кДж', val_Q_gv_mis)

print('Річне теплове навантаження на СГВ, Q_gv_r, кДж:')
val_Q_gv_r = val_Q_gv_d.dot(dni_mis)
print_table_2('Q_gv_r, кДж', val_Q_gv_r)
del t_hv_min

print(' Розрахунок сумарного теплового навантаження: '.center(80, '='))

print('Помісячне теплове навантаження системи теплопостачання (СТП), '
      'Q_tm_mis, кДж:')
val_Q_tm_mis = val_Q_op_mis + val_Q_gv_mis
print_table_13('Q_tm_mis, кДж', val_Q_tm_mis)

print('Річне теплове навантаження, Q_tm_r, кДж:')
val_Q_tm_r = val_Q_tm_mis.sum(axis=1)
print_table_2('Q_tm_r, кДж', val_Q_tm_r)

print('Помісячна теплова потужність навантаження СТП, P_tm_mis, кВт:')
val_P_tm_mis = val_Q_tm_mis / (24 * dni_mis * 3600)
print_table_13('P_tm_mis, кВт', val_P_tm_mis, fmt=FLOAT_DEC_4)

print('Максимальна потужність теплового навантаження СТП у '
      "найхолоднішу п'ятиденку, P_tm_max, кВт:")
val_P_tm_max = val_Q_op_rz / 1000 + val_P_gv_mis[..., n]
print_table_2('P_tm_max, кВт', val_P_tm_max, fmt=FLOAT_DEC_4)

print(80*'=')
print('Площа будинку, F_bud = {} м^2.'.format(F_bud))
print('Клас енергосоживання будинку:')
val_Q_e = val_Q_op_mis.sum(axis=1) / (3600 * F_bud)
print_table_2('Q_e', val_Q_e.transpose(), fmt=FLOAT_DEC_4)
class_result = np.vectorize(home_energy_class)(val_Q_e)
print_table_2('Клас енергоспоживання\nбудинку', class_result)
del n

print(' Розрахунок сонячної енергії, яка надходить на горизонтальну поверхню '
      .center(80, '='))

print('Порядковий номер дня в році станом на 15 число кожного місяця m:')
m = 15 + np.append([0], dni_mis[:-1]).cumsum()
print_table_12_2('m', m)

print('Сонячне схилення, яке дорівнює географічній широті місцевості, над '
      'якою в полудень m-го дня Сонце перебуває в зеніті, delta, град:')
delta = 23.45 * np.sin(np.radians((284 + m) / 365 * 360))
print_table_12_2('delta, град', delta.transpose(), fmt=FLOAT_DEC_4)

print('Середнє значення сонячного схилення за період: день, місяць, сезон, рік, '
      '(delta_A + delta_B) / 2 = delta_S, град:')
if system_func == 's':  # сезонно.
    # deltaA - на 15 березня, deltaB - на 15 жовтня, геліосистема функціонує з 
    # 1 березня до 31 жовтня - 8 місяців.
    delta_A = delta[2]; delta_B = delta[9]
    delta_S = (delta_A + delta_B) / 2
else:
    delta_S = 0

print('delta_S = {0:.4f} град'.format(delta_S))

beta = fi - delta_S
print('Оптимальний кут нахилу геліоколктора до горизонту, beta = {0:.4f} град.'
      .format(beta))

print('Азимутальний кут заходу Сонця для горизонтальної площини -A_h, град:')
val_A_h = -(np.degrees(np.arccos(-np.tan(np.radians(fi)) * np.tan(
                                            np.radians(delta)) )))
print_table_12_2('-Ah, град', val_A_h.transpose(), fmt=FLOAT_DEC_4)

print('Азимутальний кут заходу Сонця для випадку, нахиленої площини під кутом '
      'beta до горизонту поверхні ГК -Ab, град:')
val_A_b = -(np.degrees(np.arccos(-np.tan(np.radians(fi-beta)) * 
                                 np.tan(np.radians(delta))) ))
print_table_12_2('-Ab, град', val_A_b.transpose(), fmt=FLOAT_DEC_4)
n = (np.abs(val_A_b) > np.abs(val_A_h))
val_A_b[n] = val_A_h[n]
print_table_12_2('-Ab, град', val_A_b.transpose(), fmt=FLOAT_DEC_4)

print('Допоміжний коефіцієнт R_b перерахунку надходження лише прямої радіації '
      'із значення для горизонтальної поверхні на значення для нахиленої '
      'поверхні під кутом beta до горизонту і ораєнтованої в південному '
      'напрямку R_b:')
val_R_b = ( (np.cos(np.radians(fi-beta)) * np.cos(np.radians(delta)) * 
             np.sin(np.radians(val_A_b)) + np.radians(val_A_b * np.sin(
               np.radians(fi-beta)) * np.sin(np.radians(delta)) )) / 
            (np.cos(np.radians(fi)) * np.cos(np.radians(delta)) * 
             np.sin(np.radians(val_A_h)) + np.radians(val_A_h * 
               np.sin(np.radians(fi)) * np.sin(np.radians(delta)) )) )
print_table_12_2('R_b, град', val_R_b.transpose(), fmt=FLOAT_DEC_4)

print(' Розрахунок кількості радіації, яка надходить на похилий геліоколектор (ГК): '
      .center(80, '='))
print('Коефіцієнт перерахунку, R, надходження сумарної сонячної радіації із '
      'значенням для горизонтальної поверхні на значення для похилої поверхні:')
print('Завантаження даних із файлу "{}" ...'.format(fname_climate))
data_climate = np.loadtxt(fname_climate)[..., 1:]
print('Нижче подана таблиця середньомісячних значень [H_0, r, H_th, H_dh],\nде '
      'H_0 - позаатмосферна радіація, МДж/м^2,\nr - альбедо,\nH_th - середньодобова '
      'повна радіація, МДж/м^2,\nH_dh - розсіяна радіація, МДж/м^2.')
H_th_s = 0; H_dh_s = 0  # Середні значення повної та розсіяної радіації за місяць.
for i in range(3, 12, 2):
    H_th_s += 6 * data_climate[..., i-1] / 30
    H_dh_s += 6 * data_climate[..., i] / 30
data_15 = np.hstack((data_climate[..., (0, 1)], H_th_s[..., np.newaxis],
                     H_dh_s[..., np.newaxis]))
print(data2rst([['Місяць', 'H_0,\nМДж/м^2', 'r', 'H_th,\nМДж/м^2', 'H_dh,\nМДж/м^2'],
                *[[i, *v] for i, v in enumerate(data_15, start=1)]],
                                                 center_cells=True))
H_0 = data_15[..., 0]
r = data_15[..., 1]
H_th = data_15[..., 2]
H_dh = data_15[..., 3]

R = (1 - H_dh / H_th) * val_R_b + H_dh / H_th * (1 + np.cos(np.radians(beta)))/2 + \
        r * (1 - np.cos(np.radians(beta))) / 2
print_table_12_2('R', R, fmt=FLOAT_DEC_4)

print('Середньоденне за місяць надходження сонячної радіації на 1 м^2 похилої '
      'поверхні, H_b_d, МДж/м^2:')
H_b_d = R * H_th
print_table_12_2('H_b_d, МДж/м^2', H_b_d, fmt=FLOAT_DEC_4)

print('Помісячне та річне надходження сонячної радіації на 1 м^2 похилої '
      'поверхні ГК, H_b_mis, МДж/м^2, та H_b_r, МДж/м^2:')
H_b_mis = dni_mis * H_b_d
print_table_12_2('H_b_mis, МДж/м^2', H_b_mis, fmt=FLOAT_DEC_4)
H_b_r = H_b_mis.sum()
print('H_b_r = {0:.4f} МДж/м^2'.format(H_b_r))
I_b_d = H_b_d / (3600 * 24) * 10**6
I_0 = H_0 / (3600 * 24) * 10**6
print(data2rst([['Місяць', 'H_th,\nМДж/м^2', 'H_dh,\nМДж/м^2', 'm', 'delta,\nград',
                 'A_h,\nград', 'A_b,\nград', 'r', 'R_b', 'R', 'H_b_d,\nМДж/м^2',
                 'H_b_mis,\nМДж/м^2', 'H_0,\nВт/м^2', 'H,\nВт/м^2'], 
                 *[[i[0], '{0:.4f}'.format(i[1]), '{0:.4f}'.format(i[2]),
                  i[3], '{0:.4f}'.format(i[4]), '{0:.4f}'.format(i[5]),
                  '{0:.4f}'.format(i[6]), '{0:.4f}'.format(i[7]), 
                  '{0:.4f}'.format(i[8]), '{0:.4f}'.format(i[9]),
                  '{0:.4f}'.format(i[10]), '{0:.4f}'.format(i[11]),
                  '{0:.4f}'.format(i[12]), '{0:.4f}'.format(i[13])] 
                  for i in zip(mis, H_th, H_dh, m, delta, val_A_h, val_A_b, r,
                               val_R_b, R, H_b_d, H_b_mis, I_0, I_b_d)]
                 ], center_cells=True))
del m, n, H_th_s, H_dh_s

print(' Найближчий метод розрахунку площы геліоколекторів (ГК): '.center(80, '='))
H_b_c = H_b_mis.sum()
print('Сумарне надходження сонячної радіації на похилу поверхню ГК за рік, '
      'H_b_c = {0:.4f} МДж/м^2'.format(H_b_c))

print('Сумарне річне теплове навантаження СТ, Q_tm_r, МДж:')
val_Q_tm_r_MJ = val_Q_tm_r / 1000
print_table_2('Q_tm_r, МДж', val_Q_tm_r_MJ, fmt=FLOAT_DEC_4)

print('Сумарна площа геліоколекторів, S, м^2, при ступені заміщення тепловитрат СГВ, '
      'f = {}, та параметру vartheta = {}:'.format(f_z, vartheta))
S = vartheta * val_Q_tm_r_MJ / H_b_c
print_table_2('S, м^2', S, fmt=FLOAT_DEC_4)

print('Кількість стандартних геліоколекторів, k, площею S_0 = {} м^2:'.format(S_0))
k = np.around(S / S_0)
print_table_2('k', k)

print('Реальна площа, S_k, м^2, та коефіцієнт vartheta:')
S_k = k * S_0
vartheta = H_b_c / val_Q_tm_r_MJ * S_k
print_table_2('S_k, м^2', S_k, fmt=FLOAT_DEC_4)
print_table_2('vartheta', vartheta, fmt=FLOAT_DEC_4)

print(' Розрахунок теплопродуктивності сонячних установок: '.center(80, '='))
print('Середньомісячні коефіцієнти ясності, k_j, на 15 число:')
k_j = H_th / H_0
print_table_12_2('k_j', ('{0:.4f}'.format(v) for v in k_j))

print('Середньомісячне значення параметру, P:')
P = np.ones((N_var, 1)) * (t_hv - t_n_s) / k_j
print_table_13('P', P, fmt=FLOAT_DEC_4)

print('Значення оптичних к.к.д., eta, та витрати антифризу, G_gk, кг/год, '
      'із c_pa = {} кДж/(кг*град.С) по місяцях:'.format(c_pa))
eta = np.ones((N_var, 1)) * (F_r * eta_0 - F_r * UL * (t_hv + t_gv - 2*t_n_s) / 
                             (2*I_b_d))
print_table_13('eta', eta, fmt=FLOAT_DEC_4)

G_gk = 3.6 * I_b_d * S_k[..., np.newaxis] * eta / (3.16 * (t_gv - t_hv))
print_table_13('G_gk, кг/год', G_gk, fmt=FLOAT_DEC_4)

print('К.к.д. для найтеплішого місяця:')
t_n_s_max = t_n_s.max(); n = t_n_s.argmax()
I_b_d_tm = I_b_d[n]
eta = smp.S('F_r*eta_0-F_r*UL*(t_hv+t_gv-2*t_n_s)/(2*I_b_d)')
eta_1 = eta.subs({'F_r': F_r, 'eta_0': eta_0, 'UL': UL, 't_gv': t_gv,
                't_hv': t_hv[n], 't_n_s': t_n_s_max, 'I_b_d': I_b_d_tm})
eta_rzr = eta_1
print('Оптичний к.к.д., eta_0 = {3:.4f}, для найтеплішого місяця n = {0} із '
      't_n_s_max = {1:.1f} град.С та I_b_d = {2:.4f} Вт/м^2:'.format(
          n+1, t_n_s_max, I_b_d_tm, eta_1))

print('К.к.д. для найсяянішого місяця:')
I_b_d_max = I_b_d.max(); n_2 = I_b_d.argmax()
t_n_s_I_m = t_n_s[n_2]
if I_b_d_max >= .95*1000:
    eta_2 = eta.subs({'F_r': F_r, 'eta_0': eta_0, 'UL': UL, 't_gv': t_gv,
                't_hv': t_hv[n_2], 't_n_s': t_n_s_I_m, 'I_b_d': I_b_d_max})
    print('Оптичний к.к.д. eta_0 = {3:.4f} для місяця n_2 = {0} із '
          'I_b_d_max = {1:.4f} Вт/м^2 ~ 1000 Вт/м^2 із t_n_s_I_m = {2:.1f} град.С'
          .format(n_2+1, I_b_d_max, t_n_s_I_m, eta_2))
    if eta_2 > eta_1:
        eta_rzr = eta_2
        n = n_2
del n_2

print('Мінімально необхідна продуктивність циркуляційної помпи для '
      'незамерзаючого теплоносія, G, кг/год:')
G_gk = 3.6 * I_b_d_tm * S_k * eta_rzr / (c_pa * (t_gv - t_hv[n]))
print_table_2('G, кг/год', ('{0:.4f}'.format(v) for v in G_gk))

print('Прийнятно колектор із подвійним заскленням і селективно-поглинаючою '
      'поверхнею із коефіцієнтами:\nоптичний к.к.д. eta_0 = {0:.4f}, a = {1:.4f}, '
      'b = {2:.7f}:'.format(eta_0, a, b))
print('Ефективність роботи ГК в реальних умовах експлуатації - питома '
      'теплопродуктивність - середньоденне (протягом місяця) виробництво '
      'теплової енергії 1 м^2 його сприймаючої поверхні, q_gk_d, МДж/м^2:')
q_gk_d = eta_0 * H_b_d * (1 - a*P + b*P**2)
print_table_13('q_gk_d, МДж/м^2', q_gk_d, fmt=FLOAT_DEC_4)

print("Об'єм теплоакумулятора, V_a, м^3:")
V_a = 0.05 * S_k
print_table_2('V_a, м^3', V_a, fmt=FLOAT_DEC_4)
del k, n

print(' Аналіз помісячних балансів енергії: '.center(80, '='))
print('Помісячне виробництво тепла сонячною СГВ, H_gk_mis, МДж, загальною '
      'площею, S_k:')
val_Q_tm_mis_MJ = val_Q_tm_mis / 1000
H_gk_mis = S_k[..., np.newaxis] * q_gk_d * dni_mis
print_table_13('H_gk_mis, МДж', H_gk_mis, fmt=FLOAT_DEC_4)

val_Q_tm_mis_MJ = np.column_stack((val_Q_tm_mis_MJ[..., 0], val_Q_tm_mis_MJ))
H_gk_mis = np.column_stack((H_gk_mis[..., 0], H_gk_mis))
#val_Q_tm_mis_MJ = np.column_stack((val_Q_tm_mis_MJ, val_Q_tm_mis_MJ[..., 11]))
#H_gk_mis = np.column_stack((H_gk_mis, H_gk_mis[..., 11]))

print(' Графік теплового навантаження ТМ протягом року: '.center(80, '='))
f_kw = 3.6 * np.r_[dni_mis, dni_mis[11]] # Перерахунок МДж/міс у кВт*год/добу.
f_kw_1 = 3.6 * dni_mis  # Те ж саме.

for i in range(N_var):
    fig = plt.figure(i, **fig_data)
    fig.canvas.set_window_title('Баланс теплової енергії протягом року.\nВаріант №{}.'
                     .format(i+1))
    ax = fig.add_subplot(111)
    ax.step(np.r_[mis, 13], val_Q_tm_mis_MJ[i] / f_kw, color='b', linestyle='--',
            lw=2, label=r'$\mathrm{Q_{т.м. міс.}}$')
    # Графік виробітку ГК теплової енергії напротязі року.
    ax.step(np.r_[mis, 13], H_gk_mis[i] / f_kw, color='r', lw=2,
            label=r'$\mathrm{H_{гк. міс.}}$')
    
    if i:
        tR_st = val_R_st_1[i-1]; tR_v = val_R_v_1[i-1]; tR_p = val_R_p_1[i-1]
        tR_g = val_R_g_1[i-1]; tR_d = val_R_d_1[i-1]
    else:
        tR_st = val_R_st; tR_v = val_R_v; tR_p = val_R_p
        tR_g = val_R_g; tR_d = val_R_d
    ax.set_title(r'Помісячний виробіток теплової енергії СГК і теплове '
                 'навантаження ТМ:\n'
                 r'$\mathrm{R_{ст}=%.2f\ \frac{м^2\cdot^\circ\!C}{Вт}}$, '
                 r'$\mathrm{R_в=%.2f\ \frac{м^2\cdot^\circ\!C}{Вт}}$, '
                 r'$\mathrm{R_{п}=%.2f\ \frac{м^2\cdot^\circ\!C}{Вт}}$, '
                 r'$\mathrm{R_{г}=%.2f\ \frac{м^2\cdot^\circ\!C}{Вт}}$, '
                 r'$\mathrm{R_{д}=%.2f\ \frac{м^2\cdot^\circ\!C}{Вт}}$' % (tR_st, 
                                                        tR_v, tR_p, tR_g, tR_d))
    ax.set_xlabel('Місяці', x=1, ha="right")
    ax.set_ylabel(r'$\mathrm{Q_{тм. міс.}, кВт\cdotгод}$,' + '\n'
                  r'$\mathrm{H_{гк. міс.}, кВт\cdotгод}$', y=1.025, va='bottom', rotation=0)
    ax.set_xlim(mis[0], mis[-1]+1)
    ax.set_xticks(np.r_[mis, 13])
    ax.spines['top'].set_color(grid_color)
    ax.spines['right'].set_color(grid_color)
    ax.grid(color=grid_color)
    ax.legend(loc='upper center')

print('Визначення різниць, dH_mis, МДж:')
H_gk_mis = H_gk_mis[:, :-1]; val_Q_tm_mis_MJ = val_Q_tm_mis_MJ[:, :-1]
dH_mis = H_gk_mis - val_Q_tm_mis_MJ

for i in range(N_var):
    print(data2rst([['Місяць', 'k_j', 'P', 'q_gk_d,\nМДж/м^2', 'H_gk_mis,\nМДж',
                 'dH_mis,\nМДж'], 
                 *[[i[0], '{0:.4f}'.format(i[1]), '{0:.4f}'.format(i[2]),
                  '{0:.4f}'.format(i[3]), '{0:.4f}'.format(i[4]), '{0:.4f}'.format(i[5])] 
                  for i in zip(mis, k_j, P[i], q_gk_d[i], H_gk_mis[i], dH_mis[i])]
                 ], center_cells=True))
    #continue
    # Зафарбовування надлишку теплової енергії протягом року.
    fig = plt.figure(i)
    ax = fig.axes[0]
    jdH_mis = dH_mis[i] / f_kw_1; jH_gk_mis = H_gk_mis[i] / f_kw_1
    jQ_tm_mis_MJ = val_Q_tm_mis_MJ[i] / f_kw_1
    
    n = (jdH_mis >= 0)
    mis_1 = np.vstack((mis[n], (mis[n]+1) ))
    mis_1 = mis_1.ravel(order='F')
    
    mis_2 = mis_1[::-1]
    H = np.vstack((jH_gk_mis[n], jH_gk_mis[n]))
    H = H.ravel(order='F')
    Q = np.vstack( (jQ_tm_mis_MJ[n], jQ_tm_mis_MJ[n]) )
    Q = Q.ravel(order='F'); Q_2 = Q[::-1]
    
    ax.fill(np.hstack( (mis_1-1, mis_2-1) ), np.hstack( (H, Q_2) ), 
            color=(1, .7, .9))
    plt.savefig(os.path.join(DIRECT_PATH, 'graf_variant-{}.png'.format(i+1)),
                format='png')

print(' Розрахунок завершено! '.center(80, '='))

if IS_SHOW_GRAF:
    plt.show()