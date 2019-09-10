# Does a full breadth-first search on a webpage.
import os
import time
from urllib.parse import urldefrag

from crawl_util.crawling_tools import discover_links_from_endpoint, crawl_endpoints, done, get_window_sizes

MAX_ITER = 1000

########################################################
########## YOUR SITE BASE ADDRESS HERE #################
########## E.G. site.nl                #################
########################################################
ROOT_DOMAIN = 'google.com'

visited = set()
discovered = set()

t = time.localtime()
container_directory = 'Scan_{}_{}_{}'.format(ROOT_DOMAIN, t.tm_mon, t.tm_mday)
os.mkdir(container_directory, 0o755)
for device_name in get_window_sizes().keys():
    os.mkdir(container_directory + '/' + device_name, 0o755)

# Genesis
outgoing = discover_links_from_endpoint('', ROOT_DOMAIN)
for link in outgoing:
    # Remove fragment from the link (efficiency)
    discovered.add(urldefrag(link)[0])

while True:
    # Get a list of unvisited nodes
    unvisited = [link for link in discovered if urldefrag(link)[0] not in visited]
    if len(unvisited) is 0:
        print('Site crawled!')
        break
    else:
        print(str(len(unvisited)) + ' unvisited links left.')
    # Add new endpoints to the queue
    for link in unvisited:
        for outgoing_link in discover_links_from_endpoint(link, ROOT_DOMAIN=ROOT_DOMAIN):
            discovered.add(urldefrag(outgoing_link)[0])
        visited.add(urldefrag(link)[0])
    #  ^ Intend on visiting links in outgoing, by adding them to the visited list

    # Actually visit them and write screenshots to disk.
    crawl_endpoints(list(unvisited), max_pages=MAX_ITER, base_screenshot_dir=container_directory)

print('Visited approximately {} web pages.')
done()
