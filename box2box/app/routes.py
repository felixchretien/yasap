import json
from flask import render_template

from box2box.app import app

with open('box2box/textes/a_propos.txt', 'r') as reader:
    texte_a_propos = reader.readlines()

with open('box2box/textes/articles.json') as reader:
    articles_json = json.load(reader)


@app.route('/')
def index():
    return render_template("home.html", title='Home', active="home", last_article_route="/articles/atalanta-montreal",
                           last_article=articles_json['atalanta-montreal'])

@app.route('/articles')
def articles():
    return render_template("articles.html", title='Articles', active="articles", articles_json=articles_json)


@app.route('/a-propos')
def a_propos():
    return render_template("a_propos.html", title='À propos', active="a_propos", texte_a_propos=texte_a_propos)


@app.route('/articles/atalanta-montreal')
def articles_atalanta_montreal():
    return render_template("articles/atalanta_montreal.html", active="articles", current_article=articles_json['atalanta-montreal'])
