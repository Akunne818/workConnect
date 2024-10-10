from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the Chrome driver
# Set up the Chrome driver (adjust path if needed)
s = Service("C:\\Users\\ASUS\\.wdm\\drivers\\chromedriver\\win64\\129.0.6668.91\\chromedriver-win32\\chromedriver.exe")
driver = webdriver.Chrome(service=s)

# LinkedIn job search URL
url = 'https://www.linkedin.com/jobs/search?keywords=python+developer&location=United%20States&geoId=103644278&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'

# Open the page
driver.get(url)

# Wait for the job listings to appear
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.jobs-search__results-list'))
    )
    
    # Select all job listings
    job_listings = driver.find_elements(By.CSS_SELECTOR, '.jobs-search__results-list li')

    # Loop through the listings and extract information
    for listing in job_listings:
        try:
            # Extract job title
            job_title = listing.find_element(By.CSS_SELECTOR, 'h3').text.strip()

            # Extract company name
            company_name = listing.find_element(By.CSS_SELECTOR, 'h4').text.strip()

            # Extract job link
            job_link = listing.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')

            # If job title or company is empty, extract it from the job link
            if not job_title or not company_name:
                job_link_parts = job_link.split('/')
                job_title = job_link_parts[-1].split('-')[0]
                company_name = job_link_parts[-2].split('-at-')[-1]

            # Print the information
            print(f"Job Link: {job_link}")
            print(f"Job Title: {job_title}")
            print(f"Company: {company_name}")
            print("------------")

        except Exception as inner_e:
            print(f"Error parsing job listing: {inner_e}")

except Exception as e:
    print(f"An error occurred: {e}")

# Close the browser
driver.quit()
