# -*- coding: utf-8 -*-

from mongoengine.queryset.visitor import Q
from dwApp.models import User

__author__ = 'mehdi'


def generate_users(size):
    users_temp = User.objects().order_by('-statistics__relevantTweetCount__value')[:size]
    for user in users_temp:
        user.score = user.statistics.relevantTweetCount.value
    return users_temp


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

    academics = User.objects.filter(prof | school | dept | udb | edu | phd).order_by(
        '-statistics__relevantTweetCount__value')[:size]

    return academics


def generate_influential_users_industry(size):
    works = Q(userInfo__description__icontains='works at') & Q(userInfo__description__icontains='data')
    ent = Q(userInfo__description__icontains='entrepreneur') & Q(userInfo__description__icontains='data')
    ceo = Q(userInfo__description__icontains=' ceo ') & Q(userInfo__description__icontains='data')
    cto = Q(userInfo__description__icontains=' cto ') & Q(userInfo__description__icontains='data')
    founder = Q(userInfo__description__icontains='founder') & Q(userInfo__description__icontains='data')

    ind = User.objects.filter(works | ent | ceo | cto | founder).order_by(
        '-statistics__relevantTweetCount__value')[:size]

    return ind
