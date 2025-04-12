import requests
import main

resp = requests.get(
    url="https://www.youduzw.com/en/common/read.ttf",
    headers=main.headers
)

with open("read.ttf", mode="wb") as ttf:
    ttf.write(resp.content)