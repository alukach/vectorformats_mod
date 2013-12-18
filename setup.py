from setuptools import setup, find_packages
from setuptools.command.test import test


class TestCommand(test):
    def run(self):
        from tests.runtests import runtests
        runtests()


setup(
    name='vectorformats',
    version='0.1',
    description="Vectorformats modified to accept spanned relationships.",
    long_description=open('README.md').read(),
    author='Anthony Lukach',
    author_email='anthonylukach@gmail.com',
    license='BSD',
    url='https://github.com/alukach/vectorformats_mod',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=['simplejson'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Framework :: Django',
    ],
    cmdclass={"test": TestCommand},
)
