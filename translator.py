import requests
from bs4 import BeautifulSoup
import argparse
import sys


class Translation:

    def __init__(self):
        self.languages = {1: 'Arabic', 2: 'German', 3: 'English', 4: 'Spanish', 5: 'French', 6: 'Hebrew', 7: 'Japanese',
                          8: 'Dutch', 9: 'Polish', 10: 'Portuguese', 11: 'Romanian', 12: 'Russian', 13: 'Turkish'}
        parser = argparse.ArgumentParser()
        parser.add_argument('src_lang')
        parser.add_argument('trg_lang')
        parser.add_argument('word')
        args = parser.parse_args()

        try:
            a = list(self.languages.values()).index(args.src_lang.capitalize())
        except ValueError:
            print(f"Sorry, the program doesn't support {args.src_lang}")
            sys.exit()
        else:
            self.src_lang = a + 1

        if args.trg_lang == 'all':
            self.trg_lang = args.trg_lang.capitalize()
        else:
            try:
                a = list(self.languages.values()).index(args.trg_lang.capitalize())
            except ValueError:
                print(f"Sorry, the program doesn't support {args.trg_lang}")
                sys.exit()
            else:
                self.trg_lang = a + 1

        self.word = args.word
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        if self.trg_lang in self.languages and self.trg_lang != self.src_lang:
            self.result = []
            self.link_creation(self.trg_lang)
            print(self.result[0])
        elif self.trg_lang == 'All':
            self.result = []
            for i in self.languages:
                if i != self.src_lang:
                    self.link_creation(trg_lang=i)
            for i in self.result:
                print(i)

    def link_creation(self, trg_lang):
        link = f'https://context.reverso.net/translation/{self.languages[self.src_lang].lower()}-' \
               f'{self.languages[trg_lang].lower()}/{self.word}'
        self.request_creation(link, trg_lang)

    def request_creation(self, link, trg_lang):
        try:
            req = requests.get(link, headers=self.headers)
        except ConnectionError:
            print('Something wrong with your internet connection')
            sys.exit()
        self.trans_words(req, trg_lang)

    def trans_words(self, req, trg_lang):
        try:
            trans_words = BeautifulSoup(req.content, 'html.parser') \
                .find(id='translations-content').find_all('a')
        except AttributeError:
            print(f'Sorry, unable to find {self.word}')
            sys.exit()

        trans_words_list = []
        for i in trans_words:
            temp = ' '.join(i.text.split())
            trans_words_list.append(temp)
        self.trans_phrases(req, trg_lang, words=trans_words_list)

    def trans_phrases(self, req, trg_lang, words):
        trans_phrases_orig = [' '.join(i.text.split()) for i in
                              BeautifulSoup(req.content, 'html.parser')
                              .find_all('div', {"class": ["src ltr", "trg rtl", "trg rtl arabic"]})]
        trans_phrases_res = [' '.join(i.text.split()) for i in
                             BeautifulSoup(req.content, 'html.parser')
                             .find_all('div', {"class": ["trg ltr", "trg rtl arabic", "trg rtl"]})]
        trans_phrases_list = []
        for i in zip(trans_phrases_orig, trans_phrases_res):
            trans_phrases_list.append('\n'.join(i))
        self.file_filling(words, trg_lang, phrases=trans_phrases_list)

    def file_filling(self, words, trg_lang, phrases):
        output = f'{self.languages[trg_lang]} Translations:\n' \
                 f'{words[0]}\n' \
                 f'{self.languages[trg_lang]} Example:\n' \
                 f'{phrases[0]}'
        self.result.append(output)
        self.file_creation()

    def file_creation(self):
        open(f'{self.word}.txt', 'w').close()
        file = open(f'{self.word}.txt', 'a+', encoding='utf-8')
        for i in self.result:
            file.write(i + '\n')
        file.close()


new_trans = Translation()
