from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def read_excel(file_path):
    hotels = pd.read_excel(file_path)
    names = hotels['旅館名稱Hotel Name']
    urls = hotels['TripAdvisor網址']
    return names, urls

def get_data(url):
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.get(url)
    titles = []
    comments = []
    replies = []
    delay = (1, 2)

    # driver.find_element_by_class_name('ui_radio item').click()
    while True:
        # show whole comments, doesn't work for now
        # driver.find_element_by_link_text('更多').click()

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        for link in soup.find_all("div", {"class": "review-container"}):
            titles.append(link.find("span", {"class": "noQuotes"}).text)
            # check whether hotel replied or not
            if len(link.find_all("p", {"class": "partial_entry"})) == 1:
                comments.append(link.find("p", {"class": "partial_entry"}).text)
                replies.append(None)
            else:
                comments.append(link.find_all("p", {"class": "partial_entry"})[0].text)
                replies.append(link.find_all("p", {"class": "partial_entry"})[1].text)
        time.sleep(random.randint(delay[0], delay[1]))  # wait random seconds

        try:
            driver.find_element_by_link_text('往下').click()
        except:
            break  # break the loop at the last page

    driver.close()
    return titles, comments, replies


# file_path = 'hotel.xlsx'
# names, urls = read_excel(file_path)
# output = []
# for name_url in zip(names, urls):
#     if not name_url[1]:
#         continue
#     titles, comments = get_data(name_url[1])
#     output.append([name_url[0], data])
# print(len(output))

url = 'https://www.tripadvisor.com.tw/Hotel_Review-g13808450-d3856249-Reviews-Taichung_Harbor_Hotel-Wuqi_Taichung.html'
titles, comments, replies = get_data(url)

df = pd.DataFrame({'titles': titles, 'comments': comments, 'replies': replies})
df.to_csv('comments.csv', index=False, encoding='utf-8')

