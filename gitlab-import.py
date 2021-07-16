#!/usr/bin/python3
# -*- coding: utf-8 -*-
# vim: expandtab sw=4 ts=4:

import argparse
import gitlab
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Import projects
def import_projects(root_group, input_path):
    projects_path = os.path.join(input_path, "_projects")
    for f in os.listdir(projects_path):
        with open('%s/%s' % (projects_path, f), 'rb') as p_file:
            p_namespace = root_group # + "/" + projects_path.split("/")[-2]
            p_path = Path(f).stem.split("___")[0]
            p_name = Path(f).stem.split("___")[1]
            print("Importing Project '%s' to '%s' in '%s' (%s)" % (p_name, p_path, p_namespace, projects_path))
            try:
                output = gl.projects.import_project(file=p_file, name=p_name, path=p_path, namespace=p_namespace)
                # Get a ProjectImport object to track the import status
                project_import = gl.projects.get(output['id'], lazy=True).imports.get()
                while project_import.import_status != 'finished':
                    time.sleep(args.delay)
                    project_import.refresh()
            except gitlab.exceptions.GitlabHttpError as e:
                print("Issue with project %s in %s: %s" % (p_name, p_namespace, e))


# Import projects from all groups
def import_projects_from_groups(root_group, input_path):
    # Try to handle "/" everywhere....
    if input_path.endswith("/"):
        first_group = input_path.split("/")[-2]
    else:
        first_group = input_path.split("/")[-1]
    for r_path,d_names,f_names in os.walk(input_path):
        # We are in projects folders
        if "_projects" in d_names:
            # Try to handle "/" everywheree, again and again
            # We are in the root folder
            if len(r_path) == len(input_path) and root_group == "":
                r_group = first_group
            elif len(r_path) == len(input_path):
                r_group = root_group + "/" + first_group
            elif root_group == "":
                r_group = root_group + first_group + "/" + r_path[len(input_path):]
            else:
                r_group = root_group + "/" + first_group + "/" + r_path[len(input_path):]
            import_projects(r_group, r_path)


# Import group from an exported file in folder
def import_group(root_group, input_path):
     # Check if parent group exists and get id
    r_found = False
    parent_id = None
    if not root_group.endswith("/"):
        root = root_group + '/'
    else:
        root = root_group
    parent_group = "/".join(root.split('/')[:-1])

    if parent_group == "": # Root case
        r_found = True

    print("Import %s in parent group %s" % (input_path, parent_group))

    groups = gl.groups.list(all=True)
    for g in groups:
        if parent_group == g.full_path:
            r_found = True
            parent_id = g.id
    if r_found == False:
        print("Parent group %s not found, create it first" % parent_group)
        exit(-1)
    else:
        print("Parent group %s with id %s found" % (str(parent_group), str(parent_id)))

    group_path = os.path.join(input_path, "_group")
    g_path = group_path.split("/")[-2]
    # Check if group already exists
    for g in groups:
        if g_path == g.path and g.parent_id == parent_id:
            print("Group %s already exists in %s with parent id %s, skipping" % (g_path, root, str(parent_id)))
            return(0)

    # Convert parent id to string if not null, to avoid import error
    if parent_id is not None:
        parent_id = str(parent_id)

    for f in os.listdir(group_path):
        with open('%s/%s' % (group_path, f), 'rb') as g_file:
            print("Importing %s to %s with parent_id %s" % (Path(f).stem, group_path.split("/")[-2], parent_id))
            group = gl.groups.import_group(g_file, path=group_path.split("/")[-2], name=Path(f).stem, parent_id=parent_id)


# Main
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Gitlab project importer')
    parser.add_argument('-H', '--hostname', type=str, help='hostname of gitlab server', required=True)
    parser.add_argument('-t', '--token', type=str, help='private token', required=True)
    parser.add_argument('-r', '--root', type=str, help='root group (must exists). Must not end with \'/\'', default="")
    parser.add_argument('-i', '--input', type=str, help='input path. Must end with \'/\'', required=True)
    parser.add_argument('-d', '--delay', type=int, help='delay between two download tentative', default=30)
    args = parser.parse_args()

    if not args.input.endswith("/"):
        print("path must end with '/'")
        parser.print_help()
        exit(-1)
    if args.root.endswith("/"):
        print("root group must not end with '/'")
        parser.print_help()
        exit(-1)

    gl = gitlab.Gitlab(args.hostname, private_token=args.token)

    # Import groups (everythin is in one tgz file, also subgroups)
    import_group(args.root, args.input)

    # Import all projects from groups
    import_projects_from_groups(args.root, args.input)