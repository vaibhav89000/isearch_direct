import scrapy
import time
import os
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import re
from ..items import SearchdetailItem

class SearchSpider(scrapy.Spider):
    name = 'search'

    website_name = []
    website_type = []
    duplicate = []
    country = ''
    keyword = ''
    city = ''

    def start_requests(self):
        index = 0
        yield SeleniumRequest(
            url="https://www.google.com/",
            wait_time=1000,
            screenshot=True,
            callback=self.parse,
            meta={'index': index},
            dont_filter=True
        )

    def parse(self, response):

        driver = response.meta['driver']
        index = response.meta['index']

        firstinput = os.path.abspath(os.curdir) + "\country.txt"
        f = open(firstinput, "r")
        country_name = f.read().splitlines()

        secondinput = os.path.abspath(os.curdir) + "\keyword.txt"
        f = open(secondinput, "r")
        keyword_name = f.read().splitlines()

        thirdinput = os.path.abspath(os.curdir) + "\city.txt"
        f = open(thirdinput, "r")
        city_name = f.read().splitlines()




        self.website_type.clear()
        self.website_name.clear()
        self.duplicate.clear()
        self.country = ''
        self.keyword = ''
        self.city = ''

        length = len(country_name)
        print("\n" * 2)
        print(index, length)
        print("\n" * 2)

        if (index < length):
            print("\n" * 2)
            print('passed values')
            print("\n" * 2)

            driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input').clear()
            search_input2 = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
            search_input2.send_keys(keyword_name[index])

            time.sleep(3)
            search_button = driver.find_element_by_xpath(
                '//*[@id="tsf"]/div[2]/div[1]/div[2]/div[2]/div[2]/center/input[1]')
            search_button.click()
            time.sleep(4)


            driver = response.meta['driver']
            self.country = country_name[index]
            self.keyword = keyword_name[index]
            self.city = city_name[index]
            index += 1

            print('\n' * 2)
            print('Above yield to parse_page',driver.current_url)
            print('\n' * 2)
            yield SeleniumRequest(
                url=driver.current_url,
                wait_time=1000,
                screenshot=True,
                callback=self.parse_page,
                errback=self.errback_parse_page,
                meta={'index': index},
                dont_filter=True
            )

    def parse_page(self, response):
        Searchdetails_item = SearchdetailItem()
        driver = response.meta['driver']
        index = response.meta['index']

        if (response.url == 'https://www.google.com/'):
            finalemail = response.meta['finalemail']
            web_name = response.meta['web_name']
            web_type = response.meta['web_type']
            Searchdetails_item['url'] = web_name
            Searchdetails_item['email'] = '-'
            Searchdetails_item['country'] = self.country
            Searchdetails_item['keyword'] = self.keyword
            Searchdetails_item['city'] = self.city
            Searchdetails_item['type'] = web_type

            if (len(finalemail) == 0):
                yield Searchdetails_item
            else:
                if (len(finalemail) < 5):
                    length = len(finalemail)
                else:
                    length = 5
                for i in range(0, length):
                    Searchdetails_item['email'] = finalemail[i]
                    yield Searchdetails_item

        else:
            print('\n' * 2)
            print(driver.current_url)
            print('\n' * 2)
            # time.sleep(8)

            try:
                WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located((By.ID, "tvcap"))
                )
            except:
                print('\n' * 2)
                print('tvcap except', driver.current_url)
                print('\n' * 2)

            details = response.xpath('//div[@id="tvcap"]/div/div/ol/li/div[1]')

            for detail in details:

                name = detail.xpath('.//div/div/div[1]/w-visurl/div/span[2]/text()').get()
                if (name == None):
                    print('\n' * 2)
                    print('gone for second xpath')
                    print('\n' * 2)
                    name = detail.xpath('.//div/cite/text()').get()
                print('\n' * 2)
                print('name', name)
                print('\n' * 2)
                if (name != None):
                    name_list = name.split('/')
                    if ('http://' not in name_list[0]):
                        name_added = 'http://' + name_list[0]
                    if (name_added not in self.duplicate and 'www.' in name_added):
                        self.duplicate.append(name_added)
                        self.website_name.append(name_added)
                        self.website_type.append('organic')

            print('\n' * 2)
            print(self.website_name)
            print('\n' * 2)

            details = response.xpath('//div[@id="bottomads"]/div/div/ol/li/div[1]')

            for detail in details:

                name = detail.xpath('.//div/div/div[1]/w-visurl/div/span[2]/text()').get()
                if (name == None):
                    print('\n' * 2)
                    print('gone for second xpath')
                    print('\n' * 2)
                    name = detail.xpath('.//div/cite/text()').get()
                print('\n' * 2)
                print('name', name)
                print('\n' * 2)
                if (name != None):
                    name_list = name.split('/')
                    if ('http://' not in name_list[0]):
                        name_added = 'http://' + name_list[0]
                    if (name_added not in self.duplicate and 'www.' in name_added):
                        self.duplicate.append(name_added)
                        self.website_name.append(name_added)
                        self.website_type.append('organic')

            print('\n' * 2)
            print(self.website_name)
            print('\n' * 2)

            print('\n' * 2)
            print('check wait')
            print('\n' * 2)

            try:
                WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "i0vbXd"))
                )
            except:
                print('\n' * 2)
                print('i0vbXd except', driver.current_url)
                print('\n' * 2)

            time.sleep(3)
            # url=response.xpath('//*[@id="rso"]/div[1]/div/div[2]/div/div[4]/div[3]/div/div/a/@href').get()
            # print('\n' * 2)
            # print('url',url)
            # print('\n' * 2)
            # next_url = 'https://www.google.com'+ url
            # click_ads = driver.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div[2]/div/div[4]/div[3]/div/div/a/div/span')
            # click_ads.click()
            #
            # WebDriverWait(driver, 1000).until(
            #     EC.presence_of_element_located((By.CLASS_NAME, "section-result-title"))
            # )
            #
            # driver=response.meta['driver']
            print('\n' * 2)
            print('check xpath')
            print('\n' * 2)

            # click_moreads=driver.find_element_by_xpath('//*[@id="rso"]/div/div/div[2]/div/div[4]/div[3]/div/div/a/div/span')
            try:
                click_moreads = driver.find_element_by_xpath(
                    '//*[@id="rso"]/div/div/div/div/div/div/div/div/a/div/span[contains(text(),"More")]')
                click_moreads.click()
            except:
                print('\n' * 2)
                print('rso except', driver.current_url)
                print('\n' * 2)

            driver = response.meta['driver']
            print('\n' * 2)
            print(driver.current_url)
            print('\n' * 2)

            time.sleep(4)
            html = driver.page_source
            response_obj = Selector(text=html)

            # search_button = driver.find_element_by_xpath('(//span[@class="VqFMTc p8AiDd"])[2]')
            # search_button.click()
            # time.sleep(3)
            details = response_obj.xpath('//span[@class="VqFMTc p8AiDd"]')
            print(len(details))
            # print('\n' * 3)
            for idx in range(1, len(details) + 1):

                search_ads = driver.find_element_by_xpath("(//span[@class='VqFMTc p8AiDd'])[{}]".format(idx))
                search_ads.click()
                time.sleep(3)
                html = driver.page_source
                response_obj = Selector(text=html)
                name = response_obj.xpath('//a[@class="CL9Uqc ab_button" ][contains(text(),"Website")]/@href').get()
                print('\n' * 2)
                print('name', name)
                print('\n' * 2)
                # name_list = name.split('/')
                if (name != None):
                    if ('http://' in name or 'https://' in name):
                        pass
                    else:
                        name = 'http://' + name

                    if (name not in self.duplicate and 'www.' in name):
                        self.duplicate.append(name)
                        self.website_name.append(name)
                        self.website_type.append('map')


            print('\n' * 2)
            print(self.website_name)
            print(self.website_type)
            print('\n' * 2)

        if (len(self.website_type) != 0):
            web_url = self.website_name[0]
            web_type = self.website_type[0]
            self.website_name.pop(0)
            self.website_type.pop(0)
            print('\n' * 2)
            print('ready to emailtrack')
            print(web_url)
            print(web_type)
            print('\n' * 2)
            yield SeleniumRequest(
                url=web_url,
                wait_time=1000,
                screenshot=True,
                callback=self.emailtrack,
                errback=self.emailtrack_errback,
                meta={'index': index, 'web_name': web_url, 'web_type': web_type},
                dont_filter=True
            )
        else:
            print('\n' * 2)
            print('back to isearch')
            print('\n' * 2)
            yield SeleniumRequest(
                url='https://www.google.com/',
                wait_time=1000,
                screenshot=True,
                callback=self.parse,
                errback=self.parse_errback,
                meta={'index': index},
                dont_filter=True
            )

    def emailtrack(self, response):
        driver = response.meta['driver']
        index = response.meta['index']
        web_name = response.meta['web_name']
        web_type = response.meta['web_type']

        html = driver.page_source
        response_obj = Selector(text=html)

        links = LxmlLinkExtractor(allow=()).extract_links(response)
        Finallinks = [str(link.url) for link in links]
        links = []
        for link in Finallinks:
            if (
                    'Contact' in link or 'contact' in link or 'About' in link or 'about' in link or 'CONTACT' in link or 'ABOUT' in link):
                links.append(link)

        links.append(str(response.url))

        if (len(links) > 0):
            l = links[0]
            links.pop(0)
            uniqueemail = set()

            yield SeleniumRequest(
                url=l,
                wait_time=1000,
                screenshot=True,
                callback=self.finalemail,
                errback=self.errback_finalemail,
                meta={'index': index, 'web_name': web_name, 'web_type': web_type, 'uniqueemail': uniqueemail,
                      'links': links},
                dont_filter=True
            )
        else:
            finalemail = []
            yield SeleniumRequest(
                url='https://www.google.com/',
                wait_time=1000,
                screenshot=True,
                callback=self.parse_page,
                errback=self.errback_google,
                meta={'index': index, 'web_name': web_name, 'web_type': web_type, 'finalemail': finalemail,
                      'links': links},
                dont_filter=True
            )

    def finalemail(self, response):
        links = response.meta['links']
        driver = response.meta['driver']
        html = driver.page_source
        response_obj = Selector(text=html)
        index = response.meta['index']
        web_name = response.meta['web_name']
        web_type = response.meta['web_type']
        links = response.meta['links']

        uniqueemail = response.meta['uniqueemail']

        flag = 0
        bad_words = ['facebook', 'instagram', 'youtube', 'twitter', 'wiki', 'linkedin']
        for word in bad_words:
            if word in str(response.url):
                # return
                flag = 1
        if (flag != 1):
            html_text = str(response.text)
            mail_list = re.findall('\w+@\w+\.{1}\w+', html_text)
            #
            mail_list = set(mail_list)
            if (len(mail_list) != 0):
                for i in mail_list:
                    mail_list = i
                    if (mail_list not in uniqueemail):
                        uniqueemail.add(mail_list)
                        print('\n' * 2)
                        print(uniqueemail)
                        print('\n' * 2)
            else:
                pass

        if (len(links) > 0 and len(uniqueemail) < 5):
            print('\n' * 2)
            print('hi', len(links))
            print('\n' * 2)
            l = links[0]
            links.pop(0)
            yield SeleniumRequest(
                url=l,
                wait_time=1000,
                screenshot=True,
                callback=self.finalemail,
                errback=self.errback_finalemail,
                dont_filter=True,
                meta={'web_name': web_name, 'web_type': web_type, 'uniqueemail': uniqueemail, 'links': links,
                      'index': index}

            )
        else:
            print('\n' * 2)
            print('hello')
            print('\n' * 2)
            emails = list(uniqueemail)
            finalemail = []
            discard = ['robert@broofa.com']
            for email in emails:
                if ('.in' in email or '.com' in email or 'info' in email or '.org' in email):
                    for dis in discard:
                        if (dis not in email):
                            finalemail.append(email)
            print('\n' * 2)
            print('final', finalemail)
            print('\n' * 2)
            yield SeleniumRequest(
                url='https://www.google.com/',
                wait_time=1000,
                screenshot=True,
                callback=self.parse_page,
                errback=self.errback_google,
                dont_filter=True,
                meta={'web_name': web_name, 'web_type': web_type, 'links': links, 'finalemail': finalemail,
                      'index': index}

            )

    def emailtrack_errback(self, failure):
        meta = failure.request.meta
        web_name = meta['web_name']
        web_type = meta['web_type']
        index = meta['index']

        yield SeleniumRequest(
            url='https://www.google.com/',
            wait_time=1000,
            screenshot=True,
            callback=self.parse_page,
            errback=self.errback_google,
            meta={'index': index, 'web_name': web_name, 'web_type': web_type},
            dont_filter=True
        )

    def parse_errback(self, failure):
        meta = failure.request.meta

        yield SeleniumRequest(
            url='https://www.google.com/',
            wait_time=1000,
            screenshot=True,
            callback=self.parse,
            errback=self.parse_errback,
            meta=meta,
            dont_filter=True
        )

    def errback_finalemail(self, failure):
        meta = failure.request.meta
        links = meta['links']
        uniqueemail = meta['uniqueemail']
        if (len(links) > 0):
            l = links[0]
            links.pop(0)
            yield SeleniumRequest(
                url=l,
                wait_time=1000,
                screenshot=True,
                callback=self.finalemail,
                errback=self.errback_finalemail,
                dont_filter=True,
                meta=meta
            )
        else:
            print('\n' * 2)
            print('hello')
            print('\n' * 2)
            emails = list(uniqueemail)
            finalemail = []
            discard = ['robert@broofa.com']
            for email in emails:
                if ('.in' in email or '.com' in email or 'info' in email or '.org' in email):
                    for dis in discard:
                        if (dis not in email):
                            finalemail.append(email)
            print('\n' * 2)
            print('final', finalemail)
            print('\n' * 2)
            yield SeleniumRequest(
                url='https://www.google.com/',
                wait_time=1000,
                screenshot=True,
                callback=self.parse_page,
                errback=self.errback_google,
                dont_filter=True,
                meta=meta

            )

    def errback_parse_page(self, failure):
        meta = failure.request.meta
        index = meta['index']

        yield SeleniumRequest(
            url='https://www.google.com/',
            wait_time=1000,
            screenshot=True,
            callback=self.parse,
            errback=self.parse_errback,
            meta={'index': index},
            dont_filter=True
        )

    def errback_google(self, failure):
        meta = failure.request.meta

        yield SeleniumRequest(
            url='https://www.google.com/',
            wait_time=1000,
            screenshot=True,
            callback=self.parse_page,
            errback=self.errback_google,
            meta=meta,
            dont_filter=True
        )


