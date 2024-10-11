import requests
from bs4 import BeautifulSoup

def scrape_full_job_description(url):
    try:
        # Send a GET request to the job page
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'lxml')

            # Find the section with class 'adp-body' (full job description)
            job_body_section = soup.find(class_='adp-body')

            if job_body_section:
                # Extract the text from the 'adp-body' section
                full_description = job_body_section.get_text(separator="\n").strip()
                return full_description
            else:
                return "Full description not available."
        else:
            return f"Failed to scrape the job page. Status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred while scraping the job page: {str(e)}"

def get_adzuna_jobs():
    base_url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
    params = {
        "app_id": "60b518a4",  # Replace with your actual App ID
        "app_key": "6057c7ba906685ecc7ac88fd2e744047",  # Replace with your actual App Key
        "results_per_page": 10,  # Number of results to return per page
        "what": "python developer",  # Keyword for job search
        "where": "remote",  # Location for the job search (e.g., remote)
        "sort_by": "date"  # Sort jobs by the most recent
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        jobs = response.json()
        for job in jobs.get('results', []):
            title = job.get('title', 'N/A')
            company = job.get('company', {}).get('display_name', 'N/A')
            job_url = job.get('redirect_url', 'N/A')  # Extract the job link

            # Scrape the full job description from the job link
            full_description = scrape_full_job_description(job_url)

            # Format the output with line breaks and indentation for better readability
            print(f"\nJob Title: {title}\n")
            print(f"Company: {company}\n")
            print(f"Full Description:\n{full_description}\n")
            print(f"Link (to the job page): {job_url}\n")
            print("="*50)  # Add a separator line for each job entry
    else:
        print(f"An error occurred: {response.status_code}")

if __name__ == "__main__":
    get_adzuna_jobs()
