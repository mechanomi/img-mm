from setuptools import setup

setup(
    name='imgmm',
    packages=['imgmm'],
    include_package_data=True,
    install_requires=[
        'Flask',
        'Pillow',
        'trueskill',
        'xattr',
    ],
)
