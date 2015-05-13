# -*- coding: utf-8 -*-
from django.template.loader import get_template
from django.template import Template, Context
from django.http import Http404, HttpResponse
from dwApp.models import Tweet, Report, User

import utilities
import tweetListGen
import userListGen
import time
from mongoengine import *


def get_terms():
    reports = Report.objects().order_by('-startTime')[:100]
    term_counts = {}

    for report in reports:
        frequent_patterns = report.statistics.relevantPatterns
        frequent_hashtags = report.statistics.relevantHashtags

        if not frequent_patterns is None:
            for i in frequent_patterns:
                if term_counts.__contains__(i):
                    term_counts[i] += frequent_patterns[i]
                else:
                    term_counts[i] = frequent_patterns[i]

        if not frequent_hashtags is None:
            for i in frequent_hashtags:
                if term_counts.__contains__(i):
                    term_counts[i] += frequent_hashtags[i]
                else:
                    term_counts[i] = frequent_hashtags[i]

    return term_counts


def generate_user_lists(ucount):
    u_count = userListGen.generate_most_active_users(ucount)
    u_follower_count = userListGen.generate_most_followers_users(ucount)
    u_academia = userListGen.generate_influential_users_academia(ucount)
    u_industry = userListGen.generate_influential_users_industry(ucount)

    return u_academia, u_count, u_follower_count, u_industry


def index(request):
    title = 'DataWorld'
    term_counts = get_terms()

    t_media = tweetListGen.generate_tweets_media(20)
    # t_geo = tweetListGen.generate_tweets_geo(50)
    t_emerging = tweetListGen.generate_emerging_tweets(10)
    t_hot = tweetListGen.generate_hot_tweets(10)
    t_geo = []

    u_academia, u_count, u_follower_count, u_industry = generate_user_lists(5)

    template = get_template("index.html")
    html = template.render(
        Context({'title': title, 'term_counts': term_counts,
                 'u_count': u_count, 'u_academia': u_academia, 'u_industry': u_industry,
                 'u_follower_count': u_follower_count, 't_media': t_media,
                 't_emerging': t_emerging, 't_hot': t_hot, 't_media': t_media,
                 't_geo': t_geo}))

    return HttpResponse(html)


def about(request):
    t = get_template("about.html")
    html = t.render(Context({}))
    return HttpResponse(html)


def etweets(request):
    title = 'Emerging Tweets'
    tweets = tweetListGen.generate_emerging_tweets(100)
    t = get_template("tweets.html")
    html = t.render(Context({'title': title, 't_list': tweets}))

    return HttpResponse(html)


def htweets(request):
    title = 'Hot Tweets'
    tweets = tweetListGen.generate_hot_tweets(1000)
    t = get_template("tweets.html")
    html = t.render(Context({'title': title, 't_list': tweets}))

    return HttpResponse(html)


def gtweets(request, query):
    title = 'Tweets: ' + query
    tweets = tweetListGen.search_tweets(query, 500)
    # trend = get_term_trend(query)
    trend = {}
    t = get_template("tweets.html")
    html = t.render(Context({'title': title, 't_list': tweets, 'trend': trend}))

    return HttpResponse(html)


def users(request):
    count = 200
    title = 'Influential Users'

    u_academia, u_count, u_follower_count, u_industry = generate_user_lists(count)

    t = get_template("users.html")
    html = t.render(Context(
        {'title': title,
         'u_academia': u_academia, 'u_industry': u_industry,
         'u_count': u_count,
         'u_follower_count': u_follower_count}))

    return HttpResponse(html)