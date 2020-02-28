import requests

r = requests.post("http://httpbin.org/post")

print(r.text)