__author__ = 'mehdi'

import MySQLdb


def import_patterns(path):
    f = open(path, 'r')
    lines = f.readlines()
    patterns = {}
    category = ''
    column = ''
    for line in lines:
        if line.startswith('#'):
            category = line.replace('#', '').strip()
            patterns[category] = {}
        elif line.startswith('~'):
            column = line.replace('~', '').strip()
            cat = patterns[category]
            cat[column] = []
        else:
            if line.__len__() > 5:
                parts = line.split('-')
                cat = patterns[category]
                cat[column].append([parts[0].strip(), float(parts[1].strip())])

    return patterns


patterns = import_patterns('./user_description_patterns.txt')
db = MySQLdb.connect(host="128.195.52.58", user="mehdi", passwd="1365918", db="dwApp_user")
cur = db.cursor()
table_name = "dataworld_user"
select_query = "SELECT user_id,description,url FROM %s" % table_name
cur.execute(select_query)

for row in cur.fetchall():
    id = row[0]
    d = str(row[1])
    u = str(row[2])

    scores = {}

    for cname in patterns.keys():
        cat = patterns[cname]
        scores[cname] = []
        for colname in cat.keys():
            for p in cat[colname]:
                if colname == 'description':
                    if d.__contains__(p[0]):
                        scores[cname].append(p[1])
                elif colname == 'url':
                    if u.__contains__(p[0]):
                        scores[cname].append(p[1])

                if p[1] < .2 or p[1] > .9:
                    print p[1]

    for cname in scores.keys():
        ss = scores[cname]
        ss = sorted(ss, reverse=True)
        score = 0
        if len(ss) > 0:
            for s in ss:
                score = score + s
            score = score - ss[0]
            if len(ss) > 1:
                score = (1 - ss[0]) * (score / (len(ss) - 1))
            score = score + ss[0]

        if score > 0:
            update_query = "UPDATE %s SET %s_score=%s WHERE user_id='%s' " % (table_name, cname, str(score), id)
            print update_query
            cur.execute(update_query)

cur.close()
db.close()