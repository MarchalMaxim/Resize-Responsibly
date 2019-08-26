# Does a full breadth-first search on a webpage.
from crawl_util.crawling_tools import discover_links_from_endpoint, crawl_endpoints
from urllib.parse import urldefrag
MAX_ITER = 1000

########################################################
########## YOUR SITE BASE ADDRESS HERE #################
########## E.G. site.nl                #################
########################################################
ROOT_DOMAIN = 'google.com'

visited = set()
discovered = set()

# Genesis
outgoing = discover_links_from_endpoint('', ROOT_DOMAIN)
for link in outgoing:
    # Remove fragment fromt the link (efficiency)
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
    crawl_endpoints(list(unvisited), max_pages=MAX_ITER)

print('Indexed '+str(len(visited))+' web pages')
