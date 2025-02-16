# Kiranico Scraper

A good, old fashioned web scraper to get static data from the Kiranico Monster Hunter Database. Static implies that it cannot get any data that is loaded from their private servers via API requests when you click buttons which load dynamic data onto their site. So be informed that some data will be missing!

## Useful Info

There are 2 spiders in this project:

- `LocalDownloadSpider` which writes the HTML content of any information useful to this project and writes them to the `html` folder. These files are included for convenience, but that's how they got there. It also has the benefit of being able to write parsers without being connected to the internet (yay!)

- `KiranicoSpider` which goes through those files in the `html` folder and scrapes that data with specialized parsers and both writes this data to CSV files as well as creating tables for the data and writing that data to those files, if has a connection to Postgresql.


## Running Spiders

This project relies on the `scrapy` library as the engine to scrape HTML data. Each spider has their own name which is the class name of the spider without the `Spider` suffix i.e. `KiranicoSpider` is `kiranico`.

```bash
$ scrapy crawl kiranico
```

If you want to play around with the response data in any of the local HTML files, do the following:

```bash
$ scrapy shell ./kiranico_scraper/html/folder/file-to-parse.html
```

Read the [Scrapy Docs](https://docs.scrapy.org/en/latest/intro/overview.html) for more information.
