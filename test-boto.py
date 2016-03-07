#!/usr/bin/python
import boto
from boto.ec2.autoscale import ScalingPolicy
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


scaleout_policy=as_conn.get_all_policies(as_group='autoscale_stack-demo', policy_names=['IncreaseImmediate'])
scalein_policy=as_conn.get_all_policies(as_group='autoscale_stack-demo', policy_names=['DecreaseImmediate'])
#
if scaleout_policy == []:
    new_policy=ScalingPolicy(name='IncreaseImmediate', as_name='autoscale_stack-demo',scaling_adjustment=1,adjustment_type='ChangeInCapacity')
    as_conn.create_scaling_policy(new_policy)
if scalein_policy == []:
    new_policy=ScalingPolicy(name='DecreaseImmediate', as_name='autoscale_stack-demo',scaling_adjustment=-1,adjustment_type='ChangeInCapacity')
    as_conn.create_scaling_policy(new_policy)
#
