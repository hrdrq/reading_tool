# -*- coding: utf-8 -*-

import os

def root():
    root = os.path.expanduser('~/reading_tool_files')
    try:
        return os.readlink(root)
    except:
        return root

def get_path(relative_path):
    return root() + relative_path
