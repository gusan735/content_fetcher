import os
import sys
src_path = os.path.dirname(os.path.realpath(__file__))
project_path = os.path.dirname(src_path)
sys.path.append(project_path)
db_path = os.path.join(src_path, "project.db")
import sqlite3
import web_scraper
import csv
import json 

#VARS
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
    event_to_add = (event['id'], event['name'], event['summary'], event['type'], event['datetime'], event['location']['gps'], event['location']['name'], event['url']);
    sql = ''' INSERT INTO police_events(Id,Name,Summary,Type,Datetime,Gps,Location, Link)
              VALUES(?,?,?,?,?,?,?, ?) '''
    cur = conn.cursor()
    try:
        cur.execute(sql, event_to_add)
    except sqlite3.IntegrityError:
        return cur.lastrowid
    conn.commit()
    return cur.lastrowid

def update_police_event(event):
    conn = create_connection(db_path)
    event_to_update =  event
    sql = ''' UPDATE police_events 
            SET Name = {}, Summary = {}, Type = {}, Datetime = {}, Gps = {}, Location = {}, Link = {}, 
            WHERE Id = {}
        '''.format(event['name'], event['summary'], event['type'], event['datetime'], event['location']['gps'], event['location']['name'], event['url'], event['id']);
    cur = conn.cursor()
    cur.execute(sql, event_to_add)
    cur.commit()
    return cur.lastrowid




def create_news_tweet(tweet_id, news_tweet):
    tweet_text = news_tweet["text"]
    author_id = news_tweet["author_id"]
    created_at = news_tweet["created_at"]
    urls = news_tweet["urls"]

    i = 1
    for url in urls:
        conn = create_connection(db_path)
        fields_to_add = (tweet_id + "_"+str(i), tweet_text, author_id, created_at, url, url);
        sql = ''' INSERT INTO news_tweets(Id,Tweet_text,Author_id,Tweet_time,Link, header)
                VALUES(?,?,?,?,?,?) '''
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

def fetch_top_news_tweets_from_db(hours_back, amount):
    sql = ("""SELECT Link, Tweet_text, Author_id, Tweet_time
            FROM news_tweets
            WHERE Link in 
	        (SELECT Link
            FROM news_tweets
            WHERE datetime(Tweet_time) > datetime('now', '-{} hour')
            GROUP BY Link
            ORDER BY COUNT(DISTINCT Author_id) DESC
	        LIMIT {})""").format(hours_back, amount);
    
    conn = create_connection(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(sql)
    rows = [dict(row) for row in cur.fetchall()]
    return rows

def update_police_event(event):
    conn = create_connection(db_path)
    event_to_update = event
    sql = ''' UPDATE police_events 
            SET Name = {}, Summary = {}, Type = {}, Datetime = {}, Gps = {}, Location = {}, Link = {}
            WHERE Id = {}
        '''.format(event['name'], event['summary'], event['type'], event['datetime'], event['location']['gps'], event['location']['name'], event['url'], event['id']);
    cur = conn.cursor()
    cur.execute(sql, event_to_add)
    cur.commit()
    return cur.lastrowid




#Fetches the tweet objects that includes the mest popular news from hours_back in time.
#Does not allow duplicate author_id and link.
def fetch_interesting_crimes_from_db(days_back, limit):
    #BILBRÄNDER
    sql = ("""SELECT * FROM police_events
    WHERE (Summary LIKE '%Bilbrand%') OR (Summary LIKE '% Bil %' AND  Summary LIKE  '%Brand%')  
    AND datetime(Datetime) > datetime('now', '-{} day')""".format(days_back)
    +
    #RÅN
    """
    UNION
    SELECT *FROM police_events
    WHERE (Type = 'Rån' )
    AND datetime(Datetime) > datetime('now', '-{} day')""".format(days_back)
    +
    #BOMBER OCH SPRÄNGNINGAR
    """
    UNION
    SELECT * FROM police_events
    WHERE (Summary = 'bomb' OR Summary LIKE '%spräng%' OR Summary LIKE '%deton%' OR Type LIKE '%Detonation%')
    AND datetime(Datetime) > datetime('now', '-{} day')""".format(days_back)
    +
    #SKOTTLOSSNINGAR
    """
    UNION
    SELECT * FROM police_events
    WHERE ((Type LIKE '%Skottlo%') OR (Summary LIKE '%skott%' AND Summary NOT LIKE '%skotta%' ) OR (Summary LIKE '%skjut%' ))
    AND datetime(Datetime) > datetime('now', '-{} day')
    """.format(days_back)
    +
    ###VÅLDTÄKTER 
    """
    UNION
    SELECT * FROM police_events
    WHERE (Type LIKE '%Våldtäkt%' OR (Summary LIKE '%våldtäkt%' OR Details LIKE '%våldtäkt%'))
    AND datetime(Datetime) > datetime('now', '-{} day')""".format(days_back)
    +
    """
    ORDER BY Datetime desc
    LIMIT {}
""").format( limit);
    
    conn = create_connection(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(sql)
    rows = [dict(row) for row in cur.fetchall()]
    return rows

def fetch_police_details_in_db():
    sql = """ SELECT * FROM police_events
            WHERE Link IS NOT NULL
            AND Details IS NULL """
    conn = create_connection(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(sql)
    rows = [dict(row) for row in cur.fetchall()]
    for row in rows:
        details = web_scraper.get_police_details(row['Link'])
        print("Trying Id: " + str(row['Id']))
        update_sql = '''UPDATE police_events
                        SET Details = '{}'
                        WHERE Id = {}'''.format(str(details), row['Id'])
        conn = create_connection(db_path)
        cur = conn.cursor()
        cur.execute(update_sql)
        conn.commit()


#Fetches the tweet counts for the most popular news from hours_back in time.
#Does not allow duplicate author_id and link.
def fetch_top_news_count_from_db(hours_back, amount):
    sql = ("""SELECT Link, header, COUNT(DISTINCT Author_id) as Count
    FROM news_tweets
    WHERE datetime(Tweet_time) > datetime('now', '-{} hour')
    GROUP BY Link
    ORDER BY COUNT(DISTINCT Author_id) DESC
    LIMIT {}""").format(hours_back, amount);
    
    conn = create_connection(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(sql)
    rows = [dict(row) for row in cur.fetchall()]
    return rows

