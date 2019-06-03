# -*- coding: utf-8 -*-

import uuid
import json

from rt.base import Base
from rt.config import get_path

ARTICLES_JSON = 'articles.json'
ARTICLES_DIR = 'articles/'

def read_file(path):
    with open(get_path(path)) as f:
        data = json.load(f)
    return data

def write_file(path, data):
    with open(get_path(path), 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

class Article(Base):

    def __init__(self):
        self._list = read_file(ARTICLES_JSON)

    def list(self):
        return self._list

    def item(self, id):
        file = ARTICLES_DIR + str(id) + '.json'
        return read_file(file), file

    def add(self, title):
        id = title.replace(' ', '_')
        self._list.append(dict(title=title, id=id))
        write_file(ARTICLES_JSON, self._list)
        empty_file = dict(
            audio='',
            article=[[dict(text='', start=0, end=0)]]
        )
        write_file('{}{}.json'.format(ARTICLES_DIR, id), empty_file)
        return id, self._list
