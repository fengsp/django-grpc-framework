from collections import OrderedDict

from django.core.paginator import InvalidPage

from rest_framework.exceptions import NotFound
from rest_framework.pagination import _positive_int  # noqa: WPS450
from rest_framework.pagination import PageNumberPagination as BasePageNumberPagination

from django_grpc_framework.settings import grpc_settings
from django_grpc_framework.protobuf.json_format import parse_dict


class PageNumberPagination(BasePageNumberPagination):
    """Pagination class for service."""

    # Client can control the page size using this query parameter.
    # Default is 'None'. Set to eg 'page_size' to enable usage.
    page_size_query_param = None
    max_page_size = None
    proto_class = None

    def paginate_queryset(self, queryset, request, view=None):
        """Paginate queryset or raise 'NotFound' on receiving invalid page number."""
        self.page_size = self.get_page_size(request)  # noqa: WPS601
        if not self.page_size:
            raise Exception('page_size is not defined.')

        paginator = self.django_paginator_class(queryset, self.page_size)
        page_number = getattr(request, self.page_query_param, 1)

        if not page_number:
            page_number = 1

        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number,
                message=str(exc),
            )
            raise NotFound(msg)

        return list(self.page)

    def get_page_size(self, request):
        """Get and valiate page_size."""
        if self.page_size_query_param:
            try:
                return _positive_int(
                    getattr(request, self.page_size_query_param),
                    strict=True,
                    cutoff=self.max_page_size,
                )
            except (AttributeError, ValueError):
                return self.page_size

        return self.page_size

    def get_paginated_response(self, data):  # noqa: WPS110
        """Return a paginated style `OrderedDict` object for the given output data."""
        response = OrderedDict([
            ('count', self.page.paginator.count),
            ('pageSize', self.page_size),
            ('totalPages', self.page.paginator.num_pages),
            ('results', data),
        ])
        kwargs = {'ignore_unknown_fields': True}
        return parse_dict(response, self.proto_class(), **kwargs)
