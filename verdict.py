#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'chucheng'

from io import open
import re


class Verdict:
    def __init__(self, html):
        self.__html = html
        self.__full = self.__rule()
        return

    def __rule(self):
        from bs4 import BeautifulSoup

        # extract ruling from html
        soup = BeautifulSoup(self.__html)
        output = soup.get_text()
        return output

    def full(self):
        return self.__full

    def body(self):
        s =''

    def lines(self):

        def num(l):
            pat = ur'【裁判字號】\s*(.*)'
            matches = re.match(pat,l)
            if matches is not None:
                self.__num = matches.groups()[0].encode('utf-8')
                return self.__num
            return None


        seperated = self.__full.split('\n')
        checks = [num]
        current_check = 0
        for idx, l in enumerate(seperated):
            if current_check >= len(checks):
                break
            # num
            g = checks[current_check](l)
            if g is not None:
                print g
                current_check += 1



if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', help='crawled friendly printing HTML')
    args = parser.parse_args()
    with open(args.infile, mode='r', encoding='utf-8') as fh:
        lines = fh.read()
        v = Verdict(lines)
        print v.lines()