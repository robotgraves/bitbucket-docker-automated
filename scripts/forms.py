import requests
from requests import ConnectionError
import json
import time
from HTMLParser import HTMLParser


class MyHTMLParser(HTMLParser):

    """
    Debugging parser, useful for printing out the whole web page as a parsed set of content
    """

    def handle_starttag(self, tag, attrs):
        print "encountered a start tag:", tag
        for attr in attrs:
            print "     attr:", attr

    def handle_endtag(self, tag):
        print "encountered an end tag:", tag

    def handle_data(self, data):
        print "encountered some data", data



z = file('/home/vagrant/PycharmProjects/bamboo/bitbucket/bitbucketkey').read()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Host': 'localhost:8085'
}

r = requests.session()

x = 1
while x != 0:
    try:
        response = r.get(
            url='http://10.0.2.15:7990/setup',
            headers=headers
        )
        x = 0
    except ConnectionError as e:
        print "server still building"
        time.sleep(1)
        x += 1
    if x == 30:
        print "server taking too long to start"
        raise Exception

r = MyHTMLParser()
r.feed(response.text)
