import os
import sys
import warnings
import unittest

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py


cur_path, cur_script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(cur_path))

install_requires = [
    "celery>=4.1.0",
    "colorlog",
    "coverage",
    "docker-compose",
    "flake8>=3.4.1",
    "future",
    "kombu>=4.1.0",
    "mock",
    "pep8>=1.7.1",
    "pylint",
    "redis",
    "unittest2"
]


if sys.version_info < (2, 7):
    warnings.warn(
        "Python 2.6 is not supported.",
        DeprecationWarning)


def celery_loaders_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover("tests", pattern="test_*.py")
    return test_suite


# Don"t import celery_loaders module here, since deps may not be installed
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "celery_loaders"))

setup(
    name="celery-loaders",
    cmdclass={"build_py": build_py},
    version="1.0.4",
    description="Celery Application and Task Loader Examples",
    long_description="Examples for loading celery applications with " +
    "easy-to-discover task modules",
    author="Jay Johnson",
    author_email="jay.p.h.johnson@gmail.com",
    url="https://github.com/jay-johnson/celery-loaders",
    packages=[
        "celery_loaders",
        "celery_loaders.log",
        "celery_loaders.work_tasks",
    ],
    package_data={},
    install_requires=install_requires,
    test_suite="setup.celery_loaders_test_suite",
    tests_require=[
    ],
    scripts=[
        "./run-celery-task.py"
    ],
    use_2to3=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ])
