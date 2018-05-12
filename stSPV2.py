#! -*- coding: utf-8 -*-
'''
Created on 21.11.2017.

@author: ichet
'''

import numpy as np
from matplotlib import pyplot as plt

np.set_printoptions(precision=2)

table = np.array([
         [1,    0,  12, 45,     42.9],
         [2,    0,  12, 42.9,   40.8],
         [3,    0,  11, 40.8,   38.9],
         [4,    0,  11, 38.9,   37.0],
         [5,    0,  13, 37.0,   34.8],
         [6,    0,  14, 34.8,   32.5],
         [7,    0,  18, 32.5,   29.6],
         [8,    0,  21, 29.6,   26.2],
         [9,    21, 20, 26.2,   26.3],
         [10,   41, 20, 26.3,   29.6],
         [11,   60, 18, 29.6,   36.2],
         [12,   75, 16, 36.2,   45.5],
         [13,   77, 14, 45.5,   55.4],
         [14,   68, 14, 55.4,   63.8],
         [15,   48, 13, 63.8,   69.1],
         [16,   25, 18, 69.1,   69.9],
         [17,   2,  22, 69.9,   66.4],
         [18,   0,  24, 66.4,   63.2],
         [19,   0,  18, 63.2,   59.7],
         [20,   0,  20, 59.7,   56.3],
         [21,   0,  15, 56.3,   53.7],
         [22,   0,  11, 53.7,   51.7],
         [23,   0,  10, 51.7,   49.9],
         [24,   0,  9,  49.9,   48.3]
        ])
tau = table[..., 0]
Q_u = table[..., 1]
L_u = table[..., 2]
t_s_1 = table[..., 3]
t_s_2 = table[..., 4]

M = 750 # кг
c_p = 4.187 # КДж/кг
Q_ba = M * c_p * (t_s_2 - t_s_1)

#plt.plot(tau, Q_ba, lw=2, color='b')
#plt.plot(tau, np.zeros(tau.size), color='k', lw=1, ls='--')
##plt.plot(tau, L_u)
#plt.title(r'Енергетична акумулююча здатність водяного акумулятора $Q_{ba}$, кДж,'
#          'протягом доби')
#plt.xlabel(r'$\tau$, год')
#plt.ylabel(r'$Q_{ba}$, кДж')

Q_ba_cumsum = np.cumsum(Q_ba)[-1]
f_m = 30*.75
Q_ba_cumsum_7 = Q_ba_cumsum*f_m

f_5 = 3800 / 5200
f_6 = 4700 / 5200
f_7 = 5200
f_8 = 5000 / 5200
f_9 = 3950 / 5200

Q_u_cumsum_7 = np.cumsum(Q_u)[-1] * f_m
Q_u_cumsum_5 = Q_u_cumsum_7 * f_5
Q_u_cumsum_6 = Q_u_cumsum_7 * f_6
Q_u_cumsum_8 = Q_u_cumsum_7 * f_8
Q_u_cumsum_9 = Q_u_cumsum_7 * f_9

l_5 = 1.25
l_6 = 1.05
l_7 = 1
l_8 = 1.05
l_9 = 1.15

L_u_cumsum_7 = np.cumsum(L_u)[-1] * f_m
L_u_cumsum_5 = L_u_cumsum_7 * l_5
L_u_cumsum_6 = L_u_cumsum_7 * l_6
L_u_cumsum_8 = L_u_cumsum_7 * l_8
L_u_cumsum_9 = L_u_cumsum_7 * l_9

dQ_k_7_cumsum = Q_u_cumsum_7 - L_u_cumsum_7

Q_ba_cumsum_5 = Q_u_cumsum_5 - L_u_cumsum_5 - dQ_k_7_cumsum
Q_ba_cumsum_6 = Q_u_cumsum_6 - L_u_cumsum_6 - dQ_k_7_cumsum
Q_ba_cumsum_8 = Q_u_cumsum_8 - L_u_cumsum_8 - dQ_k_7_cumsum
Q_ba_cumsum_9 = Q_u_cumsum_9 - L_u_cumsum_9 - dQ_k_7_cumsum

#print(Q_u_cumsum_5, L_u_cumsum_5, dQ_k_7_cumsum)
plt.plot([Q_u_cumsum_5, Q_u_cumsum_6, Q_u_cumsum_7, Q_u_cumsum_8,
          Q_u_cumsum_9])

plt.plot([L_u_cumsum_5, L_u_cumsum_6, L_u_cumsum_7, L_u_cumsum_8,
          L_u_cumsum_9])

#tau_m = 90 * 

plt.show()
