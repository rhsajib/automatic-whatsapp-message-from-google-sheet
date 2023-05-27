    
#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os
import sys
# sys.path.append('dir/')
# import whatsapp
from functions import get_sheet, validate_worksheet_names, get_last_class_date, check_mobile_number, get_st_info



import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
import time




def text_formated(msgtext, br, name):
    
    # <name> will be replaced by original name
    msgtext = msgtext.replace('<name>', name)
    
    # creating a string variable for modified message
    m =''
    for i in msgtext.split('\n'):
        m = m + i + br
    return m
    



def send_message(st_info_list, msg, sm_driver):      
    """
    st_info_list : list of dictionaries    
    For istance,     
    [{'Name': 'Adiba', 'Mobile No': ['0167XXXXXXX', '0167XXXXXXX'], 'Last class date': '19', 'Status': 'TRUE'}, 
    {'Name': 'Israt Jahan Lamia', 'Mobile No': ['0167XXXXXXX', '0167XXXXXXX'], 'Last class date': '19', 'Status': 'FALSE'}]      
    
    """
        
    for st_info in st_info_list:
        if st_info['Status'] == 'FALSE':
            for phone_number in st_info['Mobile No']:
                new_tab(st_info['Name'], phone_number, msg, sm_driver)
                
                time.sleep(1)
                
                # Switch back to the main window
                # sm_driver.switch_to.window(main_window)  
                sm_driver.switch_to.window(sm_driver.window_handles[0])
    
    # as i will quit the driver at the end of my program, i need to return driver
    return sm_driver    




def new_tab(st_name, mob_num, messg, nt_driver):
    phone = '+880' + mob_num[-10:]   
    
    link = 'https://web.whatsapp.com/send?phone=' + phone + '&text=&app_absent=1'
        
    # open a new tab in blank
    nt_driver.execute_script("window.open(''),'_blannk'")
    
    # switch to the new window
    nt_driver.switch_to.window(nt_driver.window_handles[1])
    
    # change the url in the .get
    nt_driver.get(link)    
    
    nt_driver.implicitly_wait(20)
    wait = WebDriverWait(nt_driver, 60)
    
    search_box_path = '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]'           # search box path to input number
    message_box_path = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'  # message box xpath    
   
    try:
        nt_driver.find_element(By.XPATH, message_box_path)    # if there is no such element it will raise NoSuchElementException  
        message_box = wait.until(EC.presence_of_element_located((By.XPATH, message_box_path)))           

        line_break = (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT)
        
        # format message to insert student name and line breaks
        modified_msg = text_formated(messg, line_break, st_name)
    
        # write message in message box
        message_box.send_keys(modified_msg + Keys.ENTER)
        time.sleep(3)
        
    except NoSuchElementException:       
            # after proceding to this exception, it will try to find Ok button
            # if ok button does not exist, it will raise another NoSuchElementException
            try:
                ok_button_xpath = '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/button'

                # find ok button
                ok_button = nt_driver.find_element(By.XPATH, ok_button_xpath)

                # click the 'Ok' button of popup window
                ok_button.click()
                
            except NoSuchElementException:
                pass   
      
    # Close the new tab
    nt_driver.close()




def main():
    
    # get google sheet url from user
    url = input('Enter google sheet URL: ')
    
    try:
        # get all data from google sheet url
        full_sheet = get_sheet(url)

        # get name of all worksheets of the spread sheet
        actual_worksheet_names = full_sheet.worksheets()

        # read worksheet_names.txt file for given worksheet names
        with open('worksheet_names.txt', 'r') as f:               
            wsl = f.read().split(',')                                # worksheet_names.txt has coma separated worksheet names
            given_worksheet_names = [i.strip() for i in wsl]         # removed extra spaces from worksheet names

        # validate given worksheet names
        validated_ws_names = validate_worksheet_names(actual_worksheet_names, given_worksheet_names)

        if len(validated_ws_names) == 0:
            print('Please enter valid worksheet names inside the worksheet_names.txt file !!!')

        else:
            # opening chrome driver main window
            """
            # whatsapp web will require scan option for login
            # for auto login we have to use cookies and data of our chrome browser
            # this can be done using ChromeOptions (it will load data from our previous login to chrome browser)


            # ChromeOptions should be above webdriver.Chrome()
            # because first the options will load then the browser will open

            """ 

            # Set up path for whatsapp data

            ### for windows OS
            # CHROME_PROFILE_PATH = 'user-data-dir=C:/Users/<PC_name>/AppData/Local/Google/Chrome/User Data/Default/'

            ### for mac OS
            CHROME_PROFILE_PATH = 'user-data-dir=Users/sajib/Library/Application Support/Google/Chrome/Default/'  

            # Set up the Chrome options
            options = webdriver.ChromeOptions()
            options.add_argument("start-maximized")
            options.add_argument(CHROME_PROFILE_PATH)

            # Set up the Chrome driver
            driver = webdriver.Chrome(options=options)       

            # Open the webpage in chrome driver
            driver.get('https://www.google.com/')

            driver.implicitly_wait(10)
            wait = WebDriverWait(driver, 30)

            # selecting the current window as main window
            main_window = driver.current_window_handle

            # performing task for every worksheet
            for ws_name in validated_ws_names:
          
                # if I want to access the first worksheet (index 0)
                # worksheet = sheet.get_worksheet(0)
                worksheet = full_sheet.worksheet(ws_name)
                data = worksheet.get_all_values()
                df = pd.DataFrame(data)

                # list of student information
                student_info = get_st_info(df)

                if len(student_info) != 0:  
                    # read message from text file
                    with open('message.txt', 'r') as f:
                        message_body = f.read()

                    # sending message using send_message function
                    # and returning the chrome driver to quit it at the end of program       
                    c_driver = send_message(student_info, message_body, driver)

            # quit chrome driver   
            c_driver.quit()

    except:
        print('Your google sheet URL is not correct !!!')

