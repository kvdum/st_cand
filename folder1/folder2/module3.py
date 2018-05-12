# -*- coding: utf-8 -*-
'''
Created on 10 серп. 2017 р.

@author: anton
'''
from . import module2 as m1

var1 = 'Значення із: {}'.format(m1.msg)

from .module2 import msg as m2
var2 = 'Значення із: {}'.format(m2)

from .. import module1 as m3
var3 = 'Значення із: {}'.format(m3.msg)

from ..module1 import msg as m4
var4 = 'Значення із: {}'.format(m4)