from django_grpc_framework.settings import GRPC_CHANNEL_PORT
import grpc
import importlib
from django_grpc_framework.models import grcpMicroServices, grcpDataBases, grcpProtoBufFields, grpcMethod
from utils.utils import getElapse

class grpcClient():
	"""
	Common Interface to call gRPC Client
	https://stackoverflow.com/questions/301134/how-to-import-a-module-given-its-name-as-string
	"""
	
	def __init__(self, service, method='List', channel='50051', debug=True, value=None):
		
		self._statusGRPC        = True
		self._resultGRPC        = None
		self.microserviceObject = None
		self.dataBaseObject     = None
		self.pb2GRPC            = None
		self.errorObject        = None
		self.listMethod         = None
		self.grpcHandle         = None
		self.dataModel          = ''
		self.directoryService   = ''
		self.reasonError        = ''
		self.method             = method.capitalize()
		self.debug              = debug
		self.channel            = channel
		self.service            = service
		self.query              = ''
		self.abort              = True
		self.value              = value
		self.error              = 0
		self.reason             = ''
		self.queryArg           = ''
		self.startTime          = getElapse(mode='start')
		self.endTime            = 0.0 
		self.modeResult         = 'array'
		self.fields             = []
		# ------------------------------
		# -- Available Method        ---
		self.methodService      = {
			'List'    : ''   ,
			'Retrieve': 'arg',
			'Update'  : ''   ,
			'Destroy' : ''
		}
		
		# ------------------------------------
		# ---  Check Method                ---
		# ------------------------------------
		if self.method in  self.methodService:
			self.queryArg = self.methodService[self.method]
		else:
			self.prepareError(901, reason='Invalid Method [%s]' % self.method)
			return
	
		# ------------------------------------
		# --- Get Microservice Data        ---
		# ------------------------------------
		self.microserviceObject = grcpMicroServices.objects.filter(service=service)
		if self.microserviceObject:
			self.microserviceObject = self.microserviceObject[0]
			self.directoryService   = self.microserviceObject.directory
			self.modeResult         = self.microserviceObject.result
		else:
			self.prepareError(902, reason='Invalid Service [%s]' % self.service)
			return
	
		# --------------------------------
		# --  get Service Data Model   ---
		# --------------------------------
		if self.microserviceObject:
			self.dataBaseObject = grcpDataBases.objects.filter(service=self.microserviceObject)
			if self.dataBaseObject:
				self.dataBaseObject = self.dataBaseObject[0]
				self.dataModel = self.dataBaseObject.database
				# ----------------------------------------------------------------------
				# ----  Get Method Profile for current Service, method and Database ----
				methodObject = grpcMethod.objects.filter(service=self.microserviceObject, database=self.dataBaseObject, method=self.method)
				if methodObject:
					methodObject    = methodObject[0]
					self.update     = methodObject.is_update
					self.modeResult = methodObject.result
					self.queryArg   = methodObject.input
				else:
					self.prepareError(904, reason='No Method [%s] defined for Service [%s]' % (self.method, self.service))
					return
				# --------------------------------------------
				# --- Get Query Fields                     ---
				protoBuffFieldObject = grcpProtoBufFields.objects.filter(database=self.dataBaseObject, is_query=True)
				if len(protoBuffFieldObject) > 0:
					for field in protoBuffFieldObject:
						self.fields.append(field.field)
				else:
					self.prepareError(905, reason='No ProtoBuf Field defined for Service [%s]' % (self.service))
					return
			else:
				self.prepareError(903, reason='No DataBase found for this Service [%s]' % self.service)
				return
			
			# ------------------------------------------------
			# ---  Get Stub service for this SQL Table     ---
			# ------------------------------------------------
			try:
				pb2GRPCFile   = '%s.%s_pb2_grpc' % (self.directoryService, self.service)
				pb2GRPCMethod = '%sControllerStub' % (self.dataModel)
				self.pb2GRPC  = getattr(importlib.import_module(pb2GRPCFile), pb2GRPCMethod)
			except:
				self.prepareError(906, reason='No pb2 grpc python file [%s] found for this Service [%s]' % (pb2GRPCFile, self.service))
				return
				
			
			# --------------------------------------------------
			# --- Instantiate grpc Server Handle             ---
			try:
				self.grpcHandle = grpc.insecure_channel('localhost:%s' % GRPC_CHANNEL_PORT) 
			except:
				self.prepareError(907, reason='No grpc Server has been started or Invalid Port [%s]' % (GRPC_CHANNEL_PORT))
				return
				
	

	def statusGRPC(self):
		"""
		send back grpc status
		"""
		return self._statusGRPC


	def formatResult(self):
		"""
		send back grpc result format
		"""
		return self.modeResult


	def resultGRPC(self):
		"""
		send back microservice result
		"""
		return self._resultGRPC


	def resultFORMAT(self):
		"""
		send back microservice Result format
		"""
		return self.modeResult
	
	def prepareError(self, errCode, reason=''):
		self._statusGRPC = False
		self.error = errCode
		self.reasonError = reason
		self.errorProcess(errCode, custom=True)
		
		
	# -------------------------------------------------------------------------------------------
	# ---- P R E P A R E      A C C E S S    T H R O U G H     G R P C     S E R V E R      -----
	# -------------------------------------------------------------------------------------------
	def Microservice(self):
		"""
		GRPC Handler ready, Service Load, then execute it !
		"""
		# ----------------------------------------------------------------------------------
		# --- always display or extract Stub result inside the grpc Channel secure Block ---
		# --- connect to gRPC  Server with  preselected Channel Port (default : 50051 )  ---
		# ----------------------------------------------------------------------------------
		with self.grpcHandle:
			# --------------------------------------------
			# ---- Query on Django Auth User DataBase  ---
			self.stub        = self.pb2GRPC(self.grpcHandle)
			self._statusGRPC = self.executeMicroservice()
			if self._statusGRPC:
				self.loggingProcess()    # --- Log this call to socotec Microservices ---
			return self._statusGRPC
		

	# -----------------------------------------------------
	# ----  E X E C U T E    M I C R O S E R V I C E    ---
	# -----------------------------------------------------
	def executeMicroservice(self):
		"""
		Service Load, then execute it !
		"""

		arrayResult = []
		self._statuscode = True
		
		# ---------------------------------------
		# ---  Load Microservice Stub Request ---
		# ---------------------------------------
		if not self.directoryService:
			pb2StubName = '%s_pb2'      % (self.service)
		else:
			pb2StubName = '%s.%s_pb2'   % (self.directoryService, self.service)
		pb2StudMethod   = '%s%sRequest' % (self.dataModel, self.method)
		try:
			self.pb2Service  = getattr(importlib.import_module(pb2StubName), pb2StudMethod)
		except:
			self.prepareError(900, reason='Invalid Method or Service [%s]' % pb2StudMethod)
			return
		
		# -----------------------------------------------
		# ---  Prepare Query for Services if required ---
		# -----------------------------------------------
		if self.queryArg == '':
			try:
				self.listMethod = self.pb2Service()    # -- Prepare Stud Method (no Args required) ---
			except:
				self.prepareError(908, reason='Invalid Stub Request [%s.%s]' % (pb2StubName, pb2StudMethod ))
				return
		else:
			kwargs = {}
			for col in self.fields:
				kwargs['{0}'.format(col)] = self.value
			self.listMethod = self.pb2Service(**kwargs)    # -- Prepare Stud Method (no Args required) ---
			

		# -------------------------------------------------
		# ---  Execute Stud process against gRPC server ---
		# -------------------------------------------------
		try:
			stubProcess = getattr(self.stub, self.method)(self.listMethod)
			if self.modeResult == 'array':
				for dataStub in stubProcess:
					arrayResult.append(dataStub)
			else:
				arrayResult = stubProcess
		except grpc.RpcError as e:
			self._statusGRPC = self.errorProcess(e)
		else:
			self._statusGRPC = True
			self._resultGRPC = arrayResult
			self.endTime = getElapse(mode='end', startTime=self.startTime)
			return self._statusGRPC
	

	# ---------------------------------------------------------------
	# ----  G R P C       E R R O R      P R O C E S S I N G     ----
	# ---------------------------------------------------------------
	def errorProcess(self, e, custom=False):
		"""
		common error processing 
		"""
		from django_grpc_framework.models import grcpErrorCode, socioGrpcErrors
		from utils.utils import ConvChoicesToDic, getFromChoices
		
		isCustom = True
		self.endTime = getElapse(mode='end', startTime=self.startTime)
	
		# ----------------------------------------------------
		# -- will process here only native gRPC Error Code ---
		# ----------------------------------------------------
		if self.debug and not custom :
			isCustom = False
			status_code = e.code()
			(self.error, reason) = status_code.value

			print('        ')
			print(' ********************************************************')
			print(' ******  E R R O R                                  *****')
			print(' ******  %s                     *****' % e.details())
			print(' ******  %s                                  *****' % status_code.name)
			print(' ******  %s                                          *****' % self.error)
			print(' ********************************************************')
		
		# -----------------------------------------------
		# ---  CUSTOMIZED ERROR LOGGING  (non gRPC)   --- 
		# -----------------------------------------------
		if self.error > 0:
			errorNumber = self.error
			errorReason = self.reasonError
			self.errorObject = grcpErrorCode.objects.filter(code=self.error)
			if self.errorObject:
				self.errorObject = self.errorObject[0]
			
		# ---------------------------------------
		# ----  Create the Error log record   ---
		# ---------------------------------------
		self.errorObject = socioGrpcErrors.objects.create(
			service      = self.microserviceObject,    
			database     = self.dataBaseObject,    
			error        = self.errorObject,    
			method       = getFromChoices(socioGrpcErrors.CALL_TYPE, self.method, default=0),
			aborted      = self.abort,
			query        = self.query,
			reason       = errorReason,
			custom       = isCustom,
			elapse       = round(self.endTime, 2),
			
		)
		
		return False
	

	# ---------------------------------------------------------------
	# ----  G R P C     L O G G I N G    P R O C E S S I N G     ----
	# ---------------------------------------------------------------
	def loggingProcess(self):
		"""
		common LOGGING processing 
		"""
		from utils.utils import ConvChoicesToDic, getFromChoices
		from django_grpc_framework.models import grpcLogging, socioGrpcErrors
		
		
		self.endTime = getElapse(mode='end', startTime=self.startTime)
			
		# ---------------------------------------
		# ----  Create the Error log record   ---
		# ---------------------------------------
		self.loggingObject = grpcLogging.objects.create(
			service      = self.microserviceObject,    
			database     = self.dataBaseObject,    
			method       = getFromChoices(socioGrpcErrors.CALL_TYPE, self.method, default=0),
			query        = self.query,
			result       = self._resultGRPC,
			elapse       = round(self.endTime, 2),
			
		)

	
	

	
	
	
	