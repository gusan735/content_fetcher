import os
import requests
import json
import sys

#TODO:Clean this shit up
src_path = os.path.dirname(os.path.realpath(__file__))
police_events_path = os.path.dirname(src_path)
police_events_path = os.path.dirname(src_path)
project_path = os.path.join(os.path.dirname(police_events_path), "resources")
sys.path.append(project_path)
import db_broker


#VARS
src_path = os.path.dirname(os.path.realpath(__file__))
police_events_url = "https://polisen.se/api/events"

def fetch_recent_events (url):
    content = requests.get(url)
    all_events = json.loads(content.content)
    return all_events

	
def main():
	recent_events = fetch_recent_events(police_events_url)
	for event in recent_events:
		db_broker.create_police_event(event)
	db_broker.write_data_to_csv()
	
if __name__ == '__main__':
    main()

