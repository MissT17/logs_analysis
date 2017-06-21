Logs Analysis Project Description

This program allows to query the newsdata.sql using direct queries to database.

Directory Structure

In the GitHub logs_analysis project repository you will find the following files:

logproject.py - the file contains all the requests to the database
results.txt - the plain text file contaning the results of the queries
README.md - contains a short "How To" to run the program.

Pre-requisites
This project runs on the Linux-based virtual machine, so before running the code, please make sure that:
1.you setup and configure the virtual machine according to the following instructions [https://d17h27t6h515a5.cloudfront.net/topher/2017/June/5948287e_fsnd-virtual-machine/fsnd-virtual-machine.zip] 
2.version 3.5.2 of Python is installed on that machine (as the code is adapted to this version of Python)
2.the newsdata.sql file is placed in the same folder as the logproject.file on your virtual machine

Installation

This version of code is based on views, so please create the following views before you run the code:
1. open the Terminal on your computer > navigate to the vagrant folder > start the virtual machine > run psql -d news > insert the below mentioned requests one by one
      create art_auth_view
      ```psql
      create view art_auth_view as select articles.author, authors.name, articles.title, (select count(log.path) as views
        from log where log.path like '%' ||articles.slug)
        from articles, authors where authors.id = articles.author
        order by views desc;
      ```
      total_requests
      ```psql
      create view total_requests as
                   select date(time), count(status) as total_requests_pos
                   from log group by date;
      ```
      error_view
      ```psql
      create view error_view as
                   select date(time), count(status)
                   as error_requests from log where status !='200 OK'
                   group by date;
      ```
      error_perc
      ```psql
      create view error_perc as select error_view.date,
                   round(100.0 * error_requests/total_requests_pos, 2)
                   as percent from error_view, total_requests
                   where error_view.date=total_requests.date;
      ```
2. Once the views are created, close the connection with the database by clicking Ctrl+D on the keyboard > run the logproject.py in the virtual achine environment. 
3. The views at the end of the operations are dropped, which means that if you are willing to run the code again, you need to recreate the necessary views in the news table again. 


Expected Outcome

On running the logproject.py file, you will see the results displayed directly in the Terminal. The results.txt file also provides a sample of results data.

License

The setup configurations cpde as well as the newsdata.sql file were provided by Udacity in its course, the rest of the files were created by the owner of this repository.
