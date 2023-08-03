import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import chat
import win32ui
import win32con

def traverseAndReply(driver):
    actions = ActionChains(driver)
    myMessages = driver.find_element(By.XPATH, "//a[contains(@href, 'messaging')]").click()
    searchText = "Would you be willing to connect with me for an informational interview for 15 mins at your convenience?"
    
    #how many people to traverse? Most recent #20
    
    eachConnection = 0
    
    while eachConnection <50:
        
        try:
            #declare element
            conversationBlock = driver.find_elements(By.XPATH, "//div[contains(@class, 'msg-conversation-card msg-conversation')]")[eachConnection]
            actions.move_to_element(conversationBlock).perform()
            conversationBlock.click()
            messageBlock = driver.find_elements(By.XPATH, "//div[contains(@class, 'msg-s-message-list')]//p")
            latestText = messageBlock[-1].text
            
            if searchText in latestText:
                followupText = latestText.split('\n')[0] + "\nThank you for accepting my connection request! I am currently planning the next step in my career. Would you be willing to discuss with me your day-to-day work, company culture and any pointers that I should keep in mind during my search? \nThanks!"
                textBox = driver.find_element(By.XPATH, "//div[contains(@class, 'message-texteditor')]//div[contains(@aria-label, 'Write a message')]")
                textBox.send_keys(followupText)
                time.sleep(1)
                sendMessage = driver.find_element(By.XPATH, "//button[contains(., 'Send')]").click()
            
            else:
                lastPersonWhoTexted = driver.find_elements(By.XPATH, "//span[contains(@class, 'profile-link')]")
                print(lastPersonWhoTexted[-1].text)
                if "Subhrangsu Bose" not in lastPersonWhoTexted[-1].text: 
                    followupText = chat.chatFunction(latestText)
                    if "No appropriate response" not in followupText:
                        textBox = driver.find_element(By.XPATH, "//div[contains(@class, 'message-texteditor')]//div[contains(@aria-label, 'Write a message')]")
                        textBox.send_keys(followupText)
                        response = win32ui.MessageBox("You sure about this text?", "Alert!", win32con.MB_YESNOCANCEL)
                        if response == win32con.IDYES:
                            sendMessage = driver.find_element(By.XPATH, "//button[contains(., 'Send')]").click()
            eachConnection = eachConnection+1
            
        except:
            pass