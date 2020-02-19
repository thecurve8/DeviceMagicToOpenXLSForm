import xlsxwriter
import json
import os
import re

def recursion(data, identifier, row_survey, row_choices, worksheet_survey, worksheet_choices, y, n):
    data_type = data['type']
    if data_type =='group' :
        id_to_append=data['identifier']
        new_id = identifier+'_'+id_to_append
        worksheet_survey.write(row_survey, 0, 'begin_group')
        worksheet_survey.write(row_survey, 1, new_id)
        worksheet_survey.write(row_survey, 2, data['title'])
        row_survey+=1
        if 'children' in data:
            for child in data['children']:
                row_survey, row_choices = recursion(child, new_id, row_survey, row_choices, worksheet_survey, worksheet_choices, y, n)
        worksheet_survey.write(row_survey, 0, 'end_group')
        worksheet_survey.write(row_survey, 1, new_id)
        row_survey+=1
        
    else:
        row_survey, row_choices= leaf_decode(data, identifier, row_survey, row_choices, worksheet_survey, worksheet_choices, y, n)
    return row_survey, row_choices
    

def leaf_decode(data, identifier, row_survey, row_choices, worksheet_survey, worksheet_choices, y, n):
    id_to_append=data['identifier']
    new_id = identifier+'_'+id_to_append
    if 'type' in data:
        type_read = data['type']
        
        if type_read == 'text':
            type_selected = 'text'
            worksheet_survey.write(row_survey, 0, type_selected)
            worksheet_survey.write(row_survey, 1, new_id)
            worksheet_survey.write(row_survey, 2, data['title'])
            if 'hint' in data:
                worksheet_survey.write(row_survey, 3, data['hint'])
            if 'initialAnswer' in data:
                worksheet_survey.write(row_survey, 3, data['initialAnswer'])
            row_survey+=1
            
            
            
        elif type_read == 'boolean': 
            type_selected = 'select_one'
            worksheet_choices.write(row_choices, 0, new_id)
            worksheet_choices.write(row_choices, 1, 'yes')
            worksheet_choices.write(row_choices, 2, y)
            row_choices+=1
            worksheet_choices.write(row_choices, 0, new_id)
            worksheet_choices.write(row_choices, 1, 'no')
            worksheet_choices.write(row_choices, 2, n)
            row_choices+=1  
            
            type_with_choice_id = type_selected + ' ' + new_id
            worksheet_survey.write(row_survey, 0, type_with_choice_id)
            worksheet_survey.write(row_survey, 1, new_id)
            worksheet_survey.write(row_survey, 2, data['title'])
            if 'hint' in data:
                worksheet_survey.write(row_survey, 3, data['hint'])
            row_survey+=1
#            
        elif type_read == 'select':    
            type_selected = 'select_one'
            if 'multiple' in data and  data['multiple']:
                type_selected = 'select_multiple'
            
            #get choices
            choice_n=0
            for option in data['options']:
                worksheet_choices.write(row_choices, 0, new_id)
                if 'identifier' in option:
                    worksheet_choices.write(row_choices, 1, option['identifier'].replace(" ", "_"))
                else:
                    worksheet_choices.write(row_choices, 1, 'choice_'+str(choice_n).replace(" ", "_"))
                worksheet_choices.write(row_choices, 2, option['text'])
                row_choices+=1
                choice_n+=1
            if choice_n==0:
                worksheet_choices.write(row_choices, 0, new_id)
                worksheet_choices.write(row_choices, 1, 'yes')
                worksheet_choices.write(row_choices, 2, y)
                row_choices+=1
                worksheet_choices.write(row_choices, 0, new_id)
                worksheet_choices.write(row_choices, 1, 'no')
                worksheet_choices.write(row_choices, 2, n)
                row_choices+=1
                worksheet_choices.write(row_choices, 0, new_id)
                worksheet_choices.write(row_choices, 1, 'no_answer')
                worksheet_choices.write(row_choices, 2, 'no answer')
                row_choices+=1
                
                
            type_with_choice_id = type_selected + ' ' + new_id
            worksheet_survey.write(row_survey, 0, type_with_choice_id)
            worksheet_survey.write(row_survey, 1, new_id)
            worksheet_survey.write(row_survey, 2, data['title'])
            if 'hint' in data:
                worksheet_survey.write(row_survey, 3, data['hint'])
            row_survey+=1
            
        elif type_read == 'date':    
            type_selected = 'date'
            worksheet_survey.write(row_survey, 0, type_selected)
            worksheet_survey.write(row_survey, 1, new_id)
            worksheet_survey.write(row_survey, 2, data['title'])
            if 'hint' in data:
                worksheet_survey.write(row_survey, 3, data['hint'])
            if 'initialAnswer' in data:
                worksheet_survey.write(row_survey, 8, data['initialAnswer'])
            row_survey+=1
        
        elif type_read == 'time':    
            type_selected = 'time'
            worksheet_survey.write(row_survey, 0, type_selected)
            worksheet_survey.write(row_survey, 1, new_id)
            worksheet_survey.write(row_survey, 2, data['title'])
            if 'hint' in data:
                worksheet_survey.write(row_survey, 3, data['hint'])
                ##TODO check initialAnswer's format
#            if 'initialAnswer' in data:
#                worksheet_survey.write(row_survey, 8, data['initialAnswer'])
            row_survey+=1
            
        elif type_read == 'datetime':    
            type_selected = 'dateTime'
            worksheet_survey.write(row_survey, 0, type_selected)
            worksheet_survey.write(row_survey, 1, new_id)
            worksheet_survey.write(row_survey, 2, data['title'])
            if 'hint' in data:
                worksheet_survey.write(row_survey, 3, data['hint'])
                ##TODO check initialAnswer's format
#            if 'initialAnswer' in data:
#                worksheet_survey.write(row_survey, 8, data['initialAnswer'])
            row_survey+=1
            
        elif type_read == 'decimal':    
            type_selected = 'decimal'
            worksheet_survey.write(row_survey, 0, type_selected)
            worksheet_survey.write(row_survey, 1, new_id)
            worksheet_survey.write(row_survey, 2, data['title'])
            if 'hint' in data:
                worksheet_survey.write(row_survey, 3, data['hint'])
            if 'initialAnswer' in data:
                worksheet_survey.write(row_survey, 8, data['initialAnswer'])
            row_survey+=1
            
        
        elif type_read == 'integer':    
            type_selected = 'integer'
            type_selected = 'decimal'
            worksheet_survey.write(row_survey, 0, type_selected)
            worksheet_survey.write(row_survey, 1, new_id)
            worksheet_survey.write(row_survey, 2, data['title'])
            if 'hint' in data:
                worksheet_survey.write(row_survey, 3, data['hint'])
            if 'initialAnswer' in data:
                worksheet_survey.write(row_survey, 8, data['initialAnswer'])
            row_survey+=1
        
#        elif type_read == 'location':    
#            type_selected = 'geopoint'
#        
        #emails are treated as text
        elif type_read == 'email':    
            type_selected = 'text'
            worksheet_survey.write(row_survey, 0, type_selected)
            worksheet_survey.write(row_survey, 1, new_id)
            worksheet_survey.write(row_survey, 2, data['title'])
            if 'hint' in data:
                worksheet_survey.write(row_survey, 3, data['hint'])
            if 'initialAnswer' in data:
                worksheet_survey.write(row_survey, 3, data['initialAnswer'])
            row_survey+=1
            
        #phone numbers are treated like text    
        elif type_read == 'phone_number':    
            type_selected = 'text'
            worksheet_survey.write(row_survey, 0, type_selected)
            worksheet_survey.write(row_survey, 1, new_id)
            worksheet_survey.write(row_survey, 2, data['title'])
            if 'hint' in data:
                worksheet_survey.write(row_survey, 3, data['hint'])
            if 'initialAnswer' in data:
                worksheet_survey.write(row_survey, 3, data['initialAnswer'])
            row_survey+=1
            
            
#        elif type_read == 'image':    
#            type_selected = 'image'
#        
#        elif type_read == 'signature':    
#            type_selected = 'text'
#        
        elif type_read == 'barcode':    
            type_selected = 'barcode'
            worksheet_survey.write(row_survey, 0, type_selected)
            worksheet_survey.write(row_survey, 1, new_id)
            worksheet_survey.write(row_survey, 2, data['title'])
            if 'hint' in data:
                worksheet_survey.write(row_survey, 3, data['hint'])
            row_survey+=1
            
#        elif type_read == 'sketch':    
#            type_selected = 'text'
#        
#        elif type_read == 'password':    
#            type_selected = 'text'
#        
#        elif type_read == 'calculated':    
#            type_selected = 'calculate'
#            
#        elif type_read == 'resource':    
#            type_selected = 'file'
        else:
            print(type_read)
        
        
    return row_survey, row_choices

def createLabels(worksheet_survey, worksheet_choices, worksheet_settings, form_name):
    worksheet_settings.write('A1', 'form_title')
    worksheet_settings.write('B1', 'form_id')
    worksheet_settings.write('C1', 'submission_url')
    
    worksheet_settings.write('A2', form_name)
    
    worksheet_choices.write('A1', 'list_name')
    worksheet_choices.write('B1', 'name')
    worksheet_choices.write('C1', 'label')
    
    
    worksheet_survey.write('A1', 'type')
    worksheet_survey.write('B1', 'name')
    worksheet_survey.write('C1', 'label')
    worksheet_survey.write('D1', 'hint')
    worksheet_survey.write('E1', 'relevant')
    worksheet_survey.write('F1', 'Required')
    worksheet_survey.write('G1', 'appearance')
    worksheet_survey.write('H1', 'read_only')
    worksheet_survey.write('I1', 'default')
    worksheet_survey.write('J1', 'notes')
    

def translate(fileName, dest_folder, y, n):
    with open(fileName, encoding="utf-8") as f:
        data = json.load(f)
        form_name = data['title']
        
        basename =os.path.basename(fileName)
        onlyName=os.path.splitext(basename)[0]
        onlyName = re.sub('[^a-zA-Z]+', '_', onlyName)
        workbook = xlsxwriter.Workbook(dest_folder+'/'+onlyName+'.xlsx')
        
        worksheet_survey = workbook.add_worksheet('survey')
        worksheet_choices = workbook.add_worksheet('choices')
        worksheet_settings = workbook.add_worksheet('settings')
        
        createLabels(worksheet_survey, worksheet_choices, worksheet_settings, form_name)
        
        identifier="root"
        
        if 'children' in data:
            row_survey=1
            row_choices=1
            for child in data['children']:
                row_survey, row_choices = recursion(child, identifier, row_survey, row_choices, worksheet_survey, worksheet_choices, y, n)

        workbook.close()
