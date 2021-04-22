from django.core.management import call_command

from boot_django import boot_django

# call the django setup routine
boot_django()

args = []
opts = {"app": "fakeapp"}
call_command("generateproto", *args, **opts)
