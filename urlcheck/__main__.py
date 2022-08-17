# __main__.py
# additional files needed to run program: checker.py, cli.py, link_scraper.py
import asyncio
import pathlib
import sys
from urlcheck.checker import is_online, is_online_async
from urlcheck.cli import read_cli_arg, show_results, show_response, make_error_file
from urlcheck.link_scraper import scrape_links

def main():
    ''' 
    runs url checker program 
    '''
    # get user input from cli
    user_args = read_cli_arg()
    # pass input to fn to get url data
    urls = _get_urls(user_args)
    # Bool for scraping
    to_scrape = user_args.scrape
    # Bool for making request for status code
    make_request = user_args.request
    # make outfile
    outfile = user_args.output_file
    # make outfile flag for scrape_links fn to prevent error file creation
    outfile_bool = True if outfile==True else False
    # scrape each url and add to list
    if to_scrape:
        # unpack list of urls from scrape_links into one list to process
        unpacked_urls=[]
        for url in urls:
            for link in scrape_links(url,outfile_bool):
                unpacked_urls.append(link)
        urls=unpacked_urls
    # error if no urls to check
    if not urls:
        print('Error: no URLs avaialble to check', file=sys.stderr)
        sys.exit(1)
    
    # only run request option synchronously to avoid timeouts
    if make_request:
        _synchronous_check(urls,outfile,True)
    # async option is best for different base urls 
    elif user_args.asynchronous:
        asyncio.run(_asynchronous_check(urls,outfile))
    # all others default to synchronuous check
    else:
        _synchronous_check(urls,outfile)

def _get_urls(user_args) -> list:
    '''
    pulls url information from user input
    input: str or file of str (urls)
    output: list of str (urls)
    '''
    # get urls from input, default is []
    urls=_format_urls(user_args.urls)
    # if input file, unpack strs with helper fn
    if user_args.input_file:
        urls+=_read_file_urls(user_args.input_file)
    return urls

def _read_file_urls(file) -> list:
    '''
    reads urls from a file returns list of str (urls)
    input: file with urls
    output:
        successful: list of urls from file
        file not found: empty list
        empty file: error
    '''
    #find and open file from input
    file_path = pathlib.Path(file)
    if file_path.is_file():
        with file_path.open() as urls_file:
            # strip and format each str, remove any errors
            urls = [url.strip() for url in urls_file]
            if urls:
                urls=_format_urls(urls)
                return urls
            # empty file error
            print('Error: input file "{file}" is empty',file=sys.stderr)
    else:
        # incorrect file location error
        print('Error: input file not found', file=sys.stderr)
    return []

async def _asynchronous_check(urls, outfile):
    '''
    check urls asynchronously and determine online status for each link
    output prints results to console
    '''
    async def _check(url):
        error = ''
        try:
            res = await is_online_async(url)
        except Exception as e:
            res = False
            error = str(e)
        show_results(res, url, outfile,error)
    await asyncio.gather(*(_check(url) for url in urls))

def _synchronous_check(urls,outfile='',req=False):
    '''
    checks urls one by one in order that they are passed
    if req=True will perform a request for each url and display the response code
    if req=False will determine online status for each link
    output: prints results to terminal
    '''
    for url in urls:
        error = ''
        # just checking connection
        if req==False:
            try:
                res = is_online(url)
            except Exception as e:
                res=False
                error=str(e)
            show_results(res, url, outfile,error)
        else:
        # return status code for each url
            show_response(url, outfile)

def _format_urls(urls:list) -> list:
    '''
    standardizes urls for ease of use 
    appends 'http://' to the front and '/' to the end of urls as needed.
    '''
    formated_urls=[]
    for url in urls:
        if not url.startswith('http'):
            url='http://' + url
        if not url.endswith('/'):
            url= url + '/'
        formated_urls.append(url)
    return formated_urls

if __name__=='__main__':
    main()
