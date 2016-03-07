#!/usr/bin/python
import boto
from maestro.__main__ import *
from subprocess import call
import sys
import tempfile
import yaml
#
class options_object(object):
    ##execute expects an options object to be passed to it
    #__main__ uses create_parser to create the object, but it takes command line options to assemble it

    pass
#
ec2_conn = boto.connect_ec2()
as_conn = boto.connect_autoscale()
if len(sys.argv) >= 4:
    FILE=sys.argv[1]
    COMMAND=sys.argv[2]
    TYPE=sys.argv[3]
    AUTO_SCALE_GROUP=sys.argv[4]
else:
    AUTO_SCALE_GROUP='autoscale_stack-demo'
    COMMAND='status'
    FILE='/Users/bcampbell/git/docker/kraken/maestro/demo/auto-scale_stack.yml'
    #IPADDRESS='10.20.1.22'
    TYPE='stack'
#

class use_maestro(object):
    def __init__(self,instance_number,config_file,command,ip,type):
        # uses maestro load config to parse config file and replace relevant parts
        #options=None
        options=options_object()
        options.command=command
        #options.concurrency=None
        options.file=config_file
        #options.full=False
        options.ignore_dependencies=False
        options.things=[]
        #options.with_dependencies=False
        try:
            config=load_config_from_file(config_file)
        except:
            print ('Unable to get configuration from file\n')
            return(1)
        #{'stack': {'ip': '10.20.1.11', 'docker_port': 4243, 'timeout': 30}},
        config['ships']={type: {'ip': ip, 'docker_port': 4243, 'timeout': 30},}
        instance_name=type + str(instance_number)
        config['name'] =instance_name
        temp=tempfile.NamedTemporaryFile()
        yaml.dump(config, temp)
        #
        try:
            call(['/usr/local/bin/maestro','-f',temp.name,options.command])
            temp.close()
            #temp.unlink()
        except:
            print('Error attempting to %s %s' %(command,ip))
            return(1)

#
def enumerate_group():
    try:
        #instance_number=0
        group_instances=[]
        #print (AUTO_SCALE_GROUP)
        group = as_conn.get_all_groups([AUTO_SCALE_GROUP])[0]
    #    group = as_conn.get_all_groups(['dataimport-prod-m3medmium-java2'])[0]
        instances_ids = [i.instance_id for i in group.instances]
        reservations = ec2_conn.get_all_reservations(instances_ids)
        instances = [i for r in reservations for i in r.instances]
        for instance in instances:
            #	Instance is not shutting down
            if instance.state_code < 17:
                if instance.state != 'running' :
                # instance is pending, and will pull the latest code when running
                    print("Host %s is not yet up" % (instance))
                else:
                    group_instances.append(instance.private_ip_address)
                    #a=use_maestro()
                    #a.get_maestro_data(instance_number,FILE,COMMAND,instance.private_ip_address,TYPE)
                    #instance_number +=1
        return(group_instances)
    except:
        print("Auto scale group does not exist")
        return(1)

if TYPE =="stack":
    instance_number=0
    instances=enumerate_group()
    for instance in instances:
        a=use_maestro(instance_number,FILE,COMMAND,instance.private_ip_address,TYPE)
        instance_number +=1

#finally:
ec2_conn.close()
as_conn.close()
