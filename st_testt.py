# -*- coding: utf-8 -*-

'''
Created on 23.04.2018.

@author: ichet
'''

import locale
locale.setlocale(locale.LC_ALL, '')


import matplotlib.mlab as mlab

import os
from copy import deepcopy
from collections import namedtuple
from datetime import datetime
import shutil
import numpy as np
import scipy.ndimage
import math
from openpyxl import load_workbook
import sympy as smp
import gc

import re
re_sheet_data_pattern = re.compile(r'([A-Za-z]+)([0-9]+[.,]?[0-9]*)')

import matplotlib as mpl
from matplotlib import pyplot as plt, rcParams, ticker
from matplotlib.colors import to_rgb
rcParams['axes.formatter.use_locale'] = True
rcParams.update({'font.family':'serif', 'mathtext.fontset': 'dejavuserif',
                 'font.size': 14, 'axes.titlesize' : 14})

mpl.rcParams['xtick.direction'] = 'out'
mpl.rcParams['ytick.direction'] = 'out'

delta = 0.025
x = np.arange(-3.0, 3.0, delta)
y = np.arange(-2.0, 2.0, delta)
X, Y = np.meshgrid(x, y)
Z1 = mlab.bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
Z2 = mlab.bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
# difference of Gaussians
Z = 10.0 * (Z2 - Z1)


# Create a simple contour plot with labels using default colors.  The
# inline argument to clabel will control whether the labels are draw
# over the line segments of the contour, removing the lines beneath
# the label
plt.figure()
CS = plt.contour(X, Y, Z)
plt.clabel(CS, inline=1, fontsize=10, nchunk=5)
plt.title('Simplest default with labels')

plt.show()