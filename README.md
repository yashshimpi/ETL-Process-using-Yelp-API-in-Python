# ETL-Process-using-Yelp-API-in-Python
Files Uploaded:

DataExtractor.py - It is used to collect the data using yelp api based on search criteria and store it in flatfile. 
DataFeed.py - Used to ingest database with the data from flatfile .
Database_Query.py - Program to interact with the database and fetch the search results.

Steps for executing:

Requirements:
Sql server
Python 3.5/Anaconda

Add the sql access credentials in the DataFeed.py and the yelp API access credentials in DataExtractor.py.
1.Run----$ python DataExtractor.py
This will generate the flat file with the feed-data
2.Run----$ python DataFeed.py
This will store the data from the flatfile into the SQL Server.
3.Run----$ python Database_Query.py
This is the User interactive query page which will query the database and show the results.
