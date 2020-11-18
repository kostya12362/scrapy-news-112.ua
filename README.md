# scrapy-news-112.ua

first install the virtual environment

$ pip install virtualenv
$ mkdir scrapy_spider && cd scrapy_spider
$ python3 -m venv venv

$ source venv/bin/activate
scrapy startproject news
cd news
scrapy genspider news112 112.ua
cd news/spiders
git clone https://github.com/kostya12362/scrapy-news-112.ua.git
cd /scrapy-news-112.ua
scrapy crawl news112 -o news.csv
