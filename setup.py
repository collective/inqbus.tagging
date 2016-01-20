from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='inqbus.tagging',
      version=version,
      description="Auto tagging for Plone",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Dr. Volker Jaenisch, Sandra Rum',
      author_email='volker.jaenisch@inqbus.de',
      url='https://hg.inqbus.de/volker/fga/inqbus.tagging/summary',
      license='GPL',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['inqbus'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'Products.PloneKeywordManager',
          'IPTCInfo',
          'exifread',
          'plone.autoform',
          'cffi',
          'jpegtran-cffi',
#          'collective.z3cform.datagridfield'
      ],
      dependency_links=[
        "git+https://github.com/sandrarum/collective.z3cform.datagridfield.git#egg=collective.z3cform.datagridfield"
      ],
      extras_require={
        'test': [
            'plone.app.testing',
            'plone.app.robotframework[debug]',
        ],
        },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      # The next two lines may be deleted after you no longer need
      # addcontent support from paster and before you distribute
      # your package.
      setup_requires=["PasteScript"],
      paster_plugins = ["ZopeSkel"],

      )
