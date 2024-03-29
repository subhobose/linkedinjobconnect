
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import yaml
import copy

class InvalidLocationException(Exception):
    "Location other than US"
    pass

def login(driver):
    
    actions = ActionChains(driver)
    driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
    driver.maximize_window()
    
    with open('config\\credentials.yml', 'r') as file:
        config = yaml.safe_load(file)
    username = driver.find_element(By.NAME, "session_key")
    username.send_keys(config['user_email'])
    password = driver.find_element(By.NAME, "session_password")
    password.send_keys(config['password'])
    actions.send_keys(Keys.ENTER)
    actions.perform()
    time.sleep(15)

def searchAndSendRequests(driver, connectionSearchCriteria, companyName, companySpecificTeam):
    
    actions = ActionChains(driver)
    homePageURL = driver.current_url
    
    #input search criteria
    searchBar = driver.find_element(By.XPATH, "//input[contains(@class, 'search-global-typeahead__input')]")
    searchBar.clear()
    searchBar.send_keys(connectionSearchCriteria)
    actions.send_keys(Keys.ENTER)
    actions.perform()

    driver.implicitly_wait(10)
    expandPeopleList = driver.find_element(By.XPATH, "//button[contains(., 'People')]").click()
    driver.implicitly_wait(10)

    #flow to include 2nd and 3rd connections only
    selectConnections = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Connections filter.')]").click()
    driver.implicitly_wait(5)
    selectSecondConnections = driver.find_element(By.XPATH, "//label[contains(., '2nd')]").click()
    selectOtherConnections = driver.find_element(By.XPATH, "//label[contains(., '3rd+')]")
    selectOtherConnections.click()
    showConnectionResults = selectOtherConnections.find_element(By.XPATH, "./following::button[2]").click()
    time.sleep(2)

    #flow to include current company filter
    selectCurrentCompany = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Current company filter.')]").click()
    driver.implicitly_wait(5)
    selectCompanyFromList = driver.find_element(By.XPATH, "//label[contains(., '"+companyName+"')]")
    selectCompanyFromList.click()
    showCompanyResults = selectCompanyFromList.find_element(By.XPATH, "./following::button[2]").click()
    time.sleep(2)

    # selectActivelyHiring = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Actively hiring')]").click()
    # time.sleep(2)

    #page containing connections
    counter = 0
    eachConnection = 0
    noOfPagesCounter = 1
    while eachConnection <= 10:

        if counter >=10:
            break

        try:
            print(eachConnection+1)
            connectBlock = driver.find_elements(By.XPATH, "//li[contains(@class, 'reusable-search__result-container')]")[eachConnection]
            # print(connectBlock.text)
            # if connectBlock.find_element(By.XPATH, ".//span[contains(@class, 'artdeco-button__text') and contains(., 'Connect')]"):
            profileView = connectBlock.find_element(By.XPATH, ".//span[contains(@class, 'entity-result__title-text')]")
                # print(profileView.text)
            searchPeopleURL = driver.current_url
            profileView.click()
            driver.implicitly_wait(10)
            profileName = driver.find_element(By.XPATH, "//h1[contains(@class, 'text-heading-xlarge')]").text
            profileName = profileName.encode('utf-8')
            profileName = repr(profileName)[2:-1]
            currentLocation = driver.find_element(By.XPATH, "//span[contains(@class, 'text-body-small inline t-black--light break-words')]").text

            #if connection already pending
            pendingButton = driver.find_elements(By.XPATH, "//div[contains(@class, 'ph5 pb5')]//button[contains(@aria-label, 'Pending')]")
            if len(pendingButton)>0:
                raise NoSuchElementException

            # if "United States" not in currentLocation:
            #     raise InvalidLocationException
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
            if "intern" not in jobRole.lower() and "intern" not in recentCompany.lower() and companyName.lower() in recentCompany.lower():
                print("Valid! Let's connect!")
                connectButton = driver.find_elements(By.XPATH, "//div[contains(@class, 'ph5 pb5')]//button[contains(@aria-label, 'Invite')]")
                if len(connectButton) == 0:
                    moreButton = driver.find_element(By.XPATH, "//div[contains(@class, 'ph5 pb5')]//button[contains(@aria-label, 'More')]")
                    moreButton.click()
                    driver.implicitly_wait(10)
                    connectButtonAlt = driver.find_element(By.XPATH, "//div[contains(@class, 'ph5 pb5')]//div[contains(@aria-hidden, 'false')]//div[contains(@aria-label, 'Invite')]").click()
                else:
                    connectButton[0].click()
                driver.implicitly_wait(5)
                emailVerify = driver.find_elements(By.XPATH, "//label[contains(@for, 'email')]")
                if len(emailVerify)>0:
                    raise NoSuchElementException
                connectWithMessage = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Add a note')]")
                connectWithMessage.click()
                driver.implicitly_wait(5)
                companyNameInText = copy.deepcopy(companyName)
                if len(companyName.split()) > 1:
                    companyNameInText = "".join(e[0] for e in companyName.split())
                promptMessage = "Hi {},\nI am a MSCS student at UT Dallas and I am currently on the hunt for a New Grad Software 2024 role. I have been developing SW for 3+ years. \nI have closely followed {} for a long time. Can you help me become a part of the team?\nThanks!"\
                    .format(profileName.partition(' ')[0], companyNameInText)
                #     .format(profileName.partition(' ')[0], companyNameInText)
                # promptMessage = "Hi {},\nI am a MSCS student at UT Dallas and I am currently on the hunt for a Fall 2023 Internship.\n{} is one of the companies I have closely followed for a long time. Would you be willing to connect with me for an informational interview for 15 mins at your convenience?\nThanks!"\
                #     .format(profileName.partition(' ')[0], companyName)
                # promptMessage = "Hi {},\nI am a MSCS student at UT Dallas and I am currently on the hunt for a Spring 2024 Internship. I have been developing SW for 3+ years.\nI have closely followed {} and I believe I am a great fit. Can you help me become a part of the team?\nThanks!"\
                #     .format(profileName.partition(' ')[0], companyNameInText)
                addMessage = driver.find_element(By.XPATH, "//textarea").send_keys(promptMessage)
                driver.implicitly_wait(5)
                time.sleep(5)              #for checking rn, will be modified
                sendMessageButton = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Send now')]")
                sendMessageButton.click()
                counter += 1
                driver.implicitly_wait(10)
            driver.get(searchPeopleURL)
            time.sleep(3)
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
            
        #incase of pending connection requests
        except NoSuchElementException:
            print("Connect Button Not Found")
            eachConnection = eachConnection+1
            driver.get(searchPeopleURL)
            time.sleep(3)

        except InvalidLocationException:
            print("Not based outta US")
            eachConnection = eachConnection+1
            driver.get(searchPeopleURL)
            time.sleep(3)

    print("A total of {} new requests sent!". format(counter))
    driver.get(homePageURL)
        