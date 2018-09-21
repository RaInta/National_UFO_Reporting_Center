#!/usr/bin/python
#
###########################################
#
# File: nuforc_scraper.py
# Author: Ra Inta
# Description: A web-crawler (spider) to harvest data from the
# National UFO Reporting Database (NUFORC; http://www.ufocenter.com/)
# Note we could have exported the result as a CSV directly, using the
# scrapy crawl nuforc -o nuforc_raw.csv
# syntax. However, we wish to enforce data alignment in the face of
# missing data elements in the HTML tables. So we instead leverage
# the built-in checks provided by pandas DataFrame and append the result
# to the CSV.
#
# Created: August 30, 2018
# Last Modified: September 12, 2018
#
###########################################

import scrapy
import pandas as pd
import numpy as np
from lxml import html
import requests

# Prepare the header for the CSV file
# Note: this is fragile. If you alter the filename or name order in the parsing
# definition, you will have to alter the following appropriately.
names = ["date_time", "year", "month", "city", "state", "shape", "duration", "posted", "url"]
csv_filename = "national_ufo_reports.csv"
with open(csv_filename, 'w') as csv_file:
     csv_file.write(','.join(names) + '\n')

def getTableElement(n, response):
    """Unfortunately scrapy doesn't seem to have convenience functions to
    handle empty table elements. To mitigate data misalignment, we explicitly
    join an empty string to the response result."""
    x_string = '//table//td[' + str(n) + ']'
    return [''.join(x.xpath('.//text()').extract()) for x in response.xpath(x_string)]

def parsePageDates(link):
    """The date_time field in the HTML tables are of the form dd/mm/yy; this does not
    capture the actual year properly (especially for dates across centuries). However, the
    full year (i.e. yyyy), along with the month (mm) _is_ encapsulated in the name of the
    HTML page containing the data. We take this as a string and slice it accordingly."""
    relative_link = link.split("/")[-1]
    year = relative_link[4:8]
    month = relative_link[8:10]
    return year, month

class UFOSpider(scrapy.Spider):
    name = "nuforc"
    # The following URLs are from the main NUFORC pages:
    base_url = "http://www.nuforc.org/webreports/"
    link_directory = base_url + 'ndxevent.html'
    # Get the list of links from the directory page
    # This is because there is no 'next' link on the data pages, so we can't
    # follow them.
    print("Base URL: " + base_url)
    link_page = requests.get(link_directory)
    link_tree = html.fromstring(link_page.content)
    linx = link_tree.xpath('//table//td//a//@href')
    linx = ["http://www.nuforc.org/webreports/" + x for x in linx]
    # Get rid of the very last item in the link list because it's a dumping
    # ground for highly uncertain reports:
    linx.pop()
    start_urls = linx

    def parse(self, response):
        # Get proper year and month from current URL
        year, month = parsePageDates(response.url)
        # Create the DataFrame for the current year + month
        scraped_df = pd.DataFrame()
        scraped_df["date_time"] = getTableElement(1, response)
        scraped_df["year"] = year
        scraped_df["month"] = month
        scraped_df["city"] = getTableElement(2, response)
        scraped_df["state"] = getTableElement(3, response)
        scraped_df["shape"] = getTableElement(4, response)
        scraped_df["duration"] = getTableElement(5, response)
        scraped_df["posted"] = getTableElement(7, response)
        # Get all the links to the summaries in one pass:
        base_url = "http://www.nuforc.org/webreports/"
        scraped_df["url"] = \
            [ base_url + x for x in response.xpath('//table//td//a//@href').extract()]
        # Append DataFrame to the CSV
        scraped_df.to_csv("national_ufo_reports.csv", mode="a", sep=",", header=False, index=False)



###########################################
# End of nuforc_scraper.py
###########################################
