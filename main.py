from selenium import webdriver
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
import os
driver_path = 'chromedriver.exe'
browser = webdriver.Chrome(driver_path)
ROOT_DOMAIN = 'kuipris.nl'
endpoints = ['onze-diensten', 'over-ons', 'veelgestelde-vragen']  # Dummy endpoints
window_sizes = {
        'mobile': (1000, 500),
        'desktop': (420, 420),
        'tablet': (123, 456)
    }

def discover_links_from_endpoint(endpoint, ROOT_DOMAIN="kuipris.nl"):
    full_url = '{}{}'.format(ROOT_DOMAIN, endpoint)
    browser.get(full_url)
    links = browser.find_elements_by_tag_name('a')
    links = map(lambda link: link.get_attribute('href'), links)
    # returns endpoints that are in the root domain
    links_from_domain = filter(lambda x: urlparse(), links)
    return links_from_domain


def crawl_endpoints(endpoints, base_screenshot_dir="", ROOT_DOMAIN='https://kuipris.nl/',window_sizes=None):

    for index, ep in enumerate(endpoints):
        endpoint_directory = '{}/{}'.format(base_screenshot_dir, ep)
        os.mkdir(endpoint_directory, 0o755)
        full_url = 'https://{}/{}'.format(ROOT_DOMAIN, ep)
        browser.get(full_url)
        for device in window_sizes.items():
            device_name, size = device
            height, width = size
            browser.set_window_size(height, width)
            screengrab_path = "{}/Screenshot_webpage_device={}_page={}.png".format(endpoint_directory, device_name, index)
            browser.get_screenshot_as_file(screengrab_path)
print('Done')

def main():
    # Crawl some webpages and take screenshots
    MAX_ITER = 100

    pass


if __name__ == "__main__":
    main()