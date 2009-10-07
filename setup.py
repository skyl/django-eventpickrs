from setuptools import setup, find_packages

version = '0.1'

LONG_DESCRIPTION = """
=====================================
django-events
=====================================

Simple reusable app for django with jquery-ui datepickr

"""

setup(
    name='django-events',
    version=version,
    description="django-events",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    keywords='django,pinax,jquery-ui,datepickr',
    author='Skylar Saveland',
    author_email='skylar.saveland@gmail.com',
    url='http://github.com/skyl/django-events',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    setup_requires=['setuptools_git'],
)


