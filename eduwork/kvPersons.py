# -*- coding: utf-8 -*-

'''
Created on 6.02.2018.

@author: ichet
'''

import re

from kvEduInstituteData import KvDepartment, KvGroup

_RANK_CTS = u'к.т.н.'
_RANK_DTS = u'д.т.н.'

_RANKS = (_RANK_CTS, _RANK_DTS)

_POST_A = u'асп.'
_POST_SL = u'ст.в.'
_POST_DOCENT = u'доцент'
_POST_PROFESSOR = u'професор'

_POSTS = (_POST_A, _POST_SL, _POST_DOCENT, _POST_PROFESSOR)

_re_name_pattern=u"^[A-Za-zА-яЁёЄ-ЯҐа-їґ].*$"   # Мінімум один символ, який починається з літери.
_re_name = re.compile(_re_name_pattern)

class KvPerson(object):
    u'''Дані особистості
    
    @version: 0.1.0
    '''
    
    _re_lastname_pattern=u"^[A-Za-zА-яЁёЄ-ЯҐа-їґ]*$"
    _re_lastname = re.compile(_re_lastname_pattern)
    
    def __init__(self, surname, firstname, lastname='', description=''):
        self.surname = surname
        self.firstname = firstname
        self.lastname = lastname
        self.description = description
    
    @property
    def id_(self):
        u'''@return: (int)
        '''
        
        return self._id_
    
    @property
    def surname(self):
        u'''Повертає прізвище
        
        @return: (str)
        '''
        
        return self.__surname
    
    @surname.setter
    def surname(self, value):
        u'''Задає прізвище
        
        @param: value(str) - прізвище, мінімум 1 символ, який починається з літери.
        '''
        
        if _re_name.match(value):
            self.__surname = value
        else:
            raise ValueError(u'прізвище повинно починатися з літери')
    
    @property
    def firstname(self):
        u'''Повертає ім'я
        
        @return: (str)
        '''
        
        return self.__firstname
    
    @firstname.setter
    def firstname(self, value):
        u'''Задає ім'я
        
        @param: value(str) - мінімум - 1 символ, яке починається з літери.
        '''
        
        if _re_name.match(value):
            self.__firstname = value
        else:
            raise ValueError(u"ім'я повинно починатися з літери")
    
    @property
    def lastname(self):
        u'''Повертає по-батькові
        
        @return: (str)
        '''
        
        return self.__lastname
    
    @lastname.setter
    def lastname(self, value):
        u'''Задає по-батькові
        
        @param: value(str) - мінімум - 1 символ, яке починається з літери.
        '''
        
        if self._re_lastname.match(value):
            self.__lastname = value
        else:
            raise ValueError(u'по-батькові повинно починатися з літери або бути пустим')

class KvTeacher(KvPerson):
    u'''Викладач
    
    @version: 0.1.0
    '''
    
    def __init__(self, department, rank, post):
        self.__department = department
        self.rank = rank
        self.post = post
    
    
    @property
    def department(self):
        u'''Повертає кафедру
        
        @return: (KvDepartment)
        '''
        
        return self.__department
    
    @department.setter
    def department(self, value):
        u'''Задає кафедру
        
        @param: value(str) - кафедра має бути типу KvDepartment
        '''
        
        assert type(value) is KvDepartment, u'кафедра має бути типу KvDepartment'
        self.__department = value
    
    @property
    def rank(self):
        u'''Повертає звання
        
        @return: (str)
        '''
        
        return self.__rank
    
    @rank.setter
    def rank(self, value):
        if value in _RANKS:
            self.__rank = value
        else:
            raise ValueError(u'звання має бути одним із значень - {}'.format(_RANKS))
    
    @property
    def post(self):
        u'''Повертає посаду
        
        @return: (str)
        '''
        
        return self.__post
    
    @post.setter
    def post(self, value):
        if value in _POSTS:
            self.__post = value
        else:
            raise ValueError(u'посада має бути одним із значень - {}'.format(_POSTS))

class KvStudent(KvPerson):
    u'''Студент
    
    @version: 0.1.0
    '''
    
    _re_pattern_email=u"^[A-Za-z].*@.+\\..+$"
    _re_email = re.compile(_re_pattern_email)
    
    _re_pattern_phone=u"^([0-9]{3}) [0-9]{3}-[0-9]{2}-[0-9]{2}$"   # (XXX) XXX-XX-XX
    _re_phone = re.compile(_re_pattern_phone)
    
    def __init__(self, group, email, phone_1, phone_2=''):
        self.group = group
        self.email = email
        self.phone_1 = phone_1
        self.phone_2 = phone_2
    
    @property
    def id_(self):
        u'''Повертає id викладача
        '''
        
        return self._id_
    
    @property
    def group(self):
        u'''Повертає групу
        
        @return: (KvGroup)
        '''
        
        return self.__group
    
    @group.setter
    def group(self, group):
        if type(group) is KvGroup:
            self.__group = group
        else:
            raise TypeError(u'тип данних має бути KvGroup')
    
    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, text):
        if self._re_pattern_email.match(text):
            self.__email = text
        else:
            raise ValueError(u'email не може бути пустим і повинен містити @ та крапку (.)')
    
    @property
    def phone_1(self):
        u'''Повертає номер телефону в форматі (XXX) XXX-XX-XX
        
        @return: (str)
        '''
        
        return self.__phone_1
    
    @phone_1.setter
    def phone_1(self, value):
        u'''Задає номер телефону в форматі (XXX) XXX-XX-XX
        
        @param: value(str) - номер телефону
        '''
        
        if self._re_pattern_phone.match(value):
            self.__phone_1 = value
        else:
            raise ValueError(u'телефон 1 не може бути пустим і повинен бути в форматі (XXX) XXX-XX-XX')
    
    @property
    def phone_2(self):
        u'''Повертає номер телефону в форматі (XXX) XXX-XX-XX або пустий рядок
        
        @return: (str)
        '''
        
        return self.__phone_2
    
    @phone_2.setter
    def phone_2(self, value):
        u'''Задає номер телефону в форматі (XXX) XXX-XX-XX або пустий рядок
        
        @param: value(str) - номер телефону
        '''
        
        if self._re_pattern_phone.match(value) or not value:
            self.__phone_2 = value
        else:
            raise ValueError(u'телефон 2 може бути пустим і повинен бути в форматі (XXX) XXX-XX-XX')

def __test(n, k=1):
    if n == 1:
        for person in (KvPerson('Cheterbok', 'Anton', 'Orestovuch'),
                       KvPerson(u'Четербок', u'Антон', description=u'Цікаво знати'),
                       KvPerson(u'Четербок', u'Антон', '', description=u'Цікаво знати'),):
            print u'{}, {}, {}, {}'.format(person.surname, person.firstname, 
                                           person.lastname, person.description)

if __name__ == '__main__':
    __test(1)