# -*- coding: utf-8 -*-
from dwApp.sqlModels import User

__author__ = 'mehdi'


def generate_influential_users_academia(size):
    university_professor = User.objects.using('mysql').filter(description__icontains='university').filter(
        description__icontains='professor').filter(description__icontains='data')

    university_school = User.objects.using('mysql').filter(description__icontains='university').filter(
        description__icontains='school').filter(description__icontains='data')

    university_department = User.objects.using('mysql').filter(description__icontains='university').filter(
        description__icontains='department').filter(description__icontains='data')

    university_database = User.objects.using('mysql').filter(description__icontains='university').filter(
        description__icontains='database').filter(description__icontains='data')

    edu_website = User.objects.using('mysql').filter(url__icontains='.edu').filter(description__icontains='data')

    phd_student = User.objects.using('mysql').filter(description__icontains='phd').filter(
        description__icontains='student').filter(description__icontains='data')

    academia_users = university_professor | edu_website | phd_student | university_school | university_department | university_database
    academia_users = academia_users.order_by('-total_count')[:size]
    return academia_users


def generate_influential_users_industry(size):
    industry_users = User.objects.using('mysql').filter(description__icontains='works at')
    industry_users = industry_users | User.objects.using('mysql').filter(description__icontains='entrepreneur')
    industry_users = industry_users | User.objects.using('mysql').filter(description__icontains=' ceo ')
    industry_users = industry_users | User.objects.using('mysql').filter(description__icontains=' cto ')
    industry_users = industry_users | User.objects.using('mysql').filter(description__icontains='founder')
    industry_users = industry_users.order_by('-total_count')[:size]
    return industry_users
