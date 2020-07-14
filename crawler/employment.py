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
from twisted.internet.task import LoopingCall
from scrapy import signals

# Database
MONGODB = pymongo.MongoClient('192.168.1.16', 27017)
DATABASE_IN_MONGODB = MONGODB['recruitment_crawler']

# print(website_list)
website_search="employment"
web_time="crawlTime"
time.sleep(3)

#Load Chrome driver
#working_dir = os.getcwd()
#os.chdir("..")
#first_driver = webdriver.Chrome(os.getcwd() + "/chromedriver")
#second_driver = webdriver.Chrome(os.getcwd() + "/chromedriver")
#os.chdir(working_dir)
now = datetime.now()

current_time = now.strftime("%D:%H:%M:%S")
print("Current Time =", current_time)
curr = dict()
curr["item"] = "Employment"
curr["time"] = current_time

#with open('out.txt', 'w') as output:
#    output.write(curr)

DATABASE_IN_MONGODB[web_time].update_one({'item':curr["item"]},{"$set": curr},upsert=True)

driver_path = "D:/MarketingTool/Recruiment/UICrawl/crawler/chromedriver.exe"
first_driver = webdriver.Chrome(executable_path=driver_path)
second_driver = webdriver.Chrome(executable_path=driver_path)

# Start searching
for page in range(2):
    print()
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(page)
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print()
    first_driver.get("https://employment.en-japan.com/search/search_list/?aroute=12&refine=1&arearoute=1&pagenum="+str(page))
    job_card = first_driver.find_elements_by_css_selector('.toDesc')
    for card in job_card:
        try:
            job_link = card.get_attribute("href")
            second_driver.get(job_link)

            data = dict()
            data["link"] = job_link
            data["title"] = second_driver.find_element_by_css_selector(".nameSet .name").text

            ######### Application Requirements
            application_requirement = dict()
            title_list = second_driver.find_elements_by_css_selector(".descArticleUnit.dataWork .icon.item")
            data_list = second_driver.find_elements_by_css_selector(".descArticleUnit.dataWork .data")
            for i in range(len(title_list)):
                application_requirement[title_list[i].text] = data_list[i].text

            data["application_requirement"] = application_requirement

            ######### Company Profile
            company_profile = dict()
            title_list = second_driver.find_elements_by_css_selector(".descArticleUnit.dataCompanyInfoSummary .item")
            data_list = second_driver.find_elements_by_css_selector(".descArticleUnit.dataCompanyInfoSummary .data")
            for i in range(len(title_list)):
                company_profile[title_list[i].text] = data_list[i].text

            data["company_profile"] = company_profile

            print(data)
            print("==============================")

            DATABASE_IN_MONGODB[website_search].update_one({'link':data["link"]},
                                                        {"$set": data}, upsert=True)
        except Exception as e: print(e)

        time.sleep(1)
