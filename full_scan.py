# Does a full breadth-first search on a webpage.
from crawl_util.crawling_tools import discover_links_from_endpoint, crawl_endpoints

MAX_ITER = 250

########################################################
########## YOUR SITE BASE ADDRESS HERE #################
########## E.G. site.nl                #################
########################################################
ROOT_DOMAIN = ''

visited = set()
tovisit = set()

# Genesis
outgoing = discover_links_from_endpoint('', ROOT_DOMAIN)
for link in outgoing:
    tovisit.add(link)

while len(tovisit) is not 0:
    # Get a list of unvisited nodes
    outgoing = [link for link in tovisit if link not in visited]

    # Add new endpoints to the queue
    for link in outgoing:
        for discovered in discover_links_from_endpoint(link, ROOT_DOMAIN=ROOT_DOMAIN):
            tovisit.add(discovered)
        visited.add(link)
    #  ^ Intend on visiting links in outgoing, by adding them to the visited list

    # Actually visit them
    crawl_endpoints(list(tovisit), max_pages=1000)

print('visited '+str(len(visited))+' web pages')