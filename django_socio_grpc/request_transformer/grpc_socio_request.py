from urllib.parse import urlencode
from django.utils.functional import cached_property

class GRPCSocioRequest(HttpRequest):
    """
    Transform a grpc_request and a grpc_context into a python object to easily deal with compatibility behavior.
    This is the default behavior. You can override it with the setting GRPC_FRAMEWORK_REQUEST_TRANSFORMER
    """
    HEADERS_KEY = "HEADERS"
    FILTERS_KEY = "FILTERS"
    PAGINATION_KEY = "PAGINATION"
    COOKIES_KEY = "COOKIES"

    def __init__(self, grpc_request, grpc_context):

        grpc_request_metadata = dict(grpc_context.invocation_metadata())

        self.headers = grpc_request_metadata.get(HEADERS_KEY, {})
        self.filters = grpc_request_metadata.get(FILTERS_KEY, {})
        self.pagination = grpc_request_metadata.get(PAGINATION_KEY, {})
        self.cookies = grpc_request_metadata.get(COOKIES_KEY, {})

        self.old_query_params_as_dict = {**self.filters, **self.pagination}

        self.request_data = grpc_request        

    @cached_property
    def get_as_old_query_params(self):
        """
        Simulate old query params for library compatibility.
        You can override it to customize your behavior
        if you override it don't forget to specify the GRPC_FRAMEWORK_REQUEST_TRANSFORMER settings.
        """
        return urlencode(self.old_query_params_as_dict)

