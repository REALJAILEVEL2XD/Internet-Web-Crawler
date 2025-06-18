import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import urllib.robotparser
import time

# --- Settings ---
START_URL = 'https://vlib.org/'
MAX_DEPTH = 500
USER_AGENT = 'InternetWebCrawler/1.0'
CRAWL_DELAY = 0.001

visited_urls = set()
robots_cache = {}

def can_crawl(url):
    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"

    if base_url not in robots_cache:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(base_url + "/robots.txt")
        try:
            rp.read()
            robots_cache[base_url] = rp
        except:
            robots_cache[base_url] = None

    rp = robots_cache.get(base_url)
    if rp:
        return rp.can_fetch(USER_AGENT, url)
    else:
        return False

def crawl(url, depth=0):
    if depth > MAX_DEPTH:
        return
    if url in visited_urls:
        return
    if not can_crawl(url):
        print(f"🚫 Blocked by robots.txt: {url}")
        return

    print(f"🔍 Crawling (depth {depth}): {url}")
    visited_urls.add(url)

    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(url, headers=headers, timeout=10)
        content_type = response.headers.get('Content-Type', '')

        if 'text/html' not in content_type:
            print(f"⚠️ Skipping non-HTML content: {url}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string.strip() if soup.title else "No title"
        print(f"📝 Page Title: {title}")

        external_links = []
        internal_links = []

        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('#') or href.startswith('mailto:') or href.startswith('javascript:'):
                continue
            if href.startswith('//'):
                full_url = 'https:' + href
            else:
                full_url = urljoin(url, href)

            parsed_href = urlparse(full_url)

            if parsed_href.scheme not in ['http', 'https']:
                continue

            if 'wikipedia.org' not in parsed_href.netloc:
                external_links.append(full_url)
            else:
                internal_links.append(full_url)

        print(f"🔗 Found {len(external_links)} external links and {len(internal_links)} internal links.")

        # Crawl external links first (to break out of Wikipedia)
        for link_url in external_links:
            crawl(link_url, depth + 1)

        # Then crawl internal Wikipedia links
        for link_url in internal_links:
            crawl(link_url, depth + 1)

        time.sleep(CRAWL_DELAY)

    except Exception as e:
        print(f"⚠️ Error crawling {url}: {e}")

if __name__ == '__main__':
    crawl(START_URL)
