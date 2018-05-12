# -*- coding: utf-8

'''
Created on 5.03.2018.

@author: ichet
'''

import locale
locale.setlocale(locale.LC_ALL, '') # Для сортування.

import sys
import mysql.connector

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QApplication, QFormLayout,\
    QCompleter

config = {
    'user': 'root',
    'password': '126635&msl-84',
    'host': '127.0.0.1',
    'database': 'location',
    'raise_on_warnings': True,
    'use_pure': False
    }

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

def load_villages():
    cursor.execute('SELECT id_village, village, area, region FROM '
        'ua_village, ua_area, ua_region WHERE '
        'ua_village.id_area=ua_area.id_area AND ua_area.id_region=ua_region.id_region '
        'ORDER BY village;')
    return 1#cursor.fetch_all()

class KwWindow(QWidget):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        layout = QFormLayout(self)
        
        self.__villageChoice = QComboBox()
        self.__villageChoice.setEditable(True)
        
        load_villages()
        for id_village, village, area, region in cursor:
            #print(id_village, village, area, region)
            self.__villageChoice.addItem('{}, {}, {}'.format(village, area, region),
                                  id_village)
        #self.__villageChoice.setCompleter(QCompleter(['1', '2', '3'], self))
        
        layout.addRow('Географічний пункт:', self.__villageChoice)
        
        self.__latitudeLabel = QLabel('-')
        self.__latitudeLabel.setObjectName('latitudeLabel')
        
        self.__longitudeLabel = QLabel('-')
        self.__longitudeLabel.setObjectName('longitudeLabel')
        
        self.__altitudeLabel = QLabel('-')
        self.__altitudeLabel.setObjectName('altitudeLabel')
        
        layout.addRow('Широта:', self.__latitudeLabel)
        layout.addRow('Довгота:', self.__longitudeLabel)
        layout.addRow('Висота:', self.__altitudeLabel)
        
        self.setStyleSheet('''
            QLabel#latitudeLabel, QLabel#longitudeLabel, QLabel#altitudeLabel {
                font-weight: bold;
        }''')
        
        self.setWindowTitle('KwLocation - пошуковик географічних пунктів')
        
        # >>>
        self.__villageChoice.activated[int].connect(self.choice_geodata)
    
    def choice_geodata(self, index):
        village_id = self.__villageChoice.itemData(index)
        cursor.execute('SELECT latitude, longitude, altitude FROM ua_geocoords '
                       'WHERE id_village={};'.format(village_id))
        latitude, longitude, altitude = cursor.fetchone()
        self.__latitudeLabel.setNum(latitude)
        self.__longitudeLabel.setNum(longitude)
        self.__altitudeLabel.setNum(altitude)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = KwWindow()
    window.show()
    sys.exit(app.exec())

cursor.close()
cnx.close()