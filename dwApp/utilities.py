# -*- coding: utf-8 -*-
__author__ = 'mehdi'

import time
import re

common_words = {'data', 'big', 'bigdata', 'small'}


def get_word_counts(last_report):
    singles = last_report.terms
    singles = singles.replace('{', '').replace('}', '')

    count = int(last_report.tweet_count)
    terms = singles.split(', ')
    counted = {}
    for term in terms:
        term_str = term.split('=')[0]
        term_count = int(term.split('=')[1])
        if not is_common_word(term_str) and len(term_str) > 1 and term_count > 5:
            if counted.has_key(term_str):
                counted[term_str] += term_count
            else:
                counted[term_str] = term_count

    return counted


def text_url_to_link(input):
    output = ''
    s = input
    parts = re.split('[, ]+', s)
    for part in parts:
        if part.startswith('http'):
            output = output + ' ' + '<a target="_blank" href="' + part + '">(link)</a>'
        elif part.startswith('@'):
            output = output + ' ' + '<a target="_blank" href="https://twitter.com/' + part.replace('@', '').replace(':',
                                                                                                                    '') + '">' + part + '</a>'
        elif part.startswith('#'):
            output = output + ' ' + '<a target="_blank" href="https://twitter.com/search?q=%23' + part.replace('#',
                                                                                                               '').replace(
                ':',
                '') + '&src=hash">' + part + '</a>'
        elif part.__contains__('http'):
            sparts = part.split('http')
            output = output + sparts[0]
            for sp in sparts[1:]:
                output = output + '<a target="_blank" href="' + 'http' + sp + '"> (link)</a>'
        else:
            output = output + ' ' + part

    return output


def text_remove_url(input):
    output = ''
    s = input
    parts = s.split(' ')
    for part in parts:
        if not part.startswith('http'):
            output = output + ' ' + part

    return output


def is_common_word(word):
    if word in common_words:
        return True
    return False


def what_time(t):
    now = int(round(time.time()))
    diff = long(now) - long(t)
    if (diff < 30):
        return 'now'
    elif (diff < 300):
        return '5m'
    elif (diff < 1800):
        return '30m'
    elif (diff < 5500):
        return '1h'
    elif (diff < 86400):
        return str(int(diff / 3600)) + 'h'
    elif (diff < 650000):
        return str(int(diff / (24 * 3600))) + 'd'
    elif (diff < 2600000):
        return str(int(diff / (7 * 24 * 3600))) + 'w'
    else:
        return str(int(diff / (30 * 24 * 3600))) + 'mo'
