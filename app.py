import flask
import lab_main
from flask import request, Flask, render_template

TEMPLATE_DIR = "web-content/templates"
app = Flask(__name__, template_folder=TEMPLATE_DIR)

def get_top_news():
    return lab_main.get_top_links_with_headers()

def get_top_news_with_random_texts(n_tweets=5):
    return lab_main.get_top_links_with_random_texts(n_tweets)

@app.route('/')
def index():
    top_news_with_texts = get_top_news_with_random_texts()
    return render_template('index.html', posts=top_news_with_texts)

