from setuptools import setup

setup(
    name='sql',
    py_modules=['base', 'modify'],
    install_requires=['pyodbc']
)
