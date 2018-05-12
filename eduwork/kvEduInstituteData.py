# -*- coding: utf-8 -*-

'''
Created on 6.02.2018.

@author: ichet
'''

import re

_re_title_pattern=u"^[A-Za-zА-яЁёЄ-ЯҐа-їґ].*$"  # Назва складається не менше 1 символа і починається з літери.
_re_title = re.compile(_re_title_pattern)

class KvAssociation(object):
    u'''Об'єднання
    
    @version: 0.1.0
    '''
    
    def __init__(self, id_, title, logotype=None):
        self.id_ = id_
        self.title = title
        self.logotype = logotype
    
    @property
    def id_(self):
        u'''@return: (int)
        '''
        
        return self._id_
    
    @property
    def title(self):
        u'''Повертає повну назву навчального закладу
        
        @return: (str)
        '''
        
        return self.__title
    
    @title.setter
    def title(self, value):
        u'''Задає повну назву навчального закладу
        
        @param: value(str) - назва, яка повинна починатися з літери.
        '''
        
        if _re_title.match(value):
            self.__title = value
        else:
            raise ValueError(u"назва повинна починатися з літери")
    
    @property
    def logotype(self):
        u'''Повертає логотип
        
        @return: (bytes) або None
        '''
        
        return self.__logotype
    
    @logotype.setter
    def logotype(self, image):
        u'''Задає логотип навчального закладу
        
        @param: (bytes, None) - логотип.
        '''
        
        if isinstance(image, bytes) or image is None:
            self.__logotype = image
        else:
            raise ValueError(u'тип логотипу має бути типу bytes')

class Edu:
    def __init__(self, short_title, nolong_title, title, logotype):
        pass
    
    @property
    def short_title(self):
        return self.__short_title
    
    @short_title.setter
    def short_title(self, title):
        self.__short_title = title
    
    @property
    def nolong_title(self):
        return self.__nolong_title
    
    @nolong_title.setter
    def nolong_title(self, title):
        self.__nolong_title = title
    
    @property
    def title(self):
        return self.__title
    
    @title.setter
    def title(self, title):
        self.__title = title
    
    @property
    def logotype(self):
        return self.__logotype
    
    @logotype.setter
    def logotype(self, image):
        self.__logotype = image

class KvEdu(KvAssociation):
    u'''Навчальний заклад
    
    @version: 0.1.0
    '''
    
    pass

class KvInstitute(KvAssociation):
    u'''Інститут
    
    @version: 0.1.0
    '''
    
    def __init__(self, title, edu, logotype=None):
        super(KvInstitute, self).__init__(title, logotype)
        self.edu = edu
    
    @property
    def edu(self):
        u'''Повертає навчальний заклад
        
        @return: (KvEdu)
        '''
        
        return self.__edu
    
    @edu.setter
    def edu(self, value):
        u'''Задає навчальний заклад
        
        @param: value(str) - навчальний заклад має бути типу KvEdu
        '''
        
        assert type(value) is KvEdu, u'навчальний заклад має бути типу KvEdu'
        self.__edu = value

class KvDepartment(KvAssociation):
    u'''Кафедра
    
    @version: 0.1.0
    '''
    
    def __init__(self, title, institute, logotype=None):
        super(KvDepartment, self).__init__(title, logotype)
        self.institute = institute
    
    @property
    def institute(self):
        u'''Повертає інститут
        
        @return: (KvInstitute)
        '''
        
        return self.__institute
    
    @institute.setter
    def institute(self, value):
        u'''Задає інститут
        
        @param: value(str) - інститут має бути типу KvInstitute
        '''
        
        assert type(value) is KvInstitute, u'інститут має бути типу KvInstitute'
        self.__institute = value

class KvGroup(KvAssociation):
    u'''Група
    
    @version: 0.1.0
    '''
    
    def __init__(self, title, department, logotype=None):
        super(KvGroup, self).__init__(title, logotype)
        self.department = department
    
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

def __test(n, k=1):
    if n == 1:
        institute = KvInstitute(u'ІБІД', KvEdu(u'НУ "Львівська політехніка"'))
        print institute.title, institute.edu.title
    elif n == 2:
        group = KvGroup(u'ТГВ-51', KvDepartment(u'Теплогазопостачання і вентиляція',
                                                KvInstitute(u'ІБІД', 
                                                KvEdu(u'НУ "Льівська політехніка"'))))
        print group.title, group.department.title, group.department.institute.title, \
               group.department.institute.edu.title

if __name__ == '__main__':
    __test(2)