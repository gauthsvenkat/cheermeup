from utils import parseLink, playVideo

with open('urls', 'r') as f:
    urls = f.read().splitlines()

    for url in urls:
        playVideo(parseLink(url))

