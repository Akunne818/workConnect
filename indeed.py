from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Selenium options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

# Path to your ChromeDriver
driver_path = 'C:\\Users\\ASUS\\.wdm\\drivers\\chromedriver\\win64\\129.0.6668.91\\chromedriver-win32\\chromedriver.exe'

# Initialize the WebDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

try:
    # Navigate to the job page
    driver.get("https://ng.indeed.com/jobs?q=python+developer&l=Lagos&start=20")

    # Wait for job elements to be present
    WebDriverWait(driver, 100).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.job_seen_beacon')))

    job_elements = driver.find_elements(By.CLASS_NAME, "css-5lfssm")  # Adjust the class name as necessary

    for job in job_elements:
        try:
            # Extract job title
            title_element = job.find_element(By.CLASS_NAME, "jobTitle")
            job_title = title_element.text

            # Extract company name
            company_element = job.find_element(By.CLASS_NAME, "company_location")
            company_name = company_element.find_element(By.CLASS_NAME, "css-63koeb").text

            # Extract job location
            location = company_element.find_element(By.CLASS_NAME, "css-1p0sjhy").text

            # Check if the job is remote
            
            print(f"Job Title: {job_title}, Company: {company_name}, Location: {location}")
        except Exception as e:
            pass

finally:
    driver.quit()