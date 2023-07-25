import requests

url = 'https://shogidata.info/list/rateranking.html'

r = requests.get(url)

index = -1

while True:
    index = r.text.find("</a></td><td>", index + 1)
    name_start = r.text.rfind('html">', 0, index) + 6
    if index == -1:
        break
    print(r.text[name_start:index], r.text[index+13:index+19])
print(r.text)