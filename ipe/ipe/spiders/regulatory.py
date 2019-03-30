# -*- coding: utf-8 -*-
import json
import re
import html

import binascii
import scrapy


class RegulatorySpider(scrapy.Spider):
    name = 'regulatory'
    allowed_domains = ['www.ipe.org.cn']
    url = 'http://www.ipe.org.cn/'
    start_url = 'http://www.ipe.org.cn/data_ashx/GetAirData.ashx'
    cookie = {'acw_tc': '7b39758215520138409462380e7a4b67d2903e854ba217a1ef28dbd7e4fa7e', '__utmz': '105455707.1552013845.1.1.utmcsr', '.ASPXAUTH': '40A0CFD58B1441002300306235BFB8DAB2FB59D2F48C392A723FB0B2EFB063C562455D4192F4BC5E4BCBBE418B5806C1F7576C71B245692587BAA97FCD0258F21418747B823E4CF65CA11C850860289C79580BD9019C457BEC180B24D565B20D596FDF494DD20190A8D4C60C02FBE6E51C16CBB55B0E8B0458C3AC20590163ED05C0599BB7E8DDF5D50188BE2B7F45046D047BF00BF57450DD00941FEFED26F80D1CC704', 'ASP.NET_SessionId': 'aev0dzcd4izuywjpqji54yop', 'ajaxkey': 'D8E181A537026674ABA67673D4664F799DEFA487DC07061A', '__utma': '105455707.1742238327.1552013845.1552612173.1552616192.16', '__utmc': '105455707', '__utmt': '1', '__utmb': '105455707.1.10.1552616192', 'SERVERID': '8abfb74b5c7dce7c6fa0fa50eb3d63af|1552616194|1552616189'}


    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http://www.ipe.org.cn/IndustryRecord/Regulatory.aspx'
    }
    body = 'cmd=getjdxjc&keycode=4543j9f9ri334233r3rixxxyyo12&pageSize=15&pageIndex=0&countryId=1&provinceId=-1&cityId=-1&professionId=-1&indusName=&index=1'

    # 获取页码
    def start_requests(self):
        yield scrapy.Request(url=self.start_url, headers=self.headers, body=self.body, cookies=self.cookie)

    def parse(self, response):
        # with open("./test.html", 'wb') as f:
        #     f.write(response.body)
        pages = re.findall(r'data-page="(\d*?)"', response.text)
        if not pages:
            print("ERROR: cookie expired.", flush=True)
            return
        total_pages = int(pages[-1])
        for i in range(1):
            page_body = 'cmd=getjdxjc&keycode=4543j9f9ri334233r3rixxxyyo12&pageSize=15&pageIndex=' \
                        + str(i + 1) + \
                        '&countryId=1&provinceId=-1&cityId=-1&professionId=-1&indusName=&index=1'
            yield scrapy.Request(url=self.start_url, headers=self.headers, body=page_body, cookies=self.cookie,
                                 callback=self.parse_page)

    def to_char(self, matched):
        return bytearray.fromhex(matched.group(1)).decode()

    def to_kanji(self, matched):
        return ("\\u" + matched.group(1)).encode("utf-8").decode("unicode_escape")

    def parse_page(self, response):
        current_page = re.search(r'"pager active" data-page="(\d*?)"', response.text).group(1)
        print("current page: " + current_page, flush=True)
        content = re.sub(r'%([^u].)', self.to_char, re.search(r"content:'(.*)'", response.text).group(1))
        content = re.sub(r'%u(....)', self.to_kanji, content)
        records = re.findall(r'<tr.*?</tr>', content, re.DOTALL)[:1]
        for record in records:
            id = re.search(r'self\(.*?,.*?,.*?,(\d*?)\)', record).group(1)
            count = re.search(r'<td>(\d*)</td><td class', record).group(1)
            company_name = re.search(r'title="(.*?)"', record).group(1)
            location = re.search(r'([\u4E00-\u9FA5]*) / <span class="text-prov">(.*?)</span>', content)
            location = location.group(2) + "," + location.group(1)



            table_body = 'cmd=getjdxjcinfo&keycode=4543j9f9ri334233r3rixxxyyo12&pointId=&zhibiao=&companyId=' \
                          + id +  \
                          '&startYear=-1&startMonth=-1&startDay=-1&endYear=-1&endMonth=-1&endDay=-1&hourPageIndex=0'

            yield scrapy.Request(url=self.start_url, headers=self.headers, cookies=self.cookie, body = table_body,
                                 callback=self.parse_table,
                                 meta={'count': count, 'id': id, 'company_name': company_name, 'location': location})

    def parse_table(self, response):
        print("current item: " + response.meta.get("count"), flush=True)
        content = re.sub(r'%([^u].)', self.to_char, re.search(r"tableContent:'(.*)'", response.text).group(1))
        content = re.sub(r'%u(....)', self.to_kanji, content)

        with open("./test.html", 'wb') as f:
            f.write(content.encode())

        return
