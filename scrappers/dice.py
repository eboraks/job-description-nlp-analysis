from typing import Counter
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from decouple import config
import time
import pandas as pd
from datetime import datetime
import re


def get_driver(path):

     #Initializing the webdriver
    options = webdriver.ChromeOptions()

    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')

    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)

    return driver

def login(driver):

    query = "https://www.linkedin.com/login"

    driver.get(query)
    driver.find_element_by_id("username").send_keys(config('USER'))
    driver.find_element_by_id("password").send_keys(config('PWD'))
    
    print("Sleeping for 10 sec")
    time.sleep(10)
    print("Clicking on the button")
    driver.find_element_by_xpath("//button[text()='Sign in']").click()
    time.sleep(10)
    
    try:
        driver.find_element_by_css_selector("div.feed-identity-module__actor-meta")
        login_status = True
    except NoSuchElementException:
        login_status = False
    
    return login_status

def find_elements(driver, number_of_elements = 15, elements = None) -> set():

    if(elements == None):
        elements = set(driver.find_elements_by_css_selector("a.job-card-list__title"))

    for element in elements:
        driver.execute_script("arguments[0].scrollIntoView();", element)
        
    elements.update(driver.find_elements_by_css_selector("a.job-card-list__title"))
    if(len(elements) < number_of_elements):
        find_elements(driver, number_of_elements, elements)
    
    return elements





def get_job_description(driver, link):

    driver.get(link)
    time.sleep(2)

    try:
        # jobs-description-content__text
        text = driver.find_element_by_id("jobdescSec").text
    
    except NoSuchElementException:  
        text = "Error extracting job description"  
        print("Error extracting job description")
    

    # clean empty spaces a little
    text = re.sub("\n{2,}", "\n", text)

    return text

def find_jobs(driver, job_page_link) -> list:

    driver.get(job_page_link)
    time.sleep(2)
    jobs_list = driver.find_elements_by_xpath("//ul[@class='list-inline'][contains(@style,'margin-bottom')]")
    
    
    
    print("number of jobs found " + str(len(jobs_list)))    
    results = []
    counter = 0
    for job in jobs_list:
        a_tag = job.find_element_by_tag_name("a")
        counter += 1 
        time.sleep(1)
        try:
            subject = a_tag.text
            link = a_tag.get_attribute("href")
            results.append(
                {"subject": subject, 
                "url": link}
            )
        except NoSuchElementException:
            print("Error extracting job text and link")
        
    
    for job in results:
        job_desc = get_job_description(driver, job["url"])
        job["job_desc"] = job_desc
    
    
    
    return results



def main():
    path = "/Users/eliranboraks/projects/bin/chromedriver"
    driver = get_driver(path)
    
    jobs_title = [
        {"name": "dice_product_management", "link": "https://www.dice.com/jobs/q-Product+management-jobs?p={}"},
        {"name": "dice_data_scientist", "link": "https://www.dice.com/jobs/q-Data+Scientist-jobs?p={}"},
        {"name": "dice_solution_architect", "link": "https://www.dice.com/jobs/q-Solution+Architect-jobs?p={}"},
        {"name": "dice_project_management", "link": "https://www.dice.com/jobs/q-Project+management-jobs?p={}"},
        {"name": "dice_engineering_management", "link": "https://www.dice.com/jobs/q-Engineering+management-jobs?p={}"},
        {"name": "dice_business_process_management", "link": "https://www.dice.com/jobs/q-Business+process+management-jobs?p={}"},
        {"name": "dice_business_development", "link": "https://www.dice.com/jobs/q-Business+development-jobs?p={}"}

    ]

    for item in jobs_title:
        
        search_name = item["name"]
        jobs_page = item["link"]
        
        now = datetime.now().isoformat()
        now = re.sub("\.\d{6}", "", now)

        jobs = []
        for pnum in range(1,4):
            page = jobs_page.format(pnum)
            jobs.extend(find_jobs(driver, page))
        
        df = pd.DataFrame(jobs).reset_index()

        file = "data/" + search_name + "_" + now + ".csv"

        df.to_csv(file, index=False)

if(__name__ == "__main__"):
    main()



