#! /usr/bin/env python
# -*- coding: utf-8 -*-

# What this code does:
# Given a Twitter stream in JSON format, extract corresponding text stream, using only English tweets and a subset of the JSON object fields (e.g., date, id, hashtags, urls, text)
# Example run:
# python extract-json-to-text-stream.py test-syria-tweets.json json-to-text-stream-syria.json.txt

import codecs
from datetime import datetime
import json
import os
import string
import sys
import time

def parse_json_tweet(line):
    tweet = json.loads(line)
    if tweet['lang'] != 'en':
     	return ['', '', '', [], [], []]

    date = tweet['created_at']
    id = tweet['id']
    locations = tweet['user']['location']

    if 'retweeted_status' in tweet:
    	text = tweet['retweeted_status']['text']
    else:
    	text = tweet['text']

    hashtags = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
    users = [user_mention['screen_name'] for user_mention in tweet['entities']['user_mentions']]
    urls = [url['expanded_url'] for url in tweet['entities']['urls']]

    media_urls = []
    if 'media' in tweet['entities']:
	    media_urls = [media['media_url'] for media in tweet['entities']['media']]

    return [date, id, text, hashtags, users, urls, media_urls, locations]

'''start main'''
if __name__ == "__main__":
	file_timeordered_json_tweets = codecs.open(sys.argv[1], 'r', 'utf-8')
	fout = codecs.open(sys.argv[2], 'w', 'utf-8')

	#efficient line-by-line read of big files
	for line in file_timeordered_json_tweets:
		try:
			[tweet_gmttime, tweet_id, text, hashtags, users, urls, media_urls, locations] = parse_json_tweet(line)
			try:
				c = time.strptime(tweet_gmttime.replace("+0000",''), '%a %b %d %H:%M:%S %Y')
			except:
				print "pb with tweet_gmttime", tweet_gmttime, line
				pass
			tweet_unixtime = int(time.mktime(c))
			fout.write(str([tweet_unixtime, tweet_gmttime, tweet_id, text, hashtags, users, urls, media_urls, locations]) + "\n")
		except:
			pass
 	file_timeordered_json_tweets.close()
 	fout.close()
