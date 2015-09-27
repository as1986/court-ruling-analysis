#!/usr/bin/python
# -*- encoding: utf-8 -*-



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


    def query(self, term, court = u'SLD 臺灣士林地方法院'):
        self.payload['jmain1'] = term
        self.payload['jmain'] = term
        self.payload['v_court'] = court
        requested = self.__session.post('http://210.69.124.221/FJUD/FJUDQRY02_1.aspx', self.payload,
                                        headers={'referer':'http://jirs.judicial.gov.tw/FJUD/FJUDQRY01_1.aspx'})
        requested.encoding = 'utf-8'
        return requested.text



def main():
    terms = [u'賴素如', u'蔡正元']
    court = u'SLD 臺灣士林地方法院'
    c = Crawler()
    for t in terms:
        print u'term {}'.format(t)
        print c.query(t, court)


if __name__ == '__main__':
    main()