# cli.py

import argparse
import json

def read_cli_arg():
    '''
    read command line args
    '''
    parser = argparse.ArgumentParser(
        prog='urlcheck', description='check connection status of url(s)'
    )
    parser.add_argument(
        '-u',
        '--urls',
        metavar='URLs',
        nargs='+',
        type=str,
        default=[],
        help='enter one or more URLs to check their connection status',
    )
    parser.add_argument(
        '-f',
        '--input-file',
        metavar='FILE',
        type=str,
        default='',
        help='read URLs from a file',
    )
    parser.add_argument(
        '-a',
        '--asynchronous',
        action='store_true',
        help='check connectivity asynchronously',
    )
    return parser.parse_args()

def show_results(result, url, error=''):
    '''
    prints program output to terminal
    '''
    print(f'The status of "{url}" is:', end=' ')
    if result:
        print('Online 🟢')
    else:
        print(f'Unavailable ❌ \n\tError: "{error}"')
