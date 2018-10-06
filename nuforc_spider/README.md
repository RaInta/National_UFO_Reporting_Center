# Spiders and Aliens: The National UFO Reporting Center web spider 

As part of a show-case of the excellent `pandas` Python library for data analysis, this project makes use of the excellently curated [National UFO Reporting Center's online database](http://www.nuforc.org/) (see [here](../README.md) for an overview of this current project). This rich dataset is stored as a series of HTML tables on pages separated by date.

## Why do we need a spider?

An automated program that systematically traverses ('crawls') the web for information is often referred to as a 'spider'. Alternatively known as 'scraping,' this is a fairly common method of obtaining information (you may have noticed the `robots.txt` file embedded in some of your favorite websites). There are a range of tools with which to do this. We have adopted the `scrapy` scraping framework to build a spider to collect the data distributed on the National UFO Reporting Center's (NUFORC) database.

To run this spider, you'll need to install `scrapy`, using your favorite method of importing Python libraries (either `pip install scrapy` or `conda install scrapy`, if you use the Anaconda eco-system).

Then, after cloning this repo, run:

`$ scrapy crawl nuforc`

from this directory.

You should get a CSV (Comma-Separated Variable) file called "national_ufo_reports.csv", about 13 MB in size. 

---

There are two tricky parts to this spider. The first is that the NUFORC database pages don't have a 'Next' or other navigational link with which to navigate to the next page. This means that the spider queries the main page for all the links to obtain a list of base URLs (we remove the last item in this list because it's a catch-all, with limited utilty, in terms of data analysis). You don't usually have to do this if the pages have embedded navigational links. 

The second, and really the reason for making this spider in the first place (this is not the only project to attempt a web scrape of NUFORC) is that dates are handled variably within the fields of the HTML tables.  Many of the earlier date/time entries only had two digits for the year (yy), yet the archive extends from the fifteenth century to now (September 2018). This meant that most (all?) of the reports from, e.g. 1967, appear as 2067 etc.--- welcome to the future!

However, thanks to the curation efforts of NUFORC, the year and month are held as six-digit metadata in the URL for the entries; this vital information is automaticaly parsed and added to each entry by this spider.

Enjoy, Earthling!
