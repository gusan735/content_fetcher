<h1>Introduction</h1>
Some hacky python-code for playing with the Twitter API/Swedish police API and analyzing data I'm interested in.

<h2>Description</h2>
The foundatation are a couple of python scripts that grew organically on my laptop, that I later threw together into a web project. The overall vision is to gather and aggregate content from a lot of sources I'm interested in (e.g. Twitter, Youtube, Police events) and then creating a web interface which makes it easy to search and analyze the data, so I don't have to browse around the web manually and do it the old boring way.

The code is really hacky and quite experimentative, would definately benefit from more OOP concepts, structure and cleanup. This is more of a playground to test ideas :)

<h2>The algorithm</h2>
1. According to a schedule, gather data from the following sources:

*  Twitter REST-API: <b>tweet_fetcher.py</b>.

*  Open data from polisen.se (reported police events: <b>fetch_events.py</b>.
  
2. Scheduling, import and processing of data hare handled in <b>lab_main.py</b>. It also uses <b>web_scraper.py</b> to gather complementary data which are not available in the REST-APIs..

3. Data are saved in a couple of ad hoc-generated tables in a SQLite-fil e(<b>project.db</b>)

4. Content are presented to users in html/css with the help of alask-hostad web service (<b>app.py</b>).

<h2>Screens</h2>
<img width="1427" alt="Screenshot 2021-05-20 at 05 09 09" src="https://user-images.githubusercontent.com/38020265/118919780-79a20a80-b935-11eb-924c-7d669b265e53.png">
<img width="826" alt="Screenshot 2021-05-20 at 05 08 38" src="https://user-images.githubusercontent.com/38020265/118919784-7c9cfb00-b935-11eb-9ece-0e9cc618da03.png">
<img width="1435" alt="Screenshot 2021-05-20 at 00 20 25" src="https://user-images.githubusercontent.com/38020265/118919945-bc63e280-b935-11eb-9488-af41bc15bf00.png">
<img width="1436" alt="Screenshot 2021-05-20 at 00 21 05" src="https://user-images.githubusercontent.com/38020265/118919951-bf5ed300-b935-11eb-9144-fc4c94794638.png">


