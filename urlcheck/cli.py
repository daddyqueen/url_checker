# cli.py
# additional files needed to run program: 
#   checker.py, link_scraper.py, __main__.py
import argparse
import requests

def read_cli_arg():
    '''
    read command line args
    '''
    parser = argparse.ArgumentParser(
        prog='urlcheck', description='check connection status of url(s)',
        # exit_on_error=False
    )
    # prevents -a and -s from running together
    confilict_group = parser.add_mutually_exclusive_group()
    # pull url info from -u or -f
    input_group = parser.add_mutually_exclusive_group(required=True)

    input_group.add_argument( # get urls
        '-u',
        '--urls',
        metavar='URLs',
        nargs='+',
        type=str,
        default=[],
        help='enter one or more URLs to check their connection status',
        required=False,
    )
    input_group.add_argument( # get urls from file
        '-f',
        '--input-file',
        metavar='FILE',
        type=str,
        default='',
        help='read URLs from a file',
        required=False,
    )
    confilict_group.add_argument( # async flag True
        '-a',
        '--asynchronous',
        action='store_true',
        help='check url connectivity asynchronously',
        required=False,
    )
    confilict_group.add_argument( # scrape flag True
        '-s',
        '--scrape',
        action='store_true',
        help='scrapes all url data from input url(s)',
        required=False,
    )
    parser.add_argument( # request flag True
        '-r',
        '--request',
        action='store_true',
        help='requests status code of all urls' ,
        required=False,
    )
    parser.add_argument( # make error text file, 
    # use const and nargs=? to allow default name to be passed
        '-o',
        '--output-file',
        metavar='OUTFILE',
        nargs='?',
        action='store',
        const='urlcheck_errors.txt',
        help='outputs text file for all url errors that occur \
            during program execution',
        required=False,
    )
    return parser.parse_args()

def show_results(result, url, outfile, error=''):
    '''
    prints url connection status to terminal
    displays error type if site is unavailable
    '''
    if result:
        print('🟢 Online ~~', end=' ')
    else:
        print(f'❌ Unavailable\n\tError: "{error}"', end=' ')
        if outfile:
            make_error_file(url,error,outfile)
    print(f'"{url}"')

def show_response(url, outfile,error=None):
    '''
    prints program output to terminal if requests option was selected
    will display request respose of url input or an error  
    will save errors to outfile if option selected
    '''
    try:
        response = requests.get(url)
        if response:
            print(f'🟢 Status {response.status_code} ~~', end=' ')
        else:
            print(f'❌ Unavailable \n\t\
                Error: "{response.status_code}"', end=' ')
            if outfile:
                make_error_file(url,error,outfile)
                print('out')
    except Exception as e:
        error=str(e)
    # handle exceptions
    if error:
        print(f'❌ Unavailable \n\tError: "{error}"', end=' ')
        if outfile:
            make_error_file(url,error,outfile)
    print(f'"{url}"')

def make_error_file(url,error, outfile='urlcheck_errors.txt'):
    '''
    append errors to outfile
    input: str
    output: txt file
    '''
    with open(outfile, 'a') as f:
        f.write(f'{url}: {error}\n')
        