import json


class SocioProxyHttpRequest:
    HEADERS_KEY = "HEADERS"
    #     FILTERS_KEY = "FILTERS"
    #     PAGINATION_KEY = "PAGINATION"
    #     COOKIES_KEY = "COOKIES"
    MAP_HEADERS = {"AUTHORIZATION": "HTTP_AUTHORIZATION"}

    def __init__(self, grpc_context):
        grpc_request_metadata = dict(grpc_context.invocation_metadata())
        self.headers = json.loads(grpc_request_metadata.get(self.HEADERS_KEY.lower(), "{}"))
        self.META = {
            self.MAP_HEADERS.get(key.upper()): value for key, value in self.headers.items()
        }
        self.GET = {}  # QueryDict(mutable=True)
        self.POST = {}  # QueryDict(mutable=True)
        self.COOKIES = {}
        self.FILES = {}  # MultiValueDict()


class GRPCSocioProxyContext:
    """Proxy context, provide http1 proxy request object
    and grpc context object"""

    def __init__(self, grpc_context):
        self.grpc_context = grpc_context
        self.proxy_http_request = SocioProxyHttpRequest(self)

    def __getattr__(self, attr):
        try:
            if hasattr(self.grpc_context, attr):
                return getattr(self.grpc_context, attr)
            if hasattr(self.proxy_http_request, attr):
                return getattr(self.proxy_http_request, attr)
        except AttributeError:
            return self.__getattribute__(attr)


# from django.http.request import HttpRequest
# from urllib.parse import urlencode
# from .grpc_socio_request import GRPCSocioRequest
# from django.utils.datastructures import MultiValueDict


# class GRPCToHTTP(HttpRequest):

#     ACTIONS_MAP_TO_METHOD = {
#         "Create": "POST",
#         "Update": "PUT",
#         "PartialUpdate": "PATCH",
#         "List": "GET",
#         "Retrieve": "GET",
#         "Destroy": "DELETE",
#     }

#     def __init__(self, grpc_request, grpc_context, action):

#         grpc_socio = GRPCSocioRequest(grpc_request, grpc_request, action)

#         self.GET = QueryDict(grpc_socio.get_as_old_query_params(), mutable=True)
#         self.POST = QueryDict(grpc_socio.request_data, mutable=True)
#         self.COOKIES = grpc_socio.cookies
#         self.META = grpc_socio.headers
#         # INFO - A.M - 30/03/2021 - Not used now. Will need to force a format for file uploading in django-socio-grpc
#         self.FILES = MultiValueDict()

#         self.path = ""
#         self.path_info = ""
#         # INFO - A.M - 30/03/201 - Defaulting to GET until better alternative
#         self.method = ACTIONS_MAP_TO_METHOD.get(action, "GET")
#         self.resolver_match = None
#         self.content_type = None
#         self.content_params = None
