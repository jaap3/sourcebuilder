import codecs
from os.path import join, dirname
from setuptools import setup, find_packages


version = '1.0dev'
read = lambda *rnames: unicode(codecs.open(join(dirname(__file__), *rnames),
                                           encoding='utf-8').read()).strip()

setup(
    name='sourcebuilder',
    version=version,
    description='Generate (python) code using python',
    long_description='\n\n'.join((read('README.rst'), read('CHANGES.rst'),)),
    author='Jaap Roes',
    author_email='jaap.roes@gmail.com',
    url='https://github.com/jaap3/sourcebuilder',
    packages=find_packages(),
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    tests_require=['unittest2==0.5.1'],
    test_suite='unittest2.collector',
    zip_safe=False,
)
