import requests

cache = dict()

def extract_article_content(url):
    response = requests.get(url)
    content = response.content
    return content

def fetch_article(url):
    if url not in cache:
        content = extract_article_content(url)
        cache[url] = content
    return cache[url]
