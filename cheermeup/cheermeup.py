#!/usr/bin/env python
import praw
from cheermeup.utils import playVideo, isOld, parseLink
import random
import os
from appdirs import user_cache_dir


def main():

    urlspath = os.path.join(user_cache_dir(), 'cheermeupurls')

    urls = (
        [line.strip() for line in open(urlspath, 'r')]
        if os.path.exists(urlspath) and not isOld(urlspath)
        else None
    )

    if urls is None:
        reddit = praw.Reddit(
            client_id='vHxB98R_R-8HYA', client_secret=None, user_agent='cheermeup'
        )
        subs = [
            'Eyebleach',
            'Babyelephantgifs',
            'PartyParrot',
            'AnimalsBeingJerks',
            'AnimalsBeingDerps',
        ]
        urls = [
            url
            for url in [
                submission.url
                for submission in reddit.subreddit('+'.join(subs)).hot(limit=None)
            ]
            if not (url.endswith('.jpg') or url.endswith('.png'))
        ]
        with open(urlspath, 'w') as f:
            for url in urls:
                f.write("{}\n".format(url))

    url = parseLink(random.choice(urls))

    while url is None:
        url = parseLink(random.choice(urls))

    print('Press \'q\' to quit')
    playVideo(url)


if __name__ == '__main__':
    main()
