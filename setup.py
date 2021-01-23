from setuptools import find_packages, setup

setup(
    name='MSPACompiler',
    version='1.2.0',
    packages=find_packages(),
    include_package_data=True,
    author='Vlaska',
    author_email='vlaska8888@gmail.com',
    url='https://github.com/Vlaska/MSPACompiler',
    install_requires=['Arpeggio', 'lupa', 'click', 'fcache', 'loguru'],
    entry_points='''
    [console_scripts]
    mspac=MSPACompiler.scripts.mspac:mspac
    mspa=MSPACompiler.scripts.mspa:cli
    ''',
    python_requires='>=3.8',
)
