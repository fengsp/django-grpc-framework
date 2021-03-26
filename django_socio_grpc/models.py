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

	code  = models.IntegerField(default=0)
	status = models.CharField(max_length=40, null=False, blank=False, db_index=True)
	notes = models.TextField('gRPC Notes', null=True, blank=True)
	count = models.BigIntegerField(default=0)
	
	class Meta:
		app_label = 'django_grpc_framework'   
		verbose_name = _('GRPC ERROR CODE')
		verbose_name_plural = _('GRPC ERRORS CODES')
	
	
	def __str__(self):
		return '%s (%s)' % (self.code,  self.status)
	



class socioGrpcErrors(TimestampedModel):
	"""
    qRPC error during request
	"""
	
	import datetime


	CALL_TYPE = (
	    (1,       'LIST'),
	    (2,        'GET'),
	)

	ERROR_TYPE = (
	    (1,       'LIST'),
	    (2,        'GET'),
	)

	call_type  = models.IntegerField(default=0, choices=CALL_TYPE)
	
	class Meta:
		app_label = 'django_grpc_framework'   
		verbose_name = _('GRPC ERROR HANDLER')
		verbose_name_plural = _('GRPC ERRORS HANDLER')
	
	
	def __str__(self):
		return '%s (%s)' % (self.id,  self.call_type)
	
	
