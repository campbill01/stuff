#!/usr/bin/python
import boto
"""
deploy to autoscale group
will need to take args: autoscalegroupname

"""
#
ec2_conn = boto.connect_ec2()
as_conn = boto.connect_autoscale()

try:
    group = as_conn.get_all_groups(['Demo-AutoScaleGroup'])[0]
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
            else: print(instance.private_ip_address)
		# how will we deploy code to this instance? ssh/sed maestro file
		# maybe alter maestro to take ip address as arg? or maybe call this from maestro file and populate ip addresses ?
finally:
    ec2_conn.close()
    as_conn.close()
