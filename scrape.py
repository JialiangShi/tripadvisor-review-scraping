from selenium import webdriver
from bs4 import BeautifulSoup
import time
import random

def get_data(url):
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.get(url)
    titles = []
    comments = []
    delay = (1, 2)

    while True:
        # show whole comments, doesn't work for now
        # driver.find_element_by_link_text('更多').click()

        soup = BeautifulSoup(driver.page_source, 'lxml')
        for link in soup.find_all("span", {"class": "noQuotes"}):
            titles.append(link.text)
        for link in soup.find_all("p", {"class": "partial_entry"}):
            comments.append(link.text)
        time.sleep(random.randint(delay[0], delay[1]))  # wait random seconds
        # <span class="taLnk ulBlueLinks" onclick="widgetEvCall('handlers.clickExpand',event,this);">更多</span>
        try:
            driver.find_element_by_link_text('往下').click()
        except:
            break  # break the loop at the last page
    input("Press Enter to quit")
    driver.quit()
    return [titles, comments]


url = 'https://www.tripadvisor.com.tw/Hotel_Review-g13808450-d3856249-Reviews-Taichung_Harbor_Hotel-Wuqi_Taichung.html'
data = get_data(url)
print(len(data[0]))
