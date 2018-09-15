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


_add_data_table_entry.__annotations__ = {'data_manager': dict, 'data_table_name': str, 'data_table_entry': dict, 'return': dict}


def assert_prefix_exists(prefix, path, prefix_type):
    prefix_exists = False
    for filename in os.listdir(path):
        if filename.startswith(prefix):
            prefix_exists = True
            break
    else:
        if not prefix_exists:
            exit("Unable to find a file with {} prefix {} in {}".format(prefix_type, prefix, path))


assert_prefix_exists.__annotations__ = {'prefix': str, 'path': str, 'prefix_type': str, 'return': None}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a data manager output for SHAPEIT reference data')
    parser.add_argument('key', help='Short key to identify this reference set (no spaces)')
    parser.add_argument('name', help='Description of reference set')
    parser.add_argument('path', help='Filesystem path to directory containing this reference set')
    parser.add_argument('reference_prefix', help='Filename prefix for the reference (.hap / .legend / .sample) files')
    parser.add_argument('map_prefix', help='Filename prefix for map files in this reference set')
    parser.add_argument('sample_prefix', help='Filename prefix for sample file in this reference set')
    parser.add_argument('output_file', type=argparse.FileType('w'), help='JSON file used to write data manager values to')
    args = parser.parse_args()

    if not os.path.exists(args.path):
        exit("Unable to find specified path {}".format(args.path))

    assert_prefix_exists(args.reference_prefix, args.path, 'reference')
    assert_prefix_exists(args.map_prefix, args.path, 'map')
    assert_prefix_exists(args.sample_prefix, args.path, 'sample')

    for column in ('key', 'name', 'path', 'reference_prefix', 'map_prefix', 'sample_prefix'):
        value = getattr(args, column)
        if '\t' in value:
            exit("TAB character found in {} argument".format(column))

    data_manager_dict = {}
    data_table_entry = dict(value=args.key, name=args.name, path=args.path,
                            reference_prefix=args.reference_prefix, map_prefix=args.map_prefix,
                            sample_prefix=args.sample_prefix)
    _add_data_table_entry(data_manager_dict, 'shapeit_ref', data_table_entry)

    args.output_file.write(json.dumps(data_manager_dict, sort_keys=True) + '\n')
