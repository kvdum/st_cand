'''
Created on 22 трав. 2017 р.

@author: kavedium
'''

import numpy as np
from scipy.integrate import odeint
from sympy import Eq, symbols, Function, dsolve, init_printing, pretty_print, \
    exp as smp_exp
import matplotlib.pyplot as plt

init_printing(use_latex=True)

# 1 колектор.
# Варіант 1:
# Загальні змінні
tau = symbols('tau')
t_n, c_v, I_i = symbols('t_n c_v I_i')

# СГК
# ГК - система геліоколекторів
c_sgk, K_sgk, G_sgk = symbols('c_sgk K_sgk G_sgk')
t_sgk = symbols('t_sgk', cls=Function)

# 1 ГК
c_gk_i, G_gk_i, K_gk_i = symbols('c_gk_i G_gk_i K_gk_i')
t_1_gk_i, t_2_gk_i = symbols('t_1_gk_i t_2_gk_i')
t_gk_i = symbols('t_gk_i', cls=Function)

# 1:
G_I, S_I, H_I = symbols('G_I S_I H_I')

# 2:
c_I_2, K_I_2 = symbols('c_I_2 K_I_2')
t_I_2 = symbols('t_I_2', cls=Function)

# телообмінник ТО
k_B, F_B = symbols('k_B F_B')

c_I_to = symbols('c_I_to')
t_I_to = symbols('t_I_to', cls=Function)

c_II_to, K_II_to = symbols('c_II_to K_II_to')
t_II_to = symbols('t_II_to', cls=Function)

# контур II
G_II = symbols('G_II')

# 1:
c_II_1, K_II_1 = symbols('c_II_1 K_II_1')
t_II_1 = symbols('t_II_1', cls=Function)

# 2:
c_II_2, K_II_2 = symbols('c_II_2 K_II_2')
t_II_2 = symbols('t_II_2', cls=Function)

# На вході в БА:
G_x = symbols('G_x')
t_x = symbols('t_x')

# БА
c_1, K_1 = symbols('c_1 K_1')
t_1 = symbols('t_1', cls=Function)

c_2, K_2 = symbols('c_2 K_2')
t_2 = symbols('t_2', cls=Function)

c_3, K_3 = symbols('c_3 K_3')
t_3 = symbols('t_3', cls=Function)

c_m2, K_m2 = symbols('c_m2 K_m2')
t_m2 = symbols('t_m2', cls=Function)

# На виході до споживача
G_p = symbols('G_p')
t_p = symbols('t_p')

# Перевизначення функцій
eq1 = Eq(t_gk_i(tau).diff(tau), (I_i-(G_gk_i * c_v * (t_1_gk_i - t_2_gk_i) + \
                                   K_gk_i * (t_gk_i(tau) - t_n))) / c_gk_i)

eq2 = Eq(t_sgk(tau).diff(tau), (G_I * c_v * (t_gk_i(tau) - t_sgk(tau)) - \
        (K_sgk * (t_sgk(tau) - t_n) + G_I * c_v * (t_sgk(tau) - t_I_to(tau)) )) \
         /  c_sgk)

eq3 = Eq(t_I_to(tau).diff(tau), G_I * (1 - smp_exp((-k_B*F_B)/G_p)) / c_I_to)

eq4 = Eq(t_I_2(tau).diff(tau), (G_I * c_v * (t_I_to(tau) - t_I_2(tau)) - \
        K_I_2 * (t_I_to(tau) - t_n)) / c_I_2)

eq5 = Eq(t_II_2(tau).diff(tau), (G_II * c_v * (t_m2(tau) - t_II_2(tau)) - \
        K_II_2 * (t_II_2(tau) - t_n)) / c_II_2)

eq6 = Eq(t_II_to(tau).diff(tau), (G_II * c_v * (t_II_to(tau) - t_I_2(tau)) - \
        (K_II_to * (t_II_to(tau) - t_n) + G_I * c_v * \
        (t_II_to(tau) - t_II_2(tau)))) / c_II_to)

eq7 = Eq(t_II_1(tau).diff(tau), (G_II * c_v * (t_II_to(tau) - t_II_1(tau)) - \
        (K_II_1 * (t_II_1(tau) - t_n) + G_II * c_v * \
        (t_II_1(tau) - t_1(tau)))) / c_II_1)

eq8 = Eq(t_1(tau).diff(tau), (G_II * c_v * (t_II_2(tau) - t_1(tau)) - \
        K_1 * (t_1(tau) - t_n) + G_p * c_v * (t_1(tau) - t_p)) / c_1)

eq9 = Eq(t_2(tau).diff(tau), (G_II * c_v * (t_1(tau) - t_2(tau)) - \
        K_2 * (t_2(tau) - t_n)) / c_2)

eq10 = Eq(t_3(tau).diff(tau), (G_II * c_v * (t_2(tau) - t_3(tau)) - \
        K_3 * (t_3(tau) - t_n)) / c_2)

eq11 = Eq(t_m2(tau).diff(tau), (G_II * c_v * (t_3(tau) - t_m2(tau)) + \
        G_x * c_v * (t_x - t_m2(tau)) - K_m2 * (t_m2(tau) - t_n)) / c_m2)

eq12 = Eq(S_I * G_I**2, H_I)

eqs = (eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9, eq10, eq11)#, eq12]

#pretty_print(eq2)

res = dsolve(eqs)
pretty_print(res)

if __name__ == '__main__':
    pass