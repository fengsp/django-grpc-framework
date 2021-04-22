import errno
import os

from django.core.management.base import BaseCommand

from django_socio_grpc.exceptions import ProtobufGenerationException
from django_socio_grpc.protobuf.generators import ModelProtoGenerator
from django_socio_grpc.utils.model_extractor import is_app_in_installed_app, is_model_exist


class Command(BaseCommand):
    help = "Generates proto."

    def add_arguments(self, parser):
        parser.add_argument(
            "--model",
            help="dotted path to a model class",
        )
        parser.add_argument("--file", help="the generated proto file path")
        parser.add_argument("--app", help="specify Django Application")
        parser.add_argument(
            "--update", action="store_true", default=True, help="Replace the proto file"
        )
        parser.add_argument(
            "--dry-run", action="store_true", help="print proto data without writing them"
        )

    def handle(self, *args, **options):

        # ------------------------------------------
        # ---- extract protog Gen Parameters     ---
        # ------------------------------------------
        self.app_name = options["app"]
        self.model_name = options["model"]
        if self.model_name:
            self.model_name = self.model_name.lower()
        self.update_proto_file = options["update"]
        self.file_path = options["file"]
        self.dry_run = options["dry_run"]

        self.check_options()

        # ----------------------------------------------
        # --- Proto Generation Process               ---
        # ----------------------------------------------
        generator = ModelProtoGenerator(app_name=self.app_name, model_name=self.model_name)

        # ------------------------------------------------------------
        # ---- Produce a proto file on current filesystem and Path ---
        # ------------------------------------------------------------
        proto = generator.get_proto()
        if self.dry_run:
            self.stdout.write(proto)
        elif self.file_path:
            self.create_directory_if_not_exist(self.file_path)
            with open(self.file_path, "w") as f:
                f.write(proto)
        # if no filepath specified we create it in a grpc directory in the app
        else:
            auto_file_path = os.path.join(self.app_name, "grpc", f"{self.app_name}.proto")
            self.create_directory_if_not_exist(auto_file_path)
            with open(auto_file_path, "w") as f:
                f.write(proto)

    def check_options(self):
        """
        Verify the user input
        """
        if not self.app_name and not self.model_name:
            raise ProtobufGenerationException(
                detail="You need to specify at least one app or one model"
            )

        # INFO - AM - 19/04 - Find if the app passed as argument is correct
        if self.app_name and not is_app_in_installed_app(self.app_name):
            raise ProtobufGenerationException(
                app_name=self.app_name, model_name=self.model_name, detail="Invalid Django app"
            )

        # INFO - AM - 19/04 - Find if the model passed as argument is correct
        if self.model_name and not is_model_exist(self.model_name):
            raise ProtobufGenerationException(
                app_name=self.app_name,
                model_name=self.model_name,
                detail="Invalid Django model",
            )

        # --------------------------------------------------
        # --- Check Path for generating the protbuf file ---
        # --------------------------------------------------
        if self.file_path and os.path.exists(self.file_path) and not self.update_proto_file:
            raise ProtobufGenerationException(
                app_name=self.app_name,
                model_name=self.model_name,
                detail=f"File {self.file_path} already exist",
            )

    def create_directory_if_not_exist(self, file_path):
        if not os.path.exists(os.path.dirname(file_path)):
            try:
                os.makedirs(os.path.dirname(file_path))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
