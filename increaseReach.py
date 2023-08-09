import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import tkinter as tk
import chatgpt_connect
from selenium.common.exceptions import NoSuchElementException


import win32ui
import win32con


def increaseUserReachAndEngagement(driver):
    
    actions = ActionChains(driver)
    root = tk.Tk()
    eachPost = 0
    
    while eachPost < 20:
        
        try:
            eachPostBlock = driver.find_elements(By.XPATH, "//div[contains(@class, 'feed-shared-update-v2 feed-shared-update-v2')]")[eachPost]
            actions.move_to_element(eachPostBlock).perform()
            expandButton = eachPostBlock.find_element(By.XPATH, ".//li-icon[contains(@aria-label, 'Open')]")
            actions.move_to_element(expandButton).perform()
            expandButton.click()
            time.sleep(2)
            copyLinkToPostClick = driver.find_element(By.XPATH, "//h5[contains(., 'Copy link to post')]").click()
            time.sleep(10)
            postLink = root.clipboard_get()
            commentText = chatgpt_connect.connectToGPT(postLink)
            print(commentText)
            commentButton = eachPostBlock.find_element(By.XPATH, ".//span[contains(., 'Comment')]")
            actions.move_to_element(commentButton).perform()
            commentButton.click()
            commentSpace = eachPostBlock.find_element(By.XPATH, ".//following::div[contains(@data-placeholder, 'Add a comment')]")
            actions.move_to_element(commentSpace).perform()
            commentSpace.send_keys(commentText)
            response = win32ui.MessageBox("You sure about this comment?", "Alert!", win32con.MB_YESNOCANCEL)
            if response == win32con.IDYES:
                postComment = driver.find_element(By.XPATH, "//button[contains(., 'Post')]").click()
            
            eachPost = eachPost+1
        
        except NoSuchElementException:
            eachPost = eachPost + 1
            
        
    