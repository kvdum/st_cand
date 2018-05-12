#! /usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on 6.07.2017.

@author: ichet
'''

import numpy as np
import sympy as smp



L, T_i_ch, T_pov, T_z, F_i_ch, lambda_, delta, k, alpha_i_ch, c_pr, H = \
  smp.symbols('L T_i_ch T_pov T_z F_i_ch lambda_ delta k alpha_i_ch c_pr, H')
T_pidl = smp.symbols('T_pidl', func=True)
res = smp.solve(c_pr * (T_pidl/100)**4 + lambda_/delta * T_pidl - \
          (k * (T_pov - T_z) + c_pr * (T_i_ch/100)**4 + lambda_/delta * T_z - \
           alpha_i_ch * (T_i_ch - T_pov) * F_i_ch / (H * (H + L))), T_pidl)
smp.pretty_print(res)

#def T_pidl(T_i_ch, H):
 #   for r_i in res:
  #      r_i.subs({L: .63, T_i_ch: 693.15, H: 1.6, T_pov: 294.15, T_z: 254.15, 
   #               F_i_ch: .1, lambda_: 1.2, delta: .3, k: .5, alpha_i_ch: 3.8, 
    #              c_pr: 108.3})
     #   print('res:', r_i.evalf())

#if __name__ == '__main__':
    #T_pidl(0, 0)