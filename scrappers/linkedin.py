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
    driver.find_element_by_id("username").send_keys("eboraks@gmail.com")
    driver.find_element_by_id("password").send_keys("Case2214%")
    
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

    #driver.find_element_by_css_selector("div.jobs-box__html-content").text

def find_jobs(driver, job_title, location):

    query = "https://www.linkedin.com/jobs/search?keywords=" + job_title + "&location=" +location+ "%2C%20Massachusetts%2C%20United%20States&geoId=102380872&trk=homepage-jobseeker_jobs-search-bar_search-submit&position=1&pageNum=0"

    driver.get(query)

    jobs = driver.find_elements_by_css_selector("a.job-card-list__title")

    for job in jobs:
        text = job.text
        link = job.get_attribute("href")
        driver.get(link)
        print("job page")



def main():
    path = "/Users/eliranboraks/projects/bin/chromedriver"
    driver = get_driver(path)
    login(driver)
    find_jobs(driver, "product manager", "Boston")

if(__name__ == "__main__"):
    main()



