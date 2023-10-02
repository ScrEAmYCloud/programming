import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    articles = parser.table.find_all('tr', class_='athing')
    subtexts = parser.table.find_all('td', class_='subtext')

    for number in range(len(articles)):
        author = subtexts[number].find('a', class_='hnuser')
        if (author == None):
            author = ""
        else:
            author = author.text

        title = articles[number].find('span', class_='titleline').find_next("a").text
        
        points = subtexts[number].find('span', class_='score')
        if (points != None):
            points = int(points.text.split()[0])    
        else:
            points = 0
        
        url = articles[number].find('span', class_='sitebit comhead')
        if (url == None):
            url = ""
        else:
            url = url.find_next('a').text

        comments = subtexts[number].find('span', class_='subline')
        if(comments != None):
            comments = comments.find_all('a')
            if(comments != None):
                comments = comments[-1]
                if comments.text == 'discuss':
                    comments = 0
                else:
                    comments = int(comments.text.split()[0])
        if(comments == None):
            comments = 0

        news_list.append({
            "author": author, 
            "title": title, 
            "points": points, 
            'url': url,
            'comments': comments
            })

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    link = parser.find('a', class_="morelink")["href"]
    if link is None:
        raise Exception("Parsed all news")
    return str(link[link.index("?") :])


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news