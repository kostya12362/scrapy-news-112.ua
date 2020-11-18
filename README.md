# scrapy-news-112.ua
parser for the site https://112.ua/
## Installation
first install the virtual environment
```bash
$ pip install virtualenv
```

The next step is to create a directory in which our folder will be in the environment
```bash
$ mkdir scrapy_spider && cd scrapy_spider
$ python3 -m venv venv
```
We activate the environment
```bash
$ source venv/bin/activate
```
We create a project
```bash
scrapy startproject news
cd news
```
```bash
scrapy genspider news112 112.ua
cd news/spiders
git clone https://github.com/kostya12362/scrapy-news-112.ua.git
cd /scrapy-news-112.ua
```
scrapy crawl news112 -o news.csv
