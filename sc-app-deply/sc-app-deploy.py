#!/usr/bin/env python3

import sys
import os
import logging
import argparse
from contextlib import redirect_stdout

def parseArguments():
    '''
    Parses the program arguments and returns the data parsed by argparse.
    '''
    parser = argparse.ArgumentParser(description='Deploy branch specific images of Schul-Cloud to a team assigned Docker Swarm machine.')

    parser.add_argument('--version', action='version', version='1.0.0')
    def add_standard_args(parser, args_to_add):
        # each command has a slightly different use of these arguments,
        # therefore just add the ones specified in `args_to_add`.
        if 'team-number' in args_to_add:
            parser.add_argument('team-number',
                                type=int,
                                help='the number of the team to identify the team machine')
        if 'ticket-id' in args_to_add:
            parser.add_argument('ticket-id',
                            type=str,
                            help='JIRA issue ID to identify the branch')

    branch_base_names = ('develop', 'master', 'hotfix', 'feature')
    subp = parser.add_subparsers(title='Branches', metavar='\n  '.join(branch_base_names))

    # develop PARSER
    develop_parser = subp.add_parser('develop',
                                      usage=(' develop '),
                                      description='Deploy latest images from develop branch')
    develop_parser.set_defaults(func=deployDevelop)

    # master PARSER
    master_parser = subp.add_parser('master',
                                      usage=(' master '),
                                      description='Deploy latest images from master branch')
    add_standard_args(master_parser,
                      ('team-number'))
    master_parser.set_defaults(func=deployMaster)

    # hotfix PARSER
    hotfix_parser = subp.add_parser('hotfix',
                                      usage=(' hotfix '),
                                      description='Deploy latest images from hotfix branch of team')
    add_standard_args(hotfix_parser,
                      ('team-number', 'ticket-id'))
    hotfix_parser.set_defaults(func=deployHotFix)

    # feature PARSER
    feature_parser = subp.add_parser('feature',
                                      usage=(' feature '),
                                      description='Deploy latest images from feature branch of team')
    add_standard_args(feature_parser,
                      ('team-number', 'ticket-id'))
    feature_parser.set_defaults(func=deployFeature)
    parser.add_argument('--debug', '-d', dest='debug', action='store_true', default=False),
    parser.add_argument("-w", "--whatif", action='store_true', help = "If set no deploy operations are executed.")

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    try:
        if sys.version_info[0] < 3 or sys.version_info[1] < 6:
            print("This script requires Python version 3.6")
            print("Python version")
            print (sys.version)
            print("Version info.")
            print (sys.version_info)          
            print(os.environ['PATH'])
            sys.exit(1)

        parsedArgs = parseArguments()
        logging.debug('Call arguments given: %s' % sys.argv[1:])
        exit(0)
    except Exception as ex:
        exit(1)
