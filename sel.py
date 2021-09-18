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
    #driver.set_window_size(1920, 1080)
    return (driver)

selenium = get_selenium()                           
selenium.get(url)    

scroll = "document.querySelector(\'#card-scroll-container\').scrollIntoView();"

i = 10

while i > 0 :
    selenium.execute_script(scroll) # execute the js scroll
    time.sleep(2) # wait for page to load new content
    i -= 1

links = selenium.find_elements_by_tag_name("a")
job_links = []  
all_links = []  
for l in links:
    all_links.append(l.get_attribute('href'))

selenium.close()

for l in all_links:
    if "job-openings" in str(l):
        job_links.append(l)

df = pd.DataFrame()
r = 0
for j in job_links:
    response = requests.get(j)
    soup = BeautifulSoup(response.text, "lxml") 
    r += 1
    df.loc[r, 'URL'] = j
    df.loc[r, 'LOCATION'] = soup.find(attrs={"class":re.compile('headerstyle__JobViewHeaderLocation-sc*')}).text	
    df.loc[r, 'POSITION'] = soup.find(attrs={"class":re.compile('headerstyle__JobViewHeaderTitle-sc*')}).text	

    jobDetails = soup.findAll(attrs={"class":re.compile('detailsstyles__DetailsTableRow*')})

    for d in jobDetails:
        isTitle = True
        title = ""
        for dd in d :
            if isTitle:
                title = dd.text
                isTitle = False
            else:
                isTitle = True
                df.loc[r, title] = dd.text
                title = ""

    descriptions = soup.findAll(attrs={"class":re.compile('descriptionstyles__DescriptionBody*')})
    i = 1
    for d in descriptions:
        df.loc[r, 'DESCRIPTION '+ str(i)] = d.text
        i+=1
print(df.columns)
print(df)
#df.to_excel("monster.xlsx") 



