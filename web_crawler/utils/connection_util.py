import magic
import requests
from requests_html import HTMLSession


def get_page(url):
    page = requests.get(url).content.decode('utf-8')
    return page


def is_html(file):
    type = magic.from_file(file, mime=True)
    return type in 'text/html'


def get_all_page_links(url):
    all_page_links = HTMLSession().get(url).html.absolute_links
    return all_page_links
