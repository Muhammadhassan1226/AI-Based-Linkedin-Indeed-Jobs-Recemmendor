import os
from apify_client import ApifyClient

apify_client  = ApifyClient(os.getenv("APIFY_KEY"))

def fetch_linkedin_jobs(search_query,loaction="Lahore",rows=60):
    run_input = {
    "title": search_query,
    "location": loaction,
    "rows": rows,
    "proxy": {
        "useApifyProxy": True,
        "apifyProxyGroups": ["RESIDENTIAL"],
    },
    }
    run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs



def fetch_indeed_jobs(search_query,location="lahore"):
    run_input = {
    "scrapeJobs.searchUrl": f"https://www.indeed.com/jobs?q={search_query}&l={location}",
    "scrapeJobs.scrapeCompany": False,
    "count": 10,
    "outputSchema": "raw",
    "findContacts": False,
    "findContacts.contactCompassToken": None,
    }
    run = apify_client.actor("qA8rz8tR61HdkfTBL").call(run_input=run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs

    