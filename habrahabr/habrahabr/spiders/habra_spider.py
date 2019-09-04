# -*- coding: utf-8 -*-
import scrapy

from ..items import HabrahabrItem

class HabraSpider (scrapy.Spider):
    name = 'habra'
    start_urls = [
        'https://habr.com/ru/all/',
        'https://habr.com/ru/all/page2/'
    ]

    def parse(self, response):
        all_posts = response.css('.post_preview')

        for post in all_posts:
            #meta = {'author': post.css('.user-info__nickname_small::text').extract()}
            meta = {'posts_link': post.css('h2.post__title a::attr(href)').extract()}
            post_link = post.css('h2.post__title a::attr(href)').extract_first()
            yield scrapy.Request(url=post_link, callback=self.parse_article, meta=meta)

    def parse_article(self, response):
        items = HabrahabrItem()
        post_link = response.meta['posts_link']
        title = response.css('.post__title-text::text').extract_first()
        author = response.css('.user-info__nickname_small::text').extract_first()
        #author2 = response.meta['author']
        tags = response.css('.post__tag::text').extract()
        similar_posts = response.css('.post-info__title_large .post-info__title_large::attr(href)').extract()

        items['title'] = title
        items['author'] = author
        items['post_link'] = post_link
        items['tags'] = tags
        items['similar_posts'] = similar_posts

        print (items)
        yield items