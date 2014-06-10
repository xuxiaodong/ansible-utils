#!/usr/bin/env python
#
# name     : ansible-site.py, create playbook for ansible
# author   : Xu Xiaodong <xxdlhy@gmail.com>
# license  : GPL
# created  : 2014 Jun 10 
# modified : 2014 Jun 10
#

from collections import OrderedDict
import argparse
import yaml

# see also:
# http://stackoverflow.com/questions/16782112/can-pyyaml-dump-dict-items-in-non-alphabetical-order
def represent_ordereddict(dumper, data):
    value = []

    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)

        value.append((node_key, node_value))

    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)

yaml.add_representer(OrderedDict, represent_ordereddict)

def create_yml(name, hosts, user, roles, output):
    odict = OrderedDict()
    odict['name'] = name
    odict['hosts'] = hosts
    odict['user'] = user
    odict['roles'] = roles

    data = []
    data.append(odict)

    output += '.yml'
    stream = file(output, 'w')

    yaml.dump(data, stream, default_flow_style=False, explicit_start=True)

def parse_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', default='bootstrap server',
            help='playbook name')
    parser.add_argument('-s', '--hosts', required=True, help='playbook hosts')
    parser.add_argument('-u', '--user', default='root', help='playbook user')
    parser.add_argument('-r', '--roles', nargs='*', required=True,
            help='playbook roles')
    parser.add_argument('-o', '--output', default='temp', help='playbook output file')

    args = parser.parse_args()

    return [args.name, args.hosts, args.user, args.roles, args.output]

if __name__ == '__main__':
    args = parse_cmd()
    create_yml(*args)
