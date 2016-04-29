import sys
import re
from bs4 import BeautifulSoup
import requests
import json
import random
import getopt
import csv
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def split_date(datestring):
    dateparts = datestring.split('-')
    return dateparts[0], dateparts[1], dateparts[2]

def login(driver, url, email, passwd):
    """
    Implement Login
    """
    print("Trying to log in..")
    driver.get(url)
    try:
        email_input = driver.find_elements_by_name("email")[1]
        passwd_input = driver.find_elements_by_name("password")[1]
    except IndexError as e:
        print e
        sys.exit(1)

    login_btn = driver.find_element_by_name("login")
    email_input.send_keys(email)
    passwd_input.send_keys(passwd)
    login_btn.click()
    time.sleep(2)
    return driver


def chegg_scrape(category, subcategory, by, bm, bd, ey, em, ed, email, passwd):
    monthnamemap = dict([("january", 1), ("february", 2), ("march", 3), ("april", 4), ("may", 5), ("june", 6), ("july", 7), ("august", 8), ("september", 9), ("october", 10), ("november", 11), ("december", 12)])
    count = 1
    QUESTION_FOLDER = "QUESTIONS"
    ANSWER_FOLDER = "ANSWERS"
    page = ''
    done = False
    retry_count = 1
    
    if not os.path.exists(QUESTION_FOLDER):
        try:
            os.mkdir(QUESTION_FOLDER)
        except Exception as e:
            print(e)
    
    if not os.path.exists(ANSWER_FOLDER):
        try:
            os.mkdir(ANSWER_FOLDER)
        except Exception as e:
            print(e)

    # phantomjs_path = r'C:\Users\ABHI\Desktop\phantomjs-2.1.1-windows\bin\phantomjs.exe'
    driver = webdriver.PhantomJS()
    driver.implicitly_wait(50)

    baseaddress = 'http://www.chegg.com/homework-help/questions-and-answers/'
    address = baseaddress + subcategory.lower() + '-archive'
    loginaddress = 'https://www.chegg.com/auth?action=login&redirect={}/&reset_password=0'.format(address)
    
    while (not done) and retry_count < 4:
        driver = login(driver, loginaddress, email, passwd)
        try:
           elementFound = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "avatar")))
        except TimeoutException:
            print("Timeout, retrying..")
            driver = login(driver, loginaddress, email, passwd)

        done = True
        time.sleep(5)
        page = driver.page_source.encode('utf-8')
        retry_count += 1

    try:
        driver.find_element_by_class_name('avatar')
    except Exception as e:
        print e
        sys.exit(2)
    
    print "Logged in successfully"

    soup = BeautifulSoup(page, 'html.parser')
    years = soup.findAll('li', attrs={'class': 'year'})
    for year in reversed(years):
        yearnumber = year.find('p', attrs={'class': 'txt-hdr-mod'})
        yearnumber = yearnumber.text

        if int(yearnumber) < int(by):
            print 'ignoring year = {}'.format(int(yearnumber))
            continue
        if int(yearnumber) > int(ey):
            print 'exiting since year = {}'.format(int(yearnumber))
            break

        monthslist = year.find('ul', attrs={'class': 'month-list'})
        months = monthslist.findAll('li')


        for month in months:

            monthanchor = month.find('a')
            monthname = monthanchor.text
            monthnumber = monthnamemap[monthname.lower()]

            if int(yearnumber) == int(by):
                if monthnumber < int(bm):
                    print 'ignoring {}-{}'.format(int(yearnumber), monthnumber)
                    continue
            if int(yearnumber) == int(ey):
                if monthnumber > int(em):
                    print 'exiting {}-{}'.format(int(yearnumber), monthnumber)
                    break

            monthaddress = baseaddress + monthanchor['href']
            print monthaddress
            monthpage = ''
            done = False
            while not done:
                try:
                    r = driver.get(monthaddress)
                    monthpage = driver.page_source
                    done = True
                except Exception as e:
                    time.sleep(10)
                    pass
            monthsoup = BeautifulSoup(monthpage, 'html.parser')


            qaarchivemonthpage = monthsoup.find('div', attrs={'class': 'qaarchive-month-page'})
            if qaarchivemonthpage is None:
                print monthsoup.prettify().encode('utf-8')
                return

            table = qaarchivemonthpage.find('table', attrs={'class': 'calendar'})
            if table is None:
                print qaarchivemonthpage.prettify().encode('utf-8')
                return
            td = table.findAll('td')
            for tddate in td:
                tddateanchor = tddate.find('a')
                if tddateanchor is None:
                    continue

                daynumber = tddateanchor.text
                daynumber = int(daynumber)

                if int(yearnumber) == int(by):
                    if monthnumber == int(bm):
                        if daynumber < int(bd):
                            print 'ignoring {}-{}-{}'.format(int(yearnumber), monthnumber, daynumber)
                            continue
                if int(yearnumber) == int(ey):
                    if monthnumber == int(em):
                        if daynumber > int(ed):
                            print 'exiting {}-{}-{}'.format(int(yearnumber), monthnumber, daynumber)
                            break

                print 'Looking at {}-{}-{}'.format(int(yearnumber), monthnumber, daynumber)
                daypageaddres = baseaddress + tddateanchor['href']
                print daypageaddres
                daypage = ''
                done = False
                while not done:
                    try:
                        r = driver.get(daypageaddres)
                        daypage = driver.page_source
                        done = True
                    except Exception as e:
                        time.sleep(10)
                        pass
                daysoup = BeautifulSoup(daypage, 'html.parser')
                qaarchivedaypage = daysoup.find('div', attrs={'class': 'qaarchive-day-page'})
                questionslist = qaarchivedaypage.find('ul', attrs={'class': 'questions-list'})
                questionbodylist = questionslist.findAll('div', attrs={'class': 'question-body'})
                for questionbody in questionbodylist:
                    questionanchor = questionbody.find('a')
                    if questionanchor is None:
                        continue
                    questionpageaddress = 'http://www.chegg.com'+questionanchor['href']
                    print questionpageaddress
                    questionpage = ''
                    done = False
                    while not done:
                        try:
                            r = driver.get(questionpageaddress)
                            questionpage = driver.page_source
                            done = True
                        except Exception as e:
                            time.sleep(5)
                            pass

                    questionsoup = BeautifulSoup(questionpage, 'html.parser')
                    question = questionsoup.find('div', attrs={'class': 'question-body'})
                    answer = questionsoup.find('div', attrs={'class': 'answer'})
                    
                    print "questionpageaddress", questionpageaddress
                    a_has_img = None; q_has_img = None;
                    if question:
                        q_has_img = BeautifulSoup(question.text, 'html.parser').find('img')
                    if answer:
                        a_has_img = BeautifulSoup(answer.text, 'html.parser').find('img')

                    if not (q_has_img or a_has_img) and (question and answer):
                        
                        ques_file = os.path.join(QUESTION_FOLDER ,'{}.html'.format(count))
                        ans_file = os.path.join(ANSWER_FOLDER ,'{}.html'.format(count))
                        
                        with open(ques_file, 'wb') as outfile:
                            outfile.write(question.prettify().encode('utf-8'))
                        
                        with open(ans_file, 'wb') as outfile:
                            outfile.write(answer.prettify().encode('utf-8'))

                        count = count + 1
                    else:
                        print 'ignoring - {}'.format(questionpageaddress)

                print 'Done! {}-{}-{}'.format(int(yearnumber), monthnumber, daynumber)

def main(argv):
    category = ''
    subcategory = ''
    begin = ''
    end = ''

    try:
        opts, args = getopt.getopt(argv,"hu:p:c:s:b:e:",["useremail=",
                                                    "passwd=",
                                                    "category=",
                                                    "subcategory=",
                                                    "year=",
                                                    "month=",
                                                    "day="])
    except Exception as e:
        print(e)
        print 'chegg.py -u <useremail> -p <passwd> -c <category> -s <subcategory> -b <begindate> -e <enddate>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'chegg.py -u <useremail> -p <passwd> -c <category> -s <subcategory> -b <begindate> -e <enddate>'
            sys.exit()
        elif opt in ("-c", "--category"):
            category = arg
        elif opt in ("-s", "--subcategory"):
            subcategory = arg
        elif opt in ("-b", "--begindate"):
            begin = arg
        elif opt in ("-e", "--enddate"):
            end = arg
        elif opt in ("-u", "--useremail"):
            email = arg
        elif opt in ("-p", "--passwd"):
            passwd = arg
    if category == '' or subcategory == '':
        print 'chegg.py -u <useremail> -p <passwd> -c <category> -s <subcategory> -b <begindate> -e <enddate>'
        sys.exit()
    by, bm, bd = split_date(begin)
    ey, em, ed = split_date(end)
    chegg_scrape(category, subcategory, by, bm, bd, ey, em, ed, email, passwd)

if __name__ == '__main__':
    main(sys.argv[1:])


