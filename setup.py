# -*- coding:utf-8 -*-
from setuptools import setup

setup(name='flaskrestframework',
      version='0.0.3',
      description='Web APIs for Flask, made easy.',
      url='quxl.snbway.com',
      author='quxl',
      author_email='quxl@snbway.com',
      license='MIT',
      packages=['rest_framework_flask', 'rest_framework_flask/schemas'],
      install_requires=[
            'Flask>=0.10.1',
            'Flask-RESTful>=0.3.2',
            'marshmallow>=2.0.0b4'
      ],
      zip_safe=False)

