from setuptools import setup

setup(
    name='TextCompiler',
    version='1.0.3',
    packages=['TextCompiler', 'TextCompiler.tags',
              'TextCompiler.tags.luaExec',
              'TextCompiler.inputStringParser'],
    package_dir={'TextCompiler': 'src/TextCompiler'},
    package_data={'TextCompiler': ['tags/luaExec/libs/*.lua']},
    url='',
    license='',
    author='Vlaska',
    author_email='vlaska8888@gmail.com',
    description='',
)
