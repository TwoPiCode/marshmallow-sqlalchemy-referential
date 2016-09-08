import os
from setuptools import setup

def get_version():
    version_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'VERSION')
    v = open(version_path).read()
    if type(v) == str:
            return v.strip()
    return v.decode('UTF-8').strip()

readme_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)),
    'README.rst',
)
long_description = open(readme_path).read()

try:
        version = get_version()
except Exception as e:
        version = '0.0.0-dev'

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
        "marshmallow-sqlalchemy",
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
)
