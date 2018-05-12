# -*- coding: utf-8 -*-

'''
Created on 9.03.2018.

@author: ichet
@version: 1.2.0

Тема: Визначення теплових потоків від системи нетрадиційного теплопостачання 
(методика Львівського державного аграрного університету)
'''

import os
import shutil
from enum import Enum
from datetime import datetime
from dashtable import data2rst
import numpy as np
import sympy as smp

np.set_printoptions(precision=4)

class TargetGraph(Enum):
    no_showsave = 0
    save = 1
    show = 2
    show_and_save = 3

FLOAT_DEC_4 = '.4f'
target_graph = TargetGraph.show_and_save
SHOW_OWN_FRAME = True

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
fname_climate = r'C:\Users\ichet\Dropbox\myDocs\St\antStepClimaData.txt'
mis = np.arange(1, 13)
data_dni_mis = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 
                10: 31, 11: 30, 12: 31}
# СО:
t_z_h5 = -22 # Температура холодної п'ятиденки із забезпеченням 0,92.
data_t_n_s = {1: -6.1, 2: -5.6, 3: -0.7, 4: 7.2, 5: 14.3, 6: 17.6, 7: 18.8, 8: 17.7,
              9: 13.7, 10: 7.2, 11: 1.0, 12: -3.7} # Середньомісячна температура зовн. пов.
q_0 = 0.5   # Питома потужність тепловитрат, Вт/(м^3*град.С).
V_bud = 480 # Об'єм будинку по зовнішніх обмірах, м^3.
# СГВ:
N = 6   # Кількість мешканців у будинку.
data_t_hv = {1: 5, 2: 4, 3: 3, 4: 4, 5: 6, 6: 10, 7: 16, 8: 17, 9: 14, 10: 11,
             11: 8, 12: 6}  # Температура холодної води по місяцях, град.С.
t_gv = 45   # Температура гарячої води, град.С.
a_gv = 35   # Добова витрата гарячої води на 1 особу, л/добу.
# Геліоколектор:
fi = 48 # Географічна широта, град. пн. ш.
f_z = 0.8    # Ступінь заміщення тепловитрат СГВ.
vartheta = 1.7  # Параметр.
S_0 = 1.723 # площа одного геліоколектору, м^2.
F_r = 1
eta_0 = 0.813   # Оптичний ККД.
UL = 4.6
a = 0.007
b = 1.27 * 10**(-5)
c_pa = 3.16
# Теплова помпа:
tip_tp = 'WW110'
P_tp = 14.1 # Потужність, кВт.
epsilon_tp = 5.5    # Тепловий к.к.д.
epsilon_el = 0.88   # Електричний к.к.д.
P_el = 2.6  # Потужність електрична, кВт.
t_co_1 = 35 # Температура нагрітої води для СО підлоги, град.С.
t_co_2 = 30 # Температура охолодженої води для СО підлоги, град.С.
eta_K = 0.93    # К.к.д згоряння палива.
Q_n_r = 35600   # Нижча теплота згоряння палива, кДж/м^3.
c_gaz = 0.55    # Вартість 1 м^3 газу, грн/м^3.
c_el = 0.25     # Вартість 1 кВт*год, грн/(кВт*год).
# Ґрунт і контур СО підлоги:
data_t_gru = {1: 9.5, 2: 7.6, 3: 6.6, 4: 6.6, 5: 7.4, 6: 8.3, 7: 10.4, 8: 11.9,
              9: 12.8, 10: 13.2, 11: 12.7, 12: 11.4}    # Т-ра ґрунту, град.С.
q_gru = 21  # Питома тепловіддача ґрунту, Вт/м^2.
d = 25  # Внутрішній діаметр поліетиленової труби, мм.
l_0 = 1.7   # Питома довжина тепловідбору, м/м^2.

dni_mis = np.array(list(data_dni_mis.values())) # Дні місяця протягом року.
t_n_s = np.array(list(data_t_n_s.values())) # Середньомісячні температури.
t_hv = np.array(list(data_t_hv.values()))   # Температура холодної води.
t_gru = np.array(list(data_t_gru.values()))   # Температура ґрунту.

print('Шлях до файлу з джерелом кліматичних даних: "{}".'.format(fname_climate))

print('**** СО: ****')
print("Середня температура найхолоднішої п'ятиденки, t_z_h5 = {} град.С."
      .format(t_z_h5))
print('Середні температури зовнішнього повітря, t_n_s, град.С:')
print_table_12_2('t_n_s, град.С', dni_mis)
#print('Середня температура внутрішнього повітря в будинку, t_v_s = {} град.С.'
#      .format(t_v_s))
print('Питома потужність тепловитрат, q_0 = {} Вт/(м^3*град.С).'.format(q_0))
print("Об'єм будинку по зовнішніх обмірах, V_bud = {} м^3.".format(V_bud))

print('**** СГВ: ****')
print('Кількість мешканців у будинку, N = {}.'.format(N))
print('Температура холодної води по місяцях, t_hv, град.С:')
print_table_12_2('t_hv, град.С', t_hv)
print('Температура гарячої води, t_gv = {} град.С.'.format(t_gv))
print('Добова витрата гарячої води на 1 особу, a_gv = {} л/добу.'.format(a_gv))

print('**** Геліоколектор: ****')
print('Географічна широта, fi = {} пн. ш.'.format(fi))
print('Ступінь заміщення тепловитрат СГВ, f_z = {}.'.format(f_z))
print('Параметр, vartheta = {}.'.format(vartheta))
print('Площа 1-го геліоколектору, S_0 = {} м^2.'.format(S_0))
print('F_r = {}.'.format(F_r))
print('Оптичний к.к.д., eta_0 = {}.'.format(eta_0))
print('UL = {}'.format(UL))
print('a = {}, b = {}.'.format(a, b))
print('c_pa = {}.'.format(c_pa))

print('**** Теплова помпа (ТП): ****')
print('Тип: ', tip_tp)
print('Теплова потужність, P_tp = {} кВт.'.format(P_tp))
print('Тепловий к.к.д, epsilon_tp = {}.'.format(epsilon_tp))
print('Електричний к.к.д., epsilon_el = {}.'.format(epsilon_el))
print('Електрична потужність, P_el = {} кВт.'.format(P_el))
print('Т-ра нагрітої води для СО підлоги, t_co_1 = {} град.С.'.format(t_co_1))
print('Т-ра охолодженої води для СО підлоги, t_co_2 = {} град.С.'.format(t_co_2))
print('К.к.д. згоряння палива, eta_K = {}.'.format(eta_K))
print('Нижча теплота згоряння палива, Q_n_r = {} кДж/м^3.'.format(Q_n_r))
print('Вартість 1 м^3 газу, c_газ = {} грн/м^3.'.format(c_gaz))
print('Вартість 1 кВт*год, c_el = {} грн/(кВт*год).'.format(c_el))

print('**** Ґрунт і контур СО підлоги: ****')
print('Температура ґрунту по місяцях, t_gru, град.С:')
print_table_12_2('t_gru, град.С', t_gru)
print('Питома тепловіддача ґрунту, q_gru = {} Вт/м^2.'.format(q_gru))
print('Внутрішній діаметр, d = {} мм.'.format(d))
print('Питома довжина тепловідбору, l_0 = {} м/м^2.'.format(l_0))

c_pv=4.19   # Питома теплоємність води, КДж/(кг*К).
ro_v = 1000 # Густина води за нормальних умов, кг/м^3.

print(data2rst([['Місяць', 'К-сть\nднів', 't_n_s,\nград.С', 't_hv,\nград.С',
                 't_gru,\nград.С'], 
                 *[[i[0], *i[1:]] for i in zip(mis, dni_mis, t_n_s, t_hv, t_gru)]
                 ], center_cells=True))

print(' Розрахунок теплового навантаження системи опалення: '.center(80, '='))
P_op_max = round(q_0 * V_bud * (18 - t_z_h5))

print('Максимальна потужність системи опалення, P_op_max = {} Вт.'.format(P_op_max))
# Алгоритм для функціонування системи опалення в опалювальний період:
# for j=1:1:12, k(j)=1; if j<4 | j>10, l(j)=1; elseif j==4 | j==10
# l(j)=1/2;k(j)=2; else, l(j)=0; end, end
# Qop_d=round(3.6*24*q0*Vbud*(18-tns).*l.*k)
# Qop_mis=round(Qop_d./k.*dniMis)
print('Середньодобове теплове навантаження системи опалення, Q_op_d, кДж:')
Q_op_d = np.around(3.6 * 24 * q_0 * V_bud * (18 - t_n_s) )
print_table_12_2('Q_op_d, кДж', Q_op_d)

print('Середньомісячне теплове навантаження, Q_op_mis, кДж:')
Q_op_mis = Q_op_d * dni_mis
print_table_12_2('Q_op_mis, кДж', Q_op_mis)

Q_op_r = Q_op_d.dot(dni_mis)
print('Річне теплове навантаження на систему опалення, Q_op_r = {} кДж.'.format(
    Q_op_r))

print(' Розрахунок теплового навантаження системи гарячого водопостачання: '
      .center(80, '='))
print('Кількість мешканців у будинку N = {} чол.,\nТемпература гарячої води '
      't_gv = {} град.С.'.format(N, t_gv))
print('Норма витрати гарячої води на одну особу a = {} л/добу.'.format(a_gv))

print('Помісячне середньодобове теплове навантаження системи гарячого '
      'водопостачання (СГВ), Q_gv_d, кДж:')
Q_gv_d = np.around(1.2 * a_gv / 1000 * c_pv * ro_v * (t_gv - t_hv) * N)
print_table_12_2('Q_gv_d, кДж', Q_gv_d)

print('Середньомісячне значення потужності системи гарячого водопостачання, '
      'P_gv_mis, кВт:')
P_gv_mis = Q_gv_d / (3600 * 24)
print_table_12_2('P_gv_mis, кВт', P_gv_mis, fmt=FLOAT_DEC_4)

t_hv_min = t_hv.min(); n = t_hv.argmin()
print('Потужність резервного водонагрівача для n = {} міс. із t_hv_min = {} град.С, '
      'P_rez_mis_max, кВт:'.format(n+1, t_hv_min))
P_rez_mis_max = 24 / 6 * P_gv_mis[..., n]
print('P_rez_mis_max = {0:.4f} кВт.'.format(P_rez_mis_max))

print('Місячне навантаження СГВ, Q_gv_mis, кДж:')
Q_gv_mis = np.around(Q_gv_d * dni_mis)
print_table_12_2('Q_gv_mis, кДж', Q_gv_mis)

Q_gv_r = Q_gv_d.dot(dni_mis)
print('Річне теплове навантаження на СГВ, Q_gv_r = {} кДж.'.format(Q_gv_r))
del t_hv_min

print(' Розрахунок сумарного теплового навантаження: '.center(80, '='))

print('Помісячне теплове навантаження системи теплопостачання (СТП), '
      'Q_tm_mis, кДж:')
Q_tm_mis = Q_op_mis + Q_gv_mis
print_table_12_2('Q_tm_mis, кДж', Q_tm_mis)

Q_tm_r = Q_tm_mis.sum()
print('Річне теплове навантаження, Q_tm_r = {} кДж.'.format(Q_tm_r))

print('Помісячна теплова потужність навантаження СТП, P_tm_mis, кВт:')
P_tm_mis = Q_tm_mis / (24 * dni_mis * 3600)
print_table_12_2('P_tm_mis, кВт', P_tm_mis, fmt=FLOAT_DEC_4)

P_tm_max = P_op_max / 1000 + P_gv_mis[n]
print('Максимальна потужність теплового навантаження СТП у '
      "найхолоднішу п'ятиденку, P_tm_max = {0:.4f} кВт.".format(P_tm_max))
del n

print(80*'=')
print('Таблиця розрахунку теплових навантажень гібридної системи теплопостачання:')
P_rez_mis_max = np.repeat(P_rez_mis_max, 12)
M = np.c_[t_n_s, t_hv, Q_op_d/1000, Q_op_mis/1000, Q_gv_d/1000, Q_gv_mis/1000,
          Q_tm_mis/1000, np.around(P_gv_mis, 3), np.around(P_rez_mis_max, 3),
          np.around(P_tm_mis, 3)].transpose()
L = np.zeros(11); L[4] = Q_op_r/1000; L[6] = Q_gv_r/1000; L[7] = Q_tm_r/1000
table_labels = ('t_n_s,\nград.С', 't_hv,\nград.С', 'Q_op_d,\nМДж', 
                 'Q_op_mis,\nМДж', 'Q_gv_d,\nМДж', 'Q_gv_mis,\nМДж', 'Q_tm_mis,\nМДж',
                 'P_gv_mis,\nкВт', 'P_rez_mis_max,\nкВт', 'P_tm_mis,\nкВт')
spans = [([0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9],
          [0, 10], [0, 11], [0, 12], [0, 13]),
          ([0, 0], [1, 0]), ([0, 1], [1, 1]), ([0, 14], [1, 14])]

print(data2rst([['№', 'Назва\nвеличини', 'Місяці', '', '', '', '', '', '', '', '',
                 '', '', '', ''],
                 ['', '', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX',
                  'X', 'XI', 'XII', ''],
                 *[[i+1, label, item[0], item[1], item[2], item[3], item[4], item[5],
                  item[6], item[7], item[8], item[9], item[10], item[11], l] 
                    for i, (label, item, l) in enumerate(zip(table_labels, M, L))]
                  ], spans=spans, center_cells=True))

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
# deltaA - на 15 березня, deltaB - на 15 жовтня, геліосистема функціонує з 
# 1 березня до 31 жовтня - 8 місяців.
delta_A = delta[2]; delta_B = delta[9]
delta_S = (delta_A + delta_B) / 2
print('delta_S = {0:.4f} град'.format(delta_S))

beta = fi - delta_S
print('Оптимальний кут нахилу геліоколктора до горизонту, beta = {0:.4f} град.'
      .format(beta))

print('Азимутальний кут заходу Сонця для горизонтальної площини -A_h, град:')
A_h = -(np.degrees(np.arccos(-np.tan(np.radians(fi)) * np.tan(
                                            np.radians(delta)) )))
print_table_12_2('-Ah, град', A_h.transpose(), fmt=FLOAT_DEC_4)

print('Азимутальний кут заходу Сонця для випадку, нахиленої площини під кутом '
      'beta до горизонту поверхні ГК -Ab, град:')
A_b = -(np.degrees(np.arccos(-np.tan(np.radians(fi-beta)) * 
                                 np.tan(np.radians(delta))) ))
print_table_12_2('-Ab, град', A_b.transpose(), fmt=FLOAT_DEC_4)
n = (np.abs(A_b) > np.abs(A_h))
A_b[n] = A_h[n]
print_table_12_2('-Ab, град', A_b.transpose(), fmt=FLOAT_DEC_4)

print('Допоміжний коефіцієнт R_b перерахунку надходження лише прямої радіації '
      'із значення для горизонтальної поверхні на значення для нахиленої '
      'поверхні під кутом beta до горизонту і ораєнтованої в південному '
      'напрямку R_b:')
val_R_b = ( (np.cos(np.radians(fi-beta)) * np.cos(np.radians(delta)) * 
             np.sin(np.radians(A_b)) + np.radians(A_b * np.sin(
               np.radians(fi-beta)) * np.sin(np.radians(delta)) )) / 
            (np.cos(np.radians(fi)) * np.cos(np.radians(delta)) * 
             np.sin(np.radians(A_h)) + np.radians(A_h * 
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
                  for i in zip(mis, H_th, H_dh, m, delta, A_h, A_b, r,
                               val_R_b, R, H_b_d, H_b_mis, I_0, I_b_d)]
                 ], center_cells=True))
del m, n, H_th_s, H_dh_s

print(' Найближчий метод розрахунку площі геліоколекторів (ГК): '.center(80, '='))
H_b_c = H_b_mis[2:10].sum()
print('Сумарне надходження сонячної радіації на похилу поверхню ГК за сезонний '
      'період - 8 місяців, H_b_c = {0:.4f} МДж/м^2'.format(H_b_c))

Q_gv_c_MJ = Q_gv_mis[2:10].sum() / 1000
print('Сумарне сезонне теплове навантаження СГВ, Q_gv_c = {0:.4f} МДж.'.format(
    Q_gv_c_MJ))

S = vartheta * Q_gv_c_MJ / H_b_c
print('Сумарна площа геліоколекторів, S = {0:.4f} м^2, при ступені заміщення '
      'тепловитрат СГВ, f = {1}, та параметру vartheta = {2}:'.format(
          S, f_z, vartheta))

k = int(round(S / S_0))
print('Кількість стандартних геліоколекторів, k = {}, площею S_0 = {} м^2:'
      .format(k, S_0))

S_k = k * S_0
vartheta = H_b_c / Q_gv_c_MJ * S_k
print('Реальна площа, S_k = {0:.4f} м^2, та коефіцієнт vartheta = {1:.4f}.'
      .format(S_k, vartheta))

print(' Розрахунок теплопродуктивності сонячних установок: '.center(80, '='))
print('Середньомісячні коефіцієнти ясності, k_j, на 15 число:')
k_j = H_th / H_0
print_table_12_2('k_j', ('{0:.4f}'.format(v) for v in k_j))

print('Середньомісячне значення параметру, P:')
P = (t_hv - t_n_s) / k_j
print_table_12_2('P', P, fmt=FLOAT_DEC_4)

print('Значення оптичних к.к.д., eta, та витрати антифризу, G_gk, кг/год, '
      'із c_pa = {} кДж/(кг*град.С) по місяцях:'.format(c_pa))
eta = F_r * eta_0 - F_r * UL * (t_hv + t_gv - 2*t_n_s) / (2*I_b_d)
print_table_12_2('eta', eta, fmt=FLOAT_DEC_4)

G_gk = 3.6 * I_b_d * S_k * eta / (3.16 * (t_gv - t_hv))
print_table_12_2('G_gk, кг/год', G_gk, fmt=FLOAT_DEC_4)

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

# К.к.д. для найсяянішого місяця
I_b_d_max = I_b_d.max(); n_2 = I_b_d.argmax()
t_n_s_I_m = t_n_s[n_2]
if I_b_d_max >= .95*1000:
    print('К.к.д. для найсяянішого місяця:')
    eta_2 = eta.subs({'F_r': F_r, 'eta_0': eta_0, 'UL': UL, 't_gv': t_gv,
                't_hv': t_hv[n_2], 't_n_s': t_n_s_I_m, 'I_b_d': I_b_d_max})
    print('Оптичний к.к.д. eta_0 = {3:.4f} для місяця n_2 = {0} із '
          'I_b_d_max = {1:.4f} Вт/м^2 ~ 1000 Вт/м^2 із t_n_s_I_m = {2:.1f} град.С'
          .format(n_2+1, I_b_d_max, t_n_s_I_m, eta_2))
    if eta_2 > eta_1:
        eta_rzr = eta_2
        n = n_2
del n_2

G_gk = 3.6 * I_b_d_tm * S_k * eta_rzr / (c_pa * (t_gv - t_hv[n]))
print('Мінімально необхідна продуктивність циркуляційної помпи для '
      'незамерзаючого теплоносія, G = {0:.4f} кг/год.'.format(G_gk))

print('Прийнятно колектор із подвійним заскленням і селективно-поглинаючою '
      'поверхнею із коефіцієнтами:\nоптичний к.к.д. eta_0 = {0:.4f}, a = {1:.4f}, '
      'b = {2:.7f}:'.format(eta_0, a, b))
print('Ефективність роботи ГК в реальних умовах експлуатації - питома '
      'теплопродуктивність - середньоденне (протягом місяця) виробництво '
      'теплової енергії 1 м^2 його сприймаючої поверхні, q_gk_d, МДж/м^2:')
q_gk_d = eta_0 * H_b_d * (1 - a*P + b*P**2)
print_table_12_2('q_gk_d, МДж/м^2', q_gk_d, fmt=FLOAT_DEC_4)

V_a = 0.05 * S_k
print("Об'єм теплоакумулятора, V_a = {0:.4f} м^3.".format(V_a))
del k, n

print(' Аналіз помісячних балансів енергії: '.center(80, '='))
print('Помісячне виробництво тепла сонячною СГВ, H_gk_mis, МДж, загальною '
      'площею, S_k:')

H_gk_mis = S_k * q_gk_d * dni_mis
print_table_12_2('H_gk_mis, МДж', H_gk_mis, fmt=FLOAT_DEC_4)

Q_gv_mis_MJ = Q_gv_mis / 1000
print_table_12_2('Q_gv_mis, МДж', Q_gv_mis_MJ, fmt=FLOAT_DEC_4)

Q_gv_mis_MJ = np.r_[Q_gv_mis_MJ[0], Q_gv_mis_MJ]
H_gk_mis = np.r_[H_gk_mis[0], H_gk_mis]
#Q_gv_mis_MJ = np.r_[Q_gv_mis_MJ, Q_gv_mis_MJ[11]]
#H_gk_mis = np.r_[H_gk_mis, H_gk_mis[11]]

if target_graph != TargetGraph.no_showsave:
    from matplotlib import pyplot as plt, rcParams, ticker

    rcParams['axes.formatter.use_locale'] = True
    rcParams.update({'font.family':'serif', 'mathtext.fontset': 'dejavuserif',
                     'font.size': 14 if SHOW_OWN_FRAME else 10, 
                     'axes.titlesize' : 14 if SHOW_OWN_FRAME else 10})
    DIRECT_PATH = r'C:\Users\ichet\Dropbox\myDocs\St\data_antTetploMonitorDyblanu'
    if target_graph != TargetGraph.show:
        try:
            shutil.rmtree(DIRECT_PATH)
        except FileNotFoundError: pass
        os.mkdir(DIRECT_PATH)
    
    fig_data = dict(figsize=(12.5, 6), dpi=100)
    grid_color = '#ABB2B9'
    ax_pos = (0.12, .15, .8, .78) if SHOW_OWN_FRAME else (0.11, .14, .81, .79)
    
    print(' Графік теплового навантаження СГВ протягом року: '.center(80, '='))
    #f_kw = 3.6 * np.r_[dni_mis, dni_mis[11]] # Перерахунок МДж/міс у кВт*год/добу.
    #f_kw_1 = 3.6 * dni_mis  # Те ж саме.
    
    fig = plt.figure(**fig_data)
    fig.canvas.set_window_title('Баланс теплової енергії протягом року'
                     .format(i+1))
    ax = fig.add_subplot(111)
    line_1, = ax.step(np.r_[mis, 13], 1/3.6*Q_gv_mis_MJ, c='b', linestyle='-', lw=2)
    ax.annotate(r'1', xy=((mis[10]+mis[11])/2, 1/3.6*Q_gv_mis_MJ[11]), 
                xycoords='data', xytext=((mis[11]+12)/2, 1/3.6*Q_gv_mis_MJ[10]), 
                textcoords='data', va='top', ha='left', arrowprops=dict(arrowstyle='-'))
    
    # Графік виробітку ГК теплової енергії напротязі року.
    line_2, = ax.step(np.r_[mis, 13], 1/3.6*H_gk_mis, c='r', linestyle='--', lw=2)
    ax.annotate(r'2', xy=((mis[10]+mis[11])/2, 1/3.6*H_gk_mis[11]), xycoords='data',
                            xytext=((mis[11]+12)/2, 1/3.6*H_gk_mis[10]*3/4), 
                            textcoords='data', va='top', ha='left', 
                            arrowprops=dict(arrowstyle='-'))
    
    #Q_son_r = np.array([  22.2222,   60.5556,  131.9444, 230.,      367.2222,  508.3333,  644.4444,
  #767.2222,  846.9444,  898.3333,  920.5556,  936.1111])
    # Графік місячних значень сонячної радіації на горизонтальну поверхню.
    H_b_mis_GRAF = 1/3.6 * np.r_[H_b_mis[0], H_b_mis] * S_k
    line_3, = ax.step(np.r_[mis, 13], H_b_mis_GRAF, c='orange', linestyle='-.', lw=2)
    ax.annotate(r'3', xy=((mis[10]+mis[11])/2, H_b_mis_GRAF[11]), xycoords='data',
                            xytext=((mis[11]+12)/2, H_b_mis_GRAF[10]*3/4), 
                            textcoords='data', va='top', ha='left', 
                            arrowprops=dict(arrowstyle='-'))
    
    # Для фотофальків.
    Q_fotowalk = .15*1/3.6 * np.r_[H_b_mis[0], H_b_mis] * S_k
    line_4, = ax.step(np.r_[mis, 13], Q_fotowalk, color='g', linestyle=':', lw=2)
    ax.annotate(r'4', xy=((mis[10]+mis[11])/2, Q_fotowalk[11]), xycoords='data',
                            xytext=((mis[11]+12)/2, Q_fotowalk[10]*4/3), 
                            textcoords='data', va='top', ha='left', 
                            arrowprops=dict(arrowstyle='-'))
    
    y_locator_base = 100
    y_max = np.ceil(np.max(np.max([line.get_ydata() for line in (line_1, line_2, 
                                                                 line_3, line_4)])))
    y_max_k, y_max_delta = divmod(y_max, y_locator_base)
    if y_max_delta:
        y_max = y_locator_base * (y_max_k+1)
    ax.set_ylim(0, y_max)
    
    # Тепловтрати.
    ax_2 = ax.twinx()
    ax_2.set_ylabel(r'$\mathrm{Q_{втр}, кВт\cdot год}$', y=1.025, 
                   ha='right', va='bottom', rotation=0)#, color='r')
    #ax2.tick_params('y', colors='r')
    
    Q_tw = 1/3600 * np.r_[Q_op_mis[0], Q_op_mis]
    Q_tw[5:10] = 0
    line_5, = ax_2.plot(np.r_[mis, 13], Q_tw, color='#800000', 
                        linestyle=(0, (3, 1, 1, 1, 1, 1)), lw=2, drawstyle='steps')
    ax_2.annotate(r'5', xy=((mis[10]+mis[11])/2, Q_tw[11]), xycoords='data',
                            xytext=((mis[9]+mis[10])/2, .9*Q_tw[12]), 
                            textcoords='data', va='top', 
                            ha='left', arrowprops=dict(arrowstyle='-'))
    locator_y_2 = ticker.MultipleLocator(base=500)
    ax_2.yaxis.set_major_locator(locator_y_2)
    
    y_locator_base_2 = 500
    y_max_2 = np.ceil(max(Q_tw))
    y_max_k, y_max_delta = divmod(y_max_2, y_locator_base_2)
    if y_max_delta:
        y_max = y_locator_base_2 * (y_max_k+1)
    ax_2.set_ylim(0, y_max_2)
    
    ax.set_title(r'Помісячний виробіток теплової енергії СГК і теплове '
                 'навантаження СГВ', y=-(.19 if SHOW_OWN_FRAME else .17))
    ax.set_xlabel('Місяці', x=1, ha="right")
    ax.set_ylabel(r'$\mathrm{Q_{i}, кВт\cdot год}$', y=1.025, 
                  ha='right' if SHOW_OWN_FRAME else 'left', va='bottom', rotation=0)
    ax.set_xlim(mis[0], mis[-1]+1)
    ax.set_xticks(np.r_[mis, 13])
    ax.spines['top'].set_color(grid_color)
    ax.spines['right'].set_color(grid_color)
    ax.grid(color=grid_color)
    ax.legend(loc=3, ncol=5, mode='expand', bbox_to_anchor=(.05, 1.07, .9, .102),
              handles = [line_1, line_2, line_3, line_4, line_5],
              labels=[r'$\mathrm{Q_{гв\,міс.}}$', r'$\mathrm{Q_{гк.\,міс.}}$',
                      r'$\mathrm{Q_{с.р.\,міс.}}$', r'$\mathrm{Q_{foto_k.\,міс.}}$',
                      r'$\mathrm{Q_{втр.\,міс.}}$'])
    
    ax.set_position(ax_pos)
    ax_2.set_position(ax_pos)
    fig.tight_layout()
    
    print('Визначення різниць, dH_mis, МДж:')
    H_gk_mis = H_gk_mis[:-1]; Q_gv_mis_MJ = Q_gv_mis_MJ[:-1]
    dH_mis = H_gk_mis - Q_gv_mis_MJ
    print_table_12_2('dH_mis, МДж', dH_mis, fmt=FLOAT_DEC_4)
    
    print(data2rst([['Місяць', 'k_j', 'P', 'q_gk_d,\nМДж/м^2', 'H_gk_mis,\nМДж',
                 'dH_mis,\nМДж'], 
                 *[[i[0], '{0:.4f}'.format(i[1]), '{0:.4f}'.format(i[2]),
                  '{0:.4f}'.format(i[3]), '{0:.4f}'.format(i[4]), '{0:.4f}'.format(i[5])] 
                  for i in zip(mis, k_j, P, q_gk_d, H_gk_mis, dH_mis)]
                 ], center_cells=True))
    
    # Зафарбовування надлишку теплової енергії протягом року.
    fig = plt.gcf()
    ax = fig.axes[0]
    #jdH_mis = dH_mis[i] / f_kw_1; jH_gk_mis = H_gk_mis[i] / f_kw_1
    #jQ_tm_mis_MJ = val_Q_tm_mis_MJ[i] / f_kw_1
    
    n = (dH_mis >= 0)
    mis_1 = np.vstack((mis[n], (mis[n]+1) ))
    mis_1 = mis_1.ravel(order='F')
    
    mis_2 = mis_1[::-1]
    H = np.vstack((1/3.6*H_gk_mis[n], 1/3.6*H_gk_mis[n]))
    H = H.ravel(order='F')
    Q = np.vstack( (1/3.6*Q_gv_mis_MJ[n], 1/3.6*Q_gv_mis_MJ[n]) )
    Q = Q.ravel(order='F'); Q_2 = Q[::-1]
    
    ax.fill(np.hstack( (mis_1-1, mis_2-1) ), np.hstack( (H, Q_2) ), 
            color=(1, .7, .9))
    
    if target_graph in (TargetGraph.save, TargetGraph.show_and_save):
        plt.savefig(os.path.join(DIRECT_PATH, 'graf.png'),
                    format='png')
    
    del n, mis_1, mis_2, H, Q, Q_2

print(' Розрахунок параметрів теплової помпи: '.format(80, '='))

P_tp_0 = 1.2 * P_tm_max
print('Номінальна потужність теплової помпи (ТП), P_tp_0 = {0:.4f} кВт.'.format(
                                                                        P_tp_0))
print('Із каталогу вибрана ТП {} із P_тп = {} кВт, к.к.д. epsilon_тп = {}, '
      'P_el = {} кВт при t_gru = {} град.С, яка забезпечує вихідну температуру '
      't_co_1 = {} град.С.'.format(tip_tp, P_tp, epsilon_tp, P_el, t_gru[0], t_co_1))

print('Середньоденна, tau_D, год, та середньомісячна, tau_mis, год, тривалість '
      'роботи ТП:')
tau_D = 24 * P_tm_mis / P_tp
tau_mis = tau_D * dni_mis
print_table_12_2('tau_D,\nгод', tau_D, FLOAT_DEC_4)
print_table_12_2('tau_mis,\nгод', tau_mis, FLOAT_DEC_4)

print('Теплопомпова установка працює з 1 жовтня по 30 квітня - 7 місяців.')
print('Помісячна, W_el_mis, кВт*год, витрата '
      'електроенергії для приводу ТП:')
W_el_mis = tau_mis * P_el
print_table_12_2('W_el_mis, кВт*год', W_el_mis, FLOAT_DEC_4)

W_el_r = W_el_mis[0:4].sum() + W_el_mis[9:12].sum()
print('Річна витрата електроенергії для приводу ТП, W_el_r = {0:.4f} кВт*год'
      .format(W_el_r))

dt_co = t_co_1 - t_co_2
print('Перепад температур підлгового опалення (СО), dt_co = {} град.'.format(dt_co))

G_tp = 3600 * P_tm_max /  (c_pv * dt_co)
print('Витрата теплоносія в СО для підбору циркуляційної помпи, '
      'G_tp = {0:.4f} кг/год.'.format(G_tp))

P_gru = (P_tm_max - P_el) / epsilon_el
print('Необхідна потужність тепловідбору ґрунту, P_гр. = {0:.4f} кВт, при '
      'електричному к.к.д, epsilon_el = {1}.'.format(P_gru, epsilon_el))

S_gru = 1000 * P_gru / q_gru
print('Площа ґрунту, S_гр. = {0:.4f}'.format(S_gru))

l = S_gru * l_0
print('Довжина поліетиленової труби d = {0} мм через питому довжину '
      'тепловідбору, l_0 = {1} м/м^2, - l = {2:.2f} м.'.format(d, l_0, l))
del d, l_0

print(' Аналіз ефективності гібридної системи та висновки: '.format(80, '='))

V_gaz_r = Q_tm_r / (eta_K * Q_n_r)
print("Річний об'єм зекономленого газу, V_gaz_r = {0:.4f} м^3, при "
      'к.к.д., eta_K = {1}, і Q_n_r = {2} кДж/м^3.'.format(V_gaz_r, eta_K, Q_n_r))

B_gaz = V_gaz_r * c_gaz
B_el = W_el_r * c_el
print('Вартість еквівалентної кількості природнього газу, B_газ = {0:.2f} грн, '
      'та електроенергії, B_ел = {1:.2f} грн, при c_газ = {2} грн/м^3 та '
      'c_ел = {3} грн/(кВт*год).'.format(B_gaz, B_el, c_gaz, c_el))

print(' Розрахунок завершено! '.center(80, '='))    
if target_graph in (TargetGraph.show, TargetGraph.show_and_save):
    plt.show()