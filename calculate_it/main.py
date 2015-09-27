# encoding=utf-8
from socket import socket
import time

host = "ctfquest.trendmicro.co.jp"
port = 51740


EIGO = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty', 'twentyone', 'twentytwo', 'twentythree', 'twentyfour', 'twentyfive', 'twentysix', 'twentyseven', 'twentyeight', 'twentynine', 'thirty', 'thirtyone', 'thirtytwo', 'thirtythree', 'thirtyfour', 'thirtyfive', 'thirtysix', 'thirtyseven', 'thirtyeight', 'thirtynine', 'forty', 'fortyone', 'fortytwo', 'fortythree', 'fortyfour', 'fortyfive', 'fortysix', 'fortyseven', 'fortyeight', 'fortynine', 'fifty', 'fiftyone', 'fiftytwo', 'fiftythree', 'fiftyfour', 'fiftyfive', 'fiftysix', 'fiftyseven', 'fiftyeight', 'fiftynine', 'sixty', 'sixtyone', 'sixtytwo', 'sixtythree', 'sixtyfour', 'sixtyfive', 'sixtysix', 'sixtyseven', 'sixtyeight', 'sixtynine', 'seventy', 'seventyone', 'seventytwo', 'seventythree', 'seventyfour', 'seventyfive', 'seventysix', 'seventyseven', 'seventyeight', 'seventynine', 'eighty', 'eightyone', 'eightytwo', 'eightythree', 'eightyfour', 'eightyfive', 'eightysix', 'eightyseven', 'eightyeight', 'eightynine', 'ninety', 'ninetyone', 'ninetytwo', 'ninetythree', 'ninetyfour', 'ninetyfive', 'ninetysix', 'ninetyseven', 'ninetyeight', 'ninetynine', 'onehundred']


def get_question(connection):
    ret = []
    while True:
        c = connection.read(1)

        if c == "=":
            break
        ret.append(c)

    connection.read(1)
    return "".join(ret).replace(",","")


def roman_to_int(roman):
    num = 0
    r_n = {
        'M': 1000,
        'D': 500,
        'C': 100,
        'L': 50,
        'X': 10,
        'V': 5,
        'I': 1
    }
    pre = 0
    for i in range(len(roman) - 1, -1, -1):
        c = roman[i]
        if not c in r_n:
            raise Exception('Invalid Roman: {}'.format(c))
        n = r_n[c]
        if n >= pre:
            num += n
            pre = n
        else:
            num -= n
    return num



if __name__ == "__main__":
    sock = socket()
    sock.connect((host, port))

    connection = sock.makefile()

    while True:
        question = get_question(connection)
        print("> {0}".format(question))

        parsed = []

        for l in question.split(" "):
            l = l.lower()
            if l in EIGO:
                l = str(EIGO.index(l))

            else:
                l.replace("HUNDRED", "*100+")

                l = l.upper()
                if len(l) and l[0] in "MDCLXVI":
                    l = str(roman_to_int(l))

            parsed.append(l)

        print(parsed)
        question = " ".join(parsed)
        print("= {0}".format(question))




        try:
            answer = str(eval(question))
        except:
            print("Please Input")
            answer = input('--> ').strip()



        time.sleep(1)
        print("< {0}".format(answer))
        sock.send((answer+"\n").encode("ascii"))
        time.sleep(1)

    sock.close()
