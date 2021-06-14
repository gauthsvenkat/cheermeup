#!/usr/bin/env python3
import praw
import random
import os
import appdirs
import urllib
import re
import cv2
import time
import argparse
import multiprocessing
import functools


def is_not_old(filepath, period):
    return not (time.time() - os.path.getmtime(filepath) > period)


def url_is_not_image(url):
    return (not (url.endswith('.jpg') or url.endswith('.png') or url.endswith('.jpeg'))) \
           and (url.find('redd.it') > -1 or url.find('gfycat') > -1 or url.find('imgur') > -1) #make sure that the post contains videos only from these domains


def scrape_subreddit(reddit, search_limit, subreddit_name):

    all_urls = [submission.url for submission in reddit.subreddit(subreddit_name).hot(limit = search_limit)] #search for hot posts in a specific subreddit
    non_image_urls = list(filter(url_is_not_image, all_urls)) #filter out image urls

    return non_image_urls


def write_urls_to_cache(urls, cache_file_path):
    urls = random.sample(urls, len(urls)) #shuffle the urls a bit before writing them to cache
    with open(cache_file_path, 'w') as file:
        for url in urls:
            file.write("{}\n".format(url))
    return urls


def gifvmp4(url):
    return url.replace('.gifv', '.mp4') if url.endswith('.gifv') else url #cv2 can't read gifv links correctly so we change them to mp4 links


def get_post_urls(args):

    cache_file_path = os.path.join(appdirs.user_cache_dir(), args.cache_file_name)

    if os.path.exists(cache_file_path) and (is_not_old(cache_file_path, args.period)) and (not args.force_rewrite_cache):
        with open(cache_file_path, 'r') as file:
            post_urls = [line.rstrip() for line in file]

    else:
        reddit = praw.Reddit(client_id = args.client_id,
                             client_secret = None,
                             user_agent = args.user_agent,
                             check_for_updates=False,
                             comment_kind="t1",
                             message_kind="t4",
                             redditor_kind="t2",
                             submission_kind="t3",
                             subreddit_kind="t5",
                             trophy_kind="t6",
                             oauth_url="https://oauth.reddit.com",
                             reddit_url="https://www.reddit.com",
                             short_url="https://redd.it",
                             ratelimit_seconds=5,
                             timeout=16) #create the praw reddit object
        num_processes = min(multiprocessing.cpu_count(), len(args.subreddits)) #choosing an optimal number of parallel processes to use for scraping

        map_func = functools.partial(scrape_subreddit, reddit, args.search_limit) #create a partial function because the map function doesn't take more than one argument

        with multiprocessing.Pool(num_processes) as p:
            list_of_lists_urls = p.map(map_func, args.subreddits, chunksize=1) #parallely run the scrape_subreddit function for all subreddits

        post_urls = [url for subredditurls in list_of_lists_urls for url in subredditurls] #flatten the list

        post_urls = write_urls_to_cache(post_urls, cache_file_path)

    return post_urls


def post_url_to_video_url(url, regex):

    if url.endswith('.mp4') or url.endswith('.gifv') or url.endswith('.webm'):
        return gifvmp4(url)

    elif 'gfycat' in url or 'imgur' in url: #we can't directly use imgur or gfycat links and have find the video link in the webpage

        page = urllib.request.urlopen(url).read().decode('utf8')
        match = re.search(regex, page) #try and match the video url string with our regex
        url = match.group(0)
        return gifvmp4(url)

    elif 'v.redd.it' in url: #we can't directly use redd.it links and have find the full video link
        for res in ['/DASH_720.mp4', '/DASH_480.mp4', '/DASH_360.mp4']:
            try:
                urllib.request.urlopen(url + res).read()
                return gifvmp4(url + res)
            except urllib.error.HTTPError:
                continue

    return None #give up


def play_video_from_url(url):

    vid = cv2.VideoCapture(url)
    rval, frame = vid.read()

    while rval:
        cv2.imshow('press \'q\' to quit', frame)
        if cv2.waitKey(40) & 0xFF == ord('q'):
            break
        rval, frame = vid.read()

    vid.release()
    cv2.destroyAllWindows()


def main():

    parser = argparse.ArgumentParser(description = 'Play random animal videos from the commandline')
    parser.add_argument('--client-id',
                        type = str,
                        default = 'vHxB98R_R-8HYA',
                        help = 'client id for praw module to scrape reddit')
    parser.add_argument('--user-agent',
                        type = str,
                        default = 'cheermeup',
                        help = 'user agent for praw module to scrape reddit')
    parser.add_argument('--regex',
                        type = str,
                        default = 'https:\/\/(thumbs|i)\.(gfycat|imgur)\.com\/[\w-]+\.(mp4|webm)',
                        help = 'regex pattern to match for video urls')
    parser.add_argument('--cache-file-name',
                        type = str,
                        default = 'cheermeupurls.txt',
                        help = 'file name to cache urls for furture retrieval')
    parser.add_argument('--period',
                        type = int,
                        default = 86400,
                        help = 'timeperiod in seconds after which a cache file is considered old. Default = 1 day')
    parser.add_argument('--search-limit',
                        type = int,
                        default = 100,
                        help = 'maximum number of posts to scrape from a specific subreddit')
    parser.add_argument('--force-rewrite-cache',
                        action = 'store_true',
                        help = 'force rewrite cache even if it is not old')
    parser.add_argument('--tries',
                        type = int,
                        default = 5,
                        help = 'maximum number of tries to play a video before giving up')
    parser.add_argument('--subreddits',
                        type = str,
                        nargs = '+',
                        default = ['babyelephantgifs',
                                   'partyparrot',
                                   'animalsbeingjerks',
                                   'animalsbeingderps',
                                   'animalsbeingconfused',
                                   'whatswrongwithyourdog'],
                        help = 'list of subreddits to search for videos')
    args = parser.parse_args()

    post_urls = get_post_urls(args)

    #try n number of times before giving up.
    for i in range(args.tries):
        post_url = random.choice(post_urls)

        try:
            video_url = post_url_to_video_url(post_url, args.regex)
            assert video_url is not None
            play_video_from_url(video_url)
            break

        except:
            continue


if __name__ == '__main__':
    multiprocessing.freeze_support() #required for building windows binary
    main()
