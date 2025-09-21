# Harvard-Cities-PDF-Scraper

This Python project uses **Selenium** to scrape city-related publications from the [Growth Lab Harvard website](https://growthlab.hks.harvard.edu/publications/policy-area/citiesregions) and automatically downloads all available PDF files.

## Features

- Scrolls through all cities listed on a page to collect their URLs.
- Visits each city page and locates PDF download links.
- Automatically downloads PDFs to a `downloads` folder.
- Handles multiple pages of city listings.
- Waits for downloads to finish before proceeding to the next file.
- Prints informative logs to track progress.

## Requirements

- Python 3.8+
- Selenium
- WebDriver Manager for Chrome
- Google Chrome browser

Install dependencies using pip:

```bash
pip install selenium webdriver-manager
