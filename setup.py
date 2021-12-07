from setuptools import setup, find_packages

setup(
    name='logica',
    version='1.3.141',
    author='PolicyEngine team',
    author_email='',
    url='',
    description='logica',
    packages=['logica'] + find_packages(where='logica'),
    python_requires='>=3.6',
)
