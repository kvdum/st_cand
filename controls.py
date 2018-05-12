# -*- coding: utf-8 -*-

'''
Цей модуль просто було адаптовано до PyQt5
'''

import locale
import sys
import math
from webcolors import hex_to_rgb
import operator

from collections import namedtuple, OrderedDict
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT \
                                                    as NavigationToolbar
import matplotlib as mpl
from matplotlib.figure import Figure

from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QSplitter, QVBoxLayout, QStyleFactory, 
                             QSizePolicy, QLabel, QFrame, QLineEdit)
from PyQt5.QtGui import QPalette, QColor, QDoubleValidator

MCOLORS = ['#990000', '#009900', '#000099', '#999900', '#99004c', '#009999', 
           '#994c00', '#4c9900', '#4c0099', '#00994c', '#990099', '#660000', 
           '#004c99', '#666600', '#006600', '#660033', '#006666', '#330066', 
           '#663300', '#336600', '#000066', '#cc0000', '#006633', '#660066', 
           '#003366', '#00cc00', '#0000cc', '#cc0066', '#cc6600', '#0066cc', 
           '#cc00cc', '#cccc00']

# =============================================================================
def verification(value, vtype=None, lo='>=', minvalue=None, ro='<=', 
                 maxvalue=None, errmsg=''):
    ur'''Перевіряє значення або кількість елементів об'єкту на приналежність 
    діапазону допустимих значень. Вираз порівняння слід представляти так: 
    value lo minvalue та value ro maxvalue. Наприклад: вираз - 
    2 <= 5 <= 10 представляється, як 5 >= 2 та 5 <= 10, де value = 5, 
    minvalue = 2, lo = ">=", maxvalue = 10, ro = "<=".
    Якщо елементами ітераційних об'єктів є також ітераційні об'єкти, то 
    кількість елементів підраховуються лише найвищого рівня, а елементи всіх 
    іншх рівнів ігноруються.
    args:
    - value (int, float, str, unicode, tuple, list, dict, OrderedDict) - 
      перевіряєме значення;
    - vtype (type, tuple=(type1, type2, ..., typeN), list=[type1, type2, ..., 
      typeN]) - int, float, str, unicode, str, tuple, list, dict - 
      контрольний тип (контрольні типи) для значення value. Якщо None, то 
      перевірка value на контрольні типи vtype не відбувається;
    - lo ('str') - >=, >, ==, != - лівий операнд, який прирівнює нижню 
      границю діапазону;
    - minvalue (int, float) - нижня (ліва) границя діапазону. Якщо None, то 
      прирівнювання не відбувається;
    - ro ('str') - <=, < - правий операнд, який прирівнює верхню границю 
      діапазону;
    - maxvalue (int, float) - верхня (права) границя діапазону. Якщо None, то 
      прирівнювання не відбувається;
    - errmsg (str, unicode) - повідомлення-доповнення помилки, якщо value - 
      не в діапазоні допустимих значень.
    Examples:
    1) verification(u'сто', minvalue=2, maxvalue=256) -> 2 <= 3 <= 256;
    2) verification(u'сто', str);
    3) verification(value=16, vtype=(float, int, str), lo='==', minvalue=16, 
       errmsg=u'число') -> 16 == 16;
    4) verification(10.24, float, ro='<', maxvalue=10.25, errmsg=u'число') ->  
       10.24 < 10.25;
    5). verification(5.37, float, '>', 5.36, errmsg=u'число') -> 5.37 > 5.36;
    6). verification(4, int, '>', 3, '<', 5, u'число') -> 3 < 4 < 5.
    '''
    # Перевірка значення на дозволені типи і в разі успіху, за необхідності, 
    # конвертація в порівняльне значення.
    if type(value) in (int, float):
        compvalue = value
    elif isinstance(value, str) or type(value) in (tuple, list, dict, 
                                                          OrderedDict):
        compvalue = len(value)
    else:
        raise ChTypeError(u'Тип value - не int, float, str, unicode, tuple, \
list, dict, OrderedDict!')
    
    # Перевірка типу value контрольним типам vtype, якщо його 
    # значення - не None.
    if not vtype is None:
        if isinstance(vtype, type): vtype = (vtype,)
        
        if not isinstance(value, vtype):
            raise ChValueError(u'Невірний тип! {value:s} має бути {types:s}!'.\
                               format(value=capt_txt(txt=errmsg), 
                                      types=', '.join(str(vt) for vt in vtype))
                               )
    
    # Перевірка операндів на дозволені значення.
    if not lo in ('>=', '>', '==', '!='):
        raise ChValueError(u'Недопустимий лівий операнд порівняння! \
Допустимі значення - ">=", ">", "==", "!=".')
    
    if not ro in ('<=', '<'):
        raise ChValueError(u'Недопустимий правий операнд порівняння! \
Допустимі значення - "<=", "<".')
    
    # Перевірка граничних значень на дозволені типи.
    if not minvalue is None and not type(minvalue) in (int, float):
        raise ChTypeError(u'Тип minvalue може бути int або float.')
    
    if not maxvalue is None and not type(maxvalue) in (int, float):
        raise ChTypeError(u'Тип maxvalue може бути int або float.')
    
    # Перевірка правильності заданих аргументів.
    if not maxvalue is None and minvalue >= maxvalue:
        raise ChValueError(u'Неправильно задано аргументи: \
minvalue = {minvalue:s} не може бути більше або рівне maxvalue = {maxvalue:s}.'.\
        format(minvalue=str(minvalue), maxvalue=str(maxvalue)))
    
    run_lo = True; run_ro = True
    
    if minvalue is None: run_lo = False
    else:
        # Конвертація текстових операторів у функції.
        if lo == '>': lo = operator.gt
        elif lo == '>=': lo = operator.ge
        else:
            maxvalue = None
            if lo == '==': lo = operator.eq
            elif lo ==  '!=': lo = operator.ne
    
    if maxvalue is None: run_ro = False
    else:
        # Конвертація текстових операторів у функції.
        if ro == '<': ro = operator.lt
        elif ro == '<=': ro = operator.le
    
    # Порівняння зліва.
    if run_lo and not lo(compvalue, minvalue):
        
        if lo is operator.gt:
            errcomp = u'не більше'
        elif lo is operator.ge:
            errcomp = u'менше'
        elif lo is operator.eq:
            errcomp = u'не дорівнює'
        elif lo is operator.ne:
            errcomp = u'дорівнює'
        
        raise ChValueError(u'Недопустиме порівняння! {errmsg:s} - {errcomp:s} \
{minvalue:s}.'.format(errmsg=capt_txt(txt=errmsg), errcomp=errcomp, 
                      minvalue=str(minvalue)))
    
    if run_ro and not ro(compvalue, maxvalue):
        
        if ro is operator.lt:
            errcomp = u'не менше'
        elif ro is operator.le:
            errcomp = u'більше'
        
        raise ChValueError(u'Недопустиме порівняння! {errmsg:s} - {errcomp:s} \
{maxvalue:s}.'.format(errmsg=capt_txt(txt=errmsg), errcomp=errcomp, 
                      maxvalue=str(maxvalue)))

# ==============================================================================
class ChMColors():
    ur'''Палітра кольорів в шістнадцятковій системі числення для зафарбовування 
    об'єктів інтерфейсу
    '''
    
    __mcolors = MCOLORS
    
# ------------------------------------------------------------------------------
    def __init__(self, short_format=False):
        ur'''
        args:
        - short_format(bool) - короткий формат представлення в шістнадцятковій 
          системі числення. Наприклад, #4c9900 при True буде 4c9900.
        '''
        
        self.__i = -1
        
        if short_format: self.__mcolors = [mcolor[1:] for mcolor in MCOLORS]
    
# ------------------------------------------------------------------------------
    @property
    def current_color(self):
        ur'''Повертає поточний колір
        
        return: str
        '''
        
        return self.__mcolors[self.__i]
    
# ------------------------------------------------------------------------------
    @property
    def colors(self):
        ur'''Повертає доступні кольори
        return: list
        '''
        
        return self.__mcolors
    
# ------------------------------------------------------------------------------
    @property
    def max_color_index(self):
        ur'''Повертає максимальний індекс кольору
        
        return: int
        '''
        
        return len(self.__mcolors) - 1

# ------------------------------------------------------------------------------
    @property
    def index(self):
        ur'''Повертає поточний індекс вибраного кольору
        
        return: int
        '''
        return self.__i
    
    @index.setter
    def index(self, value):
        ur'''Задає поточний індекс вибраного кольору. Якщо потім використати 
метод next() для отримання кольору з цим індексом, тоді значення слід 
зменшити на 1
        args:
        - value (int) - індекс кольору від -1 до max_color_index
        '''
        if value < len(self.__mcolors):
            self.__i = value
        else:
            raise IndexError(u'Не існує кольору із запитуваним індексом. \
Максимальний індекс може бути %d.' % self.max_color_index)
    
# ------------------------------------------------------------------------------
    @staticmethod
    def get_color_(index, rgb=False):
        ur'''Повертає колір у повному форматі за вказаним індексом.
        Якщо індекс більше max_color_index, повертає колір з індексом, 
        пропорційним len(colors) і є в діапазоні [0, max_color_index]
        args:
        - index(int) - індекс кольору (від 0 до max_color_index);
        - rgb(bool) - при True повертає колір, як tuple, в форматі RGB.
        
        return: str, tuple
        '''
        
        c = MCOLORS[index % len(MCOLORS)]
        if rgb:
            return hex_to_rgb(c)
        else:
            return c

# ------------------------------------------------------------------------------
    def get_color(self, index, rgb=False):
        ur'''Повертає колір за вказаним індексом.
        Якщо індекс більше max_color_index, повертає колір з індексом, 
        пропорційним len(colors) і є в діапазоні [0, max_color_index]
        args:
        - index(int) - індекс кольору (від 0 до max_color_index);
        - rgb(bool) - при True повертає колір, як tuple, в форматі RGB.
        
        return: str
        '''
        
        c = self.__mcolors[index % len(self.__mcolors)]
        if rgb:
            return hex_to_rgb(c)
        else:
            return c

# ------------------------------------------------------------------------------
    def reset(self):
        ur'''Скидає індекс у -1 (не вибране значення)
        '''
        
        self.__i = -1

# ------------------------------------------------------------------------------
    def next(self):
        ur'''Повертає наступний колір.
        Якщо наступний колір виходить за діапазон доступних кольорів, тоді 
        його індекс скидається в 0, і буде повернено перший колір.
        
        return: str
        '''
        
        self.__i += 1
        
        if self.__i >= len(self.__mcolors): self.__i = 0
        
        return self.__mcolors[self.__i]
                      
toolbar_type = namedtuple('toolbar_type', 'ALL PROPERTIES NAVIGATION_TOOLBAR')\
                           ('all', 'properties', 'navigation_toolbar')

DEFAULT_MARKER_NAMES = ['>', '<', 'v', 'd', '^', '*', 'p', '8', 'o', 's', 'h', 
                        'D', 'H', '1', '2', '3', '4', 'x', 'I', '+', '.', 2, \
                        3, 4, 5, 6, 7]

# ==============================================================================
def mpl_syms_to_unicode(text):
    ur'''Заміщає спеціальні символи matplotlib символами unicode
    '''
    return text.replace(u'$^\circ$', u'\u00B0')

# ==============================================================================
class GChGraphWidget(QWidget):
    
# ------------------------------------------------------------------------------
    def __init__(self, figure_canvas, ttoolbar=toolbar_type.ALL, parent=None):
        super(GChGraphWidget, self).__init__(parent=parent)
        
        main_vbox = QVBoxLayout(self)
        
        if ttoolbar != toolbar_type.NAVIGATION_TOOLBAR:
            splitter = QSplitter(QtCore.Qt.Horizontal, self)
            splitter.setStyle(QStyleFactory.create('Cleanlooks'))
            
            self.canvas = ChStaticMplCanvas(splitter)
            splitter.addWidget(self.canvas)
            
            self.properties = GChGraphPoperties(self.canvas, self)
            splitter.addWidget(self.properties)
            
            main_vbox.addWidget(splitter)
        else:
            figure_canvas.setParent(self)
            self.canvas = figure_canvas
            main_vbox.addWidget(self.canvas)
        
        if ttoolbar in (toolbar_type.NAVIGATION_TOOLBAR, toolbar_type.ALL):
            self.toolbar = NavigationToolbar(self.canvas, self)
            main_vbox.insertWidget(0, self.toolbar)

# ==============================================================================
class GChGraphFromNT(QWidget):
    
# ------------------------------------------------------------------------------
    def __init__(self, parent=None):
        super(GChGraphFromNT, self).__init__(parent=parent)
        
        main_vbox = QVBoxLayout(self)
        
        self.canvas = ChStaticMplCanvas(self)
        main_vbox.addWidget(self.canvas)
        
        self.toolbar = NavigationToolbar(self.canvas, self)
        main_vbox.insertWidget(0, self.toolbar)

# ==============================================================================
class ChMplCanvas(FigureCanvas):
    ur'''Базовий клас для створення графіку'''
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        mpl.rcParams['font.family'] = 'serif'
        mpl.rcParams['font.serif'] = 'Times New Roman', 'Ubuntu', 'Arial', \
                                       'Tahoma','Calibri'
        mpl.rcParams['axes.titlesize'] = 'medium'
        mpl.rcParams['axes.formatter.use_locale'] = True
        
        mpl.rcParams['figure.subplot.bottom'] = 0.15
        mpl.rcParams['figure.subplot.left'] = 0.16
        mpl.rcParams['figure.subplot.right'] = 0.86
        mpl.rcParams['figure.subplot.top'] = 0.85#0.75
        
        mpl.rcParams['legend.fontsize'] = 'medium'
        
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        #self.axes.hold(False)
        
        super(ChMplCanvas, self).__init__(fig)
        self.setParent(parent)
        
        self.compute_initial_figure()
        
        self.setSizePolicy(QSizePolicy.Expanding,
                           QSizePolicy.Expanding)
        self.updateGeometry()

# ------------------------------------------------------------------------------
    def compute_initial_figure(self):
        pass

# ==============================================================================
class ChStaticMplCanvas(ChMplCanvas):
    """Simple canvas with a sine plot."""
    
# ------------------------------------------------------------------------------
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super(ChStaticMplCanvas, self).__init__(parent, width, height, dpi)
    
# ------------------------------------------------------------------------------
    def to_plot(self, data, header, subtitle):
        self.axes.clear()
        
        X = []; Y=[]
        
        for i, row in enumerate(data):
            t = row[0]
            
            for k, T in enumerate(row[1:]):
                if not i:
                    X.append([])
                    Y.append([])
                
                if not isinstance(T, str):
                    X[k].append(t)
                    Y[k].append(T)
        
        mcolors = ChMColors()
        for i, (x, y, h) in enumerate(zip(X, Y, header)):
            if i == 0:
                ax = self.axes
                ax.set_ylabel(ur'Теплова потужність, $Q_г$, Вт')#ur'Питома теплопродуктивність, $q_г, \frac{Вт}{м^2}$')
                #ur'''Графіки зміни питомої теплопродуктивності,
#$q_г, \frac{Вт}{м^2}$, та теплової потужності геліопокрівлі
#%s, $Q_г$, Вт'''
                ax.set_title(ur'''Графік зміни теплової потужності
геліопокрівлі %s, $Q_г$, Вт''' \
                  % subtitle, fontweight='bold')
                ax.grid(True, color='gray')
                ax.set_xlabel(u'Час, год.')
            elif i == 1:
                ax = self.axes.twinx()
                ax.set_ylabel(ur'Теплова потужність, $Q_г$, Вт')
            
            lc = mcolors.next()
            mc = [c/255. for c in ChMColors.get_color_(mcolors.index, rgb=True)]
            mc.append(0.4)  # alpha-канал.
            ax.plot(x, y, color=lc, label=h, linewidth=1.5,
                           marker=DEFAULT_MARKER_NAMES[i], markerfacecolor=mc)
        
        xt = [int(v) for v in ax.get_xticks()[:-1]]
        xt.append(math.ceil(ax.get_xticks()[-1]))
        ax.set_xticks(xt)
        if len(X): ax.legend(loc=2, frameon=False, fontsize=9)
        
        self.draw()
    
# ------------------------------------------------------------------------------
    def compute_initial_figure(self): pass
        #import numpy as np
        
        #self.axes.clear()
        #self.axes.grid(self.grid_cb.isChecked())
        
        #t = np.arange(0.0, 3.0, 0.01)
        #self.axes.hold(True)
        
        #for x in xrange(33):
         #   s = t - x/5.
          #  self.axes.plot(t, s)
        
        #self.axes.set_title(u'Графік вимірювань температури з датчиків')
        #self.axes.set_xlabel(u'Час, хв.')
        #self.axes.set_ylabel(u'Температури датчиків, град. C')
        
        #self.draw()


# ==============================================================================
class HStaticLine(QFrame):
    ur'''Горизонтальна лінія для розділення віджетів
    version: 0.2.0
    '''
    
# ------------------------------------------------------------------------------
    def __init__(self, parent=None):
        ur'''
        args:
        - parent(QWidget) - батьківський віджет.
        '''
        
        super(HStaticLine, self).__init__(parent=parent)
        
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

# ==============================================================================
class GChNumLabel(QLabel):
    
# ------------------------------------------------------------------------------
    def __init__(self, num_fmt=r'%.15g', parent=None):
        super(GChNumLabel, self).__init__(u'-', parent=parent)
        
        self.__num_fmt = num_fmt
        self.__as_err = False
        self.__value = None
        self.__foregroundColor = self.palette().color(
                     QPalette.Foreground).name()
        self.setAlignment(QtCore.Qt.AlignRight)
        
        self.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse | 
                                     QtCore.Qt.TextSelectableByKeyboard)
        self.setFrameShape(QFrame.Panel)
        self.setFrameShadow(QFrame.Plain)
        self.setMinimumWidth(100)
    
# ------------------------------------------------------------------------------
    @QtCore.pyqtSlot(float)
    @QtCore.pyqtSlot(int)
    def setNum(self, value):
        self.setText(value)
    
# ------------------------------------------------------------------------------
    @QtCore.pyqtSlot(str)
    def setText(self, text):
        if self.__as_err:
            self.__value = None
            super(GChNumLabel, self).setText(
              u'<font color="red"><b>%s</b></color>' % text)
        else:
            self.__value = int(text) if 'd' in self.__num_fmt or '.0f' in \
              self.__num_fmt else float(self.__num_fmt % float(text))
            super(GChNumLabel, self).setText(u'<font color="%s"><b>%s</b></color>' \
              % (self.__foregroundColor, locale.format(self.__num_fmt, text)))
    
# ------------------------------------------------------------------------------
    @QtCore.pyqtSlot()
    def text(self):
        return str(super(GChNumLabel, self).text()).strip('</b>')
    
# ------------------------------------------------------------------------------
    def value(self):
        return self.__value
        
# ------------------------------------------------------------------------------
    def error(self):
        self.__as_err = True
        self.setText(u'NaN')
        self.__as_err = False
    

# ==============================================================================
class GChNumEdit(QLineEdit):
    ur'''Поле для введення числових даних
    args:
    - value (int, float) - числове значення, яке вводиться в поле;
    - parent (QtGui.QWidget) [None] - батьківський віджет.
    '''
    
    valueChanged = QtCore.pyqtSignal([float], name='valueChanged')
    errorValue = QtCore.pyqtSignal([str], name='errorValue')
    
    def __init__(self, value=0, parent=None):
        verification(value, (float, int), errmsg=u'value')
        
        super(GChNumEdit, self).__init__(str(value), parent=parent)
        
        self.setAlignment(QtCore.Qt.AlignRight)
        
        # Коректує ввід лише чисельних символів.
        self.setValidator(QDoubleValidator(-sys.float_info.max, 
                                                 sys.float_info.max, 
                                                 sys.float_info.dig, self))
        # Ініціалізація палітри за промовчанням.
        self.__appearance = self.palette()
        
        # Обробник події зміни тексту.
        self.textChanged[str].connect(self.__corect_value)

# ------------------------------------------------------------------------------
    def value(self):
        ur'''Повертає числове значення
        
        return: float
        '''
        sep = locale.localeconv()['decimal_point']
        text = self.text()
        text.replace(sep, '.')
        
        return float(text)

# ------------------------------------------------------------------------------
    @QtCore.pyqtSlot(float)
    @QtCore.pyqtSlot(int)
    def setValue(self, value):
        ur'''Приймає числове значення
        args:
        - value (float, int) - числове значення.
        '''
        verification(value, (float, int), errmsg=u'value')
        QLineEdit.setText(self, str(value))
    
# ------------------------------------------------------------------------------
    @QtCore.pyqtSlot(str)    
    def __corect_value(self, text):
        ur'''Коректує значення для обробки події зміни значення і генерує або 
             сигнал зміни значення, або сигнал про введене помилкове значення
        args:
        - text (str) - тектове значення.
        '''
        sep = locale.localeconv()['decimal_point']
        text.replace(sep, '.')
        
        try:
            self.setPalette(self.__appearance)
            self.valueChanged[float].emit(float(text))
        except ValueError:
            palette = QPalette()
            palette.setColor(self.backgroundRole(), 
                             QColor(240, 190, 195))
            self.setPalette(palette)
            self.errorValue[str].emit(text)