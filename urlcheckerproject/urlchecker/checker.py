import asyncio
from http.client import HTTPConnection
from urllib.parse import urlparse
import aiohttp

def site_is_online(url, timeout=2):
    #return true if the target URL is online.

    #raise an exception otherwise.

    error = Exception("Unknown Error")
    parser = urlparse(url)
    host = parser.netloc or parser.path.split('/')[0]
    for port in (80, 443):
        connection = HTTPConnection(host=host, port=port, timeout=timeout)
        try:
            connection.request('HEAD', '/')
            return True
        except Exception as e:
            error = e
        finally:
            connection.close()
    raise error

async def site_is_online_async(url, timeout=2):
    #return true if the target url is online
    
    #raise an exception otherwise

    error = Exception("Unknown Error")
    parser = urlparse(url)
    host = parser.netloc or parser.path.split('/')[0]
    for scheme in ('http', 'https'):
        target_url = scheme + '://' + host
        async with aiohttp.ClientSession() as session:
            try:
                await session.head(target_url, timeout=timeout)
                return True
            except asyncio.exceptions.TimeoutError:
                error = Exception('Timed Out')
            except Exception as e:
                error = e
    raise error