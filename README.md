# Cheermeup
Command line program that plays random animal from your favorite animal subreddits!

## Standalone [executable](https://github.com/andohuman/cheermeup/releases/tag/v1.0.1) (windows only)

![](https://i.imgur.com/uHT9ygp.gif)


## As a commandline app (available on windows and unix)

![](https://i.imgur.com/DPDNtVJ.gif)

Created by [u/andohuman](https://www.reddit.com/user/andohuman) | [@andohuman](https://twitter.com/andohuman)

## 1. Getting started
This app works by scraping videos from a some of the popular animal subreddits.

If you want to run the standalone binary (windows only), download it from [here](https://github.com/andohuman/cheermeup/releases/download/v1.0.1).

Else if you want to install as a python module and mess with the code, stick around.

## 2. Installation

Before we proceed with the actual installation, consider installing this package in a virtual python environment.

### Installing venv
Install the virtualenv python package with the following command :-
```pip3 install virtualenv```

You can now go ahead and create a virtual environment with the following command :-
``` python3 -m venv YOUR_ENV_NAME/```

Now activate the virtual environment you just created :-
#### On windows
``` YOUR_ENV_NAME\Scripts\activate```
#### On unix systems
``` source YOUR_ENV_NAME/bin/activate```

You can now proceed with the installation of the package

### Installing using pip
You can use the python package manager pip to install this package, although it is recommended that you install the package from source for the latest updates.

Run ```pip3 install cheermeup```

### Installing from source (Recommended)
1. Clone this repository
```git clone https://github.com/andohuman/cheermeup.git```

If you're on windows you can download the zip from [here](https://github.com/andohuman/cheermeup/archive/master.zip) and extract the archive.

2. cd into the folder and install the package by executing

```cd cheermeup```

```pip3 install .```

Note: If you're installing on linux without virtualenv you might have to add ```/home/{YOUR_USERNAME}/.local/bin/``` to your ```$PATH```.

* Run the app by executing ```cheermeup```.

Note: When you run the program for the first time (of the day by default) it may take a couple of seconds, depending on your internet connection and speed to fetch the links and cache them.

If you want to scrape videos from your own subreddits you can do so with the following argument
```cheermeup --subreddits SUBREDDIT_NAME SUBREDDIT_NAME SUBREDDIT_NAME ...```

Execute ```cheermeup --help``` for more options

By default cheermeup only scrapes videos from the following subreddits:- 

babyelephantgifs
partyparrot
animalsbeingjerks
animalsbeingderps
animalsbeingconfused
whatswrongwithyourdog
startledcats
zoomies

If you would like to checkout more options head over to [r/MadeMeSmile](https://www.reddit.com/r/MadeMeSmile/wiki/related-sub-suggestions)'s list of good subreddits and add your own subreddits with the ```--subreddits``` argument.

It has to be mentioned that the more subreddits you add the slower it will take if the app is caching before playing the video (usually the first run of the day).

If you're seeing the same videos over and over again and would like to refresh the cache run the app with the ```--force-rewrite-cache``` flag.

## 2.1 (optional | windows only)  Instructions to build standalone executable 
We would need to install the pyinstaller python package which lets us build an executable from a given python source.

Run ```pip3 install pyinstaller```

cd into the src directory and execute
```pyinstaller -w -F cheermeup.py```

The ```-w``` flag supresses terminal window and the ```-F``` makes pyinstaller procduces only one single executable file
You will find the newly built binary ```cheermeup.exe``` in the ```dist``` folder.



## 3. Improvements (help needed)

1. Please note that this is an alpha project I put together in a couple of hours and it might not exactly be stable all the time. Feel free to raise an issue and I'll try and look into it

2. I also want to release linux and macos binaries but pyinstaller and cx_freeze won't play well with cv2, which is a dependancy and I also don't have a mac to test this tool on. If anyone would like to help/contribute (in this regard or any other bugs you find) please issue a pull request.
