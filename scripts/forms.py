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


class IllegalStateParser(HTMLParser):
    """
    pulls out error codes from data sections
    """
    def __init__(self, data):
        """
        :param data: string 
        """
        HTMLParser.__init__(self)
        self.data = data
        self.results = False

    def handle_data(self, data):
        if self.data in data:
            self.results = True


class XSRFParser(HTMLParser):
    """
    Pulls data out of a tag, name, value setup
    """
    def __init__(self, tag, type=None, name=None, value=None):
        """
        :param tag: string
        :param type: string
        :param name: string
        :param value: string
        """
        HTMLParser.__init__(self)
        self.recording = 0
        self.data = []
        self.tag = tag
        self.type = type
        self.name = name
        self.value = value

    def handle_starttag(self, tag, attrs):
        if tag != self.tag:
            return

        if self.recording:
            self.recording += 1
            return

        if self.name:
            dict_parsed = {}
            for name, value in attrs:
                dict_parsed[name] = value
            if dict_parsed['type'] == self.type and dict_parsed['name'] == self.name:
                self.data = dict_parsed['value']
            else:
                return
            self.recording = 1

        if not self.name:
            # print "getting tag"
            if tag == self.tag:
                # print "tag gotten, adding recording"
                self.recording = 1

    def handle_endtag(self, tag):
        if tag == self.tag and self.recording:
            # print "clearing tag"
            self.recording -= 1

time.sleep(10)

z = file('/home/vagrant/PycharmProjects/bamboo/bitbucket/bitbucketkey').read()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Host': 'localhost:8085'
}

database_form = {
    'locale': "en_US",
    'step': "database",
    'internal': "true",
    'type': "postgres",
    'hostname': "",
    'port': "5432",
    'database': "",
    'username': "",
    'password': "",
    'submit': "",
    'atl_token': "",
}

keycode_form = {
    'step': 'settings',
    'applicationTitle': 'Bitbucket',
    'baseUrl': 'http://10.0.2.15:7990',
    'license-type': 'false',
    'license': str(z),
    'licenseDisplay': str(z),
    'submit': 'Next',
    'atl_token': ''
}

admin_form = {
    'step': 'user',
    'username': 'bamboo',
    'fullname': 'test',
    'email': 'test@test.test',
    'password': 'test',
    'confirmPassword': 'test',
    'skipJira': 'Go+to+Bitbucket',
    'atl_token': ''
}

r = requests.session()

x = 1
while x != 0:
    try:
        response = r.get(
            url='http://10.0.2.15:7990/setup',
            headers=headers
        )
        parser_A = IllegalStateParser(data="starting up")
        parser_A.feed(response.text)
        parser_B = IllegalStateParser(data="Atlassian Bitbucket - Starting")
        parser_B.feed(response.text)
        parser_end = IllegalStateParser(data="Welcome to Bitbucket")
        parser_end.feed(response.text)
        if parser_A.results or parser_B.results:
            print "Atlassian Bitbucket is starting up"
            time.sleep(1)
            x += 1
        elif parser_end.results:
            x = 0
        else:
            parsed = MyHTMLParser()
            parsed.feed(response.text)
            print "unexpected UI"
            raise Exception

    except ConnectionError as e:
        print "server still building"
        time.sleep(1)
        x += 1
    if x == 260:
        print "server taking too long to start"
        raise Exception


response = r.post(
    url="http://localhost:7990/setup",
    headers=headers,
    # cookies=cookies,
    data=database_form
)

parsed = XSRFParser(tag='input', type='hidden', name='atl_token')
parsed.feed(response.text)

cookies = {
    'atl.xsrf.token': parsed.data
}

database_form["atl_token"] = parsed.data

response = r.post(
    url="http://localhost:7990/setup",
    headers=headers,
    cookies=cookies,
    data=database_form
)

parser_A = IllegalStateParser(data="I have a Bitbucket license key")
parser_A.feed(response.text)
if not parser_A.results:
    print "Not at license screen, failing"
    raise Exception

keycode_form['atl_token'] = database_form['atl_token']

response = r.post(
    url="http://localhost:7990/setup",
    headers=headers,
    cookies=cookies,
    data=keycode_form
)

parser_A = IllegalStateParser(data='Administrator account setup')
parser_A.feed(response.text)
if not parser_A.results:
    print "Not at administrator screen, failing"
    raise Exception

admin_form['atl_token'] = keycode_form['atl_token']

response = r.post(
    url="http://localhost:7990/setup",
    headers=headers,
    cookies=cookies,
    data=admin_form
)

parser_A = IllegalStateParser(data='Log in - Bitbucket')
parser_A.feed(response.text)
if not parser_A.results:
    print "Not Login Screen, failing"
    raise Exception

print "build complete"

