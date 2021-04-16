from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import json
import os
import re


if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)
else:
    configTemplate = {"Usernames": "", "Windows Username": ""}

    with open(os.getcwd() + "/config.json", "w+") as f:
        json.dump(configTemplate, f)



PATH = "C:\chromedriver.exe"


delay = configData["Delay"]
nameList = configData["Usernames"]
windowsUsername = configData["Windows Username"]

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')

driver = webdriver.Chrome(PATH, chrome_options=options)

gameNumber = 0



def newUser(username, number, gameNumber):
    driver.get("https://acquire.tlstyer.com/")
    logIn(username)
    time.sleep(1)
    if number % 3 == 0 or gameNumber == 0:
        return createGame()
    else:
        watchGame(gameNumber)
        return gameNumber

def watchGame(gameNumber):
    driver.find_element_by_xpath(".//div[@id='lobby-game-{}']//input[@value='Watch']".format(gameNumber)).click()

def logIn(username):
    loggedIn = False
    while not loggedIn:
        driver.find_element_by_id("login-form-username").clear()
        driver.find_element_by_id("login-form-username").send_keys(username)
        print("typed in a username")
        driver.find_element_by_xpath("//input[@value='Login']").click()
        loggedIn = True
        
def createGame():
    createdGame = False
    while not createdGame:
        Select(driver.find_element_by_id('cg-max-players')).select_by_value("1")
        driver.find_element_by_id("button-create-game").click()
        time.sleep(0.5)
        
        for elem in driver.find_elements_by_xpath('.//span[@class = "header"]'):
            return int(elem.text.replace(":", "").replace("Game #", ""))
            createdGame = True


usernames = nameList.split(",")

count = 0
for username in usernames:
    username.strip()
    gameNumber = newUser(username, count, gameNumber)
    print(gameNumber)
    driver.execute_script("window.open('https://acquire.tlstyer.com/');")
    driver.switch_to.window(driver.window_handles[-1])
    count += 1
driver.execute_script("window.close();")
    