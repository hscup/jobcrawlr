from distutils.core import setup

setup(
    name='jobcrawler',
    version='0.1.0',
    scripts=['jobcrawler.py'],
    url='',
    license='LICENSE.txt',
    description='Job crawler',
    long_description=open('README.md').read(),
    install_requires=[
        "requests >= 2.18.4",
        "lxml==4.0.0",
    ],
)