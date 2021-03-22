import requests
import os
import configparser
import json
from datetime import datetime, timedelta

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'


def auth():
    config = configparser.RawConfigParser()
    config.read('/Users/gustavandre/Desktop/Projekt/config.ini')
    bearer_token = config.get('TWITTER', 'APP_BEARER_TOKEN')
    return bearer_token

def get_start_time():
    current_date = datetime.now()
    start_date = current_date - timedelta(hours = 12)
    return start_date.isoformat("T") + "Z"

def add_medias_to_query_string():
    config = configparser.RawConfigParser()
    config.read('/Users/gustavandre/Desktop/Projekt/config.ini')
    medias = json.loads(config.get('TWITTER', 'MEDIAS'))

    url_string = ""
    for media in medias:
        url_string = url_string + "url:\"gp.se\" OR ".format(media)
    #Remove last 'OR' clause
    url_string = url_string[:-4]
    return url_string


def create_url():
    query = "-is:retweet -is:quote ({})".format("url:\"samnytt.se\"")
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, ge id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    tweet_fields = "author_id,created_at,entities,text,withheld"
    tweet_mode = "extended"
    start_time = get_start_time()
    max_results = 10
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&tweet.fields={}&start_time={}&max_results={}".format(
        query, tweet_fields, start_time, max_results
    )
    return url

def add_links_to_dict(link_dicts, json_response):
    for obj in json_response["data"]:
        entities = obj["entities"]
        if "urls" in entities:
            for url in entities["urls"]:
                #print(url["expanded_url"])
                if (url["expanded_url"]) not in link_dicts:
                    link_dicts[url["expanded_url"]] = 1
                else:
                    link_dicts[url["expanded_url"]] += 1
    #print (json.dumps(link_dicts))
    return link_dicts

    #Add links to dict 
    #return new dict
    pass

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
        if (i > 50):
            break
        next_token = json_response["meta"]["next_token"]
        print(next_token)

        #TODO: Functionize
        next_url = create_url() + "&next_token="+next_token
        #
        json_response = connect_to_endpoint(next_url, create_headers(auth()))
        output_dict = add_links_to_dict(output_dict, json_response)
    return output_dict

def main():
    bearer_token = auth()
    url = create_url()
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    print(json.dumps(json_response, indent=4, sort_keys=True))
    """
    news_links = process_links_from_all_requests(json_response)
    sorted_news_links = {k: v for k, v in sorted(news_links.items(), key=lambda item: item[1], reverse=True)}
    i = 0 
    for key in sorted_news_links:
        if (i > 10):
            break
        print(key + " : " +  str(sorted_news_links[key])) 
        i+=1
    """ 

if __name__ == "__main__":
    main()
