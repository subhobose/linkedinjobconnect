import scraper
import messages
import traverseConnections

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def main():
    companyName = "Tesla"
    connectionSearchCriteria = companyName + " software manager"
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=chrome_options)
    
    scraper.login(driver)
    # messages.traverseAndReply(driver)
    scraper.searchAndSendRequests(driver, connectionSearchCriteria, companyName)
    driver.quit()

if __name__ == "__main__":
    main()