# -*- coding: utf-8 -*-
from django.contrib.gis.gdal import field

from dwApp.mongoModels import Tweet
from dateutil import parser

import utilities

__author__ = 'mehdi'


def search_tweets(query, size):
    tweets = []
    tweet_ids = []
    tweets_temp = Tweet.objects().order_by('-header__tweet_time', '-tweet__favorite_count').filter(
        tweet__text__icontains=str(query))[:size]
    for t in tweets_temp:
        if not tweet_ids.__contains__(t.tweet.id):
            tweet_time = t.header.tweet_time
            t.tweet.time = utilities.what_time(long(tweet_time) / 1000)
            t.tweet.text = utilities.text_url_to_link(t.tweet.text)
            tweets.append(t.tweet)
            tweet_ids.append(t.tweet.id)
    return tweets


def generate_tweets_geo(size):
    tweets = []
    tweet_ids = []
    tweets_temp = Tweet.objects(tweet__geo__ne=None)
    # | Tweet.objects(Tweet.objects(tweet__retweeted_status__geo__ne=None))
    for t in tweets_temp:
        if not tweet_ids.__contains__(t.tweet.id):
            tweet_time = t.header.tweet_time
            t.tweet.time = utilities.what_time(tweet_time)
            t.tweet.text = utilities.text_url_to_link(t.tweet.text)
            tweets.append(t.tweet)
            tweet_ids.append(t.tweet.id)
    return tweets


def generate_tweets_media(size):
    tweets = []
    tweet_ids = []
    tweets_temp = Tweet.objects(tweet__entities__media__sizes__large__w__gte=700).order_by('-header__tweet_time',
                                                                                           '-tweet__retweet_count',
                                                                                           '-tweet__favorite_count')[
                  :size]

    for t in tweets_temp:
        if not tweet_ids.__contains__(t.tweet.id) and (
                    not t.tweet.retweeted_status or not tweet_ids.__contains__(t.tweet.retweeted_status.id)):
            t.tweet.text = utilities.text_remove_url(t.tweet.text)
            t.tweet.time = utilities.what_time(long(t.header.tweet_time) / 1000.0)
            tweets.append(t.tweet)
            tweet_ids.append(t.tweet.id)
            if t.tweet.retweeted_status:
                tweet_ids.append(t.tweet.retweeted_status.id)
    return tweets


def generate_emerging_tweets(size):
    tweets = []
    tweet_ids = []
    tweets_temp = Tweet.objects().order_by('-header__org_tweet_time',
                                           '-header__tweet_time')[:size * 2]
    for t in tweets_temp:
        retweet_status = t.tweet.retweeted_status
        if not tweet_ids.__contains__(retweet_status.id):
            tweet_time = retweet_status.created_at
            tweet_time = parser.parse(tweet_time)
            retweet_status.time = utilities.what_time(int(tweet_time.strftime("%s")))
            retweet_status.text = utilities.text_url_to_link(retweet_status.text)
            retweet_status.score = retweet_status.retweet_count * 1.5 + retweet_status.favorite_count
            tweets.append(retweet_status)
            tweet_ids.append(retweet_status.id)

    tweets = sorted(tweets, key=lambda k: k.score, reverse=True)

    return tweets


def generate_hot_tweets(size):
    tweets = []
    tweet_ids = []
    tweets_temp = Tweet.objects().order_by(
        '-tweet__retweeted_status__retweet_count',
        '-tweet__retweeted_status__favorite_count')[:size * 2]

    tweets_temp2 = Tweet.objects().order_by(
        '-tweet__retweeted_status__retweet_count',
        '-tweet__retweeted_status__favorite_count')[:size * 2].distinct('tweet.retweeted_status')
    print len(tweets_temp2)

    for t in tweets_temp:
        retweet_status = t.tweet.retweeted_status
        if not tweet_ids.__contains__(retweet_status.id):
            tweet_time = retweet_status.created_at
            tweet_time = parser.parse(tweet_time)
            retweet_status.time = utilities.what_time(int(tweet_time.strftime("%s")))
            retweet_status.text = utilities.text_url_to_link(retweet_status.text)
            retweet_status.score = retweet_status.retweet_count * 1.5 + retweet_status.favorite_count
            tweets.append(retweet_status)
            tweet_ids.append(retweet_status.id)

    tweets = sorted(tweets, key=lambda k: k.score, reverse=True)
    return tweets

