#!/usr/bin/env python
# coding: utf-8



import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException
import time





def send_message(mob_num, msg):
    """
    # whatsapp web will require scan option for login
    # for auto login we have to use cookies and data of our chrome browser
    # this can be done using ChromeOptions (it will load data from our previous login to chrome browser)


    # ChromeOptions should be above webdriver.Chrome()
    # Because first the options will load then the browser will open

    """ 
    
    CHROME_PROFILE_PATH = 'user-data-dir=dir/Users/sajib/Library/Application Support/Google/Chrome/Default/'  # for windows OS

    options = webdriver.ChromeOptions()
    
    #options.add_argument('--headless')
    options.add_argument("start-maximized")
    options.add_argument(CHROME_PROFILE_PATH)

    driver = webdriver.Chrome(options=options)   
    phone = '+880' + mob_num[-10:]
    url = 'https://web.whatsapp.com/send?phone=' + phone + '&text=&app_absent=1'        
    driver.get(url)
    
    driver.implicitly_wait(10)
    wait = WebDriverWait(driver, 30)

    search_box_path = '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]'           # search box path to input number
    message_box_path = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'  # message box xpath
    driver.find_element(By.XPATH, message_box_path)
    try:
        driver.find_element(By.XPATH, message_box_path)   # if there is no such element it will raise NoSuchElementException  
        message_box = wait.until(EC.presence_of_element_located((By.XPATH, message_box_path)))           

        # line_break = (Keys.SHIFT)+(Keys.ENTER)+(Keys.SHIFT)
    
        # write message in message box
        message_box.send_keys(msg + Keys.ENTER)
        time.sleep(3)
        
    except NoSuchElementException:       
            # after proceding to this exception, it will try to find Ok button
            # if ok button does not exist, it will raise another NoSuchElementException
            try:
                ok_button_xpath = '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/button'

                # find ok button
                ok_button = driver.find_element(By.XPATH, ok_button_xpath)

                # click the 'Ok' button of popup window
                ok_button.click()
                
            except NoSuchElementException:
                pass

    driver.quit()
    time.sleep(2)
    





