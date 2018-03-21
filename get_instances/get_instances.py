#!/usr/bin/env python
import boto3
import os,sys
# get credentials
#   parse config file for creds if not in env

# type of item to search (name, security group)

# find
# output ip : name

class Connection():
    def __init__(self, env=None):
        self.aws_access_key = ""
        self.aws_secret_key = ""
        self.session_token = ""
        self.get_credentials(env)
        self.conn = boto3.client()

    def get_credentials(self, env=None):
        try:
            self.aws_access_key = os.environ("AWS_ACCESS_KEY_ID")
            self.aws_secret_key = os.environ("AWS_SECRET_ACCESS_KEY")
            try:
                self.session_token = os.environ("AWS_SESSION_TOKEN")
            except KeyError as e:
                print(e)

        except KeyError as e:
            try:
                print("Access key variables not set... " + e)
                print("Looking up credentials for " + env + " in ~/.aws/credentials")
                from configparser import ConfigParser
                config = ConfigParser()
                config.read("~/.aws/credentials")
                self.aws_access_key = config.get(env, 'aws_access_key_id')
                self.aws_secret_key = config.get(env, 'aws_secret_access_key')
            except:
                print("Unable to find any methods to authenticate, exiting")
                exit(1)

class Search():
    def __init__(self, connection, region, search_item):
        client = boto3.client('ec2')
        self.instances = client.describe_instances(
            Filters = [
                {
                    'Name': 'tag:Name',
                    'Values': [search_item]
                }
            ]
        )
        self.addresses=[]
        for instance in self.instances:
            self.addresses.append(instance['Rservations']['Instances']['PrivateIpAddress'])


def get_args():
    import argparse
    parser = argparse.ArgumentParser
    parser.add_argument(
        "env", help="Environment to search")
    parser.add_argument(
        "region", help="Region to search in", default = "us-west-2")
    parser.add_argument(
        "search_item", help="Item to search for")
    args = parser.parse_args()
    return args.env, args.region, args.search_item

def main(argv):
    env, region, search_item = get_args()
    connection = Connection(env, region)
    instances = Search(connection, region)
    print(Search.instances)

if __name__ == "main":
    main(sys.argv)

