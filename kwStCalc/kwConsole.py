# -*- coding: utf-8 -*-
'''
Created on 9.12.2017.

@author: ichet
'''

import sys
import re

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QDialogButtonBox, 
                             QTextEdit, QAction, QCheckBox, QApplication, 
                             QWidget, QPushButton, QLabel)

from kwColor import KwColorChoicer
from kwFont import KwFontDataChoicer
from kwRedirect import KwLogOut

class KwConsoleSetupDialog(QDialog):
    u'''Перейменований KwResultSetupDialog
    @version: 0.3.0
    '''
    
    def __init__(self, setup, default_text_color='#fff', 
                 default_background_color='#300A24', *args, **kwargs):
        super(KwConsoleSetupDialog, self).__init__(*args, **kwargs)
        
        font_name_setup = setup['font']['name']
        font_size_setup = setup['font']['size']
        line_wrap = setup.get('line_wrap', False)
        #color_setup = setup['color']
        #background_color_setup = setup['background_color']
        
        self.__font_dataChoicer = KwFontDataChoicer(font_name_setup,
                                                    font_size_setup)
        def getColor(color):
            u'''Повертає колір з тексту
            
            @param color (str) - колір у форматі rgb, rgba. 
                                 Наприклад: rgba(255, 255, 255, 128).
            '''
            
            return QColor(*[int(c) for c in re.findall(r'[A-Za-z0-9]+', 
                                                       color)[1:]])
        
        self.__colorChoicer = KwColorChoicer(getColor(setup['color']), 
                                             default_text_color)
        self.__backgroundChoicer = KwColorChoicer(getColor(setup['background_color']),
                                                  default_background_color, True)
        self.__lineWrapChecker = QCheckBox(u'Переносити довгі рядки', self)
        self.__lineWrapChecker.setChecked(line_wrap)
        
        layout = QVBoxLayout(self)
        
        contLayout = QFormLayout()
        contLayout.addRow(u'Шрифт:', self.__font_dataChoicer)
        contLayout.addRow(u'Колір тексту:', self.__colorChoicer)
        contLayout.addRow(u'Колір фону:', self.__backgroundChoicer)
        contLayout.addRow(self.__lineWrapChecker)
        
        layout.addLayout(contLayout)
        
        bbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                                parent=self)
        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)
        
        layout.addWidget(bbox, alignment=Qt.AlignRight | Qt.AlignBottom)
        
        self.setWindowTitle(u'Установки')
        self.setWindowFlags(self.windowFlags() ^ Qt.MSWindowsFixedSizeDialogHint
                            ^ Qt.WindowContextHelpButtonHint)
        
        self.__setup = setup
        self.exec_()
    
    @pyqtSlot()
    def accept(self):
        setup = self.__setup
        
        setup['font']['name'] = str(self.__font_dataChoicer.font)
        setup['font']['size'] = self.__font_dataChoicer.size
        textColor = self.__colorChoicer.color
        setup['color'] = 'rgb({}, {}, {})'.format(textColor.red(), textColor.green(), 
                                                  textColor.blue())
        backgroundColor = self.__backgroundChoicer.color
        setup['background_color'] = 'rgba({}, {}, {}, {})'.format(backgroundColor.red(), 
                                                        backgroundColor.green(), 
                                                        backgroundColor.blue(),
                                                        backgroundColor.alpha())
        setup['line_wrap'] = self.__lineWrapChecker.isChecked()
        
        super(KwConsoleSetupDialog, self).accept()

class KwConsoleBrowser(QTextEdit):
    u'''Перейменований KwResultBrowser
    
    @version: 0.2.0
    '''
    
    def __init__(self, setup, *args, **kwargs):
        super(KwConsoleBrowser, self).__init__(*args, **kwargs)
        
        self.setObjectName('consoleBrowser')
        self.setReadOnly(True)
        #self.setLineWrapMode(QTextEdit.NoWrap)
        
        self.__setup = setup
        self.apply_setup()
        
    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu()
        setupAction = QAction(u'Установки...', self)
        setupAction.triggered.connect(self.change_setup)
        menu.addSeparator()
        menu.addAction(setupAction)
        menu.exec_(self.mapToGlobal(event.pos()))
    
    @pyqtSlot()
    def change_setup(self):
        KwConsoleSetupDialog(self.__setup, parent=self)
        self.apply_setup()
    
    def apply_setup(self):
        setup = self.__setup
        
        font = QFont(setup['font']['name'], setup['font']['size'])
        self.setFont(font)
        
        self.setStyleSheet(r'''QTextEdit#consoleBrowser {{
            color: {};
            background-color: {};
        }}
        '''.format(setup['color'], setup['background_color']))
        
        if setup.get('line_wrap', True):
            self.setLineWrapMode(self.WidgetWidth)
        else:
            self.setLineWrapMode(self.NoWrap)
    
    def start_redirect(self):
        u'''Перенаправляє потік в цю консоль
        '''
        
        self.__stdout_original = sys.stdout
        self.__stderr_original = sys.stderr
        sys.stdout = KwLogOut(self)
        sys.stderr = KwLogOut(self, QColor(255, 0, 0))
        
    def end_redirect(self):
        u'''Закінчує перенаправлення
        '''
        
        sys.stdout = self.__stdout_original
        sys.stderr = self.__stderr_original

def __test(n, k=0):
    if n == 1:
        app = QApplication(sys.argv)
        if k == 1:
            
            def click_button():
                console.start_redirect()
                print(u'Цікаво, куди буде записано вивід?')
                print(u'Ти впевнений, що це цікаво?')
                raise ValueError('Error is help?')
                print(u'Так, звичайно!')
                print(u'Закінчено!')
                console.end_redirect()
                print(u'А тепер куди вивід?')
                print(u'Все, гаразд!')
            
            window = QWidget()
            button = QPushButton(u'Запустити')
            button.clicked.connect(click_button)
            layout = QVBoxLayout(window)
            layout.addWidget(button)
            layout.addWidget(QLabel(u'Тестова консоль:'))
            console = KwConsoleBrowser(setup={'font': {'name': 
                'Console', 'size': 8}, 'color': 'rgb(255, 255, 255)', 
              'background_color': 'rgba(0, 0, 0, 218)', 'line_wrap': False})
            layout.addWidget(console)
            window.show()
            
        sys.exit(app.exec_())

if __name__ == '__main__':
    __test(1, 1)