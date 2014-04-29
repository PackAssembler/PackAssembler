import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'pyramid',
    'mongoengine',
    'cffi',
    'bcrypt',
    'mandrill',
    'wtforms',
    'htmllaundry',
    'nose',
    'nose-mongoengine',
    'coverage',
    'pyramid_mako'
]

setup(
    name='packassembler',
    version='0.1',
    description='Pack Assembler',
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='Stephen McIntosh',
    author_email='stephenmac7@gmail.com',
    url='https://mml.stephenmac.com/',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=requires,
    test_suite='packassembler',
    entry_points="""\
    [paste.app_factory]
    main = packassembler:main
    """,
)
