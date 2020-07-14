from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
import time
import re
import pymongo
from datetime import datetime

# Database
MONGODB = pymongo.MongoClient('192.168.1.16', 27017)
DATABASE_IN_MONGODB = MONGODB['recruitment_crawler']

# print(website_list)
web_time="crawlTime"
website_search="greenjapan"
time.sleep(3)

#Load Chrome driver
now = datetime.now()

current_time = now.strftime("%D:%H:%M:%S")
print("Current Time =", current_time)
curr = dict()
curr["item"] = "Greenjapan"
curr["time"] = current_time

#with open('out.txt', 'w') as output:
#    output.write(curr)

DATABASE_IN_MONGODB[web_time].update_one({'item':curr["item"]},{"$set": curr},upsert=True)

driver_path = "D:/MarketingTool/Recruiment/UICrawl/crawler/chromedriver.exe"
first_driver = webdriver.Chrome(executable_path=driver_path)
second_driver = webdriver.Chrome(executable_path=driver_path)

# Start searching
for page in range(290):
    print()
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(page)
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print()
    first_driver.get('https://www.green-japan.com/search_key/01?key=2vkn2gx21xjyx34dfj15&keyword=&page='+str(page))
    job_card = first_driver.find_elements_by_css_selector('.js-search-result-box.card-info')
    for card in job_card:
        try:
            job_link = card.get_attribute("href")
            second_driver.get(job_link)

            data = dict()
            data["link"] = job_link
            data["title"] = second_driver.find_element_by_css_selector('.job-offer-heading>h2').text
            data["bussiness_content"] = second_driver.find_element_by_css_selector('.com_content__basic-info p:nth-child(3)').text
            data["job_description"] = second_driver.find_element_by_css_selector('.com_content__basic-info>p:nth-child(5)').text

            ######### Company Profile
            company_profile = dict()
            company_profile_dom = ".detail-content-table.js-impression:nth-child(3)"
            for i in range(1, len(second_driver.find_elements_by_css_selector(company_profile_dom + ' tr'))+1):
                key = second_driver.find_element_by_css_selector(company_profile_dom + ' tr:nth-child('+str(i)+') th').text.lower().replace(" ","_")
                content = second_driver.find_element_by_css_selector(company_profile_dom + ' tr:nth-child('+str(i)+') td').text.lower().replace(" ","_")
                company_profile[key] = content
            data["company_profile"] = company_profile

            employment_regulations = dict()
            employment_regulations_dom = ".detail-content-table.js-impression:nth-child(7)"
            for i in range(1, len(second_driver.find_elements_by_css_selector(employment_regulations_dom + ' tr'))+1):
                key = second_driver.find_element_by_css_selector(employment_regulations_dom + ' tr:nth-child('+str(i)+') th').text.lower().replace(" ","_")
                content = second_driver.find_element_by_css_selector(employment_regulations_dom + ' tr:nth-child('+str(i)+') td').text.lower().replace(" ","_")
                employment_regulations[key] = content
            data["employment_regulations"] = employment_regulations


            DATABASE_IN_MONGODB[website_search].update_one({'link':data["link"]},
                                                        {"$set": data}, upsert=True)
            print(data)
            print("===========================================================================================================")
        except Exception as e: print(e)

        time.sleep(1)
