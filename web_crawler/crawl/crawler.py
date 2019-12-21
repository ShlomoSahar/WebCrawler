import concurrent.futures
import os
import time
import string
import unicodedata
import logging
from web_crawler.utils import utilities, connection_util, hash_map
from urllib.parse import urlparse


class Crawl:

    def __init__(self, url, depth):
        self.root_url = url
        self.depth = depth
        self.logger = logging.getLogger('crawlLogger')
        self.validate_depth()
        self.root_dir = self.get_root_directory()
        self.url_cache = hash_map.HashMap()

    def validate_depth(self):
        if self.depth <= 0:
            self.logger.error(f"Depth must be positive int value")
            exit(1)

    def start(self):
        start_time = round(time.time(), 3)
        self.logger.info(
            f"Starting crawl url [{self.root_url}], required depth [{self.depth}]. start time [{time.strftime('%X %x %z')}]")
        root_page_file = self.get_page_file_name(self.root_url)
        if not connection_util.is_html(os.path.join(self.root_dir, root_page_file)):
            self.logger.error(f"Root URL {self.root_url} is not of type 'text/html', stop processing")
            exit(1)
        self.start_crawling(self.root_url, self.depth)
        end_time = time.time()
        running_time = round(end_time - start_time, 3)
        self.logger.info(f"End crawling. URL [{self.root_url}], depth [{self.depth}]. running time [{running_time}]")

    def start_crawling(self, url, depth):
        height = int(depth)
        is_root = url is self.root_url
        if not is_root:
            url_key = f"{self.root_dir}:{self.create_file_name(url)}"
            if self.url_in_cache(url_key):
                self.logger.debug(f"URL [{url}] has been already processed, details are cached.")
            else:
                file_name = self.get_page_file_name(url)
                self.write_to_cache(url_key, url)

            if not connection_util.is_html(os.path.join(self.root_url, file_name)):
                self.logger.debug(f"URL [{url}] is not type 'text/html'")
                return

        if height > 0:
            current_depth = self.depth - depth
            self.logger.debug(f"Processing URL [{url}] at depth [{current_depth}]")
            all_page_links = connection_util.get_all_page_links(url)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_to_url = {executor.submit(self.start_crawling, link, height - 1): link for link in
                                 all_page_links}
                for _ in concurrent.futures.as_completed(future_to_url):
                    self.logger.debug(f"Thread finished")

    def get_page_file_name(self, url):
        url_file_name = self.create_file_name(url)
        file = os.path.join(self.root_dir, url_file_name)
        content = connection_util.get_page(url)
        if not os.path.isfile(file):
            with open(file, "w") as contentFile:
                contentFile.write(content)
                self.logger.debug(f"File [{url_file_name}] created successfully")
        else:
            self.logger.debug(f"File [{url_file_name}] already exists")
        return url_file_name

    def create_file_name(self, url):
        whitelist = "-_.() %s%s" % (string.ascii_letters, string.digits)
        char_limit = 255
        replace = ' '
        for r in replace:
            filename = url.replace(r, '_')
        cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
        cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
        return cleaned_filename[:char_limit]

    def get_root_directory(self):
        parsed_url = urlparse(self.root_url)
        directory_name = parsed_url.netloc
        utilities.create_directory_if_needed(directory_name, self.logger)
        return directory_name

    def url_in_cache(self, key):
        return self.url_cache.contains_key(key)

    def write_to_cache(self, key, url):
        self.url_cache.put(key, url)
