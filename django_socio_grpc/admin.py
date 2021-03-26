from django.contrib import admin
from django_grpc_framework.models import *


class grcpErrorCodeAdmin(admin.ModelAdmin):
	"""

	"""

	list_display = ('code', 'status', 'notes', 'count', 'created', 'is_active')
	fields = ('code', 'status', 'notes', 'created',  'is_active', 'is_delete' )
	ordering = ('code', )
	list_filter = ['is_active',  'is_delete', ]
	#list_editable = ['status', ]
	#readonly_fields =  ['xxxxxx',  ]
	search_fields = ['notes', 'status',]
	
	
admin.site.register(grcpErrorCode, grcpErrorCodeAdmin)	
	

