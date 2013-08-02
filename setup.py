import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'pyramid',
    'mongoengine',
    ]

setup(name='mcmanager',
      version='0.1',
      description='MC Manager Server',
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
      test_suite="mmlserver",
      entry_points="""\
      [paste.app_factory]
      main = mmlserver:main
      """,
      )
