from django_grpc_framework.settings import GRPC_CHANNEL_PORT
import grpc
import importlib
from django_grpc_framework.models import grcpMicroServices, grcpDataBases

def grpcClient(service, method='List', channel='50051'):
	"""
	Common Interface to call gRPC Client
	https://stackoverflow.com/questions/301134/how-to-import-a-module-given-its-name-as-string
	"""
	
	import carcheck_pb2_grpc, carcheck_pb2
	
	status             = True
	microserviceObject = None
	dataBaseObject     = None
	dataModel          = ''
	directoryService   = ''
	method             = method.capitalize()
	
	# ------------------------------------
	# --- Get Microservice Data        ---
	# ------------------------------------
	microserviceObject = grcpMicroServices.objects.filter(service=service)
	if microserviceObject:
		microserviceObject = microserviceObject[0]
		directoryService = microserviceObject.directory
	else:
		status = False
		return status
	
	# --------------------------------
	# --  get Service Data Model   ---
	# --------------------------------
	if microserviceObject:
		dataBaseObject = grcpDataBases.objects.filter(service=microserviceObject)
		if dataBaseObject:
			dataBaseObject = dataBaseObject[0]
			dataModel = dataBaseObject.database
			
	# ------------------------------------------------
	# ---  Get Stub service for this SQL Table     ---
	# ------------------------------------------------
	pb2GRPCFile = '%s.%s_pb2_grpc' % (directoryService, service)
	pb2GRPCMethod = '%sControllerStub' % (dataModel)
	pb2GRPC     = getattr(importlib.import_module(pb2GRPCFile), pb2GRPCMethod)
	
	# ---------------------------------------------------------------------------------
	# --- connect to gRPC  Server with  preselected Channel Port (default : 50051 ) ---
	# ---------------------------------------------------------------------------------
	with grpc.insecure_channel('localhost:%s' % GRPC_CHANNEL_PORT) as channel:

		# --------------------------------------------
		# ---- Query on Django Auth User DataBase  ---
		stub = pb2GRPC(channel)
		stubResult = Microservice(stub, service, dataModel, method=method, directory=directoryService)
		return stubResult
		
		
def Microservice(stub, service, dataModel, method="List", directory=""):
	"""
	Service Load, then execute it !
	"""
	arrayResult = []
	status      = True

	# ---------------------------------------
	# ---  Load Microservice Stub Request ---
	# ---------------------------------------
	if not directory:
		pb2StubName = '%s_pb2'      % (service)
	else:
		pb2StubName = '%s.%s_pb2'   % (directory, service)
	pb2StudMethod   = '%s%sRequest' % (dataModel, method)
	pb2Service  = getattr(importlib.import_module(pb2StubName), pb2StudMethod)

	listMethod = pb2Service()        # -- Prepare Stud Method ---

	# -------------------------------------------------
	# ---  Execute Stud process against gRPC server ---
	# -------------------------------------------------
	try:
		stubProcess = getattr(stub, method)(listMethod)
		for dataStub in stubProcess:
			arrayResult.append(dataStub)
	except grpc.RpcError as e:
		status = errorProcess(e)
		return status, arrayResult
	else:
		return status, arrayResult
	
	
def errorProcess(self, e):
	"""
	common error processing 
	"""
	
	print('        ')
	print(' *****************************')
	print(' ******  E R R O R       *****')
	print(' ******  %s              *****' % e.details())
	status_code = e.code()
	print(' ****** %s               *****' % status_code.name)
	print(' ****** %s               *****' % status_code.value)
	# ---------------------------------------------
	# -- -extended Error  processing here .... ----
	if grpc.StatusCode.INVALID_ARGUMENT == status_code:
		# do your stuff here
		pass 
	return False

	
	
	
	