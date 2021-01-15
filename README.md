# project_225

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Folkas/project_225/blob/main/LICENSE)

## Table of contents:
* [General info](#general-info)
* [Setup](#setup)
* [Features](#features)
* [Other](#other)


## General info:
This repository contains functions for Turing College module 2 spring 2 final assignment. The functions scrape ebay webpage, store data in postgreSQL tables, join and export them to .csv file

## Setup
To run this project, install it using `pip` command:
```
!pip install git+https://github.com/Folkas/project_225.git
```
The scraping function is in ```ebay_function``` module at ```functions``` directory:
```
from functions import ebay_function as eb
```
The database functions are located in ``` database ``` module at ```functions``` directory:
```
from functions import database as db
```

## Features:
In ebay_function:
* category_no() - assigns number to the items (1 for bracelet, 2 for shoes and 3 for dress)
* collect_ebay(no_examples, keyword) - performs web scraping for keyword input for no_examples number of samples

In database:
* create_tables() - creates two SQL type tables for scraped items from ebay webpage in Heroku database: category (id: int, category: str) and ebay (id: serial, category: int, title: varchar, price: varchar, urlItem: varchar, urlImage: varchar)
* insert_data_into_categories() - inserts data into previously created categories table in Heroku database for scraped items from the ebay website.
* insert_data_into_ebay(dataframe) - inserts data from pandas dataframe into previously created ebay table in Heroku database for scraped items from the ebay website
* join_to_csv() - joins ebay and categories tables into a single table using LEFT JOIN and exports to ebay_data.csv file

## Other
* Many thanks to Valdas and Karolis for help building this project!
