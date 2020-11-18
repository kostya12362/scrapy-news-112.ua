# scrapy-news-112.ua
parser for the site https://112.ua/
## Installation
first install the virtual environment
```bash
$ pip install virtualenv
```

The next step is to create a directory in which our folder will be in the environment
```linux
$ mkdir scrapy_spider && cd scrapy_spider
$ python3 -m venv venv
```
We activate the environment
```linux
$ source venv/bin/activate
```
We create a project
```linux
$ scrapy startproject news
$ cd news
```
```linux
$ scrapy genspider news112 112.ua
$ cd news/spiders
$ git clone https://github.com/kostya12362/scrapy-news-112.ua.git
$ cd /scrapy-news-112.ua
```
## Fix settings
In your settings.py file comment out
```python
ROBOTS TXT OBEY = True
```
## Run spider 
To start and save the file in csv, run
```linux
$ scrapy crawl news112 -o news.csv
```
