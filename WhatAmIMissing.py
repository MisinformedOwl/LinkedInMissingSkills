from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import configparser
from time import sleep
from keyboard import is_pressed as pressed

missing = {}

def AddNewSkills(listOfSkills):
    for l in listOfSkills:
        missing.update({l : missing.get(l, 0)+1})

def Login():
    sleep(1)
    search = driver.find_element(By.ID, "username")
    search.send_keys(config["Linkedin details"]["Name"])
    search = driver.find_element(By.ID, "password")
    search.send_keys(config["Linkedin details"]["Pass"])
    search.send_keys(Keys.RETURN)
    sleep(3)
    
    try:
        search = driver.find_element(By.XPATH, "//a[starts-with(@id, 'ember')]")
        print("No captcha")
    except Exception:
        input("Waiting for clearance")
    
    return driver

def clean(search):
    skills = search.text[search.text.rfind("\n")+2:]
    skills = skills.replace("and ", "")
    skills = skills.split(", ")
    AddNewSkills(skills)

#%% Config
config = configparser.RawConfigParser()
config.read("config.ini")

#%% Driver

driver = wd.Firefox()
driver.get("https://www.linkedin.com/login")

driver = Login()

driver.maximize_window()

sleep(2)

driver.get("https://www.linkedin.com/jobs/collections/recommended/")

sleep(3)

page = 1

while True:
    page+=1
    scrollbar = driver.find_elements(By.XPATH, "//ul[@class='scaffold-layout__list-container']/li[starts-with(@id, 'ember')]")
    ammount = len(scrollbar)
    print(f"There are {ammount} of jobs displayed")
    for s in range(ammount):
        scrollbar[s].click()
        
        sleep(1.4)
        
        try:
            search = driver.find_element(By.XPATH, "//a[@class='app-aware-link ' and @href='#HYM']")
            search.click()
            sleep(1)
            search = driver.find_element(By.XPATH, "//div[@class='pt5']/div[@class='job-details-how-you-match__skills-item-wrapper display-flex flex-row pt4'][2]")
            clean(search)
        except IndexError:
            if (len(search) > 0):
                clean(search[0])
                continue
        except Exception:
            print(f"Job has no skills displayed {s}")
        
        if pressed("q"):
            break
        sleep(0.6)
    
    if pressed("q"):
        break
    
    
    try:
        driver.find_element(By.XPATH, f"//button[@class='jobs-search-pagination__indicator-button ' and @aria-label='Page {page}']").click()
    except Exception:
        driver.find_element(By.XPATH, "//button[@aria-label='Page 9']").click()
    
    sleep(1)

#%%
print(sorted(missing.items(), key=lambda item: item[1]))
