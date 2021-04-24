from zeus.database.uptime import get_websites_for_all
from flask import current_app as app
import concurrent.futures
import requests
from functools import partial
from zeus import LIST_OF_UPTIME_WEBSITE_TO_CHECK


def uptime_cron_method():   
    source_data = get_websites_for_all()
    process_users_data = {}
    for data in source_data:
        username = dict(data)['username']
        if not username in process_users_data:
            process_users_data[username] = []
        process_users_data[username].append(data['website'])
    with concurrent.futures.ProcessPoolExecutor(5) as executor:
        futures = {
            executor.submit(partial(run, user), process_users_data[user]): user for user in process_users_data
        }
        for fut in concurrent.futures.as_completed(futures):
            original_task = futures[fut]
            LIST_OF_UPTIME_WEBSITE_TO_CHECK[original_task] = fut.result()

def check_site(site):
    try:
        status = requests.get(site, timeout=5).status_code
        if status == 200:
            return "up"
    except requests.exceptions.ConnectionError:
        pass
    return "down"

def run(user, sites):
    results = []
    with concurrent.futures.ThreadPoolExecutor(100) as executor:
        for arg, res in zip(sites, executor.map(check_site, sites)):
            results.append({"website": arg, "status": res})
    return results