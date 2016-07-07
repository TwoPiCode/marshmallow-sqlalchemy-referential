import os
from setuptools import setup

readme_path = os.path.join(os.path.dirname(
  os.path.abspath(__file__)),
  'README.rst',
)
long_description = open(readme_path).read()
version_path = os.path.join(os.path.dirname(
  os.path.abspath(__file__)),
  'VERSION',
)
version = open(version_path).read()

setup(
  name='marshmallow-sqlalchemy-referential',
  version=version,
  py_modules=['marshmallow_sqlalchemy_referential'],
  author="Nick Whyte",
  author_email='nick@nickwhyte.com',
  description="A marshmallow-sqlalchemy field allows referential CRUD on "
              "relational fields.",
  long_description=long_description,
  url='https://github.com/twopicode/marshmallow-sqlalchemy-referential',
  zip_safe=False,
  install_requires=[
        "marshmallow",
        "marshmallow-sqlalchemy",
  ],
  classifiers=[
    'Intended Audience :: Developers',
    'Programming Language :: Python',
  ],
)
