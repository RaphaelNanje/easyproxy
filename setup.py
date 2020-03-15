from setuptools import setup

setup(
        name='easyasyncproxy',
        version='0.0.1',
        packages=['easyproxy', 'easyproxy.proxy', 'easyproxy.proxy.tests',
                  'easyproxy.scraperapi', 'easyproxy.scraperapi.tests',
                  'easyproxy.scrapestack', 'easyproxy.scrapestack.tests'],
        url='https://github.com/RaphaelNanje/easyproxy',
        license='MIT',
        author='Raphael Nanje',
        author_email='rtnanje@gmail.com',
        description='',
        install_requires=[
                'requests',
                'yarl',
                'attrs',
        ],
        extras_require={
                'dev': ['python-dotenv']
        }
)
