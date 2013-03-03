#-*- coding: utf-8 -*-

from pit import Pit
import mechanize
import re
import lxml.html

class KindleHighlight(object):
    def __init__(self, email, password, domain='jp'):
        self.br = mechanize.Browser()
        self.br.set_handle_robots(False)
        self.br.addheaders = [("User-agent", "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13")]
        if domain == 'jp':
            page = self.br.open("https://www.amazon.co.jp/ap/signin?openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fkindle.amazon.co.jp%3A443%2Fauthenticate%2Flogin_callback%3Fwctx%3D%252F&pageId=amzn_kindle&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.assoc_handle=amzn_kindle_jp&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0")
        else:
            page = self.br.open("https://www.amazon.com/ap/signin?openid.assoc_handle=amzn_kindle&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=0&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.return_to=https%3A%2F%2Fkindle.amazon.com%3A443%2Fauthenticate%2Flogin_callback%3Fwctx%3D%252F&pageId=amzn_kindle")

        page.set_data(re.sub('<!DOCTYPE(.*)>', '', page.get_data()))
        self.br.set_response(page)
        self.br.select_form(name = 'signIn')
        self.br['email'] = email
        self.br['password'] = password

        signedin_page = self.br.submit()
        self.scrape_highlights(signedin_page)

    def scrape_highlights(self, signedin_page):
        # follow link
        highlights_page = self.br.follow_link(url_regex='your_highlights')

        # scrape next book
        self.books2highlighs = dict(dict([]))        
        self.get_next_books(highlights_page)

    def get_next_books(self, page):
        dom = lxml.html.fromstring(page.read())

        # get title, author, highlights
        title = dom.xpath("//span[@class='title']/a")
        title = title[0].text.strip()

        hdic = {}
        author = dom.xpath("//span[@class='author']")
        hdic['author'] = author[0].text.strip()[3:]

        harray = []
        highlights = dom.xpath("//span[@class='highlight']")
        for h in highlights:
            harray.append(h.text)
        hdic['text'] = harray

        self.books2highlighs[title] = hdic

        # get next book
        next_book = dom.xpath("//a[@id='nextBookLink']")
        next_url = next_book[0].attrib['href']
        if not re.search('upcoming_asin', next_url):
            return
        else:
            next_page = self.br.follow_link(url=next_url)
            self.get_next_books(next_page)
        
def main():
    config = Pit.get('amazon.co.jp', {'require': {'email': 'email', 'password': 'password'}})

    domain = 'jp'
    kindle = KindleHighlight(config['email'], config['password'], domain)

    for k, v in kindle.books2highlighs.items():
        print '[title] %s' % k
        print '[author] %s' % v['author']
        for text in v['text']:
            print text
    
if __name__ == '__main__':
    main()
