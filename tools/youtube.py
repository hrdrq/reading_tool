# -*- coding: utf-8 -*-

import argparse
import json
import os
import xml.etree.ElementTree as ET

END_OFFSET = 10
S_TO_MS = 1000

class Convert():

    def __init__(self, source_file, output_file):
        self.source_file = source_file
        self.output_file = output_file
        self.read_xml()

    def read_xml(self):
        if os.path.exists(self.output_file):
            with open(self.output_file) as f:
                result = json.load(f)
        else:
            result = dict(audio=None)
        tree = ET.parse(self.source_file)
        transcript = tree.getroot()
        result['article'] = [[]]
        for text in transcript:
            attrib = text.attrib
            if 'dur' not in attrib:
                continue

            start = int(float(attrib['start']) * 1000)
            dur = int(float(attrib['dur']) * 1000)
            result['article'][0].append(dict(
                start=start,
                end=start + dur,
                text=text.text.replace('\n', ' ')
            ))
        with open(self.output_file, 'w') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source_file')
    parser.add_argument('output_file')

    args = parser.parse_args()
    Convert(args.source_file, args.output_file)
