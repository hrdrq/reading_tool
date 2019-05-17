# -*- coding: utf-8 -*-

import uuid
import json

from rt.base import Base

ARTICLES_JSON = 'articles.json'
ARTICLES_DIR = 'articles/'

def read_file(path):
    f = open(path)
    data = json.load(f)
    f.close()
    return data

class Article(Base):

    def __init__(self):
        pass

    def list(self):
        return read_file(ARTICLES_JSON)

    def item(self, id):
        return read_file(ARTICLES_DIR + str(id) + '.json')
