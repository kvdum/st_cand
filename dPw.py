#! /usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Created on 10 трав. 2017 р.

@author: kavedium
'''

import sys, os
import json
import datetime as dt
#import locale
#locale.setlocale(locale.LC_ALL, '')

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout,\
    QLineEdit, QMainWindow, QMenu, QAction, QMessageBox, QTableView, \
    QAbstractItemView, QSpinBox, QGridLayout, QLabel, QFontComboBox, QGroupBox,\
    QHBoxLayout, QToolBar
from PyQt5.Qt import QKeySequence, QApplication
from PyQt5.QtCore import Qt, pyqtSlot, QLocale, QLibraryInfo, QTranslator, \
                        QAbstractTableModel, QVariant
from PyQt5.QtGui import QIcon, QColor, QBrush

DOCMAP = {'doc': {'data': [{'N': 0, 'Type': '', 't': 0, 'Q': 0, 'l': 0, 
                            'Material': '', 'Manufactur': '', 'd': '', 
                            'Zeta': ''}],
                  'info': {'version': '',
                           'datetime': dt.datetime.utcnow()}
                 }
         }

publish_info = {'to_whom': '', 'page_start': 0,
                               'append_num': 0, 'section_name': '',
                               'font': ''}

class PublishInfo:
    
    def __init__(self, to_whom='', page_start=0, append_num=0, section_name=0,
                 font=''):
        self.to_whom = to_whom
        self.page_start = page_start
        self.append_num = append_num
        self.section_name = section_name
        self.font = font
    
    @property
    def to_whom(self):
        return self.__to_whom
    
    @to_whom.setter
    def to_whom(self, value):
        self.__to_whom = str(value)
    
    @property
    def page_start(self):
        return self.__page_start
    
    @page_start.setter
    def page_start(self, value):
        if not isinstance(value, int):
            raise TypeError('Початкова сторінка повинна бути числом')
        
        if value < 1:
            raise ValueError('Початкова сторінка має бути більше 0')
        
        self.__page_start = int(value)
    
    @property
    def append_num(self):
        return self.__append_num
    
    @append_num.setter
    def append_num(self, value):
        if not isinstance(value, int):
            raise TypeError('№ табл./дод. повинна бути числом')
        
        if value < 1:
            raise ValueError('№ табл./дод. має бути більше 0')
        
        self.__append_num = int(value)
    
    @property
    def section_name(self):
        return self.__section_name
    
    @section_name.setter
    def section_name(self, value):
        self.__section_name = str(value)
    
    @property
    def font(self):
        return self.__font
    
    @font.setter
    def font(self, value):
        self.__font = str(value)

class DPw:
    
    def __init__(self, N, type_='', t=0, Q=0, l=0, material='', d='', zeta=''):
        self.__N = N
        self.__type_ = type_
        self.__t = t
        self.__Q = Q
        self.__l = l
        self.__material = material
        self.__manufactur = manufactur
        self.__d = d
        self.__zeta = zeta
    
    @property
    def N(self):
        return self.__N
    
    @N.setter
    def N(self, value):
        if not isinstance(value, int):
            raise TypeError('Номер ділянки має бути цілим числом')
        
        if value < 1:
            raise ValueError('Номер ділянки має бути більший 0')
        
        self.__N = value
    
    @property
    def type_(self):
        return self.__type_
    
    @type_.setter
    def type_(self, value):
        self.__type_ = str(type_)
    
    @property
    def t(self):
        return self.__t
    
    @t.setter
    def t(self, value):
        try:
            self.__t = float(value)
        except TypeError:
            raise TypeError('t має бути числом')
        
        if value < 0:
            raise ValueError("t не має бути від'мною")
    
    @property
    def Q(self):
        return self.__Q
    
    @Q.setter
    def Q(self, value):
        try:
            self.__Q = float(value)
        except TypeError:
            raise TypeError('Q має бути числом')
        
        if value < 0:
            raise ValueError("Q не має бути від'мною")
    
    @property
    def l(self):
        return self.__l
    
    @l.setter
    def l(self, value):
        try:
            self.__l = float(value)
        except TypeError:
            raise TypeError('l має бути числом')
        
        if value < 0:
            raise ValueError("l не має бути від'мною")
    
    @property
    def material(self):
        return self.__material
    
    @material.setter
    def material(self, value):
        self.__material = str(value)
    
    @property
    def d(self):
        return self.__d
    
    @d.setter
    def d(self, value):
        value = str(value).upper().split('x')
        
        def is_number(val):
            if not val.replace('.', '', 1).isdigit():
                raise ValueError('Некоректно задано d')
        
        if len(value) == 1:
            value = is_number(value.strip())
        elif len(value) == 2:
            v1, v2 = value
            value = is_number(v1.strip())+'x'+is_number(v2.strip())
        else:
            raise ValueError('Некоректно задано d')
        
        self.__d = value
    
    @property
    def zeta(self):
        return self.__zeta
    
    @zeta.setter
    def zeta(self, value):
        self.__zeta = str(value)

class Document:
    
    __docmap = None
    
    @staticmethod
    def set_docmap(docmap):
        Document.__docmap = docmap
    
    @staticmethod
    def get_docmap():
        return Document.__docmap
    
    def __init__(self, default_short_title='Невідомий', 
                 ext_title=None):
        
        self.__init_dt = dt.datetime.utcnow()
        
        #self.__default_dirpath = default_dirpath
        ext = (os.extsep + ext_title) if ext_title else ''
        self.__ext = ext
        self.__defaul_title = default_short_title + ext
        self.__title = self.__defaul_title
    
    @property
    def init_dt(self):
        return self.__init_dt
    
    @property
    def default_title(self):
        return self.__defaul_title
    
    @property
    def ext(self):
        return self.__ext
    
    @property
    def title(self):
        return self.__title
    
    @title.setter
    def title(self, title):
        self.__title = title
        self.__path_to_file = os.path.dirname(title)
    
    @property
    def path_to_file(self):
        return self.__path_to_file
    
    @path_to_file.setter
    def path_to_file(self, path_to_file):
        self.__path_to_file = path_to_file
        self.__title = os.path.filename(path_to_file)
    
    def open(self, path_to_file):
        pass
    
    def save(self, path_to_file, data):
        self.__path_to_file = path_to_file
        
        data = [['1', 'T-11', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5'],
                ['1', 'T-21', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20x5,5', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5'],
                ['1', 'T-11', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20x5,5', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5']
                 ]
        
        obj_data = []
        for row in data:
            row_data = {}
            row_data[]
        
        #try:
         #   with open(self.__path_to_file, 'r', encoding='utf-8'):
          #      jon.dump()
        
        #json.dump(obj, fp, skipkeys, ensure_ascii, check_circular, allow_nan, cls, indent, separators, default, sort_keys)

class ContentWidget(QWidget):
    
    def __init__(self, parent):
        super().__init__(parent=parent)
        
        to_whomEdit = QLineEdit(self)
        section_nameEdit = QLineEdit(self)
        fontChoice = QFontComboBox(self)
        page_startEdit = QSpinBox(self)
        page_startEdit.setRange(1, 1000)
        page_startEdit.setSuffix(' стор.')
        append_numEdit = QSpinBox(self)
        append_numEdit.setRange(1, 100)
        
        publishGroupBox = QGroupBox('Для публікації', self)
        publishLayout = QGridLayout(publishGroupBox)
        
        publishLayout.addWidget(QLabel('Кому:'), 0, 0)
        publishLayout.addWidget(to_whomEdit, 0, 1)
        
        publishLayout.addWidget(QLabel('Почати з:'), 0, 3)
        publishLayout.addWidget(page_startEdit, 0, 4)
        
        publishLayout.addWidget(QLabel('№ табл./дод.:'), 0, 6)
        publishLayout.addWidget(append_numEdit, 0, 7)
        
        publishLayout.addWidget(QLabel('Назва розділу:'), 1, 0)
        publishLayout.addWidget(section_nameEdit, 1, 1)
        
        publishLayout.addWidget(QLabel('Шрифт:'), 1, 3)
        publishLayout.addWidget(fontChoice, 1, 4, 1, 4)
        
        publishLayout.setColumnMinimumWidth(2, 5)
        
        t1Edit = QSpinBox(self)
        t1Edit.setRange(0, 150)
        t1Edit.setValue(95)
        t1Edit.setSuffix(' \N{DEGREE CELSIUS}')
        
        t2Edit = QSpinBox(self)
        t2Edit.setRange(0, 150)
        t2Edit.setValue(70)
        t2Edit.setSuffix(' \N{DEGREE CELSIUS}')
        
        tLayout = QHBoxLayout()
        tLayout.addWidget(QLabel('t_1:'))
        tLayout.addWidget(t1Edit)
        tLayout.addSpacing(5)
        tLayout.addWidget(QLabel('t_2:'))
        tLayout.addWidget(t2Edit)
        tLayout.addStretch()
        
        dPwWidget = KwDPwWidget(self)
        dPwWidget.layout().setContentsMargins(0, 0, 0, 0)
        
        layout = QVBoxLayout(self)
        layout.addWidget(publishGroupBox)
        layout.addLayout(tLayout)
        layout.addWidget(dPwWidget)
    
class KwDPwWidget(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        table = self.createTable()
        
        sums_sheet = '''QLabel {
                        background-color: yellow;
                        padding: 2px;
                        border: 1px solid blue;
                        font-weight: bold;
                      }'''
        
        sum_lLabel = QLabel('52,17', self)
        sum_lLabel.setStyleSheet(sums_sheet)
        
        sumRlLabel = QLabel('-', self)
        sumRlLabel.setStyleSheet(sums_sheet)
        
        sumZLabel = QLabel('-', self)
        sumZLabel.setStyleSheet(sums_sheet)
        
        sumRlZLabel = QLabel('-', self)
        sumRlZLabel.setStyleSheet(sums_sheet)
        
        sum_infoLayout = QHBoxLayout()
        sum_infoLayout.addStretch()
        
        sum_infoLayout.addWidget(QLabel('\N{N-ARY SUMMATION}l, м:'))
        sum_infoLayout.addWidget(sum_lLabel)
        sum_infoLayout.addSpacing(5)
        
        sum_infoLayout.addWidget(QLabel('\N{N-ARY SUMMATION}R\N{MIDDLE DOT}l, Па:'))
        sum_infoLayout.addWidget(sumRlLabel)
        sum_infoLayout.addSpacing(5)
        
        sum_infoLayout.addWidget(QLabel('Z, Па:'))
        sum_infoLayout.addWidget(sumZLabel)
        sum_infoLayout.addSpacing(5)
        
        sum_infoLayout.addWidget(QLabel('\N{N-ARY SUMMATION}(R\N{MIDDLE DOT}l+Z) Па:'))
        sum_infoLayout.addWidget(sumRlZLabel)
        
        layout = QVBoxLayout(self)
        layout.addWidget(table)
        layout.addLayout(sum_infoLayout)
    
    def createTable(self):
        table = QTableView(self)
        
        header = ['№\nділ.', 'Тип', 't,\n\N{DEGREE CELSIUS}', 'Q, Вт', 'G,\nкг/год', 
                  'L, л/с', 'l, м', 'Матеріал', 'Виробник', 
                  'dв\n(dз\N{MULTIPLICATION SIGN}\N{GREEK SMALL LETTER DELTA}),\nмм', 
                  'v,\nм/с', 'R,\nПа/м', 'R\N{MIDDLE DOT}l,\nПа', 
                  '\N{GREEK SMALL LETTER ZETA}', 
                  '\N{N-ARY SUMMATION}\N{GREEK SMALL LETTER ZETA}', 
                  'Z, Па', '\N{N-ARY SUMMATION}(R\N{MIDDLE DOT}l+Z),\nПа']
        tableModel = DPwTableModel(self.table_data(), header, parent=self)
        table.setModel(tableModel)
        self.setMinimumSize(400, 300)
        
        table.setShowGrid(True)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        verticalHeader = table.verticalHeader()
        verticalHeader.setVisible(True)
        
        horizontalHeader = table.horizontalHeader()
        horizontalHeader.setStretchLastSection(True)
        
        table.resizeColumnsToContents()
        
        nrows = len(self.table_data())
        for row in range(nrows):
            table.setRowHeight(row, 18)
        
        table.setSortingEnabled(True)
        
        return table
    
    def table_data(self):
        data = [['1', 'T-11', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5'],
                ['1', 'T-21', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20x5,5', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5'],
                ['1', 'T-11', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20x5,5', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5'],
                ['1', 'T-21', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20x5,5', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5'],
                ['1', 'T-11', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20x5,5', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5'],
                ['1', 'T-11', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5'],
                ['1', 'T-21', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20x5,5', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5'],
                ['1', 'T-11', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20x5,5', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5'],
                ['1', 'T-21', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20x5,5', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5'],
                ['1', 'T-11', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20x5,5', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5'],
                ['1', 'T-11', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5'],
                ['1', 'T-21', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20x5,5', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5'],
                ['1', 'T-11', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20x5,5', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5'],
                ['1', 'T-21', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20x5,5', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5'],
                ['1', 'T-11', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20x5,5', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5'],
                ['1', 'T-11', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5'],
                ['1', 'T-21', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20x5,5', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5'],
                ['1', 'T-11', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20x5,5', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5'],
                ['1', 'T-21', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20x5,5', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5'],
                ['1', 'T-11', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20x5,5', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5'],
                ['1', 'T-11', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5'],
                ['1', 'T-21', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20x5,5', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5'],
                ['1', 'T-11', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20x5,5', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5'],
                ['1', 'T-21', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20x5,5', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5'],
                ['1', 'T-11', '90', '1800', '315', '23,5', '50', 'met', 'Eko', '20x5,5', '0.1', '3.1',
                 '15.2', '2*{k90}*0,5+3*{t}*1,5+2*{kr)*0,3+4*{o}*1+2*{r}*1,5', '9.1', '13,1', '16.5']
               ]
        return data

class DPwTableModel(QAbstractTableModel):
    
    def __init__(self, data_in, header_data, parent=None, *args):
        
        super().__init__(parent, *args)
        
        self.array_data = data_in
        self.header_data = header_data
    
    def rowCount(self, parent):
        return len(self.array_data)
    
    def columnCount(self, parent):
        return len(self.array_data[0])
    
    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role == Qt.BackgroundRole:
            if index.column() in (*range(10, 13), *range(14, 17)):
                return QBrush(QColor('#ffe6e6'))
            if index.row() % 2 == 0:
                return QBrush(QColor(255, 255, 255))
            else:
                return QBrush(QColor(255, 255, 225))
        elif role == Qt.TextAlignmentRole:
            if index.column() in (7, 8, 13):
                return Qt.AlignLeft | Qt.AlignVCenter
            else:
                return Qt.AlignCenter
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.array_data[index.row()][index.column()])
    
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.header_data[col])
        elif orientation == Qt.Vertical:
            if role == Qt.DisplayRole:
                return QVariant(col+1)
            elif role == Qt.TextAlignmentRole:
                return Qt.AlignCenter | Qt.AlignVCenter
        return QVariant()
    
    def sort(self, Ncol, order):
        pass
        #self.emit()

class KwMainWindow(QMainWindow):
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        KWApp.this.windows.append(self)
        
        menubar = self.menuBar()
        
        contentWidget = ContentWidget(self)
        self.setCentralWidget(contentWidget)
        
        message = 'Привіт, я готова до роботи!'
        self.statusBar().showMessage(message)
        
        self.createActions()
        self.createMenus()
        self.create_toolbars()
        
        self.setWindowTitle('Гідравлічний розрахунок системи опалення')
    
    def create_toolbars(self):
        stdTooBbar = QToolBar('Стандартна')
        stdTooBbar.addAction(self.newAct)
        stdTooBbar.addAction(self.openAct)
        stdTooBbar.addAction(self.saveAct)
        stdTooBbar.addSeparator()
        stdTooBbar.addAction(self.printAct)
        stdTooBbar.addSeparator()
        stdTooBbar.addAction(self.cutAct)
        stdTooBbar.addAction(self.copyAct)
        stdTooBbar.addAction(self.pasteAct)
        stdTooBbar.addSeparator()
        stdTooBbar.addAction(self.undoAct)
        stdTooBbar.addAction(self.redoAct)
        
        tableToolBar = QToolBar('Таблиця')
        tableToolBar.addAction(self.append_table_rowAct)
        tableToolBar.addAction(self.insert_table_rowAct)
        tableToolBar.addAction(self.remove_table_rowsAct)
        
        self.addToolBar(stdTooBbar)
        self.addToolBar(tableToolBar)
    
    def createMenus(self):
        menubar = self.menuBar()
        
        fileMenu = menubar.addMenu('&Файл')
        fileMenu.addAction(self.newAct)
        fileMenu.addAction(self.openAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.saveAct)
        fileMenu.addAction(self.save_asAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exportAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.printAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.propertiesAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.closeAct)
        
        editMenu = menubar.addMenu('&Зміни')
        editMenu.addAction(self.undoAct)
        editMenu.addAction(self.redoAct)
        editMenu.addSeparator()
        editMenu.addAction(self.cutAct)
        editMenu.addAction(self.copyAct)
        editMenu.addAction(self.pasteAct)
        editMenu.addSeparator()
        editMenu.addAction(self.select_allAct)
        
        tableMenu = menubar.addMenu('&Таблиця')
        tableMenu.addAction(self.append_table_rowAct)
        tableMenu.addAction(self.insert_table_rowAct)
        tableMenu.addAction(self.remove_table_rowsAct)
        tableMenu.addSeparator()
        tableMenu.addAction(self.cleart_tableAct)
        
        helpMenu = menubar.addMenu('&Довідка')
        helpMenu.addAction(self.aboutAct)
        helpMenu.addAction(self.aboutQtAct)
    
    def createActions(self):
        self.newAct = QAction(QIcon.fromTheme("document-new"), '&Новий', self)
        self.newAct.setShortcuts(QKeySequence.New)
        self.newAct.setStatusTip('Створює новий файл')
        self.newAct.triggered.connect(self.newFile)
        
        self.openAct = QAction(QIcon.fromTheme("document-open"), 'Відкрити...', self)
        self.openAct.setShortcuts(QKeySequence.Open)
        self.openAct.setStatusTip('Відкриває файл')
        self.openAct.triggered.connect(self.open)
        
        self.saveAct = QAction(QIcon.fromTheme("document-save"), 'Зберегти', self)
        self.saveAct.setShortcuts(QKeySequence.Save)
        self.saveAct.setStatusTip('Зберігає файл')
        self.saveAct.triggered.connect(self.save)
        
        self.save_asAct = QAction(QIcon.fromTheme("document-save-as"), 'Зберегти як...', self)
        self.save_asAct.setShortcuts(QKeySequence.SaveAs)
        self.save_asAct.setStatusTip('Зберігає файл під новим іменем')
        self.save_asAct.triggered.connect(self.save)
        
        self.exportAct = QAction('Експорт...', self)
        self.exportAct.setStatusTip('Експортує вміст файлу в інші формати')
        self.exportAct.triggered.connect(self.export)
        
        self.printAct = QAction(QIcon.fromTheme("document-print"), 'Друк...', self)
        self.printAct.setShortcuts(QKeySequence.Print)
        self.printAct.setStatusTip('Друкує вміст файлу')
        self.printAct.triggered.connect(self.print_)
        
        self.propertiesAct = QAction(QIcon.fromTheme("document-properties"), 
                                     'Властивості...', self)
        self.propertiesAct.setStatusTip('Властивості файлу')
        self.propertiesAct.triggered.connect(self.properties)
        
        self.closeAct = QAction(QIcon.fromTheme("window-close"), 'Закрити', self)
        self.closeAct.setShortcuts(QKeySequence.Close)
        self.closeAct.setStatusTip('Закриває вікно')
        self.closeAct.triggered.connect(self.closeWindow)
        
        self.undoAct = QAction(QIcon.fromTheme("edit-undo"), 'Скасувати', self)
        self.undoAct.setShortcuts(QKeySequence.Undo)
        self.undoAct.setStatusTip('Скасовує зміни')
        self.undoAct.triggered.connect(self.undo)
        
        self.redoAct = QAction(QIcon.fromTheme("edit-redo"), 'Повернути', self)
        self.redoAct.setShortcuts(QKeySequence.Redo)
        self.redoAct.setStatusTip('Повертає скасовані зміни')
        self.redoAct.triggered.connect(self.redo)
        
        self.cutAct = QAction(QIcon.fromTheme("edit-cut"), 'Вирізати', self)
        self.cutAct.setShortcuts(QKeySequence.Cut)
        self.cutAct.setStatusTip('Вирізає вміст в буфер обміну')
        self.cutAct.triggered.connect(self.cut)
        
        self.copyAct = QAction(QIcon.fromTheme("edit-copy"), 'Копіювати', self)
        self.copyAct.setShortcuts(QKeySequence.Copy)
        self.copyAct.setStatusTip('Копіює вміст в буфер обміну')
        self.copyAct.triggered.connect(self.copy)
        
        self.pasteAct = QAction(QIcon.fromTheme("edit-paste"), 'Вставити', self)
        self.pasteAct.setShortcuts(QKeySequence.Paste)
        self.pasteAct.setStatusTip('Вставляє вміст з буфер обміну')
        self.pasteAct.triggered.connect(self.paste)
        
        self.select_allAct = QAction(QIcon.fromTheme("edit-select-all"), 
                                     'Вибрати все', self)
        self.select_allAct.setShortcuts(QKeySequence.SelectAll)
        self.select_allAct.setStatusTip('Виділяє весь вміст')
        self.select_allAct.triggered.connect(self.select_all)
        
        
        self.append_table_rowAct = QAction(QIcon.fromTheme("list-add"),
                                           'Додати рядок', self)
        self.append_table_rowAct.setStatusTip('Додає пустий рядок в таблицю')
        self.append_table_rowAct.triggered.connect(self.append_table_row)
        
        self.insert_table_rowAct = QAction(QIcon.fromTheme("insert-object"),
                                           'Вставити рядок', self)
        self.insert_table_rowAct.setStatusTip('Вставляє пустий рядок в таблицю')
        self.insert_table_rowAct.triggered.connect(self.insert_table_row)
        
        self.remove_table_rowsAct = QAction(QIcon.fromTheme("list-remove"), 
                                            'Видалити рядки', self)
        self.remove_table_rowsAct.setStatusTip('Видаляє виділені рядки з таблиці')
        self.remove_table_rowsAct.triggered.connect(self.remove_table_rows)
        
        self.cleart_tableAct = QAction(QIcon.fromTheme("edit-clear"), 
                                       'Очистити таблицю', self)
        self.cleart_tableAct.setStatusTip('Видаляє всі рядки таблиці')
        self.cleart_tableAct.triggered.connect(self.clear_table)
        
        
        self.aboutAct = QAction(QIcon.fromTheme("help-about"), 'Про програму...', self)
        self.aboutAct.setStatusTip('Показує інформацію про програму')
        self.aboutAct.triggered.connect(self.about)
        
        self.aboutQtAct = QAction('Про Qt...', self)
        self.aboutQtAct.setStatusTip('Показує інформацію про графічний фреймворк Qt')
        self.aboutQtAct.triggered.connect(self.aboutQt)
    
    @pyqtSlot()
    def newFile(self):
        win = KwMainWindow()
        win.show()
        
    @pyqtSlot()
    def open(self):
        pass
    
    @pyqtSlot()
    def save(self):
        pass
        #fname = QtGui.QFileDialog.getSaveFileName(self, 
         # directory=os.path.join(winpaths.get_my_documents(), 
          #  proposed_history_name()), filter=u'Історія (*%s)' % HISTORY_DB_EXT))
    
    @pyqtSlot()
    def export(self):
        pass
    
    @pyqtSlot()
    def print_(self):
        pass
    
    @pyqtSlot()
    def properties(self):
        pass
    
    @pyqtSlot()
    def closeWindow(self):
        self.close()
    
    @pyqtSlot()
    def undo(self):
        pass
    
    @pyqtSlot()
    def redo(self):
        pass
    
    @pyqtSlot()
    def cut(self):
        pass
    
    @pyqtSlot()
    def copy(self):
        pass
    
    @pyqtSlot()
    def paste(self):
        pass
    
    @pyqtSlot()
    def select_all(self):
        pass
    
    @pyqtSlot()
    def append_table_row(self):
        pass
    
    @pyqtSlot()
    def insert_table_row(self):
        pass
    
    @pyqtSlot()
    def remove_table_rows(self):
        pass
    
    @pyqtSlot()
    def clear_table(self):
        pass
    
    @pyqtSlot()
    def about(self):
        QMessageBox.about(self, QApplication.applicationDisplayName(), 
          '''<strong>{name}</strong><br>Версія: <strong>{version}</strong><br>
Copyright \N{COPYRIGHT SIGN} {organization}, {years}<br>{description}.'''.format(name=QApplication.applicationDisplayName(),
            version=QApplication.applicationVersion(), 
            organization=QApplication.organizationName(), years='2017',
            description='Програма для гідравлічного розрахунку системи опалення'))
    
    @pyqtSlot()
    def aboutQt(self):
        QMessageBox.aboutQt(self)
    
    def closeEvent(self, e):
        result = QMessageBox.warning(self, QApplication.applicationDisplayName(), 
                  'Зберегти дані перед закриттям?', QMessageBox.Save | \
                  QMessageBox.Discard | QMessageBox.Cancel, QMessageBox.Save)
        
        if result == QMessageBox.Save:
            self.save()
            e.accept()
        elif result == QMessageBox.Discard:
            e.accept()
        else:
            e.ignore()

class KWApp(QApplication):
    
    this = None
    
    def __init__(self, args):
        super().__init__(args)
        
        self.setDefaultAppLocale()
        
        self.windows = []
        
        KWApp.this = self

    def setDefaultAppLocale(self):
        
        translationsPath = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
        locale = QLocale.system()
        
        self.__qtTranslator = QTranslator()
        if self.__qtTranslator.load(locale, "qt", "_", translationsPath):
            self.installTranslator(self.__qtTranslator)
        
        self.__qtBaseTranslator = QTranslator()
        if self.__qtBaseTranslator.load(locale, "qtbase", "_", translationsPath):
            self.installTranslator(self.__qtBaseTranslator)

def test(n, k):
    if n == 1:
        app = KWApp(sys.argv)
    
        app.setApplicationVersion('0.1.0')
        app.setOrganizationName('Kavedium Ltd.')
        
        win = KwMainWindow()
        win.show()
        
        sys.exit(app.exec())
    if n == 2:
        if k == 1:
            d = Document()
            print(d.default_title)
            print(d.ext)
        elif k == 2:
            d = Document(ext_title='dpw')
            d.set_docmap(DOCMAP)
            print(d.get_docmap())
            print(d.default_title)
            print(d.ext)

if __name__ == '__main__':
    test(2, 2)
    