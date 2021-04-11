import os
import requests
import json
import sys

# TODO:Clean this shit up
src_path = os.path.dirname(os.path.realpath(__file__))
police_events_path = os.path.dirname(src_path)
project_path = os.path.dirname(src_path)
resources_path = os.path.join(os.path.dirname(project_path), "resources")
sys.path.append(resources_path)
sys.path.append(project_path)
import db_broker
#import web_scraper

# VARS
src_path = os.path.dirname(os.path.realpath(__file__))
police_events_url = "https://polisen.se/api/events"


def fetch_recent_events(url):
    content = requests.get(url)
    all_events = json.loads(content.content)
    return all_events


def main():
    recent_events = fetch_recent_events(police_events_url)
    for event in recent_events:
        event = fix_police_datetime(event)
        db_broker.create_police_event(event)
    db_broker.fetch_police_details_in_db()


def fix_police_datetime(event):
    fixed_event = event
    datetime_string = event['datetime']
    datetime_string_fixed = ""
    if (len(datetime_string) == 25):
        datetime_string_fixed = datetime_string[:11] + \
            '0' + datetime_string[11:]
        fixed_event['datetime'] = datetime_string_fixed
    return fixed_event


if __name__ == '__main__':
    main()
