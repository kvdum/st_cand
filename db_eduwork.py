# -*- coding: utf-8

'''
Created on 31.02.2018

@author: ichet
'''

from mysql.connector import MySQLConnection, Error
from dashtable import data2rst
from PIL import Image

config_eduwork = {
    'user': 'root',
    'password': '126635&msl-84',
    'host': '127.0.0.1',
    'database': 'eduwork',
    #'raise_on_warnings': True,
    'charset': 'utf8',
    'use_unicode': True,
    'get_warnings': True
    }

config_eduwork_temp = {
    'user': 'root',
    'password': '126635&msl-84',
    'host': '127.0.0.1',
    'database': 'eduwork_temp',
    #'raise_on_warnings': True,
    'charset': 'utf8',
    'use_unicode': True,
    'get_warnings': True
    }

def read_file(filename):
    with open(filename, mode='rb') as f:
        data = f.read()
    return data

def add_edu(short_title, nolong_title, title, logotype=None):
    if logotype:
        logotype = read_file(logotype)
    else:
        logotype = None
    
    query = 'INSERT INTO `edu` VALUE (%s, %s, %s, %s, %s)'
    args = None, short_title, nolong_title, title, logotype
    try:
        conn = MySQLConnection(**config_eduwork)
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
    except Error as err:
        print(err)
    else:
        print(' Навчальний заклад упішно додано! '.center(80, '='))
    finally:
        cursor.close()
        conn.close()
        
def view_edu(add_logotype=False):
    try:
        conn = MySQLConnection(**config_eduwork)
        cursor = conn.cursor()
        header = lambda: [d[0] for d in cursor.description]
        if add_logotype:
            cursor.execute('SELECT * FROM `edu`')
            print(data2rst([header(), 
                         *[[*row[:-1], row[-1][:10]+b'...' if row[-1] is not None else None] 
                           for row in cursor]], center_cells=True))
        else:
            cursor.execute('SELECT `id_edu`, `short_title`, `nolong_title`, `title` FROM `edu`')
            print(data2rst([header(), 
                         *[list(row) for row in cursor]], center_cells=True))
    except Error as err:
        print(err)
    finally:
        cursor.close()
        conn.close()

def add_institute(id_edu, short_title, title, logotype=None):
    if logotype:
        logotype = read_file(logotype)
    else:
        logotype = None
    
    query = 'INSERT INTO `institute` VALUE (%s, %s, %s, %s, %s)'
    args = None, id_edu, short_title, title, logotype
    try:
        conn = MySQLConnection(**config_eduwork)
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
    except Error as err:
        print(err)
    else:
        print(' Інститут упішно додано! '.center(80, '='))
    finally:
        cursor.close()
        conn.close()
        
def view_institute(add_logotype=False):
    try:
        conn = MySQLConnection(**config_eduwork)
        cursor = conn.cursor()
        header = lambda: [d[0] for d in cursor.description]
        if add_logotype:
            cursor.execute('SELECT * FROM `institute`')
            print(data2rst([header(), 
                         *[[*row[:-1], row[-1][:10]+b'...' if row[-1] is not None else None] 
                           for row in cursor]], center_cells=True))
        else:
            cursor.execute('SELECT `id_institute`, `id_edu`, `short_title`, `title` FROM `institute`')
            print(data2rst([header(), 
                         *[list(row) for row in cursor]], center_cells=True))
    except Error as err:
        print(err)
    finally:
        cursor.close()
        conn.close()

def add_department(id_institute, short_title, title, logotype=None):
    if logotype:
        logotype = read_file(logotype)
    else:
        logotype = None
    
    query = 'INSERT INTO `department` VALUE (%s, %s, %s, %s, %s)'
    args = None, id_institute, short_title, title, logotype
    try:
        conn = MySQLConnection(**config_eduwork)
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
    except Error as err:
        print(err)
    else:
        print(' Кафедру упішно додано! '.center(80, '='))
    finally:
        cursor.close()
        conn.close()
        
def view_department(add_logotype=False):
    try:
        conn = MySQLConnection(**config_eduwork)
        cursor = conn.cursor()
        header = lambda: [d[0] for d in cursor.description]
        if add_logotype:
            cursor.execute('SELECT * FROM `department`')
            print(data2rst([header(), 
                         *[[*row[:-1], row[-1][:10]+b'...' if row[-1] is not None else None] 
                           for row in cursor]], center_cells=True))
        else:
            cursor.execute('SELECT `id_department`, `id_institute`, `short_title`, `title` FROM `department`')
            print(data2rst([header(), 
                         *[list(row) for row in cursor]], center_cells=True))
    except Error as err:
        print(err)
    finally:
        cursor.close()
        conn.close()

def add_group(id_institute, title, course):
    
    query = 'INSERT INTO `group` VALUE (%s, %s, %s, %s)'
    args = None, id_institute, title, course
    try:
        conn = MySQLConnection(**config_eduwork)
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
    except Error as err:
        print(err)
    else:
        print(' Групу упішно додано! '.center(80, '='))
    finally:
        cursor.close()
        conn.close()
        
def view_group():
    try:
        conn = MySQLConnection(**config_eduwork)
        cursor = conn.cursor()
        header = lambda: [d[0] for d in cursor.description]
        cursor.execute('SELECT * FROM `group`')
        print(data2rst([header(), *[list(row) for row in cursor]], center_cells=True))
    except Error as err:
        print(err)
    finally:
        cursor.close()
        conn.close()

def add_account_temp(email, password, ip, mac, verification_code, is_confirmed=False):
    query = 'INSERT INTO `account_temp` VALUE (%s, %s, PASSWORD(%s), %s, %s, %s, %s, %s)'
    args = None, email, password, ip, mac, verification_code, is_confirmed, None
    try:
        conn = MySQLConnection(**config_eduwork_temp)
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
    except Error as err:
        print(err)
    else:
        print(' Тимчасовий обліковий запис створено! '.center(80, '='))
    finally:
        cursor.close()
        conn.close()

def view_account_temp(is_full=False):
    try:
        conn = MySQLConnection(**config_eduwork_temp)
        cursor = conn.cursor()
        if is_full:
            query = 'SELECT * FROM `account_temp`'
        else:
            query = 'SELECT `email`, `ip`, `mac`, `get_datetime` FROM account_temp'
        cursor.execute(query)
        print(data2rst([[d[0] for d in cursor.description], *[list(row) for row in cursor]], center_cells=True))
    except Error as err:
        print(err)
    finally:
        cursor.close()
        conn.close()

def add_user(email, password, phone_1, ph, ip, mac, verification_code, is_confirmed=False):
    query = 'INSERT INTO `account_temp` VALUE (%s, %s, PASSWORD(%s), %s, %s, %s, %s, %s)'
    args = None, email, password, ip, mac, verification_code, is_confirmed, None
    try:
        conn = MySQLConnection(**config_eduwork_temp)
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
    except Error as err:
        print(err)
    else:
        print(' Тимчасовий обліковий запис створено! '.center(80, '='))
    finally:
        cursor.close()
        conn.close()

def add_task(id_subject, state_actual, title, id_idata, view, images, id_teacher, semester, year, description, deadline, price):
    query = 'INSERT INTO `task` VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    args = None, id_subject, state_actual, title, id_idata, view, images, id_teacher, semester, year, description, deadline, price
    try:
        conn = MySQLConnection(**config_eduwork)
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
    except Error as err:
        print(err)
    else:
        print(' Завдання створено! '.center(80, '='))
    finally:
        cursor.close()
        conn.close()

def __test(n, k=1):
    if n == 1:
        add_edu('НУ "ЛП"', 'НУ "Львівська політехніка"', 
            'Національний університет "Львівська політехніка"',
            r'C:\Users\ichet\Downloads\Lviv_Polytechnic.png')
    elif n == 2:
        if k == 1:
            view_edu()
        elif k == 2:
            view_edu(add_logotype=True)
    elif n == 3:
        add_institute(39, "ІБІД", "Інститут будівництва та інженерії довкілля", 
            r'C:\Users\ichet\Downloads\327_tmp2-327_m.png')
    elif n == 4:
        if k == 1:
            view_institute()
        elif k == 2:
            view_institute(add_logotype=True)
    elif n == 5:
        add_department(1, "ТГВ", "Теплогазопостачання і вентиляції", None)
    elif n == 6:
        if k == 1:
            view_department()
        elif k == 2:
            view_department(add_logotype=True)
    elif n == 7:
        add_group(1, "ТГВ-51", 5)
    elif n == 8:
        view_group()
    elif n == 9:
        add_account_temp('kavedium@meta.ua', '12773x-aX', '127.0.0.1', 'dk9-bz', '&kz')
    elif n == 10:
        if k == 1:
            view_account_temp()
        elif k == 2:
            view_account_temp(True)
    elif n == 11:
        if k == 1:
            add_task(1, 1, 'Розрахунок теплового режиму приміщення', 1, r'\uselatex{}', 'ks', 1, 1, 2003, 'В цій роботі...', 2, 250)
            add_task(1, 3, 'Опалення і вентилція житлового будинку', 2, r'\uselatex{}', 'ks1', 2, 1, 2006, 'В цій роботі...', 2, 350)

if __name__ == '__main__':
    __test(11, 1)