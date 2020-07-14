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
website_search="nextrikunabi"
web_time="crawlTime"
time.sleep(3)

#Load Chrome driver
now = datetime.now()

current_time = now.strftime("%D:%H:%M:%S")
print("Current Time =", current_time)
curr = dict()
curr["item"] = "Nextrikunabi"
curr["time"] = current_time

#with open('out.txt', 'w') as output:
#    output.write(curr)

DATABASE_IN_MONGODB[web_time].update_one({'item':curr["item"]},{"$set": curr},upsert=True)

driver_path = "D:/MarketingTool/Recruiment/UICrawl/crawler/chromedriver.exe"
first_driver = webdriver.Chrome(executable_path=driver_path)
second_driver = webdriver.Chrome(executable_path=driver_path)

# Start searching
for page in range(1, 40800, 50):
    print()
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(page)
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print()
    first_driver.get("https://next.rikunabi.com/lst/crn"+str(page)+".html")
    job_card = first_driver.find_elements_by_css_selector('.rnn-button.rnn-button--primary.js-abScreen__more')
    for card in job_card:
        try:
            job_link = card.get_attribute("href")
            second_driver.get(job_link)
            job_tab_link =  second_driver.find_element_by_css_selector(".rn3-companyOfferTabMenu__navItemLink.js-tabRecruitment").get_attribute("href")
            second_driver.get(job_tab_link)
            
            data = dict()
            data["link"] = job_tab_link
            data["title"] = second_driver.find_element_by_css_selector(".rn3-companyOfferHeader__heading").text

            ########### Application Requirement
            application_requirement = dict()
            application_requirement["header"] = second_driver.find_element_by_css_selector(".rn3-companyOfferRecruitment__headText").text

            heading_list = second_driver.find_elements_by_css_selector(".rn3-companyOfferRecruitment__heading")
            text_list = second_driver.find_elements_by_css_selector(".rn3-companyOfferRecruitment__text")

            for i in range(len(heading_list)):
                application_requirement[heading_list[i].text] = text_list[i].text

            data["application_requirement"] = application_requirement

            ########### Company Profile
            company_profile = dict()
            heading_list = second_driver.find_elements_by_css_selector(".rn3-companyOfferCompany__heading")
            text_list = second_driver.find_elements_by_css_selector(".rn3-companyOfferCompany__text")

            for i in range(len(heading_list)):
                company_profile[heading_list[i].text] = text_list[i].text

            data["company_profile"] = company_profile

            ########### About Application
            about_application = dict()
            heading_list = second_driver.find_elements_by_css_selector(".rn3-companyOfferEntry__heading")
            text_list = second_driver.find_elements_by_css_selector(".rn3-companyOfferEntry__text")

            for i in range(len(heading_list)):
                about_application[heading_list[i].text] = text_list[i].text

            data["about_application"] = about_application

            DATABASE_IN_MONGODB[website_search].update_one({'link':data["link"]},
                                                        {"$set": data}, upsert=True)

            print(data)
            print("===========================================================================================================")
        except Exception as e: print(e)

        time.sleep(1)
