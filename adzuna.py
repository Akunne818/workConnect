import requests

def get_adzuna_jobs():
    base_url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
    params = {
        "app_id": "60b518a4",  # Replace with your actual App ID
        "app_key": "6057c7ba906685ecc7ac88fd2e744047",  # Replace with your actual App Key
        "results_per_page": 10,  # Number of results to return per page
        "what": "software engineer",  # Keyword for job search
        "where": "remote",  # Location for the job search (e.g., remote)
        "sort_by": "date"  # Sort jobs by the most recent
    }

    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        jobs = response.json()
        for job in jobs.get('results', []):
            title = job.get('title', 'N/A')
            company = job.get('company', {}).get('display_name', 'N/A')
            description = job.get('description', 'N/A')
            print(f"Job Title: {title} | Company: {company} | Description: {description}")
    else:
        print(f"An error occurred: {response.status_code}")

if __name__ == "__main__":
    get_adzuna_jobs()