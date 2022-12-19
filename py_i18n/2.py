import json
from socket import herror
import requests

word = input('请输入您要翻译的单词')
header = {

    "User-Agent":
}

data = {



}

url = 'https://fanyi.baidu.com/sug'
response = requests.post(url, data = data, headers = header).text

print(json.loads(response))