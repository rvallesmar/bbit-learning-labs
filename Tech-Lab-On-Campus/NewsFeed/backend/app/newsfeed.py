"""Module for retrieving newsfeed information."""

from dataclasses import dataclass
from datetime import datetime
from app.utils.redis import REDIS_CLIENT
from operator import attrgetter


@dataclass
class Article:
    """Dataclass for an article."""

    author: str
    title: str
    body: str
    publish_date: datetime
    image_url: str
    url: str


def get_all_news() -> list[Article]:
    """Get all news articles from the datastore."""
    # 1. Use Redis client to fetch all articles
    # 2. Format the data into articles
    # 3. Return the as a list of articles sorted by most recent
    full_articles = REDIS_CLIENT.get_entry('all_articles')
    final_lst = []

    for article in full_articles:
        final_lst.append(__turn_to_article(article))
    
    return final_lst


def get_featured_news() -> Article | None:
    """Get the featured news article from the datastore."""
    # 1. Get all the articles
    # 2. Select and return the featured article
    return sorted(get_all_news(), key= attrgetter('publish_date'), reverse=True)

def __turn_to_article(data):
    return Article(author=data['author'],
                   title=data['title'],
                   body=data['text'],
                   publish_date= datetime.fromisoformat(data['published']),
                   image_url=data['thread']['main_image'],
                   url=data['url'])
