#!/usr/local/bin/env python
__author__ = 'bcampbell'
import requests
import json
import pprint
from sys import exit
requests.packages.urllib3.disable_warnings()
#
URL='https://platform.REDACTED.com/kraken-security/user/login'
AGENCY_URL='https://platform.REDACTED.com/kraken-security/agency'
USERNAME='krakenadmin@REDACTED.com'
PASSWORD='REDACTED'
br=requests.Session()
try:
    browser=br.post(URL,json={"username":"krakenadmin@REDACTED.com","clearTextPassword":"REDACTED"})
    browser=br.get(AGENCY_URL)
    #print(browser.headers['content-type'])
    #data=json.loads(browser.text)
    data=json.loads(browser.content)
    #pprint.pprint(data)
    count=len(data['result'])
except:
    print ("kraken-security returned an unknown error")
    exit(2)
#n=0
#for i in data['result']:
#    print n
#    print (i)
#    n+=1
#print count
if count <= 1:
    print "No agencies returned"
    exit(2)
else:
    print "kraken security is functioning normally"
    exit(0)
