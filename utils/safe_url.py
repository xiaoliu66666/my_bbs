from flask import request
from urllib.parse import urlparse, urljoin
from . import log

"""
urlparse:
Parse a URL into 6 components:
    <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
    Return a 6-tuple: (scheme, netloc, path, params, query, fragment).
    
urljoin:
Join a base URL and a possibly relative URL to form an absolute
    interpretation of the latter.    
"""


def is_safe_url(url):
    ref_url = urlparse(request.host_url)
    # log("ref_url跟它的类型：", ref_url, type(ref_url))
    # log("url跟它的类型：", url, type(url))
    test_url = urlparse(urljoin(request.host_url, url))
    return (test_url.scheme in ("http", "https") and
            ref_url.netloc == test_url.netloc)
