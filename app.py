import flask
import lab_main
from flask import request, Flask, render_template

TEMPLATE_DIR = "web-content/templates"
app = Flask(__name__, template_folder=TEMPLATE_DIR)

def get_top_news():
    return lab_main.get_top_links_with_headers()

@app.route('/')
def index():
    top_news = get_top_news()
    return render_template('index.html', posts=top_news)

