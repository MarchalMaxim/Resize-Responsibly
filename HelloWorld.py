from main import crawl_endpoints, discover_links_from_endpoint

links = discover_links_from_endpoint('','kuipris.nl')
crawl_endpoints(links, max_pages=20)