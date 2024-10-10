import requests

def get_remoteok_jobs():
    url = "https://remoteok.io/api"
    response = requests.get(url)
    jobs = response.json()

    # Sort jobs by position and date posted
    sorted_jobs = sorted(jobs[1:], key=lambda job: (job.get('position'), job.get('date')))

    for job in sorted_jobs:  # Skipping the first element (metadata)
        print(f"Job Title: {job.get('position')} | Company: {job.get('company')} | Date: {job.get('date')}")

if __name__ == "__main__":
    get_remoteok_jobs()


