# -*- coding: utf-8 -*-

import os

def root():
    return os.path.expanduser('~/reading_tool_files/')

def get_path(relative_path):
    return root() + relative_path
