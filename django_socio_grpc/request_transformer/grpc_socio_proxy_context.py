import json


class SocioProxyHttpRequest:
    HEADERS_KEY = "HEADERS"
    MAP_HEADERS = {"AUTHORIZATION": "HTTP_AUTHORIZATION"}
    FILTERS_KEY = "FILTERS"
    PAGINATION_KEY = "PAGINATION"

    def __init__(self, grpc_context):
        grpc_request_metadata = dict(grpc_context.invocation_metadata())
        self.headers = json.loads(grpc_request_metadata.get(self.HEADERS_KEY.lower(), "{}"))
        self.META = {
            self.MAP_HEADERS.get(key.upper()): value for key, value in self.headers.items()
        }
        # INFO - A.D.B - 04/01/2021 - Not implemented for now
        self.GET = {}
        self.POST = {}
        self.COOKIES = {}
        self.FILES = {}

        # Computed params
        self.query_params = self.get_query_params(grpc_request_metadata)

    def get_query_params(self, grpc_request_metadata):
        filters_params = json.loads(grpc_request_metadata.get(self.FILTERS_KEY, "{}"))
        pagination_params = json.loads(grpc_request_metadata.get(self.PAGINATION_KEY, "{}"))
        return {**filters_params, **pagination_params}

    def build_absolute_uri(self):
        return "NYI"


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
