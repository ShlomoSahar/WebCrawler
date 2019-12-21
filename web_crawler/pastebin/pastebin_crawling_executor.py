#!/user/bin/env python
import os
import threading
import coloredlogs

from web_crawler.crawl import crawler
from web_crawler.pastebin import pastebin_content_handler
from web_crawler.utils import directory_watcher

"""
Since the new pastes are appears in the root page (pastebin.com) we need to crawler the first level of the site. as a result depth = 1
"""
CRAWLING_DEPTH = 1
RUNNING_INTERVAL = 120
SITE_TO_CRAWLING = "https://pastebin.com/"
WORKING_DIRECTORY = os.getcwd() + "/pastebin.com"


def start_periodic_crawling():
    crawler.start()
    threading.Timer(RUNNING_INTERVAL, start_periodic_crawling).start()


if __name__ == '__main__':
    coloredlogs.install(level='DEBUG', isatty=True)
    crawler = crawler.Crawl(SITE_TO_CRAWLING, CRAWLING_DEPTH)
    handler = pastebin_content_handler.PastebinCrawlerHandler()
    directory_watcher = directory_watcher.DirectoryWatcher(WORKING_DIRECTORY, handler)
    directory_watcher.start()
    start_periodic_crawling()
