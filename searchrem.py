import csv
import html
import re
from bs4 import BeautifulSoup
import requests
import json


def robust_cleaning(text):
    """Cleans HTML tags, entities, and non-human readable characters from text."""
    # Step 1: Parse HTML tags with BeautifulSoup
    soup = BeautifulSoup(text, "html.parser")
    clean_text = soup.get_text(separator=' ')

    # Step 2: Unescape HTML entities
    clean_text = html.unescape(clean_text)

    # Step 3: Replace non-human readable characters
    clean_text = re.sub(r'â', "'", clean_text)
    clean_text = re.sub(r'â', '-', clean_text)
    clean_text = re.sub(r'Â', '', clean_text)

    # Step 4: Remove extra whitespace
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()

    return clean_text


def get_jobs(search_keywords):
    """Retrieves job listings from RemoteOK API based on search keywords."""
    jobs = []
    for keyword in search_keywords:
        url = f"https://remoteok.io/api?tag={keyword}"

        # Set up headers to mimic a browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

        # Send a GET request to the API
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            jobs.extend(response.json()[1:])  # Ignore metadata element
        else:
            print(f"Failed to retrieve jobs for '{keyword}'. Status code: {response.status_code}")
    
    return jobs


def save_to_csv(jobs, filename="jobs.csv"):
    """Saves job listings to a CSV file."""
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # Write header row
        writer.writerow(["Job Title", "Company", "Location", "Description", "Apply Link"])

        # Write job data rows
        for job in jobs:
            description = robust_cleaning(job.get('description', ''))
            writer.writerow([
                job.get('position', 'N/A'), 
                job.get('company', 'N/A'), 
                job.get('location', 'N/A'), 
                description, 
                job.get('url', 'N/A')
            ])


def main():
    # Define the search keywords (Python developer jobs)
    search_keywords = ["python", "developer", "backend", "fullstack"]

    # Retrieve job listings
    jobs = get_jobs(search_keywords)

    if jobs:
        # Save job details to a CSV file
        save_to_csv(jobs)

        print(f"{len(jobs)} jobs saved to 'jobs.csv'")
    else:
        print("No jobs found.")


if __name__ == "__main__":
    main()
