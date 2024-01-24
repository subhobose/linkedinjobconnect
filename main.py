import scraper
# import messages
import traverseConnections
import increaseReach

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#Philips, Ansys, Honda, Tesla, 
def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)
    
    scraper.login(driver)
    # increaseReach.increaseUserReachAndEngagement(driver)
    # messages.traverseAndReply(driver)
    
    companyList = ["Pure Storage"]
    companySpecificTeam = ["Data Science"]
    
    for i in range(len(companyList)):
        connectionSearchCriteria = companyList[i] + " software manager"
        scraper.searchAndSendRequests(driver, connectionSearchCriteria, companyList[i], companySpecificTeam[0])
    driver.quit()

if __name__ == "__main__":
    main()