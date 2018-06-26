ALEX46 = "http://www.ics.uci.edu/~thornton/ics46/"
ALEX45C = "http://www.ics.uci.edu/~thornton/ics45c/"

PATTIS = ""

import requests
import re
import time

class NotFoundError(Exception):
    pass

def get_data(url):
    t = requests.get(url)
    return t.text


def findurls(t):
    l = re.findall('href="[\w/]*"',t)
    if not l:
        print(t)
        raise NotFoundError
    return l

def download(baseurl,l):
    for i in range(4,len(l)):
        ii = l[i].lstrip('href="')
        ii = ii.rstrip('"')
        if "Project" in ii:
            print("[{:2f}%]Downloading ".format(i/len(l))+ii+"...")
            c = requests.get(baseurl+ii)
            with open("alex_ics45c/"+ii,'wb') as f:
                f.write(c.content)
            time.sleep(10)

if __name__ == "__main__":
    download(ALEX45C,findurls(get_data(ALEX45C+"Schedule.html")))
    #download(ALEX46,findurls(get_data(ALEX46+"Schedule.html")))
    #downlaod()
