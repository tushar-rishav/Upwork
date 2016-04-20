# -*- coding: utf-8 -*-
"""
Scrap email address of all agents from 
https://www.statefarm.com/agent/US/KY/Bowling-Green
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (NoSuchWindowException,
                                        ElementNotVisibleException,
                                        TimeoutException)


def main():
    url = raw_input(">Url: ")

    driver = webdriver.PhantomJS()
    driver.implicitly_wait(60)
    driver.get(url)
    
    # Fetch all the hyperlinks for agents
    agents = driver.find_elements_by_css_selector('.span4 > a')
    
    data = [] # A list of tuple containing (agent name, agent email)
    for agent in agents:
        agent_name = agent.get_attribute('title').__str__()
        print("Fetching agent {}".format(agent_name))
        
        try:
            agent.click()
        except ElementNotVisibleException:
            print("{} is hidden".format(agent.get_attribute('title').__str__()))
            continue

        # Switch to the newly opened popup window
        driver.switch_to.window('helpcenter1')
        # Click the email button
        driver.find_element_by_id('nonPilot_agent_Email_id').click()
        try:
            # Wait until the form has been loaded
            elementFound = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "businessEmailAddress")))
        except TimeoutException:
            # retry
            print("Timeout, retrying..")
            driver.find_element_by_id('nonPilot_agent_Email_id').click()
        
        if elementFound:
            emailField = driver.find_element_by_id('businessEmailAddress')
            agent_email = emailField.get_attribute('value').__str__()
            data.append((agent_name, agent_email))
        else:
            print("{}'s email not found".format(agent_name))

        driver.switch_to.window('')

    print(data)

if __name__ == "__main__":
    main()
