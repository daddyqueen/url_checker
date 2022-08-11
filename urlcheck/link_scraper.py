# link_scraper.py
from bs4 import BeautifulSoup
import requests

from urlcheck.cli import read_cli_arg

# user_args = read_cli_arg()

def scrape_links(URL):
    '''
    scrape links from URL
    will try to format URL if not in proper format
    input: URL
    output: list of all links embedded in URL
    '''
    # clean up user input
    if not URL.startswith('http'):
        URL = 'http://' + URL
    if not URL.endswith('/'):
        URL = URL + '/'
    # request page data
    try:
        res = requests.get(URL)
    except Exception as e:
        raise e

    soup = BeautifulSoup(res.content, 'html.parser')
    link_list=[]
    for a in soup.find_all('a', href=True):
        # check format of links
        if a['href'].startswith('http'):
            link_list.append(a['href'])
        else:
            # append relative link to base url remove leading '/'
            if a['href'].startswith('/'):
                link_list.append(URL+a['href'][1:])
            else:
                link_list.append(URL+a['href'])
    return link_list


# if __name__=='__main__':
#     URL= input('Enter an address to scrape: ')
#     print(scrape_links(URL))