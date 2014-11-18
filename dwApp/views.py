# -*- coding: utf-8 -*-
from django.template.loader import get_template
from django.template import Template, Context
from django.http import Http404, HttpResponse
from dwApp.mongoModels import Tweet, Report
from dwApp.sqlModels import User

import utilities
import tweetListGen
import userListGen
import time


def get_last_report():
    last_report = Report.objects().order_by('-start_time').first()
    return last_report


def get_term_trend(term):
    result = []
    reports = Report.objects()
    ordered_reports = reports.order_by('-start_time')[:100]
    for indx, report in enumerate(ordered_reports):
        wc = utilities.get_word_counts(report)
        # start_time = datetime.fromtimestamp(report.start_time / 1000)
        if wc.has_key(term):
            freq = float(wc.get(term)) / float(report.tweet_count)
            result.append([-indx, freq])
        else:
            result.append([-indx, float(0)])
    return result


def index(request):
    title = 'DataWorld'
    last_report = get_last_report()
    term_counts = utilities.get_word_counts(last_report)

    t_media = tweetListGen.generate_tweets_media(20)
    # t_geo = tweetListGen.generate_tweets_geo(50)
    t_geo = []
    ucount = 5
    u_count = User.objects.using('mysql').all().order_by('-total_count')[:ucount]
    for user in u_count:
        user.score = user.total_count

    u_w_count = User.objects.using('mysql').all().order_by('-window_count')[:ucount]
    for user in u_w_count:
        user.score = user.window_count

    u_follower_count = User.objects.all().using('mysql').order_by('-follower_count')[:ucount]
    for user in u_follower_count:
        user.score = user.follower_count

    u_academia = userListGen.generate_influential_users_academia(ucount)
    for user in u_academia:
        user.score = user.total_count

    u_industry = userListGen.generate_influential_users_industry(ucount)
    for user in u_industry:
        user.score = user.total_count

    t_emerging = tweetListGen.generate_emerging_tweets(10)
    t_hot = tweetListGen.generate_hot_tweets(10)

    template = get_template("index.html")
    html = template.render(
        Context({'title': title, 'term_counts': term_counts, 'u_academia': u_academia,
                 'u_industry': u_industry,
                 'u_count': u_count,
                 'u_w_count': u_w_count,
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
    tweets = tweetListGen.search_tweets(query, 1000)
    trend = get_term_trend(query)
    t = get_template("tweets.html")
    html = t.render(Context({'title': title, 't_list': tweets, 'trend': trend}))

    return HttpResponse(html)


def users(request):
    count = 200
    title = 'Influential Users'

    u_count = User.objects.using('mysql').all().order_by('-total_count')[:count]
    for user in u_count:
        user.score = user.total_count

    u_w_count = User.objects.using('mysql').all().order_by('-window_count')[:count]
    for user in u_w_count:
        user.score = user.window_count

    u_follower_count = User.objects.all().using('mysql').order_by('-follower_count')[:count]
    for user in u_follower_count:
        user.score = user.follower_count

    start = time.time()
    u_academia = userListGen.generate_influential_users_academia(count)
    for user in u_academia:
        user.score = user.total_count

    u_industry = userListGen.generate_influential_users_industry(count)
    for user in u_industry:
        user.score = user.total_count

    t = get_template("users.html")
    html = t.render(Context(
        {'title': title,
         'u_academia': u_academia, 'u_industry': u_industry,
         'u_count': u_count,
         'u_w_count': u_w_count,
         'u_follower_count': u_follower_count}))

    return HttpResponse(html)