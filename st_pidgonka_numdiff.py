# -*- coding: utf-8 -*-

import locale
locale.setlocale(locale.LC_ALL, '')

import sys, os
import winpaths
import errno
import numpy as np
from scipy.interpolate import interp1d

from matplotlib import pyplot as plt, rcParams, ticker, gridspec
rcParams['axes.formatter.use_locale'] = True
rcParams.update({'font.family':'serif', 'mathtext.fontset': 'dejavuserif',
                 'font.size': 14, 'axes.titlesize' : 14})

np.set_printoptions(precision=3)

dir_name = 'st'

I300 = 300
I600 = 600
I900 = 900

I = I600
is_canonic = False
is_print = True
R = 2

fig_data = dict(figsize=(12.5, 6), dpi=100)
grid_color = '#ABB2B9'
ax_pos = (0.09, .23, .88, .71)
if is_canonic:
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

    with open(os.path.join(path_name, 'data.txt'), 'r') as f:
        data = np.array([[float(v) for v in row.split('\t')] for row in f])
    
    data = data[..., (0, -3, -2, -1)]
    print(data)

    tau = np.linspace(0, 6*60*60, 60)  
else:
    if I == I300:
        xy_t_gk = ( (0, 25), (30, 56.5), (60, 67.5), (90, 70.5),  (120, 71.3), (180, 71.3),
                    (240, 71.3), (300, 71.3), (330, 71.3), (360, 71.3) )
        
        xy_t_1 = ( (0, 25), (30, 35.5), (60, 42.8), (120, 51.5), (180, 55.5),
                   (240, 57.6), (300, 58.8), (330, 58.8), (360, 58.8) )
        
        xy_t_2 = ( (0, 25), (30, 28.8), (60, 33.0), (120, 41.8), (180, 48.5),
                   (240, 52.0), (300, 53.1), (330, 53.4), (360, 53.6) )
        
        
        xy_t_m2 = ( (0, 25), (30, 27.0), (60, 30.0), (120, 37.8), (180, 44.5),
                    (240, 47.5), (300, 48.5), (330, 48.8), (360, 49.1) )
    elif I == I600:
        xy_t_gk = ( (0, 25), (30, 62.3), (60, 74.5), (90, 78.0),  (120, 78.3), (180, 78.3),
                    (240, 78.3), (300, 78.3), (330, 78.3), (360, 78.3) )
        
        xy_t_1 = ( (0, 25), (30, 38.0), (60, 46.5), (120, 57), (180, 64),
                   (240, 68.0), (300, 70.0), (330, 70.2), (360, 70.2) )
        
        xy_t_2 = ( (0, 25), (30, 29.0), (60, 34.5), (120, 47.0), (180, 55.5),
                   (240, 61.0), (300, 64.1), (330, 64.6), (360, 64.8) )
        
        
        xy_t_m2 = ( (0, 25), (30, 27.3), (60, 31.1), (120, 41.5), (180, 50.5),
                    (240, 56.0), (300, 58.9), (330, 59.8), (360, 60.3) )
    elif I == I900:
        xy_t_gk = ( (0, 25), (30, 63.5), (60, 78.0), (90, 83.0),  (120, 84.2), (180, 84.6),
                    (240, 84.6), (300, 84.6), (330, 84.6), (360, 84.6) )
        
        xy_t_1 = ( (0, 25), (30, 40.0), (60, 50.0), (120, 64.0), (180, 73.0),
                   (240, 78.5), (300, 81.0), (330, 81.6), (360, 81.6) )
        
        xy_t_2 = ( (0, 25), (30, 30.0), (60, 36.0), (120, 50.5), (180, 62.5),
                   (240, 70.5), (300, 74.2), (330, 74.9), (360, 75.1) )
        
        
        xy_t_m2 = ( (0, 25), (30, 27.6), (60, 32.3), (120, 44.0), (180, 55.5),
                    (240, 63.2), (300, 67.5), (330, 68.4), (360, 68.6) )
    
    xy = (xy_t_gk, xy_t_1, xy_t_2, xy_t_m2)
    x1 = np.linspace(0, 360, 100)

#raise SystemExit(0)  
ylabels = (r'$\mathrm{t_{гк},\,{}^{\circ}C}$', 
           r'$\mathrm{t_1,\,{}^{\circ}C}$', r'$\mathrm{t_2,\,{}^{\circ}C}$', 
           r'$\mathrm{t_{m_2},\,{}^{\circ}C}$')
titles = (r'Зміна середньої температури колектора, {} ',
          r'Зміна температури в першому шарі, {}, бака-акумулятора',
          r'Зміна температури в другому шарі, {}, бака-акумулятора',
          r'Зміна температури в останньому шарі, {}, бака-акумулятора'
          )

for i, (yl, title) in enumerate(zip(ylabels, titles)):
    if R == 1:
        if not i:
            rcParams.update({'font.size': 10, 'axes.titlesize' : 10})
            fig = plt.figure(figsize=(12.2, 6), dpi=100)
            gs = gridspec.GridSpec(2, 2) 
            gs.update(left=0.06, right=0.97, wspace=0.2, top=.94, bottom=.05, 
                      hspace=.5)
        ax = plt.subplot(gs[i])
    else:
        fig = plt.figure(**fig_data)
        ax = fig.add_subplot(111)
        ax.set_position(ax_pos)
    
    if is_canonic:
        x = tau/60
        y = data[..., i]
        ax.plot(x, y, lw=3)
    else:
        x = []
        y = []
        for x_i, y_i in xy[i]:
            x.append(x_i)
            y.append(y_i) 
        
        f = interp1d(x, y, kind='cubic')
        
        #ax.plot(x, y, 'o', lw=3)
        ax.plot(x1, f(x1), lw=3, color='k')
        
        # Кореляція.
        z = np.polyfit(x, y, 3)
        p = np.poly1d(z)
        eq = str(p)
        #ax.plot(x, [p(k) for k in x], ls='--', lw=3, color='g')
    
    x_locator_base = 30
    y_locator_base = 5
    
    x_min = np.floor(min(x))
    x_min_delta = x_min % x_locator_base
    if x_min_delta:
        x_min -= x_min_delta
    x_max = np.ceil(max(x))
    x_max_k, x_max_delta = divmod(x_max, x_locator_base)
    if x_max_delta:
        x_max = x_locator_base * (x_max_k+1)
    locator_x = ticker.MultipleLocator(base=x_locator_base)
    ax.xaxis.set_major_locator(locator_x)
    ax.set_xlim(x_min, x_max)
    
    ax.set_xlabel(r'$\mathrm{\tau, хв}$', x=1, ha="right")
    
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
                  % (45, 25))
    ax.set_title(title + r'при $\mathrm{I = ' + str(I) + r'\,\frac{Вт}{м^2}}$' + 
                 '\n{}'.format(eq), y=-0.32)#1.10)
    ax.spines['top'].set_color(grid_color)
    ax.spines['right'].set_color(grid_color)
    ax.grid(color=grid_color)
    
    if is_print:
        img_name = 'graph_{}.png'.format(i+1)
        
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