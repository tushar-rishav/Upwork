# -*- coding: utf-8 -*-

"""
Scrap CBSE Website to extract data for all the schools
url:    http://cbseaff.nic.in/cbse_aff/schdir_Report/userview.aspx

"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from peewee import *
from requests import Session
import sys
import time

req = Session()

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
    )
DCAP = dict(DesiredCapabilities.PHANTOMJS)
DCAP["phantomjs.page.settings.userAgent"] = USER_AGENT

class Info:
    """
    School Info page
    """
    BASE_URL = "http://cbseaff.nic.in/cbse_aff/schdir_Report/AppViewdir.aspx"
    
    def __init__(self, **kwargs):
        
        for attr, value in kwargs.items():
            setattr(self, attr, value)

    def extract_data(self):
        """
        Extract data from school info table
        :returns:
            A dictionary of all info.
        """
        
        info_dict = {}
        params = {'affno':self.affno}

        
        req.params.update(params)
        r = req.get(Info.BASE_URL)
        
        raw = r.text.encode('utf-8')
        
        # Fix the stupid code style followed by CBSE developers
        raw = raw.replace('<center>','')
        raw = raw.replace('</center>','')
        raw = raw.replace('<CENTER>','')
        raw = raw.replace('</CENTER>','')
        raw = raw.replace('<font>','')
        raw = raw.replace('</font>','')
        raw = raw.replace('<FONT>','')
        raw = raw.replace('</FONT>','')

        page = BeautifulSoup( raw, 'html.parser')
        phone = ''.join('-'.join(page.table.find_all('tr')[9].stripped_strings).split() 
                )+''.join('-'.join(page.table.find_all('tr')[10].stripped_strings).split())
        noOfExp = ''.join('-'.join(page.table.find_all('tr')[20].stripped_strings).split() 
                )+''.join('-'.join(page.table.find_all('tr')[21].stripped_strings).split())
        location = page.find(id='foldinglist1').table.findAll('td')[1::2]
        nature = page.find(id='foldinglist2').table.findAll('td')[1::2]
        facil = page.find(id='Ul5').findAll('td')[1::2]
        try:
            total_students = reduce(lambda x, y: int(x) + int(y),
                                [''.join(i.stripped_strings) for i in page.find(id='Ul1').findAll('td')[7:][0::4] ]).__str__()
        except:
            total_students = None
        try:
            area = page.find(id='Ul4').findAll('td')[2:12][1::2]
        except:
            area = None

        data = {
        'name':page.table.find_all('tr')[2].findChildren()[2].text.strip(),
        'affno':self.affno,
        'state':page.table.find_all('tr')[4].findChildren()[2].text.strip(),
        'district':page.table.find_all('tr')[5].findChildren()[2].text.strip(),
        'address':page.table.find_all('tr')[6].findChildren()[2].text.strip(),
        'pin':page.table.find_all('tr')[7].findChildren()[2].text.strip(),
        'phone':phone.encode('utf-8'),
        'fax':page.table.find_all('tr')[11].findChildren()[2].text.strip(),
        'email':page.table.find_all('tr')[12].findChildren()[2].text.strip(),
        'website':page.table.find_all('tr')[13].findChildren()[2].text.strip(),
        'foundationYear':page.table.find_all('tr')[14].findChildren()[2].text.strip(),
        'firstOpeningDate':page.table.find_all('tr')[15].findChildren()[2].text.strip(),
        'head':self.head,
        'sex':page.table.find_all('tr')[17].findChildren()[2].text.strip(),
        'principalEducational':page.table.find_all('tr')[18].findChildren()[2].text.strip(),
        'noOfExp': noOfExp,
        'status':page.table.find_all('tr')[22].findChildren()[2].text.strip(),
        'affiliationType':page.table.find_all('tr')[23].findChildren()[2].text.strip(),
        'afiliationfFrom':page.table.find_all('tr')[25].findChildren()[2].text.strip(),
        'afiliationfTo':''.join(page.table.find_all('tr')[26].findChildren()[2].text.split()),
        'trustName':page.table.find_all('tr')[27].findChildren()[2].text.strip(),
        'location_nearest_railway_station':''.join(location[0].stripped_strings),
        'location_nearest_railway_station_distance':''.join(location[1].stripped_strings),
        'location_nearest_police_station':''.join(location[2].stripped_strings),
        'location_nearest_police_station_distance':''.join(location[3].stripped_strings),
        'location_nearest_nationalised_bank':''.join(location[4].stripped_strings),
        'location_nearest_nationalised_bank_distance':''.join(location[5].stripped_strings),
        'nature_category_of_school':''.join(nature[0].stripped_strings),
        'nature_medium_of_instruction':''.join(nature[1].stripped_strings),
        'nature_types_of_school':''.join(nature[2].stripped_strings),
        'enrolment':total_students,
        'infraStructure':'-'.join(list(page.find(id='Ul2').stripped_strings)[1:]),
        'teachingStaff':'-'.join(list(page.find(id='Ul3').stripped_strings)[1:]),
        
        'physical_infrastructure_area_of_campus_in_sqmts':''.join(area[0].stripped_strings) if area else None,
        'physical_infrastructure_area_of_campus_in_acres':''.join(area[1].stripped_strings) if area else None,
        'physical_infrastructure_built_up_area':''.join(area[2].stripped_strings) if area else None,
        'physical_infrastructure_number_of_sites':''.join(area[3].stripped_strings) if area else None,
        'physical_infrastructure_area_of_playground':''.join(area[4].stripped_strings) if area else None,
        'facilities':'-'.join(list(page.find(id='Ul5').stripped_strings)[1:]),
        'facilities_total_number_of_books' : ''.join(facil[0].stripped_strings) if facil else None,
        'facilities_swimming_pool' : ''.join(facil[5].stripped_strings) if facil else None,
        'facilities_indoor_games' : ''.join(facil[6].stripped_strings) if facil else None,
        'facilities_dance_rooms' : ''.join(facil[7].stripped_strings) if facil else None,
        'facilities_gymnasium' : ''.join(facil[8].stripped_strings) if facil else None,
        'facilities_music_rooms' : ''.join(facil[9].stripped_strings) if facil else None,
        'facilities_hostel' : ''.join(facil[10].stripped_strings) if facil else None,
        'facilities_health_and_medical_check': ''.join(facil[11].stripped_strings) if facil else None, 
        }
        for key in data:
            data[key] = data[key].encode('utf-8') if data[key] else 'NA'

        return data



class Scrap:
    """
    Instance of School
    """
    
    def __init__(self):
        self.url = "http://cbseaff.nic.in/cbse_aff/schdir_Report/userview.aspx"

    
    def extract(self):
        """
        Extract affiliation and head name for all CBSE schools
        :returns:
            List of dictionary containing affiliation number and name of
            school head
        """
        driver = webdriver.PhantomJS(desired_capabilities=DCAP)
        driver.implicitly_wait(50)
        print "Fetching.."
        driver.get(self.url)
        driver.find_element_by_id("optlist_0").click()
        key_text = driver.find_element_by_id("keytext")
        key_text.send_keys('a')
        key_text.send_keys(Keys.RETURN)
        time.sleep(2)
        
        try:
            soup = BeautifulSoup( driver.page_source.encode('utf-8'), 'html.parser')
            elementFound = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "lbltot")))
        
        except TimeoutException as e:
            print("Timeout, retrying..")
            with open('log','w') as log:
                log.write(str(e))
            self.extract()

        total_count = int(driver.find_element_by_id("lbltot").text)
        print "Total {} Schools found.".format(total_count)
        per_page = 25
        
        school_data = []
        try:
            for i in xrange(1, total_count + 1, per_page):
                print "{0} - {1}".format(i, i + per_page)
                page = BeautifulSoup( driver.page_source.encode('utf-8'), 'html.parser')
                table = page.find(id='T1').tbody.tr.td.findAll('table')[2::3]
                
                for entry in table:
                    aff_no = entry.findAll('tr')[0].td.text.split('.')[1]
                    head = entry.findAll('tr')[2].td.text.split(':')[1]
                    sinfo = Info( affno=aff_no, head=head)
                    school_data.append(sinfo.extract_data())

                nextBtn = driver.find_element_by_id("Button1")
                time.sleep(1)
                if not nextBtn.get_attribute("disabled"):    
                    nextBtn.click()
                else:
                    break
        except KeyboardInterrupt:
            print "Exiting.."
            driver.quit()
            return school_data
            
        driver.quit()
        print "Data extracted successfully"
        return school_data

database = MySQLDatabase('upwork', user='root',passwd='')


class BaseModel(Model):
    class Meta:
        database = database

class School(BaseModel):
    """
    Save the data to DB
    """
    affno =  CharField(unique=True)
    name = CharField(default=None)
    state = CharField(default=None)
    district = CharField(default=None)
    address = CharField(default=None)
    pin = CharField(default=None)
    phone = CharField(default=None)
    fax = CharField(default=None)
    email = CharField(default=None)
    website = CharField(default=None)
    foundationYear = CharField(default=None)
    firstOpeningDate = CharField(default=None)
    head = CharField(default=None)
    sex = CharField(default=None)
    principalEducational = CharField(default=None)
    noOfExp =  CharField(default=None)
    status = CharField(default=None)
    affiliationType = CharField(default=None)
    afiliationfFrom = CharField(default=None)
    afiliationfTo = CharField(default=None)
    trustName = CharField(default=None)
    location_nearest_railway_station = CharField(default=None)
    location_nearest_railway_station_distance = CharField(default=None)
    location_nearest_police_station = CharField(default=None)
    location_nearest_police_station_distance = CharField(default=None)
    location_nearest_nationalised_bank = CharField(default=None)
    location_nearest_nationalised_bank_distance = CharField(default=None)
    nature_category_of_school = CharField(default=None)
    nature_medium_of_instruction = CharField(default=None)
    nature_types_of_school = CharField(default=None)
    enrolment = CharField(default=None)
    infraStructure = CharField(default=None)
    teachingStaff = CharField(default=None)
    physical_infrastructure_area_of_campus_in_sqmts = CharField(default=None) 
    physical_infrastructure_area_of_campus_in_acres = CharField(default=None) 
    physical_infrastructure_built_up_area = CharField(default=None) 
    physical_infrastructure_number_of_sites = CharField(default=None) 
    physical_infrastructure_area_of_playground = CharField(default=None) 
    facilities_total_number_of_books = CharField(default=None)
    facilities_swimming_pool = CharField(default=None)
    facilities_indoor_games = CharField(default=None)
    facilities_dance_rooms = CharField(default=None)
    facilities_gymnasium = CharField(default=None)
    facilities_music_rooms = CharField(default=None)
    facilities_hostel = CharField(default=None)
    facilities_health_and_medical_check= CharField(default=None) 


def db_init():
    database.connect()
    if not School.table_exists():
        database.create_tables([School]) 


def main():
    bot = Scrap()
    data = bot.extract()
    
    db_init()
    print "Saving to database.."
    for item in data:
        try:
            entry = School.create(**item)
        except IntegrityError:
            entry = School.update(**item).where(School.affno == item['affno'])
    print "All data saved to Database"
    database.close()

if __name__=="__main__":
    main()

