# -*- coding: utf-8 -*-

import argparse
from os import listdir

class Convert():

    def __init__(self, source_path, output_path):
        self.source_path = source_path
        self.output_path = output_path
        self.read_lang()

    def read_lang(self):
        file_list = [f for f in listdir(self.source_path) if not f.startswith('.')]
        self.langs = file_list

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source_path')
    parser.add_argument('output_path')

    args = parser.parse_args()
    Convert(args.source_path, args.output_path)
