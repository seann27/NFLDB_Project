The scripts in this folder read from a large CSV play-by-play database file stored locally (~0.7 GB). This file is too big to store on github.

- build_sql_db.py parses the csv files and inserts the data into the mysql database
	- issues:
			- Need to add season/week to dataframe
			- Need to add commandline option parser
			- Need to add datetime parser
			- Functions to build metrics?
				- Manipulate DF or execute separate SQL queries?
