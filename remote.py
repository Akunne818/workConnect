import requests

import re
def get_remoteok_jobs():
    url = "https://remoteok.io/api"
    response = requests.get(url)
    jobs = response.json()

    # Sort jobs by position and date posted
    sorted_jobs = sorted(jobs[1:], key=lambda job: (job.get('position'), job.get('date')))

    for job in sorted_jobs:  # Skipping the first element (metadata)
        print("Job Title:", job.get('position'))
        print("Company:", job.get('company'))
        print("Date:", job.get('date'))
        print("Categories:", job.get('categories'))
        print("Tags:", job.get('tags'))
        print("Type:", job.get('type'))
        print("Location:", job.get('location'))
        print("Company Logo:", job.get('company_logo'))
        print("Company URL:", job.get('company_url'))
        print("Source:", job.get('source'))
        print("Source URL:", job.get('source_url'))
        print("Apply URL:", job.get('url'))
        print("Salary:", job.get('salary'))
        print("Description:", re.sub(r'<[^>]*>', '', job.get('description')))
        print("="*50) 


if __name__ == "__main__":
    get_remoteok_jobs()


