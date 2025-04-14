from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
import tldextract as tld
import os

from crawl_util.load_config import get_window_sizes, get_ignored_extensions

driver_path = 'chromedriver.exe'
options = webdriver.ChromeOptions()
options.headless = True

service = Service(driver_path)
browser = webdriver.Chrome(service=service, options=options)

def discover_links_from_endpoint(endpoint, ROOT_DOMAIN="google.com"):
    if endpoint is None:
        return []

    full_url = urlparse(f'https://{ROOT_DOMAIN}/{urlparse(endpoint).path}')
    if not _validate_url(full_url):
        return []

    browser.get(full_url.geturl())
    anchors = browser.find_elements(By.TAG_NAME, 'a')
    links = [link.get_attribute('href') for link in anchors]

    # Filter links from the same root domain
    links_from_domain = filter(
        lambda link: link and tld.extract(ROOT_DOMAIN).domain == tld.extract(link).domain,
        links
    )
    return list(links_from_domain)

def _validate_url(full_url):
    if any(full_url.path.endswith(ext) for ext in get_ignored_extensions()):
        print(f'Skipped page with ignored extension: {full_url.path}')
        return False
    if full_url.scheme == 'mailto':
        print(f'Skipped mailto: {full_url.geturl()}')
        return False
    return True

def _format_url(full_url):
    path = full_url.path
    return ''.join(char if char.isalnum() else '_' for char in path)

def done():
    browser.quit()

def crawl_endpoints(endpoints, base_screenshot_dir="", ROOT_DOMAIN='google.com', max_pages=10):
    crawled = 0
    for ep in endpoints:
        full_url = urlparse(ep)
        if crawled >= max_pages:
            print('! Max number of pages reached, aborting !')
            break

        if not _validate_url(full_url):
            continue

        browser.get(full_url.geturl())
        for device_name, (width, height) in get_window_sizes().items():
            browser.set_window_size(width, height)

            # Make sure output directories exist
            output_dir = os.path.join(base_screenshot_dir, device_name)
            os.makedirs(output_dir, exist_ok=True)

            screengrab_path = os.path.join(output_dir, f"{_format_url(full_url)}.png")
            # Optionally resize to full scroll height
            scroll_width = browser.execute_script('return document.body.parentNode.scrollWidth')
            scroll_height = browser.execute_script('return document.body.parentNode.scrollHeight')
            if(scroll_width == 0 or scroll_height == 0):
                continue
            browser.set_window_size(scroll_width, scroll_height)

            browser.find_element(By.TAG_NAME, 'body').screenshot(screengrab_path)
            print(f"Saved screenshot to {screengrab_path}")
            crawled += 1

if __name__ == "__main__":
    # Example usage:
    endpoints = ["https://www.google.com/search?q=test"]
    crawl_endpoints(endpoints)
    pass
