#!/usr/bin/python3
# -*- coding: utf-8 -*-
# vim: expandtab sw=4 ts=4:

import argparse
import gitlab
import os
import sys
import time
from datetime import datetime

# Export Projects
def export_project(project, output_path, group_path):
    print("Exporting project %s (%s) with id %d" % (project.path, project.name, project.id))
    p_export = project.exports.create()

    # Wait for the 'finished' status
    p_export.refresh()
    while p_export.export_status != 'finished':
        time.sleep(args.delay)
        p_export.refresh()

    # Create output project path if no exists
    p_path = os.path.join(output_path, now, group_path, "_projects")
    os.makedirs(p_path, exist_ok=True)
    # Download the result
    with open('%s/%s___%s.tgz' % (p_path, project.path, project.name), 'wb') as f:
        p_export.download(streamed=True, action=f.write)


def export_group(group, output_path):
    print("Exporting group %s" % group.id)
    g_group = gl.groups.get(group.id)
    g_export =  g_group.exports.create()

    # Exporting group is fast, without refresh status
    time.sleep(3)

    # Create output project path if no exists
    g_path = os.path.join(output_path, now, group.full_path, "_group")
    os.makedirs(g_path, exist_ok=True)
    # Download the result
    with open('%s/%s.tgz' % (g_path, group.name), 'wb') as f:
        g_export.download(streamed=True, action=f.write)


def export_subprojects_from_group(group):
    subgroups = group.subgroups.list()
    for subgroup in subgroups:
        sgroup = gl.groups.get(subgroup.id, lazy=True)
        print("[SUBGROUP]: %s" % (subgroup.full_path))
        #export_group(subgroup, args.output)
        export_projects_from_group(sgroup)
        export_subprojects_from_group(sgroup)


def export_projects_from_group(group):
    # Get projects for the current group
    group_detail = gl.groups.get(group.id)
    projects = group_detail.projects.list()
    for project in projects:
        print("[PROJECT]: %s - %s" % (group_detail.full_path, project.name))
        export_project(gl.projects.get(project.id), args.output, group_detail.full_path)


# Main
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Gitlab project exporter')
    parser.add_argument('-H', '--hostname', type=str, help='hostname of gitlab server', required=True)
    parser.add_argument('-t', '--token', type=str, help='private token', required=True)
    parser.add_argument('-g', '--group', type=str, help='root group', required=True)
    parser.add_argument('-o', '--output', type=str, help='output folder', default="./exports/")
    parser.add_argument('-d', '--delay', type=int, help='delay between two download tentative', default=1)
    args = parser.parse_args()

    gl = gitlab.Gitlab(args.hostname, private_token=args.token)
    now = datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")

    # list all groups
    groups = gl.groups.list(all=True)
    for group in groups:
        if args.group == group.full_path:
            # Export root group
            export_group(group, args.output)

            # Export root projects from that group
            export_projects_from_group(group)

            # Export subprojects, and then get projects for these subgroups
            export_subprojects_from_group(group)
