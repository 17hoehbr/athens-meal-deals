import undetected_chromedriver as uc
import re
import csv
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


driver = uc.Chrome()

# navigate to the Autotrader website
driver.get("https://www.kroger.com/weeklyad")

# Wait for the results container to load
closebtn = driver.find_element(By.CSS_SELECTOR, '.kds-DismissalButton')

closebtn.click()

modalbtn = driver.find_element(By.CSS_SELECTOR, '.CurrentModality-button')

modalbtn.click()

zipbtn = driver.find_element(By.CSS_SELECTOR, '.PostalCodeSearchBox--drawer')

zipbtn.click()

zipsearch = driver.find_element(By.CSS_SELECTOR, '.kds-Input--compact')

zipsearch.sendKeys("45701")

setzipbtn = driver.find_element(By.CSS_SELECTOR, '.kds-SolitarySearch-button')

pickupbtn = driver.find_element(By.CSS_SELECTOR, '.pb-8 > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > button:nth-child(1)')

pickupbtn.click()

shoppickupbtn = driver.find_element(By.CSS_SELECTOR, 'button.variant-fill:nth-child(1)')

shoppickupbtn.click()

sleep(3)

downloadpdfbtn = driver.find_element(By.CSS_SELECTOR, '.kds-Link--l')

downloadpdfbtn.click()

# close the browser
driver.quit()
