import re
from setuptools import find_packages, setup


with open('django_grpc_framework/__init__.py', 'rb') as f:
    version = str(eval(re.search(r'__version__\s+=\s+(.*)',
        f.read().decode('utf-8')).group(1)))


setup(
    name='djangogrpcframework',
    version=version,
    description='gRPC for Django.',
    long_description=open('README.rst', 'r', encoding='utf-8').read(),
    url='https://github.com/fengsp/django-grpc-framework',
    author='Shipeng Feng',
    author_email='fsp261@gmail.com',
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.6",
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
