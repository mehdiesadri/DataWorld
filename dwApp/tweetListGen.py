# -*- coding: utf-8 -*-
from mongoengine.queryset.visitor import Q
from dwApp.models import Tweet
import dateutil.parser
from datetime import datetime
from dateutil import parser

import utilities

__author__ = 'mehdi'


def search_tweets(query, size):
    tweets = []
    tweet_ids = []
    query_parts = str(query).split(",")
    q = Q()
    for qp in query_parts:
        q = q & Q(status__text__icontains=str(qp).strip())

    tweets_temp = Tweet.objects.filter(q).order_by('-timestamp', '-status__retweetCount', '-status__favoriteCount')[
                  :size]

    for t in tweets_temp:
        if not tweet_ids.__contains__(t.status.id):
            tweet_time = t.timestamp
            t.status.time = utilities.what_time(long(tweet_time) / 1000)
            t.status.text = utilities.text_url_to_link(t.status.text)
            t.status.score = t.status.favoriteCount + t.status.retweetCount * 1.5
            tweets.append(t.status)
            tweet_ids.append(t.status.id)

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
    tweets_temp = Tweet.objects(status__mediaEntities__exists=True).order_by(
        '-timestamp',
        '-relevance',
        '-status__retweetCount', '-status__favoriteCount')[:size]

    for t in tweets_temp:
        if not tweet_ids.__contains__(t.status.id) and (
                    not t.status.retweetedStatus or not tweet_ids.__contains__(t.status.retweetedStatus.id)):
            t.status.text = utilities.text_remove_url(t.status.text)
            t.status.time = utilities.what_time(long(t.timestamp) / 1000.0)
            tweets.append(t.status)
            tweet_ids.append(t.status.id)
            if t.status.retweetedStatus:
                tweet_ids.append(t.status.retweetedStatus.id)

    return tweets


def generate_emerging_tweets(size):
    tweets = []
    tweet_ids = []
    tweets_temp = Tweet.objects(status__retweetedStatus__exists=True).order_by('-relevance', '-timestamp',
                                                                               '-status__retweetCount')[
                  :size * 2]

    for t in tweets_temp:
        ents = assign_entities(t)
        retweetedStatus = t.status.retweetedStatus
        if retweetedStatus is not None and not tweet_ids.__contains__(retweetedStatus.id):
            retweetedStatus.time = utilities.what_time(int(t.timestamp))
            retweetedStatus.text = utilities.text_url_to_link(retweetedStatus.text)
            retweetedStatus.text = utilities.highlight_entities(retweetedStatus.text, ents)
            retweetedStatus.score = retweetedStatus.retweetCount * 1.5 + retweetedStatus.favoriteCount
            retweetedStatus.relevance = t.relevance
            tweets.append(retweetedStatus)
            tweet_ids.append(retweetedStatus.id)

    tweets = sorted(tweets, key=lambda k: k.score * k.relevance, reverse=True)
    return tweets


def generate_hot_tweets(size):
    tweets = []
    tweet_ids = []
    tweets_temp = Tweet.objects(status__retweetedStatus__exists=True).order_by('-relevance',
                                                                               '-status__retweetedStatus__retweetCount',
                                                                               '-status__retweetedStatus__favoriteCount')[
                  :size * 5]

    for t in tweets_temp:
        ents = assign_entities(t)
        retweetedStatus = t.status.retweetedStatus
        if not tweet_ids.__contains__(retweetedStatus.id):
            retweetedStatus.time = utilities.what_time(int(t.timestamp))
            retweetedStatus.text = utilities.text_url_to_link(retweetedStatus.text)
            retweetedStatus.text = utilities.highlight_entities(retweetedStatus.text, ents)
            retweetedStatus.score = retweetedStatus.retweetCount * 1.5 + retweetedStatus.favoriteCount
            retweetedStatus.relevance = t.relevance
            tweets.append(retweetedStatus)
            tweet_ids.append(retweetedStatus.id)

    tweets = sorted(tweets, key=lambda k: k.score * k.relevance, reverse=True)
    return tweets


def assign_entities(t):
    ents = {}
    for e in t.entities:
        val = t.entities[e].split('\t')[1].split(",")
        if len(val) < 1:
            continue
        i = 0
        first = val[i]
        first_parts = first.split("~~")
        while (len(first_parts) < 3):
            i = i + 1
            first = first + "," + val[i]
            first_parts = first.split("~~")
        if float(first_parts[2]) >= 1:
            ents[e] = first_parts
    return ents
