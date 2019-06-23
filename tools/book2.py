# -*- coding: utf-8 -*-

import argparse
import os
import csv
import json
import shutil

class Convert():

    def __init__(self, source_path, output_path):
        self.source_path = source_path
        self.output_path = output_path
        self.read_lang()
        self.read_csv()
        self.write_json()

    def read_lang(self):
        file_list = [f for f in os.listdir(self.source_path) if not f.startswith('.')]
        self.langs = file_list

    def read_csv(self):
        self.titles = []
        self.contents = []
        for i in range(1, 101):
            title = None
            id = None
            csv_files = []
            for lang in self.langs:
                dir = os.path.join(self.source_path, '{}/{}'.format(lang, i))
                csv_file = [f for f in os.listdir(dir) if f.endswith('.csv')][0]
                csv_files.append(os.path.join(dir, csv_file))
                if not title:
                    title = str(i) + os.path.splitext(csv_file)[0]
                    id = 'book2/' + str(i)
                    self.titles.append(dict(title=title, id=id))
                self.copy_file(os.path.join(dir, 'audio'), lang)

            sentences = []
            for row in zip(*(self.csv_file_to_row(csv_file) for csv_file in csv_files)):
                sentence = [dict(text=lang_row[1], audio="book2/{}/{}".format(self.langs[index], lang_row[2])) for (index, lang_row) in enumerate(row)]
                sentences.append(sentence)
            self.contents.append((i, sentences))

    def write_json(self):
        articles_csv = os.path.join(self.output_path, "articles.json")
        with open(articles_csv, 'w') as f:
            json.dump(dict(title='book2', children=self.titles), f, indent=2, ensure_ascii=False)

        for i, content in self.contents:
            dir = os.path.join(self.output_path, 'articles')
            if not os.path.exists(dir):
                os.makedirs(dir)
            file = os.path.join(dir, '{}.json'.format(i))
            with open(file, 'w') as f:
                json.dump(dict(audio=False, article=content), f, indent=2, ensure_ascii=False)

    def csv_file_to_row(self, path):
        with open(path) as f:
            reader = csv.reader(f)
            l = [row for row in reader]
        return l

    def copy_file(self, source_dir, lang):
        destination_dir = os.path.join(self.output_path, 'book2/' + lang)
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        for item in os.listdir(source_dir):
            s = os.path.join(source_dir, item)
            d = os.path.join(destination_dir, item)
            shutil.copy2(s, d)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source_path')
    parser.add_argument('output_path')

    args = parser.parse_args()
    Convert(args.source_path, args.output_path)
