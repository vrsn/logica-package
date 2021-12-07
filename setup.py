from setuptools import setup, find_packages

setup(
    name='logica',
    version='1.3.141',
    author='PolicyEngine team',
    author_email='',
    url='',
    description='logica',
    package_dir={"": "logica"},
    packages=find_packages(where='logica'),
    py_modules=['logica'],
    python_requires='>=3.6',
)
