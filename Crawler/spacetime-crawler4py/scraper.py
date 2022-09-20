import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from urllib.parse import urldefrag
from nltk.tokenize import RegexpTokenizer
import os.path
import uuid
from os.path import exists

stop_words = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't",
              "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't",
              "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down",
              "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't",
              "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself",
              "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
              "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of",
              "off", "on", "once", "only", "or", "other", "ought", "our", "ours	ourselves", "out", "over", "own",
              "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than",
              "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these",
              "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under",
              "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't",
              "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why",
              "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your",
              "yours", "yourself", "yourselves"]


def scraper(url, resp):
    # check response status
    links = []

    if is_valid(url) and (
            resp.status == 200 or resp.status == 201 or resp.status == 202) and resp.raw_response is not None:
        ##get tokens
        tokens = tokenize(resp.raw_response.content)
        if len(tokens) < 20:
            return links
        # comopute freq
        freq = computeWordFrequencies(tokens)

        path = os.getcwd() + "/pages"
        name = str(uuid.uuid5(uuid.NAMESPACE_DNS, url)) + ".txt"
        filepath = os.path.join(path, str(name))
        # save to pages
        with open(filepath, "a", encoding='utf-8') as pages:
            pages.write(url + '\n')
            for KEY in freq:
                pages.write("%s -> %s \n" % (KEY, freq[KEY]))

        links = extract_next_links(url, resp)

        return [link for link in links if is_valid(link)]
    else:
        return links


def extract_next_links(url, resp):
    # Implementation required. url: the URL that was used to get the page resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there
    # was some kind of problem. resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    # resp.raw_response.url: the url, again resp.raw_response.content: the content of the page! Return a list with
    # the hyperlinks (as strings) scrapped from resp.raw_response.content
    res_link = []
    remove_frag_link = []

    # avoid no information
    if resp.raw_response is not None:
        parse = BeautifulSoup(resp.raw_response.content, "html.parser")
        for element in parse.findAll('a'):
            res_link.append(element.get('href'))

            # throw fragments away
        for count, link in enumerate(res_link):
            res_link[count] = urldefrag(link)[0]

    res_link = set(res_link)

    return res_link


def is_valid(url):
    # Decide whether to crawl this url or not.
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            # print("1")
            return False

        domains = [".ics.uci.edu", ".cs.uci.edu", ".informatics.uci.edu",
                   ".stat.uci.edu", "today.uci.edu"]

        if not any(domain in parsed.netloc for domain in domains):
            # print("2")
            return False

        path = os.getcwd() + "/pages"
        name = str(uuid.uuid5(uuid.NAMESPACE_DNS, url)) + ".txt"
        filepath = os.path.join(path, str(name))

        # if url already crawled, skip it
        if (exists(filepath)):
            # print("3")
            return False

        # avoid traps
        # replytocome same information page, ical image download
        if (re.search(r'calendar|events|share|replytocom|cgi-bin|includes|var|order|doc_id|docid|feed|sort|filter|limit|wp|action|tribe_events|date|tribe_event_display|tribe-bar-date|fbclid|redirec_to|attachment_id|afgxx_page_id|page_id|json|ical',
                      parsed.query.lower())):
            # print("4")
            return False

        if (re.search(r'.java|.py|.ps.Z|eps.Z', parsed.path)):
            # print("5")
            return False
        
        if "mt-live.ics.uci.edu" in parsed.netloc:
            if "events"  in parsed.path:
                # print("6")
                return False
        if "wics.ics.uci.edu" in parsed.netloc:
            if "events"  in parsed.path:
                # print("6")
                return False
        
        # event
        if "today.uci.edu" in parsed.netloc:
            if "department/information_computer_sciences" not in parsed.path:
                # print("6")
                return False

        
        if (re.search(r'(\/pdf\/)', parsed.path.lower())):
            return False
        if (re.search(r'(\/ppsx\/)', parsed.path.lower())):
            return False

        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv|ppsx"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print("TypeError for ", parsed)
        raise


def tokenize(content):
    parse = BeautifulSoup(content, "html.parser")
    element = parse.get_text()

    words = list()

    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(element)

    res = list()

    ## make it ascii, so quicker
    for item in words:
        if item not in stop_words:
            try:
                item.encode(encoding='utf-8').decode('ascii')
            except UnicodeDecodeError:
                continue
            else:
                if len(item) > 1:
                    res.append(item.lower())

    return res


def computeWordFrequencies(listFre):
    dict = {}

    for item in listFre:
        if item in dict:
            dict[item] += 1
        else:
            dict[item] = 1
    return dict




