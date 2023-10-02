from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session, update_label, load_fresh_news, extract_all_news_from_db
from bayes import NaiveBayesClassifier, prepare_data


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
    load_fresh_news(s)
    redirect("/news")


@route("/recommendations")
def recommendations():
    s = session()

    labeled_news = s.query(News).filter(News.label != None).all()
    unlabeled_news = s.query(News).filter(News.label == None).all()
    model = NaiveBayesClassifier()

    X: tp.List[str] = []
    y: tp.List[str] = []

    for article in labeled_news:
        X.append(article.title)
        y.append(article.label)

    model.fit(X, y)

    for article in unlabeled_news:
        prediction = model.predict(article.title)
        article.prediction = prediction

    s.commit()

    news = extract_all_news_from_db(s)
    return template("news_template_recommendations", rows=news, more_button=False, label=False)


if __name__ == "__main__":
    run(host="localhost", port=8080)

