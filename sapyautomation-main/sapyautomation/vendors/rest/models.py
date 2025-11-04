import enum
from collections import namedtuple


class RequestType(enum.Enum):
    GET = 1
    POST = 2
    PUT = 3


GetRequest = namedtuple('GetRequest', 'url headers')

PostRequest = namedtuple('PostRequest', 'url headers data')
