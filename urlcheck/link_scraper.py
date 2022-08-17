# link_scraper.py
# additional files needed to run program: checker.py, cli.py, __main__.py

from bs4 import BeautifulSoup
import requests
from urlcheck.cli import read_cli_arg, make_error_file

def scrape_links(url,outfile_bool=False):
    '''
    scrape links from url
    will try to format url if not in proper format
    input: url
    output: 
        success: list of all links embedded in url
        error: return [] and write error to optional outfile
    '''

    # request page data
    try:
        res = requests.get(url)
    except Exception as e:
        # res=False
        error = str(e)
        if outfile_bool:
            make_error_file(url, error)
        print(f'❌ Unavailable\n\tError: "{error}" "{url}"')
        return []

    soup = BeautifulSoup(res.content, 'html.parser')

    link_list=[]
    for a in soup.find_all('a', href=True):
        # check format of links
        if a['href'].startswith('http'):
            link_list.append(a['href'])
        else:
            # append relative link to base url remove leading '/'
            if a['href'].startswith('/'):
                link_list.append(url+a['href'][1:])
            else:
                link_list.append(url+a['href'])
    return link_list
