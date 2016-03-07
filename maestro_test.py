#!/usr/bin/python
#from maestro.__main__ import *
import subprocess
FILE='/Users/bcampbell/git/docker/kraken/maestro/dev/dev_stack2.yml'
#DEFAULT_MAESTRO_FILE='maestro.yml'
#DEFAULT_MAESTRO_COMMAND='status',''
#main(DEFAULT_MAESTRO_COMMAND,FILE)
COMMAND='status'
FLAG='-f'
#this is ugly, but I was unable to get maestro __main to parse the config correctly
# not sure where I was going wrong
subprocess.call(['/usr/local/bin/maestro',FLAG,FILE,COMMAND])
