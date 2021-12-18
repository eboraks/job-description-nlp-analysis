from typing import Counter
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from decouple import config
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
    time.sleep(5)

    try:
        # jobs-description-content__text
        text = driver.find_element_by_css_selector("div.jobs-box__html-content").text

        # in case text is too small, try to get text from span
        if(len(text) < 1500):
            text = ''
            job_description = driver.find_element_by_css_selector("div.jobs-box__html-content")
            for span in job_description.find_elements_by_css_selector('span'):
                text += span.text

                # this this code with https://www.linkedin.com/jobs/view/2837437087/?eBP=CwEAAAF9uVaVA9n0rdmTKX5qdRh-PXU5Arg5SRqMq0GpqXFPNCuQVlBc-XEmbrtKYKzfCio9OBOfDXdFY4ZesVBiMswzCrUG5cEypAPmefGMhc5yhZOiz7xK-eMChTBRRWiNE0MD0yk4APpBwum-PfTSaa59n5nmsBYzN1HorjV2VJoaluuXBJjapaza_loFdgPLfmn2GY-wSpnC0n-sD2kncRe7LgGYCTpUm3iN8gF_Yr3pnVMceO7DfHCsRXfGeTYhEQZb7U1WOyMDNTec8U3VfFVF0VHisFlCPTSc6IgR1czsyloeMELhICiGL5geYggdWnkAydYTVSqcn0RWuu1K5Dn3HUD124qCtks_daW5SWll4vEUQy4k3xZcPw&recommendedFlavor=ACTIVELY_HIRING_COMPANY&refId=PmFecZPc882H7DbWcXCtYw%3D%3D&trackingId=zHvEu%2BgyIqQW3dN%2FkLnJGw%3D%3D&trk=flagship3_search_srp_jobs
                if(len(text) < 1000):
                    text = ''
                    elements = span.find_elements_by_tag_name("*")
                    for element in elements:
                        if(len(element.text) > 10):
                            text += element.text
                    

    
    except NoSuchElementException:  
        text = 'emptry'  
        print("Error extracting job description")
    
    return text

def find_jobs(driver, job_title, location):

    query = "https://www.linkedin.com/jobs/search?keywords=" + job_title + "&location=" +location+ "%2C%20Massachusetts%2C%20United%20States&geoId=102380872&trk=homepage-jobseeker_jobs-search-bar_search-submit&position=1&pageNum=0"

    driver.get(query)
    
    time.sleep(2)
    jobs = find_elements(driver, number_of_elements=25)
    
    print("number of jobs found " + str(len(jobs)))    
    results = []
    counter = 0
    for job in jobs:
        counter += 1 
        time.sleep(2)
        try:
            subject = job.text
            link = job.get_attribute("href")
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
    login(driver)
    
    # Debug a specific job
    #link = "https://www.linkedin.com/jobs/view/2837437087/?eBP=CwEAAAF9uVaVA9n0rdmTKX5qdRh-PXU5Arg5SRqMq0GpqXFPNCuQVlBc-XEmbrtKYKzfCio9OBOfDXdFY4ZesVBiMswzCrUG5cEypAPmefGMhc5yhZOiz7xK-eMChTBRRWiNE0MD0yk4APpBwum-PfTSaa59n5nmsBYzN1HorjV2VJoaluuXBJjapaza_loFdgPLfmn2GY-wSpnC0n-sD2kncRe7LgGYCTpUm3iN8gF_Yr3pnVMceO7DfHCsRXfGeTYhEQZb7U1WOyMDNTec8U3VfFVF0VHisFlCPTSc6IgR1czsyloeMELhICiGL5geYggdWnkAydYTVSqcn0RWuu1K5Dn3HUD124qCtks_daW5SWll4vEUQy4k3xZcPw&recommendedFlavor=ACTIVELY_HIRING_COMPANY&refId=PmFecZPc882H7DbWcXCtYw%3D%3D&trackingId=zHvEu%2BgyIqQW3dN%2FkLnJGw%3D%3D&trk=flagship3_search_srp_jobs"
    #text = get_job_description(driver, link)
    #print(text)
    
    jobs = find_jobs(driver, "data engineer", "Boston")

    df = pd.DataFrame(jobs).reset_index()
    df.to_csv('data/linkedin_jobs.csv', index=False)

if(__name__ == "__main__"):
    main()



