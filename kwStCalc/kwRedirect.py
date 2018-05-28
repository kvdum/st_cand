# -*- coding: utf-8 -*-

'''
Created on 09.05.2018.
Версія з 0.1.0. з PyQt4

Created on 10.12.2017.

@version: 0.1.1
@author: ichet
'''

from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import qApp

class KwLogOut:
    u'''Перенаправляє stdout або stderr у QTextEdit
    
    Вивід відбувається в основному потоці
    
    @version: 0.1.0
    '''
    
    def __init__(self, edit, color=None):
        """(edit, out=None, color=None) -> can write stdout, stderr to a
        QTextEdit.
        edit = QTextEdit
        out = alternate stream ( can be the original sys.stdout )
        color = alternate color (i.e. color stderr a different color)
        """
        
        self.__edit = edit
        if color and not hasattr(KwLogOut, '_KwLogOut__defaultCharFormat'):
            # Запам'ятовуємо формат за промовчанням.
            KwLogOut.__defaultCharFormat = self.__edit.currentCharFormat()
        self.__color = color

    def write(self, text):
        u'''Записує текст
        
        @param text (str) - текст.
        '''
        
        self.__edit.moveCursor(QTextCursor.End)   # Переміщуємо курсор в кінець.
        
        if self.__color:
            self.__edit.setTextColor(self.__color)
        elif hasattr(KwLogOut, '_KwLogOut__defaultCharFormat'):
            self.__edit.setCurrentCharFormat(KwLogOut.__defaultCharFormat)
        
        self.__edit.insertPlainText(text)  # Вставляє текст у вказану позицію.
        
        qApp.processEvents()