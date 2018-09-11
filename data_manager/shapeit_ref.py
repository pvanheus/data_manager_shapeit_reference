#!/usr/bin/env python3

from __future__ import division, print_function
import argparse
import json
import os
import os.path


def _add_data_table_entry(data_manager_dict, data_table_name, data_table_entry):
    data_manager_dict['data_tables'] = data_manager_dict.get('data_tables', {})
    data_manager_dict['data_tables'][data_table_name] = data_manager_dict['data_tables'].get(data_table_name, [])
    data_manager_dict['data_tables'][data_table_name].append(data_table_entry)
    return data_manager_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a data manager output for SHAPEIT reference data')
    parser.add_argument('key', help='Short key to identify this reference set (no spaces)')
    parser.add_argument('description', help='Description of reference set')
    parser.add_argument('path', help='Filesystem path to directory containing this reference set')
    parser.add_argument('prefix', help='Filename prefix for files in this reference set')
    parser.add_argument('output_file', type=argparse.FileType('w'), help='JSON file used to write data manager values to')
    args = parser.parse_args()

    if not os.path.exists(args.path):
        exit("Unable to find specified path {}".format(args.path))

    prefix_exists = False
    for filename in os.listdir(args.path):
        if filename.startswith(args.prefix):
            prefix_exists = True
            break
    else:
        if not prefix_exists:
            exit("Unable to find a file with prefix {} in {}".format(args.prefix, args.path))

    for column in ('key', 'description', 'path', 'prefix'):
        value = getattr(args, column)
        if '\t' in value:
            exit("TAB character found in {} argument".format(column))

    data_manager_dict = {}
    data_table_entry = dict(key=args.key, description=args.description, path=args.path, prefix=args.prefix)
    _add_data_table_entry(data_manager_dict, 'shapeit_ref', data_table_entry)

    args.output_file.write(json.dumps(data_manager_dict) + '\n')
