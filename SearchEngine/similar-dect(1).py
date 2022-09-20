import os.path
import os
import hashlib
import json
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from partialIndex import tokenize

ps = PorterStemmer()

path = os.getcwd() + "/developer/DEV"

def simhash(file_path):
    freq = {}
    with open(file_path, 'r', encoding="utf-8") as f:
        try:
            contents = json.load(f)
        except json.decoder.JSONDecodeError:
            return
        url = contents['url']
        html_info = contents['content']

        wordss = tokenize(html_info)

        freq = process_content(wordss)

    sumBinary = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    for key in freq:
        #binary_key = ' '.join(format(ord(c), 'b') for c in key)
        binary_obj = hashlib.shake_128(key.encode('utf-8')).digest(32)

        current_byte = 0
        for byte in binary_obj:
            if byte == 0:
                sumBinary[current_byte] += (-1 * freq[key])
            elif byte == 1:
                sumBinary[current_byte] += (1 * freq[key])
            current_byte += 1
    # print(sumBinary)
    returnBinary = []
    for value in sumBinary:
        if value > 0:
            returnBinary.append(1)
        else:
            returnBinary.append(0)
    #print(returnBinary)
    return returnBinary

def process_content(content):
    freq = {}

    # compute_freq and position
    for words in content:
        if words not in freq:
            freq[words] = 1
        else:
            freq[words] += 1

    return freq

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

def similarity_hamming(binary1, binary2):
    hamming_distance = 0

    current_byte = 0
    for byte in binary1:
        if binary1[current_byte] != binary2[current_byte]:
            hamming_distance += 1
        current_byte += 1

    return 1-(hamming_distance/len(binary1))
            
if __name__ == '__main__':
    count = 0
    with open('report_near_duplicate.txt', 'a') as f:
        f.write("near duplicate: \n")

        near_similar_files = {}
        near_similar_folder = {}
        for file in os.listdir(path):
            for webs in os.listdir(path + "/" + file):
                # get real path
                real_path = path + "/" + file + "/" + webs
                near_similar_files[real_path] = "/" + file + "/" + webs
                # get simhash value 1
                simhash_value1 = simhash(real_path)
                # get file 2
                for file2 in os.listdir(path):
                    # don't check finished(1) folder again
                    if file2 in near_similar_folder:
                        continue
                    for webs2 in os.listdir(path + "/" + file2):
                        # don't check finished(1) file again
                        if webs2 in near_similar_files:
                            continue
                        # get real path2
                        real_path2 = path + "/" + file2 + "/" + webs2
                        # get simhash value 2
                        simhash_value2 = simhash(real_path2)
                        # get similarity
                        similarity_percent = similarity_hamming(simhash_value1, simhash_value2)
                        # add real_path2 to delete list file if over 0.95
                        if (similarity_percent >= 0.95):
                            f.write(file2 + "/" + webs2+":"+str(similarity_percent)+"\n")
                            print("Found similar = "+str(similarity_percent))
                            os.remove(real_path2)
                            near_similar_files[real_path2] = "/" + file2 + "/" + webs2
            near_similar_folder[file] = True

        f.write("near duplicate end. \n")

        print("Found similarity End. ")