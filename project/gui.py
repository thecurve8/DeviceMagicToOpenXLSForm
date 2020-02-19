# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 18:26:59 2020

@author: A086787
"""
import PySimpleGUI as sg
from project.translation import translate

def main():

    sg.theme('Dark Blue 3')  # please make your windows colorful
    
    layout = [[sg.Text('Select the json file downloaded from DeviceMagic and the destination folder for the xlsx file')],
                [sg.Text('JSON file', size=(15, 1)), sg.InputText(), sg.FileBrowse()],
                [sg.Text('Destination folder', size=(15,1)), sg.InputText(), sg.FolderBrowse()],
                [sg.Text('Select language of the survey'), sg.Combo(['english', 'français'])], #used to know how to write yes/no in boolean questions
                [sg.Text('You can go to:')],
                [sg.Text('https://opendatakit.org/xlsform/')],
                [sg.Text('to create a pdf from the xlsx file (select the xlsx file, submit and then preview in Enkento) ')],
                [sg.Submit(), sg.Cancel()]]
    
    
    window = sg.Window('DeviceMagic JSON to XMLForm', layout)
    event, values = window.read()
    window.close()
    file_path, folder_path, language = values[0], values[1], values[2]       # get the data from the values dictionary
    y='yes'
    n='no'
    if(language=='français'):
        y='oui'
        n='non'
    translate(file_path, folder_path,y,n)

if __name__ == "__main__":
    main()