#!/usr/bin/env 
# coding: utf-8


import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import sys
sys.path.append('dir/')



def get_sheet(url):
    scope = [
        "https://spreadsheets.google.com/feeds", 
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/spreadsheets"
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name('dir/credentials.json', scope)
    client = gspread.authorize(credentials)
    sheet = client.open_by_url(url)  # or client.open_by_key('YOUR_SPREADSHEET_ID')
    return sheet



def validate_worksheet_names(actual_list, given_list):
    actual_wsheets = [worksheet.title for worksheet in actual_list]
    
    # sometimes actual worksheet names contain extra space at the begining or end of the title like ' s1 24', ' IIFGR '
    # but user do not give these spaces in given worksheet names
    # so we should convert given names to actual names
    
    converted_list = [ws for ws in actual_wsheets if ws.strip() in given_list]
    return converted_list



def get_last_class_date(dates):
    # getting last date of class
    for i, date in enumerate(dates):
        if date != '' and 'Khata' not in date:   #  here date is an integer
            last_date_of_class = date
            index = i
    return last_date_of_class, index



def check_mobile_number(mob_num):
    if mob_num == '':          
        return []
    return [mob_num]


def get_st_info(df):
    class_dates = df.loc[2]
    last_class_date, date_index = get_last_class_date(class_dates)
    
    # create list to store student info
    st_info = []
    
    # student data starts from row = 5
    row = 5
    
    while row < df.shape[0]:       
        st_data = df.loc[row]
        
        # checking if student name exists in the cell
        if st_data[1] == '':
            row += 1
            pass

        else:
            # create dictionary for every student 
            dic = {}   

            # name
            dic['Name'] = st_data[1]

            # mobile number
            dic['Mobile No'] = check_mobile_number(st_data[3])
            
            # some students have multiple phone number
            if df.iloc[row+1,1] == '':
                another_moble_no = df.iloc[row+1,3]
                dic['Mobile No'] += check_mobile_number(another_moble_no)
                row += 2           
            else:
                row += 1

            if len(dic['Mobile No']) == 0:
                dic['Mobile No'] = ['not available']

            # last class date
            dic['Last class date'] = last_class_date


            # attendance status
            dic['Status'] = st_data[date_index]

            # print(dic)
            st_info.append(dic)
    
    return st_info

