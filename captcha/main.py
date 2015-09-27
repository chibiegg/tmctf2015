# encoding=utf-8

import requests
from PIL import Image
from io import BytesIO
import subprocess

cookies = {}

import re

POINT_RE = re.compile(">(\d+)/500<")

def login(username, password):
    global cookies

    url = "http://ctfquest.trendmicro.co.jp:8080/acf2e28903f698eda9bdefc043b6edc3/signin"

    # Get form
    response = requests.get(url)
    cookies = response.cookies

    data = {
        "username":username,
        "password":password,
        "fuel_csrf_token":cookies["fuel_csrf_token"]
    }
    response = requests.post(url, data=data, cookies=cookies)
    cookies = response.cookies
    return ("challenge" in response.text)

def get_point():
    global cookies
    url = "http://ctfquest.trendmicro.co.jp:8080/acf2e28903f698eda9bdefc043b6edc3/challenge"
    response = requests.get(url, cookies=cookies)
    cookies = response.cookies
    body = response.text
    point = int(POINT_RE.search(body).group(1))
    print("POINT: {0}".format(point))
    return point


def challenge():
    global cookies

    url = "http://ctfquest.trendmicro.co.jp:8080/acf2e28903f698eda9bdefc043b6edc3/image"
    response = requests.get(url, cookies=cookies)
    #cookies = response.cookies
    try:
        image = Image.open(BytesIO(response.content)).convert('RGB')
    except:
        return
    base_color = image.getpixel((0, 0))


    pix = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            if pix[i,j] == base_color:
                pix[i,j] = (255, 255, 255)
            else:
                pix[i,j] = (0, 0, 0)

    #image = image.resize((int(image.size[0]/2), int(image.size[1]/2))).convert('1')
    image = image.convert('1')
    image2 = image.copy()

    pix = image.load()
    pix2 = image2.load()
    for i in range(2, image.size[0]-2):
        for j in range(2, image.size[1]-2):
            histgram = [0, 0]
            for di in range(-2, 3):
                for dj in range(-2, 3):
                    point = (i+di,j+dj)
                    color = pix[point[0], point[1]] > 0
                    histgram[color] += 1

            if histgram[0] > histgram[1]:
                pix2[i,j] = 0
            else:
                pix2[i,j] = 255

    image2.show()
    image2.save("image.png")

    result = ocr()
    print(len(result))
    if not result or "0" in result or "O" in result or "j" in result.lower() or "w" in result.lower() or len(result) != 4:
        print("Skip")
        return

    for i in range(500):
        submit(result)
        get_point()
    exit(1)

def ocr():
    subprocess.check_output(["rm", "-f", "result.txt"])
    subprocess.check_output(["tesseract", "image.png", "result", "-psm", "8", "letters"])
    result = subprocess.check_output(["cat", "result.txt"])
    try:
        result = result.decode("ascii").strip()
    except:
        result = None
    print(result)
    return result

def submit(captcha):
    global cookies

    url = "http://ctfquest.trendmicro.co.jp:8080/acf2e28903f698eda9bdefc043b6edc3/challenge"
    data = {
        "captcha":captcha,
        "fuel_csrf_token":cookies["fuel_csrf_token"]
    }
    response = requests.post(url, data=data, cookies=cookies)
    cookies = response.cookies
    return ("challenge" in response.text)


if __name__ == "__main__":
    assert login("chibieggx", "test"), "Login failer"
    while get_point() < 500:
        challenge()
