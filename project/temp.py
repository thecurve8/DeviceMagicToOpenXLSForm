import xlsxwriter
import json

def recursion(data, identifier, row_survey, row_choices, worksheet_survey, worksheet_choices):
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
                row_survey, row_choices = recursion(child, new_id, row_survey, row_choices, worksheet_survey, worksheet_choices)
        worksheet_survey.write(row_survey, 0, 'end_group')
        worksheet_survey.write(row_survey, 1, new_id)
        row_survey+=1
        
    else:
        row_survey, row_choices= leaf_decode(data, identifier, row_survey, row_choices, worksheet_survey, worksheet_choices)
    return row_survey, row_choices
    

def leaf_decode(data, identifier, row_survey, row_choices, worksheet_survey, worksheet_choices):
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
            
            
            
#        elif type_read == 'boolean': 
#            ##TODO generate Yes/No
#            type_selected = 'select_one'
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
                worksheet_choices.write(row_choices, 2, 'oui')
                row_choices+=1
                worksheet_choices.write(row_choices, 0, new_id)
                worksheet_choices.write(row_choices, 1, 'no')
                worksheet_choices.write(row_choices, 2, 'non')
                row_choices+=1
                worksheet_choices.write(row_choices, 0, new_id)
                worksheet_choices.write(row_choices, 1, 'no_answer')
                worksheet_choices.write(row_choices, 2, 'ne sais pas / ne souhaite pas répondre')
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
                worksheet_survey.write(row_survey, 3, data['initialAnswer'])
            row_survey+=1
        
#        elif type_read == 'time':    
#            type_selected = 'time'
        
#        elif type_read == 'datetime':    
#            type_selected = 'dateTime'
#        
        elif type_read == 'decimal':    
            type_selected = 'decimal'
            worksheet_survey.write(row_survey, 0, type_selected)
            worksheet_survey.write(row_survey, 1, new_id)
            worksheet_survey.write(row_survey, 2, data['title'])
            if 'hint' in data:
                worksheet_survey.write(row_survey, 3, data['hint'])
            if 'initialAnswer' in data:
                worksheet_survey.write(row_survey, 3, data['initialAnswer'])
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
                worksheet_survey.write(row_survey, 3, data['initialAnswer'])
            row_survey+=1
        
#        elif type_read == 'location':    
#            type_selected = 'geopoint'
#        
#        elif type_read == 'email':    
#            type_selected = 'text'
#        
#        elif type_read == 'phone_number':    
#            type_selected = 'text'
#        
#        elif type_read == 'image':    
#            type_selected = 'image'
#        
#        elif type_read == 'signature':    
#            type_selected = 'text'
#        
#        elif type_read == 'barcode':    
#            type_selected = 'barcode'
#        
#        elif type_read == 'sketch':    
#            type_selected = 'text'
#        
#        elif type_read == 'password':    
#            type_selected = 'barcode'
#        
        elif type_read == 'calculated':    
            type_selected = 'calculate'
            
        elif type_read == 'resource':    
            type_selected = 'file'
        
        
    return row_survey, row_choices

def translate(fileName):
    with open(fileName) as f:
        data = json.load(f)
        form_name = data['title']
        
        workbook = xlsxwriter.Workbook('hello.xlsx')
        worksheet_survey = workbook.add_worksheet('survey')
        worksheet_choices = workbook.add_worksheet('choices')
        worksheet_settings = workbook.add_worksheet('settings')
        
        
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
        
        identifier="root"
        
        if 'children' in data:
            row_survey=1
            row_choices=1
            for child in data['children']:
                row_survey, row_choices = recursion(child, identifier, row_survey, row_choices, worksheet_survey, worksheet_choices)
        
        
        workbook.close()
