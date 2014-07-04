from setuptools import setup, find_packages
import os

version = '0.0.1'

setup(
    name='bullows_erpnext',
    version=version,
    description='Bullows ERPNext Extension',
    author='Webnotes',
    author_email='developers@erpnext.com',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=("frappe",),
)
