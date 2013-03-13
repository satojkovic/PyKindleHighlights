#-*- coding: utf-8 -*-

import mechanize
import re
from pyquery import PyQuery as pq

class PyKindleHighlights(object):
    """
    scrape highlights from kindle.amazon.co.jp
    """
    def __init__(self, email, password):
        self.br = mechanize.Browser()
        self.br.set_handle_robots(False)
        self.br.addheaders = [("User-agent", "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13")]

        page = self.br.open("https://www.amazon.co.jp/ap/signin?openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fkindle.amazon.co.jp%3A443%2Fauthenticate%2Flogin_callback%3Fwctx%3D%252F&pageId=amzn_kindle&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.assoc_handle=amzn_kindle_jp&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")
        page.set_data(re.sub('<!DOCTYPE(.*)>', '', page.get_data()))
        self.br.set_response(page)

        self.br.select_form(name = 'signIn')
        self.br['email'] = email
        self.br['password'] = password

        # scrape kindle highlights
        self.scrape_highlights()

    def scrape_highlights(self):
        # sign in
        signedin_page = self.br.submit()

        # move to highlights page
        highlights_page = self.br.follow_link(url_regex='your_highlights')

        # get highlights recursively
        self.highlights = []
        self.get_next_highlights(highlights_page, self.highlights)

    def get_next_highlights(self, page, highlights):
        dom = pq(page.read())

        # get title, author, highlights
        highlights.append( self.Highlight(dom) )

        # get next book
        next_book = dom("a#nextBookLink")
        next_url = next_book[0].attrib['href']
        if not re.search('upcoming_asin', next_url):
            return
        else:
            next_page = self.br.follow_link(url=next_url)
            self.get_next_highlights(next_page, highlights)

    class Highlight:
        def __init__(self, dom):
            self.text = []
            for h in dom("span.highlight"):
                self.text.append(h.text)
            self.title = dom("span.title>a")[0].text.strip()
            self.author = dom("span.author")[0].text.strip()[3:]

