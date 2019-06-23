# -*- coding: utf-8 -*-

import argparse
import json
import os

END_OFFSET = 10

class Convert():

    def __init__(self, source_file, output_file, content_start, content_end):
        self.source_file = source_file
        self.output_file = output_file
        self.content_start = content_start
        self.content_end = content_end
        self.read_json()
        self.write_json()

    def read_json(self):
        with open(self.source_file) as f:
            self.content = json.load(f)

    def write_json(self):
        if os.path.exists(self.output_file):
            with open(self.output_file) as f:
                result = json.load(f)
        else:
            result = dict(audio=None)
        result['article'] = []
        paragraphs = self.content['paragraphs']
        paragraphs_num = len(paragraphs)
        for p_index, paragraph in enumerate(paragraphs):
            paragraph = paragraph['cues']
            sentences_num = len(paragraph)
            sentences = []
            for s_index, sentence in enumerate(paragraph):
                if p_index == paragraphs_num - 1 and s_index == sentences_num -1:
                    end = self.content_end
                elif s_index == sentences_num -1:
                    end = paragraphs[p_index + 1]['cues'][0]['time'] + self.content_start - END_OFFSET
                else:
                    end = paragraph[s_index + 1]['time'] + self.content_start - END_OFFSET
                sentences.append(dict(
                    start=self.content_start + sentence['time'],
                    end=end,
                    text=sentence['text'].replace('\n', ' ')
                ))
            result['article'].append(sentences)
        # print(result)
        with open(self.output_file, 'w') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source_file')
    parser.add_argument('output_file')
    parser.add_argument('content_start', type=int)
    parser.add_argument('content_end', type=int)

    args = parser.parse_args()
    Convert(args.source_file, args.output_file, args.content_start, args.content_end)
