
import os.path
import os
import json


if __name__ == '__main__':
    path = os.getcwd() + "/partial"
    a = 0
    count = 0

    real_path = path + "/" + "0.json"
    real_path1 = path + "/" + "20000.json"
    result_path2 = path + "/" + "result.json"
    f_check = 0
    f1_check = 0
    with open(real_path, "r", encoding="utf-8") as f, open(real_path1, "r", encoding="utf-8") as f1, open(result_path2, "a" ,encoding= "utf-8") as r:
        x = json.loads(f.readline())
        y = json.loads(f1.readline())


        while x != "" or y != "":
            a += 1
            print(a)
            if x[0] < y[0]:
                json.dump(x,r)
                r.write("\n")
                line = f.readline()
                if line == '':
                    break
                x = json.loads(line)
            elif x[0] > y[0]:
                json.dump(y, r)
                r.write("\n")
                line = f1.readline()
                if line == '':
                    break
                y = json.loads(line)
            else:
                x[1].update(y[1])

                json.dump(x, r)
                r.write("\n")
                line = f.readline()
                line1 = f1.readline()
                if line == '':
                    break
                if line1 == '':
                    break
                x = json.loads(line)
                y = json.loads(line1)

    real_path = path + "/" + "result.json"
    real_path1 = path + "/" + "40000.json"
    result_path2 = path + "/" + "Real_result.json"
    f_check = 0
    f1_check = 0
    with open(real_path, "r", encoding="utf-8") as f, open(real_path1, "r", encoding="utf-8") as f1, open(result_path2, "a", encoding="utf-8") as r:
        x = json.loads(f.readline())
        y = json.loads(f1.readline())



        while x != "" or y != "":
            a += 1
            print(a)
            if x[0] < y[0]:
                json.dump(x, r)
                r.write("\n")
                line = f.readline()
                if line == '':
                    break
                x = json.loads(line)
            elif x[0] > y[0]:
                json.dump(y, r)
                r.write("\n")
                line = f1.readline()
                if line == '':
                    break
                y = json.loads(line)
            else:
                x[1].update(y[1])

                json.dump(x, r)
                r.write("\n")
                line = f.readline()
                line1 = f1.readline()
                if line == '':
                    break
                if line1 == '':
                    break
                x = json.loads(line)
                y = json.loads(line1)







