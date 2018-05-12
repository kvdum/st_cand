# -*- coding: utf-8 -*-

'''
Created on 9.09.2018.

@author: ichet
'''

import sys

from matplotlib.backends.backend_qt5agg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

from PyQt5.QtCore import Qt, QLibraryInfo, QLocale, QTranslator
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QWidget,\
    QFormLayout, QLineEdit, QSpinBox, QGroupBox, QVBoxLayout, QPushButton,\
    QScrollArea, QSizePolicy, QBoxLayout, QDockWidget
    
from kwConsole import KwConsoleBrowser

class KwMainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        sp = QSizePolicy()
        sp.setHorizontalPolicy(QSizePolicy.Expanding)
        sp.setVerticalPolicy(QSizePolicy.Expanding)
        sp.setVerticalStretch(1)
        
        q_0Edit = QLineEdit()
        V_budEdit = QLineEdit()
        
        NEdit = QSpinBox()
        NEdit.setRange(1, 999)
        NEdit.setSuffix(' чол')
        
        t_gvEdit = QSpinBox()
        t_gvEdit.setRange(25, 70)
        t_gvEdit.setSingleStep(5)
        t_gvEdit.setSuffix(' \N{DEGREE CELSIUS}')
        
        a_gvEdit = QSpinBox()
        a_gvEdit.setRange(15, 99)
        a_gvEdit.setSuffix(' л/добу')
        
        f_zEdit = QLineEdit()
        varthetaEdit = QLineEdit()#1.7)
        S_0Edit = QLineEdit()
        F_rEdit = QLineEdit()#1)
        eta_0Edit = QLineEdit()#0.813)
        ULEdit = QLineEdit()
        aEdit = QLineEdit()
        bEdit = QLineEdit()
        c_paEdit = QLineEdit()
        
        P_tpEdit = QLineEdit()
        epsilon_tpEdit = QLineEdit()
        epsilon_elEdit = QLineEdit()
        P_elEdit = QLineEdit()
        
        t_co_1Edit = QSpinBox()
        t_co_1Edit.setRange(25, 70)
        t_co_1Edit.setSingleStep(5)
        t_co_1Edit.setSuffix(' \N{DEGREE CELSIUS}')
        
        t_co_2Edit = QSpinBox()
        t_co_2Edit.setRange(20, 60)
        t_co_2Edit.setSingleStep(5)
        t_co_2Edit.setSuffix(' \N{DEGREE CELSIUS}')
        
        eta_KEdit = QLineEdit()
        Q_n_rEdit = QLineEdit()
        c_gazEdit = QLineEdit()
        c_elEdit = QLineEdit()
        
        q_gruEdit = QLineEdit()
        d_gruEdit = QSpinBox()
        d_gruEdit.setRange(5, 99)
        d_gruEdit.setSuffix('  мм')
        
        l_0_gruEdit = QLineEdit()
        
        calcButton = QPushButton('Визначити')
        calcButton.setObjectName('calcButton')
        
        outputConsoleBrowser = KwConsoleBrowser(setup={'font': {'name': 
                'Console', 'size': 8}, 'color': 'rgb(255, 255, 255)', 
              'background_color': 'rgba(0, 0, 0, 218)', 'line_wrap': False})
        outputConsoleBrowser.setSizePolicy(sp)
        
        graphWidget = QMainWindow()
        
        self.__graphCanvas = FigureCanvas(Figure(figsize=(5, 3)))
        graphWidget.addToolBar(Qt.TopToolBarArea,
                               NavigationToolbar(self.__graphCanvas, self))
        graphWidget.setCentralWidget(self.__graphCanvas)
        
        soGroup = QGroupBox('Для системи опалення (СО):')
        soInputLayout = QFormLayout(soGroup)
        
        soInputLayout.addRow('Питома потужність тепловтрат, q<sub>0</sub>, '
                             'Вт/(м<sup>3</sup>\N{MIDDLE DOT}\N{DEGREE CELSIUS}):', 
                             q_0Edit)
        soInputLayout.addRow("Об'єм будинку по зовнішніх обмірах, V<sub>буд</sub>, "
                             "м<sup>3</sup>:", V_budEdit)
        
        sgvGroup = QGroupBox(u'Для системи гарячого водопостачання (СГК):')
        sgvInputLayout = QFormLayout(sgvGroup)
        sgvInputLayout.addRow('Кількість мешканців у будинку, N:', NEdit)
        sgvInputLayout.addRow('Температура гарячої води, t<sub>гв</sub>:', t_gvEdit)
        sgvInputLayout.addRow('Добова витрата гарячої води на 1 особу, a<sub>гв</sub>:',
                              a_gvEdit)
        
        sgkGroup = QGroupBox('Для системи геліоколекторів (СГК):')
        sgkInputLayout = QFormLayout(sgkGroup)
        sgkInputLayout.addRow('Ступінь заміщення тепловтрат СГВ, f<sub>з</sub>:', f_zEdit)
        sgkInputLayout.addRow('Параметр, \N{GREEK SMALL LETTER ETA}:', varthetaEdit)
        sgkInputLayout.addRow('Площа 1-го геліоколектора, S<sub>0</sub>, м<sup>2</sup>:',
                              S_0Edit)
        sgkInputLayout.addRow('F<sub>r</sub>:', F_rEdit)
        sgkInputLayout.addRow('Оптичний ККД, \N{GREEK SMALL LETTER ETA}:', eta_0Edit)
        sgkInputLayout.addRow('Коефіцієнт тепловтрат, UL, Вт/(м<sup>2</sup>)'
                              '\N{MIDDLE DOT}\N{DEGREE CELSIUS}):', ULEdit)
        sgkInputLayout.addRow('a:', aEdit)
        sgkInputLayout.addRow('b:', bEdit)
        sgkInputLayout.addRow('c<sub>pa</sub>, кДж/(кг\N{MIDDLE DOT}\N{DEGREE CELSIUS}):',
                              c_paEdit)
        
        tpGroup = QGroupBox('Для теплової помпи (ТП):')
        tpInputLayout = QFormLayout(tpGroup)
        tpInputLayout.addRow('Теплова потужність, P<sub>тп</sub>, кВт:', P_tpEdit)
        tpInputLayout.addRow('Тепловий к.к.д, \N{GREEK SMALL LETTER EPSILON}'
                             '<sub>тп</sub>', epsilon_tpEdit)
        tpInputLayout.addRow('Електричний к.к.д., \N{GREEK SMALL LETTER EPSILON}'
                             '<sub>ел</sub>:', epsilon_elEdit)
        tpInputLayout.addRow('Електрична потужність, P<sub>ел</sub>, кВт:', P_elEdit)
        tpInputLayout.addRow('Т-ра нагрітої води для СО підлоги, t<sub>co 1</sub>:',
                             t_co_1Edit)
        tpInputLayout.addRow('Т-ра охолодженої води для СО підлоги, t<sub>co 2</sub>:',
                             t_co_2Edit)
        tpInputLayout.addRow('К.к.д. згоряння палива, eta_K:', eta_KEdit)
        tpInputLayout.addRow('Нижча теплота згоряння палива, Q_n_r, кДж/м<sup>3</sup>:',
                             Q_n_rEdit)
        tpInputLayout.addRow('Вартість 1 м^3 газу, c<sub>газ</sub>, грн/м<sup>3</sup>:',
                             c_gazEdit)
        tpInputLayout.addRow('Вартість 1 кВт\N{MIDDLE DOT}год, c<sub>ел</sub>, '
                             'грн/м<sup>3</sup>:', c_elEdit)
        
        gruGroup = QGroupBox('Для ґрунту і контуру СО підлоги:')
        gruInputEdit = QFormLayout(gruGroup)
        gruInputEdit.addRow('Питома тепловіддача ґрунту, q<sub>ґр</sub>, '
                            'Вт/м<sup>2</sup>:', q_gruEdit)
        gruInputEdit.addRow('Внутрішній діаметр, d, мм:', d_gruEdit)
        gruInputEdit.addRow('Питома довжина тепловідбору, l<sub>0</sub>, '
                            'м/м<sup>2</sup>:', l_0_gruEdit)
        
        inputScrollArea = QScrollArea()
        inputScrollArea.setWidgetResizable(True)
        inputScrollArea.setSizePolicy(sp)
        
        inputDataPanel = QWidget()
        inputDataLayout = QVBoxLayout(inputDataPanel)
        
        inputDataLayout.addWidget(soGroup)
        inputDataLayout.addWidget(sgvGroup)
        inputDataLayout.addWidget(sgkGroup)
        inputDataLayout.addWidget(tpGroup)
        inputDataLayout.addWidget(gruGroup)
        
        inputScrollArea.setWidget(inputDataPanel)
        
        inputWidget = QWidget()
        inputLayout = QFormLayout(inputWidget)
        #inputLayout.setContentsMargins(0, 0, 0, 0)
        inputLayout.setRowWrapPolicy(QFormLayout.WrapAllRows)
        inputLayout.addRow('Вхідні дані:', inputScrollArea)
        inputLayout.addWidget(calcButton)
        
        consoleViewWidget = QWidget()
        consoleViewLayout = QFormLayout(consoleViewWidget)
        consoleViewLayout.setRowWrapPolicy(QFormLayout.WrapAllRows)
        consoleViewLayout.addRow(u'Результати:', outputConsoleBrowser)
        
        contentWidget = QSplitter(Qt.Horizontal)
        #viewSplitter = QSplitter(Qt.Vertical)
        
        ioSplitter = QSplitter(Qt.Vertical)
        ioSplitter.setStretchFactor(0, 1)
        ioSplitter.setStretchFactor(1, 0)
        ioSplitter.setSizes([200, 320])
        ioSplitter.setChildrenCollapsible(False)
        
        ioSplitter.addWidget(inputWidget)
        ioSplitter.addWidget(consoleViewWidget)
        
        contentWidget.addWidget(ioSplitter)
        contentWidget.addWidget(graphWidget)
        
        self.setCentralWidget(contentWidget)
        
        self.resize(1000, 640)
        
    def _update_canvas(self):
        self.__graphCanvas.clear()
        
        self.__graphCanvas.figure.canvas.draw()


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
        
        

class KwAntTeploMonitorDbl(QApplication):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setDefaultAppLocale()

    def setDefaultAppLocale(self):
        translationsPath = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
        locale = QLocale.system()
        
        self.__qtTranslator = QTranslator()
        if self.__qtTranslator.load(locale, "qt", "_", translationsPath):
            self.installTranslator(self.__qtTranslator)
        
        self.__qtBaseTranslator = QTranslator()
        if self.__qtBaseTranslator.load(locale, "qtbase", "_", translationsPath):
            self.installTranslator(self.__qtBaseTranslator)

def main(n):
    app = KwAntTeploMonitorDbl(sys.argv)
    app.setApplicationName('KwAntTeploMonitorDbl')
    app.setApplicationVersion('1.0.0')
    
    if n == 1:
        window = KwMainWindow()
    elif n == 2:
        window = QWidget()
        layout = QVBoxLayout(window)
        button = QPushButton('Як тебе не любити')
        button.setObjectName('calcButton')
        layout.addWidget(button)
        
        setup = {'setup': {'app':
            {'name': QApplication.applicationName(),
             'version': QApplication.applicationVersion()},
            'KwResultBrowser': {'font': {'name': 'Monospace', 'size': 7}, 
                                  'color': '#fff', 'background_color': '#300A24'}
                           }
                 }
        
        browser = KwResultBrowser(setup['setup']['KwResultBrowser'])
        browser.setText('Anton')
        layout.addWidget(browser)
        colorButton = KwColorButton()
        layout.addWidget(colorButton)
        colorChoicer = KwColorChoicer(Qt.green, Qt.magenta)
        layout.addWidget(colorChoicer)
        font_dataChoicer = KwFontDataChoicer()
        font_dataChoicer.fontChanged[str].connect(lambda font: print(font))
        font_dataChoicer.font_sizeChanged[int].connect(lambda s: print(s))
        layout.addWidget(font_dataChoicer)
        
    with open('ww_style.css', 'r') as f:
        app.setStyleSheet(f.read())
        
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main(1)