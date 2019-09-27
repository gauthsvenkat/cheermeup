import urllib
from urllib.request import urlopen
import re
import cv2
from time import time
import os

REGEX = "https:\/\/(thumbs|i)\.(gfycat|imgur)\.com\/[\w-]+\.(mp4|webm)"
TIMEPERIOD = {
    'hour': 60 * 60,
    'halfday': 60 * 60 * 12,
    'day': 60 * 60 * 24,
    'month': 60 * 60 * 24 * 30,
}


def httpmp4(url):
    url = url.replace('.gifv', '.mp4') if url.endswith('.gifv') else url
    return url.replace('https:', 'http:') if url.startswith('https:') else url


def parseLink(url):
    if url.endswith('.mp4') or url.endswith('.gifv') or url.endswith('.webm'):
        return httpmp4(url)

    elif 'gfycat' in url or 'imgur' in url:

        page = urlopen(url).read().decode('utf8')
        match = re.search(REGEX, page)
        url = match.group(0)

        return httpmp4(url)

    elif 'v.redd.it' in url:

        for res in ['/DASH_1080', '/DASH_720', '/DASH_480', '/DASH_360', '/DASH_240']:
            try:
                urlopen(url + res).read()
                return httpmp4(url + res)
            except urllib.error.HTTPError:
                continue

    return None


def playVideo(url):
    assert url is not None, "Some error in parsing the link :-(. Try again"

    clip = cv2.VideoCapture(url)
    rval, frame = clip.read()

    while rval:
        cv2.imshow('nice', frame)

        if cv2.waitKey(40) & 0xFF == ord('q'):
            break

        rval, frame = clip.read()

    cv2.destroyAllWindows()


def isOld(filename, period='day'):
    return True if TIMEPERIOD[period] < time() - os.path.getmtime(filename) else False
