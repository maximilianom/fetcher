try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

from fetcher import VERSION

setup(
    name='fetcher',
    version=VERSION,
    description='Fetcher',
    author='Maximiliano Mendez',
    author_email='',
    url='',
    install_requires=[
        "Django==1.2.3",
        "psycopg2==2.4.4",
        "Fabric==1.4.0",
        "pika==0.9.5",
        "boto==2.2.2",
    ],
    packages=find_packages(),
    include_package_data=True,
)
