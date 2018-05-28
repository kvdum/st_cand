# coding: utf-8

import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout

class MyWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        layout = QHBoxLayout(self)
        
        label = QLabel('Як прекрасний цей світ!')
        layout.addWidget(label)

class MyApp(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.mainWnd = MyWindow()
        self.mainWnd.setWindowTitle('Hello PyQt')
        self.mainWnd.setWindowIcon(QIcon('class_x24.ico'))
        self.mainWnd.show()

if __name__ == '__main__':
    app = MyApp(sys.argv)
    sys.exit(app.exec())