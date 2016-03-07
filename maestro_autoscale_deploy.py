#!/usr/bin/python
import boto
from boto.ec2.autoscale import ScalingPolicy
from maestro.__main__ import *
from subprocess import call
import sys
import tempfile
from time import sleep
import yaml
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
    COMMAND='start'
    FILE='/Users/bcampbell/git/docker/kraken/maestro/demo/auto-scale_stack.yml'
    #IPADDRESS='10.20.1.22'
    TYPE='dataimport'
#
class new_maestro(object):
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
            use_maestro(temp.name,options.command)
            #call(['/usr/local/bin/maestro','-f',temp.name,options.command])
            temp.close()
            #temp.unlink()
        except:
            print('Error attempting to %s %s' %(command,ip))
            return(1)

#
class options_object(object):
    ##execute expects an options object to be passed to it
    #__main__ uses create_parser to create the object, but it takes command line options to assemble it
    pass
##############
def use_maestro(config_file,command,section=None):
    if section == None:
        call(['/usr/local/bin/maestro','-f',config_file,command])
    else:
        call(['/usr/local/bin/maestro','-f',config_file,command,section])

def use_scaling():
    check_policies()
    n=0
    group_size=len(enumerate_group())
    if (group_size != 1):
        while (n < group_size):
            scaleout()
            sleep(5)
            scalein()
            n +=1
    else:
        scaleout()

def check_policies():
    scaleout_policy=as_conn.get_all_policies(as_group=AUTO_SCALE_GROUP, policy_names=['IncreaseImmediate'])
    scalein_policy=as_conn.get_all_policies(as_group=AUTO_SCALE_GROUP, policy_names=['DecreaseImmediate'])
#
    if scaleout_policy == []:
        new_policy=ScalingPolicy(name='IncreaseImmediate', as_name=AUTO_SCALE_GROUP,scaling_adjustment=1,adjustment_type='ChangeInCapacity')
        as_conn.create_scaling_policy(new_policy)
    if scalein_policy == []:
        new_policy=ScalingPolicy(name='DecreaseImmediate', as_name=AUTO_SCALE_GROUP,scaling_adjustment=-1,adjustment_type='ChangeInCapacity')
        as_conn.create_scaling_policy(new_policy)

def scalein():
    as_conn.execute_policy('DecreaseImmediate',AUTO_SCALE_GROUP)
    print("Scaling in group %s") % AUTO_SCALE_GROUP
def scaleout():
    as_conn.execute_policy('IncreaseImmediate',AUTO_SCALE_GROUP)
    print("Scaling out group %s") % AUTO_SCALE_GROUP
#
def enumerate_group():
    try:
        group_instance=[]
     # instance_number=0
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
                    #a=new_maestro()
                    #a=new_maestro(instance_number,FILE,COMMAND,instance.private_ip_address,TYPE)
                    #instance_number +=1
                    group_instance.append(instance.private_ip_address)
        return(group_instance)
    except:
        print("Failed to enumerate autoscale group")
        return(1)

#

def do_stack(FILE,COMMAND,TYPE):
    instances=enumerate_group()
    instance_number = 0
    for instance in instances:
        a=new_maestro(instance_number,FILE,COMMAND,instance,TYPE)
        instance_number += 1
#

if TYPE =='stack':
    a=do_stack(FILE,COMMAND,TYPE)
elif TYPE =='dataimport':
    use_scaling()
elif TYPE =='scheduledtask':
    use_maestro(FILE,COMMAND,TYPE)
else:
    print("undefined type")
    exit()


#finally:
ec2_conn.close()
as_conn.close()
