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

website_search="tenshoku"
web_time="crawlTime"
time.sleep(3)

# Load Chrome driver
now = datetime.now()

current_time = now.strftime("%D:%H:%M:%S")
print("Current Time =", current_time)
curr = dict()
curr["item"] = "Tenshoku"
curr["time"] = current_time

#with open('out.txt', 'w') as output:
#    output.write(curr)

DATABASE_IN_MONGODB[web_time].update_one({'item':curr["item"]},{"$set": curr},upsert=True)

driver_path = "D:/MarketingTool/Recruiment/UICrawl/crawler/chromedriver.exe"
first_driver = webdriver.Chrome(executable_path=driver_path)
second_driver = webdriver.Chrome(executable_path=driver_path)

# Start searching
for page in range(163, 185):
    print()
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print(page)
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    print()
    first_driver.get("https://tenshoku.mynavi.jp/search/list/?pageNum="+str(page))
    job_card = first_driver.find_elements_by_css_selector('.linkArrowS')
    for card in job_card:
        try:
            job_link = card.get_attribute("href").split("?")[0].replace("msg/","").replace("adv1/","")
            second_driver.get(job_link)

            data = dict()
            data["link"] = job_link
            data["title"] = second_driver.find_element_by_css_selector(".blockWrapper .occName").text

            ######### Job Description
            data["job_description"] = second_driver.find_element_by_css_selector(".jobPointArea__wrap-jobDescription").text

            ######### Target Person
            data["target_person"] = second_driver.find_element_by_css_selector(".leftBlock.clearfix>.jobPointArea__head").text \
                            +"\n"+  second_driver.find_element_by_css_selector(".leftBlock.clearfix>.jobPointArea__body--large").text

            ######### Application Requirements
            application_requirement = dict()
            title_list = second_driver.find_elements_by_xpath("/html/body/div[1]/div[5]/div[4]/div/div[2]/div[1]/table[1]/tbody/tr")
            for i in range(1,len(title_list)+1):
                title = second_driver.find_element_by_xpath("/html/body/div[1]/div[5]/div[4]/div/div[2]/div[1]/table[1]/tbody/tr["+str(i)+"]/th").text
                body = second_driver.find_element_by_xpath("/html/body/div[1]/div[5]/div[4]/div/div[2]/div[1]/table[1]/tbody/tr["+str(i)+"]/td").text
                application_requirement[title] = body
            data["application_requirement"] = application_requirement
            
            ######### Company Profile
            company_profile = dict()
            title_list = second_driver.find_elements_by_css_selector(".jobOfferTable.thL .jobOfferTable__head")
            data_list = second_driver.find_elements_by_css_selector(".jobOfferTable.thL .jobOfferTable__body")
            for i in range(len(title_list)):
                company_profile[title_list[i].text] = data_list[i].text
            data["company_profile"] = company_profile

            ######### Application Method
            application_method = dict()
            title_list = second_driver.find_elements_by_css_selector(".jobOfferTable.jobOfferTable-howToApply.thXL .jobOfferTable__head")
            data_list = second_driver.find_elements_by_css_selector(".jobOfferTable.jobOfferTable-howToApply.thXL .jobOfferTable__body")
            for i in range(len(title_list)):
                application_method[title_list[i].text] = data_list[i].text
            data["application_method"] = application_method

            DATABASE_IN_MONGODB[website_search].update_one({'link':data["link"]},
                                                        {"$set": data}, upsert=True)

            print(data)
            print("==============================")
        
        except Exception as e: print(e)

        time.sleep(1)