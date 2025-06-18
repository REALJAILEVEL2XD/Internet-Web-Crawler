# Internet Web Crawler

A Python web crawler that starts from the Wikipedia main page and follows links while respecting robots.txt rules.  
Great for exploring websites and gathering links automatically!

## Features

- Respects robots.txt to avoid forbidden pages  
- Crawls both internal and external links  
- Configurable max crawl depth  
- Uses `requests` and `BeautifulSoup` for web scraping  

## Requirements

- Python 3.x  
- `requests`  
- `beautifulsoup4`  

## Installation

You can install the required Python packages with:

```bash
pip install requests beautifulsoup4
