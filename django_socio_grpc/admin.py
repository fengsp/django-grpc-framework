from django.contrib import admin
from django_grpc_framework.models import *


class grcpErrorCodeAdmin(admin.ModelAdmin):
	"""

	"""

	list_display = ('code', 'category', 'status', 'notes', 'count', 'created', 'is_active')
	fields = ('code', 'category', 'status', 'notes', 'created',  'is_active', 'is_delete' )
	ordering = ('code', )
	list_filter = ['is_active',  'is_delete', 'category' ]
	list_editable = ['category', ]
	#readonly_fields =  ['xxxxxx',  ]
	search_fields = ['notes', 'status',]



class grcpDataBasesAdmin(admin.ModelAdmin):
	"""

	"""

	list_display = ('service', 'django', 'database', 'description', 'created', 'is_active')
	fields = ('service', 'django', 'database', 'description',  'created',  'is_active', 'is_delete' )
	ordering = ('service', 'database', )
	list_filter = ['is_active',  'is_delete', 'django' ]
	#list_editable = ['category', ]
	#readonly_fields =  ['xxxxxx',  ]
	search_fields = ['django', 'database', 'description',]




class grcpMicroServicesAdmin(admin.ModelAdmin):
	"""

	"""

	list_display = ('service', 'category', 'count', 'created', 'is_active')
	fields = ('service', 'directory', 'category', 'description', 'count', 'created',  'is_active', 'is_delete' )
	ordering = ('service', )
	list_filter = ['is_active',  'is_delete', ]
	#list_editable = ['status', ]
	#readonly_fields =  ['xxxxxx',  ]
	search_fields = ['description', 'service',]
	


class socioGrpcErrorsAdmin(admin.ModelAdmin):
	"""

	"""

	list_display = ('service', 'database', 'error', 'call_type', 'created', 'is_active')
	fields = ('service', 'database', 'error', 'call_type', 'aborted', 'query', 'created',  'is_active', 'is_delete' )
	ordering = ('service', )
	list_filter = ['is_active',  'is_delete', ]
	#list_editable = ['status', ]
	#readonly_fields =  ['xxxxxx',  ]
	#search_fields = ['description', 'service',]

	

class grcpProtoBufAdmin(admin.ModelAdmin):
	"""

	"""

	list_display = ('protobuf', 'service', 'created', 'is_active')
	fields = ('protobuf', 'file', 'service', 'created',  'is_active', 'is_delete' )
	ordering = ('protobuf', )
	list_filter = ['is_active',  'is_delete', ]
	#list_editable = ['status', ]
	#readonly_fields =  ['xxxxxx',  ]
	#search_fields = ['description', 'service',]



class grcpProtoBufFieldsAdmin(admin.ModelAdmin):
	"""

	"""

	list_display = ('database', 'protobuf', 'field', 'is_query', 'created', 'is_active')
	fields = ('database', 'protobuf', 'field', 'is_query', 'field_sequence', 'query_sequence', 'created',  'is_active', 'is_delete' )
	ordering = ('protobuf', )
	list_filter = ['is_active',  'is_delete', ]
	#list_editable = ['status', ]
	#readonly_fields =  ['xxxxxx',  ]
	#search_fields = ['description', 'service',]



	
	
admin.site.register(grcpErrorCode, grcpErrorCodeAdmin)	
admin.site.register(grcpMicroServices, grcpMicroServicesAdmin)	
admin.site.register(grcpDataBases, grcpDataBasesAdmin)	
admin.site.register(socioGrpcErrors, socioGrpcErrorsAdmin)	
admin.site.register(grcpProtoBuf, grcpProtoBufAdmin)	
admin.site.register(grcpProtoBufFields, grcpProtoBufFieldsAdmin)	



	

