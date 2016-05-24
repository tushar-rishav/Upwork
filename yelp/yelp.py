"""
Extract data from yelp.com
"""
from bs4 import BeautifulSoup
import csv
import random
from requests import Session
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import socket
import sys
import time


def encode(text, code="utf-8"):
    try:
        return text.encode(code)
    except AttributeError:
        return text;

class Bot:
    USER_AGENT = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
        )
    DCAP = dict(DesiredCapabilities.PHANTOMJS)
    DCAP["phantomjs.page.settings.userAgent"] = USER_AGENT
    driver = webdriver.PhantomJS()
    driver.implicitly_wait(40)
    driver.set_page_load_timeout(30)
    req = Session()
    def __init__(self):
        socket.setdefaulttimeout(10)


class Page:
    search_btn_id = "header-search-submit"
    search_input_id = "dropperText_Mast"

    def __init__(self):
        pass

    @staticmethod
    def get_url(location, start):
        return "http://www.yelp.com/search?find_loc={}&cflt=restaurants&start={}".format(location, start)


class Hotel:

    LOCATION = set()
    LOCATION_DONE = set()
    ZIP_FILE = "zip.txt"
    ZIP_DONE_FILE = "zip_done.txt"
    ZIP_DONE = set()

    def __init__(self, **kwargs):
        self.attr_list = """
        zip
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

    def extract(self):
        result = []
        attrs = self.attr_list.split()
        for a in attrs:
            val = getattr(self, a) if getattr(self, a) else "NA"
            result.append("{value}".format(attr=a, value=encode(val)))
        return result

    @classmethod
    def get_zips(cls):
        
        with open(Hotel.ZIP_DONE_FILE, 'r+') as zipdf:
            cls.LOCATION_DONE = {int(zz.strip()) for zz in zipdf if zz.strip()}
        with open(Hotel.ZIP_FILE, 'r+') as zipfile:
            cls.LOCATION = {int(zz.strip()) for zz in zipfile if zz.strip()} # Set to avoid duplicates

        return list(cls.LOCATION - cls.LOCATION_DONE) 

class Record:
    def __init__(self):
        self.filename = "data.csv"

    def save(self, data):
        with open(self.filename, 'ab') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(data)


def main():
    d = Bot.driver
    record = Record()
    valid_zips = Hotel.get_zips()
    if not valid_zips:
        print("All data extracted already. Maybe enter a new zip code.")
        sys.exit(0)

    for loc in valid_zips:
        print(loc)
        Hotel.ZIP_DONE.add(loc)
        hotel_detail = []
        for start in range(0,2000,10):
            url = Page.get_url(loc, start)
            time.sleep(random.randint(1, 2) * .931467298)
            try:
                d.get(url)
            except TimeoutException:
                print("RELOADING..{}".format(loc))
                d.refresh()
            refs = []
            for reftag in d.find_elements_by_css_selector('.indexed-biz-name>a'):
                refs.append(reftag.get_attribute('href'))   
            if not refs:
                print("End of search for Zip Code {}".format(loc))
                break;
            for ref in refs:
                time.sleep(random.randint(1, 2) * .931467298)
                print("Processing {}".format(ref))                
                try:
                    d.get(ref)
                except TimeoutException:
                    print("RELOADING..{}".format(ref))
                    d.refresh()
                try:
                    elementFound = WebDriverWait(d, 30).until(
                        EC.presence_of_element_located((By.TAG_NAME, "address")))
                except TimeoutException:
                    print("Retrying..{}".format(ref))
                    d.get(ref)
                soup = BeautifulSoup(d.page_source, 'lxml')
                name = soup.h1.text.strip()
                try:
                    _zip = soup.select('span[itemprop="postalCode"]')[0].text.strip()
                except:
                    _zip = loc
                try:
                    phone = soup.select(".biz-phone")[0].text.strip()
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
                try:
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
                except:
                    pass

                hotel = Hotel(zip=_zip,
                              name=name,
                              phone=phone,
                              website=website,
                              cuisine_type=cuisine_type,
                              number_of_reviews=number_of_reviews,
                              avg_review=avg_review,
                              delivery=delivery,
                              takeout=takeout,
                              caters=caters)
                
                record.save(hotel.extract())
        with open(Hotel.ZIP_DONE_FILE, 'ab') as zdf:
            zdf.write('\n' + str(loc))
        print("Zip Code {} done".format(loc))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        with open(Hotel.ZIP_DONE_FILE, 'ab') as zdf:
            for zipdone in Hotel.ZIP_DONE:
                zdf.write('\n' + str(zipdone))
        print("Closed.")
