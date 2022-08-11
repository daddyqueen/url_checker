# __main__.py
import asyncio
import pathlib
import sys

from urlcheck.checker import is_online, is_online_async
from urlcheck.cli import read_cli_arg, show_results, show_response
from urlcheck.link_scraper import scrape_links

def main():
    ''' 
    runs url checker program 
    '''
    user_args = read_cli_arg()
    urls = _get_urls(user_args)
    to_scrape = user_args.scrape
    make_request = user_args.request
    if to_scrape:
        urls = scrape_links(to_scrape)
    if not urls:
        print('Error: no URLs avaialble to check', file=sys.stderr)
        sys.exit(1)
    if make_request and to_scrape:
        _synchronous_check(urls,True)
    elif user_args.asynchronous:
        asyncio.run(_asynchronous_check(urls))
    else:
        _synchronous_check(urls)

def _get_urls(user_args):
    '''
    pulls url information from user input
    input: str or file of str (urls)
    output: list of str (urls)
    '''
    urls=user_args.urls
    if user_args.input_file:
        urls+=_read_file_urls(user_args.input_file)
    return urls

def _read_file_urls(file):
    '''
    reads urls from a file returns list of str (urls)
    input: file with urls
    output:
        successful: list of urls from file
        file not found: empty list
        empty file: error
    '''
    file_path = pathlib.Path(file)
    if file_path.is_file():
        with file_path.open() as urls_file:
            urls = [urls.strip() for url in urls_file]
            if urls:
                return urls
            print('Error: input file "{file}" is empty',file=sys.stderr)
    else:
        print('Error: input file not found', file=sys.stderr)
    return []

async def _asynchronous_check(urls):
    '''
    check urls asynchronously
    '''
    async def _check(url):
        error = ''
        try:
            res = await is_online_async(url)
        except Exception as e:
            res = False
            error = str(e)
        # if req==None:
        #     show_results(res, url, error)
    await asyncio.gather(*(_check(url) for url in urls))

def _synchronous_check(urls,req=False):
    '''
    checks urls one by one in order
    if req=True will perform a request for each url and display the response code
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
            show_results(res, url, error)
        else:
        # getting status code for each url
            show_response(url)
            
if __name__=='__main__':
    main()
