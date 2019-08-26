from selenium import webdriver
from urllib.parse import urlparse
import os
import time
import tldextract as tld
from crawl_util.load_config import get_window_sizes, get_ignored_extensions
driver_path = 'chromedriver.exe'
options = webdriver.ChromeOptions()
options.headless = True
browser = webdriver.Chrome(driver_path, options=options)
t = time.localtime()
container_directory = 'crawl{}_{}_{}'.format(t.tm_hour, t.tm_min, t.tm_sec)
os.mkdir(container_directory, 0o755)
for device_name in get_window_sizes().keys():
    os.mkdir(container_directory + '/' + device_name, 0o755)

def discover_links_from_endpoint(endpoint, ROOT_DOMAIN="google.com"):
    if endpoint is None:
        return []
    full_url = urlparse('https://{}/{}'.format(ROOT_DOMAIN, urlparse(endpoint).path))
    if not _validate_url(full_url):
        return []
    browser.get(full_url.geturl())
    anchors = browser.find_elements_by_tag_name('a')
    links = list(map(lambda link: link.get_attribute('href'), anchors))
    # returns endpoints that are in the root domain
    links_from_domain = filter(
                lambda link: link is not None and tld.extract(ROOT_DOMAIN).domain == tld.extract(link).domain,
                [link for link in links if link is not None]
            )
    return list(links_from_domain)

def _validate_url(full_url):
    # full_url is a parsed url
    if any([full_url.path.endswith(ext) for ext in get_ignored_extensions()]):
        print('Skipped page with ignored extension: ' + full_url.path)
        return False
    if full_url.scheme == 'mailto':
        print('Skipped mailto: ' + full_url.geturl())
        return False
    return True


def crawl_endpoints(endpoints, base_screenshot_dir="", ROOT_DOMAIN='google.com',  max_pages=10):
    crawled = 0
    for index, ep in enumerate(endpoints):
        full_url = urlparse(ep)
        if crawled >= max_pages:
            print('! Max number of pages reached, aborting !')
            break

        # Deciding whether we want to visit this page or not:
        if not _validate_url(full_url):
            continue
        browser.get(full_url.geturl())
        for device in get_window_sizes().items():
            device_name, size = device
            height, width = size
            browser.set_window_size(height, width)
            screengrab_path = '{}/{}/screen_{}.png'.format(container_directory, device_name, ''.join([c for c in full_url.path if c.isalnum()]))
            S = lambda X: browser.execute_script('return document.body.parentNode.scroll' + X)
            browser.set_window_size(S('Width'), S('Height'))  # May need manual adjustment
            browser.find_element_by_tag_name('body').screenshot(screengrab_path)
            crawled += 1
