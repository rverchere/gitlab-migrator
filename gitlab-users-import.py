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
    parser.add_argument('-i', '--input', type=str, help='input file', default='users.json')
    args = parser.parse_args()

    gl = gitlab.Gitlab(args.hostname, private_token=args.token)

    with open(args.input, 'r') as f:
        json_users = json.load(f)
        for json_user in json_users:
            try:
                g_user = gl.users.create(json_user)
                print("%s created with id %s" % (json_user['email'], g_user.id))
            except (gitlab.exceptions.GitlabCreateError, gitlab.exceptions.GitlabHttpError) as e:
                print("Cannot create user %s:  %s" % (json_user['email'], e))


