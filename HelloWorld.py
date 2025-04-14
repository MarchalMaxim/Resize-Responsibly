from crawl_util.crawling_tools import crawl_endpoints, discover_links_from_endpoint

links = discover_links_from_endpoint('', 'google.com')
crawl_endpoints(links, max_pages=200)