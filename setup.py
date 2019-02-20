#!/usr/bin/env python
import os
import re
import sys

from setuptools import find_packages, setup


def get_version(*file_paths):
    """Retrieves the version from fd_dj_accounts/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("fd_dj_accounts", "__init__.py")


if sys.argv[-1] == 'tag':
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

# note: the "typing information" of this project's packages is not made available to its users
#   automatically; it needs to be packaged and distributed. The way to do so is fairly new and
#   it is specified in PEP 561 - "Distributing and Packaging Type Information".
#   See:
#   - https://www.python.org/dev/peps/pep-0561/#packaging-type-information
#   - https://github.com/python/typing/issues/84
#   - https://github.com/python/mypy/issues/3930
_package_data = {
    'fd_dj_accounts': [
        # Indicates that the "typing information" of the package should be distributed.
        'py.typed',
    ],
}

setup(
    name='fyndata-django-accounts',
    version=version,
    description="""Reusable Django app to replace the default Django user (account) model.""",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',  # for Markdown: 'text/markdown'
    author='Fyndata (Fynpal SpA)',
    author_email='no-reply@fyndata.com',
    url='https://github.com/fyndata/fyndata-django-accounts',
    packages=find_packages(
        exclude=[
            'docs',
            'tests*',
        ]),
    python_requires='>=3.6, <3.8',
    include_package_data=True,
    install_requires=[
        'Django>=2.1',
    ],
    test_suite='tests',
    tests_require=[
        # note: include here only packages **imported** in test code (e.g. 'requests-mock'),
        #   NOT those like 'coverage' or 'tox'.
        'psycopg2-binary>=2.6.7',
    ],
    license="MIT",
    zip_safe=False,
    keywords='fyndata-django-accounts',
    classifiers=[
        # See https://pypi.org/classifiers/
        'Development Status :: 3 - Alpha',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
