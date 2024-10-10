import requests
from bs4 import BeautifulSoup

def extract(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}
    url = f"https://ng.indeed.com/jobs?q=python+developer&l=Lagos&start={page}&vjk=cd819a99166e560c"
    r = requests.get(url, headers=headers)
    if r.status_code == 403:
        print("403 Forbidden")
        print(r.headers)
        print(r.text)
    return r.status_code


print(extract(0)) # extract(0)  