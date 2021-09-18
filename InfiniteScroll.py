from selenium import webdriver
from selenium.webdriver.common.keys import Keys                       
import time
import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
import re

url = 'https://www.monster.com/jobs/search?q=Data+Scientist&where=NewYork'
chrome_driver_path = 'C:\\Users\\Puujee\\Documents\\chromedriver\\chromedriver.exe'

def get_selenium():                           
    options = webdriver.ChromeOptions()
    #options.add_argument('--ignore-certificate-errors')
    #options.add_argument('--incognito')
    #options.add_argument('headless')                        
    driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=options)
    driver.set_window_size(490, 1080)
    return (driver)

selenium = get_selenium()                           
selenium.get(url)   
 
i = 1
while i > 0:
    print(i)
    
    time.sleep(1) 
    selenium.execute_script("window.scrollBy(0, 200);")
    try:
        load_more = selenium.find_elements_by_class_name(re.compile('job-search-resultsstyle__LoadMoreContainer-sc*')) 
        print(load_more)
    except:
        i+=1
    


links = selenium.find_elements_by_tag_name("a")
job_links = []  
all_links = []  
for l in links:
    all_links.append(l.get_attribute('href'))

selenium.close()




