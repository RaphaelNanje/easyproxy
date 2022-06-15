from setuptools import find_packages, setup

setup(
    name='easyasyncproxy',
    version='3.0.0',
    packages=find_packages(),
    url='https://github.com/RaphaelNanje/easyproxy',
    license='MIT',
    author='Raphael Nanje',
    author_email='rtnanje@gmail.com',
    description='',
    install_requires=[
        'requests',
        'requests[socks]',
        'yarl',
        'attrs',
        'urllib3'
    ],
    extras_require={
        'dev': ['python-dotenv']
    }
)
