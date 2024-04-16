from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='pyloghub',
    version='0.1.3',
    packages=find_packages(),
    description='The `pyloghub` package provides convinient access to various Log-hub API services for Supply Chain Visualization, Network Design Optimization, and Transport Optimization as well as access to the Log-hub platform data.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/log-hub/log-hub-python',
    author='Log-hub AG',
    author_email='support@log-hub.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=required,
    package_data={'pyloghub': ['sample_data/*.xlsx']},
    include_package_data=True,
)
