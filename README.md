# Logs Analysis Project Description

This program allows to query the newsdata.sql using direct queries to the database.

# Directory Structure

In the GitHub *logs_analysis* project repository you will find the following files:

  * `log_project.py` - the file contains all the requests to the database
  * `results.txt` - the plain text file containing the results of the queries
  * `README.md` - contains a short "How To" to run the program.

# Pre-requisites
This project was created on a Linux-based virtual machine with vagrant, so before running the code, please make sure that you either:
1. setup and configure the virtual machine as [follows](https://d17h27t6h515a5.cloudfront.net/topher/2017/June/5948287e_fsnd-virtual-machine/fsnd-virtual-machine.zip) 
or
2. have the following installed and created:
    * postgresql
    * python3
    * pip3 
    * psycopg2
    * download the `newsdata.sql` file [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
    * create database *news* containing the data from `newsdata.sql`

# Installation

This version of code is based on views, so please create the following views before you run the code:
1. open the Terminal or another command line interface tool on your computer, access the database *news* and insert the below mentioned requests one by one:

      *art_auth_view* - this view allows to combine in one table rather than three the names of the authors with the names of the articles and the quantity of times those articles have been viewed individually.(In the `log_project.py` after that I just sum up all the views of articles per author and display them in the order from most to least viewed). 
      ```psql
      create view art_auth_view as select articles.author, authors.name, articles.title, (select count(log.path) as views
        from log where log.path like '%' ||articles.slug) from articles, authors where authors.id = articles.author order by views desc;
      ```
      These three views will help identify the number of requests that lead to errors:
      
      *total_requests* - this view allows to sum up in one view the amount of total requests per day
      ```psql
      create view total_requests as select date(time), count(status) as total_requests_pos from log group by date;
      ```
      *error_view* - this view summs up the amount of requests per day that were not successful
      ```psql
      create view error_view as select date(time), count(status) as error_requests from log where status !='200 OK' group by date;
      ```
      *error_perc* - this view allows to calculate and round up the percentage of error requests per day
      ```psql
      create view error_perc as select error_view.date, round(100.0 * error_requests/total_requests_pos, 2) as percent from error_view,   total_requests where error_view.date=total_requests.date;
      ```
      The final request in `log_project.py` displays only the days where the number of errors exceeded 1%.
      
2. Once the views are created, close the connection with the database by clicking `Ctrl+D` on the keyboard for Mac > run the `log_project.py`. 

__Note__: The views at the end of the operations are dropped, which means that if you are willing to run the code again, you need to recreate the necessary views in the news table again. 

# Expected Outcome

On running the `log_project.py` file, you will see the results displayed directly in the Terminal. The `results.txt` file also provides a sample of results data.

# License

The setup configurations code as well as the `newsdata.sql` file were provided by Udacity in its course, the rest of the files were created by the owner of this repository.
