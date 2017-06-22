#!/usr/bin/env python3


import psycopg2
import datetime


try:
    conn = psycopg2.connect("dbname = news")
except:
    print("I am unable to connect to the database")
cur = conn.cursor()
cur.execute("""select articles.title, count(title) as number
            from log, articles
            where log.path LIKE '%'  || articles.slug and log.status = '200 OK'
            group by title order by number desc limit 3;""")
result = cur.fetchall()
print ("The most popular articles of all times are:")
for row in result:
    print('"'+row[0]+'"', '-', row[1], 'views')
print (' ')
cur.execute("""select name, sum(views) as visits
            from art_auth_view group by name order by visits desc;""")
result = cur.fetchall()
print ("The most popular article authors of all times are:")
for row in result:
    print(row[0], '-', row[1], 'views')
print (' ')
cur.execute("""select * from error_perc
            where percent > 1.0 order by percent desc;""")
print("On these days more than 1% of requests lead to errors:")
errors = cur.fetchall()
for row in errors:
        date = row[0]
        date = datetime.datetime.strptime(str(date), '%Y-%m-%d').strftime('%B %d, %Y')  # NOQA
        percent = str(row[1])+'%'
        print (date, '-', percent, 'errors')
cur.execute("drop view total_requests, error_view, error_perc, art_auth_view;")
