# -*- coding: utf-8 -*-
from dwApp.models import User

__author__ = 'mehdi'


def generate_users(size):
    users_temp = User.objects().order_by('-statistics__relevantTweetCount__value')[:size]
    for user in users_temp:
        user.score = user.statistics.relevantTweetCount.value
    return users_temp


def generate_influential_users_academia(size):
    university_professor = User.objects.filter(userInfo__description__icontains='university').filter(
        userInfo__description__icontains='professor').filter(userInfo__description__icontains='data')

    university_school = User.objects.filter(userInfo__description__icontains='university').filter(
        userInfo__description__icontains='school').filter(userInfo__description__icontains='data')

    university_department = User.objects.filter(userInfo__description__icontains='university').filter(
        userInfo__description__icontains='department').filter(userInfo__description__icontains='data')

    university_database = User.objects.filter(userInfo__description__icontains='university').filter(
        userInfo__description__icontains='database').filter(userInfo__description__icontains='data')

    edu_website = User.objects.filter(userInfo__url__icontains='.edu').filter(userInfo__description__icontains='data')

    phd_student = User.objects.filter(userInfo__description__icontains='phd').filter(
        userInfo__description__icontains='student').filter(userInfo__description__icontains='data')

    academia_users = university_professor
    academia_users = academia_users.order_by('-statistics__relevantTweetCount__value')[:size]
    return academia_users


def generate_influential_users_industry(size):
    industry_users = User.objects.filter(userInfo__description__icontains='works at')
    # industry_users = industry_users | User.objects.filter(userInfo__description__icontains='entrepreneur')
    # industry_users = industry_users | User.objects.filter(userInfo__description__icontains=' ceo ')
    # industry_users = industry_users | User.objects.filter(userInfo__description__icontains=' cto ')
    # industry_users = industry_users | User.objects.filter(userInfo__description__icontains='founder')
    industry_users = industry_users.order_by('-statistics__relevantTweetCount__value')[:size]
    return industry_users
