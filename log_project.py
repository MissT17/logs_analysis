#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import psycopg2
import datetime
from db_views import DB_views

views = DB_views()
views.views()

try:
    conn = psycopg2.connect("dbname = news")
except:
    print("I am unable to connect to the database")
cur = conn.cursor()
# cur.execute("""select log.path, count(path) as number from log
#                 group by path order by number desc limit 5;""")
# first_result=cur.fetchall()
# print('these are just logs:')
# for row in first_result:
#     print(row)
cur.execute("""select articles.title, count(title) as number
            from log, articles
            where log.path LIKE '%'  || articles.slug
            group by title order by number desc limit 3;""")
result = cur.fetchall()
print ("The results are:")
for row in result:
    print('"', row[0], '"', '-', row[1], 'views')
# cur.execute("""create view art_auth_view as
#             select articles.author, authors.name,
#             articles.title, (select count(log.path) as views
#             from log where log.path like '%' ||articles.slug)
#             from articles, authors where authors.id = articles.author
#             order by views desc;""")
# print ("the view is created")
cur.execute("""select name, sum(views) as visits
        from art_auth_view group by name order by visits desc;""")
print("selection from the view done")
result = cur.fetchall()
print ("The most viewed authors are:")
for row in result:
    print(row[0], '-', row[1], 'views')
#cur.execute("drop view art_auth_view;")
# cur.execute("""create view total_requests as
#             select date(time), count(status) as total_requests_pos
#             from log group by date;""")
# print("total_requsts view created")
# cur.execute("""create view error_view as
#             select date(time), count(status)
#             as error_requests from log where status !='200 OK'
#             group by date;""")
# print("error_view created")
# cur.execute("""create view error_perc as select error_view.date,
#             round(100.0 * error_requests/total_requests_pos, 2)
#             as percent from error_view, total_requests
#             where error_view.date=total_requests.date;""")
# print("data aggregated in one table")
cur.execute("""select * from error_perc
            where percent > 1.0 order by percent desc;""")
print("On these days more than 1% of requests lead to errors:")
errors = cur.fetchall()
for row in errors:
        date = row[0]
        date = datetime.datetime.strptime(str(date), '%Y-%m-%d').strftime('%B %d, %Y')
        #dt_obj = datetime.datetime.strftime(date, '%Y-%m-%d')
        percent = str(row[1])+'%'
        print (date, '-', percent, 'errors')
cur.execute("drop view total_requests, error_view, error_perc, art_auth_view;")
