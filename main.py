import time
from typing import List
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup, Tag
import re

import os, shutil
import requests
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

from pypdf import PdfWriter

from guis import UiProgressBar, UiSelectMusicUrl

url = UiSelectMusicUrl("Saisie URL Musescore").show(debug=True)

if url == "":
    exit()

driverPath = ChromeDriverManager().install()
service = Service(driverPath)
driver:Chrome = webdriver.Chrome(service=service)

driver.get(url)
#driver.get("https://musescore.com/user/2466621/scores/4680761")
driver.maximize_window()

#Validate cookies

WebDriverWait(driver, 10) \
    .until(EC.element_to_be_clickable((By.XPATH, "//*[@id=\"qc-cmp2-ui\"]/div[2]/div/button[2]")))
driver.find_element(By.XPATH, "//*[@id=\"qc-cmp2-ui\"]/div[2]/div/button[2]").click()

sheetsWrapper = driver.find_element(By.ID, "jmuse-scroller-component")

musicSheetTags = []
musicSheetLinks = {}
musicName = ""

progressBar = UiProgressBar("Progression du téléchargement").updateLabel("Téléchargement des pages...")

while len(musicSheetLinks) < len(musicSheetTags) or len(musicSheetTags) == 0:

    soup:BeautifulSoup = BeautifulSoup(driver.page_source, 'html.parser')
    
    if musicName == "":
        musicName = soup.find("meta", {"property": "og:title"})["content"]
        musicName = re.sub(r"[^a-zA-Z0-9_\.\s-]", "", musicName)
        

    def isSheetTag(tag:Tag):
        return \
            set(["EEnGW", "F16e6"]) == set(tag.get("class", [])) and \
            tag.parent.get("id") == "jmuse-scroller-component"

    musicSheetTags:List[Tag] = soup.find_all(lambda tag : isSheetTag(tag))    

    for musicSheetTag in musicSheetTags:
        imgTags:List[Tag] = musicSheetTag.find_all("img", {"class": "KfFlO"})

        for imgTag in imgTags:
            if not imgTag.get("src") is None:
                musicSheetLinks[imgTag["alt"]] = imgTag["src"]

    

    driver.execute_script("arguments[0].scrollTo({top:arguments[0].scrollTop + 600, left:0, behavior: \"smooth\"});", sheetsWrapper)
    time.sleep(0.5)

    progressBar.updateProgress(len(musicSheetLinks) / len(musicSheetTags))



if not os.path.exists("temp"):
    os.mkdir("temp")

remoteFiles: List[str] = dict().items()

progressBar.updateLabel("Transformation des pages en PDF...").updateProgress(0)

for index,(remoteFileName, remoteFile) in enumerate(dict(sorted(musicSheetLinks.items(), key = lambda x:x[0])).items()):
    remoteFile:str = remoteFile
    fileExtension = remoteFile.split("?")[0].split(".")[-1]
    
    localFileDefaultExtension = os.path.join("temp", f"page {index}.{fileExtension}")
    localFilePdfExtension = os.path.join("temp", f"page {index}.pdf")
    
    requestResponse = requests.get(remoteFile)
    with open(localFileDefaultExtension, "wb") as f:
        f.write(requestResponse.content)
    

    if fileExtension == "svg":
        drawing = svg2rlg(localFileDefaultExtension)
        renderPDF.drawToFile(drawing, localFilePdfExtension)
    elif fileExtension == "png":
        drawing = png2rlg
        renderPDF.drawToFile(drawing, localFilePdfExtension)

    musicSheetLinks[remoteFileName] = localFilePdfExtension

    progressBar.updateProgress((index + 1) / len(musicSheetLinks))

merger = PdfWriter()
for pdf in musicSheetLinks.values():
    merger.append(pdf)

merger.write(musicName + ".pdf")
merger.close()

shutil.rmtree("temp")

assert 1 == 1