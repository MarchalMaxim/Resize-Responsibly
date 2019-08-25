from selenium import webdriver
from urllib.parse import urlparse
import os
import time
import tldextract as tld
from crawl_util.window_sizes import get_window_sizes
driver_path = 'chromedriver.exe'
browser = webdriver.Chrome(driver_path)
window_sizes = get_window_sizes()

t = time.localtime()
container_directory = 'crawl{}_{}_{}'.format(t.tm_hour, t.tm_min, t.tm_sec)
os.mkdir(container_directory, 0o755)
for device_name in window_sizes.keys():
    os.mkdir(container_directory + '/' + device_name, 0o755)

def discover_links_from_endpoint(endpoint, ROOT_DOMAIN="kuipris.nl"):
    if endpoint is None:
        return []
    full_url = 'https://{}/{}'.format(ROOT_DOMAIN, urlparse(endpoint).path)
    browser.get(full_url)
    anchors = browser.find_elements_by_tag_name('a')
    links = list(map(lambda link: link.get_attribute('href'), anchors))
    # returns endpoints that are in the root domain
    links_from_domain = filter(
                lambda link: link is not None and tld.extract(ROOT_DOMAIN).domain == tld.extract(link).domain,
                [link for link in links if link is not None]
            )
    return list(links_from_domain)


def crawl_endpoints(endpoints, base_screenshot_dir="", ROOT_DOMAIN='https://kuipris.nl/',  max_pages=10):
    crawled = 0
    for index, ep in enumerate(endpoints):
        if crawled >= max_pages:
            print('! Max number of pages reached, aborting !')
            break
        full_url = urlparse(ep)
        print('visiting: '+full_url.geturl())
        browser.get(full_url.geturl())
        for device in window_sizes.items():
            device_name, size = device
            height, width = size
            browser.set_window_size(height, width)
            screengrab_path = '{}/{}/screen_{}.png'.format(container_directory, device_name, ''.join([c for c in full_url.path if c.isalnum()]))
            browser.get_screenshot_as_file(screengrab_path)
            crawled += 1


