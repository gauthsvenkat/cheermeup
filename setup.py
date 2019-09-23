import setuptools

setuptools.setup(
    name             = 'cheermeup',
    version          = '0.1',
    description      = 'Command line program to play random animal videos.',
    url              = 'https://github.com/andohuman/cheermeup',
    download_url     = 'https://github.com/andohuman/cheermeup/archive/1.0.tar.gz',
    author           = 'andohuman',
    author_email     = 'andohuman@gmail.com',
    maintainer       = 'andohuman',
    maintainer_email = 'andohuman@gmail.com',
    packages         = setuptools.find_packages(),
    install_requires = ['opencv-python', 'praw', 'appdirs'],
    entry_points     = {
        'console_scripts': [
            'cheermeup=cheermeup.cheermeup:main',
        ],
    },
)