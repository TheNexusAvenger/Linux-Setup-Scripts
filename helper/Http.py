"""
TheNexusAvenger

Helpers functions for Http calls.
"""

import urllib.request


def httpGet(url: str, headers: dict[str, str] = None) -> bytes:
    """Runs an HTTP GET call.

    :param url: URL to call.
    :param headers: Additional headers to set.
    :return: The contents of the request.
    """

    request = urllib.request.Request(url)
    request.add_header("User-Agent", "NexusLinusSetupAutomation")
    if headers is not None:
        for headerName in headers.keys():
            request.add_header(headerName, headers[headerName])
    return urllib.request.urlopen(request).read()