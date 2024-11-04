import requests
import re

def fetch_html(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def get_articles_from_source(source, num):
    regexp = r'<a href="(\/wiki\/.*?)".*?title="(.*?)"'

    links, titles = [], []
    for match in re.finditer(regexp, source):
        if ":" in match.group(1):  # wrong namespace
            continue

        links.append(match.group(1))
        titles.append(match.group(2))
        if len(links) == num:
            return links, titles
    return links, titles

def get_images_from_source(source, num):
    regexp = r'<img.*src="(\/\/upload\.wikimedia\.org.*?)"'

    urls = []
    for match in re.finditer(regexp, source):
        urls.append(match.group(1))
        if len(urls) == num:
            return urls
    return urls

def get_external_source_urls(source, num):
    srcs = re.search(r'<h2 id="Przypisy">(.*)<h2 id="Linki_zewnętrzne">', source, re.DOTALL | re.MULTILINE)
    if srcs is not None:
        srcs = srcs.group(1)
    else: return []

    regexp = r'class="external text".*?href="(.*?)">'
    urls = []
    for match in re.finditer(regexp, srcs):
        urls.append(match.group(1))
        if len(urls) == num:
            return urls
    return urls

def get_cat_names(source, num):
    catlinks =  re.search(r'<div id="catlinks".*', source, re.DOTALL | re.MULTILINE)
    if catlinks is not None:
        catlinks = catlinks.group()
    else: return []

    regexp = r'<a href="\/wiki\/Kategoria:.*?title="Kategoria:(.*?)">'
    names = []
    for match in re.finditer(regexp, catlinks):
        names.append(match.group(1))
        if len(names) == num:
            return names
    return names

def print_info_from_article(article_src):
    _, titles = get_articles_from_source(article_src, 5)
    img_urls = get_images_from_source(article_src, 3)
    exts = get_external_source_urls(source, 3)
    cats = get_cat_names(article_src, 3)

    print(" | ".join(titles))
    print(" | ".join(img_urls))
    print(" | ".join(exts))
    print(" | ".join(cats))


category = input().strip()
url = f"https://pl.wikipedia.org/wiki/Kategoria:{category}"
cat_page = fetch_html(url)
cat_page_mw_pages_div = re.search(r'<div id="mw-pages">.*', cat_page, re.DOTALL | re.MULTILINE).group()
top_urls, top_titles = get_articles_from_source(cat_page_mw_pages_div, 2)

for url in top_urls:
    source = fetch_html(f"https://pl.wikipedia.org{url}")
    source = re.search(r'class="mw-body-content".*', source, re.DOTALL | re.MULTILINE).group()
    print_info_from_article(source)
