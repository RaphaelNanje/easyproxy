from setuptools import setup

setup(
        name='easyasyncproxy',
        version='0.0.1',
        packages=['easyasyncproxy', 'easyasyncproxy.proxy',
                  'easyasyncproxy.proxy.tests',
                  'easyasyncproxy.scraperapi',
                  'easyasyncproxy.scraperapi.tests',
                  'easyasyncproxy.scrapestack',
                  'easyasyncproxy.scrapestack.tests'],
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
