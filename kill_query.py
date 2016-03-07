#!/usr/bin/env python
import MySQLdb
import sys
#
dbuser='admin'
database='information_schema'

if len(sys.argv) >= 2:
    ENV=sys.argv[1]
    if ENV =='dev':
        dbhost='foobahdev-rds.czubfkmesfxs.us-east-1.rds.amazonaws.com'
        dbpass='REDACTED'
    elif ENV=='demo':
        dbhost='foobahdemo-rds.czubfkmesfxs.us-east-1.rds.amazonaws.com'
        dbpass='REDACTED'
    elif ENV=='prod':
        dbhost='foobahprod-db.czubfkmesfxs.us-east-1.rds.amazonaws.com'
        dbpass='REDACTED'
    elif ENV=='qa':
        dbhost='foobahqa-rds.czubfkmesfxs.us-east-1.rds.amazonaws.com'
        dbpass='REDACTED'
    else :
        print ('Invalid environment specified, please use dev/demo/qa/prod')
        exit(1)
else :
    print('Usage: kill_query.py ENV(where env=dev/demo/qa/prod)')
    exit(0)
#
try:
    db=MySQLdb.connect(dbhost,dbuser,dbpass='REDACTED'
    cursor=db.cursor()
except MySQLdb.Error,e:
    print('Error connecting to %s' % dbhost)
    exit(1)
try:
    #cursor.execute("select Id  from information_schema.PROCESSLIST where DB='warehouse'  and Command='Sleep'")
    cursor.execute("select Id from information_schema.PROCESSLIST where DB='warehouse' and TIME > '180' and Command='Query'")
#
    results=cursor.fetchall()
    for row in results:
         #print ("Would have killed Id %s ") % (row[0])
         # only for test do not run on prod
         #cursor.execute('kill connection %s ' % row[0])
         cursor.execute(' kill query %s ' % row[0])
#
except MySQLdb.Error, e:
    print ('errror in sql : %s') % (e)
except:
    print "Error: unable to execute query"
db.close()

