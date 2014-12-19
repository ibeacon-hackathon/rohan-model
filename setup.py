from setuptools import setup, find_packages

# If you have issues with this, install using requirements.txt

setup(
    name = 'rohan-model',
    packages = find_packages(),
    version = '0.1.0',
    description = "Rohan model layer",
    author = 'Alon Diamant',
    author_email = 'diamant.alon@gmail.com',
    url = 'http://github.com/ibeacon-hackathon/rohan-model',
    install_requires = ['requests >=1.2.0,<1.2.99'],
    dependency_links=['https://github.com/assisantunes/python-firebase/tarball/master#egg=pyfbase'],
    classifiers = [
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU General Public License',
        ]
)
