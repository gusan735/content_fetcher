import sqlite3
import os
import csv
import json 
#VARS
src_path = os.path.dirname(os.path.realpath(__file__))
db_path = os.path.join(src_path, "project.db")

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e) 
    return conn

def write_data_to_csv():
    with sqlite3.connect(db_path) as connection:
        csvWriter = csv.writer(open(os.path.join(src_path, "all_events.csv"), "w"))
        c = connection.cursor()
        c.execute("SELECT * FROM police_events")
        rows = c.fetchall()
        csvWriter.writerows(rows)


def create_police_event(event):
    conn = create_connection(db_path)
    event_to_add = (event['id'], event['name'], event['summary'], event['type'], event['datetime'], event['location']['gps'], event['location']['name']);
    sql = ''' INSERT INTO police_events(Id,Name,Summary,Type,Datetime,Gps,Location)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    try:
        cur.execute(sql, event_to_add)
    except sqlite3.IntegrityError:
        return cur.lastrowid
    conn.commit()
    return cur.lastrowid

def create_police_event(event):
    conn = create_connection(db_path)
    event_to_add = (event['id'], event['name'], event['summary'], event['type'], event['datetime'], event['location']['gps'], event['location']['name']);
    sql = ''' INSERT INTO police_events(Id,Name,Summary,Type,Datetime,Gps,Location)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    try:
        cur.execute(sql, event_to_add)
    except sqlite3.IntegrityError:
        return cur.lastrowid
    conn.commit()
    return cur.lastrowid

def create_news_tweet(tweet_id, news_tweet):
    tweet_text = news_tweet["text"]
    author_id = news_tweet["author_id"]
    created_at = news_tweet["created_at"]
    urls = news_tweet["urls"]

    i = 1
    for url in urls:
        conn = create_connection(db_path)
        fields_to_add = (tweet_id + "_"+str(i), tweet_text, author_id, created_at, url);
        sql = ''' INSERT INTO news_tweets(Id,Tweet_text,Author_id,Tweet_time,Link)
                VALUES(?,?,?,?,?) '''
        i+=1
        cur = conn.cursor()
        try:
            cur.execute(sql, fields_to_add)
        except sqlite3.IntegrityError:
            return False
        conn.commit()
    return True


def add_headers_to_news_tweet(link_with_header):
    header = link_with_header["header"]
    link = link_with_header["link"]
    fields_to_add = (header, link);
    sql = """UPDATE news_tweets
            SET header = ?
            WHERE Link = ?
            """

    conn = create_connection(db_path)
    cur = conn.cursor()
    cur.execute(sql, fields_to_add)
    conn.commit()

"""
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
"""


#Fetches the tweet objects that includes the mest popular news from hours_back in time.
#Does not allow duplicate author_id and link.
def fetch_top_news_tweets_from_db(hours_back, amount):
    sql = ("""SELECT Link, Tweet_text, Author_id, Tweet_time
            FROM news_tweets
            WHERE Link in 
	        (SELECT Link
            FROM news_tweets
            WHERE Tweet_time > datetime('now', '-{} hour')
            GROUP BY Link
            ORDER BY COUNT(DISTINCT Author_id) DESC
	        LIMIT {})""").format(hours_back, amount);
    
    conn = create_connection(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(sql)
    rows = [dict(row) for row in cur.fetchall()]
    return rows

#Fetches the tweet counts for the most popular news from hours_back in time.
#Does not allow duplicate author_id and link.
def fetch_top_news_count_from_db(hours_back, amount):
    sql = ("""SELECT Link, header, COUNT(DISTINCT Author_id) as Count
    FROM news_tweets
    WHERE Tweet_time > datetime('now', '-{} hour')
    GROUP BY Link
    ORDER BY COUNT(DISTINCT Author_id) DESC
    LIMIT {}""").format(hours_back, amount);
    
    conn = create_connection(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(sql)
    rows = [dict(row) for row in cur.fetchall()]
    return rows
