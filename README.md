# Toronto Housing Scrape using Python-Scrapy

## Project Description

This project is a web scraper built using Python and Scrapy to collect housing data from various real estate websites in Toronto. The goal is to gather comprehensive data on housing listings, including details such as price, square footage, type, and other relevant attributes. The collected data is then cleaned and processed for further analysis.

## Features

- **Web Scraping**: Utilizes Scrapy to scrape housing data from multiple real estate websites.
- **Data Cleaning**: Includes functions to clean and preprocess the scraped data, such as handling missing values, converting data types, and computing additional attributes.
- **Data Analysis**: Computes useful metrics like average square footage and filters out irrelevant listings.
- **Data Export**: Exports the cleaned data to CSV and Excel formats for easy analysis and sharing.


## Data Cleaning Functions

- **`clean_sqft(data)`**: Cleans and formats the square footage data.
- **`compute_sqft_average(data)`**: Computes the average square footage.
- **`fill_na_with_zero(data)`**: Fills missing values with zero.
- **`remove_vacant_land(data)`**: Removes listings marked as vacant land.
- **`remove_office_types(data)`**: Removes listings marked as office types.
