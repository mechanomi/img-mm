from setuptools import setup

setup(
    name='img-mm',
    packages=['img-mm'],
    include_package_data=True,
    install_requires=[
        'Flask',
        'Pillow',
        'trueskill',
        'xattr',
    ],
)
