# Scraping of Real Estate Listings 🏠

Welcome to the scraping project for the real estate listings dataset from RealtyLink.org!

## Project Overview📖

This project aims to collect data on rental properties from RealtyLink.org, perform scraping using Scrapy, and conduct analysis on the collected dataset. The project aims to provide insights into the rental market, including rental prices, property locations, and property descriptions.

## Scraping Script 📜:

The project's main component is a Scrapy spider (RealtyLinkSpider) designed to scrape rental property listings from the RealtyLink.org website. 

The spider navigates through multiple listing pages, extracting property titles, addresses, descriptions, prices, and other relevant information.

# How to install 🆕:
Using GitHub
Ensure you have Python 3 installed.

## Clone the repository:

```
git clone https://github.com/goldenuni/scraper-realitylink.git
cd scraper-realitylink
```
## How to Run ▶️
1. Create a virtual environment: ```python -m venv venv```

2. Activate the virtual environment:
   - On Windows: venv\Scripts\activate
   - On macOS and Linux: source venv/bin/activate

3. Install dependencies:
  ```pip install -r requirements.txt```
4. Run the Scrapy spider to scrape data via terminal: 
```scrapy crawl realtylink -o data.json```
