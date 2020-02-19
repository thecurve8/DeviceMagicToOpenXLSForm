# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 13:41:52 2020

@author: A086787
"""

from selenium import webdriver

driver = webdriver.Firefox() # Initialize the webdriver session
driver.get('http://www.nationalrail.co.uk/') # replaces "ie.navigate"
driver.find_element_by_id('sltArr').find_elements_by_tag_name('option')[1].click()