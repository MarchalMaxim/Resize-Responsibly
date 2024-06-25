from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Open Google
driver.get("http://www.google.com")

# Wait for a few seconds to ensure the page loads completely
time.sleep(3)

# Take a screenshot and save it
driver.save_screenshot("google_homepage.png")

# Close the browser
driver.quit()
