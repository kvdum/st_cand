# -*- coding: utf-8 -*-

'''
Created on 9.05.2018.

@author: ichet
'''

import os
import sys
if getattr(sys, 'frozen', False):
    # frozen
    SCRIPT_FOLDER = os.path.dirname(sys.executable)
else:
    SCRIPT_FOLDER = os.path.dirname(os.path.realpath(__file__))
os.chdir(SCRIPT_FOLDER)

import traceback
import io, pickle
from openpyxl import load_workbook

from matplotlib.backends.backend_qt5agg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

from PyQt5.QtCore import Qt, QLibraryInfo, QLocale, QTranslator, QRegExp,\
    pyqtSignal, pyqtProperty
from PyQt5.QtGui import QRegExpValidator, QValidator, QIcon, QFontDatabase,\
    QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter, QWidget,\
    QFormLayout, QLineEdit, QSpinBox, QGroupBox, QVBoxLayout, QPushButton,\
    QScrollArea, QSizePolicy, QAbstractSpinBox, QComboBox
    
from kwConsole import KwConsoleBrowser

class KwNumberEdit(QLineEdit):
    '''Віджет для введення цілих і дійсних чисел
    
    @version: 0.1.0
    
    @param: value (int, str) - значення, яке є або може бути числом.
    '''
    
    class NumberException(Exception):
        pass
    
    # https://ru.stackoverflow.com/questions/575862/Регулярное-выражение-для-чисел-с-плавающей-точкой
    doubleRegExp = QRegExp(r'^[-+]?[0-9]*[.,]?[0-9]+(?:[eE][-+]?[0-9]+)?$')
    
    valueChanged = pyqtSignal([float], name='valueChanged')
    
    def __init__(self, value=0, parent=None):
        super().__init__(parent=parent)
        
        self.setValidator(QRegExpValidator(self.doubleRegExp, self))
        self.value = value
        
        # >>>
        self.textChanged.connect(self.__textToValueChanged)
    
    def __textToValueChanged(self, text):
        try:
            if text:
                self.valueChanged.emit(float(text.replace(',', '.')))
            else:
                self.setText('0')
                self.selectAll()
        except:
            pass
    
    @pyqtProperty(float)
    def value(self):
        value = float(self.text().replace(',', '.'))
        if value.is_integer():
            value = int(value)
        return value
    
    @value.setter
    def value(self, value):
        self.setText(self.__get_value(str(value)))
        self.valueChanged.emit(self.value)
    
    def __get_value(self, text):
        state = self.validator().validate(text, 0)[0]
        if state == QValidator.Acceptable:
            return text
        else:
            raise KwNumberEdit.NumberException(
                    '{} - неправильно задано число'.format(text))
        #elif state == QValidator.Intermediate:
        #else

class KwMainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        sp = QSizePolicy()
        sp.setHorizontalPolicy(QSizePolicy.Expanding)
        sp.setVerticalPolicy(QSizePolicy.Expanding)
        sp.setVerticalStretch(1)
        
        wb_city_data = load_workbook(filename=r'ДСТУ-Н Б В.1.1-27_2010.xlsx', 
                                     read_only=True, data_only=True)
        self.__ws_city_I_ser_m_sj = wb_city_data['Лист1']
        self.__ws_city_t_z = wb_city_data['Т2. Температура зовн. пов.']
        
        self.__cityChoice = QComboBox()
        self.__cityChoice.addItems(c[0].value for c in 
                                   self.__ws_city_I_ser_m_sj['A6':'A605'] if c[0].value)
        
        self.__q_0Edit = KwNumberEdit(.5)
        self.__V_budEdit = KwNumberEdit(480)
        
        self.__NEdit = QSpinBox()
        self.__NEdit.setRange(1, 999)
        self.__NEdit.setSuffix(' чол')
        self.__NEdit.setValue(6)
        
        self.__t_gvEdit = QSpinBox()
        self.__t_gvEdit.setRange(25, 70)
        self.__t_gvEdit.setSingleStep(5)
        self.__t_gvEdit.setSuffix(' \N{DEGREE CELSIUS}')
        self.__t_gvEdit.setValue(45)
        
        self.__a_gvEdit = QSpinBox()
        self.__a_gvEdit.setRange(15, 99)
        self.__a_gvEdit.setSuffix(' л/добу')
        self.__a_gvEdit.setValue(35)
        
        self.__f_zEdit = KwNumberEdit(.8)
        self.__varthetaEdit = KwNumberEdit(1.7)
        self.__S_0Edit = KwNumberEdit(1.723)
        self.__F_rEdit = KwNumberEdit(1)
        self.__eta_0Edit = KwNumberEdit(0.813)
        self.__ULEdit = KwNumberEdit(4.6)
        self.__aEdit = KwNumberEdit(.007)
        self.__bEdit = KwNumberEdit(1.27E-5)
        self.__c_paEdit = KwNumberEdit(3.16)
        
        self.__P_tpEdit = KwNumberEdit(14.1)
        self.__epsilon_tpEdit = KwNumberEdit(5.5)
        self.__epsilon_elEdit = KwNumberEdit(.88)
        self.__P_elEdit = KwNumberEdit(2.6)
        
        self.__t_co_1Edit = QSpinBox()
        self.__t_co_1Edit.setRange(25, 70)
        self.__t_co_1Edit.setSingleStep(5)
        self.__t_co_1Edit.setSuffix(' \N{DEGREE CELSIUS}')
        self.__t_co_1Edit.setValue(35)
        
        self.__t_co_2Edit = QSpinBox()
        self.__t_co_2Edit.setRange(20, 60)
        self.__t_co_2Edit.setSingleStep(5)
        self.__t_co_2Edit.setSuffix(' \N{DEGREE CELSIUS}')
        self.__t_co_2Edit.setValue(30)
        
        self.__eta_KEdit = KwNumberEdit(.93)
        self.__Q_n_rEdit = KwNumberEdit(35600)
        self.__c_gazEdit = KwNumberEdit(.55)
        self.__c_elEdit = KwNumberEdit(.25)
        
        self.__q_gruEdit = KwNumberEdit(21)
        
        self.__d_gruEdit = QSpinBox()
        self.__d_gruEdit.setRange(5, 99)
        self.__d_gruEdit.setSuffix('  мм')
        self.__d_gruEdit.setValue(25)
        
        self.__l_0_gruEdit = KwNumberEdit(1.7)
        
        calcButton = QPushButton('Визначити')
        calcButton.setObjectName('calcButton')
        
        self.__outputConsoleBrowser = KwConsoleBrowser(setup={'font': {'name': 
              QFont('Hack').family(), 'size': 8}, 'color': 'rgb(255, 255, 255)', 
              'background_color': 'rgba(0, 0, 0, 218)', 'line_wrap': False})
        self.__outputConsoleBrowser.setSizePolicy(sp)
        
        graphWidget = QMainWindow()
        graphWidget.setMinimumWidth(380)
        
        self.__graphCanvas = self.__createFigureCanvas()
        graphWidget.addToolBar(Qt.TopToolBarArea,
                               NavigationToolbar(self.__graphCanvas, self))
        graphWidget.setCentralWidget(self.__graphCanvas)
        
        cityLayout = QFormLayout()
        cityLayout.addRow('Місто:', self.__cityChoice)
        
        soGroup = QGroupBox('Для системи опалення (СО):')
        soInputLayout = QFormLayout(soGroup)
        
        soInputLayout.addRow('Питома потужність тепловтрат, q<sub>0</sub>, '
                             'Вт/(м<sup>3</sup>\N{MIDDLE DOT}\N{DEGREE CELSIUS}):', 
                             self.__q_0Edit)
        soInputLayout.addRow("Об'єм будинку по зовнішніх обмірах, V<sub>буд</sub>, "
                             "м<sup>3</sup>:", self.__V_budEdit)
        
        sgvGroup = QGroupBox(u'Для системи гарячого водопостачання (СГК):')
        sgvInputLayout = QFormLayout(sgvGroup)
        sgvInputLayout.addRow('Кількість мешканців у будинку, N:', self.__NEdit)
        sgvInputLayout.addRow('Температура гарячої води, t<sub>гв</sub>:', self.__t_gvEdit)
        sgvInputLayout.addRow('Добова витрата гарячої води на 1 особу, a<sub>гв</sub>:',
                              self.__a_gvEdit)
        
        sgkGroup = QGroupBox('Для системи геліоколекторів (СГК):')
        sgkInputLayout = QFormLayout(sgkGroup)
        sgkInputLayout.addRow('Ступінь заміщення тепловтрат СГВ, f<sub>з</sub>:', self.__f_zEdit)
        sgkInputLayout.addRow('Параметр, \u03D1:', self.__varthetaEdit)
        sgkInputLayout.addRow('Площа 1-го геліоколектора, S<sub>0</sub>, м<sup>2</sup>:',
                              self.__S_0Edit)
        sgkInputLayout.addRow('F<sub>r</sub>:', self.__F_rEdit)
        sgkInputLayout.addRow('Оптичний ККД, \N{GREEK SMALL LETTER ETA}:', self.__eta_0Edit)
        sgkInputLayout.addRow('Коефіцієнт тепловтрат, UL, Вт/(м<sup>2</sup>)'
                              '\N{MIDDLE DOT}\N{DEGREE CELSIUS}):', self.__ULEdit)
        sgkInputLayout.addRow('a:', self.__aEdit)
        sgkInputLayout.addRow('b:', self.__bEdit)
        sgkInputLayout.addRow('c<sub>pa</sub>, кДж/(кг\N{MIDDLE DOT}\N{DEGREE CELSIUS}):',
                              self.__c_paEdit)
        
        tpGroup = QGroupBox('Для теплової помпи (ТП):')
        tpInputLayout = QFormLayout(tpGroup)
        tpInputLayout.addRow('Теплова потужність, P<sub>тп</sub>, кВт:', self.__P_tpEdit)
        tpInputLayout.addRow('Тепловий к.к.д, \N{GREEK SMALL LETTER EPSILON}'
                             '<sub>тп</sub>', self.__epsilon_tpEdit)
        tpInputLayout.addRow('Електричний к.к.д., \N{GREEK SMALL LETTER EPSILON}'
                             '<sub>ел</sub>:', self.__epsilon_elEdit)
        tpInputLayout.addRow('Електрична потужність, P<sub>ел</sub>, кВт:', self.__P_elEdit)
        tpInputLayout.addRow('Т-ра нагрітої води для СО підлоги, t<sub>co 1</sub>:',
                             self.__t_co_1Edit)
        tpInputLayout.addRow('Т-ра охолодженої води для СО підлоги, t<sub>co 2</sub>:',
                             self.__t_co_2Edit)
        tpInputLayout.addRow('К.к.д. згоряння палива, eta_K:', self.__eta_KEdit)
        tpInputLayout.addRow('Нижча теплота згоряння палива, Q<sub>n r</sub>, кДж/м<sup>3</sup>:',
                             self.__Q_n_rEdit)
        tpInputLayout.addRow('Вартість 1 м<sup>3</sup> газу, c<sub>газ</sub>, грн/м<sup>3</sup>:',
                             self.__c_gazEdit)
        tpInputLayout.addRow('Вартість 1 кВт\N{MIDDLE DOT}год, c<sub>ел</sub>, '
                             'грн/м<sup>3</sup>:', self.__c_elEdit)
        
        gruGroup = QGroupBox('Для ґрунту і контуру СО підлоги:')
        gruInputEdit = QFormLayout(gruGroup)
        gruInputEdit.addRow('Питома тепловіддача ґрунту, q<sub>ґр</sub>, '
                            'Вт/м<sup>2</sup>:', self.__q_gruEdit)
        gruInputEdit.addRow('Внутрішній діаметр, d, мм:', self.__d_gruEdit)
        gruInputEdit.addRow('Питома довжина тепловідбору, l<sub>0</sub>, '
                            'м/м<sup>2</sup>:', self.__l_0_gruEdit)
        
        inputScrollArea = QScrollArea()
        inputScrollArea.setWidgetResizable(True)
        inputScrollArea.setSizePolicy(sp)
        
        inputDataPanel = QWidget()
        inputDataLayout = QVBoxLayout(inputDataPanel)
        
        inputDataLayout.addLayout(cityLayout)
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
        consoleViewLayout.addRow(u'Результати:', self.__outputConsoleBrowser)
        
        contentSplitter = QSplitter(Qt.Horizontal)
        contentSplitter.setStretchFactor(0, 1)
        contentSplitter.setStretchFactor(1, 0)
        contentSplitter.setSizes([350, 380])
        contentSplitter.setChildrenCollapsible(False)
        
        ioSplitter = QSplitter(Qt.Vertical)
        ioSplitter.setStretchFactor(0, 1)
        ioSplitter.setStretchFactor(1, 0)
        ioSplitter.setSizes([200, 320])
        ioSplitter.setChildrenCollapsible(False)
        ioSplitter.setMinimumWidth(380)
        
        ioSplitter.addWidget(inputWidget)
        ioSplitter.addWidget(consoleViewWidget)
        
        contentSplitter.addWidget(ioSplitter)
        contentSplitter.addWidget(graphWidget)
        
        self.setCentralWidget(contentSplitter)
        
        self.resize(1200, 640)
        
        # <<<
        for inputValueWidget in inputWidget.findChildren((QAbstractSpinBox,
                                                          KwNumberEdit)):
            inputValueWidget.valueChanged.connect(self._reset_output_data)
        
        for inputValueWidget in inputWidget.findChildren(QComboBox):
            inputValueWidget.activated.connect(self._reset_output_data)
        
        calcButton.clicked.connect(self.calc_script)
    
    def __createFigureCanvas(self):
        '''Створює область виводу графіків.
        '''
        
        graphCanvas = FigureCanvas(Figure())
        cid = graphCanvas.figure.canvas.mpl_connect('button_press_event', 
                                                    self.subplot_clicked)
        return graphCanvas
    
    def _reset_output_data(self):
        '''Скидає дані виводу'''
        
        self.__outputConsoleBrowser.clear()
        
        self.__graphCanvas.figure.clear()
        self.__graphCanvas.figure.canvas.draw()
    
    def subplot_clicked(self, event):
        '''Спрацьовує при кліках миші
        В даному випадку відслідковуються тільки подвійні кліки мишею.
        Відкриває графік у збільшеному окремому вікні.
        '''
        
        if event.dblclick:
            if not event.inaxes: return # Завчасно завершує, якщо немає графіків.
            
            view_graph_params = get_show_own_frame_params(True)
            
            buf = io.BytesIO()
            figure_embedded = self.__graphCanvas.figure # Вихідний зразок.
            
            # Створється повна бінарна копія графіків.
            pickle.dump(figure_embedded.axes[0], buf)
            buf.seek(0)
            ax = pickle.load(buf)
            
            # Перетворюється в модальний діалог.
            fig = plt.figure(**get_figure_data())
            fig_backend_window = plt.get_current_fig_manager().window
            fig_backend_window.setParent(self)
            fig_backend_window.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
            fig_backend_window.setWindowModality(True)
            
            ax.figure = fig
            fig.axes.append(ax)
            fig.add_axes(ax)
            
            buf = io.BytesIO()
            pickle.dump(figure_embedded.axes[1], buf)
            buf.seek(0)
            ax_2 = pickle.load(buf)
            
            ax_2.figure = fig
            fig.axes.append(ax_2)
            fig.add_axes(ax_2)
            
            #dummy = fig.add_subplot(111)
            #ax.set_position(dummy.get_position())
            #ax_2.set_position(dummy.get_position())
            #dummy.remove()
            
            # Перетворення границь вписання графіків у нове вікно виводу.
            embedded_fig_size = figure_embedded.get_size_inches()
            fig_size = fig.get_size_inches()
            scale_x = fig_size[0]/embedded_fig_size[0]
            scale_y = fig_size[1]/embedded_fig_size[1]
            x_0, y_0, x_1, y_1 = view_graph_params['ax_pos'] #ax.get_position().bounds
            x_0 *= scale_x; x_1 *= scale_x
            y_0 *= scale_y; y_1 *= scale_y
            
            ax_pos = (1.2*x_0, y_0, x_1, y_1)  # Корекція розміщення.
            ax.set_position(ax_pos)
            ax_2.set_position(ax_pos)
            
            fig.canvas.set_window_title(figure_embedded.own_window_title)
            
            for item in ([ax.xaxis.label, ax.yaxis.label] +
                         ax.get_xticklabels() + ax.get_yticklabels() + 
                         [ax_2.xaxis.label, ax_2.yaxis.label] +
                         ax_2.get_xticklabels() + ax_2.get_yticklabels() +
                         ax.get_legend().texts +
                         [child for child in ax.get_children() if isinstance(
                             child, matplotlib.text.Annotation)] +
                         [child for child in ax_2.get_children() if isinstance(
                             child, matplotlib.text.Annotation)]):
                item.set_fontsize(view_graph_params['font_size'])
            ax.title.set_fontsize(view_graph_params['ax_titlesize'])
            
            ax.title.set_y(view_graph_params['ax_title_y'] * scale_y)
            ax.yaxis.get_label().set_ha(view_graph_params['ax_ha'])
            
            fig.show()
    
    def calc_script(self):
        '''Визначення даних
        '''
        
        consoleCursor = self.__outputConsoleBrowser.viewport().cursor()
        self.__outputConsoleBrowser.viewport().setCursor(Qt.WaitCursor)
        self.__outputConsoleBrowser.start_redirect()
        try:
            self.__outputConsoleBrowser.clear()
            #if self.__graphCanvas.figure.axes:
            #    self.__graphCanvas.figure.axes.remove(self.__graphCanvas.figure.axes[0])
            self.__graphCanvas.figure.clear()
            
            # Перестворюється область виводу графіків для коректних відсупів.
            graphWidget = self.__graphCanvas.parentWidget()
            self.__graphCanvas.deleteLater()
            self.__graphCanvas = self.__createFigureCanvas()
            graphWidget.setCentralWidget(self.__graphCanvas)
            
            for city_data_row in self.__ws_city_t_z['A7': 'Z145']:
                if city_data_row[0].value == self.__cityChoice.currentText():
                    city_t_z_h5 = int(city_data_row[17].value)
                    city_data_t_n_s = {i: float(c.value) for i, c in
                                       enumerate(city_data_row[1:13], start=1)}
                    break
            
            for row_index in range(6, 605, 24):
                if (self.__ws_city_I_ser_m_sj['A{}'.format(row_index)].value == 
                      self.__cityChoice.currentText()):
                    phi_grad = int(self.__ws_city_I_ser_m_sj['B{}'.format(row_index)].value)
                    phi_min =  round(int(self.__ws_city_I_ser_m_sj['C{}'
                                           .format(row_index)].value)/60., 2)
                    city_phi = phi_grad + phi_min
                    break
            
            
            
            self.__graphCanvas.figure.canvas.draw()
        except BaseException as err:
            print(u' Завчасно закінчено! '.center(79, u'='))
            print(err)
            print(traceback.print_exc())
        self.__outputConsoleBrowser.end_redirect()
        self.__outputConsoleBrowser.viewport().setCursor(consoleCursor)

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
    app_exec_name = 'kwCalcGQ'
    app.setApplicationName(app_exec_name)
    app.setApplicationVersion('0.1.0')
    app.setWindowIcon(QIcon(os.path.abspath('class_x24.png')))
    app.setApplicationDisplayName('{} v {}'.format(app_exec_name.lstrip('kw'),
                                  app.applicationVersion()))
    QFontDatabase.addApplicationFont('Hack-Regular.ttf')
    
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