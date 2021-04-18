import getopt
import json
import os
import sys

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


def main(argv):
    filename = "config"
    opts, args = getopt.getopt(argv,"c:",["config="])
    for opt, arg in opts:
        if opt in ("-c", "--config"):
            filename = arg
    config = "/" + str(filename).strip(".json").strip() + ".json"
    if os.path.exists(os.getcwd() + config):
        with open("." + config) as f:
            configData = json.load(f)
    else:
        configTemplate = {"Usernames": ""}

        with open(os.getcwd() + config, "w+") as f:
            json.dump(configTemplate, f)

    driver_path = Path("/chromedriver.exe")
    userDataDir = Path(r"/chromedriver/User Data")

    nameList = configData["Usernames"]

    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Chrome(executable_path=os.path.dirname(os.path.abspath(__file__)) + "/chromedriver.exe",
                              chrome_options=options)

    game_number = 0

    usernames = nameList.split(",")

    count = 0
    for username in usernames:
        username.strip()
        game_number = new_user(driver, username, count, game_number)
        print(game_number)
        driver.execute_script("window.open('https://acquire.tlstyer.com/');")
        driver.switch_to.window(driver.window_handles[-1])
        count += 1
    driver.execute_script("window.close();")


def new_user(driver, username_input, nth_user, game_number_input):
    driver.get("https://acquire.tlstyer.com/")
    login(driver, username_input)
    # if nth_user % 3 == 0 or game_number_input == 0:
    #    return create_game(driver)
    # else:
    #    watch_game(driver, game_number_input)
    #    return game_number_input


def watch_game(game_number_input):
    wait_for_element(By.XPATH, ".//div[@id='lobby-game-{}']//input[@value='Watch']".format(game_number_input)).click()


def login(driver, username_input):
    driver.find_element_by_id("login-form-username").clear()
    driver.find_element_by_id("login-form-username").send_keys(username_input)
    print("typed in a username")
    driver.find_element_by_xpath("//input[@value='Login']").click()


def create_game(driver):
    Select(wait_for_element(By.ID, 'cg-max-players')).select_by_value("1")
    driver.find_element_by_id("button-create-game").click()
    elem = wait_for_element(By.XPATH, './/span[@class = "header"]')
    return int(elem.text.replace(":", "").replace("Game #", ""))


def wait_for_element(driver, by, value):
    print("waiting for element to load")
    return WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, value)))


main(sys.argv[1:])
input("Press Enter to continue...")