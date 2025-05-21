import requests
import pandas as pd
import json

# Jobicy API Extraction

BASE_URL = "https://jobicy.com/api/v2/remote-jobs?count=50&geo={geo}"
regions = ["latam", "europe", "usa", "apac"]

unique_jobs_jobicy = {}

for region in regions:
    url = BASE_URL.format(geo=region)
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'jobs' in data:
                jobs = data['jobs']
                for job in jobs:
                    job['region'] = region  
                    unique_jobs_jobicy[job['id']] = job
            else:
                print(f"No jobs found in region: {region}")
        
        else:
            print(f"Request Error in {region}: {response.status_code}")
    
    except Exception as e:
        print(f"Request Error in {region}: {str(e)}")

all_jobs_jobicy = list(unique_jobs_jobicy.values())

df = pd.DataFrame(all_jobs_jobicy)
df.to_csv('data/raw/jobicy_jobs.csv', index=False)

print(" jobicy data extracted and saved succesfully")

# Remotive API Extraction
base_url = "https://remotive.com/api/remote-jobs"
categories = ["software-dev", "data"]
search_terms = ["python", "R", "SQL"]

unique_jobs_remotive = {}

for category in categories:
    for term in search_terms:
        params = {
            "category": category,
            "search": term,
            "limit": 300
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            jobs = data.get("jobs", [])
            for job in jobs:
                unique_jobs_remotive[job['id']] = job
            print(f"Jobs extracted for category: {category} and search term: {term}, count: {len(jobs)}")
        else:
            print(f"Error obtaining data for category {category} and search term {term}: {response.status_code}")

print(f"Total jobs extracted from Remotive: {len(unique_jobs_remotive)}")

all_jobs_remotive = list(unique_jobs_remotive.values())

df = pd.DataFrame(all_jobs_remotive)
df.to_csv("data/raw/remotive_jobs.csv", index=False)




