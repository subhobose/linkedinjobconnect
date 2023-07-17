from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import pandas as pd

companyName = "AMD" + " software"
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
actions = ActionChains(driver)

driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
driver.maximize_window()
username = driver.find_element(By.NAME, "session_key")
username.send_keys("subhobose99@gmail.com")
password = driver.find_element(By.NAME, "session_password")
password.send_keys("fYrjah-pujqes-qyrqu4")
actions.send_keys(Keys.ENTER)
actions.perform()
driver.implicitly_wait(10)

#extract list of connections
nameList = []
headlineList = []
time.sleep(5)
myNetworkButton = driver.find_element(By.PARTIAL_LINK_TEXT, "My Network")
myNetworkButton.click()
driver.implicitly_wait(10)
seeConnections = driver.find_element(By.CLASS_NAME, "mn-community-summary__entity-info-icon")
seeConnections.click()
driver.implicitly_wait(5)

#find total number of connections
totalNumberOfConnectionString = driver.find_element(By.CLASS_NAME, "mn-connections__header").text
totalNumberOfConnections = totalNumberOfConnectionString.split()[0]
totalNumberOfConnections = pd.to_numeric(totalNumberOfConnections)

#scrolling all connections into view
counter = 1
while counter<=10:
    print(counter)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    counter = counter+1

    try:
        moreConnectionsButton = driver.find_element(By.XPATH, "//button[contains(@class, 'scaffold-finite-scroll__load-button')]")
        moreConnectionsButton.click()
        time.sleep(2)
    
    except:
        pass
        print("Button Not Found")
        time.sleep(2)

#
for eachConnection in range(totalNumberOfConnections):

    try:
        connNameElement = driver.find_elements(By.XPATH, "//span[contains(@class, 'mn-connection-card__name')]")[eachConnection]
        connName = connNameElement.text
        print(connName)
        nameList.append(connName)
    
    except IndexError:
        print("Reached End Of List")
        break
    
print(nameList)


#input company
# searchOrg = driver.find_element(By.XPATH, '/html/body/div[5]/header/div/div/div/div[1]/input')
# searchOrg.send_keys(companyName)
# actions.send_keys(Keys.ENTER)
# actions.perform()
# driver.implicitly_wait(10)
# peopleButton = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div[2]/section/div/nav/div/ul/li[3]/button')
# peopleButton.click()