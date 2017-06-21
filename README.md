Logs Analysis Project Description

This program allows to query the newsdata.sql using direct queries to database.

Directory Structure

In the GitHub logs_analysis project repository you will find the following files:

logproject.py - the file contains all the requests to the database
results.txt - the plain text file contaning the results of the queries
README.md - contains a short "How To" to run the program.

Pre-requisites
This project runs on the Linux-based virtual machine, so before running the code, please make sure that:
1.you setup and configure the virtual machine according to the follwoing instructions [https://d17h27t6h515a5.cloudfront.net/topher/2017/June/5948287e_fsnd-virtual-machine/fsnd-virtual-machine.zip] 
2.version 3.5.2 of Python is installed on that machine (as the code is adapted to this version of Python)
2.the newsdata.sql file is placed in the same folder as the logproject.file on your virtual machine

Installation

This version of code is based on views, so please creat the following views before you run the code:
1. open the Terminal on your computer, navigate to the vagrant folder
1. create art_auth_view
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



Download the files from the GitHub repository. It's important that all the files are saved within the same folder on your computer.
Open the terminal on your machine (if you use Mac: go to Applications > Utilities > Terminal, on Windows machines it corresponds to Start > Program Files > Accessories > Command Prompt).
Navigate in the terminal to the folder that contains the downloaded files.
Run the entertainment_center.py file.
Expected Outcome

On running the entertainment_center.py file, a new tab will open in your browser and a webpage with the posters of my favourite movies will be displayed. By clicking on a poster image, you will activate the video trailer which will be displayed in the center of the page. The video will start automatically once you click on the poster and the player window opens. The video will stop automatically and the player will be closed, if you click outside the video window or close the player. On hovering the images, a short movie description will be displayed over the poster.

License

The fresh_tomatoes.py code was provided by Udacity in its course, the rest of the files were created by the owner of this repository on the basis of the introductory course to Python class given by Udacity. All poster images were taken from Wikipedia, just like the short descriptions of the films.
