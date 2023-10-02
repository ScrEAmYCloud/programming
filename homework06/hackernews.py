from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session, update_label, load_fresh_news
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    label = request.query["label"]
    id = request.query["id"]
    update_label(session=s, id=id, label=label)
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    load_fresh_news(session=s)
    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    pass


if __name__ == "__main__":
    run(host="localhost", port=8080)

