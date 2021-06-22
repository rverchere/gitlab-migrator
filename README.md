# Gitlab Export/Import

Some scripts to export and import groups, projects and users from/to a gitlab instance.

You need some python dependencies to make it work:
* python-gitlab

*Note*: this script as not been tested so much, enhancements are welcome!

## Group and Projects

### Export
The `gitlab-export.py` script exports a group wih all its projects and subprojects, given a group name.

When using it, it generates a folder in `exports/` with the name of the group, plus:
* `_group` folder containing all groups information
 * `GROUP_NAME.tgz`: group name archive
* `subgroup\_projects\` folders containing all projects information
 * `PROJECT_PATH__PROJECT_NAME.tgz`: project archive, given the name and path

*Note*: the folders are important, as every one created is associated to sub project

#### Usage
```shell
usage: gitlab-export.py [-h] -H HOSTNAME -t TOKEN -g GROUP [-o OUTPUT] [-d DELAY]

Gitlab project exporter

optional arguments:
  -h, --help            show this help message and exit
  -H HOSTNAME, --hostname HOSTNAME
                        hostname of gitlab server
  -t TOKEN, --token TOKEN
                        private token
  -g GROUP, --group GROUP
                        root group
  -o OUTPUT, --output OUTPUT
                        output folder
  -d DELAY, --delay DELAY
                        delay between two download tentative
```

### Import
The `gitlab-import.py` script import a group wih all its projects and subprojects, given a root group name. The group will be created under this one.

It uses same folder architecture than the export script.

#### Usage
```
usage: gitlab-import.py [-h] -H HOSTNAME -t TOKEN [-r ROOT] -i INPUT [-d DELAY]

Gitlab project importer

optional arguments:
  -h, --help            show this help message and exit
  -H HOSTNAME, --hostname HOSTNAME
                        hostname of gitlab server
  -t TOKEN, --token TOKEN
                        private token
  -r ROOT, --root ROOT  root group (must exists). Must not end with '/'
  -i INPUT, --input INPUT
                        input path. Must end with '/'
  -d DELAY, --delay DELAY
                        delay between two download tentative
```

## Users

### Export
The `gitlab-users-export.py` exports users in a JSON format to a file, with the minimum required fields

#### Usage
```shell
usage: gitlab-users-export.py [-h] -H HOSTNAME -t TOKEN -o FILENAME

Gitlab users exporter

optional arguments:
  -h, --help            show this help message and exit
  -H HOSTNAME, --hostname HOSTNAME
                        hostname of gitlab server
  -t TOKEN, --token TOKEN
                        private token
  -o FILENAME, --output FILENAME
                        filename
```

#### JSON Result
```json
    {
        "email": "remi.verchere@axians.com",
        "name": "Remi",
        "username": "Verchere",
        "bio": "",
        "linkedin": "",
        "twitter": "",
        "organization": null,
        "reset_password": true
    }
```

### Import
The `gitlab-users-import.py` import users from a JSON file, with the minimum required fields

#### Usage
```
usage: gitlab-users-import.py [-h] -H HOSTNAME -t TOKEN [-i INPUT]

Gitlab users exporter

optional arguments:
  -h, --help            show this help message and exit
  -H HOSTNAME, --hostname HOSTNAME
                        hostname of gitlab server
  -t TOKEN, --token TOKEN
                        private token
  -i INPUT, --input INPUT
                        input file
```

## License

Apache-2.0 License