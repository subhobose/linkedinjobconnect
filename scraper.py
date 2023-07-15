from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

companyName = "AMD" + " software"
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
actions = ActionChains(driver)

driver.get("https://www.linkedin.com/")
username = driver.find_element(By.XPATH, '//*[@id="session_key"]')
username.send_keys("subho.spotify@gmail.com")
password = driver.find_element(By.XPATH, '//*[@id="session_password"]')
password.send_keys("Linkedineachi$1")
signIn = driver.find_element(By.XPATH, '//*[@id="main-content"]/section[1]/div/div/form/div[2]/button')
signIn.click()
driver.implicitly_wait(10)

#input company
searchOrg = driver.find_element(By.XPATH, '/html/body/div[5]/header/div/div/div/div[1]/input')
searchOrg.send_keys(companyName)
actions.send_keys(Keys.ENTER)
actions.perform()
driver.implicitly_wait(10)
peopleButton = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div[2]/section/div/nav/div/ul/li[3]/button')
peopleButton.click()