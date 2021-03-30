from django.http.request import HttpRequest
from urllib.parse import urlencode
from .grpc_socio_request import GRPCSocioRequest
from django.utils.datastructures import MultiValueDict

class GRPCToHTTP(HttpRequest):

    ACTIONS_MAP_TO_METHOD = {
        "Create": "POST",
        "Update": "PUT",
        "PartialUpdate": "PATCH",
        "List": "GET",
        "Retrieve": "GET",
        "Destroy": "DELETE"
    }

    def __init__(grpc_request, grpc_context, action):

        grpc_socio = GRPCSocioRequest(grpc_request, grpc_request, action)

        self.GET = QueryDict(grpc_socio.get_as_old_query_params(), mutable=True)
        self.POST = QueryDict(grpc_socio.request_data, mutable=True)
        self.COOKIES = grpc_socio.cookies
        self.META = grpc_socio.headers
        # INFO - A.M - 30/03/2021 - Not used now. Will need to force a format for file uploading in django-socio-grpc 
        self.FILES = MultiValueDict()

        self.path = ''
        self.path_info = ''
        # INFO - A.M - 30/03/201 - Defaulting to GET until better alternative
        self.method = ACTIONS_MAP_TO_METHOD.get(action, "GET")
        self.resolver_match = None
        self.content_type = None
        self.content_params = None
