# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 14:14:34 2020

@author: A086787
"""
import re
s = "aésjklsdf21"
s = re.sub('[^a-zA-Z]+', '_', s)
print(s)