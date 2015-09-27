#!/usr/bin/python
# -*- encoding: utf-8 -*-

from bs4 import BeautifulSoup


class Crawler:

    def __init__(self):

        import requests
        self.__session = requests.Session()
        self.__session.get('http://210.69.124.221/FJUD/FJUDQRY01_1.aspx',
                           headers={'referer':'http://jirs.judicial.gov.tw/FJUD/FJUDQRY01_1.aspx'}
                           )

        self.payload = {'nccharset':'BB354331','v_court': '','v_sys':'M','jud_year': '',
                        'sel_judword':'常用字別', 'jud_case':'', 'jud_no':'', 'jud_no_end':'',
                        'jt':'', 'dy1':'', 'dm1':'', 'dd1':'', 'dy2':'', 'dm2':'', 'dd2':'', 'jmain1':'',
                        'kw':'', 'keyword':'', 'sdate':'', 'edate':'', 'jud_title':'', 'jmain':'',
                        'Button':'查詢', 'searchkw': '賴素如'
                        }
        self.prefix = 'http://210.69.124.221/FJUD/'


    def query(self, term, court = u'SLD 臺灣士林地方法院'):
        self.payload['jmain1'] = term
        self.payload['jmain'] = term
        self.payload['v_court'] = court
        requested = self.__session.post('http://210.69.124.221/FJUD/FJUDQRY02_1.aspx', self.payload,
                                        headers={'referer':'http://jirs.judicial.gov.tw/FJUD/FJUDQRY01_1.aspx'})
        requested.encoding = 'utf-8'
        return requested.text

    def get(self, page):
        results = self.__session.get(page, headers={'referer':'http://jirs.judicial.gov.tw/FJUD/FJUDQRY02_1.aspx'})
        ruling = BeautifulSoup(results.text)
        friendly = ruling.findAll('a', text='友善列印')[0]
        friendly_results = self.__session.get(self.prefix+friendly['href'],
                                              headers={'referer':'http://jirs.judicial.gov.tw/FJUD/FJUDQRY03_1.aspx'})
        friendly_results.encoding = 'utf-8'
        return friendly_results.text

    def cleanse(self, crawled):
        soup = BeautifulSoup(crawled)
        return soup('pre')[0].get_text()

    def get_links(self, query_results):
        to_return = []
        soup = BeautifulSoup(query_results)
        entries = soup.findAll("table", { "id" : "Table3" })
        # print entries
        for e in entries:
            links = e.findAll('a')
            # print links
            for l in links:
                cand = l['href']
                if cand is not None and cand is not '#':
                    to_return.append(self.prefix+cand)

        return to_return

def main():
    terms = [u'賴素如', u'蔡正元']
    court = u'SLD 臺灣士林地方法院'
    c = Crawler()
    for t in terms:
        print u'term {}'.format(t)
        q = c.query(t, court)
        links = c.get_links(q)
        for l in links:
            print c.cleanse(c.get(l))



if __name__ == '__main__':
    main()