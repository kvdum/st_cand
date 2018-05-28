# -*- coding: utf-8 -*-
'''
Created on 09.05.2018.
Версія з 0.2.0. з PyQt4

Created on 3.11.2017.

@version: 0.2.1
@author: ichet
'''

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import (QWidget, QToolButton, QHBoxLayout, 
                             QColorDialog, QSizePolicy)

class KwColorButton(QToolButton):
    u'''Кнопка із зображенням кольору
    
    @version: 0.2.0
    '''
    
    SIZE_DEFAULT = 0
    SIZE_HINT = 1
    
    colorChanged = pyqtSignal(QColor, name='colorChanged')
    
    def __init__(self, color=Qt.black, size=SIZE_DEFAULT, changing_tooltip=True, 
                 *args, **kwargs):
        super(KwColorButton, self).__init__(*args, **kwargs)
        
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
        
        super(KwColorButton, self).paintEvent(e)
        
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QColor('#606060'))
        qp.setBrush(self.__color)
        qp.drawRect(5, 5, w-11, h-11)
        qp.end()
    
    @property
    def color(self):
        u'''Повертає колір
        
        @return QColor
        '''
        
        return self.__color
    
    @color.setter
    def color(self, color):
        u'''Встановлює колір
        
        @param color (QColor) - колір.
        '''
        
        color = QColor(color)
        self.__color = color
        self.repaint()
        if self.__changing_tooltip:
            self.setToolTip(self.color.name())
        self.colorChanged.emit(color)

class KwColorChoicer(QWidget):
    u'''Віджет вибору кольору
    
    @version: 0.2.0
    '''
    
    colorChanged = pyqtSignal(QColor, name='colorChanged') 
    
    def __init__(self, color, standard_color, isAlphaChennel=False, *args, **kwargs):
        super(KwColorChoicer, self).__init__(*args, **kwargs)
        
        self.__isAlphaChannel = isAlphaChennel
        
        self.__colorButton = KwColorButton(color, changing_tooltip=False, 
                                           parent=self)
        
        self.__colorButton.setToolTip(u'Вибрати колір')
        self.__colorButton.clicked.connect(self.change_color)
        self.__colorButton.colorChanged.connect(self.colorChanged.emit)
        
        self.__std_colorButton = KwColorButton(standard_color, 
                                               changing_tooltip=False, 
                                               parent=self)
        self.__std_colorButton.setToolTip(
            u'Встановити поточним колір за промовчанням')
        self.__std_colorButton.clicked.connect(self.change_standard_color)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        layout.addWidget(self.__colorButton)
        layout.addWidget(self.__std_colorButton)
        layout.addStretch()
    
    @pyqtSlot()
    def change_color(self):
        u'''Змінює колір
        '''
        
        if self.__isAlphaChannel:
            color = QColorDialog.getColor(self.__colorButton.color, self,
                                          u'Виберіть колір', 
                                          options=QColorDialog.ShowAlphaChannel)
        else:
            color = QColorDialog.getColor(self.__colorButton.color, self)
            
        if color.isValid():
            self.__colorButton.color = color
    
    @pyqtSlot()
    def change_standard_color(self):
        u'''Встановлює колір за промовчанням
        '''
        
        self.__colorButton.color = self.__std_colorButton.color
    
    @property
    def color(self):
        u'''Повертає вибраний колір.
        '''
        
        return self.__colorButton.color