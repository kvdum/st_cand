# -*- coding: utf-8 -*-

'''
Created on 09.05.2018.
Версія з 0.2.0. з PyQt4

Created on 1.12.2017.

@author: ichet
'''

import sys
from PyQt5.QtCore import (Qt, QAbstractItemModel, QModelIndex, pyqtSignal, 
                          QStringListModel)
from PyQt5.QtGui import QFontMetrics, QFontDatabase, QFont
from PyQt5.QtWidgets import (QApplication, QDialog, QListView, QRadioButton,
    QComboBox, QLabel, QHBoxLayout, QGridLayout, QVBoxLayout, QDialogButtonBox,
    QGroupBox, QFrame, QSizePolicy, QAbstractItemView,
    QCheckBox, qApp, QPushButton, QFontDialog, QWidget,
    QFontComboBox, QSpinBox)

#from kvFonts import free_font_path_generator

STYLE_REGULAR = 0
STYLE_BOLD = 1
STYLE_ITALIC = 2
STYLE_BOLD_ITALIC = 3
STYLE_THIN = 4
STYLE_LIGHT = 5
STYLE_BLACK = 6

#font_id = fontDatabase.addApplicationFont(
#    r'C:\Users\ichet\Dropbox\MyApps\workspace4.6\kwWorkPrint\workGenerator\fonts\Hack\Hack-Regular.ttf')
#for font_name in fonts_ttf:
#    fontIds.append(fontDatabase.addApplicationFont(os.path.join(r'')))
#fontDatabase.removeAllApplicationFonts()
#fontIds = []
#for font_fname in fonts_ttf:
#    fontIds.append(fontDatabase.addApplicationFont(font_fname))

class KwFontDataChoicer(QWidget):
    u'''
    @version: 0.1.1
    '''
    
    fontChanged = pyqtSignal(str, name='fontChanged')
    font_sizeChanged = pyqtSignal(int, name='font_sizeChanged')
    
    def __init__(self, font='', size=10, *args, **kwargs):
        super(KwFontDataChoicer, self).__init__(*args, **kwargs)
        
        self.__fontChoice = QFontComboBox(self)
        self.__fontChoice.setCurrentFont(QFont(font))
        #.setCurrentText(font)
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
        layout.addWidget(self.__fontChoice, 1)
        layout.addWidget(self.__font_sizeEdit, 0)
    
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

class KwWorkFontDialog(QDialog):
    u'''Діалогове вікно вибору шрифта
    
    @version: 0.1.0
    '''
    
    
    
    def __init__(self, *args, **kwargs):
        super(KwWorkFontDialog, self).__init__(*args, **kwargs)
        
        #fontIds = []
        #for font_fname in free_font_path_generator():
        #    fontIds = QFontDatabase.addApplicationFont(font_fname)
        #QFontDatabase.removeAllApplicationFonts()
        
        fontFreeFilterChecker = QCheckBox(u'Вільні')
        fontNoFreeFilterChecker = QCheckBox(u'Невільні')
        
        fontRating5FilterChecker = QCheckBox(u'Найкращі')
        fontRating4FilterChecker = QCheckBox(u'Добрі')
        fontRating3FilterChecker = QCheckBox(u'Задовільні')
        
        fontUseStrict_FilterChecker = QCheckBox(u'Діловодство, наука')
        fontUseWriting_FilterChecker = QCheckBox(u'Рукопис')
        fontUseFantasy_FilterChecker = QCheckBox(u'Декорації, реклама')
        
        fontFamilyListView = QListView()
        fontFamilyListView.setMinimumWidth(250)
        #fontFamilyModel = QStringListModel([str(fontDatabase.sty)])
        
        fontStyleListView = QListView()
        fontStyleListView.setFixedWidth(150)
        
        fontSizeListView = QListView()
        fontSizeListView.setFixedWidth(60)
        fontSizeModel = QStringListModel([str(v) for v in (
            6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 72)])
        fontSizeListView.setModel(fontSizeModel)
        fontSizeListView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        fontSampleWidget = QLabel(u'ІіЇїРр')
        fontSampleWidget.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        fontSampleWidget.setStyleSheet(r'''QLabel {
          font: normal normal 72pt "Consolas";
          padding: 3px;
          qproperty-alignment: AlignCenter;
          color: black;
          background-color: white;
          }''')
        
        sampleGroup = QGroupBox(u'Зразок:')
        sampleLayout = QHBoxLayout(sampleGroup)
        sampleLayout.addWidget(fontSampleWidget)
        
        fontFilterLayout = QHBoxLayout()
        
        fontAccessFilterGroup = QGroupBox(u'Доступність:')
        fontAccessFilterLayout = QVBoxLayout(fontAccessFilterGroup)
        fontAccessFilterLayout.addWidget(fontFreeFilterChecker)
        fontAccessFilterLayout.addWidget(fontNoFreeFilterChecker)
        fontAccessFilterLayout.addStretch()
        fontFilterLayout.addWidget(fontAccessFilterGroup)
        
        fontUseFilterGroup = QGroupBox(u'Призначення:')
        fontUseFilterLayout = QVBoxLayout(fontUseFilterGroup)
        fontUseFilterLayout.addWidget(fontUseStrict_FilterChecker)
        fontUseFilterLayout.addWidget(fontUseWriting_FilterChecker)
        fontUseFilterLayout.addWidget(fontUseFantasy_FilterChecker)
        fontFilterLayout.addWidget(fontUseFilterGroup)
        
        fontRatingFilterGroup = QGroupBox(u'Оцінка:')
        fontRatingFilterLayout = QVBoxLayout(fontRatingFilterGroup)
        fontRatingFilterLayout.addWidget(fontRating5FilterChecker)
        fontRatingFilterLayout.addWidget(fontRating4FilterChecker)
        fontRatingFilterLayout.addWidget(fontRating3FilterChecker)
        fontFilterLayout.addWidget(fontRatingFilterGroup)
        
        fontLayout = QGridLayout()
        
        familyLayout = QVBoxLayout()
        familyLayout.setSpacing(3)
        familyLayout.addWidget(QLabel(u'Шрифт:'))
        familyLayout.addWidget(fontFamilyListView)
        fontLayout.addLayout(familyLayout, 0, 0)
        
        styleLayout = QVBoxLayout()
        styleLayout.setSpacing(3)
        styleLayout.addWidget(QLabel(u'Стиль:'))
        styleLayout.addWidget(fontStyleListView)
        fontLayout.addLayout(styleLayout, 0, 1)
        
        sizeLayout = QVBoxLayout()
        sizeLayout.setSpacing(3)
        sizeLayout.addWidget(QLabel(u'Розмір:'))
        sizeLayout.addWidget(fontSizeListView)
        fontLayout.addLayout(sizeLayout, 0, 2)
        
        fontLayout.addWidget(sampleGroup, 1, 0, 1, 3)
        
        bbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        
        layout = QVBoxLayout(self)
        testButton = QPushButton(u'Тестова: відкрити шрифт')
        testButton.clicked.connect(lambda: QFontDialog.getFont())
        layout.addWidget(testButton)
        layout.addLayout(fontFilterLayout)
        layout.addLayout(fontLayout)
        layout.addSpacing(5)
        layout.addWidget(bbox)
        
        self.setWindowTitle(u'Вибір шрифта')
        self.setWindowFlags(self.windowFlags() ^ Qt.WindowContextHelpButtonHint)
        
        # Налаштування.
        fontMaxPointSize = fontSizeListView.font()
        # print(QFontDatabase.families())
        fontMaxPointSize.setPointSize(72)
        fm = QFontMetrics(fontMaxPointSize)
        fontSampleWidget.setMinimumHeight(fm.size(Qt.TextSingleLine 
                             | Qt.TextShowMnemonic, u'Їр').height())
        
        fontSizeListView.setCurrentIndex(fontSizeModel.match(fontSizeModel.index(
            0, 0), Qt.DisplayRole, fontSizeListView.font().pointSize())[0])
        
        fontFreeFilterChecker.setChecked(True)
        
        fontUseStrict_FilterChecker.setChecked(True)
        
        fontRating5FilterChecker.setChecked(True)
        fontRating4FilterChecker.setChecked(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = KwWorkFontDialog()
    window.exec_()
    sys.exit(app.exec_())