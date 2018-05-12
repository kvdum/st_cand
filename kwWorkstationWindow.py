#! /usr/bin/env/python3
# -*- coding: utf-8 -*-

'''
Created on 16 трав. 2017 р.

@author: kavedium
'''

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGroupBox,\
    QComboBox, QTextEdit, QPushButton, QLabel, QHBoxLayout,\
    QSpinBox, QMenu, QAction, QDialog, QFormLayout, QFontComboBox, QToolButton,\
    QSizePolicy, QColorDialog, QMessageBox, QDialogButtonBox

from kwShare import Rho_wN, RvEkoplastic, RvHaka, RvMetal, SPR_VogelNoot, \
                      SPR_RADIK_KLASIK, T_z_DSTU_2010, WindDirDSTU_2010
from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal, QSize, QLibraryInfo, QLocale,\
    QTranslator
from PyQt5.QtGui import QFont, QColor, QPalette, QPainter
import json

class KwColorButton(QToolButton):
    
    SIZE_DEFAULT = 0
    SIZE_HINT = 1
    
    colorChanged = pyqtSignal(QColor, name='colorChanged')
    
    def __init__(self, color=Qt.black, size=SIZE_DEFAULT, changing_tooltip=True, 
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.__changing_tooltip = changing_tooltip
        self.color = color
        
        if size == self.SIZE_DEFAULT:
            size = (32, 32)
        elif size == self.SIZE_HINT:
            size = self.sizeHint()
        
        if isinstance(size, (tuple, list)):
            w, h = size
        else:
            w = size.width(); h = size.height()
        
        self.setMinimumSize(w, h)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        self.setCursor(Qt.PointingHandCursor)
        
    def paintEvent(self, e):
        size = self.contentsRect().size()
        w = size.width()
        h = size.height()
        
        super().paintEvent(e)
        
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QColor('#606060'))
        qp.setBrush(self.__color)
        qp.drawRect(5, 5, w-11, h-11)
        qp.end()
    
    @property
    def color(self):
        return self.__color
    
    @color.setter
    def color(self, color):
        color = QColor(color)
        self.__color = color
        self.repaint()
        if self.__changing_tooltip:
            self.setToolTip(self.color.name())
        self.colorChanged.emit(color)

class KwColorChoicer(QWidget):
    
    colorChanged = pyqtSignal(QColor, name='colorChanged') 
    
    def __init__(self, color, standard_color, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.__colorButton = KwColorButton(color, changing_tooltip=False, 
                                           parent=self)
        
        self.__colorButton.setToolTip('Вибрати колір')
        self.__colorButton.clicked.connect(self.change_color)
        self.__colorButton.colorChanged.connect(self.colorChanged.emit)
        
        self.__std_colorButton = KwColorButton(standard_color, 
                                               changing_tooltip=False, 
                                               parent=self)
        self.__std_colorButton.setToolTip(
            'Встановити поточним колір за промовчанням')
        self.__std_colorButton.clicked.connect(self.change_standard_color)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        layout.addWidget(self.__colorButton)
        layout.addWidget(self.__std_colorButton)
        layout.addStretch()
    
    @pyqtSlot()
    def change_color(self):
        color = QColorDialog.getColor(self.__colorButton.color, self)
        if color.isValid():
            self.__colorButton.color = color
    
    @pyqtSlot()
    def change_standard_color(self):
        self.__colorButton.color = self.__std_colorButton.color
    
    @property
    def color(self):
        return self.__colorButton.color

class KwFontDataChoicer(QWidget):
    
    fontChanged = pyqtSignal(str, name='fontChanged')
    font_sizeChanged = pyqtSignal(int, name='font_sizeChanged')
    
    def __init__(self, font='', size=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.__fontChoice = QFontComboBox(self)
        self.__fontChoice.setCurrentText(font)
        self.__fontChoice.currentIndexChanged[str].connect(
            self.fontChanged.emit)
        
        self.__font_sizeEdit = QSpinBox(self)
        self.__font_sizeEdit.setRange(5, 72)
        self.__font_sizeEdit.setValue(size)
        self.__font_sizeEdit.valueChanged[int].connect(
            self.font_sizeChanged.emit)
        
        layout = QHBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.__fontChoice)
        layout.addWidget(self.__font_sizeEdit)
    
    @property
    def font_data(self):
        return self.__fontChoice.currentText(), self.__font_sizeEdit.value()
    
    @font_data.setter
    def font_data(self, font, size):
        self.__fontChoice.setCurrentText(font)
        self.__font_sizeEdit.setValue(size)
    
    @property
    def font(self):
        return self.__fontChoice.currentText()
    
    @font.setter
    def font(self, font):
        self.__fontChoice.setCurrentText(font)
    
    @property
    def size(self):
        return self.__font_sizeEdit.value()
    
    @size.setter
    def size(self, size):
        return self.__font_sizeEdit.setValue(size)

class KwResultSetupDialog(QDialog):
    
    def __init__(self, setup, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        font_name_setup = setup['font']['name']
        font_size_setup = setup['font']['size']
        color_setup = setup['color']
        background_color_setup = setup['background_color']
        
        self.__font_dataChoicer = KwFontDataChoicer(font_name_setup,
                                                    font_size_setup)
        self.__colorChoicer = KwColorChoicer(color_setup, '#fff')
        self.__backgroundChoicer = KwColorChoicer(background_color_setup,
                                                  '#300A24')
        
        layout = QVBoxLayout(self)
        
        contLayout = QFormLayout()
        contLayout.addRow('Шрифт:', self.__font_dataChoicer)
        contLayout.addRow('Колір тексту:', self.__colorChoicer)
        contLayout.addRow('Колір фону:', self.__backgroundChoicer)
        
        layout.addLayout(contLayout)
        
        bbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                                self)
        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)
        
        layout.addWidget(bbox, alignment=Qt.AlignRight | Qt.AlignBottom)
        
        self.setWindowTitle('Установки')
        
        self.__setup = setup
        self.exec()
    
    @pyqtSlot()
    def accept(self):
        setup = self.__setup
        
        setup['font']['name'] = self.__font_dataChoicer.font
        setup['font']['size'] = self.__font_dataChoicer.size
        setup['color'] = self.__colorChoicer.color.name()
        setup['background_color'] = self.__backgroundChoicer.color.name()
        
        super().accept()

class KwResultBrowser(QTextEdit):
    
    def __init__(self, setup, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setReadOnly(True)
        self.setLineWrapMode(QTextEdit.NoWrap)
        
        self.__setup = setup
        self.apply_setup()
        
    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu()
        setupAction = QAction('Установки...', self)
        setupAction.triggered.connect(self.change_setup)
        menu.addSeparator()
        setup = menu.addAction(setupAction)
        menu.exec_(self.mapToGlobal(event.pos()))
    
    @pyqtSlot()
    def change_setup(self):
        KwResultSetupDialog(self.__setup)
        self.apply_setup()
    
    def apply_setup(self):
        setup = self.__setup
        
        font = QFont(setup['font']['name'], setup['font']['size'])
        self.setFont(font)
        
        self.setStyleSheet('QTextEdit {color: %s; background-color: %s;}' %
                           (setup['color'], setup['background_color']))

class KwCalcButton(QPushButton):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setObjectName('calcButton')
        self.setText('Визначити')

class KwWorkWindow(QWidget):
    
    CONFIG_FNAME = '{}.ini'.format('KwWorkWindow')
    
    def load_db(self):
        self.__t_z_data = T_z_DSTU_2010()
        self.__janguary_wind_dir = WindDirDSTU_2010()
        self.__july_wind_dir = WindDirDSTU_2010(ws_name=WindDirDSTU_2010.JULY_WS_NAME)
        self.__spr_VogelNoot = SPR_VogelNoot(sheet=1)   # 75/65/20
        self.__spr_RADIK_KLASIK = SPR_RADIK_KLASIK()
    
    @pyqtSlot()
    def calc_t_z_data(self):
        try:
            self.__resultEdit_1.setText(self.__t_z_data.calculate_publish(
                self.__cityChoice_1.currentText()))
        except Exception as err:
            self.setupResultErrMsg(self.__resultEdit_1, err)
    
    @pyqtSlot()
    def calc_wind_dir(self):
        try:
            season = self.__seasonChoice_2.currentData()
            if season == 'jan':
                wind_dir = self.__janguary_wind_dir
            elif season == 'jul':
                wind_dir = self.__july_wind_dir
            else:
                raise ValueError('В базі немає даних для характеристик вітру в сезоні - {}'\
                                 .format(season))
            
            self.__resultEdit_2.setText(wind_dir.calculate_publish(
                self.__cityChoice_2.currentText()))
            
            self.__resultEdit_2.setText('{}\n{}'.format(
                self.__resultEdit_2.toPlainText(), wind_dir.betas_publish(
                    self.__cityChoice_2.currentText())))
        except Exception as err:
            self.setupResultErrMsg(self.__resultEdit_2, err)
    
    @pyqtSlot()
    def calc_spr(self):
        try:
            vendor = self.__vendorChoice_3.currentData()
            if vendor == 'radik klasic':
                spr = self.__spr_RADIK_KLASIK
            elif vendor == 'vogel_noot':
                spr = self.__spr_VogelNoot
            
            h = self.__hChoice_3.currentText()
            if h != 'var':
                h = int(h)
            
            self.__resultEdit_3.setText(spr.calc_publish(Q_pr=self.__QEdit_3.value(), 
                             model=self.__modelChoice_3.currentText(),
                             h=h, t_1=self.__t_1Edit_3.value(), 
                             t_2=self.__t_2Edit_3.value(),
                             t_v=self.__t_vEdit_3.value()))
        except Exception as err:
            self.setupResultErrMsg(self.__resultEdit_3, err)
    
    def setupResultErrMsg(self, resultEdit, err):
        resultEdit.setText('<font color="red">{}</font>'.format(err))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.__setup = {}
        self.load_setup()
        
        self.load_db()
        
        layout = QVBoxLayout(self)
        
        gb_1 = QGroupBox('Параметри зовнішнього повітря:')
        
        self.__cityChoice_1 = QComboBox(self)
        self.__cityChoice_1.addItems(self.__t_z_data.cities())
        
        calcButton_1 = KwCalcButton(self)
        calcButton_1.clicked.connect(self.calc_t_z_data)
        
        self.__resultEdit_1 = KwResultBrowser(
            self.__setup['setup']['result_t_z'], self)
        
        gb_1Layout = QVBoxLayout(gb_1)
        gb_1subLayout = QHBoxLayout()
        gb_1subLayout.addWidget(QLabel('Місто:'))
        gb_1subLayout.addWidget(self.__cityChoice_1)
        gb_1subLayout.addSpacing(5)
        gb_1subLayout.addWidget(calcButton_1)
        gb_1subLayout.addStretch()
        
        gb_1Layout.addLayout(gb_1subLayout)
        gb_1Layout.addWidget(self.__resultEdit_1)
        
        layout.addWidget(gb_1)
        
        # -----------------------------------------------
        gb_2 = QGroupBox('Характеристики вітру:')
        
        self.__cityChoice_2 = QComboBox(self)
        self.__cityChoice_2.addItems(self.__janguary_wind_dir.cities())
        
        self.__seasonChoice_2 = QComboBox(self)
        self.__seasonChoice_2.addItem('cічень', 'jan')
        self.__seasonChoice_2.addItem('липень', 'jul')
        
        calcButton_2 = KwCalcButton(self)
        calcButton_2.clicked.connect(self.calc_wind_dir)
        
        self.__resultEdit_2 = KwResultBrowser(
            self.__setup['setup']['result_wind'], self)
        
        gb_2Layout = QVBoxLayout(gb_2)
        gb_2subLayout = QHBoxLayout()
        gb_2subLayout.addWidget(QLabel('Місто:'))
        gb_2subLayout.addWidget(self.__cityChoice_2)
        gb_2subLayout.addSpacing(5)
        gb_2subLayout.addWidget(QLabel('Сезон:'))
        gb_2subLayout.addWidget(self.__seasonChoice_2)
        gb_2subLayout.addSpacing(5)
        gb_2subLayout.addWidget(calcButton_2)
        gb_2subLayout.addStretch()
        
        gb_2Layout.addLayout(gb_2subLayout)
        gb_2Layout.addWidget(self.__resultEdit_2)
        
        layout.addWidget(gb_2)
        
        # ------------------------------------------------
        gb_3 = QGroupBox('Нагрівальні прилади:')
        
        self.__t_1Edit_3 = QSpinBox(self)
        self.__t_1Edit_3.setRange(0, 150)
        self.__t_1Edit_3.setValue(95)
        
        self.__t_2Edit_3 = QSpinBox(self)
        self.__t_2Edit_3.setRange(0, 150)
        self.__t_2Edit_3.setValue(70)
        
        self.__t_vEdit_3 = QSpinBox(self)
        self.__t_vEdit_3.setRange(0, 50)
        self.__t_vEdit_3.setValue(20)
        
        self.__QEdit_3 = QSpinBox(self)
        self.__QEdit_3.setRange(0, 10**6)
        
        self.__vendorChoice_3 = QComboBox(self)
        self.__vendorChoice_3.addItem('Radik Klasic', 'radik klasic')
        self.__vendorChoice_3.addItem('Vogel&Noot', 'vogel_noot')
        
        self.__modelChoice_3 = QComboBox(self)
        self.__modelChoice_3.addItem('var')
        self.__modelChoice_3.setEditable(True)
        
        self.__hChoice_3 = QComboBox(self)
        self.__hChoice_3.addItem('500')
        self.__hChoice_3.addItem('var')
        self.__hChoice_3.setEditable(True)
        
        calcButton_3 = KwCalcButton(self)
        calcButton_3.clicked.connect(self.calc_spr)
        
        self.__resultEdit_3 = KwResultBrowser(
            self.__setup['setup']['result_spr'], self)
        
        gb_3Layout = QVBoxLayout(gb_3)
        
        h1_gb_3subLayout = QHBoxLayout()
        h1_gb_3subLayout.addWidget(QLabel('t_1:'))
        h1_gb_3subLayout.addWidget(self.__t_1Edit_3)
        h1_gb_3subLayout.addSpacing(5)
        h1_gb_3subLayout.addWidget(QLabel('t_2:'))
        h1_gb_3subLayout.addWidget(self.__t_2Edit_3)
        h1_gb_3subLayout.addSpacing(5)
        h1_gb_3subLayout.addWidget(QLabel('t_v:'))
        h1_gb_3subLayout.addWidget(self.__t_vEdit_3)
        h1_gb_3subLayout.addSpacing(5)
        h1_gb_3subLayout.addWidget(QLabel('Q, Вт:'))
        h1_gb_3subLayout.addWidget(self.__QEdit_3)
        h1_gb_3subLayout.addStretch()
        gb_3Layout.addLayout(h1_gb_3subLayout)
        
        h2_gb_3subLayout = QHBoxLayout()
        h2_gb_3subLayout.addWidget(QLabel('Марка:'))
        h2_gb_3subLayout.addWidget(self.__vendorChoice_3)
        h2_gb_3subLayout.addSpacing(5)
        h2_gb_3subLayout.addWidget(QLabel('Тип:'))
        h2_gb_3subLayout.addWidget(self.__modelChoice_3)
        h2_gb_3subLayout.addSpacing(5)
        h2_gb_3subLayout.addWidget(QLabel('h, мм:'))
        h2_gb_3subLayout.addWidget(self.__hChoice_3)
        h2_gb_3subLayout.addSpacing(5)
        h2_gb_3subLayout.addWidget(calcButton_3)
        h2_gb_3subLayout.addStretch()
        gb_3Layout.addLayout(h2_gb_3subLayout)
        
        gb_3Layout.addWidget(self.__resultEdit_3)
        
        layout.addWidget(gb_3)
        
        self.setWindowTitle('{} v {}'.format(QApplication.applicationName(),
                                             QApplication.applicationVersion()))
        
    def closeEvent(self, event):
        self.save_setup()
    
    def default_setup(self):
        setup = {'setup': {'app':
            {'name': QApplication.applicationName(),
             'version': QApplication.applicationVersion()},
            'result_t_z': {'font': {'name': 'Monospace', 'size': 7}, 
                                  'color': '#fff', 'background_color': '#300A24'},
            'result_wind': {'font': {'name': 'Monospace', 'size': 7}, 
                                  'color': '#fff', 'background_color': '#300A24'},
            'result_spr': {'font': {'name': 'Monospace', 'size': 7}, 
                                  'color': '#fff', 'background_color': '#300A24'}
                           }
                 }
        return setup
    
    def load_setup(self):
        try:
            with open(self.CONFIG_FNAME, 'r') as f:
                setup = json.load(f)
                
            if setup['setup']['app']['name'] != QApplication.applicationName() or \
           setup['setup']['app']['version'] != QApplication.applicationVersion():
                QMessageBox.warning(self, QApplication.applicationName(), 
              'Поточний файл налаштувань створений не для цієї програми або \
засторілий.\nПрийняті нові налаштування за промовчанням.')
                setup = self.default_setup()
        except Exception as err:
            QMessageBox.critical(self, QApplication.applicationName(), 
                                 str(err))
            setup = self.default_setup()
        finally:
            self.__setup = setup
    
    def save_setup(self):
        try:
            with open(self.CONFIG_FNAME, 'w') as f:
                json.dump(self.__setup, f)
        except Exception as err:
            QMessageBox.critical(self, QApplication.applicationName(), 
                                 str(err))

def setDefaultAppLocale(app):
    translationsPath = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
    locale = QLocale.system()
    
    app.__qtTranslator = QTranslator()
    if app.__qtTranslator.load(locale, "qt", "_", translationsPath):
        app.installTranslator(app.__qtTranslator)
    
    app.__qtBaseTranslator = QTranslator()
    if app.__qtBaseTranslator.load(locale, "qtbase", "_", translationsPath):
        app.installTranslator(app.__qtBaseTranslator)

def main(n):
    app = QApplication(sys.argv)
    setDefaultAppLocale(app)
    app.setApplicationName('KwWorkWindow')
    app.setApplicationVersion('1.0.0')
    
    if n == 1:
        window = KwWorkWindow()
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