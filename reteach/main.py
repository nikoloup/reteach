#!/usr/bin/env python

# Copyright 2011 Adam Zapletal
#
# This file is part of Reteach
# Reteach is free software licensed under the GPLv3. See LICENSE for details.

import os
import sys
import optparse

import bb9_course

def parse_options():
    parser = optparse.OptionParser(
        usage = 'reteach [options] input.zip',
        description = 'Converts Blackboard 9 courses to Moodle 1.9 courses',
        version = 'reteach 1.0'
    )

    parser.add_option(
        '-o', '--outfile',
        action='store',
        dest='out_name',
        help='a name for the output archive'
    )

    parser.add_option(
        '-f', '--folder',
        action='store_true',
        dest='is_folder',
        help='tells reteach to expect a folder and convert all zips in it'
    )

    parser.add_option(
	'-c', '--courseid',
	action='store',
	dest='course_id',
	help='course auto increment id in moodle, needed for hard-linked files'
    )

    parser.add_option(
	'-s', '--staffinfo',
	action='store_true',
	dest='transfer_staffinfo',
	help='tells reteach to also transfer staffinfo as a section'
    )

    parser.add_option(
	'-t', '--titles',
	action='store_true',
	dest='transfer_titles',
	help='tells reteach to also transfer blackboard sections titles as moodle section titles'
    )

    (options, args) = parser.parse_args()

    if not args:
        parser.print_help()
        sys.exit(1)

    return options, args

def main():
    options, args = parse_options()

    input_path = args[0]

    if not os.path.exists(input_path):
        print 'Error: %s does not exist' % input_path
        sys.exit(1)

    if options.transfer_staffinfo:
	transfer_staffinfo = 1
    else:
	transfer_staffinfo = 0

    if options.transfer_titles:
	transfer_titles = 1
    else:
	transfer_titles = 0

    parameters = {'transfer_staffinfo':transfer_staffinfo, 'transfer_titles':transfer_titles}	

    if options.is_folder:
        if not os.path.isdir(input_path):
            print 'Error: %s is not a directory' % input_path
            sys.exit(1)

        out_path = input_path + '_converted'

        if os.path.exists(out_path):
            print 'Error: Directory %s already exists' % out_path
            sys.exit(1)

        zip_names = [f for f in os.listdir(input_path) if f.endswith('.zip')]

        if not len(zip_names):
            print 'Error: There are no zip files in %s' % input_path
            sys.exit(1)

        os.mkdir(out_path)

        if options.course_id:
                course_id = options.course_id
        else:
                course_id = 0

        for zip_name in zip_names:
            fixed_out_name = '%s_converted.zip' % zip_name[:-4]

            full_in_name = os.path.join(input_path, zip_name)
            full_out_name = os.path.join(out_path, fixed_out_name)

            try:
                bb9_course.create_moodle_zip(full_in_name, full_out_name, course_id, parameters)
            except Exception as e:
                # TODO
                print 'Error converting %s' % zip_name
		print e
	    course_id = int(course_id)+1

    else:
        if not os.path.isfile(input_path):
            print 'Error: %s is not a file' % input_path
            sys.exit(1)

        if not input_path.endswith('.zip'):
            print 'Error: %s is not a zip file' % input_path
            sys.exit(1)

        if options.out_name:
            out_name = options.out_name
        else:
            out_name = '%s_converted.zip' % input_path[:-4]

	if options.course_id:
	    course_id = options.course_id
	else:
	    course_id = 0

        bb9_course.create_moodle_zip(input_path, out_name,course_id, parameters)

if __name__ == '__main__':
    main()
