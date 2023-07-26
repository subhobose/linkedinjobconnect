import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


import pandas as pd

def traverseAndSaveConnections(driver):
    
    actions = ActionChains(driver)
    nameList = []
    headlineList = []
    # extract list of connections
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

    for eachConnection in range(totalNumberOfConnections):

        try:
            connNameElement = driver.find_elements(By.XPATH, "//span[contains(@class, 'mn-connection-card__name')]")[eachConnection]
            connName = connNameElement.text.encode('utf-8')
            nameList.append(repr(connName)[2:-1])

            connHLElement = driver.find_elements(By.XPATH, "//span[contains(@class, 'mn-connection-card__occupation')]")[eachConnection]
            connHL = connHLElement.text.encode('utf-8')
            headlineList.append(repr(connHL)[2:-1])

    
        except IndexError:
            print("Reached End Of List")
            break
    
    return nameList, headlineList
