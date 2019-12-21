import logging
import os
from tinydb import TinyDB

from web_crawler.utils.utilities import create_directory_if_needed


class PastesDatabase:

    def __init__(self):
        create_directory_if_needed(os.getcwd() + '/db', logging.getLogger('pastesDatabase'))
        self.db = TinyDB(os.getcwd() + '/db/pastes.json')

    def insert(self, paste_model):
        self.db.insert({'Author': paste_model.Author, 'Title': paste_model.Title, 'Content': paste_model.Content,
                        'Date': paste_model.Date})
