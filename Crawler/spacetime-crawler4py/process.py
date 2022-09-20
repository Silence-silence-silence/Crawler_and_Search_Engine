# coding=utf-8
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import os.path
import os
from urllib.parse import urlparse
import tldextract

def print_hi():
    path = os.getcwd() + "/pages"

    unique = {}
    freq = {}
    longest = 0
    longest_page = ""
    count = 0
    all_url = []
    for file in os.listdir(path):
       
        count = count + 1
        if file != ".ipynb_checkpoints":
            print(file)
            path = os.getcwd() + "/pages"

            filepath = os.path.join(path, file)
            
            with open (filepath, 'r') as f:
            
                url = f.readline()
                all_url.append(url)
                parsed = urlparse(url)
                
                subdomain = parsed.netloc.lower()

                if ".ics.uci.edu" in subdomain:
                    print ("yes")
                    if subdomain in unique:
                        unique[subdomain] += 1
                    else:
                        unique[subdomain] = 1
                
                lines = f.readlines()

                if (len(lines) > longest):
                    longest = len(lines)
                    longest_page = url

                for items in lines:
                    res = items.split(" -> ")
                    token = res[0]
                    number = int(res[1].rstrip(" \n"))
                    
                   
                    if token in freq:
                        freq[token] += number
                    else:
                        freq[token] = number

            
    with open ('report.txt', 'a') as f:
        f.write(str(count) + "\n")
        resultFre = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        f.write("50 common words"+ "\n")
        for item in resultFre[:50]:
            f.write(str(item)+ "\n")
        f.write("longest : " + longest_page + "with words : " + str(longest)+ "\n")
        f.write("unique url:"+ "\n")
        unique = sorted(unique.items(), key=lambda x: x[0])
        for KEY in unique:
            f.write(str(KEY)+ "\n")
        
    with open ('allUrls.txt', 'a') as u:
        for items in all_url:
            u.write(items)
        

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi()
    

    
   
   


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
