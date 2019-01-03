from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def read_excel(file_path):
    hotels = pd.read_excel(file_path)
    hotel_name = hotels['旅館名稱Hotel Name']
    urls = hotels['TripAdvisor網址']
    return hotel_name, urls

def scrape_data(url):
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.get(url)
    names = []
    titles = []
    star_ratting = []
    location = []
    date = []
    comments = []
    replies = []
    delay = (1, 2)

    # driver.find_element_by_class_name('ui_radio item').click()
    for i in range(1):  # break when there is no more pages
        # show whole comments, doesn't work for now
        # driver.find_element_by_link_text('所有語言').click()
        # driver.find_element_by_link_text('更多').click()

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        for link in soup.find_all("div", {"class": "review-container"}):

            titles.append(link.find("span", {"class": "noQuotes"}).text)

            # < span class ="ui_bubble_rating bubble_50" > < / span >
            star_ratting.append(link.select("span[class^=ui_bubble_rating]")[0]['class'][1][-2])

            # if there is location shown, name and location will be shown together
            if link.find("div", {"class": "userLoc"}):
                loc = link.find("div", {"class": "userLoc"}).text
                location.append(loc)
                name_loc = link.find("div", {"class": "info_text"}).text
                names.append(name_loc.rstrip(loc))
            else:
                location.append(None)
                names.append(link.find("div", {"class": "info_text"}).text)

            d = link.find("div", {"class": "prw_rup prw_reviews_stay_date_hsx"}).text
            if d:
                date.append(d.split()[1])
            else:
                date.append(None)

            # if there is more than 2 comments, the 1st is the comment and the 2nd is the reply
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
    return names, titles, star_ratting, location, date, comments, replies


file_path = 'hotel.xlsx'
hotels = []
names = []
titles = []
star_ratting = []
location = []
date = []
comments = []
replies = []

hotel_name, urls = read_excel(file_path)

for hotel_url in zip(hotel_name, urls):
    n, t, s, l, d, c, r = scrape_data(hotel_url[1])
    hotels.extend([hotel_url[0] for i in range(len(t))])
    names.extend(n)
    titles.extend(t)
    star_ratting.extend(s)
    location.extend(l)
    date.extend(d)
    comments.extend(c)
    replies.extend(r)

# url = 'https://www.tripadvisor.com.tw/Hotel_Review-g13808450-d3856249-Reviews-Taichung_Harbor_Hotel-Wuqi_Taichung.html'
# titles, comments, replies = scrape_data(url)

df = pd.DataFrame({'hotels': hotels, 'names': names, 'titles': titles, 'star_ratting':star_ratting,
                   'location':location, 'date': date, 'comments': comments, 'replies': replies})
df.to_csv('comments.csv', index=False, encoding='utf-8')

