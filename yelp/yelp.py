"""
Extract data from yelp.com
"""
from bs4 import BeautifulSoup
import openpyxl
from openpyxl import Workbook
from openpyxl.writer.write_only import WriteOnlyCell
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import sys
from requests import Session
import time


class Bot:
    USER_AGENT = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
        )
    DCAP = dict(DesiredCapabilities.PHANTOMJS)
    DCAP["phantomjs.page.settings.userAgent"] = USER_AGENT
    driver = webdriver.Firefox()
    driver.implicitly_wait(40)
    req = Session()
    def __init__(self):
        pass


class Page:
    search_btn_id = "header-search-submit"
    search_input_id = "dropperText_Mast"

    def __init__(self):
        pass

    @staticmethod
    def get_url(location, start):
        return "http://www.yelp.com/search?find_loc={}&start={}".format(location, start)


class Hotel:

    LOCATION = ['Austin, TX', 'Houston, TX', 'Colorado, TX',
                'Spring, TX', 'Denver, TX', 'The Woodlands, TX']

    def __init__(self, **kwargs):
        self.attr_list = """
        name
        phone
        website
        cuisine_type
        number_of_reviews
        avg_review
        delivery
        takeout
        caters
        """
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def __str__(self):
        result = ""
        attrs = self.attr_list.split()
        print(attrs)
        for a in attrs:
            result += "{attr}:{value},".format(attr=a, value=getattr(self, a))
        return result


def main():
    d = Bot.driver
    for loc in Hotel.LOCATION:
        hotel_detail = []
        for start in range(0,991,10):
            url = Page.get_url(loc, start)
            d.get(url)
            refs = []
            for reftag in d.find_elements_by_css_selector('.indexed-biz-name>a'):
                refs.append(reftag.get_attribute('href'))   
            for ref in refs:
                time.sleep(1)
                print("Processing {}".format(ref))                
                d.get(ref)
                try:
                    elementFound = WebDriverWait(d, 30).until(
                        EC.presence_of_element_located((By.TAG_NAME, "address")))
                except TimeoutException:
                    print("Retrying..{}".format(ref))
                    d.get(ref)
                soup = BeautifulSoup(d.page_source, 'lxml')
                name = soup.h1.text
                try:
                    phone = soup.select(".biz-phone")[0].text
                except:
                    phone = None
                try:
                    website = soup.find_all("div", class_="biz-website")[0].a.text.strip()
                except:
                    website = None
                try:
                    cuisine_type = ''.join(soup.find_all("span", class_="category-str-list")[0].stripped_strings).strip()
                except:
                    cuisine_type = None
                try:
                    number_of_reviews = soup.select('span[itemprop="reviewCount"]')[0].text.strip()
                except:
                    number_of_reviews = None
                try:
                    avg_review = soup.select('meta[itemprop="ratingValue"]')[0].get('content').strip()
                except:
                    avg_review = None

                b_info = soup.select(".short-def-list")[-1].find_all('dl')
                delivery = None
                takeout = None
                caters = None
                for info in b_info:
                    if info.find('dt').text.strip() == "Delivery":
                        delivery = info.find('dd').text.strip()
                    elif info.find('dt').text.strip() == "Caters":
                        caters = info.find('dd').text.strip()
                    elif info.find('dt').text.strip() == "Take-out":
                        takeout = info.find('dd').text.strip()

                hotel = Hotel(name=name,
                              phone=phone,
                              website=website,
                              cuisine_type=cuisine_type,
                              number_of_reviews=number_of_reviews,
                              avg_review=avg_review,
                              delivery=delivery,
                              takeout=takeout,
                              caters=caters)
                print(hotel)
                hotel_detail.append(hotel)
        break;


if __name__ == "__main__":
    main()
