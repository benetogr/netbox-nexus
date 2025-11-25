from setuptools import find_packages, setup

setup(
    name='netbox-nexus',
    version='0.1',
    description='A NetBox plugin for Netdisco, CUCM, and LDAP integration',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
