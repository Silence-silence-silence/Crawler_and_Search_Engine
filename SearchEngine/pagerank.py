import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urldefrag
import os
from random import choice
import operator

path = os.getcwd() + "/developer/DEV"

def extract_links_list(content):
    res_link = []

    # avoid no information
    if content is not None:
        # parse content with html,
        # might give warning for those contents look like url
        parse = BeautifulSoup(content, "html.parser")
        for element in parse.findAll('a'):
            link = element.get('href')
            # throw fragments away
            link = urldefrag(link)[0]
            res_link.append(link)

    # remove duplicated
    res_link = list(set(res_link))

    return res_link

if __name__ == '__main__':
    # structure: key=url, value=file_path
    url_dict = {}
    # structure: key=url, value=reach count
    urlCount_dict = {}

    # collect all files and urls
    for file in os.listdir(path):
        for webs in os.listdir(path + "/" + file):
            file_path = path + "/" + file + "/" + webs
            with open(file_path, 'r', encoding="utf-8") as f:
                try:
                    contents = json.load(f)
                except json.decoder.JSONDecodeError:
                    break
                url = contents['url']
                url_dict[url] = file_path
                urlCount_dict[url] = 0

    print("collect urls done")

    # infinite loop count
    maximum_run = 500000
    current_run = 0
    url_dict_list = list(url_dict.keys())

    selected_url = choice(url_dict_list)
    while True:
        file_path = url_dict[selected_url]

        with open(file_path, 'r', encoding="utf-8") as f:
            try:
                contents = json.load(f)
            except json.decoder.JSONDecodeError:
                break
            url_list = extract_links_list(contents['content'])

            # get next url
            if url_list:
                goto_url = choice(url_list)
                if goto_url in urlCount_dict:
                    selected_url = goto_url
                    urlCount_dict[selected_url] += 1
                else:
                    selected_url = choice(url_dict_list)
            else:
                selected_url = choice(url_dict_list)

        current_run += 1
        print(str(current_run)+f" ({current_run/maximum_run*100:0.1f}%)")
        if current_run >= maximum_run:
            break

    # sort result
    sorted_tuples = sorted(urlCount_dict.items(), key=operator.itemgetter(1), reverse=True)
    sorted_dict = {k: (v/maximum_run) for k, v in sorted_tuples}

    # output result
    with open('report_pagerank.txt', 'a') as f:
        json.dump(sorted_dict, f)
