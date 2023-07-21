from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

# from traverseConnections import traverseAndSaveConnections

class InvalidLocationException(Exception):
    "Location other than US"
    pass

companyName = "AMD"
connectionSearchCriteria =companyName + " software india"
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
actions = ActionChains(driver)

driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
driver.maximize_window()
username = driver.find_element(By.NAME, "session_key")
username.send_keys("subhobose99@gmail.com")
password = driver.find_element(By.NAME, "session_password")
password.send_keys("Enter password")
actions.send_keys(Keys.ENTER)
actions.perform()
driver.implicitly_wait(10)

# nameList, headLineList = traverseAndSaveConnections()
# print(nameList, headLineList)

#input search criteria
searchBar = driver.find_element(By.XPATH, "//input[contains(@class, 'search-global-typeahead__input')]").send_keys(connectionSearchCriteria)
actions.send_keys(Keys.ENTER)
actions.perform()

driver.implicitly_wait(10)
expandPeopleList = driver.find_element(By.XPATH, "//button[contains(., 'People')]").click()
driver.implicitly_wait(10)

#page containing connections
counter = 0
eachConnection = 0
noOfPagesCounter = 1
while eachConnection <= 10:

    if counter >=10:
        break

    try:
        print(eachConnection)
        connectBlock = driver.find_elements(By.XPATH, "//div[contains(@class, 'entity-result__item')]")[eachConnection]
        # print(connectBlock.text)
        if connectBlock.find_element(By.XPATH, ".//span[contains(@class, 'artdeco-button__text') and contains(., 'Connect')]"):
            profileView = connectBlock.find_element(By.XPATH, ".//span[contains(@class, 'entity-result__title-text')]")
            # print(profileView.text)
            searchPeopleURL = driver.current_url
            profileView.click()
            driver.implicitly_wait(10)
            profileName = driver.find_element(By.XPATH, "//h1[contains(@class, 'text-heading-xlarge')]").text
            currentLocation = driver.find_element(By.XPATH, "//div[contains(@class, 'pv-text-details__left-panel mt2')]").text

            if "United States" not in currentLocation:
                raise InvalidLocationException
            #if most recent experience is independent
            experienceLocator = driver.find_element(By.XPATH, "//div[contains(@class, 'pvs-header__title-container') and contains(., 'Experience')]")
            jobRoleLocator = experienceLocator.find_element(By.XPATH, "./following::span[1]")
            jobRole = jobRoleLocator.text
            if companyName.lower() not in jobRole.lower():
                recentCompanyLocator = jobRoleLocator.find_element(By.XPATH, "./following::span[3]")
                recentCompany = recentCompanyLocator.text
            else:
                #if most recent experience has multiple roles in the same company
                recentCompany = jobRole
                jobRoleLocator = experienceLocator.find_element(By.XPATH, "./following::span[10]")
                jobRole = jobRoleLocator.text
                additionalData = experienceLocator.find_element(By.XPATH, "./following::span[7]").text
                jobRole = jobRole + additionalData


            print(profileName)
            print(jobRole)
            print(recentCompany)

            #include check condition to send
            if "intern" not in jobRole.lower() and companyName.lower() in recentCompany.lower():
                print("Valid! Let's connect!")
                connectButton = driver.find_element(By.XPATH, "//div[contains(@class, 'ph5 pb5')]//button[contains(@aria-label, 'Invite')]")
                connectButton.click()
                driver.implicitly_wait(5)
                connectWithMessage = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Add a note')]")
                connectWithMessage.click()
                driver.implicitly_wait(5)
                promptMessage = "Hi {},\nI am a MSCS student at UT Dallas and I am currently on the hunt for a Fall 2023 internship.\n{} is one of the companies I have closely followed for a long time. Would you be willing to connect with me for an informational interview for 15 mins at your convenience?\nThanks!"\
                    .format(profileName.partition(' ')[0], companyName)
                addMessage = driver.find_element(By.XPATH, "//textarea").send_keys(promptMessage)
                driver.implicitly_wait(5)
                time.sleep(30)              #for checking rn, will be modified
                sendMessageButton = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Send now')]")
                sendMessageButton.click()
                counter += 1
                driver.implicitly_wait(10)
            driver.get(searchPeopleURL)
            eachConnection = eachConnection+1
    
    except IndexError:
        try:
            print(driver.current_url)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            goToNextPage = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Next')]").click()
            print("New Page")
            noOfPagesCounter = noOfPagesCounter+1
            time.sleep(3)
            eachConnection = 0
        except NoSuchElementException:
            print("End of Results reached")
        
    except NoSuchElementException:
        print("Connect Button Not Found")
        eachConnection = eachConnection+1

    except InvalidLocationException:
        print("Not based outta US")
        eachConnection = eachConnection+1
        driver.get(searchPeopleURL)

print("A total of {} new requests sent!". format(counter))
    