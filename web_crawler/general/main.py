#!/user/bin/env python
import argparse
import coloredlogs
from web_crawler.crawl import crawler

if __name__ == '__main__':
    coloredlogs.install(level='DEBUG', isatty=True)
    parser = argparse.ArgumentParser(description='web crawler')
    parser.add_argument('-u', '--url', help="URL to start crawling from", required=True)
    parser.add_argument('-d', '--depth', help="Crawling depth",required=True, type=int)
    args = parser.parse_args()
    crawler = crawler.Crawl(args.url, args.depth)
    crawler.start()
