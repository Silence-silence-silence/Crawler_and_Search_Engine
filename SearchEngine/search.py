import math
import sys
import json

from nltk import RegexpTokenizer
from nltk.stem import PorterStemmer

from collections import Counter
import time

from numpy import dot
from numpy.linalg import norm
ps = PorterStemmer()








if __name__ == '__main__':
    with open("url.json","r",encoding="utf-8") as f,open("indexOfindex.json","r",encoding="utf-8") as f1:

        url_hash = json.load(f)
        index_hash = json.load(f1)

    prompt = input("Enter your search (q/Q to quit): ")
    while prompt != "q" and prompt != "Q":
        query = []
        posting = []
        result = {}
        postingwithword = {}

        count = 0

        start = time.perf_counter()

        tokenizer = RegexpTokenizer(r'[^\W_]+|[^\W_\s]+')
        words = tokenizer.tokenize(prompt)

        queryCount = {}
        for items in words:
            itemsTemp = ps.stem(items.lower())
            if itemsTemp not in queryCount.keys():
                queryCount[itemsTemp] = 1
            else:
                queryCount[itemsTemp] += 1
            #query.append(itemsTemp)
        query = queryCount.keys()
        queryVector = list(queryCount.values())

        with open("tf_idf.json","r",encoding= "utf-8") as f:
            for items in query:
                char_position = 0
                if len(items) == 1:
                    char_position = index_hash[items]
                else:
                    first_two_letter = items[0] + items[1]
                    char_position = index_hash[first_two_letter]

                f.seek(char_position)

                line = f.readline()
                data = json.loads(line)
                while data[0] != items:
                    line = f.readline()
                    data = json.loads(line)

                postingwithword[data[0]] = data[1]
                posting.append(data[1])




        def sortrule(r):
            return len(r)

        posting.sort(key=sortrule)                                            #-- do not sort

        #print(posting)

        #find intersection
        t = {}
        count = 0
        noresult = False
        for items in posting:

            if len(t) == 0:
                # print(count)
                if count != 0:
                    noresult = True
                    break
                t = items
            else:
                t = {x: t[x] for x in t if x in items}

            count += 1




        for items in posting:
                for key in items:
                    items[key] = float(items[key])

        #print(posting)

        document_scores = {}
        document_len = {}
        query_tfidf = {}

        for items in queryCount:
            query_tfidf[items] = 1 + math.log(queryCount[items], 10)


        if len(query) > 1:
            # get cosine similarity (ONLY if query is more than 1 terms)
            # for items in query_tfidf:
            for items in query_tfidf:
                for documents in t:
                    if documents not in document_scores:
                        document_scores[documents] = postingwithword[items][documents] * query_tfidf[items]
                    else:
                        document_scores[documents] += postingwithword[items][documents] * query_tfidf[items]


            print(queryCount)
        else:
            # if ONLY 1 term in query, use tfidf
            for d in posting:
                for items in d:
                    document_scores[items] = d[items]

        #print(result)

        top5 = dict(Counter(document_scores).most_common(5))

        end = time.perf_counter()
        print(f"Search the result in {end - start:0.4f} seconds")
        for items in top5:
            print(url_hash[items])
            print(document_scores[items])

        prompt = input("Enter your search (q/Q to quit): ")