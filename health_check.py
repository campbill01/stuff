#!/usr/bin/env python
__author__ = 'bcampbell'
import urllib2
import json
import sys
import string
#check_kraken_stack
#set manually during testing, add parameters  later
if len(sys.argv) >=2:
    HOST=sys.argv[1]
    PORT=sys.argv[2]
else:
    HOST='10.20.1.10'
    PORT='8012'
#PORTLIST=[8010,8011,8012,8013,8014]
#SERVICES=['security','services','warehouse','email','scheduledtask']
#
#8014 has no hibernate, just deadlock
#8011 has no hibernate, has all agencies
#  (call mysql client to return total number of agencies, and iterate checking status)?
#8010,8012,8013 has hibernate and deadlock
# security:8010 services:8011 warehouse:8012 email:8013 scheduledtask:8014
def get_data(HOST,PORT):
   try:
       data={}
       status=[]
       response=urllib2.urlopen('http://{0}:{1}/healthcheck'.format(HOST,PORT))
   except urllib2.HTTPError, e:
       error=e.read()
       data=json.loads(error)
       return(1,'WARN',string.replace(str(data),'u\'','\''))
       #return('failed with error code - %s.' % e.code)
   except urllib2.URLError, e:
       return(2, 'CRITICAL', 'failed with error code -  {0}'.format(e.reason))
   except :
       print('Web Server Unknown error')
       return(3,'WARN', 'Web call failed')
   data=json.load(response)
   for key,value in data.items():
       subvalue=str(value).split(':')
       for sub in subvalue:
           if 'False' in sub:
               status.append(key)
               #print key
   if status:
       return 2,'CRITICAL',status
   else:
       return 0,'ALL OK',string.replace(str(data.keys()),'u\'','\'')

   return(data)
##
if __name__=='__main__':
    #HOST='10.20.31.10'
    #PORT='8014'
    status,state,message=get_data(HOST,PORT)
    print message, state
    #print status
    exit(status)

