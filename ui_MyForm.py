# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\ichet\Dropbox\MyApps\workspace4.6\edu_work\MyForm.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MyForm(object):
    def setupUi(self, MyForm):
        MyForm.setObjectName("MyForm")
        MyForm.resize(300, 70)
        self.horizontalLayout = QtWidgets.QHBoxLayout(MyForm)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(MyForm)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.btnQuit = QtWidgets.QPushButton(MyForm)
        self.btnQuit.setObjectName("btnQuit")
        self.verticalLayout.addWidget(self.btnQuit)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(MyForm)
        QtCore.QMetaObject.connectSlotsByName(MyForm)

    def retranslateUi(self, MyForm):
        _translate = QtCore.QCoreApplication.translate
        MyForm.setWindowTitle(_translate("MyForm", "Моя форма"))
        self.label.setText(_translate("MyForm", "Тестовий надпис"))
        self.btnQuit.setText(_translate("MyForm", "Надпис на кнопці. Клікай, скільки завгодно!!!"))

