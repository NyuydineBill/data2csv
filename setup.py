from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

setup(
    name='django_admin_data_export',
    version='1.0.11',
    description='A comprehensive Django app that enhances the admin interface with advanced export functionality for CSV, Excel, and JSON formats.',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    author='Nyuydine Bill',
    author_email='billleynyuy@gmail.com',
    url='https://github.com/NyuydineBill/data2csv',
    packages=['admin_export'],
    include_package_data=True,
    license='MIT',
    install_requires=[
        'Django>=3.2',
        'openpyxl>=3.0.7',
    ],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-django>=4.0',
            'black>=22.0',
            'flake8>=4.0',
            'isort>=5.0',
        ],
        'docs': [
            'Sphinx>=4.0',
            'sphinx-rtd-theme>=1.0',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Office/Business :: Financial :: Spreadsheet',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    python_requires='>=3.8',
    keywords='django admin export csv excel json data',
    project_urls={
        'Bug Reports': 'https://github.com/NyuydineBill/data2csv/issues',
        'Source': 'https://github.com/NyuydineBill/data2csv',
        'Documentation': 'https://github.com/NyuydineBill/data2csv#readme',
    },
    zip_safe=False,
)
