from django.urls import reverse   # from django.urls
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save, pre_delete
from django.db.models import Avg, Count, Q, Sum
from django.utils import timezone
from django_mysql.models import ListCharField, ListTextField
from django.db.models import IntegerField, SmallIntegerField
from django.utils.translation import ugettext_lazy as _ 


class TimestampedModel(models.Model):
	"""
	A model baseclass adding 'created at' and 'last modified at'
	fields to models.
	"""
	created = models.DateTimeField(blank=True)
	modified = models.DateTimeField(blank=True)
	is_active = models.BooleanField(default=True)
	is_delete = models.BooleanField(default=False)

	class Meta:
		abstract = True
		app_label = 'account'

	def save(self, **kwargs):
		"""
		On save, update timestamps
		"""
		import datetime

		now = datetime.datetime.now()
		if not self.id:
			self.created = now
		self.modified = now
		super(TimestampedModel, self).save(**kwargs)


class grcpErrorCode(TimestampedModel):
	"""
    Official Google gRPC error code
	"""

	ERROR_TYPE = (
	    (1,       'Critical'),
	    (2,       'Warning'),
	)

	code     = models.IntegerField(default=0)
	status   = models.CharField(max_length=40, null=False, blank=False, db_index=True)
	notes    = models.TextField('gRPC Notes', null=True, blank=True)
	count    = models.BigIntegerField(default=0)
	category = models.IntegerField(default=1, choices=ERROR_TYPE, verbose_name="Error Type")
	
	class Meta:
		app_label = 'django_grpc_framework'   
		verbose_name = _('GRPC ERROR CODE')
		verbose_name_plural = _('GRPC ERRORS CODES')
	
	
	def __str__(self):
		return '%s (%s)' % (self.code,  self.status)
	

class grcpMicroServices(TimestampedModel):
	"""
    Official socotec Cross reference for available microservices
	"""
	
	SERVICE_TYPE = (
	    (1,       'SOCOTEC'),
	    (2,        'GOOGLE'),
	)

	service     = models.CharField(max_length=40, null=False, blank=False, db_index=True, verbose_name='Service Name')
	category    = models.IntegerField(default=1, choices=SERVICE_TYPE, verbose_name="Services Category")
	description = models.TextField('gRPC Notes', null=True, blank=True)
	count       = models.BigIntegerField(default=0, verbose_name='Count Access')
	directory   = models.CharField(max_length=60, null=False, blank=False, db_index=True, verbose_name='Service Directory')
	
	class Meta:
		app_label = 'django_grpc_framework'   
		verbose_name = _('GRPC SERVICE REFERENCE')
		verbose_name_plural = _('GRPC SERVICES REFERENCES')
		
	def clean(self):
		self.directory=service		
	
	
	def __str__(self):
		return '%s' % (self.service)


class grcpDataBases(TimestampedModel):
	"""
    Official gRPC Socotec  Databases
	"""
	from utils.utils import getAppList, getModelList
	
	appChoices = getAppList()     # --  get Django application list ---
	#modelChoices = getModelList()   # --  get Django Data Model list ---

	django       = models.CharField(max_length=40, null=False, blank=False, db_index=True, default="", verbose_name="Django Application", choices=appChoices)
	database     = models.CharField(max_length=40, null=False, blank=False, db_index=True, default="",verbose_name="Table SQL")
	description  = models.TextField('gRPC Notes', null=True, blank=True)
	service      = models.ForeignKey(grcpMicroServices, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Socotec Microservice")    
	
	class Meta:
		app_label = 'django_grpc_framework'   
		verbose_name = _('GRPC DATABASE')
		verbose_name_plural = _('GRPC DATABASES')
	
	
	def __str__(self):
		return '%s' % (self.database)
	



class socioGrpcErrors(TimestampedModel):
	"""
    qRPC error during request
	"""
	
	import datetime


	CALL_TYPE = (
	    (1,        'List'),
	    (2,        'Create'),
		(3,        'Retrieve'),
		(4,        'Update'),
		(5,        'Destroy'),
	)


	service      = models.ForeignKey(grcpMicroServices, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Socotec Microservice")    
	database     = models.ForeignKey(grcpDataBases, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Database Microservice")    
	error        = models.ForeignKey(grcpErrorCode, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Microservice Error")    
	call_type    = models.IntegerField(default=0, choices=CALL_TYPE)
	aborted      = models.BooleanField(default=False, verbose_name="Thread aborted ?")
	query        = models.TextField(default='', null=True, blank=True)
	
	class Meta:
		app_label = 'django_grpc_framework'   
		verbose_name = _('GRPC ERROR HANDLER')
		verbose_name_plural = _('GRPC ERRORS HANDLER')
	
	
	def __str__(self):
		return '%s (%s-%s)' % (self.call_type, self.error.code, self.error.status)
	
	

class grcpProtoBuf(TimestampedModel):
	"""
    Official gRPC Protobuf and PBD2 GRPC definition for Socotecio Services
	"""

	protobuf     = models.CharField(max_length=50, null=False, blank=False, db_index=True, default="",verbose_name="Proto Name")
	file         = models.CharField(max_length=50, null=False, blank=False, db_index=True, default="",verbose_name="Proto File")
	service      = models.ForeignKey(grcpDataBases, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Microservice Database")    
	
	class Meta:
		app_label           = 'django_grpc_framework'   
		verbose_name        = _('GRPC PROTOBUF')
		verbose_name_plural = _('GRPC PROTOBUF')
	
	
	def __str__(self):
		return '%s' % (self.protobuf)
	


class grcpProtoBufFields(TimestampedModel):
	"""
    Official gRPC Protobuf Data Models fields definitions
	"""

	database       = models.ForeignKey(grcpDataBases, null=True, blank=True, on_delete=models.CASCADE,  verbose_name="Microservice Database")    
	protobuf       = models.ForeignKey(grcpProtoBuf, null=True, blank=True, on_delete=models.CASCADE,   verbose_name="Microservice Protobuf")    
	field          = models.CharField(max_length=50, null=False, blank=False, db_index=True, default="",verbose_name="Protobuf Field")
	is_query       = models.BooleanField(default=False)
	field_sequence = models.IntegerField(default=1, verbose_name="Field Sequence")
	query_sequence = models.IntegerField(default=1, verbose_name="Query Sequence" )
	
	class Meta:
		app_label           = 'django_grpc_framework'   
		verbose_name        = _('GRPC PROTOBUF FIELD')
		verbose_name_plural = _('GRPC PROTOBUF FIELDS')
	
	
	def __str__(self):
		return '%s' % (self.field)
	
	
