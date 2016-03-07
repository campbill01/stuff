#!/usr/bin/env python
#!/usr/local/bin/env python
__author__ = 'bcampbell'
import requests
import json
import pprint
from sys import exit
requests.packages.urllib3.disable_warnings()
#
URL='https://platform.foo.com/kraken-security/user/login'
AGENCY_URL='https://platform.foo.com/kraken-security/agency'
USERNAME='krakenadmin@foo.com'
PASSWORD='REDACTED'
br=requests.Session()
try:
    browser=br.post(URL,json={"username":"krakenadmin@foo.com","clearTextPassword":"REDACTED"})
    browser=br.get(AGENCY_URL, timeout=5.0)
    #print(browser.headers['content-type'])
    #data=json.loads(browser.text)
    data=json.loads(browser.content)
    #pprint.pprint(data)
    count=len(data['result'])
except requests.exceptions.RequestException as e:
    print e
    exit(2)
except:
    print (" Platform returned an unknown error")
    exit(2)
#n=0
#for i in data['result']:
#    print n
#    print (i)
#    n+=1
#print count
if count <= 1:
    print "System Error: Login completed, but no agencies returned"
    exit(2)
else:
    print " Platform is functioning normally"
    exit(0)

