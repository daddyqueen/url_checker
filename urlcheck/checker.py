# checker.py
import aiohttp
import asyncio
# make connection with url and handle http requests
from http.client import HTTPConnection
# use to parse urls
from urllib.parse import urlparse

def is_online(url, timeout = 5):
    '''
    Returns True if website is online, raises exception if not.
    input: URL , number of seconds to try before timeout connection
    output: bool/error
    '''

    error = Exception('something went wrong')
    parser = urlparse(url)
    host = parser.netloc or parser.path.split('/')[0]
    for port in (80, 443):
        connection = HTTPConnection(host=host, port=port, timeout = timeout)
        try:
            connection.request('Head', '/')
            return True
        except Exception as e:
            error =e
        finally:
            connection.close()
    raise error
    
async def is_online_async(url,timeout=60):
    '''
    checks online status asynchronously
    Returns True if website is online, raises exception if not.
    input: URL , number of seconds to try before timeout connection
    output: bool/error
    '''
    error = Exception('unknown error')
    parser = urlparse(url)
    host = parser.netloc or parser.path.split('/')[0]
    for scheme in ('http','https'):
        target_url = scheme + '://' + host
        async with aiohttp.ClientSession() as session:
            try:
                await session.head(target_url, timeout=timeout)
                return True
            except asyncio.exceptions.TimeoutError:
                error=Exception('timed out')
            except Exception as e:
                error = e
        raise error
        