# import translator
# from translate import Translator

import urllib.request
import urllib.parse
import json
import os
from os import path


# Translator(from_lang="Chinese", to_lang="English").translate('你好')
# translator1 = Translator(from_lang="english", to_lang="chinese")


def get_data(words):
    data = {}
    data["type"] = "AUTO"
    data["i"] = words
    data["doctype"] = "json"
    data["xmlVersion"] = "1.8"
    data["keyfrom:fanyi"] = "web"
    data["ue"] = "UTF-8"
    data["action"] = "FY_BY_CLICKBUTTON"
    data["typoResult"] = "true"
    data = urllib.parse.urlencode(data).encode('utf-8')
    return data

def url_open(url, data):
    req = urllib.request.Request(url, data)
    req.add_header(
        "User-Agent",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    )
    response = urllib.request.urlopen(req)
    html = response.read()
    html = html.decode("utf-8")
    return html


def get_json_data(html):
    # print(html)
    result = json.loads(html)
    result = result['translateResult']
    result = result[0][0]['tgt']
    return result


def main(line):
    words = line
    url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule&smartresult=ugc&sessionFrom=dict.top"

    data = get_data(words)
    html = url_open(url, data)
    result = get_json_data(html)
    # print("The result: %s" % result)
    return result


# if __name__ == "__main__":
#     # while True:
#         # main()
#     main()


def translate(file, to_file1):
    # from_file = r'./source/' + file
    # to_file = r'./translate/' + file
    from_file = r'' + file
    to_file = r'' + to_file1
    word_list = []
    with open(from_file) as file_object:
        lines = file_object.readlines()
        for line in lines:
            request_translate = True
            for word in line:
                # word.replace('\n','')
                if word == " ": continue
                if word == "#":
                    # print(line)
                    tr_line = main(line)
                    # tr_line = translator1.translate(line)
                    # print(tr_line)
                    # ''.startswith('#')
                    if tr_line[0] != '#':
                        word_list.append('\t#' + tr_line[:-1])
                    else:
                        word_list.append('\t' + tr_line[:-1])

                    request_translate = False
                    break
            if request_translate:
                word_list.append(line[:-1])

    new_words = "\n".join(word_list)

    with open(to_file, 'w', encoding="utf-8") as myfile:
        print(new_words)
        myfile.write(new_words)


# file = 'jei-client.ini'
# file = 'advancementplaques-common.toml'

# file = 'betterfpsdist-common.toml'
# translate(file)
# print("Ok!")


# 定义一个函数
def scaner_file(url):
    #遍历当前路径下所有文件
    file = os.listdir(url)
    for f in file:
        #字符串拼接
        real_url = path.join(url, f)
        #打印出来
        # print(real_url)

        file = real_url
        print('Is translating ' + file + 'file ----')

        # sum = 10         # 设置倒计时时间
        # timeflush = 0.25  # 设置屏幕刷新的间隔时间
        # for i in range(0, int(sum/timeflush)):
        #     list = ["\\", "|", "/", "—"]
        #     index = i % 4
        #     print("\r程序正在运行 {}".format(list[index]), end="")

        translate(file, file.replace('source', 'translate'))
        print("Ok!")
        
#调用自定义函数
scaner_file("./source/")
