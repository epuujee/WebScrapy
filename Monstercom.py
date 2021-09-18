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

      
job_links = []  
all_links = []        

def getLink(url):
    selenium = get_selenium() 
    selenium.get(url)    

    scroll = "document.querySelector(\'#card-scroll-container\').scrollIntoView();"
    selenium.execute_script(scroll)
    time.sleep(3)

    links = selenium.find_elements_by_tag_name("a")
    
    for l in links:
        all_links.append(l.get_attribute('href'))

    selenium.close()

    for l in all_links:
        if "job-openings" in str(l):
            job_links.append(l)

getLink(url)


page = 1

while page < 3:
    getLink(str(url)+"&page="+str(page))
    page += 1

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
    
    print(str(r) + " jobs found.")
print(df.columns)
print(df)



