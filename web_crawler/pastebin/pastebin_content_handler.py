import logging
from bs4 import BeautifulSoup
from web_crawler.pastebin import paste_model
from web_crawler.pastebin.db import pastes_db

from web_crawler.utils.utilities import convert_str_time_to_utc, read_file_content


class PastebinCrawlerHandler:

    def __init__(self):
        self.created = 'created'
        self.modified = 'modified'
        self.title_class_name = 'paste_box_line1'
        self.author_and_date_class_name = 'paste_box_line2'
        self.content_id = 'paste_code'
        self.user_index = 1
        self.db = pastes_db.PastesDatabase()
        self.logger = logging.getLogger('pastebinContentHandlerLogger')

    def handle(self, file_path, event_type, is_directory):
        if self.should_process_event(event_type, is_directory):
            self.parse_file(file_path)

    def should_process_event(self, event_type, is_directory):
        return is_directory == False and (event_type == self.created or event_type == self.modified)

    def parse_file(self, file_path):
        self.logger.debug(f"Got file [{file_path}]. start processing")
        html = read_file_content(file_path)
        parsed_html = BeautifulSoup(html, 'lxml')
        if not self.is_not_paste(parsed_html):
            self.logger.debug(f"[{file_path}] is not a paste")
            return
        author = self.parse_author(parsed_html)
        title = self.parse_title(parsed_html)
        content = self.parse_content(parsed_html)
        utc_date = self.parse_and_convert_to_utc_time(parsed_html)
        model = paste_model.PasteModel(author, title, content, utc_date.__str__())
        self.db.insert(model)

    def parse_author(self, parsed_html):
        details = parsed_html.body.find('div', attrs={'class': self.author_and_date_class_name}).text.split('\n')
        normalized_author = details[self.user_index].rstrip().lstrip()
        return normalized_author

    def parse_utc_time(self, parsed_html):
        time = parsed_html.body.find('div', attrs={'class': self.author_and_date_class_name})
        res = time.find('span')
        date = res['title']
        return date

    def parse_title(self, parsed_html):
        return parsed_html.body.find('div', attrs={'class': self.title_class_name}).text

    def parse_content(self, parsed_html):
        content = parsed_html.body.find('textarea', attrs={'id': self.content_id}).text
        content_stripped_spaces = ""
        for line in content.splitlines():
            content_stripped_spaces += (line.strip() + "\n")
        return content_stripped_spaces

    def parse_and_convert_to_utc_time(self, parsed_html):
        date = self.parse_utc_time(parsed_html)
        utc_time = convert_str_time_to_utc(date)
        return utc_time

    def is_not_paste(self, parsed_html):
        return parsed_html.body.find('div', attrs={'class': self.title_class_name}) and parsed_html.body.find('div',
                                                                                                              attrs={
                                                                                                                  'class': self.author_and_date_class_name})
