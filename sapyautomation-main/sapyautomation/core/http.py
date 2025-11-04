import requests


def get_request(url,  # pylint: disable=too-many-arguments
                params=None, allow_redirects=True, auth=None,
                cert=None, cookies=None, headers=None, proxies=None,
                stream=False, timeout=None, verify=True) -> object:
    """This method sends a get request to a generic url

        This method receives an url mandatory from the user,
        and other type of variables that are not
        mandatory. This gets an specific data in a generic
        url that user establishes in the method.

        Args:
            url: The site or web page of the request.
            params: A dictionary, list of tuples or bytes to
                    send as a query string.
            allow_redirects: A Boolean to enable/disable redirection.
            auth: A tuple to enable a certain HTTP authentication.
            cert: A String or Tuple specifying a cert file or key.
            cookies: A dictionary of cookies to send to the specified url.
            headers: A dictionary of HTTP headers to send to the specified url.
            proxies: A dictionary of the protocol to the proxy url.
            stream: A Boolean indication if the response should be
                    immediately downloaded (False) or streamed (True).
            timeout: A number, or a tuple, indicating how many seconds
                    to wait for the client to make a connection and/or
                    send a response.
            verify: A Boolean or a String indication to verify the servers
                    TLS certificate or not.

        Return:
            response: The response of the request.

        Exceptions:
            If there is no response on the web page or site, it is going
            to raise an Exception that says that there was an error trying
            to connect with the "Server" or the site


    """
    kwargs = {}

    if params:
        kwargs['params'] = params
    if allow_redirects:
        kwargs['allow_redirects'] = allow_redirects
    if auth:
        kwargs['auth'] = auth
    if cert:
        kwargs['cert'] = cert
    if cookies:
        kwargs['cookies'] = cookies
    if headers:
        kwargs['headers'] = headers
    if proxies:
        kwargs['proxies'] = proxies
    if stream:
        kwargs['stream'] = stream
    if timeout:
        kwargs['timeout'] = timeout
    if verify:
        kwargs['verify'] = verify

    try:
        response = requests.get(url, kwargs)
        return response
    except ConnectionError:
        raise Exception(f"The web page \"{url}\" you are trying "
                        f"to get data of is not responding"
                        f"or it is not a correct url.")


def post_request(url, data,  # pylint: disable=too-many-arguments
                 json=None, files=None, allow_redirects=True,
                 auth=None, cert=None, cookies=None, headers=None,
                 proxies=None, stream=False, timeout=None,
                 verify=False) -> object:
    """This method sends a post request to a generic url

        This method receives an url and data mandatory form
        the user, and other type of variables that are not
        mandatory. This posts in a generic url that user establishes
        in the method.

        Args:
            url: The site or web page of the request.
            data: A dictionary, list of tuples, bytes or a file object
                    to send to the specified url
            json: A JSON object to send to the specified url
            files: images, or documents to post on the site.
            allow_redirects: A Boolean to enable/disable redirection.
            auth: A tuple to enable a certain HTTP authentication.
            cert: A String or Tuple specifying a cert file or key.
            cookies: A dictionary of cookies to send to the specified url.
            headers: A dictionary of HTTP headers to send to the specified url.
            proxies: A dictionary of the protocol to the proxy url.
            stream: A Boolean indication if the response should be immediately
                    downloaded (False) or streamed (True).
            timeout: A number, or a tuple, indicating how many seconds to wait
                    for the client to make a connection
                    and/or send a response.
            verify: A Boolean or a String indication to verify the servers TLS
                    certificate or not.

        Returns:
            response: The response of the request.

        Exceptions:
            If there is no response on the web page or site, it is going
            to raise an Exception that says that there was an error trying
            to connect with the "Server" or the site
    """

    kwargs = {}

    if data:
        kwargs['data'] = data
    if json:
        kwargs['json'] = json
    if files:
        kwargs['files'] = files
    if allow_redirects:
        kwargs['allow_redirects'] = allow_redirects
    if auth:
        kwargs['auth'] = auth
    if cert:
        kwargs['cert'] = cert
    if cookies:
        kwargs['cookies'] = cookies
    if headers:
        kwargs['headers'] = headers
    if proxies:
        kwargs['proxies'] = proxies
    if stream:
        kwargs['stream'] = stream
    if timeout:
        kwargs['timeout'] = timeout
    if verify:
        kwargs['verify'] = verify

    try:
        response = requests.post(url, kwargs)
        return response

    except ConnectionError:
        raise Exception(f"The web page \"{url}\" you are trying"
                        f" to post data on is not responding"
                        f" or it is not a correct url.")


def put_request(url, data, headers=None) -> object:
    """This method sends a put request to a generic url

        This method receives an url and data at least from user
        to create a data put request on the web page or site
        that he is going to modify in the request.

        Args:
            url: The site or web page of the request.
            data: A dictionary, list of tuples, bytes or a file
                    object to send to the specified url
            headers: A dictionary of HTTP headers to send to the
                    specified url.

        Returns:
            response: the response of the request.

        Exceptions:
            If there is no response on the web page or site, it
            is going to raise an Exception that says that there
            was an error trying to connect with the "Server" or the site

    """
    try:
        if headers and data:
            response = requests.put(url, headers=headers, data=data)
        elif data:
            response = requests.put(url, data=data)

        return response

    except ConnectionError:
        raise Exception(f"The web page \"{url}\" you are trying"
                        f" to post data on is not responding"
                        f"or it is not a correct url.")


def delete_request(url: str,  # pylint: disable=too-many-arguments
                   data=None, headers=None, timeout=None,
                   allow_redirects=True, cert=None, auth=None,
                   cookies=None, proxies=None, stream=False,
                   verify=True) -> object:
    """This method sends a delete request to a generic url

        This method receives an url and data mandatory form
        the user, and other type of variables that are not
        mandatory. This posts in a generic url that user
        establishes in the method.

        Args:
            url: The site or web page of the request.
            data: A dictionary, list of tuples, bytes or a
            file object to send to the specified url
            allow_redirects: A Boolean to enable/disable
            redirection.
            auth: A tuple to enable a certain HTTP authentication.
            cert: A String or Tuple specifying a cert file or key.
            cookies: A dictionary of cookies to send to the
            specified url.
            headers: A dictionary of HTTP headers to send to the
            specified url.
            proxies: A dictionary of the protocol to the proxy url.
            stream: A Boolean indication if the response should be
            immediately downloaded (False) or streamed (True).
            timeout: A number, or a tuple, indicating how many seconds
            to wait for the client to make a connection
                    and/or send a response.
            verify: A Boolean or a String indication to verify the
            servers TLS certificate or not.

        Return:
            response: The response of the request.

        Exceptions:
            If there is no response on the web page or site, it is
            going to raise an Exception that says that there was an
            error trying to connect with the "Server" or the site

    """

    kwargs = {}

    if timeout:
        kwargs['timeout'] = timeout
    if headers:
        kwargs['headers'] = headers
    if data:
        kwargs['data'] = data
    if allow_redirects:
        kwargs['allow_redirects'] = allow_redirects
    if cert:
        kwargs['cert'] = cert
    if auth:
        kwargs['auth'] = auth
    if cookies:
        kwargs['cookies'] = cookies
    if proxies:
        kwargs['proxies'] = proxies
    if stream:
        kwargs['stream'] = stream
    if verify:
        kwargs['verify'] = verify

    try:
        response = requests.delete(url, **kwargs)
        return response

    except ConnectionError:
        raise Exception(f"The web page \"{url}\" you are trying"
                        f" to delete data of is not responding"
                        f"or it is not a correct url.")


def patch_request(url, data, headers=None) -> object:
    """This method sends a patch request to a generic url

        This method receives an url and data at least from
        user to create a data patch on the web page or site
        that he is going to modify in the request.

        Args:
            url: The site or web page of the request.
            data: A dictionary, list of tuples, bytes or a
            file object to send to the specified url
            headers: A dictionary of HTTP headers to send to
            the specified url.

        Returns:
            response: the response of the request.

        Exceptions:
            If there is no response on the web page or site, it
            is going to raise an Exception that says that there
            was an error trying to connect with the "Server" or
            the site
    """
    try:
        if headers and data:
            response = requests.patch(url, headers=headers, data=data)
        elif data:
            response = requests.patch(url, data=data)
        else:
            print("No data or headers to patch.")
        return response
    except ConnectionError:
        raise Exception(f"The web page \"{url}\" "
                        f"you are trying to post data on is not responding"
                        f"or it is not a correct url.")
