from setuptools import setup

setup(name='mundowumpus',
        version='0.0.1',
        packages=['mundowumpus'],
        package_dir={'mundowumpus': 'src'},
        install_requires=['gym>=0.10.5',  'numpy'],
        py_modules=[])
