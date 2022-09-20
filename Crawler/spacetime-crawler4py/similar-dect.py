import os.path
import os
import hashlib

path = os.getcwd() + "/pages"
urltext = {}

def checksum():
    checksum = {}

    for file in os.listdir(path):

        total = 0
        if file != ".ipynb_checkpoints":
            filepath = os.path.join(path, file)
            with open(filepath, 'r') as f:
                url = f.readline()
                lines = f.readlines()

                for items in lines:
                    res = items.split(" -> ")
                    token = res[0]
                    number = int(res[1].rstrip(" \n"))
                    charSum = 0
                    for char in token:
                        charSum += ord(char)
                    total = total + charSum * number

                checksum[url] = total
        # print("processing the checksum:" + file)

    check_Sum = checksum
    result = []
    for toSearch in check_Sum:
        # print("looking for aim file:" + toSearch)
        for items in check_Sum:
            if (toSearch != items):
                if (check_Sum[toSearch] == check_Sum[items]):
                    result.append(toSearch.rstrip("\n") + " and " + items.rstrip("\n") + " with same checksum : " + str(
                        check_Sum[items]) + "\n")

    return result


def simhash(file_path):
    freq = {}
    with open(file_path, 'r') as f:
        url = f.readline()
        urltext[file_path] = url
        lines = f.readlines()

        for items in lines:
            res = items.split(" -> ")
            token = res[0]
            number = int(res[1].rstrip(" \n"))

            if token in freq:
                freq[token] += number
            else:
                freq[token] = number

    sumBinary = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for key in freq:
        # binary_key = ' '.join(format(ord(c), 'b') for c in key)
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
    # print(returnBinary)
    return returnBinary


def similarity_hamming(binary1, binary2):
    hamming_distance = 0

    current_byte = 0
    for byte in binary1:
        if binary1[current_byte] != binary2[current_byte]:
            hamming_distance += 1
        current_byte += 1

    return 1 - (hamming_distance / len(binary1))


if __name__ == '__main__':
    with open('report_exact_duplicate.txt', 'a') as f:
        f.write("exact duplicate search:\n")
        for items in checksum():
            f.write(items)
    f.close()
    print("exact duplicate end.")
    with open('report_near_duplicate.txt', 'a') as f:
        f.write("near duplicate: \n")

        near_similar_files = []
        file_list = os.listdir(path)
        index = 0
        while index < len(file_list):
            file = file_list[index]
            total = 0
            if file != ".ipynb_checkpoints":
                filepath = os.path.join(path, file)
                simhash_value1 = simhash(filepath)
                # print("searching for file:" + file)

                index2 = index
                while index2 < len(file_list):
                    searchFiles = file_list[index2]
                    if searchFiles != ".ipynb_checkpoints":
                        if (file != searchFiles):
                            # print("pairing for file " + file + "for " + searchFiles)
                            filepath2 = os.path.join(path, searchFiles)
                            simhash_value2 = simhash(filepath2)
                            similarity_percent = similarity_hamming(simhash_value1, simhash_value2)

                            if (similarity_percent >= 0.95):

 
                                f.write(urltext[filepath] + " and " + urltext[filepath2].rstrip("\n") + " with similarity: " + str(
                                    similarity_percent) + "\n")

                    index2 += 1
            # for items in near_similar_files:
            #    f.write(items)
            index += 1
            print(index/len(file_list))
        f.write("near duplicate end. \n")

    f.close()