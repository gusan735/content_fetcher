import requests
import os
import configparser
import json
from datetime import datetime, timedelta
import web_scraper
from resources import db_broker


#GLOBAL 
config = configparser.RawConfigParser()
config.read('/Users/gustavandre/Desktop/Projekt/config.ini') 
REQUEST_LIMIT = int(config.get('TWITTER', 'REQUEST_LIMIT'))
HOURS_BACK_IN_TIME = int(config.get('TWITTER', 'HOURS_BACK_IN_TIME')) + 1
N_LINKS_TO_PRINT = int(config.get('TWITTER', 'N_LINKS_TO_PRINT'))
MAX_RESULTS = int(config.get('TWITTER', 'MAX_RESULTS'))
MEDIAS = json.loads(config.get('TWITTER', 'MEDIAS'))
N_LINKS_TO_DB = int(config.get('TWITTER', 'N_LINKS_TO_DB'))

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
def auth():
    config = configparser.RawConfigParser()
    config.read('/Users/gustavandre/Desktop/Projekt/config.ini')
    bearer_token = config.get('TWITTER', 'APP_BEARER_TOKEN')
    return bearer_token

def get_start_time():
    #currently not used
    current_date = datetime.now()
    registry_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources", "registry.json")
    with open(registry_file_path) as registry_file:
        registry = json.load(registry_file)
        last_tweet_search = datetime.strptime(registry["last_tweet_search"], '%Y-%m-%dT%H:%M:%S.%fZ') - timedelta(minutes=15)
        return last_tweet_search.isoformat("T") + "Z"
    """
    start_date = current_date - timedelta(hours = HOURS_BACK_IN_TIME)
    """
    #return start_date.isoformat("T") + "Z"

def set_last_tweet_search(datetime):
    registry_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "resources", "registry.json")
    registry = {}
    with open(registry_file_path) as registry_file:
        registry = json.load(registry_file)
        registry["last_tweet_search"] = str(datetime.isoformat("T") + "Z")
    with open(registry_file_path, "w") as registry_file:
        json.dump(registry, registry_file)
    

def add_medias_to_query_string():
    medias = json.loads(config.get('TWITTER', 'MEDIAS'))

    url_string = ""
    for media in medias:
        url_string = url_string + "url:\"{}\" OR ".format(media)
    #Remove last 'OR' clause
    url_string = url_string[:-4]
    return url_string


def create_url():
    query = "-is:retweet -is:quote ({})".format(add_medias_to_query_string())
    tweet_fields = "author_id,created_at,entities,text,withheld"
    tweet_mode = "extended"
    start_time = get_start_time()
    max_results = MAX_RESULTS
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&tweet.fields={}&start_time={}&max_results={}".format(
        query, tweet_fields, start_time, max_results
    )
    return url

def add_links_to_dict(link_dicts, json_response):
    for obj in json_response["data"]:
        entities = obj["entities"]
        id = obj["id"]
        text = obj["text"]
        author = obj["author_id"]
        created_at = obj["created_at"]
        urls = []
        if "urls" in entities:
            for url in entities["urls"]:
                #Some links to DN will give 2 urls where one is real and the other one is just http://DN.SE So this is not needed.
                if (url["expanded_url"] == 'http://DN.SE'):
                    continue
                if not (has_author_tweeted_link(url["expanded_url"], author, link_dicts)):
                    urls.append(url["expanded_url"])
        if len(urls) == 0:
            continue
        link_dicts[id] = {}
        link_dicts[id]["text"] = text
        link_dicts[id]["author_id"] = author
        link_dicts[id]["created_at"] = created_at
        link_dicts[id]["urls"] = urls

    return link_dicts

def has_author_tweeted_link(link, author_id, link_dicts):
    for id in link_dicts:
        if link_dicts[id]["author_id"] == author_id:
            if (link in link_dicts[id]["urls"]):
                return True
    return False


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def process_links_from_all_requests(json_response):
    output_dict = {}
    i = 0
    while "next_token" in json_response["meta"]:
        i +=1
        if (i > REQUEST_LIMIT):
            break
        next_token = json_response["meta"]["next_token"]
        next_url = create_url() + "&next_token="+next_token
        json_response = connect_to_endpoint(next_url, create_headers(auth()))
        output_dict = add_links_to_dict(output_dict, json_response)
    return output_dict


def fetch_news_tweets():
    bearer_token = auth()
    url = create_url()
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    news_links = process_links_from_all_requests(json_response)
    set_last_tweet_search(datetime.utcnow())
    
    return news_links
