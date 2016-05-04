# -*- coding: utf-8 -*-

"""
Scrap CBSE Website to extract data for all the schools
url:    http://cbseaff.nic.in/cbse_aff/schdir_Report/userview.aspx

"""

import argparse
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
        try:
            location = page.find(id='foldinglist1').table.findAll('td')[1::2]
        except:
            location = None
        try:
            nature = page.find(id='foldinglist2').table.findAll('td')[1::2]
        except:
            nature = None
        try:
            facil = page.find(id='Ul5').findAll('td')[1::2]
        except:
            facil = None
        try:
            total_students = reduce(lambda x, y: int(x) + int(y),
                                [''.join(i.stripped_strings) for i in page.find(id='Ul1').findAll('td')[7:][0::4] ]).__str__()
        except:
            total_students = None
        try:
            area = page.find(id='Ul4').findAll('td')[2:12][1::2]
        except:
            area = None
        try:
            name=page.table.find_all('tr')[2].findChildren()[2].text.strip()
        except:
            name= None
        try:
           affno=self.affno
        except:
            affno=None
        try:
            state=page.table.find_all('tr')[4].findChildren()[2].text.strip()
        except:
            state=None
        try:
            district=page.table.find_all('tr')[5].findChildren()[2].text.strip()
        except:
            district=None
        try:
            address=page.table.find_all('tr')[6].findChildren()[2].text.strip()
        except:
            address=None
        try:
            pin=page.table.find_all('tr')[7].findChildren()[2].text.strip()
        except:
            pin=None
        try:
            phone=phone
        except:
            phone=None
        try:
            fax=page.table.find_all('tr')[11].findChildren()[2].text.strip()
        except:
            fax=None
        try:
            email=page.table.find_all('tr')[12].findChildren()[2].text.strip()
        except:
            email=None
        try:
            website=page.table.find_all('tr')[13].findChildren()[2].text.strip()
        except:
            website=None
        try:
            foundationYear=page.table.find_all('tr')[14].findChildren()[2].text.strip()
        except:
            foundationYear=None
        try:
            firstOpeningDate=page.table.find_all('tr')[15].findChildren()[2].text.strip()
        except:
            firstOpeningDate=None
        try:
            head=self.head
        except:
            head=None
        try:
            sex=page.table.find_all('tr')[17].findChildren()[2].text.strip()
        except:
            sex=None
        try:
            principalEducational=page.table.find_all('tr')[18].findChildren()[2].text.strip()
        except:
            principalEducational=None
        try:
            noOfExp= noOfExp
        except:
            noOfExp=None
        try:
            status=page.table.find_all('tr')[22].findChildren()[2].text.strip()
        except:
            status=None
        try:
            affiliationType=page.table.find_all('tr')[23].findChildren()[2].text.strip()
        except:
            affiliationType=None
        try:
            afiliationfFrom=page.table.find_all('tr')[25].findChildren()[2].text.strip()
        except:
            afiliationfFrom=None
        try:
            afiliationfTo=''.join(page.table.find_all('tr')[26].findChildren()[2].text.split())
        except:
            afiliationfTo=None
        try:
            trustName=page.table.find_all('tr')[27].findChildren()[2].text.strip()
        except:
            trustName=None
        try:
            location_nearest_railway_station=''.join(location[0].stripped_strings)
        except:
            location_nearest_railway_station=None
        try:
            location_nearest_railway_station_distance=''.join(location[1].stripped_strings)
        except:
            location_nearest_railway_station_distance=None
        try:
            location_nearest_police_station=''.join(location[2].stripped_strings)
        except:
            location_nearest_police_station=None
        try:
            location_nearest_police_station_distance=''.join(location[3].stripped_strings)
        except:
            location_nearest_police_station_distance=None
        try:

            location_nearest_nationalised_bank=''.join(location[4].stripped_strings)
        except:
            location_nearest_nationalised_bank=None
        try:

            location_nearest_nationalised_bank_distance=''.join(location[5].stripped_strings)
        except:
            location_nearest_nationalised_bank_distance=None
        try:

            nature_category_of_school=''.join(nature[0].stripped_strings)
        except:
           nature_category_of_school =None        
        try:

            nature_medium_of_instruction=''.join(nature[1].stripped_strings)
        except:
            nature_medium_of_instruction=None
        try:

            nature_types_of_school=''.join(nature[2].stripped_strings)
        except:
           nature_types_of_school =None
        try:

            enrolment=total_students
        except:
           enrolment =None
        try:

            infraStructure='-'.join(list(page.find(id='Ul2').stripped_strings)[1:])
        except:
            infraStructure=None
        try:

            teachingStaff='-'.join(list(page.find(id='Ul3').stripped_strings)[1:])
        except:
            teachingStaff=None


        try:
            physical_infrastructure_area_of_campus_in_sqmts=''.join(area[0].stripped_strings) if area else None
        except:
            physical_infrastructure_area_of_campus_in_sqmts=None
        try:
            physical_infrastructure_area_of_campus_in_acres=''.join(area[1].stripped_strings) if area else None
        except:
            physical_infrastructure_area_of_campus_in_acres=None
        try:
            physical_infrastructure_built_up_area=''.join(area[2].stripped_strings) if area else None
        except:
            physical_infrastructure_built_up_area=None
        try:
            physical_infrastructure_number_of_sites=''.join(area[3].stripped_strings) if area else None
        except:
            physical_infrastructure_number_of_sites=None
        try:
            physical_infrastructure_area_of_playground=''.join(area[4].stripped_strings) if area else None
        except:
            physical_infrastructure_area_of_playground=None
        try:
            facilities_total_number_of_books = ''.join(facil[0].stripped_strings) if facil else None
        except:
            facilities_total_number_of_books=None
        try:
            facilities_swimming_pool = ''.join(facil[5].stripped_strings) if facil else None
        except:
            facilities_swimming_pool=None
        try:
            facilities_indoor_games = ''.join(facil[6].stripped_strings) if facil else None
        except:
            facilities_indoor_games=None
        try:
            facilities_dance_rooms = ''.join(facil[7].stripped_strings) if facil else None
        except:
            facilities_dance_rooms=None
        try:
            facilities_gymnasium = ''.join(facil[8].stripped_strings) if facil else None
        except:
            facilities_gymnasium=None
        try:
            facilities_music_rooms = ''.join(facil[9].stripped_strings) if facil else None
        except:
            facilities_music_rooms=None
        try:
            facilities_hostel = ''.join(facil[10].stripped_strings) if facil else None
        except:
            facilities_hostel=None
        try:
            facilities_health_and_medical_check= ''.join(facil[11].stripped_strings) if facil else None 
        except:
            facilities_health_and_medical_check=None
        
        data = {
            'affno': affno,
            'name': name,
            'state': state,
            'district':district ,
            'address': address,
            'pin': pin,
            'phone': phone,
            'fax': fax,
            'email': email,
            'website': website,
            'foundationYear': foundationYear,
            'firstOpeningDate': firstOpeningDate,
            'head': head,
            'sex': sex,
            'principalEducational': principalEducational,
            'noOfExp':  noOfExp,
            'status': status,
            'affiliationType': affiliationType,
            'afiliationfFrom': afiliationfFrom,
            'afiliationfTo': afiliationfTo,
            'trustName': trustName,
            'location_nearest_railway_station': location_nearest_railway_station,
            'location_nearest_railway_station_distance':location_nearest_railway_station_distance ,
            'location_nearest_police_station': location_nearest_police_station,
            'location_nearest_police_station_distance': location_nearest_police_station_distance,
            'location_nearest_nationalised_bank':location_nearest_nationalised_bank ,
            'location_nearest_nationalised_bank_distance': location_nearest_nationalised_bank_distance,
            'nature_category_of_school': nature_category_of_school,
            'nature_medium_of_instruction':nature_medium_of_instruction ,
            'nature_types_of_school': nature_types_of_school,
            'enrolment':enrolment ,
            'infraStructure':infraStructure ,
            'teachingStaff':teachingStaff ,
            'physical_infrastructure_area_of_campus_in_sqmts':physical_infrastructure_area_of_campus_in_sqmts , 
            'physical_infrastructure_area_of_campus_in_acres':physical_infrastructure_area_of_campus_in_acres , 
            'physical_infrastructure_built_up_area':physical_infrastructure_built_up_area , 
            'physical_infrastructure_number_of_sites': physical_infrastructure_number_of_sites, 
            'physical_infrastructure_area_of_playground':physical_infrastructure_area_of_playground , 
            'facilities_total_number_of_books':facilities_total_number_of_books ,
            'facilities_swimming_pool':facilities_swimming_pool ,
            'facilities_indoor_games':facilities_indoor_games ,
            'facilities_dance_rooms':facilities_dance_rooms ,
            'facilities_gymnasium':facilities_gymnasium ,
            'facilities_music_rooms': facilities_music_rooms,
            'facilities_hostel': facilities_hostel,
            'facilities_health_and_medical_check':facilities_health_and_medical_check
        }
        for key in data:
            data[key] = data[key].encode('utf-8') if data[key] else 'NA'
        return data



class Scrap:
    """
    Instance of School
    """
    
    def __init__(self, start):
        self.start = start
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
        per_page = 25
        try:
            for i in xrange(1, self.start):
                nextBtn = driver.find_element_by_id("Button1")
                if not nextBtn.get_attribute("disabled"):    
                    nextBtn.click()
                    time.sleep(1)
                else:
                    break
                total_count -= (25 * self.start)
        except Exception as e:
            print e
        print "Total {} Schools found.".format(total_count)
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
                    if len(school_data) >= 50:
                        db_init()
                        print "Saving {0} - {1} to database..".format( i + 25 - len(school_data), i+24)
                        for item in school_data:
                            try:
                                entry = School.create(**item)
                            except IntegrityError:
                                entry = School.update(**item).where(School.affno == item['affno'])
                        print "All data saved to Database"
                        database.close()
                        school_data = []

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
    name = TextField(default=None)
    state = TextField(default=None)
    district = TextField(default=None)
    address = TextField(default=None)
    pin = TextField(default=None)
    phone = TextField(default=None)
    fax = TextField(default=None)
    email = TextField(default=None)
    website = TextField(default=None)
    foundationYear = TextField(default=None)
    firstOpeningDate = TextField(default=None)
    head = TextField(default=None)
    sex = TextField(default=None)
    principalEducational = TextField(default=None)
    noOfExp =  TextField(default=None)
    status = TextField(default=None)
    affiliationType = TextField(default=None)
    afiliationfFrom = TextField(default=None)
    afiliationfTo = TextField(default=None)
    trustName = TextField(default=None)
    location_nearest_railway_station = TextField(default=None)
    location_nearest_railway_station_distance = TextField(default=None)
    location_nearest_police_station = TextField(default=None)
    location_nearest_police_station_distance = TextField(default=None)
    location_nearest_nationalised_bank = TextField(default=None)
    location_nearest_nationalised_bank_distance = TextField(default=None)
    nature_category_of_school = TextField(default=None)
    nature_medium_of_instruction = TextField(default=None)
    nature_types_of_school = TextField(default=None)
    enrolment = TextField(default=None)
    infraStructure = TextField(default=None)
    teachingStaff = TextField(default=None)
    physical_infrastructure_area_of_campus_in_sqmts = TextField(default=None) 
    physical_infrastructure_area_of_campus_in_acres = TextField(default=None) 
    physical_infrastructure_built_up_area = TextField(default=None) 
    physical_infrastructure_number_of_sites = TextField(default=None) 
    physical_infrastructure_area_of_playground = TextField(default=None) 
    facilities_total_number_of_books = TextField(default=None)
    facilities_swimming_pool = TextField(default=None)
    facilities_indoor_games = TextField(default=None)
    facilities_dance_rooms = TextField(default=None)
    facilities_gymnasium = TextField(default=None)
    facilities_music_rooms = TextField(default=None)
    facilities_hostel = TextField(default=None)
    facilities_health_and_medical_check= TextField(default=None) 


def db_init():
    database.connect()
    if not School.table_exists():
        database.create_tables([School]) 
def parse_arg():
    parser = argparse.ArgumentParser(
        description=(
            "Convert given source code into .pdf with syntax highlighting"),
        epilog="Author:tushar.rishav@gmail.com"
    )
    parser.add_argument("-s",
                        "--start",
                        help="Starting page",
                        type=int,
                        default = 1)
    return parser.parse_args()

def main():
    args = parse_arg()
    print "Starting from page {}".format(args.start)
    try:
        bot = Scrap(args.start)
        data = bot.extract()
    except KeyboardInterrupt:
        print "Saving data to database.."
        db_init()
        print "Saving to database.."
        for item in data:
            try:
                entry = School.create(**item)
            except IntegrityError:
                entry = School.update(**item).where(School.affno == item['affno'])
        print "All data saved to Database"
        database.close()
        sys.exit(0)

    
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

