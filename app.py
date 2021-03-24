import flask
import lab_main
from flask import request, Flask, render_template, redirect, url_for

TEMPLATE_DIR = "web-content/templates"
app = Flask(__name__, template_folder=TEMPLATE_DIR)

def get_top_news():
    return lab_main.get_top_links_with_headers()

def get_top_news_with_random_texts(n_tweets, hours_back):
    return lab_main.get_top_links_with_random_texts(n_tweets, hours_back)

@app.route('/')
def index():
    return redirect(url_for('index_12h'))

@app.route('/12h')
def index_12h():
    top_news_with_texts = get_top_news_with_random_texts(5, 12)
    return render_template('index.html', posts=top_news_with_texts, hours_back = 12)


@app.route('/24h')
def index_24h():
    top_news_with_texts = get_top_news_with_random_texts(5, 24)
    return render_template('index.html', posts=top_news_with_texts, hours_back = 24)


@app.route('/7d')
def index_7d():
    top_news_with_texts = get_top_news_with_random_texts(5, 168)
    return render_template('index.html', posts=top_news_with_texts, hours_back = 168)
