# Exports window sizes as a dictionary: {device_name => (height, width)}
import csv
import re
window_sizes = {}
with open('crawl_util/schermafmetingen.txt', 'r') as f:
    reader = csv.reader(f, delimiter=';')
    for line in reader:
        device, width, height = line
        device = ''.join([c for c in device if c.isalnum()])
        window_sizes[device] = (int(width), int(height))

def get_window_sizes():
    return window_sizes