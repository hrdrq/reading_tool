# -*- coding: utf-8 -*-

class Base(object):

    def __init__(self):
        pass

    @property
    def debug(self):
        import pdb
        return pdb.set_trace
