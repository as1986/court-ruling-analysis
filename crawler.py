#!/usr/bin/python
# -*- encoding: utf-8 -*-

from bs4 import BeautifulSoup
import logging


class Crawler:
    def __init__(self):

        import requests
        logging.basicConfig(filename='crawler.log', level=logging.WARNING)
        self.__session = requests.Session()
        self.__session.get('http://210.69.124.221/FJUD/FJUDQRY01_1.aspx',
                           headers={'referer': 'http://jirs.judicial.gov.tw/FJUD/FJUDQRY01_1.aspx'}
                           )

        self.payload = {'nccharset': 'BB354331', 'v_court': '', 'v_sys': 'M', 'jud_year': '',
                        'sel_judword': '常用字別', 'jud_case': '', 'jud_no': '', 'jud_no_end': '',
                        'jt': '', 'dy1': '', 'dm1': '', 'dd1': '', 'dy2': '', 'dm2': '', 'dd2': '', 'jmain1': '',
                        'kw': '', 'keyword': '', 'sdate': '', 'edate': '', 'jud_title': '', 'jmain': '',
                        'Button': '查詢', 'searchkw': '賴素如'
                        }
        self.prefix = 'http://210.69.124.221/FJUD/'

    def query(self, term, court=u'SLD 臺灣士林地方法院'):
        self.payload['jmain1'] = term
        self.payload['jmain'] = term
        self.payload['v_court'] = court
        for _ in xrange(3):
            try:
                requested = self.__session.post('http://210.69.124.221/FJUD/FJUDQRY02_1.aspx', self.payload,
                                                headers={'referer': 'http://jirs.judicial.gov.tw/FJUD/FJUDQRY01_1.aspx'})
                break
            except Exception as e:
                logging.warning('post failed: {}'.format(e))

        requested.encoding = 'utf-8'
        return requested.text

    def get(self, page):
        results = self.__session.get(page, headers={'referer': 'http://jirs.judicial.gov.tw/FJUD/FJUDQRY02_1.aspx'})
        ruling = BeautifulSoup(results.text)
        friendly = ruling.findAll('a', text='友善列印')[0]
        friendly_results = self.__session.get(self.prefix + friendly['href'],
                                              headers={'referer': 'http://jirs.judicial.gov.tw/FJUD/FJUDQRY03_1.aspx'})
        friendly_results.encoding = 'utf-8'
        return friendly_results.text

    def cleanse(self, crawled):
        soup = BeautifulSoup(crawled)
        return soup('form')[0].get_text()

    def get_links(self, query_results):
        to_return = []
        soup = BeautifulSoup(query_results)
        entries = soup.findAll("table", {"id": "Table3"})
        # print entries
        for e in entries:
            links = e.findAll('a')
            # print links
            for l in links:
                cand = l['href']
                if cand is not None and cand is not '#':
                    to_return.append(self.prefix + cand)

        # check if page has next page
        next_page = soup.findAll('a', href=True, text='下一頁')
        if len(next_page) > 0:
            # follow up
            follow_up_page = self.prefix + next_page[0]['href']
            follow_up_results = self.__session.get(follow_up_page,
                                                   headers={
                                                       'referer': 'http://jirs.judicial.gov.tw/FJUD/FJUDQRY02_1.aspx'
                                                   }
                                                   )
            to_return.extend(self.get_links(follow_up_results.text))

        return to_return


class LawmakerList:
    def __init__(self, fname):
        import csv
        from io import open
        with open(fname, mode='r', encoding='utf-8') as fh:
            raw_rows = [x.encode('utf-8') for x in fh]
            reader = csv.reader(raw_rows)
            self.rows = []
            for r in reader:
                self.rows.append(r)

    def next(self):
        for idx, row in enumerate(self.rows):
            yield idx, row


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--from-idx', default=1, type=int)
    args = parser.parse_args()
    lst = LawmakerList('/Users/as1986/Downloads/list_utf8.csv')

    courts = ["TPD 臺灣臺北地方法院", "SLD 臺灣士林地方法院", "PCD 臺灣新北地方法院", "ILD 臺灣宜蘭地方法院", "KLD 臺灣基隆地方法院", "TYD 臺灣桃園地方法院",
              "SCD 臺灣新竹地方法院", "MLD 臺灣苗栗地方法院", "TCD 臺灣臺中地方法院", "CHD 臺灣彰化地方法院", "NTD 臺灣南投地方法院", "ULD 臺灣雲林地方法院",
              "CYD 臺灣嘉義地方法院", "TND 臺灣臺南地方法院", "KSD 臺灣高雄地方法院", "HLD 臺灣花蓮地方法院", "TTD 臺灣臺東地方法院", "PTD 臺灣屏東地方法院",
              "PHD 臺灣澎湖地方法院", "KMD 福建金門地方法院", "LCD 福建連江地方法院"]
    c = Crawler()

    for idx, r in lst.next():
        if idx < args.from_idx:
            continue
        t = r[0]
        print 'term {}'.format(t)
        for court in courts:
            court_abbr = court.split()[0]
            q = c.query(t, court)
            links = c.get_links(q)
            for l_idx, l in enumerate(links):
                # print l
                full_text = c.cleanse(c.get(l))
                from io import open
                with open('rulings/{}_{}_{}_{}'.format(idx, t, court_abbr, l_idx), mode='w', encoding='utf-8') as fh:
                    fh.write(full_text)
                import time
                time.sleep(.3)


if __name__ == '__main__':
    main()
