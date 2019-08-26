# Exports window sizes as a dictionary: {device_name => (height, width)}
import csv
import os
# Caches results.
window_sizes = {}
ignored_extensions = []
resolvepackage = lambda s: '' if s is None else s+'/'

def get_window_sizes():
    if len(window_sizes) is not 0:
        return window_sizes
    with open(resolvepackage(__package__)+'schermafmetingen.txt', 'r') as f:
        reader = csv.reader(f, delimiter=';')
        for line in reader:
            device, width, height = line
            device = ''.join([c for c in device if c.isalnum()])
            window_sizes[device] = (int(width), int(height))
    return window_sizes


def get_ignored_extensions():
    if len(ignored_extensions) is not 0:
        return ignored_extensions
    with open(resolvepackage(__package__)+'ignored_extensions.csv', 'r') as f:
        extensions = list(csv.reader(f, delimiter=','))
    for ext in extensions[0]: # todo this is going to break sooner or later.
        ignored_extensions.append(ext.strip())
    return ignored_extensions


x = get_ignored_extensions()
y = get_ignored_extensions()