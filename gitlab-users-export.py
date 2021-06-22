#!/usr/bin/python3
# -*- coding: utf-8 -*-
# vim: expandtab sw=4 ts=4:

import argparse
import gitlab
import json
from pprint import pprint

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Gitlab users exporter')
    parser.add_argument('-H', '--hostname', type=str, help='hostname of gitlab server', required=True)
    parser.add_argument('-t', '--token', type=str, help='private token', required=True)
    parser.add_argument('-o', '--output', type=str, help='output file', default='users.json')
    args = parser.parse_args()

    gl = gitlab.Gitlab(args.hostname, private_token=args.token)
    
    json_users = []
    users = gl.users.list(all=True)
    for user in users:
        json_user = {
            "email": user.email,
            "name": user.name,
            "username": user.username,
            "bio": user.bio,
            "linkedin": user.linkedin,
            "twitter": user.twitter,
            "organization": user.organization,
            "reset_password": True
        }
        json_users.append(json_user)

    with open(args.output, 'w') as f:
        f.write(json.dumps(json_users, indent=4))



