# encoding=utf-8

import re
import requests
from PIL import Image
from io import BytesIO

BASE_URL = "http://ctfquest.trendmicro.co.jp:43210/click_on_the_different_color"
NEXT_URL_RE = re.compile("'(.+)\?x=")
IMAGE_URL_RE = re.compile("(/img/.+\.png)")


def fetch(url):
    print("="*20)
    print(url)
    response = requests.get(url)
    body = response.text
    print(body)
    print(response.headers)
    image_url = "http://ctfquest.trendmicro.co.jp:43210{0}".format(IMAGE_URL_RE.search(body).group(1))


    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))

    image.show()

    histgram = {}
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            r,g,b = image.getpixel((i,j))

            if (r,g,b) == (255, 255, 255):
                continue

            if not (r,g,b) in histgram:
                histgram[(r,g,b)] = {
                    "count":0,
                    "point":(i, j),
                }
            histgram[(r,g,b)]["count"] += 1

    histgram = list(histgram.values())

    color_1 = histgram[0]
    color_2 = histgram[1]

    target = color_1

    if color_1["count"] > color_2["count"]:
        target = color_2

    next_url = "http://ctfquest.trendmicro.co.jp:43210{0}?x={1}&y={2}".format(
        NEXT_URL_RE.search(body).group(1),
        target["point"][0], target["point"][1]
    )

    return next_url

if __name__ == "__main__":
    i = 1
    url = BASE_URL
    while True:
        print(i)
        url = fetch(url)
        i += 1
