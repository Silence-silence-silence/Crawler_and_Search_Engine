# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import os.path
import os
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer

import urllib

ps = PorterStemmer()

important_words = []

def get_content(name):
    # Use a breakpoint in the code line below to debug your script.
    print('Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.




def tokenize(content):
    parse = BeautifulSoup(content, "html.parser")
    element = parse.get_text()

    # filter out words that are noise i.e. menu bar items (here assuming menu bar items are less than 15 character count)

    # from https://github.com/nltk/nltk/issues/1900
    tokenizer = RegexpTokenizer(r'[^\W_]+|[^\W_\s]+')
    words = tokenizer.tokenize(element)

    res = list()

    ## make it ascii, so quicker
    for item in words:
        try:
            item.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            continue
        else:
            res.append(ps.stem(item.lower()))

    return res


def importanwords(content):
    parse = BeautifulSoup(content, "html.parser")
    important_words = []

    temp = parse.findAll('h1')
    temp += parse.findAll('h2')
    temp += parse.findAll('h3')
    temp += parse.findAll('title')
    temp += parse.findAll('strong')
    temp += parse.findAll('b')

    tokenizer = RegexpTokenizer(r'[^\W_]+|[^\W_\s]+')

    for items in temp:
        x = items.get_text()
        important_words += tokenizer.tokenize(x)

    stemandlower = []
    for items in important_words:
        stemandlower.append(ps.stem(items.lower()))
    return stemandlower


def process_content(content, importantw):
    freq = {}

    # compute_freq and position
    for words in content:
        if words not in freq:
            if words in importantw:
                freq[words] = 100

            else:
                freq[words] = 1
        else:
            if words in importantw:
                freq[words] += 100

            else:
                freq[words] += 1
    return freq


global doc_id
doc_id = 0

url_hash = {}
global file_breakpoint

already_indexed = []
def file_path(count):
    global doc_id
    result_dict = {}

    path = os.getcwd() + "/developer/DEV"
    counts = 0

    for file in os.listdir(path):
        if file not in already_indexed:
            if counts >= 20000:
                return result_dict
            already_indexed.append(file)
            for webs in os.listdir(path + "/" + file):
                real_path = path + "/" + file + "/" + webs
                with open(real_path, "r", encoding="utf-8") as f:
                    try:
                        contents = json.load(f)
                    except json.decoder.JSONDecodeError:
                        continue
                    url = contents['url']
                    html_info = contents['content']

                    wordss = tokenize(html_info)

                    important_words = importanwords(html_info)
                    freq_list = process_content(wordss, important_words)

                    for words in freq_list:
                        if words not in result_dict:
                            doc_freq_dict = {}
                            doc_freq_dict[doc_id] = freq_list[words]
                            result_dict[words] = doc_freq_dict
                        else:
                            if doc_id not in result_dict[words]:
                                result_dict[words][doc_id] = freq_list[words]
                            else:
                                result_dict[words][doc_id] += freq_list[words]


                    if doc_id not in url_hash:
                        url_hash[doc_id] = url
                counts += 1
                print(doc_id)
                doc_id += 1

    return result_dict






def store_index():
    file_no = [0,20000,40000]
    for count in file_no:
        result = sorted(file_path(count).items(), key=lambda x: x[0])
        path = os.getcwd() + "/partial/" + str(count) + ".json"
        with open(path, "a", encoding='utf-8') as f:
            for items in result:
                json.dump(items, f)
                f.write("\n")



if __name__ == '__main__':
    store_index()

    print(doc_id)
    with open("url.json", "a", encoding='utf-8') as f:
        json.dump(url_hash,f)

    print(already_indexed)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
