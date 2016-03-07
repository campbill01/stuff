#!/usr/bin/env python
import boto
from os import walk,listdir,chdir
AWS_ACCESS_KEY_ID='REMOVED'
AWS_SECRET_ACCESS_KEY='REDACTED'
#
conn = boto.connect_s3(AWS_ACCESS_KEY_ID , AWS_SECRET_ACCESS_KEY)
bucket= conn.get_bucket('campbill')
chdir('/Users/bcampbell/work')
mypath='/Users/bcampbell/work'
files=[]
dirs=[]
for (dirpath,dirnames,filenames) in walk(mypath):
	files.extend(filenames)
	dirs.extend(dirnames)
	break
print dirs
from boto.s3.key import Key
for file in files:
	k = Key(bucket)
	k.key = file
	k.set_contents_from_filename(file)

