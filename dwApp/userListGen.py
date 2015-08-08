# -*- coding: utf-8 -*-

from mongoengine.queryset.visitor import Q
from dwApp.models import User

__author__ = 'mehdi'


def generate_most_followers_users(size):
    temp_users = User.objects().order_by('-userInfo__followersCount')[:size]
    users = []
    for user in temp_users:
        u = user.userInfo
        u.score = user.userInfo.followersCount
        users.append(u)
    return users


def generate_most_active_users(size):
    temp_users = User.objects().order_by('-statistics__relevantTweetCount__value')[:size]
    users = []
    for user in temp_users:
        u = user.userInfo
        u.score = user.statistics.relevantTweetCount.value
        users.append(u)
    return users


def generate_influential_users_academia(size):
    prof = Q(userInfo__description__icontains='university') & Q(userInfo__description__icontains='professor')
    school = Q(userInfo__description__icontains='university') & Q(userInfo__description__icontains='school') & Q(
        userInfo__description__icontains='data')
    dept = Q(userInfo__description__icontains='university') & Q(userInfo__description__icontains='department') & Q(
        userInfo__description__icontains='data')
    udb = Q(userInfo__description__icontains='university') & Q(userInfo__description__icontains='database')
    edu = Q(userInfo__url__icontains='.edu') & Q(userInfo__description__icontains='data')
    phd = Q(userInfo__description__icontains='phd') & Q(userInfo__description__icontains='student') & Q(
        userInfo__description__icontains='data')

    temp_users = User.objects.filter(prof | school | dept | udb | edu | phd).order_by(
        '-statistics__relevantTweetCount__value')[:size]

    users = []
    for user in temp_users:
        u = user.userInfo
        u.score = user.statistics.relevantTweetCount.value
        users.append(u)

    return users


def generate_influential_users_industry(size):
    works = Q(userInfo__description__icontains='works at') & Q(userInfo__description__icontains='data')
    ent = Q(userInfo__description__icontains='entrepreneur') & Q(userInfo__description__icontains='data')
    ceo = Q(userInfo__description__icontains=' ceo ') & Q(userInfo__description__icontains='data')
    cto = Q(userInfo__description__icontains=' cto ') & Q(userInfo__description__icontains='data')
    founder = Q(userInfo__description__icontains='founder') & Q(userInfo__description__icontains='data')
    topcomp = (Q(userInfo__description__icontains='google') | Q(userInfo__description__icontains='facebook') | Q(
        userInfo__description__icontains='twitter') | Q(userInfo__description__icontains='instagram') | Q(
        userInfo__description__icontains='yelp') | Q(
        userInfo__description__icontains='yahoo') | Q(userInfo__description__icontains='microsoft') | Q(
        userInfo__description__icontains='cloudera')) & ( Q(userInfo__description__icontains='scientist') | Q(
        userInfo__description__icontains='engineer') | Q(
        userInfo__description__icontains='manager'))

    temp_users = User.objects.filter(works | ent | ceo | cto | founder | topcomp).order_by(
        '-statistics__relevantTweetCount__value')[:size]

    users = []
    for user in temp_users:
        u = user.userInfo
        u.score = user.statistics.relevantTweetCount.value
        users.append(u)

    return users
