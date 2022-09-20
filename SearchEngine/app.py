from flask import Flask, render_template, flash, request

app = Flask(__name__, template_folder='templates')


@app.route("/", methods=('GET', 'POST'))
def search():
    title = "Search"
    return render_template('main.html', title=title)


@app.route("/result", methods=["post"])
def result():
    prompt = request.form.get("query")

    query = []
    posting = []

    postingwithword = {}



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

    query = queryCount.keys()

    query_ignore = []

    with open("tf_idf.json", "r", encoding="utf-8") as f:
        for items in query:
            char_position = 0
            if len(items) == 1:
                if items in index_hash:
                    char_position = index_hash[items]
            else:
                first_two_letter = items[0] + items[1]
                if first_two_letter in index_hash:
                    char_position = index_hash[first_two_letter]

            f.seek(char_position)

            line = f.readline()
            data = json.loads(line)
            while data[0] != items:
                # when current data no longer match first_two_letter, or length is 1 (which have only 1 position but not found)
                # => the term is no exist in index table
                line = f.readline()
                data = json.loads(line)
                if data[0][0] + data[0][1] != first_two_letter or len(items) == 1:
                    query_ignore.append(items)
                    break

            if data[0] == items:
                postingwithword[data[0]] = data[1]
                posting.append(data[1])
            # remove query_ignore from query and queryCount, which are all unneccessary(not exist) terms

    if len(query_ignore) == len(words):
        end = time.perf_counter()

        print(f"Search the result in {end - start:0.4f} seconds")

        output = "<h1> No Result</h1>"
        output += "<h2> Search the result in " + "{0:.4f}".format(end - start) + " seconds </h2>"
        output += "<a href=http://127.0.0.1:5000/> Go Back to Main</a>"
        return output


    print(query_ignore)
    print(queryCount)
    for items in query_ignore:
        del queryCount[items]
    def sortrule(r):
        return len(r)

    posting.sort(key=sortrule)  # -- do not sort

    # print(posting)

    # find intersection
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

    if noresult:
        end = time.perf_counter()

        print(f"Search the result in {end - start:0.4f} seconds")

        output = "<h1> No Result</h1>"
        output += "<h2> Search the result in " + "{0:.4f}".format(end - start) + " seconds </h2>"
        output += "<a href=http://127.0.0.1:5000/> Go Back to Main</a>"
        return output

    for items in posting:
        for key in items:
            items[key] = float(items[key])

    # print(posting)

    document_scores = {}

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

    # print(result)

    top5 = dict(Counter(document_scores).most_common(5))

    end = time.perf_counter()
    print(f"Search the result in {end - start:0.4f} seconds")

    output = "<h1> Result: </h1>"
    output += "<h2> Search the result in " + "{0:.4f}".format(end - start) +" seconds </h2>"

    top5_pagerankadded ={}

    for items in top5:

        top5_pagerankadded[items] = page_rank[url_hash[items]] *1000+ document_scores[items]


    top5_pagerankadded = dict(Counter(top5_pagerankadded).most_common(5))


    for items in top5_pagerankadded:
        # print(top5_pagerankadded[items])
        # print(top5[items])
        output += "<a href = "+url_hash[items]+">" + url_hash[items] + "</a>"
        output += "<p> </p>"


    output += "<a href=http://127.0.0.1:5000/> Go Back to Main</a>"
    return output


# @app.route("/")
# def home():
#     return "<h1> main page <h1>"
#
# @app.route("/<name>")
# def user(name):
#     return f"Hello {name}!"

url_hash = {}
index_hash = {}
page_rank = {}

if __name__ == "__main__":
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

    with open("url.json", "r", encoding="utf-8") as f, open("indexOfindex.json", "r", encoding="utf-8") as f1, open("report_pagerank.txt","r",encoding="utf-8") as f2:

        url_hash = json.load(f)
        index_hash = json.load(f1)
        page_rank = json.load(f2)


    app.run()
