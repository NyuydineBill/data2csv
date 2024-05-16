from setuptools import setup, find_packages

setup(
    name='django-admin-export',
    version='0.0.1',
    description='A Django app that enhances the admin interface by providing custom actions for exporting data to CSV or Excel format.',
    long_description='Django Admin Export Package is a Django app that enhances the Django admin interface by providing custom admin actions for exporting selected items to CSV or Excel format.',
    author='Nyuydine Bill',
    author_email='billleynyuy@gmail.com',
    url='https://github.com/NyuydineBill/data2csv',
    packages=find_packages(),
    install_requires=[
        'Django>=3.0',
        'openpyxl>=3.0.7',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
