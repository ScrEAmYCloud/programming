from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scraputils import get_news
import typing as tp

Base = declarative_base()   
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)

Base.metadata.create_all(bind=engine)

def make_news_from_tag(dictoanary: dict) -> "News":
    temp_news = News(
            title = dictoanary["title"],
            author = dictoanary["author"],
            url = dictoanary['url'],
            comments = dictoanary['comments'],
            points = dictoanary['points'],
        )
    return temp_news

RawNewsList = tp.List[tp.Dict[str, tp.Union[int, str]]]

def add_news(session: session, raw_news_list: RawNewsList) -> None:
    news = [News(**news_data) for news_data in raw_news_list]
    session.add_all(news)
    session.commit()

def update_label(session: session, id: int, label: str) -> None:
    entry = session.query(News).get(id)
    if entry is not None:
        entry.label = label
        session.commit()

def load_fresh_news(session: session, url: str = "https://news.ycombinator.com/newest") -> None:
    fresh_news: RawNewsList = []
    news = get_news(url, n_pages=1)
    for item in news:
        title, author = item["title"], item["author"]
        exists = list(session.query(News).filter(News.title == title, News.author == author))
        if not exists:
            fresh_news.append(item)
    if fresh_news:
        add_news(session=session, raw_news_list=fresh_news)