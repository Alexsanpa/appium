import requests

from sapyautomation.vendors.rest.models import (RequestType, PostRequest,
                                                GetRequest)


class RequestConstructor:
    """ Helper to construct requests by type

    Args:
        base_url(str): base url
        path(str): url path
        headers(dict): headers to be added to the request
        params(dict): params/data to be added to the request
        request_type(RequestType): Request type code
    """
    def __init__(self, base_url: str, path: str, headers: dict,
                 params: dict, request_type: RequestType):
        url = f"{base_url}{path}?"
        data = {}

        if params is not None:
            for key, value in ((key, params[key]) for key in params.keys()):
                if request_type is RequestType.GET:
                    url += f"{key}={value}&"

                elif request_type is RequestType.POST:
                    data[key] = value
            url = url[:-1]

        if request_type is RequestType.GET:
            self.request = GetRequest(url, headers)

        elif request_type is RequestType.POST:
            self.request = PostRequest(url, headers, data)

    def execute(self):
        """ Makes the call with the constructed request
        """
        response = None
        if isinstance(self.request, GetRequest):
            response = requests.get(self.request.url,
                                    headers=self.request.headers,
                                    verify=False)

        elif isinstance(self.request, PostRequest):
            response = requests.post(self.request.url,
                                     headers=self.request.headers,
                                     json=self.request.data,
                                     verify=False)

        return response
