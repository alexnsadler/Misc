"""Program to automatically log user in to google calendar."""

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def open_calendar(email_add, password):
    """Automatically login to Google Calendar."""
    print "Opening Google Calendar..."

    driver = webdriver.Chrome()
    driver.get("https://calendar.google.com/calendar/")

    email = driver.find_element_by_id("identifierId")
    email.send_keys(email_add)
    email.send_keys(Keys.RETURN)

    time.sleep(1)

    actions = ActionChains(driver)
    actions.send_keys(password + Keys.RETURN)
    actions.perform()
