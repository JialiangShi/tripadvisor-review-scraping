from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import requests
from bs4 import BeautifulSoup

driver = webdriver.Chrome('/usr/local/bin/chromedriver')  # Optional argument, if not specified will search path.
# or, fill in your ANACONDA_INSTALL_DIR and try this:
# driver = webdriver.Chrome('ANACONDA_INSTALL_DIR/chromedriver-Darwin')

# <span class="taLnk ulBlueLinks" onclick="widgetEvCall('handlers.clickExpand',event,this);">更多</span>
URL = 'https://www.tripadvisor.com.tw/Hotel_Review-g13808671-d306446-Reviews-Grand_Hotel_Taipei-Zhongshan_District_Taipei.html'
driver.get(URL)
# driver.find_element_by_class_name("taLnk ulBlueLinks").click()
# here is where some useful work would typically happen
# search_box = driver.find_element_by_name('search')
# search_box.send_keys('wings')
# search_box.submit()

# Selenium hands the page source to Beautiful Soup
titles = []
comments = []
delay = (2, 3)
# <span class="noQuotes">舊式飯店</span>
# <p class="partial_entry">古色古香的飯店，雖然交通不太方便，但飯店有提供接駁車搭乘往捷運站，職員亦親切有禮。房間舒適，風景好，會再入住</p>
# driver.find_element_by_link_text('往下').click()

for i in range(10):

    soup = BeautifulSoup(driver.page_source, 'lxml')
    for link in soup.find_all("span", {"class": "noQuotes"}):
        titles.append(link.text)
    for link in soup.find_all("p", {"class": "partial_entry"}):
        comments.append(link.text)

    time.sleep(random.randint(delay[0], delay[1]))  # wait random seconds
    try:
        driver.find_element_by_link_text('往下').click()
    except:
        break


print(titles)
# print(comments)
input("Press Enter to quit")
driver.quit() # close browser