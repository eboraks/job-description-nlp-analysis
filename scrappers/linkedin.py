from typing import Counter
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd


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
    driver.find_element_by_id("username").send_keys("")
    driver.find_element_by_id("password").send_keys("")
    
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


def get_job_description(driver, link):

    driver.get(link)
    time.sleep(10)
    return driver.find_element_by_css_selector("div.jobs-box__html-content").text

def find_jobs(driver, job_title, location):

    query = "https://www.linkedin.com/jobs/search?keywords=" + job_title + "&location=" +location+ "%2C%20Massachusetts%2C%20United%20States&geoId=102380872&trk=homepage-jobseeker_jobs-search-bar_search-submit&position=1&pageNum=0"

    driver.get(query)

    time.sleep(20)
    jobs = driver.find_elements_by_css_selector("a.job-card-list__title")

    print("number of jobs found " + str(len(jobs)))    
    results = []
    counter = 0
    for job in jobs:
        counter += 1 
        time.sleep(2)
        subject = job.text
        link = job.get_attribute("href")
        results.append(
            {"subject": subject, 
            "url": link}
        )
        if(counter > 10):
            break
    
    for job in results:
        job_desc = get_job_description(driver, job["url"])
        job["job_desc"] = job_desc
    
    
    
    return results



def main():
    path = "/Users/eliranboraks/projects/bin/chromedriver"
    driver = get_driver(path)
    login(driver)
    jobs = find_jobs(driver, "product manager", "Boston")

    df = pd.DataFrame(jobs).reset_index()
    df.to_csv('data/linkedin_jobs.csv', index=False)

if(__name__ == "__main__"):
    main()



