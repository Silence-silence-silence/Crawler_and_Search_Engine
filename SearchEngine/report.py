import os
import json
import math

import numpy as np
from numpy.linalg import norm
from nltk.stem.snowball import SnowballStemmer


if __name__ == '__main__':
    path = os.getcwd() + "/partial"
    result_path2 = path + "/" + "Real_result.json"
    count = 0
    url_count = 0

    index_hash = {}
    char_count = 0
    with open(result_path2, "r", encoding="utf-8") as f,open("tf_idf.json","a",encoding="utf-8") as f1, open("indexOfindex.json","a",encoding="utf-8") as f2:
        x = json.loads(f.readline())

        while x != "":

            if len(x[0]) ==1:
                if x[0] not in index_hash:
                    index_hash[x[0]] = char_count
            else:
                first_two_letter = x[0][0] + x[0][1]

                if first_two_letter not in index_hash:
                    print(first_two_letter)
                    index_hash[first_two_letter] = char_count



            for items in x[1]:
                x[1][items] = "{0:.4f}".format ((1 + math.log(x[1][items], 10)) * math.log10(55393 / len(x[1])))


            normal_factor = 1 / np.linalg.norm(list(x[1].values()))

            for k in x[1]:

                x[1][k] = "{0:.4f}".format (float(x[1][k]) * normal_factor)



            json.dump(x, f1)
            charlen = len(json.dumps(x))
            f1.write("\n")

            char_count += charlen + 2
            line = f.readline()
            if line == "":
                break
            x = json.loads(line)

        json.dump(index_hash,f2)

    with open("url.json","r",encoding="utf-8") as f:
        data = json.load(f)
        for items in data:
            url_count += 1


    print(count)
    print(url_count)






