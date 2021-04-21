import asyncio
import errno
import logging
import os
import sys
from concurrent import futures

import grpc
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import autoreload

from django_socio_grpc.settings import grpc_settings

logger = logging.getLogger("django_socio_grpc")


class Command(BaseCommand):
    help = "Starts an async gRPC server"

    # Validation is called explicitly each time the server is reloaded.
    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument(
            "address",
            nargs="?",
            default=f"[::]:{grpc_settings.GRPC_CHANNEL_PORT}",
            help="Optional address for which to open a port.",
        )
        parser.add_argument(
            "--max-workers",
            type=int,
            default=10,
            dest="max_workers",
            help="Number of maximum worker threads.",
        )
        parser.add_argument(
            "--dev",
            action="store_true",
            dest="development_mode",
            help=(
                "Run the server in development mode.  This tells Django to use "
                "the auto-reloader and run checks."
            ),
        )

    def handle(self, *args, **options):
        self.address = options["address"]
        self.development_mode = options["development_mode"]
        self.max_workers = options["max_workers"]

        # set GRPC_ASYNC to "true" in order to start server asynchronously
        os.environ.setdefault("GRPC_ASYNC", "True")

        asyncio.run(self.run(**options))

    async def run(self, **options):
        """Run the server, using the autoreloader if needed."""
        if self.development_mode:
            if hasattr(autoreload, "run_with_reloader"):
                autoreload.run_with_reloader(self.inner_run, **options)
            else:
                autoreload.main(self.inner_run, None, options)
        else:
            logger.info(
                ("Starting async gRPC server at %(address)s\n")
                % {
                    "address": self.address,
                }
            )
            await self._serve()

    async def _serve(self):
        server = grpc.aio.server(
            futures.ThreadPoolExecutor(max_workers=self.max_workers),
            interceptors=grpc_settings.SERVER_INTERCEPTORS,
        )
        grpc_settings.ROOT_HANDLERS_HOOK(server)
        server.add_insecure_port(self.address)
        await server.start()
        try:
            await server.wait_for_termination()
        except KeyboardInterrupt:
            # Shuts down the server with 0 seconds of grace period. During the
            # grace period, the server won't accept new connections and allow
            # existing RPCs to continue within the grace period.
            await server.stop(0)

    def inner_run(self, *args, **options):
        # ------------------------------------------------------------------------
        # If an exception was silenced in ManagementUtility.execute in order
        # to be raised in the child process, raise it now.
        # ------------------------------------------------------------------------
        autoreload.raise_last_exception()
        logger.info('"Performing system checks...\n\n')
        self.check(display_num_errors=True)

        # -----------------------------------------------------------
        # Need to check migrations here, so can't use the
        # requires_migrations_check attribute.
        # -----------------------------------------------------------
        self.check_migrations()
        quit_command = "CTRL-BREAK" if sys.platform == "win32" else "CONTROL-C"
        serverStartDta = (
            f"Django version {self.get_version()}, using settings {settings.SETTINGS_MODULE}\n"
            f"Starting development async gRPC server at {self.address}\n"
            f"Quit the server with {quit_command}s.\n"
        )

        # --------------------------------------------
        # ---  START ASYNC GRPC SERVER             ---
        # --------------------------------------------
        logger.info(serverStartDta)
        try:
            asyncio.run(self._serve())
        except OSError as e:
            # Use helpful error messages instead of ugly tracebacks.
            ERRORS = {
                errno.EACCES: "You don't have permission to access that port.",
                errno.EADDRINUSE: "That port is already in use.",
                errno.EADDRNOTAVAIL: "That IP address can't be assigned to.",
            }
            try:
                error_text = ERRORS[e.errno]
            except KeyError:
                error_text = e
            errorData = f"Error: {error_text}"
            logger.error(errorData)
            # Need to use an OS exit because sys.exit doesn't work in a thread
            os._exit(1)

        # ---------------------------------------
        # ----  EXIT OF GRPC SERVER           ---
        except KeyboardInterrupt:
            logger.warning("Exit gRPC Server")
            sys.exit(0)
