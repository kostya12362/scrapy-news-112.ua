# -*- coding: utf-8 -*-
import scrapy
import datetime
import re


class News112Spider(scrapy.Spider):
    name = 'news112'
    start_urls = []
    custom_settings = {
        'FEED_EXPORT_ENCODING': 'utf-8',
        'LOG_LEVEL': 'INFO'
    }
    headers = {
        'content-type': 'text/html; charset=UTF-8'
        }

    not_text = []
    text = []

    def __init__(self, *args, **kwargs):
        super(News112Spider, self).__init__(*args, **kwargs)
        page_start = input("Input start_page = ").strip()
        self.start_urls.append(f"https://112.ua/archive/p{page_start}")
        self.page_finish = input("Input finished page = ").strip()

    def parse(self, response, **kwargs):
        links = response.xpath('//li[@class="large-12 medium-12 '
                               'small-12 news-item one-column description"]//@href').extract()
        for link in links:
            post_url = response.urljoin(link)
            yield scrapy.Request(post_url, callback=self.publish)

        nextpage = response.xpath('//a[@rel="next"]/@href').extract_first()
        if int(re.findall(r'\d+', nextpage)[-1])-1 < int(self.page_finish):
            print('Парсит')
            yield scrapy.Request(response.urljoin(nextpage),
                                 callback=self.parse)

    def publish(self, response):
        date_published = response.xpath('//head/meta[@property="og:updated_time"]//attribute::content').extract()
        fb_id = response.xpath('//meta[@property="fb:app_id"]/@content').extract_first()
        url = f"https://www.facebook.com/v2.11/plugins/share_button.php?app_id={fb_id}&" \
              f"href={response.url}&layout=button_count&locale=ru_RU&sdk=joey"
        author_list = list(filter(lambda a: a != '\xa0', response.xpath(
            '//section[@class="page-cont list-content"]//strong//text()').extract()))
        author = 'NEWS_SITE_NAME'

        if response.xpath('//section[@class="page-cont list-content"]'
                          '//h2[contains(@style, "text-align: center;")]//text() |'
                          '//section[@class="page-cont list-content"]'
                          '//p[contains(@style, "text-align: center;")]//text()').extract() != [] \
                or ('/interview/' in response.url):
            author = 'NEWS_SITE_NAME'
        else:
            for i in author_list:
                if 'Перевод' in i:
                    author = author_list[-3]
                    break
                else:
                    author = author_list[-1]

        if response.xpath('//div[@class="article-content_text"]') != []:
            self.not_add = response.xpath(
                '//div[@class="article-content_text"]//*[script]//text() | '
                '//div[@class="article-content_text"]//style//text() | '
                '//div[@class="article-content_text"]//*[contains(@class, "article-img  align_justify")]//text() |'
                '//div[@class="article-content_text"]//*[contains(@class, "article_attached acenter")]//text() |'
                '//div[@class="article-content_text"]//*[contains(@class, "content-slider")]//text()').extract()
            self.text = response.xpath('//div[@class="article-content_text"]//text() |'
                                       '//div[@class="column auto p-a-clear"]/'
                                       'div[@class="playlist-main-video description"]'
                                       '/div[@class="v-descr"]//text()').extract()
        elif response.xpath('//section[@class="page-cont list-content"]') != []:
            self.not_add = response.xpath(
                '//section[@class="page-cont list-content"]//script//text() | '
                '//section[@class="page-cont list-content"]//style//text() | '
                '//section[@class="page-cont list-content"]//'
                '*[contains(@class, "article-img  align_justify width-full")]//text() |'
                '//section[@class="page-cont list-content"]//'
                '*[contains(@class, "row  align-spaced align-middle section-block-vert mob-hide clear-tags")]//text() |'
                '//section[@class="page-cont list-content"]//'
                '*[contains(@class, "article-img  align_justify width-full")]//text() |'
                '//section[@class="page-cont list-content"]//'
                '*[contains(@class, "article-attachment right r mob-hide")]//text() |'
                '//section[@class="page-cont list-content"]//'
                '*[(contains(text(), "blog@112.ua" ))]/..//text() |'
                '//section[@class="page-cont list-content"]//strong//text()').extract()
            self.text = response.xpath('//section[@class="page-cont list-content"]//text() |'
                                       '//div[@class="column auto p-a-clear"]'
                                       '/div[@class="playlist-main-video description"]'
                                       '/div[@class="v-descr"]//text()').extract()

        for string_not_add in self.not_add:
            for string_text in self.text:
                if string_not_add == string_text:
                    self.text.remove(string_text)
        text = re.sub(r'\s+', ' ', ''.join(self.text)).strip()

        try:
            category = response.xpath('//ul[@class="row align-middle"]/li/a/span/text()').extract()[-1]
        except:
            category = None

        data = {
            'title': response.xpath('//head/meta[@property="og:title"]//attribute::content').extract()[0],
            'text': text,
            'lang': response.xpath('//html/@lang').extract()[0],
            'link': response.url,
            'Category': category,
            'source': response.xpath('//div[@class="article-source"]/a[@class="source-link"]/text()').extract(),
            'shares': '',
            'author': author,
            'view': response.xpath('//div[@class="datetime align-justify align-middle"]/'
                                   'span[@class="count-view n-ch"]/text()').get(),
            'topic': None,
            'date_published': date_published,
            'date_parsed': datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
            'tags': [tag[1:] for tag in response.xpath('//div[@class="article-tags"]/a/text()').extract()],
            'image': response.xpath('//div[@class="article-content_text"]//img/@src | '
                                    '//section[@class="page-cont list-content"]'
                                    '//div[@class="article-img  align_justify width-full"]//@href '
                                    '//div[@class="end-video"]/div[@class="stick-wrap"]/'
                                    'div[@class="stick"]/video/@poster').extract()
        }
        yield scrapy.Request(url,
                             meta={'item_data': data},
                             callback=self.progress)


    def progress(self, response):
        data = response.meta['item_data']
        data['shares'] = response.xpath('//span[contains(text(), "Поделиться")]'
                                        '/following-sibling::span[1]/text()').extract_first()
        data['shares'] = None if data['shares'] == '0' else data['shares']
        print(data)
        yield data
