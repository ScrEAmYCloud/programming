from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scraputils import get_news

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