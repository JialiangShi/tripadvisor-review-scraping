from selenium import webdriver
import requests
from bs4 import BeautifulSoup

driver = webdriver.Chrome('/usr/local/bin/chromedriver')  # Optional argument, if not specified will search path.
# or, fill in your ANACONDA_INSTALL_DIR and try this:
# driver = webdriver.Chrome('ANACONDA_INSTALL_DIR/chromedriver-Darwin')

# <span class="taLnk ulBlueLinks" onclick="widgetEvCall('handlers.clickExpand',event,this);">更多</span>

driver.get('https://www.tripadvisor.com.tw/Hotel_Review-g13808671-d306446-Reviews-Grand_Hotel_Taipei-Zhongshan_District_Taipei.html')
# driver.find_element_by_class_name("taLnk ulBlueLinks").click()
# here is where some useful work would typically happen
# search_box = driver.find_element_by_name('search')
# search_box.send_keys('wings')
# search_box.submit()
#
# <p class="partial_entry">古色古香的飯店，雖然交通不太方便，但飯店有提供接駁車搭乘往捷運站，職員亦親切有禮。房間舒適，風景好，會再入住</p>
# Selenium hands the page source to Beautiful Soup

soup = BeautifulSoup(driver.page_source, 'lxml')

for link in soup.find_all("p", {"class":"partial_entry"}):
    print(link.text)

input("Press Enter to quit")
driver.quit() # close browser