all: clean-pyc test

tox-test:
	tox

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lines:
	find . -name "*.py"|xargs cat|wc -l

release:
	python setup.py sdist upload
	python setup.py bdist_wheel upload

test:
	@py.test -vv --tb=short tests

flake8:
	@flake8 --ignore=E501,F401,W292,W503 django_grpc_framework examples/tutorial/blog examples/tutorial/tutorial examples/tutorial/blog_client.py examples/quickstart/account examples/null_support/snippets
