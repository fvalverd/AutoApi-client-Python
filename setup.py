# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = '0.0.1'

setup(
    name='AutoApiClient',
    version=version,
    description="Automatic API REST from Python",
    long_description="""""",
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: GNU/Linux',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='api rest authentication automatic web json',
    author='Felipe Valverde Campos',
    author_email='felipe.valverde.campos@gmail.com',
    url='https://github.com/fvalverd/AutoApi-Client-Python',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "requests==2.6.2"
    ],
    tests_require=['nose', 'requests_mock'],
    test_suite="tests",
    entry_points="""
    # -*- Entry points: -*-
    """,
)
