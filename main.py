from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import re

driverPath = ChromeDriverManager().install()
service = Service(driverPath)

driver:Chrome = webdriver.Chrome(service=service)

driver.get("https://musescore.com/user/21769911/scores/4918059")
driver.maximize_window()

#Validate cookies
driver.find_elements(By.XPATH, "//*[@id=\"qc-cmp2-ui\"]/div[2]/div/button[2]")[0].click()

sheetsWrapper = driver.find_element(By.ID, "jmuse-scroller-component")

musicSheets = {}
musicName = ""

currentSheetId = 0
maxSheetId = 1

while currentSheetId < maxSheetId:

    htmlParse:BeautifulSoup = BeautifulSoup(driver.page_source, 'html.parser')
    sheetsElements = htmlParse.find_all("img", {"class": "KfFlO"})

    if musicName == "":
        musicName = sheetsElements[0]["alt"]
        musicName = re.sub(r" – \d+ of \d+ pages", "", musicName)

    for sheetObj in htmlParse.find_all("img", {"class": "KfFlO"}):
        musicSheets[sheetObj["alt"]] = sheetObj["src"]

assert 1 == 1