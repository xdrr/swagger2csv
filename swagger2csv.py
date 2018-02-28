#!/usr/bin/python

import os
import json
import sys
import requests
from urlparse import urlparse

def parse_docs(url_file):
    with open(url_file, 'r') as f:
        urls = f.read()
    f.close()

    for url in urls.split('\n'):
        if url == None or url == '':
            continue

        r = requests.get(url)
        apidocs = r.json()

        if len(apidocs['apis']) < 1:
            print "This swagger doc has no APIs defined!"
            sys.exit(1)

        csv = {}

        for api in apidocs['apis']:
            domain = urlparse(url).hostname
            if domain not in csv:
                csv[domain] = []
            csv[domain].append(api['path'])

        with open('apis.csv', 'w') as f:
            f.write("domain,endpoint\n")
            for domain in csv:
                for endpoint in csv[domain]:
                    f.write("{},{}\n".format(domain,endpoint))
        f.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: {} [file containing URLs]".format(sys.argv[0])
        sys.exit(1)

    parse_docs(sys.argv[1])
