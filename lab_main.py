import requests
import os
import time
import schedule
import configparser
import json
import random
from datetime import datetime, timedelta
import web_scraper
from resources import db_broker
import tweet_fetcher


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
def print_links(links_with_headers):
    counter = 0
    for obj in links_with_headers:
        #Bad links doesnt count!
        print(str(counter + 1) + ": " + obj["header"] + " : " + obj["link"] + " : " + str(obj["count"]))
        print ("----------------------")
        counter +=1

def add_headers_to_links(sorted_news_links, amount):
    #TODO: Remove duplicate links
    output = []
    counter = 1
    for obj in list(sorted_news_links):
        link = obj["Link"]
        count = obj["Count"]
        if (counter > amount):
            break
        header = web_scraper.get_article_heading(link)
        link_count_with_header = {}
        link_count_with_header["header"] = header
        link_count_with_header["link"] = link
        link_count_with_header["count"] = count
        output.append(link_count_with_header)
        counter+=1
    return output

#Adding top n tweets of the given period to DB

def add_links_to_db(n, news_links, sorted_link_counts):
    counter = 0
    #Adding only top n tweets to db
    for link in sorted_link_counts:
        if counter > n:
            break
        for id in news_links:
            for url in news_links[id]["urls"]:
                if (url == link):
                    db_broker.create_news_tweet(id, news_links[id])
        counter += 1

def count_links(link_dicts):
    link_counts = {}

    for id in link_dicts:
        for url in link_dicts[id]["urls"]:
            if (url not in link_counts):
                link_counts[url] = 1
            else:
                link_counts[url] +=1
    return link_counts

def print_random_tweets(n_tweets, link_tweets_with_texts):
    #Loop thrugh each value link link_texts and print n random tweets frorm it
    i = 1
    for link in link_tweets_with_texts:
        texts = link_tweets_with_texts[link]["texts"]
        header = link_tweets_with_texts[link]["header"]
        print("------------")
        print ("\n" + str(i) +": "+ header +": " + link)

        random_tweets = random.sample(texts, n_tweets)
        for tweet in random_tweets:
            if (len(tweet) > 5):
                print ("---------")
                print(tweet)
        i += 1


def add_texts_to_links_2(link_counts, link_tweets):
    #Create a link dict with texts added for each link:
    link_outputs = {}
    for obj1 in link_counts:
        header_link = obj1["Link"]
        header= obj1["header"]
        count = obj1["Count"]
        texts = []
        link_outputs[header_link] = {}
        for obj2 in link_tweets:
            tweet_link = obj2["Link"]
            tweet_text = obj2["Tweet_text"]
            if header_link == tweet_link:
                tweet_link = obj2["Link"]
                tweet_text = obj2["Tweet_text"]
                altered_text = ' '.join(word for word in tweet_text.split(' ') if not word.startswith('http')).split("http")[0]
                if header not in altered_text and len(altered_text) > 2:
                    texts.append(altered_text)
        link_outputs[header_link]["texts"] = texts
        link_outputs[header_link]["header"] = header
        link_outputs[header_link]["count"] = count
    return link_outputs

def fetch_links_to_db():
    news_links = tweet_fetcher.fetch_news_tweets()
    print("LINKS PROCESSED TO DICT")
    link_counts = count_links(news_links)
    sorted_link_counts= {k: v for k, v in sorted(link_counts.items(), key=lambda item: item[1], reverse=True)}
    add_links_to_db(N_LINKS_TO_DB, news_links, sorted_link_counts)
    headers = get_top_links_with_headers()
    add_headers_to_db(headers)
    print("LINKS ADDED TO DB WITH HEADERS")

def get_top_links_with_headers():
   # link_tweets = db_broker.fetch_top_news_tweets_from_db(hours_back=12, amount=10)
    link_counts = db_broker.fetch_top_news_count_from_db(hours_back=12, amount=N_LINKS_TO_DB)
    link_counts_with_headers = add_headers_to_links(link_counts, N_LINKS_TO_DB)
    return link_counts_with_headers

def add_headers_to_db(links_with_headers):
    for link in links_with_headers:
        db_broker.add_headers_to_news_tweet(link)

def get_top_links_with_random_texts(n_tweets, hours_back):
    link_tweets = db_broker.fetch_top_news_tweets_from_db(hours_back=hours_back, amount=N_LINKS_TO_PRINT)
    link_counts = db_broker.fetch_top_news_count_from_db(hours_back=hours_back, amount=N_LINKS_TO_PRINT)
    links_with_texts = add_texts_to_links_2(link_counts, link_tweets)

    output = []

    for link in links_with_texts:
        sample_size = n_tweets
        if (sample_size > len(links_with_texts[link]["texts"])):
            sample_size = len(links_with_texts[link]["texts"])
        new_dict = {}
        new_dict["link"] = link
        new_dict["header"] = links_with_texts[link]["header"]
        new_dict["texts"] = []
        new_dict["count"] = links_with_texts[link]["count"]
        random_tweets = random.sample(links_with_texts[link]["texts"], sample_size)
        new_dict["texts"] = random_tweets
        output.append(new_dict) 
    return output

def main():
    #TODO: Clean this shit up...
    #schedule.every(20).minutes.do(fetch_links_to_db)
    #while True:
    #    schedule.run_pending()
    fetch_links_to_db()
    #link_tweets = db_broker.fetch_top_news_tweets_from_db(hours_back=12, amount=20)
    #top_tweets_with_headers = get_top_links_with_headers()
    #link_counts_with_headers_and_texts = add_texts_to_links(top_tweets_with_headers, link_tweets)
    #print_links(top_tweets_with_headers)
   # print_random_tweets(10, link_counts_with_headers_and_texts)
    

if __name__ == "__main__":
    main()
