from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

# Initialize the Chrome driver (replace with your ChromeDriver path)
service = ChromeService(executable_path="C:\\Users\\ASUS\\.wdm\\drivers\\chromedriver\\win64\\129.0.6668.91\\chromedriver-win32\\chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Open the Adzuna job search page
url = "https://www.adzuna.com/search?q=python+developer&location=Lagos"
driver.get(url)

# Wait for jobs to load
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 'job'))
)

# Data storage
data = []

while True:
    try:
        # Extract job listings on the current page
        jobs = driver.find_elements(By.CLASS_NAME, 'job')

        for job in jobs:
            try:
                title = job.find_element(By.TAG_NAME, 'h2').text
                company = job.find_element(By.CLASS_NAME, 'company').text
                location = job.find_element(By.CLASS_NAME, 'location').text
                link = job.find_element(By.TAG_NAME, 'a').get_attribute('href')
                data.append([title, company, location, link])
            except Exception as e:
                print(f"Error extracting job: {e}")

        # Find and click the 'Next' button to load more jobs
        next_button = driver.find_element(By.LINK_TEXT, 'Next')
        next_button.click()
        time.sleep(5)  # Wait for the new page to load

    except Exception as e:
        print("No more pages or an error occurred:", e)
        break  # Exit the loop when no more pages are available

# Print the extracted data
for job in data:
    print(f"Job Title: {job[0]}, Company: {job[1]}, Location: {job[2]}, Link: {job[3]}")

# Close the driver
driver.quit()
