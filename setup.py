from setuptools import find_packages, setup

setup(
    name='TextCompiler',
    version='1.1.1',
    packages=find_packages(),
    include_package_data=True,
    author='Vlaska',
    author_email='vlaska8888@gmail.com',
    install_requires=['Arpeggio', 'lupa']
)
