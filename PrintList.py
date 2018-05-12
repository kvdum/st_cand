# -*- coding: utf-8 -*-

'''
Created on 19.09.2017.

@author: anton
'''

from PyQt5 import QtCore, QtGui, QtPrintSupport
import os
os.chdir(r'C:\Users\ichet\YandexDisk\Значки')

class PrintList:
    def __init__(self):
        self.printer = QtPrintSupport.QPrinter()
        self.headerFont = QtGui.QFont('Arial', pointSize=10, 
                                      weight=QtGui.QFont.Bold)
        self.bodyFont = QtGui.QFont('Arial', pointSize=10)
        self.footerFont = QtGui.QFont('Arial', pointSize=9, italic=True)
        self.headerFlags = QtCore.Qt.AlignHCenter | QtCore.Qt.TextWordWrap
        self.bodyFlags = QtCore.Qt.TextWordWrap
        self.footerFlags = QtCore.Qt.AlignHCenter | QtCore.Qt.TextWordWrap
        color = QtGui.QColor(QtCore.Qt.black)
        self.headerPen = QtGui.QPen(color, 2)
        self.bodyPen = QtGui.QPen(color, 1)
        self.margin = 5
        self._resetData()
    
    def _resetData(self):
        self.headers = None
        self.columnWidths = None
        self.data = None
        self._brush = QtCore.Qt.NoBrush
        self._currentRowHeight = 0
        self._currentPageHeight = 0
        self._headerRowHeight = 0
        self._footerRowHeight = 0
        self._currentPageNumber = 1
        self._painter = None
    
    def printData(self):
        self._painter = QtGui.QPainter()
        self._painter.begin(self.printer)
        self._painter.setBrush(self._brush)
        if self._headerRowHeight == 0:
            # Для заголовку
            self._painter.setFont(self.headerFont)
            self._headerRowHeight = self._calculateRowHeight(self.columnWidths,
                                                             self.headers)
        if self._footerRowHeight == 0:
            self._painter.setFont(self.footerFont)
            self._footerRowHeight = self._calculateRowHeight([self.printer.width()],
                                                             'Сторінка')
        for i in range(len(self.data)):
            height = self._calculateRowHeight(self.columnWidths,
                                              self.data[i])
            if self._currentPageHeight + height > self.printer.height() - \
                self._footerRowHeight - 2*self.margin:
                self._printFooterRow()
                self._currentPageHeight = 0
                self._currentPageNumber += 1
                self.printer.newPage()
            if self._currentPageHeight == 0:
                self._painter.setPen(self.headerPen)
                self._painter.setFont(self.headerFont)
                self.printRow(self.columnWidths, self.headers,
                              self._headerRowHeight, self.headerFlags)
                self._painter.setPen(self.bodyPen)
                self._painter.setFont(self.bodyFont)
            self.printRow(self.columnWidths, self.data[i], height,
                          self.bodyFlags)
        self._printFooterRow()
        self._painter.end()
        self._resetData()
    
    def _calculateRowHeight(self, widths, cellData):
        # Визначення максимальної висоти рядка
        height = 0
        for i in range(len(widths)):
            # Визначення мінімального граничного прямокутника, куди би
            # помістився текст. Мінімальна - 50 пікселів.
            r = self._painter.boundingRect(0, 0, widths[i] - 2*self.margin, 50, 
                                           QtCore.Qt.TextWordWrap, str(cellData[i]))
            h = r.height() + 2*self.margin
            if height < h:
                height = h
        return height
    
    def printRow(self, widths, cellData, height, flags):
        # Друкує рядок
        x = 0
        for i in range(len(widths)):
            self._painter.drawText(x + self.margin, self._currentPageHeight + \
                                   self.margin, widths[i] - 2*self.margin, 
                                   height - 2*self.margin, flags, str(cellData[i]))
            self._painter.drawRect(x, self._currentPageHeight,
                                   widths[i], height)
            x += widths[i]
        self._currentPageHeight += height
    
    def _printFooterRow(self):
        # Нижній колонтитул
        self._painter.setFont(self.footerFont)
        self._painter.drawText(self.margin, self.printer.height() - 
                               self._footerRowHeight - self.margin, 
                               self.printer.width() - 2*self.margin, 
                               self._footerRowHeight - 2*self.margin, 
                               self.footerFlags, 'Сторінка ' + str(self._currentPageNumber))