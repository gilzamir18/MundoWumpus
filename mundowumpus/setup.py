from setuptools import setup

setup(name='mundowumpus',
        version='0.0.1',
        packages=['mundowumpus'],
        package_dir={'mundowumpus': 'src'},
        install_requires=['gym>=0.26.2',  'numpy'],
        py_modules=[])
