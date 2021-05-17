import asyncio
import logging
import os

from asgiref.sync import async_to_sync, sync_to_async
from django import db

from django_socio_grpc.exceptions import GRPCException, Unimplemented
from django_socio_grpc.request_transformer.grpc_socio_proxy_context import (
    GRPCSocioProxyContext,
)

logger = logging.getLogger("django_socio_grpc")


class ServicerProxy:
    def __init__(self, ServiceClass, **initkwargs):
        self.service_instance = ServiceClass(**initkwargs)
        # TODO - AM - 06/05 - convert to boolean ?
        self.grpc_async = os.environ.get("GRPC_ASYNC", False)

    def call_handler(self, action):
        if self.grpc_async:

            async def async_handler(request, context):
                # db connection state managed similarly to the wsgi handler
                db.reset_queries()
                # INFO - AM - 22/04/2021 - next line break tests. Need to more understand the drowback about memory in production
                # db.close_old_connections()
                try:
                    self.service_instance.request = request
                    self.service_instance.context = GRPCSocioProxyContext(context, action)
                    self.service_instance.action = action
                    await sync_to_async(self.service_instance.before_action)()

                    # INFO - AM - 05/05/2021 - getting the real function in the service and then calling it if necessary
                    instance_action = getattr(self.service_instance, action)
                    return await instance_action(
                        self.service_instance.request, self.service_instance.context
                    )
                except GRPCException as grpc_error:
                    logger.error(grpc_error)
                    context.abort(grpc_error.status_code, grpc_error.get_full_details())
                finally:
                    # INFO - AM - 22/04/2021 - next line break tests. Need to more understand the drowback about memory in production
                    # db.close_old_connections()
                    pass

            return async_handler
        else:

            def handler(request, context):
                # db connection state managed similarly to the wsgi handler
                db.reset_queries()
                # INFO - AM - 22/04/2021 - next line break tests. Need to more understand the drowback about memory in production
                # db.close_old_connections()
                try:
                    self.service_instance.request = request
                    self.service_instance.context = GRPCSocioProxyContext(context, action)
                    self.service_instance.action = action
                    self.service_instance.before_action()

                    # INFO - AM - 05/05/2021 - getting the real function in the service and then calling it if necessary
                    instance_action = getattr(self.service_instance, action)
                    if asyncio.iscoroutinefunction(instance_action):
                        instance_action = async_to_sync(instance_action)
                    return instance_action(
                        self.service_instance.request, self.service_instance.context
                    )
                except GRPCException as grpc_error:
                    logger.error(grpc_error)
                    context.abort(grpc_error.status_code, grpc_error.get_full_details())
                finally:
                    # INFO - AM - 22/04/2021 - next line break tests. Need to more understand the drowback about memory in production
                    # db.close_old_connections()
                    pass

            return handler

    def __getattr__(self, action):
        if not hasattr(self.service_instance, action):
            raise Unimplemented()

        return self.call_handler(action)
