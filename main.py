from selenium import webdriver
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
import os
import time
import tldextract as tld
driver_path = 'chromedriver.exe'
browser = webdriver.Chrome(driver_path)

window_sizes = {
        'mobile': (400, 667),
        'desktop': (420, 420),
        'tablet': (1127,754)
    }

def discover_links_from_endpoint(endpoint, ROOT_DOMAIN="kuipris.nl"):

    full_url = 'https://{}/{}'.format(ROOT_DOMAIN, endpoint)
    browser.get(full_url)
    anchors = browser.find_elements_by_tag_name('a')
    links = list(map(lambda link: link.get_attribute('href'), anchors))
    # returns endpoints that are in the root domain
    links_from_domain = filter(
                lambda link: tld.extract(ROOT_DOMAIN).domain == tld.extract(link).domain,
                links
            )
    return links_from_domain


def crawl_endpoints(endpoints, base_screenshot_dir="", ROOT_DOMAIN='https://kuipris.nl/',  max_pages=10):
    # make directories
    t = time.localtime()
    container_directory = 'crawl{}_{}_{}'.format(t.tm_hour, t.tm_min, t.tm_sec)
    os.mkdir(container_directory, 0o755)
    for device_name in window_sizes.keys():
        os.mkdir(container_directory+'/'+device_name, 0o755)

    crawled = 0
    for index, ep in enumerate(endpoints):
        if crawled >= max_pages:
            break
        endpoint_directory = '{}/{}'.format(base_screenshot_dir, ep)
        full_url = urlparse(ep)
        browser.get(full_url.geturl())
        for device in window_sizes.items():
            device_name, size = device
            height, width = size
            browser.set_window_size(height, width)
            screengrab_path = '{}/{}/Screenshot{}.png'.format(container_directory, device_name, index)
            browser.get_screenshot_as_file(screengrab_path)
            crawled += 1
print('Done')

def main():
    # Crawl some webpages and take screenshots
    MAX_ITER = 100

    pass


if __name__ == "__main__":
    crawl_endpoints([''])