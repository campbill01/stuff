__author__ = 'bill'
import requests
#from mechanize import Browser, ParseResponse
sysman='http://www.indeed.com/jobs?q=linux+system+administrator+%24120%2C000&l=02703&sort=date&radius=15&rq=1'
devops='http://www.indeed.com/jobs?q=linux+devops+%24110%2C000&l=02703&sort=date&radius=15&rq=1'
br=requests.Session()
browser=br.get(sysman)
print browser.text