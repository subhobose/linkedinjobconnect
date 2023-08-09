import scraper
import messages
import traverseConnections
import increaseReach

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#Philips, Ansys, Honda, Tesla
def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)
    
    scraper.login(driver)
    # increaseReach.increaseUserReachAndEngagement(driver)
    
    # messages.traverseAndReply(driver)
    
    companyList = ["Symplicity"]
    
    for companyName in companyList:
        connectionSearchCriteria = companyName + " software manager"
        scraper.searchAndSendRequests(driver, connectionSearchCriteria, companyName)
    driver.quit()

if __name__ == "__main__":
    main()