from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import configparser
from time import sleep
import pandas as pd
import matplotlib.pyplot as plt

missing = {}

def AddNewSkills(listOfSkills):
    for l in listOfSkills:
        missing.update({l : missing.get(l, 0)+1})

def clean(search):
    try:
        skills = search.text.replace("and ", "")
        skills = skills.split(", ")
        AddNewSkills(skills)
    except Exception:
        print("There was an error")

#%% Config
config = configparser.RawConfigParser()
config.read("config.ini")

#%% Driver

driver = wd.Firefox()
driver.get("https://www.linkedin.com/jobs/")
search = driver.find_element(By.LINK_TEXT, "Go to your feed")
search.send_keys(Keys.RETURN)
driver.maximize_window()

sleep(1)

search = driver.find_element(By.LINK_TEXT, "Sign in")
search.send_keys(Keys.RETURN)

sleep(1)
search = driver.find_element(By.ID, "username")
search.send_keys(config["Linkedin details"]["Name"])
search = driver.find_element(By.ID, "password")
search.send_keys(config["Linkedin details"]["Pass"])
search.send_keys(Keys.RETURN)

sleep(2)

driver.get("https://www.linkedin.com/jobs/")


sleep(3)

try:
    search = driver.find_element(By.ID, "recentSearchesIndex__0")
    search.click()
    print("No captcha")
except Exception:
    input("Waiting for clearance")
    driver.get("https://www.linkedin.com/jobs/")
    sleep(3)
    search = driver.find_element(By.ID, "recentSearchesIndex__0")
    search.click()

sleep(2)

page = 1

while True:
    page+=1
    scrollbar = driver.find_elements(By.XPATH, "//ul[@class='scaffold-layout__list-container']/li[starts-with(@id, 'ember')]")
    ammount = len(scrollbar)
    print(f"There are {ammount} of jobs displayed")
    for s in range(ammount):
        scrollbar[s].click()
        
        sleep(0.5)
        
        try:
            driver.find_element(By.XPATH, "//a[@class='app-aware-link ' and @href='#HYM']").click()
            sleep(0.2)
            search = driver.find_elements(By.XPATH, "//div[@class='pt5']/div[@class='job-details-how-you-match__skills-item-wrapper display-flex flex-row pt4'][1]/div[@class='display-flex flex-column overflow-hidden']/a[starts-with(@class, 'app-aware')]")
            clean(search[1])
        except IndexError:
            if (len(search) > 0):
                clean(search[0])
                continue
            print(f"Job has no skills displayed {s}")
            print(search)
        except Exception:
            continue
        
        sleep(0.1)
    
    try:
        driver.find_element(By.XPATH, f"//ul[@class='artdeco-pagination__pages artdeco-pagination__pages--number']/li[@data-test-pagination-page-btn='{page}']").click()
    except Exception:
        driver.find_element(By.XPATH, "//button[@aria-label='Page 9']").click()
    
    sleep(1)

#%%
print(sorted(missing.items(), key=lambda item: item[1]))
