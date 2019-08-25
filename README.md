# webcrawler
Webcrawler that takes screenshots of different viewports of pages it has visited.

## Installation
1. You need a webdriver for your favorite browser. This project only supports Chrome 76 at the moment.
Download link for the webdriver: https://sites.google.com/a/chromium.org/chromedriver/downloads
When you're done, unpack the .exe and place it in your IDE repository.

2. Install the dependencies by typing pip install -r requirements.txt into the terminal.

## Usage
Run HelloWorld.py to see a minimum example of what is done.
To get a full website scan, change the variable ROOT_DOMAIN in the full_scan.py file to whatever you want.
For example, if you want to scan https://google.com, set ROOT_DOMAIN = 'google.com'
