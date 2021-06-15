import setuptools
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setuptools.setup(
    name             = 'cheermeup',
    version          = '1.0.1',
    description      = 'Command line program to play random animal videos.',
    long_description = read('README.md'),
    long_description_content_type='text/markdown',
    license_files    = ('LICENSE',),
    url              = 'https://github.com/andohuman/cheermeup',
    download_url     = 'https://github.com/andohuman/cheermeup/archive/refs/tags/v1.0.1.tar.gz',
    author           = 'Gautham Venkataraman',
    author_email     = 'gauthsvenkat@gmail.com',
    maintainer       = 'Gautham Venkataraman',
    maintainer_email = 'gauthsvenkat@gmail.com',
    packages         = setuptools.find_packages(),
    install_requires = ['opencv-python', 'praw', 'appdirs'],
    entry_points     = {
        'console_scripts': [
            'cheermeup=src.cheermeup:main',
        ],
    },
)
