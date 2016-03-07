#!/usr/bin/env python
# requires boto3 and a valid api key
import boto3
import sys
AUTO_SCALING_GROUP_NAME='dataimport-prod-m3medmium-java2'
LIFE_CYCLE_HOOK_NAME='dataimport-prod-scalein'
LIFE_CYCLE_TRANSITION='autoscaling:EC2_INSTANCE_TERMINATING'
NOTIFICATION_TARGET_ARN='arn:aws:sns:us-east-1:410719960219:SCALIN_DATAIMPORTCONSUMER_PROD'
ROLE_ARN='arn:aws:iam::410719960219:role/as-dataimportconsumer-prod'
def usage():
    print "Requires one parameter either Put(creates lifecycle hook) or Delete(removes lifecycle hook)"
    exit(0)
client=boto3.client('autoscaling')
if len(sys.argv) == 3:
    if sys.argv[2].lower() == 'test':
        AUTO_SCALING_GROUP_NAME='dataimportconsumer-dev'

if len(sys.argv) >= 2:
    if sys.argv[1].lower() == 'put':
        try:
          response=client.put_lifecycle_hook(LifecycleHookName=LIFE_CYCLE_HOOK_NAME,
                                             AutoScalingGroupName=AUTO_SCALING_GROUP_NAME,
                                             LifecycleTransition=LIFE_CYCLE_TRANSITION,
                                             NotificationTargetARN=NOTIFICATION_TARGET_ARN,
                                             RoleARN=ROLE_ARN)
        except Exception, e:
            print("failure to put lifecycle hook %s") % e
            exit(1)
    elif sys.argv[1].lower() == 'delete':
        try:
          response=client.delete_lifecycle_hook(LifecycleHookName=LIFE_CYCLE_HOOK_NAME,
                                                AutoScalingGroupName=AUTO_SCALING_GROUP_NAME)
        except Exception, e:
            print("failure to delete lifecycle hook %s") %e
            exit(1)
    else:
        usage()
else:
    usage()

print(response)
exit(0)