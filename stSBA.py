# -*- coding: utf-8 -*-

'''
Created on 4.05.2018.

@author: ichet
'''

import locale
locale.setlocale(locale.LC_ALL, '')
import os
import numpy as np
import shutil
from datetime import datetime
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt, rcParams, ticker

rcParams['axes.formatter.use_locale'] = True
rcParams.update({'font.family':'serif', 'mathtext.fontset': 'dejavuserif',
                 'font.size': 16, 'axes.titlesize' : 16})

GU_SHEMA_1 = 'одноконтурна'
GU_SHEMA_2 = 'двоконтурна'

GU_shema = GU_SHEMA_2 #'одноконтурна'
IS_Q_CP = True
IS_SHOW_GRAF = True
DIRECT_PATH = r'C:\Users\ichet\Dropbox\myDocs\St\Сезонні ВБА'
try:
    # Спочатку видаляється папка.
    shutil.rmtree(DIRECT_PATH)
except FileNotFoundError: pass
os.mkdir(DIRECT_PATH)   # Потім створюється папка.

print('Розрахунок проводиться в {}.'.format(datetime.strftime(datetime.now(),
                                                          '%d.%m.%Y %H:%M:%S')))

np.set_printoptions(precision=2)

fig_data = dict(figsize=(12.5, 6), dpi=100)
grid_color = '#ABB2B9'
ax_pos = (0.09, .23, .88, .71)

def calc_F_N(K_GK, F_GK, G_TN, c_TN, shema, K_TO=None, F_TO=None):
    N_GK = K_GK * F_GK / (G_TN * c_TN)
    if shema == GU_SHEMA_1:
        F_N = 1 - np.exp(-N_GK)
    else:
        N_TO = K_TO * F_TO / (G_TN * c_TN)
        F_N = (1 - np.exp(-N_GK)) * (1 - np.exp(-N_TO)) / (1 - np.exp(-(N_GK + N_TO)))
    return F_N

#tau_1 = tau_c / np.pi * np.arcsin(vartheta_a_)
#tau_2 = tau_c / np.pi * (np.pi - np.arcsin(vartheta_a_))

#Q_day_GK = (7.2 * 10**3 / np.pi * eta_GU * G_TN * c_TN * vartheta_m * tau_c * 
#            F_N * Psi_c * (np.sqrt(1 - vartheta_a_**2) - vartheta_a_ * 
#                           np.arccos(vartheta_a_)))

#F_vartheta_a_ = np.sqrt(1 - vartheta_a_**2) - vartheta_a_ * np.arccos(vartheta_a_)
#Q_day_GK = (7.2 * 10**3 / np.pi * eta_GU * G_TN * c_TN * F_N * vartheta_m * 
#            tau_c * Psi_c * F_vartheta_a_)

#Q_day_BA_losses = 8.64 * 10**4 * lambda_iz / delta_iz * F_iz * vartheta_m * vartheta_a_
#vartheta_turn_ = (t_turn - t_ns) / vartheta_m
#Q_day_consumer = G_consumer * c_a * (vartheta_a_ - vartheta_turn_) * vartheta_m * T_d

def calc_t_a(V_a, t_a_0, E_m, tau_c, Psi_c, t_ns, k, K_GK, gamma_GK, F_GK, F_iz, 
        lambda_iz, delta_iz, G_TN_n, F_N, eta_GU, n, t_post=0, t_turn=None, 
        G_cp=None):
    print('t_a_0', t_a_0)
    vartheta_m = gamma_GK / K_GK * E_m * k
    vartheta_ap_ = (t_a_0 - t_ns) / vartheta_m
    
    vartheta_turn_ = (t_turn - t_ns) / vartheta_m
    T_d = 24    # Тривалість доби, год.
    Q_cp = G_cp * c_a * ((t_a_0 - t_ns) / vartheta_m - vartheta_turn_) * vartheta_m * T_d * n
    
    alpha = 86400 * lambda_iz * F_iz / (delta_iz * V_a * rho * c_a)
    beta = 86400 * G_cp / (V_a * rho)
    delta = Q_cp / (V_a * rho * c_a * vartheta_m)
    
    kappa = 7200 * tau_c * Psi_c / (np.pi * V_a * rho * c_a) * eta_GU * G_TN_n * c_TN * F_N * F_GK
    
    if t_a_0 >= t_post:
        a = .56 * kappa
        b = -(1.59 * kappa + alpha)
        c = kappa - delta
    else:
        a = .56 * kappa
        b = -(1.59 * kappa + alpha + beta)
        c = kappa + beta * vartheta_turn_
    
    D = 4 * a * c - b**2
    
    Z = (2*a * vartheta_ap_ + b - np.sqrt(-D)) / (2*a * vartheta_ap_ + b + 
                                                  np.sqrt(-D)) * np.exp(n * np.sqrt(-D))
    
    vartheta_a_ = (1 + Z) * np.sqrt(-D) / ( (1 - Z) * 2*a ) - b / (2*a)
    t_a = vartheta_m * ( (1 + Z) * np.sqrt(-D) / ((1 - Z) * 2*a) - b / (2*a)) + t_ns
    
    if t_a_0 < t_post and np.abs(t_a_0 - t_a) > .1:
        print('BZEEEMA')
        vartheta_m, vartheta_ap_, kappa, alpha, beta, delta, D, a, b, Z, vartheta_a_, t_a = \
        calc_t_a(V_a, (t_a_0 + t_a) / 2, E_m, tau_c, Psi_c, t_ns, k, K_GK, gamma_GK, F_GK, F_iz, 
        lambda_iz, delta_iz, G_TN_n, F_N, eta_GU, n, t_post, t_turn, 
        G_cp)
    
    return vartheta_m, vartheta_ap_, kappa, alpha, beta, delta, D, a, b, Z, vartheta_a_, t_a

# Розрахунки.
c_a = 4187  # Питома теплоємність теплоносія в БА, Дж/(кг*К)
c_TN = 4187 # Питома теплоємність теплоносія в контурі геліоколектора, Дж/(кг*К) 
rho = 997  # м^3
V_a = 1    # Об'єм БА, м^3
t_a_0 = 25  # Початкова температура води в БА, град. С
#E_m = {1: 723, 2: 669, 3: 784, 4: 834, 5: 943, 6: 959, 7: 1013, 8: 1001, 9: 908,
#       10: 869, 11: 783, 12: 753}#915   # Інтенсивність сонячної радіації, Вт/м^2
E_m = {1: 280, 2: 386, 3: 537, 4: 645, 5: 829, 6: 901, 7: 862, 8: 741, 9: 591, 
       10: 436, 11: 296, 12: 223}
tau_c = {1: 8.86, 2: 10.13, 3: 11.93, 4: 13.22, 5: 15.42, 6: 16.27, 7: 15.81, 
         8: 14.37, 9: 12.57, 10: 10.72, 11: 9.05, 12: 8.18}#15.17 # Тривалість світлового дня, год/добу
Psi_c = {1: .48, 2: .53, 3: .58, 4: .62, 5: .64, 6: .72, 7: .73, 8: .70, 9: .67,
         10: .61, 11: .55, 12: .50}#.55 # Коефіцієнт сонячного сяяння
t_ns = {1: -4.0, 2: -2.7, 3: 1.4, 4: 7.9, 5: 13.4, 6: 16.3, 7: 17.7, 8: 17.2, 
        9: 13.0, 10: 8.0, 11: 2.5, 12: -2.2}#15.4 # Температура навколишнього повітря, град. С
beta_GK = 48    # Кут розташування геліоколектора, град. пн. ш.
Phi_dif = .21
phi = 49.82
r_a = .2
#k = .87 # Коефіцієнт перерахування інтенсивності сонячної радіації.
K_GK = 6.9  # Коефіцієнт тепловтрат, Вт/(м^2*К)
gamma_GK = .72  # Коефцієнт поглинання сонячної радіації.
F_GK = 20#15 # Сумарна площа, м^2.
F_iz = 12.095#75   # Площа поверхні теплообміну, м^2.
lambda_iz = .05#.05 # Коефіцієнт теплопровідності, Вт/(м*К)
delta_iz = .5  # Товщина ізоляції, м.
G_TN = .054 # кг/с.
#F_N = .35
eta_GU = .92    # Коефіцієнт корисної дії геліоустановки.
n = n = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 
         11: 30, 12: 31}#31  # Кількість днів у травні.

if IS_Q_CP:
    t_post = 45 # Температура постачання, град. С
    t_turn = {1: 25, 2: 25, 3: 25, 4: 25, 5: 25, 6: 25, 7: 25, 8: 25, 9: 25,
          10: 25, 11: 25, 12: 25}#10
    G_cp = .018
else:
    t_post = 0
    
    t_turn = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0,
             10: 0, 11: 0, 12: 0}
    
    G_cp = 0

K_TO = 6.9*2.5
F_TO = 6

G_TN_n = G_TN / F_GK
print('G_TN_n = {:.4f} кг/(м^2*с)'.format(G_TN_n))

F_N = calc_F_N(K_GK, F_GK, G_TN, c_TN, GU_shema, K_TO, F_TO)
print('F_N = {:.2f}'.format(F_N))

def calc_t_seson(t_a_0, E_m, tau_c, k, Psi_c, t_ns, n, t_turn, G_TN_n, F_N):
    
    vartheta_m, vartheta_ap_, kappa, alpha, beta, delta, D, a, b, Z, vartheta_a_, t_a = \
      calc_t_a(V_a, t_a_0, E_m, tau_c, Psi_c, t_ns, k, K_GK, gamma_GK, F_GK, F_iz, 
            lambda_iz, delta_iz, G_TN_n, F_N, eta_GU, n, t_post, t_turn, 
            G_cp)
    
    print('vartheta_m = {:.0f} град.С, vartheta_ap = {:.3f}, kappa = {:.5f} 1/добу, '
          'alpha = {:.5f} 1/добу, beta = {:.5f} 1/добу, delta = {:.5f} 1/добу, '
          'D = {:.6f} 1/доба^2, a = {:.6f} 1/доба, b = {:.6f} 1/доба, Z = {:.2f}, '
          'vartheta_a_ = {:.3f}, t_a = {:.1f} град.С'.format(vartheta_m, vartheta_ap_, 
            kappa, alpha, beta, delta, D, a, b, Z, vartheta_a_, t_a))
    
    return t_a

d = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
t_a_list = []
n_days = 0

R_s = [1.5917, 1.4516, 1.3026, 1.0178, 0.9011, 0.8481, 0.8691, 0.9746, 1.1885,
       1.4418, 1.6278, 1.6487]
for i in sorted(E_m.keys()):
    n_days += n[i]
    
    m_d = sum(d[key] for key in range(1, i)) + 15
    Delta = 23.45 * np.sin(np.deg2rad((284 + m_d) / 365 * 360))
    A = np.rad2deg(np.arccos(-np.tan(np.deg2rad(phi - beta_GK)) * np.tan(np.deg2rad(Delta))))
    
    R = ( np.pi*A/180*np.sin(np.deg2rad(Delta))*np.sin(np.deg2rad(phi - beta_GK)) + 
          np.cos(np.deg2rad(Delta))*np.cos(np.deg2rad(phi - beta_GK)) * np.sin(np.deg2rad(A)) ) / \
        ( np.pi*A/180*np.sin(np.deg2rad(Delta))*np.sin(np.deg2rad(phi)) + np.cos(np.deg2rad(Delta))*np.cos(np.deg2rad(phi))*np.sin(np.deg2rad(A)) )
    
    R = R_s[i-1]
    k = (1 - Phi_dif)*R + Phi_dif*(1 + np.cos(beta_GK))/2 + r_a*(1 - np.cos(beta_GK))/2
    
    #k = .87
    
    print('R = {:.2f}'.format(R))
    print('k = {:.2f}'.format(k))
    res = calc_t_seson(t_a_0, E_m[i], tau_c[i], k, Psi_c[i], t_ns[i], 
                                           n[i], t_turn[i], G_TN_n, F_N)
    t_a_list.append( (n_days, res) )

t_a_list = np.array(t_a_list)

xlabel = r'Дні, $\mathrm{n}$'
ylabel = r'$\mathrm{t_a}$, $\mathrm{{}^\circ C}$'

fig = plt.figure(**fig_data)
ax = fig.add_subplot(111)

x = t_a_list[..., 0]
y = t_a_list[..., 1]
x_1 = np.linspace(x.min(), x.max(), 100)
f = interp1d(x, y, kind='cubic')
y_1 = f(x_1)
plt.plot(x_1, y_1, lw=2.5)
plt.plot(x, y, 'o', lw=2.5)
y = y_1

x_locator_base = 30
x_min = np.floor(min(x))
x_min_delta = x_min % x_locator_base
if x_min_delta:
    x_min -= x_min_delta
x_max = np.ceil(max(x))
x_max_k, x_max_delta = divmod(x_max, x_locator_base)
if x_max_delta:
    x_max = x_locator_base * (x_max_k+1)

y_locator_base = 2 if IS_Q_CP else 5
y_min = np.floor(min(y))
y_min_delta = y_min % y_locator_base
if y_min_delta:
    y_min -= y_min_delta
y_max = np.ceil(max(y))
y_max_k, y_max_delta = divmod(y_max, y_locator_base)
if y_max_delta:
    y_max = y_locator_base * (y_max_k+1)

ax.set_xlabel(xlabel, x=1, ha="right")
locator_x = ticker.MultipleLocator(base=x_locator_base)
ax.xaxis.set_major_locator(locator_x)
ax.set_xlim(x_min, x_max)

ax.set_ylabel(ylabel, y=1.025, va='bottom', rotation=0)
locator_y = ticker.MultipleLocator(base=y_locator_base)
ax.yaxis.set_major_locator(locator_y)
ax.set_ylim(y_min, y_max)

ax.set_title(r'Температура теплоносія в тепловому акумуляторі, $\mathrm{t_a}$, '
             r'$\mathrm{{}^\circ C}$', y=-0.32)
ax.spines['top'].set_color(grid_color)
ax.spines['right'].set_color(grid_color)
ax.grid(color=grid_color)
ax.set_position(ax_pos)

plt.savefig(os.path.join(DIRECT_PATH, 'n = {}.png'.format(len(n))), format='png', 
            dpi=fig_data['dpi'])

print(" Розв'язок завершено! ".center(50, '='))

if IS_SHOW_GRAF:
    plt.show()