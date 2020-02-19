# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 10:01:29 2020

@author: A086787
"""
"""
Converts only basic questions
Examples of things not supported:
-files
-signatures
-default answers
-logic (hide/show questions)
-calculated answers
-select choices from external source
-location
-image
-password
-sketch
"""
#To create exec file run pyinstaller .\cli.py
from project.gui import main

if __name__ == '__main__':
    main()